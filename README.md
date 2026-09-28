# comfyui-opencc-zh

> 给 **ComfyUI-Whisper** 用的「繁转简」节点：Whisper 转中文字幕时经常输出繁体，
> 本节点串在 `Apply Whisper` 与 `Save SRT` 之间，在写出字幕之前把繁体统一转成简体。

## 解决什么问题

用 Whisper 给中文录音转字幕，输出常常是繁体（尤其 `large-v3` 系列与老录音）。
事后拿工具批量转一遍很麻烦。本节点把这一步放回工作流里，**一次接线，每次自动**。

## 安装

### 方式一：ComfyUI-Manager

搜索 `opencc-zh` → Install → 重启 ComfyUI。

### 方式二：手动

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/kevinhuang999/comfyui-opencc-zh.git
```

手动 clone 时依赖**不会自动装**，需要自己跑一次（必须用 ComfyUI 自己的 Python 环境）：

```bash
<ComfyUI 目录>/python/python.exe -m pip install -r requirements.txt
```

> 秋叶整合包（ComfyUI-aki）用户：Python 在 `D:\ComfyUI-aki-v3.2\python\python.exe`，
> **不是** `python_embeded`。装错环境节点会报 `No module named 'opencc'`。
>
> 方式一（Manager 安装）会读仓库里的 `requirements.txt` 自动装依赖，不用手动执行。

装完**重启 ComfyUI**，节点出现在 `whisper` 分类下（显示名「繁转简（字幕）」）。

## 节点

**繁转简（字幕）** · `OpenCCZhConvert`

| | |
|---|---|
| 输入 | `alignment` — 类型 `whisper_alignment`，接 `Apply Whisper` 的 `segments_alignment` |
| | `config` — 转换模式，见下表 |
| 输出 | `alignment` — 转换后结果，接 `Save SRT` |
| | `text` — 纯文本，接 `PreviewAny` 可直接看字幕内容 |

### config 选项

| 值 | 含义 |
|---|---|
| `none` | **不转换**（原样透传）— 想关掉繁转简时选它，**不用改连线** |
| `t2s` | 繁体 → 简体（最常用，默认） |
| `tw2s` | 台湾正体 → 简体 |
| `s2t` | 简体 → 繁体 |
| `s2tw` | 简体 → 台湾正体 |
| `s2hk` | 简体 → 香港繁体 |
| `hk2s` | 香港繁体 → 简体 |

## 接线

```
LoadAudio → Apply Whisper → OpenCCZhConvert → Save SRT
                                  └──────────→ PreviewAny（看纯文本）
```

节点在链路中间，想临时关掉把 `config` 选成 `none` 即可，**不用断线改接**。

## 说明

- **开着会不会误伤简体？** 实测 8 组「一对多」陷阱词（著作/著名/显著、面条/里面/公里、
  干活/干燥/干部、发展/头发、了解/了却、后面/皇后 等）在 `t2s` 下**全部原样通过，0/8 被改动**。
  所以平时开着无副作用，属于真保险。
- 底层用 [`opencc-python-reimplemented`](https://pypi.org/project/opencc-python-reimplemented/)
  （纯 Python wheel，无需编译），转换规则来自 [OpenCC](https://github.com/BYVoid/OpenCC)。
- **已知反例，如实记录**：短音频上 `large-v3-turbo` 可能漏字（如「或者」听成「或」）。
  本节点只做繁简转换，**不做纠错**——字幕准确度取决于所选 Whisper 模型。

## License

MIT
