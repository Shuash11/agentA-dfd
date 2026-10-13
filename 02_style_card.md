# AgentA DFD — Style Card (v1, reference-informed)

> **Purpose:** the conventions every AgentA DFD file follows.
> **Reference images = CONTEXT ONLY.** They showed what a student/college-standard DFD looks like
> (approach: simple, black-and-white, numbered processes and stores, level hierarchy, narrative
> words). We adopt the *standard and approach* — we do **not** copy their content, their school
> letterhead, or decorative flourishes. All content comes ONLY from `00_narrative_reference.md`
> plus the scope rule (user-facing actions only).

---

## 1. Notation (one family everywhere — Gane & Sarson-flavored)

| Symbol | Shape | Rules |
|---|---|---|
| **Process** | Sharp rectangle with a horizontal divider band near the top; **ID in the band** (`1.0`), name centered below | Verb + object, Title Case, 1–4 words |
| **External entity** | Plain sharp rectangle, name centered, placed at the **page edges** | Allowed entities ONLY: `End User`, `AI Service (Online)`, `Email`, `Device` |
| **Data store** | **Open-ended rectangle** — the TOP edge, BOTTOM edge, LEFT edge and a vertical DIVIDER are drawn, but there is **NO right edge**: the box is open on the right. A small compartment on the left holds the D-number; the wider area to its right holds the store name (`D1 │ User Accounts`) | Connects only to processes; has both an in-flow and an out-flow overall |
| **Data flow** | Thin straight/orthogonal black line, **single solid arrowhead**, one short data-name label (`Sign-in details`, `Credentials`, `Chat message`, `AI reply`) | Never bidirectional, never numbered |
| **Overall style** | Pure **black on white** (`#000` on `#FFF`), uniform thin lines, no color, no fills, no shadows, no icons | Diagram labels: small sans (Arial/Calibri). Page text: serif (Times New Roman). Headings: bold serif |

### The data store symbol — exact construction

A data store is drawn as an **open-ended rectangle**. The divider sits about **40px** from the left
edge, the D-number is centred at `x0+20`, and the store name is centred in the remaining width:

```html
<path class="bp" d="M{x0},{y0} H{x0+W} M{x0},{y0+H} H{x0+W} M{x0},{y0} V{y0+H} M{x0+40},{y0} V{y0+H}"/>
```

That is four strokes — top edge, bottom edge, left edge, divider. **Nothing is drawn on the right.**

- It **MUST NOT** be drawn as a closed rectangle.
- It must not look like `D5 |`, with a full-height divider as the main visual feature. The divider
  reads as a small left compartment; the open right side is what makes the symbol a data store.

## 2. Numbering (fixed across the whole set)

- **Context Diagram:** one process, ID **0**, named `AgentA`.
- **Level 0 (Diagram 0):** processes `1.0 … 5.0` — `1.0` Register · `2.0` Login · `3.0` Chat ·
  `4.0` Profile & Account · `5.0` Forgot Password.
- **Level 2:** children of parent `X.0` → `X.1, X.2, … X.n` (3–6 per diagram). No deeper levels.
- **`3.0` is named simply `Chat`** — not "Chats", and not "Chat with Coach". Both longer names were
  rejected.
- **Removed processes:** Model Download and Image Generation were **REMOVED at the instructor's
  request** and no longer exist in the set. There is no process 6.0 or 7.0, and no figure for them.
- **Data stores:** `D1` User Accounts · `D2` Chats · `D3` Messages · `D4` AI Model · `D5` Session —
  identical ID + name in every file they appear.

## 3. The deliverable set — ONE diagram per separate file (in `C:\Users\joashua\Downloads\dfd-generator-zen`)

