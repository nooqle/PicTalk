# PicTalk

![License](https://img.shields.io/github/license/nooqle/PicTalk?style=flat-square)
![Skill](https://img.shields.io/badge/Agent-Skill-111111?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Supported-222222?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Supported-6B5B95?style=flat-square)

[English README](./README.en.md)

PicTalk 是一个把长文、报告、会议纪要和产品说明转成信息图的 Agent Skill。

很多内容写完以后，真正要展示给别人看时，需要一张图先把结构讲清楚。PicTalk 做的就是这件事：读取素材，提炼重点，选择合适的图式，然后生成一张或几张可以直接放进汇报里的信息图。

## 能做什么

- 从文章、Markdown、会议纪要、PDF 摘要或粘贴文本中提取核心结构。
- 根据内容自动选择图式，例如层级、流程、循环、转化、时间线、矩阵。
- 输出中文或英文信息图，适合策略汇报、产品说明、文章配图和演讲材料。
- 使用 HTML/CSS 模板渲染最终图片，中文、数字和标题会更稳定。
- 提供分镜 JSON、渲染脚本和校验脚本，方便重复生成和继续修改。

## 样例

### 层级扩散

![层级扩散图式](./docs/images/card-01.png)

### 协同循环

![协同循环图式](./docs/images/card-02.png)

### 转化逻辑

![转化逻辑图式](./docs/images/card-03.png)

### 用户操作流程

![用户操作流程图式](./docs/images/meal-flow.png)

样例文件在 `docs/images/`，对应分镜是 `docs/images/storyboard.json` 和 `docs/images/meal-flow-storyboard.json`。

## 快速开始

### Claude Code

```bash
git clone https://github.com/nooqle/PicTalk.git
cp -r PicTalk/pictalk ~/.claude/skills/pictalk
```

安装后可以这样说：

```text
用 PicTalk 把这篇文章做成 3 张信息图，中文输出，适合放进汇报。
```

### Codex

把 `pictalk/` 放到 Codex 的 skills 目录后使用：

```text
Use $pictalk to turn this article into presentation-ready infographics.
```

### 本地直接运行

仓库里包含可运行的示例分镜：

```bash
python pictalk/scripts/validate_storyboard.py docs/images/storyboard.json
python pictalk/scripts/render_storyboard.py docs/images/storyboard.json --output-dir docs/images
```

生成流程图示例：

```bash
python pictalk/scripts/validate_storyboard.py docs/images/meal-flow-storyboard.json
python pictalk/scripts/render_storyboard.py docs/images/meal-flow-storyboard.json --output-dir docs/images
```

## 常用请求

```text
把这篇文章转成一张能讲清核心逻辑的信息图。
```

```text
把这份产品说明做成 3 张图：一张流程图，一张能力结构图，一张结论图。
```

```text
把这段会议纪要做成可视化总结，保留关键数字和专有名词。
```

```text
基于这份 Markdown 生成一张 3:4 竖版中文信息图。
```

## 工作流程

PicTalk 的基本流程很简单：

1. 读取素材，识别主题、论点、阶段、角色、关系和结论。
2. 决定输出几张图。
3. 选择图式并生成 storyboard。
4. 用 HTML/CSS 模板渲染 PNG。
5. 运行校验脚本，检查结构、尺寸和文字覆盖。

如果你只需要快速出图，可以让 Agent 直接跑完整流程。如果你要精修，可以先改 storyboard，再重新渲染。

## 图式

### Premium 图式

| 图式 | 适合内容 |
| --- | --- |
| `premium-hierarchy-diffusion` | 层级、成熟度、能力栈、需求升级 |
| `premium-cycle-system` | 反馈循环、运营飞轮、协同循环 |
| `premium-transformation-logic` | 旧状态到新状态、问题到方案、信号到结构 |
| `premium-process-flow` | 用户旅程、产品流程、AI 处理管线、流式输出 |

### 通用图式

| 图式 | 适合内容 |
| --- | --- |
| `arrow-flow` | 任务流程、操作步骤、交接链路 |
| `timeline` | 时间线、版本节奏、事件顺序 |
| `matrix` | 分类对比、优先级、责任划分 |
| `layer-stack` | 分层结构、能力等级、成熟度 |
| `cycle` | 循环机制、持续改进 |
| `comparison` / `transformation` | 对比、转化、方案说明 |

## 设计系统

PicTalk 默认使用偏克制的汇报风格：

- 竖版 `1086x1448`，适合文章配图和长图。
- 横版 `1536x1024`，适合流程图和演示页。
- 主色以深蓝为主，配合绿色、橙色、紫色做语义区分。
- 模块有固定圆角、边框、阴影和留白规则。
- 图中优先使用图标、编号、箭头、连接线和结论带来表达结构。

默认色彩：

| 角色 | 色值 |
| --- | --- |
| 标题深蓝 | `#071B49` |
| 主蓝 | `#0757D8` |
| 绿色 | `#128348` |
| 橙色 | `#E77800` |
| 紫色 | `#5A2BAE` |
| 正文 | `#111827` |
| 边框 | `#BFD2F5` |
| 背景 | `#FFFFFF` |

## 项目结构

```text
pictalk/
├── SKILL.md
├── agents/
│   ├── openai.yaml
│   └── generic.yaml
├── assets/
│   ├── storyboard-template.json
│   └── template-infographic.html
├── references/
│   ├── layouts.md
│   ├── pattern-library.md
│   ├── storyboard-schema.md
│   ├── style-guide.md
│   ├── text-accuracy.md
│   └── image-prompts.md
└── scripts/
    ├── validate_storyboard.py
    ├── render_storyboard.py
    ├── qa_rendered_html.py
    ├── qa_benchmark_image.py
    └── analyze_layout_alignment.py

docs/
├── images/
│   ├── card-01.png
│   ├── card-02.png
│   ├── card-03.png
│   ├── meal-flow.png
│   ├── storyboard.json
│   └── meal-flow-storyboard.json
└── pictalk-premium-layout-design.md
```

## 校验

常用校验命令：

```bash
python pictalk/scripts/validate_storyboard.py docs/images/storyboard.json
python pictalk/scripts/render_storyboard.py docs/images/storyboard.json --output-dir docs/images --keep-html
python pictalk/scripts/qa_rendered_html.py docs/images/card-01.html docs/images/card-02.html docs/images/card-03.html
```

如果你有参考图，可以比较版心、留白和内容覆盖率：

```bash
python pictalk/scripts/qa_benchmark_image.py benchmark.png docs/images/card-01.png
```

## License

MIT. See [LICENSE](./LICENSE).
