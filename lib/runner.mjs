/**
 * 调本地 Python CLI：python -m napcat_api <args> --json。
 *
 * 只负责进程与 JSON 解析；错误统一抛 CliError，让工具层转成模型可读的失败。
 */

export class CliError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = 'CliError';
    this.exitCode = details.exitCode;
    this.stdout = details.stdout ?? '';
    this.stderr = details.stderr ?? '';
    this.spillPath = details.spillPath;
  }
}

function tail(text, limit = 4000) {
  const value = String(text ?? '');
  return value.length > limit ? `…（前 ${value.length - limit} 字符省略）\n${value.slice(-limit)}` : value;
}

async function resolvePython(ctx, options) {
  const candidates = [];
  if (typeof options.python === 'string' && options.python.trim() !== '') {
    candidates.push(options.python.trim());
  } else {
    candidates.push('python', 'py');
  }

  const failures = [];
  for (const candidate of candidates) {
    try {
      return await ctx.subprocess.resolveExecutable(candidate);
    } catch (error) {
      failures.push(`${candidate}: ${error?.message ?? error}`);
    }
  }
  throw new CliError(
    `找不到可用的 Python 解释器（${failures.join('；')}）。请在插件配置里设置 python 为绝对路径。`,
  );
}

/**
 * 运行一次 CLI。
 *
 * @param ctx 插件上下文（需要 subprocess 服务）
 * @param options {cwd, python, timeoutMs}
 * @param argv 传给 napcat_api 的参数（不含解释器与 --json）
 * @param signal 工具调用方的取消信号
 * @returns 解析后的 JSON 值
 */
export async function runCli(ctx, options, argv, signal) {
  const cwd = options.cwd;
  if (typeof cwd !== 'string' || cwd.trim() === '') {
    throw new CliError('插件配置缺少 cwd（napcat_api 包所在目录）');
  }

  const exe = await resolvePython(ctx, options);
  const env = {
    PYTHONUTF8: '1',
    PYTHONIOENCODING: 'utf-8',
  };
  if (typeof options.pythonPath === 'string' && options.pythonPath.trim() !== '') {
    env.PYTHONPATH = options.pythonPath;
  }

  const controller = new AbortController();
  const forwardAbort = () => controller.abort();
  if (signal !== undefined) {
    if (signal.aborted) controller.abort();
    else signal.addEventListener('abort', forwardAbort, { once: true });
  }
  const timeoutMs = Number(options.timeoutMs) > 0 ? Number(options.timeoutMs) : 120000;
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  timer.unref?.();

  let handle;
  try {
    handle = ctx.subprocess.spawn({
      argv: [exe, '-m', 'napcat_api', ...argv, '--json'],
      cwd,
      env,
      stdio: {
        stdin: 'ignore',
        stdout: { maxBytes: 8 * 1024 * 1024, spill: { maxBytes: 64 * 1024 * 1024 } },
        stderr: { maxBytes: 1024 * 1024, spill: { maxBytes: 8 * 1024 * 1024 } },
      },
      graceMs: 3000,
      signal: controller.signal,
    });
  } catch (error) {
    clearTimeout(timer);
    signal?.removeEventListener?.('abort', forwardAbort);
    throw new CliError(`启动 Python 失败：${error?.message ?? error}`);
  }

  let outcome;
  try {
    outcome = await handle.done;
  } catch (error) {
    clearTimeout(timer);
    signal?.removeEventListener?.('abort', forwardAbort);
    throw new CliError(`Python 进程失败：${error?.message ?? error}`);
  } finally {
    clearTimeout(timer);
    signal?.removeEventListener?.('abort', forwardAbort);
  }

  const stdout = handle.collected.stdout ? handle.collected.stdout.readFrom(0) : { text: '', truncated: false };
  const stderr = handle.collected.stderr ? handle.collected.stderr.readFrom(0) : { text: '', truncated: false };
  const outText = stdout.text ?? '';
  const errText = stderr.text ?? '';

  if (controller.signal.aborted) {
    throw new CliError(`调用超时（${timeoutMs}ms）或已取消`, {
      exitCode: outcome.exitCode ?? undefined,
      stdout: outText,
      stderr: errText,
      spillPath: stdout.spillPath ?? stderr.spillPath,
    });
  }

  if (outcome.exitCode !== 0) {
    throw new CliError(
      `napcat_api 退出码 ${outcome.exitCode}：${tail(errText || outText) || '无输出'}`,
      {
        exitCode: outcome.exitCode ?? undefined,
        stdout: outText,
        stderr: errText,
        spillPath: stdout.spillPath ?? stderr.spillPath,
      },
    );
  }

  try {
    return JSON.parse(outText);
  } catch (error) {
    throw new CliError(`napcat_api 输出不是 JSON：${tail(outText) || error?.message || '空输出'}`, {
      exitCode: outcome.exitCode ?? undefined,
      stdout: outText,
      stderr: errText,
      spillPath: stdout.spillPath,
    });
  }
}