| # | File name | Heading | Caption | Parent |
|---|---|---|---|---|
| 1 | `Figure 1 - Context Diagram.html` | CONTEXT DIAGRAM | Figure 1. Context Diagram of the AgentA System | process 0 |
| 2 | `Figure 2 - Level 0 DFD (Diagram 0).html` | LEVEL 0 DFD (DIAGRAM 0) | Figure 2. Level 0 DFD (Diagram 0) of the AgentA System | — |
| 3 | `Figure 3 - Registration DFD.html` | LEVEL 2 DFD PROCESS 1.0 (REGISTRATION) | Figure 3. Level 2 DFD Process 1.0 (Registration) | 1.0 |
| 4 | `Figure 4 - Login DFD.html` | LEVEL 2 DFD PROCESS 2.0 (LOGIN) | Figure 4. Level 2 DFD Process 2.0 (Login) | 2.0 |
| 5 | `Figure 5 - Chat DFD.html` | LEVEL 2 DFD PROCESS 3.0 (CHAT) | Figure 5. Level 2 DFD Process 3.0 (Chat) | 3.0 |
| 6 | `Figure 6 - Profile & Account DFD.html` | LEVEL 2 DFD PROCESS 4.0 (PROFILE & ACCOUNT) | Figure 6. Level 2 DFD Process 4.0 (Profile & Account) | 4.0 |
| 7 | `Figure 7 - Forgot Password DFD.html` | LEVEL 2 DFD PROCESS 5.0 (FORGOT PASSWORD) | Figure 7. Level 2 DFD Process 5.0 (Forgot Password) | 5.0 |

### Level-2 skeletons (as built)

- **1.0 Registration** (End User · D1): 1.1 Enter Sign-Up Details · 1.2 Submit Registration ·
  1.3 Display Recovery Code
- **2.0 Login** (End User, Device · D1, D5): 2.1 Choose Sign-In Method · 2.2 Enter Credentials ·
  2.3 Verify Credentials · 2.4 Unlock with Biometric · 2.5 Open Dashboard · 2.6 Sign Out
- **3.0 Chat** (End User, AI Service (Online) · D2, D3, D4): 3.1 Open Chat List · 3.2 Create New Chat ·
  3.3 Enter Message · 3.4 Select AI Engine · 3.5 Receive AI Reply · 3.6 Delete Chat
- **4.0 Profile & Account** (End User · D1, D5): 4.1 View Profile · 4.2 Edit Profile ·
  4.3 Save Changes · 4.4 Change Password · 4.5 Delete Account · 4.6 Confirm Deletion
- **5.0 Forgot Password** (End User, Email · D1): 5.1 Enter Email · 5.2 Request Code ·
  5.3 Enter Code · 5.4 Verify Code · 5.5 Set New Password · 5.6 Confirm Password Changed

**Balancing required:** the flows crossing into/out of each Level-2 diagram must match the flows
touching its parent `X.0` on the Level 0 (Diagram 0) figure.

## 4. Page furniture (same simple layout in every file)

1. **Header line:** `AgentA` (left) · `Data Flow Diagrams` (right), thin rule below.
   NO college names, NO logos.
2. **Heading:** centered, bold — e.g. `CONTEXT DIAGRAM` / `LEVEL 2 DFD PROCESS 1.0 (REGISTRATION)`.
3. **The diagram** (inline SVG).
4. **Caption below the diagram**, centered italic: `Figure N. Level 2 DFD Process X.0 (Name)`.
5. **"Narrative Flow of Data"** paragraph (5–8 sentences, present tense, plain words — a human must
   be able to read the diagram from this paragraph: name every process and store by ID, and
   describe every flow).
6. **Footer:** left `AgentA | Data Flow Diagrams` · right `Page N of 7`.

## 5. Drawing rules

- Left→right flow; entities on the edges; stores along the top/bottom margins; processes center.
- **Every DFD must have small boxes.** All boxes are small.
- **The external entity (user) box must be SMALL** — a small plain rectangle. Never a tall vertical
  bar, and never a 3D or shaded box.
- **Do not push the boxes to be consistent sizes across all DFDs, because some diagrams are small.**
  Size each diagram on its own content. Figure 2's Level 0, for example, uses 150×56 process boxes
  and a 120×56 entity box, while the Level 2 figures are sized to their own layouts. There is no
  single global pixel size applied to all seven files.
- Counts: Context = exactly 1 process + 4 entities, **no stores**; Level 0 = one End User plus the
  five main user functions; Level 2 = 3–6 processes.
- **The Level 0 / Diagram 0 figure shows exactly ONE `End User` entity and the five main user
  functions left to right, with NO data stores and no other entities.** This is the instructor's
  explicit instruction: "this is it, no need anything else, just one user from left to right".
  Data stores first appear on the Level 2 figures.
