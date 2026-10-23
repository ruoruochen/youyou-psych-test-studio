# 又又心理测试工作室

[English](README.md) · [Skill 执行入口](SKILL.md) · [迭代记录](ITERATIONS.md)

一个从测试主题推进到研究策划、完整资料包、本地答题网页，再按指令部署到上码 Upma 的 Codex Skill。适用于原创娱乐与自我探索测试，也可按有出处资料的适用范围制作量表。它不提供临床诊断，也不代表新编题目已经具备心理测量信效度。

本仓库的 Skill 执行入口使用英文，使用说明提供中英双语；生成项目默认中文，也可按要求调整。

## 能做什么

1. **先交付完整资料包**：全部题目与选项、可复算的计分和平局规则、所有结果与报告、来源和使用边界、结构化数据及计分校验样例。题数、维度数和结果数根据主题确定。
2. **提供三种风格预览**：A **青绿清简**、B **米金书卷**、C **雾紫编辑**，也可根据明确参考图定制。[在本地打开风格画廊](assets/style-gallery/index.html)。
3. **确认后制作网页**：确认内容、风格和开始制作后，由 Agent 实现手机答题、返回修改、进度恢复、计算报告、维度图、真正可下载的中文 PDF 和分享海报 PNG。最终打包为自包含的 `site/index.html`，运行依赖随站点提供。
4. **验收后按指令上线**：本地成品通过验收且已有明确部署授权后，Agent 核对 Upma 当前登录、项目额度和平台规则，发布最终站点，并在实际网络条件下验证正式入口和导出。此前明确要求“验收后部署”的授权继续有效。

三种风格是可切换的静态界面示意。项目助手负责登记与检查；它不是任意主题通用的自动评分引擎，也不会一条命令生成正式测试。每套题库和网页由 Agent 按确认后的资料包研究、实现。

## 安装

安装 Git 后，将仓库克隆到 Codex 的技能目录：

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/ruoruochen/youyou-psych-test-studio.git "${CODEX_HOME:-$HOME/.codex}/skills/youyou-psych-test-studio"
```

如果目标目录已存在，更新原安装，不要覆盖克隆。若 Codex 尚未列出该 Skill，开启新聊天后使用。

## 调用示例

在聊天中调用 `$youyou-psych-test-studio`，提供主题或已有项目：

> 我要做一个“面对变化时的应对方式”自我探索测试，先研究并交付完整资料包。

> 方案可以，用 B 米金书卷做本地网页。

> 网页没问题。调用当前 Skill 的部署能力，帮我部署。

一句话可以同时确认方案、风格和本地制作；已有明确授权不重复确认。

新项目默认保存在当前使用者的 `~/codex_workspace/心理测试网页/`，优先服从你的目录偏好。助手的 `init --output` 可指定项目目录，`list --root` 可指定项目集合目录：

```sh
python3 "${CODEX_HOME:-$HOME/.codex}/skills/youyou-psych-test-studio/scripts/studio.py" --help
python3 "${CODEX_HOME:-$HOME/.codex}/skills/youyou-psych-test-studio/scripts/studio.py" init --topic "面对变化的应对方式" --output "$HOME/codex_workspace/心理测试网页/应对变化"
python3 "${CODEX_HOME:-$HOME/.codex}/skills/youyou-psych-test-studio/scripts/studio.py" list --root "$HOME/codex_workspace/心理测试网页"
```

助手还支持详情、编辑保存、确认记录、风格准备、交付检查、软归档和恢复。测试项目独立保存，不写进已安装的 Skill 本体。

## 工具依赖与边界

- **Python 3**：项目助手仅使用标准库。
- **具备联网研究和编程能力的 Agent**：负责来源核验、内容设计、计分实现与网页制作。需要的 PDF／PNG 导出库随最终站点打包。
- **环境已有的授权浏览器能力**：用于真实交互、文件下载检查和部署。Ego 可用时优先使用，并先读其 Skill 与当前 CLI 指南；否则使用环境已有的其他授权浏览器工具。不依赖旧心理测试 Skill。
- **Upma 访问能力**：登录或验证码可能需要你本人完成。免费额度与可用条件在部署当时核对；单次网络验证不代表国内所有网络永久可达。

默认在浏览器本地处理答案和导出；账号、支付、追踪及云端收集答案需要另行提出。部署只上传最终站点，不上传研究资料或凭证。原创测试应如实说明其编辑探索性质；有出处的量表遵守实际使用权限与解释范围。

分阶段细则见[规划资料包](references/planning.md)、[本地制作](references/local-build.md)和 [Upma 部署](references/deployment-upma.md)。
