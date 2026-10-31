"""NapCat OneBot 11 的 Python 封装。

快速使用：
    from napcat_api import NapCatClient, text, image

    client = NapCatClient()
    client.send_group(123456, [text("你好"), image("D:/pics/a.png")])
    client.call("get_group_list")
"""

from . import segments, spec
from .client import NapCatClient, NapCatError, call
from .segments import at, at_all, face, file, image, json_card, markdown, node, record, reply, text, video
from .spec import action_names, get_action, spec_version

__version__ = "1.0.0"
__all__ = [
    "NapCatClient",
    "NapCatError",
    "call",
    "action_names",
    "get_action",
    "spec_version",
    "segments",
    "spec",
    "text",
    "at",
    "at_all",
    "reply",
    "face",
    "image",
    "record",
    "video",
    "file",
    "json_card",
    "markdown",
    "node",
]
