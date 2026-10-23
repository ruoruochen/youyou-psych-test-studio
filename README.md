# Youyou Psych Test Studio

[中文说明](README.zh-CN.md) · [Skill instructions](SKILL.md) · [Iteration notes](ITERATIONS.md)

A Codex skill that takes a psychological-test theme through research, a complete reviewable content package, a local web app, and optional Upma deployment. Designed for original entertainment and self-exploration tests, or properly sourced instruments used within their supported scope. It does not provide clinical diagnosis or establish psychometric validity.

The skill entry point is written in English. User documentation is available in English and Chinese; generated projects default to Chinese unless requested otherwise.

## What you get

1. **Plan first:** a full question bank and answer options, reproducible scoring and tie rules, every result and report, source records and usage boundaries, structured data, and scoring validation examples. Question, dimension, and result counts follow the theme rather than a fixed template.
2. **Choose a style:** three bundled, switchable static interface previews—A **Jade Minimal**, B **Parchment Gold**, and C **Mist Editorial**. A supplied visual reference can also guide a custom design. [Open the gallery locally](assets/style-gallery/index.html).
3. **Confirm and build:** after you approve the content, style, and local build, the agent implements the mobile-first questionnaire, answer editing and progress recovery, calculated reports, dimension charts, a real downloadable Chinese PDF, and a shareable PNG. The final app is packaged as a self-contained `site/index.html` with bundled runtime dependencies.
4. **Review, then publish:** inspect the local app first. Once it is accepted and deployment has been explicitly authorized, the agent checks current Upma login, project limits, and service terms; publishes the final site; and verifies the public address and exports within the available network conditions. An earlier explicit instruction to deploy after acceptance remains valid.

The gallery contains design examples. The helper is a project manager, not a universal scoring engine or a one-command questionnaire generator. The agent researches and implements each approved model.

## Install

With Git installed, clone this repository into your Codex skills directory:

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/ruoruochen/youyou-psych-test-studio.git "${CODEX_HOME:-$HOME/.codex}/skills/youyou-psych-test-studio"
```

If that directory already exists, update the existing installation instead of cloning over it. Start a new Codex chat if the skill is not yet listed.

## Use

Invoke `$youyou-psych-test-studio` with a theme or an existing project:

> I want a self-exploration test about how people handle change. Research and prepare the complete planning package first.

> The content looks good. Use style B and build the local website.

> The local website is accepted. Use this skill’s deployment workflow to publish it to Upma.

Chinese deployment wording: **调用当前 Skill 的部署能力，帮我部署。** Existing explicit approvals remain valid; one instruction can approve the plan, style, and build together.

New projects default to `~/codex_workspace/心理测试网页/`. Your directory preferences take precedence. The helper supports `init --output` for a project location and `list --root` for a collection location:

```sh
python3 "${CODEX_HOME:-$HOME/.codex}/skills/youyou-psych-test-studio/scripts/studio.py" --help
python3 "${CODEX_HOME:-$HOME/.codex}/skills/youyou-psych-test-studio/scripts/studio.py" init --topic "Handling change" --output "$HOME/codex_workspace/心理测试网页/handling-change"
python3 "${CODEX_HOME:-$HOME/.codex}/skills/youyou-psych-test-studio/scripts/studio.py" list --root "$HOME/codex_workspace/心理测试网页"
```

The helper also supports project details, edits, confirmation records, style preparation, delivery checks, soft archive, and restore. Projects are stored separately from the installed skill.

## Tools and boundaries

- **Python 3:** the helper uses only the standard library.
- **An agent with web research and coding capabilities:** required for current source research, content design, scoring implementation, and the web app. PDF/PNG export libraries, when needed, are bundled with the generated site.
- **An authorized browser capability:** required for interaction checks, real downloads, and deployment. Prefer Ego when available and read its skill and current CLI guide before use; otherwise use the environment’s available authorized browser tools. No older psychological-test skill is required.
- **Upma access:** deployment may require you to complete login or verification. Free limits and availability are checked at the time of publishing. A successful check on one network does not guarantee permanent access from every network in China.

Answers and exports stay in the browser by default; accounts, payments, tracking, and cloud answer collection require a separate request. Deployment uploads only the final site, not the research package or credentials. Original tests must be described as editorial exploration models, and sourced instruments retain their actual permissions and interpretation limits.

See [planning](references/planning.md), [local build](references/local-build.md), and [Upma deployment](references/deployment-upma.md) for the staged workflow.
