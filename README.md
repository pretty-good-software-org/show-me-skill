# show-me-skill

An [Agent Skill](https://agentskills.io/specification), `show-me`, that helps an agent explain the current topic
visually. It picks the smallest view that makes the point clear and keeps the prose around it brief.

| Shape             | Shows                                                                |
| ----------------- | -------------------------------------------------------------------- |
| Pseudocode        | Logic or an algorithm                                                |
| Call tree         | Runtime control flow                                                 |
| Component tree    | UI structure, with the state and module boundaries that matter       |
| API-surface diff  | Changed exported symbols and signatures, grouped by file             |
| File tree         | File responsibilities or a broad refactor                            |
| Mermaid diagram   | Interactions, workflows, states, domain models, and architecture     |
| `diff` of a shape | What changes in a component, file layout, call tree, or control flow |
| Focused HTML file | A visual UI, layout, or comparison too dense for a diagram           |

When another skill names the shape it wants, `show-me` uses that shape directly. The Mermaid guide in
[`references/diagram-types.md`](skills/show-me/references/diagram-types.md) maps questions to diagram kinds.

## Requirements

None beyond an agent that loads Agent Skills. Fenced Mermaid renders inline in Claude Desktop, claude.ai, artifacts,
and pi. Terminal agents such as Claude Code and Codex CLI show it as raw text unless a Mermaid rendering hook draws it;
there the skill prefers a call tree or pseudocode.

## Installation

With [APM](https://github.com/microsoft/apm), pinned to a release:

```bash
apm install pretty-good-software-org/show-me-skill#v1.3.1
```

Without APM, copy the skill directory into your agent's skills directory, for example for Claude Code:

```bash
git clone --depth 1 --branch v1.3.1 https://github.com/pretty-good-software-org/show-me-skill.git
cp -R show-me-skill/skills/show-me ~/.claude/skills/
```

## Usage

Ask the agent to "show me" something, for example "show me the call flow when a form is submitted" or "diagram this
state machine". The skill's [`SKILL.md`](skills/show-me/SKILL.md) holds the shapes and when to use each.

## Development

Development uses [mise](https://mise.jdx.dev/), which installs the pinned tools from the lock files:

```bash
mise run setup:default
mise run lint:default
mise run test:default
```

`setup:default` also installs the Git hooks. Changes are recorded with [Changie](https://changie.dev/) in `.changes/`
and merged into [`CHANGELOG.md`](CHANGELOG.md).

## License

[MIT](LICENSE)