- **Level 0 flow labels (the approved chain):**
  `End User →[sign-up details]→ 1.0 →[new account]→ 2.0 →[chat message]→ 3.0 →[profile details]→
  4.0 →[reset request]→ 5.0`, plus the return flow `5.0 →[new password]→ 2.0`.
  The return arrow exists because without it `5.0 Forgot Password` was a dead-end process with no
  output, which breaks the rule that every process has at least one output.
- **Avoid line crossings wherever practical** — prefer direct horizontal/vertical routes. A FEW
  clearly drawn crossings (≤4) are acceptable in this deliverable; do not agonize over geometry.
  Never draw leaning/slanted wires across the drawing just to dodge a crossing.
  No bidirectional arrows (split into two); every process ≥1 in + ≥1 out; no entity→entity,
  entity→store, store→store, or store→entity flows.
- **Human labels only** — no code identifiers (`is_synced`, `auth.uid`, `user_id`), no backend
  jargon (RLS, sync engine, tombstones, API, 429). Simple, natural, report-style English.
- Scope: user-visible actions only (scope rule in `00_narrative_reference.md`).

## 6. Delivery format

- **Primary:** self-contained **HTML with inline SVG** — no external refs, no CDN, no JavaScript,
  system fonts only. Prints to PDF as crisp black-and-white on A4/Letter.
- **Fallback:** standalone `.svg` per diagram.

## 7. Reviewer checklist (verify each file against this)

1. The file is one of the seven deliverables, correctly named: `Figure 1 - Context Diagram.html` ·
   `Figure 2 - Level 0 DFD (Diagram 0).html` · `Figure 3 - Registration DFD.html` ·
   `Figure 4 - Login DFD.html` · `Figure 5 - Chat DFD.html` ·
   `Figure 6 - Profile & Account DFD.html` · `Figure 7 - Forgot Password DFD.html`.
2. The system is named **AgentA** everywhere — process 0, heading, caption and narrative. The words
   "AI Skill Coach" do not appear in any file.
3. Page furniture complete: header `AgentA` (left) / `Data Flow Diagrams` (right) with a thin rule
   below; centered heading; diagram; `Figure N. …` caption; "Narrative Flow of Data" paragraph;
   footer `AgentA | Data Flow Diagrams` (left) / `Page N of 7` (right).
4. One notation family across all files; the four symbol shapes match this card; pure #000 on #FFF —
   no color, fills, shadows, gradients, icons.
5. Data stores are **open-ended rectangles** — top edge, bottom edge, left edge and a divider, with
   no right edge — never a closed rectangle. Small D-number compartment on the left, store name in
   the wider right area. Store IDs D1–D5 identical everywhere.
6. Numbering correct and consistent: Context = process 0; Diagram 0 = 1.0–5.0; each Level 2 = X.1–X.n
   under its stated parent; no skips or duplicates.
7. **No Model Download and no Image Generation** process, figure, flow or store anywhere in the set.
8. Figure 2 (Level 0 / Diagram 0) shows exactly one small `End User` box and the five functions
   `1.0 Register` → `2.0 Login` → `3.0 Chat` → `4.0 Profile & Account` → `5.0 Forgot Password` left
   to right, with no data stores and no other entities. The return flow `5.0 →[new password]→ 2.0`
   is present.
9. Every box is small, including the external entity box — a small plain rectangle, never a tall
   vertical bar and never a 3D/shaded box. Sizes are chosen per diagram, not forced to one global
   pixel size across all seven files.
10. Every process ≥1 input and ≥1 output; every store ≥1 input and ≥1 output overall; no illegal flows
    (entity↔entity, entity↔store, store↔store, entity→process exclusion, etc.); no bidirectional arrows.
11. Each Level-2 diagram balanced with its parent X.0 (boundary flows match).
12. Context diagram = process 0 + the 4 entities + labeled flows only, NO data stores.
13. Every flow carries exactly one short data-name label; process names are verb phrases; no code
    identifiers or backend jargon anywhere.
14. Narrative matches the graphic (processes/stores named by ID; nothing contradicted).
15. Scope rule holds: user-visible actions only; only the 4 entities; no Supabase/GitHub/sync internals.
16. Opens and prints at 100% with no clipped text.
