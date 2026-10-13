# AgentA — Data Flow Diagrams

Nine data flow diagrams for the AgentA app, plus the multi-agent OpenCode system that draws them.

![context diagram](Figure%201%20-%20Context%20Diagram.html)

## What is in here

**Deliverables**

| File | What it is |
|---|---|
| `00_narrative_reference.md` | Shared context: scope rule, entities, processes, data stores |
| `01_reference_image_notes.md` | Notes on the reference screenshots |
| `02_style_card.md` | Typography and layout rules the diagrams follow |
| `Figure 1` – `Figure 9` | Rendered diagrams: context, level 1, login, registration, forgot password, chat, image generation, model download, profile |
| `AgentA - Data Flow Diagrams.docx` / `.pdf` | Submission document |
| `*.jpeg` | Reference screenshots |

**Agent system** — `.opencode/agent/`

| Agent | Model | Permission | Job |
|---|---|---|---|
| `dfd-leader` | `space-bunny-free` | — | Talks to you, drives the loop |
| `dfd-researcher` | `longcat-2.5-preview-free` | read | Establishes DFD conventions |
| `dfd-designer` | `space-bunny-free` | **write** | Writes the diagram file |
| `dfd-summarizer` | `mimo-v2.6-flash-free` | read | Decides what the diagram may show |
| `humanizer` | `ling-3.1-flash-free` | read | Rewrites labels into plain language |
| `dfd-reviewer` | `step-5-preview-free` | read | Returns PASS or FAIL — the only stop condition |

Only `dfd-designer` can write files. Everything else reports back.

## Setup

```bash
git clone <this-repo>
cd dfd-generator-zen
cd .opencode && npm install
```

Then in OpenCode, authenticate once:

```text
/connect          # choose OpenCode, paste your API key
/models           # confirm the free models are visible
```

Free models still require an account and a key — they are free to use, not anonymous.

## The loop

```
researcher → designer → summarizer → humanizer → designer → reviewer
                 ↑                                          │
                 └──────────── FAIL, repeat ───────────────┘
```

1. **researcher** picks the best format and the notation rules
2. **designer** writes the diagram
3. **summarizer** challenges it — returns `KEEP`, `CUT`, or `MOVE DOWN` per element
4. **humanizer** rewrites the labels that survived
5. **reviewer** returns PASS or numbered problems

The summarizer is the piece that stops the diagram from becoming a wall of boxes. It enforces a hard limit of **3–9 processes per diagram** and cuts decision diamonds, loops, stores on a context diagram, and read-only or write-only stores.

## Model notes

All models are OpenCode Zen free tiers. **No agent reviews work produced by the same model that made it** — the designer and the PASS/FAIL gate are deliberately different models, because a model tends to approve its own output.

Three caveats:

- **Every free tier is a limited-time offer.** The team is using the window for feedback and can withdraw any of them.
- **Two agents may have their data used** to improve the model during the free period (`mimo`, `ling`). The designer, the gate, and the researcher run zero-retention models.
- **Most of these models are unverified.** `space-bunny-free` is the only one we have actually run.

## Known gaps

Be aware of these before relying on it:

- **The loop has no round limit and no deadlock escape.** `dfd-leader.md` says to keep going until the reviewer passes. If the reviewer holds a position the designer cannot satisfy, it will loop indefinitely. Fix this before a long unattended run.
- **Black-on-white may need explicit config.** Mermaid applies a coloured default theme unless overridden with `themeVariables`. The designer is not currently told how to force it, and the reviewer will FAIL the diagram if it renders in colour.
- **`variant: max` may not apply to Zen models.** It was carried over from the previous provider and is unconfirmed.
- **`package-lock.json` is not committed.** `npm install` regenerates it, but you will not get a byte-identical dependency tree.
