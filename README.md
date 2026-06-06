# PicTalk · 长文变信息图

![License](https://img.shields.io/github/license/nooqle/PicTalk?style=flat-square) ![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square) ![Storyboard Validated](https://img.shields.io/badge/Storyboard-Validated-128348?style=flat-square) ![Claude Code](https://img.shields.io/badge/Claude%20Code-Supported-6B5B95?style=flat-square) ![Codex](https://img.shields.io/badge/Codex-Supported-222222?style=flat-square) ![Cursor](https://img.shields.io/badge/Cursor-Available-00B4D8?style=flat-square)

> 🌏 **English version: [README.en.md](./README.en.md)**

一个适配 Claude Code / Codex / Cursor 等 Agent 环境的信息图技能，用于将长文内容转化为**逻辑清晰、文字精准的可视化信息图**。

核心能力：读取文章或素材 → 提取论证结构 → 优先选择 premium 锁定版式（层级扩散、协同循环、转化逻辑、流程主轴） → 构建分镜 → 确定性渲染文字 → 校验交付。

它不依赖图像模型生成最终文字。所有中文、英文、数字、公式、标签均通过确定性文本层渲染，保证文字零差错。

## 样例图库

**层级扩散图式（Hierarchy Diffusion）** — 共同语言如何长出来

![PicTalk 信息图效果展示 - 层级扩散图式](./docs/images/card-01.png)

**飞轮型图式（Cycle）** — 默会知识的协同转译循环

![PicTalk 信息图效果展示 - 飞轮图式](./docs/images/card-02.png)

**转化逻辑图式（Transformation Logic）** — 从信号到囫囵语的协同转化

![PicTalk 信息图效果展示 - 转化逻辑图式](./docs/images/card-03.png)

**用户操作流程图式（Premium Process Flow）** — 餐食 AI 识别报告链路

![PicTalk 信息图效果展示 - 用户操作流程图式](./docs/images/meal-flow.png)

样例文件已纳入仓库：`docs/images/card-01.png`、`docs/images/card-02.png`、`docs/images/card-03.png`、`docs/images/meal-flow.png`。对应分镜在 `docs/images/storyboard.json` 和 `docs/images/meal-flow-storyboard.json`。

## 30 秒开始

**Claude Code 用户：**

```bash
# 把 pictalk/ 复制到 Claude Code 技能目录
cp -r pictalk ~/.claude/skills/pictalk
```

也可以直接把这段话发给有 shell 权限的 AI Agent：

```text
帮我安装 PicTalk 技能。请把 https://github.com/nooqle/PicTalk 克隆到本地，然后将 pictalk/ 目录复制到 ~/.claude/skills/pictalk，安装完成后检查 SKILL.md、references/、assets/ 是否存在。
```

**Codex 用户：**

```text
Use $pictalk to turn this article into a concise set of presentation-ready infographics with varied diagram forms.
```

安装后直接对 Agent 说：

```text
帮我把这篇文章做成 3-5 张信息图，用时间线和箭头流展示核心逻辑。
```

也可以试这些请求：

```text
帮我把这份报告转化为可视化信息图，中文输出，用蓝绿色调。
把这段会议纪要做成 4 张图，一张用矩阵图式，一张用漏斗图式。
基于这份文档做一组信息图，确保所有数字和专有名词准确无误。
```

## 效果

- 📐 **Premium 锁定版式**：`premium-hierarchy-diffusion`、`premium-cycle-system`、`premium-transformation-logic`、`premium-process-flow`，面向“一张图讲清一件事”
- 🧭 **通用图式 fallback**：转化、时间线、箭头流、层级堆叠、矩阵、飞轮等，用于次级卡片和简单结构
- ✍️ **确定性文字渲染**：所有最终文字通过 HTML/SVG/PPTX 等确定性层渲染，不依赖图像模型画字
- 🎨 **语义色彩系统**：12 色语义调色板，按含义分配颜色而非装饰，支持自定义映射
- 📋 **分镜先于渲染**：先构建 JSON 分镜（含文字账本、图式选择、论证依据），再进入渲染
- 🔍 **自动校验**：Python 脚本校验分镜结构、必填字段、图式类型、品牌保护规则
- 🌐 **中英双语**：面向中英文混合内容优化，CJK 字体排版规则内置
- 🚫 **零意外品牌**：PicTalk 不出现在最终图片中，除非用户明确要求

## 适合 / 不适合

**✅ 合适**：策略汇报信息图 / 文章核心逻辑可视化 / 中文为主的信息图 / 产品功能对比图 / 会议纪要可视化 / 演讲配图

**❌ 不合适**：大段表格数据展示（建议用 Excel）/ 需要照片级写实的场景 / 需要交互式数据仪表盘

## 常见使用场景

| 任务 | 推荐方式 |
|------|---------|
| 长文章变信息图 | 先提取论证结构，再按 3-5 张节奏生成图组 |
| 产品/方案对比 | 用转化型或矩阵图式，突出新旧差异 |
| 流程/时间线可视化 | 用箭头流或时间线图式，保留步骤顺序和产出节点 |
| 组织/责任梳理 | 用责任地图或泳道图式，明确归属和协作关系 |
| 策略/层级表达 | 用层级堆叠或金字塔图式，体现优先级和成熟度 |
| 会议纪要可视化 | 先筛核心结论，再按论证链路选 2-3 个图式 |

## 为什么是确定性文字渲染

大多数"文章变图片"工具失败在两个地方：先过度概括再设计，然后让图像模型发明或篡改文字。PicTalk 用更严格的循环解决这个问题：

```text
读取素材 → 提取论证 → 选择图式 → 构建分镜（含文字账本）→ 锁定版式 HTML 渲染 → 校验交付
```

- 分镜 `text_ledger` 是所有可见文字的唯一来源，渲染时逐字取用，不得改写
- 锁定 HTML/CSS 版式负责默认最终图片，避免让弱模型临场发明版式
- 渲染后逐条比对可见文字与 text_ledger，高风险 token（专有名词、缩写、百分比、日期）必须人工检查
- 有图片生成能力时，可生成无文字视觉底图或探索草稿，但最终交付优先使用确定性文字层

## 平台支持

| 平台 | 状态 | 说明 |
|------|------|------|
| Claude Code | 支持 | 原生 Skill 工作流，复制到 `~/.claude/skills/` 即可 |
| Codex | 支持 | 通过 `agents/openai.yaml` 适配，使用 `$pictalk` 触发 |
| Cursor / 其他本地 Agent | 可用 | 需要能读写文件并执行 shell 命令 |
| 普通 Chatbot | 不推荐 | 没有文件系统时，很难稳定生成分镜和校验输出 |

## 安装

### 方式一：Claude Code 安装（推荐）

```bash
# 克隆仓库并复制技能目录
git clone https://github.com/nooqle/PicTalk.git /tmp/pictalk-repo
cp -r /tmp/pictalk-repo/pictalk ~/.claude/skills/pictalk
```

### 方式二：把下面这段话直接发给 AI

> 帮我安装 `PicTalk` 这个 Agent 技能。请按下面步骤做：
>
> 1. 确保 `~/.claude/skills/` 目录存在（不存在就创建）
> 2. 执行 `git clone https://github.com/nooqle/PicTalk.git /tmp/pictalk-repo`
> 3. 执行 `cp -r /tmp/pictalk-repo/pictalk ~/.claude/skills/pictalk`
> 4. 验证：`ls ~/.claude/skills/pictalk/` 应该看到 `SKILL.md`、`references/`、`assets/` 三项
> 5. 告诉我安装好了，之后我说"做一组信息图"之类的话就会触发这个技能

### 方式三：Codex 安装

将 `pictalk/` 目录放入 Codex 技能目录，使用 `$pictalk` 语法触发。

### 触发方式

装好后，Agent 会在对话里自动发现并调用这个技能。触发关键词：

- "帮我把这篇文章做成信息图"
- "生成一组可视化信息图"
- "用时间线图式展示这个流程"
- "turn this article into infographics"
- "create a set of presentation-ready visual cards"

## 使用流程

技能本身是结构化工作流，Agent 会逐步引导：

1. **读取素材** — 文章、PDF、会议纪要、笔记或粘贴文本
2. **提取论证** — 主论点、支撑论据、因果链、阶段、角色、指标、矛盾点、结论
3. **决定图数** — 1 张核心图，2-3 张主要分支，4-7 张密集内容，超过 7 张建议分章
4. **选择图式** — 为每张图选择最匹配逻辑的图式，避免全部使用卡片网格
5. **构建分镜** — 记录精确可见文字、布局类型、premium 语义槽位、论据来源、色彩角色、文字账本
6. **渲染图片** — 优先使用锁定 HTML/CSS 版式确定性渲染；图像模型只作为可选视觉底图或探索草稿
7. **校验交付** — 检查文字准确性、图式多样性、论据依据、品牌保护

详细说明见 [`SKILL.md`](./pictalk/SKILL.md)。

## 视觉图式

PicTalk 内置 4 种 premium 锁定版式和一组通用 fallback 图式。用户要求“有质感”“层级指示”“一张图说清楚”时，优先使用 premium 版式。

| Premium 版式 | 适用场景 |
|--------------|---------|
| `premium-hierarchy-diffusion` | 层级、需求升级、成熟度、能力栈、高带低、右侧人群层 |
| `premium-cycle-system` | 反馈循环、运营飞轮、转译循环、持续改进；内环阶段芯片 + 双层反馈路径 |
| `premium-transformation-logic` | 输入碎片→校准闸门→输出结构；每列判断句 + 转化产物包 |
| `premium-process-flow` | 用户旅程、产品操作流程、AI 处理管线；四阶段主轴 + 流式输出带 + 检查点 |

通用图式用于 secondary cards 或简单表达：

| 图式 | 适用场景 |
|------|---------|
| 转化（Transformation） | 新旧对比、问题→方案、现状→目标 |
| 时间线（Timeline） | 议程、版本路径、事件序列、阶段 |
| 箭头流（Arrow Flow） | 流程、价值链、任务交接、决策路径 |
| 层级堆叠（Layer Stack） | 成熟度、用户分层、能力等级、需求层级 |
| 矩阵（Matrix） | 分类交叉分析、决策矩阵、优先级评估 |
| 责任地图（Responsibility Map） | 归属关系、协作接口、共享指标 |
| 飞轮（Cycle） | 反馈循环、运营节奏、持续改进 |
| 漏斗（Funnel） | 从广泛到聚焦的筛选、证据收敛、决策路径 |
| 金字塔（Pyramid） | 优先级、基础架构、战略阶梯、依赖关系 |
| 放射地图（Radial Map） | 中心论点向外辐射、驱动因素、影响分析 |
| 泳道（Swimlane） | 跨团队流程、角色分工、交接节点 |
| 计分卡（Scorecard Plus） | 高层图式 + 关键指标/原则面板 |

图式选择规则和反模式见 [`pattern-library.md`](./pictalk/references/pattern-library.md)。

## 色彩系统

默认 12 色语义调色板，按含义分配颜色：

| 角色 | 色值 | 用途 |
|------|------|------|
| `title_navy` | `#071B49` | 主标题、最强文字 |
| `primary_blue` | `#0757D8` | 主箭头、徽章、结论条 |
| `blue_light` | `#EAF2FF` | 蓝色模块填充、图标底 |
| `green` | `#128348` | 用户、行为、成功、治理 |
| `green_light` | `#EAF7EF` | 绿色模块填充 |
| `orange` | `#E77800` | 知识、警示、中间层强调 |
| `orange_light` | `#FFF1DE` | 橙色模块填充 |
| `purple` | `#5A2BAE` | 探索、创新、进阶主题 |
| `purple_light` | `#F1EAFB` | 紫色模块填充 |
| `gray` | `#6B7280` | 过去状态、次要标签 |
| `border` | `#BFD2F5` | 模块细边框 |
| `text` | `#111827` | 正文文字 |

自定义规则：保留对比度，按含义分配颜色。用户自选调色板时，将颜色映射到上述语义角色。

排版规则见 [`style-guide.md`](./pictalk/references/style-guide.md)。

## 分镜格式

每份输出以分镜 JSON 为源。一个最小的卡片条目：

```json
{
  "id": "card-01",
  "title": "认知转变：从旧模式到新模式",
  "layout_type": "transformation",
  "primary_pattern": "transformation",
  "composition": {
    "dominant_structure": "左右两区通过大箭头连接，底部用结论条收束。",
    "not_card_grid": true,
    "visible_marks": ["左右分区", "大箭头", "编号", "底部结论条"]
  },
  "text_ledger": [
    "认知转变：从旧模式到新模式",
    "过去：旧模式",
    "动作先行",
    "价值难以沉淀",
    "核心结论：把价值路径讲清楚，行动才有共同方向。"
  ]
}
```

校验分镜：

```bash
python pictalk/scripts/validate_storyboard.py pictalk/assets/storyboard-template.json
```

一键渲染分镜为 PNG：

```bash
python pictalk/scripts/render_storyboard.py storyboard.json --template pictalk/assets/template-infographic.html --output-dir output/
```

保留 HTML 后做基础视觉 QA：

```bash
python pictalk/scripts/render_storyboard.py storyboard.json --output-dir output/ --keep-html
python pictalk/scripts/qa_rendered_html.py output/card-01.html
```

如果有参考图，把候选图和 benchmark 做版面密度、边缘留白和底部留白对比：

```bash
python pictalk/scripts/qa_benchmark_image.py benchmark.png output/card-01.png
```

默认阈值会卡尺寸、上/左/右边距、底部留白和内容覆盖率；过不了时不要交付，继续调整布局或换用更匹配的 premium 版式。

分镜完整 schema 见 [`storyboard-schema.md`](./pictalk/references/storyboard-schema.md)，文字准确性规则见 [`text-accuracy.md`](./pictalk/references/text-accuracy.md)。

## 示例请求

复制下面任意一条给 Agent，再附上你的文章、Markdown 或素材文件：

```text
帮我把这篇文章转化为 3-5 张信息图，用时间线和箭头流展示核心逻辑，蓝色调。
```

```text
把这个产品对比文档做成可视化信息图，用矩阵图式突出差异，确保所有数据准确。
```

```text
基于这份会议纪要做一组 4 张的信息图，每张用不同图式，中文输出。
```

```text
Turn this report into 5 presentation-ready infographics. Use varied diagram forms. Ensure all numbers and acronyms are exact.
```

## 目录结构

```
pictalk/
├── SKILL.md                      ← 技能主文件：工作流、原则、校验规则
├── agents/
│   ├── openai.yaml               ← Codex 适配器配置
│   └── generic.yaml              ← 通用 Agent 适配器配置
├── assets/
│   ├── storyboard-template.json  ← 可直接校验和渲染的 premium 分镜模板
│   └── template-infographic.html ← 锁定 HTML/CSS 渲染模板
├── references/
│   ├── layouts.md                ← premium + 通用锁定版式契约
│   ├── pattern-library.md        ← 12 种图式 + 组合方案 + 反模式
│   ├── storyboard-schema.md      ← 分镜 JSON schema 完整文档
│   ├── style-guide.md            ← 画布尺寸、12 色调色板、排版、组件、布局族
│   ├── text-accuracy.md          ← 文字准确性规则、text_ledger 工作流、高风险 token
│   └── image-prompts.md          ← 可选图像生成模式：无文字底图 / image-text 草稿
└── scripts/
    ├── validate_storyboard.py    ← 校验分镜结构、必填字段、图式类型、品牌保护
    ├── render_storyboard.py      ← 分镜 JSON → PNG 一键渲染
    ├── qa_rendered_html.py       ← 检查渲染 HTML 是否越界或裁切文字
    ├── qa_benchmark_image.py     ← 与参考图比较尺寸、留白和版面覆盖率
    └── analyze_layout_alignment.py ← 拆解样本版心、边距、覆盖率和密度峰值
docs/
└── images/                       ← 示例信息图截图
    ├── card-01.png
    ├── card-02.png
    ├── card-03.png
    └── meal-flow.png
```

## 核心设计原则

1. **论据先于视觉** — 来源证据比视觉美化更重要
2. **逻辑先于阅读** — 读者在读完文字之前就应该看到逻辑结构
3. **卡片是容器，不是构图** — 卡片只是局部容器，每张图必须有主导的图式结构
4. **每条可见文字来自分镜账本** — 渲染只从 `text_ledger` 取字符串
5. **最终图片不含生成伪文字** — 图像模型从不画最终文字
6. **有疑则标疑，不造确定性** — 来源不确定时展示不确定性，而非编造看似干净的逻辑
7. **图式多样性** — 3 张以上的图组，至少使用 3 种不同图式
8. **术语统一** — Skill 就是 Skill，不中英混译

## Roadmap

- 补充真实案例和可打开的信息图示例
- 增加更多 premium 锁定版式和视觉 QA 检查
- 优化多语言文字 QA 工作流
- 增加更多调色板预设
- 增加 Cursor / Windsurf 等平台的适配器配置
- 支持从 URL 直接读取文章并生成信息图

## FAQ

**PicTalk 和普通"文章变图片"有什么区别？**

核心区别是确定性文字渲染。PicTalk 不让图像模型画文字，而是通过 HTML/SVG/PPTX 的文本层精确渲染。同时先提取论证结构再选择图式，而不是简单地把文字排成卡片。

**支持哪些输出格式？**

支持 HTML/CSS 导出 PNG/PDF、SVG、PPTX/Keynote/Google Slides。核心是确定性文本渲染，具体格式取决于渲染环境。

**可以自定义颜色吗？**

可以。用户提供的调色板会被映射到语义角色（primary、accent_success、accent_warning 等），保持对比度和可读性。

**分镜 JSON 是必须的吗？**

建议使用。分镜是文字准确性的基础，也方便迭代。但如果只是快速出图，可以跳过完整分镜，直接生成。

**怎么更新到最新版？**

重新运行安装命令，或在本地技能目录执行 `git pull`。

## 贡献

Bug、图式需求、渲染器模板、校验规则改进——欢迎开 Issue 或 PR。改动请优先：

- 新图式进 `references/pattern-library.md` 并给出适用场景
- 新渲染器模板提供对应 `assets/` 文件
- 校验规则更新同步到 `scripts/validate_storyboard.py`
- 文字准确性规则更新同步到 `references/text-accuracy.md`
- 分镜 schema 更新同步到 `references/storyboard-schema.md`

## License

MIT. See [LICENSE](./LICENSE).
