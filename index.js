/**
 * Host 插件：napcat-tools。
 *
 * 把 NapCat 的 OneBot 11 API 暴露成两个模型工具：
 *   - napcat_call：调用任意官方 action（文档里的 204 个）
 *   - napcat_send：常用发消息快捷方式（群/私聊，文本+媒体+引用+@）
 *
 * 两个工具都只是拼 argv，交给 D:\DSH_WorkArea 下的 Python 包 napcat_api 执行，
 * 这样 QQQ 操作的全部协议细节仍留在一处可独立测试的 Python 代码里。
 */
import { runCli } from './lib/runner.mjs';

export const name = 'napcat-tools';

/** 注册工具需要 tools 服务，运行 Python 需要 subprocess 服务。 */
export const inject = ['tools', 'subprocess'];

const TAG = '[napcat-tools]';

const DEFAULTS = {
  cwd: 'D:\\DSH_WorkArea',
  python: '',
  pythonPath: '',
  timeoutMs: 120000,
};

function text(value) {
  return [{ type: 'text', text: value }];
}

function renderJson(_args, value) {
  return text(JSON.stringify(value, null, 2));
}

function presentCall(args) {
  return {
    card: 'generic',
    title: `NapCat ${args.action}`,
    rawInput: args,
  };
}

export function apply(ctx, pluginConfig = {}) {
  const logger = ctx.logger ?? console;
  const log = (level, message) => {
    try {
      const method = typeof logger?.[level] === 'function' ? logger[level] : console[level];
      (method ?? console.log).call(logger, `${TAG} ${message}`);
    } catch {
      /* 日志失败不影响工具 */
    }
  };

  const options = { ...DEFAULTS, ...(pluginConfig !== null && typeof pluginConfig === 'object' ? pluginConfig : {}) };
  if (options.enabled === false) {
    log('info', '已在插件配置中禁用');
    return;
  }
  log('info', `已启用，cwd=${options.cwd}，python=${options.python || '自动查找'}`);

  const run = (argv, exec) => runCli(ctx, options, argv, exec?.signal);

  ctx.effect(
    () =>
      ctx.tools.register({
        name: 'napcat_call',
        description:
          '调用 NapCat/OneBot 11 官方 API 的任意 action（当前文档 204 个）。' +
          'action 名见 NapCat 官方文档，如 get_login_info、get_group_list、send_group_msg、set_group_ban、upload_group_file；' +
          'params 是该 action 的 JSON 参数对象，会原样传给 NapCat HTTP 接口。' +
          '需要先知道参数结构时可先调用 action=get_version_info 或查看本地文档；未知 action 也可直接尝试。',
        parameters: {
          type: 'object',
          additionalProperties: false,
          properties: {
            action: {
              type: 'string',
              description: '官方 action 名，例如 get_login_info / send_group_msg / get_group_list',
            },
            params: {
              type: 'object',
              additionalProperties: true,
              description: '传给该 action 的 JSON 参数对象；没有参数可省略',
            },
            force: {
              type: 'boolean',
              description: '参数不在官方文档里时仍强制发送（默认 false）',
            },
          },
          required: ['action'],
        },
        output: {
          schema: {
            type: 'object',
            additionalProperties: false,
            properties: {
              ok: { type: 'boolean' },
              action: { type: 'string' },
              data: {},
            },
            required: ['ok'],
          },
          render: renderJson,
        },
        presentCall,
        async execute(args, exec) {
          const action = String(args.action ?? '').trim();
          if (action === '') throw new Error('action 不能为空');
          const params = args.params ?? {};
          if (params === null || typeof params !== 'object' || Array.isArray(params)) {
            throw new Error('params 必须是 JSON 对象');
          }
          const argv = ['call', action, '--params', JSON.stringify(params)];
          if (args.force === true) argv.push('--force');
          const data = await run(argv, exec);
          return { ok: true, action, data };
        },
      }),
    'napcat-call',
  );

  ctx.effect(
    () =>
      ctx.tools.register({
        name: 'napcat_send',
        description:
          '向 QQ 群或私聊发消息（NapCat send_group_msg / send_private_msg 的快捷封装）。' +
          'target 写 group:群号 或 user:QQ号；文本、图片、文件、语音、视频、@、引用可任意组合。' +
          '本地图片/文件路径会由 Python 侧读取并转成 base64；也可以直接给 http(s) 或 base64:// 地址。' +
          '只发文本时优先用 napcat_send，复杂 action 用 napcat_call。',
        parameters: {
          type: 'object',
          additionalProperties: false,
          properties: {
            target: {
              type: 'string',
              description: '发送目标：group:123456（群）或 user:123456（私聊）',
            },
            text: { type: 'string', description: '文本内容' },
            images: {
              type: 'array',
              items: { type: 'string' },
              description: '图片：本地路径、http(s) URL 或 base64://',
            },
            files: {
              type: 'array',
              items: { type: 'string' },
              description: '文件：本地路径、http(s) URL 或 base64://',
            },
            at: {
              type: 'array',
              items: { type: 'string' },
              description: '要 @ 的 QQ 号列表；all 表示全体成员',
            },
            reply: { type: 'string', description: '引用消息的 message_id' },
            record: { type: 'string', description: '语音：本地路径、URL 或 base64://' },
            video: { type: 'string', description: '视频：本地路径、URL 或 base64://' },
            face: {
              type: 'array',
              items: { type: 'string' },
              description: 'QQ 表情 id 列表',
            },
            markdown: { type: 'string', description: 'Markdown 内容（NapCat 支持的场景）' },
            jsonCard: { type: 'string', description: 'JSON 卡片内容（JSON 字符串）' },
            dryRun: { type: 'boolean', description: '只构造请求并返回，不真正发送' },
          },
          required: ['target'],
        },
        output: {
          schema: {
            type: 'object',
            additionalProperties: false,
            properties: {
              ok: { type: 'boolean' },
              action: { type: 'string' },
              data: {},
              dryRun: { type: 'boolean' },
            },
            required: ['ok'],
          },
          render: renderJson,
        },
        presentCall: (args) => ({
          card: 'generic',
          title: `NapCat 发送 -> ${args.target ?? ''}`,
          rawInput: args,
        }),
        async execute(args, exec) {
          const target = String(args.target ?? '').trim();
          const matched = /^(group|g|private|user|u|p)\s*[:/]\s*(\d+)$/i.exec(target);
          if (matched === null) {
            throw new Error('target 需要写成 group:123456 或 user:123456');
          }
          const isGroup = /^(group|g)$/i.test(matched[1]);
          const argv = ['send', isGroup ? '-g' : '-u', matched[2]];

          if (typeof args.text === 'string' && args.text !== '') argv.push('--text', args.text);
          for (const value of args.images ?? []) argv.push('--image', String(value));
          for (const value of args.files ?? []) argv.push('--file', String(value));
          for (const value of args.at ?? []) argv.push('--at', String(value));
          for (const value of args.face ?? []) argv.push('--face', String(value));
          if (args.reply !== undefined && args.reply !== null) argv.push('--reply', String(args.reply));
          if (typeof args.record === 'string' && args.record !== '') argv.push('--record', args.record);
          if (typeof args.video === 'string' && args.video !== '') argv.push('--video', args.video);
          if (typeof args.markdown === 'string' && args.markdown !== '') argv.push('--markdown', args.markdown);
          if (typeof args.jsonCard === 'string' && args.jsonCard !== '') argv.push('--json-card', args.jsonCard);
          if (args.dryRun === true) argv.push('--dry-run');

          const data = await run(argv, exec);
          return {
            ok: true,
            action: isGroup ? 'send_group_msg' : 'send_private_msg',
            ...(args.dryRun === true ? { dryRun: true } : {}),
            data,
          };
        },
      }),
    'napcat-send',
  );
}
