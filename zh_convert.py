"""
OpenCC 中文转换节点（字幕用）

用途：whisper 转中文字幕时常输出繁体，用本节点在写入 SRT 之前转成简体。
输入类型与 ComfyUI-Whisper 节点的 `segments_alignment` 对齐，可直接串在
`Apply Whisper` 与 `Save SRT` 之间。

`config` 选 `none` 即**关闭转换**（原样透传），无需改动连线，便于开关。
"""

import json

try:
    from opencc import OpenCC
except Exception:  # pragma: no cover
    OpenCC = None

_CACHE = {}

# none 放第一项：想关掉繁转简时直接选它，不用动连线
CONFIGS = [
    "none",
    "t2s",
    "tw2s",
    "s2t",
    "s2tw",
    "s2hk",
    "hk2s",
]

_DESC = {
    "none": "不转换（关闭繁转简，原样输出）",
    "t2s": "繁体 -> 简体（最常用）",
    "tw2s": "台湾正体 -> 简体",
    "s2t": "简体 -> 繁体",
    "s2tw": "简体 -> 台湾正体",
    "s2hk": "简体 -> 香港繁体",
    "hk2s": "香港繁体 -> 简体",
}


def _get(config: str):
    if OpenCC is None:
        raise RuntimeError(
            "未安装 opencc。请在 ComfyUI 的 Python 环境执行："
            "pip install opencc-python-reimplemented"
        )
    if config not in _CACHE:
        _CACHE[config] = OpenCC(config)
    return _CACHE[config]


class OpenCCZhConvert:
    """把 whisper 的对齐结果整体转换（默认繁转简），同时输出纯文本。

    config 选 `none` 时不做任何转换，等效于"关掉繁转简"。
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "alignment": ("whisper_alignment", {
                    "description": "来自 Apply Whisper 的 segments_alignment"
                }),
                "config": (CONFIGS, {
                    "default": "t2s",
                    "description": "选 none 即关闭转换；t2s = 繁体转简体（常用）",
                }),
            },
        }

    RETURN_TYPES = ("whisper_alignment", "STRING")
    RETURN_NAMES = ("alignment", "text")
    FUNCTION = "convert"
    CATEGORY = "whisper"

    def convert(self, alignment, config):
        data = json.loads(alignment) if isinstance(alignment, str) else alignment
        if not data:
            return ([], "")

        if config == "none":
            out = [dict(seg) for seg in data]
            print("[OpenCC] 已关闭转换，原样透传 %d 段" % len(out))
        else:
            cc = _get(config)
            out = []
            for seg in data:
                item = dict(seg)
                item["value"] = cc.convert(str(seg.get("value", "")))
                out.append(item)
            print("[OpenCC] %s 转换完成，%d 段 -> %s"
                  % (config, len(out), "".join(x["value"] for x in out)[:80]))

        text = "".join(x["value"] for x in out).strip()
        return (out, text)


NODE_CLASS_MAPPINGS = {
    "OpenCCZhConvert": OpenCCZhConvert,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenCCZhConvert": "繁转简（字幕）",
}
