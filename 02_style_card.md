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
| **Data store** | Open-ended rectangle with a left ID compartment: `D1 │ User Accounts` | Connects only to processes; has both an in-flow and an out-flow overall |
| **Data flow** | Thin straight/orthogonal black line, **single solid arrowhead**, one short data-name label (`Credentials`, `Chat Message`, `AI Reply`, `OTP`) | Never bidirectional, never numbered |
| **Overall style** | Pure **black on white** (`#000` on `#FFF`), uniform thin lines, no color, no fills, no shadows, no icons | Diagram labels: small sans (Arial/Calibri). Page text: serif (Times New Roman). Headings: bold serif |

## 2. Numbering (fixed across the whole set)

- **Context Diagram:** one process, ID **0**, named `AgentA AI Skill Coach`.
- **Level 1 (Diagram 0):** processes `1.0 … 7.0`.
- **Level 2:** children of parent `X.0` → `X.1, X.2, … X.n` (5–9 per diagram). No deeper levels.
- **Data stores:** `D1` User Accounts · `D2` Chats · `D3` Messages · `D4` AI Model · `D5` Session —
  identical ID + name in every file they appear.

## 3. The deliverable set — ONE diagram per separate file (in `C:\projects\dfd for agenta`)

| # | File name | Heading | Caption | Parent |
|---|---|---|---|---|
| 1 | `Figure 1 - Context Diagram.html` | CONTEXT DIAGRAM | Figure 1. Context Diagram of the AgentA System | process 0 |
| 2 | `Figure 2 - Level 1 DFD (Diagram 0).html` | LEVEL 1 DFD (DIAGRAM 0) | Figure 2. Level 1 DFD (Diagram 0) of the AgentA System | — |
| 3 | `Figure 3 - Login DFD.html` | LEVEL 2 DFD PROCESS 1.0 (LOGIN) | Figure 3. Level 2 DFD Process 1.0 (Login) | 1.0 |
| 4 | `Figure 4 - Registration DFD.html` | LEVEL 2 DFD PROCESS 2.0 (REGISTRATION) | Figure 4. Level 2 DFD Process 2.0 (Registration) | 2.0 |
| 5 | `Figure 5 - Forgot Password DFD.html` | LEVEL 2 DFD PROCESS 3.0 (FORGOT PASSWORD) | Figure 5. Level 2 DFD Process 3.0 (Forgot Password) | 3.0 |
| 6 | `Figure 6 - Chat DFD.html` | LEVEL 2 DFD PROCESS 4.0 (CHAT) | Figure 6. Level 2 DFD Process 4.0 (Chat) | 4.0 |
| 7 | `Figure 7 - Image Generation DFD.html` | LEVEL 2 DFD PROCESS 5.0 (IMAGE GENERATION) | Figure 7. Level 2 DFD Process 5.0 (Image Generation) | 5.0 |
| 8 | `Figure 8 - Model Download DFD.html` | LEVEL 2 DFD PROCESS 6.0 (MODEL DOWNLOAD) | Figure 8. Level 2 DFD Process 6.0 (Model Download) | 6.0 |
| 9 | `Figure 9 - Profile & Account DFD.html` | LEVEL 2 DFD PROCESS 7.0 (PROFILE & ACCOUNT) | Figure 9. Level 2 DFD Process 7.0 (Profile & Account) | 7.0 |

### Suggested Level-2 skeletons (adapt wording if something reads awkwardly — keep it human)

- **1.0 Login** (End User, Device · D1, D5): 1.1 Choose Sign-In Method · 1.2 Enter Credentials ·
  1.3 Verify Credentials · 1.4 Unlock with Biometric · 1.5 Open Dashboard · 1.6 Sign Out
- **2.0 Registration** (End User · D1): 2.1 Enter Sign-Up Details · 2.2 Submit Registration ·
  2.3 Display Recovery Code
- **3.0 Forgot Password** (End User, Email · D1): 3.1 Enter Email · 3.2 Request Code ·
  3.3 Enter Code · 3.4 Verify Code · 3.5 Set New Password · 3.6 Confirm Password Changed
- **4.0 Chat** (End User, AI Service (Online) · D2, D3, D4): 4.1 Open Chat List · 4.2 Create New Chat ·
  4.3 Enter Message · 4.4 Select AI Engine · 4.5 Receive AI Reply · 4.6 Delete Chat
- **5.0 Image Generation** (End User, AI Service (Online) · D2, D3): 5.1 Enter Image Prompt ·
  5.2 Check Connection · 5.3 Request Image · 5.4 Show Generated Image · 5.5 Save Image to Chat
- **6.0 Model Download** (End User, AI Service (Online) · D4): 6.1 Start Download · 6.2 Show Progress ·
  6.3 Save Model · 6.4 Confirm Model Ready
- **7.0 Profile & Account** (End User · D1, D5): 7.1 View Profile · 7.2 Edit Profile · 7.3 Save Changes ·
  7.4 Change Password · 7.5 Delete Account · 7.6 Confirm Deletion

**Balancing required:** the flows crossing into/out of each Level-2 diagram must match the flows
touching its parent `X.0` on the Level 1 diagram.

## 4. Page furniture (same simple layout in every file)

1. **Header line:** `AgentA AI Skill Coach` (left) · `Data Flow Diagrams` (right), thin rule below.
   NO college names, NO logos.
2. **Heading:** centered, bold — e.g. `CONTEXT DIAGRAM` / `LEVEL 2 DFD PROCESS 1.0 (LOGIN)`.
3. **The diagram** (inline SVG).
4. **Caption below the diagram**, centered italic: `Figure N. Level 2 DFD Process X.0 (Name)`.
5. **"Narrative Flow of Data"** paragraph (5–8 sentences, present tense, plain words — a human must
   be able to read the diagram from this paragraph: name every process and store by ID, and
   describe every flow).
6. **Footer:** left `AgentA AI Skill Coach | Data Flow Diagrams` · right `Page N of 9`.

## 5. Drawing rules

- Left→right flow; entities on the edges; stores along the top/bottom margins; processes center.
- Counts: Context = exactly 1 process + 4 entities, **no stores**; Level 1 = processes 1.0–7.0;
  Level 2 = 5–9 processes.
- **Avoid line crossings wherever practical** — prefer direct horizontal/vertical routes. A FEW
  clearly drawn crossings (≤4) are acceptable in this deliverable; do not agonize over geometry.
  Never draw leaning/slanted wires across the drawing just to dodge a crossing.
  No bidirectional arrows (split into two); every process ≥1 in + ≥1 out; no entity→entity,
  entity→store, store→store, or store→entity flows.
- Branch pairs labeled on both sides: `if online` / `if offline`, `if yes` / `if no`.
- **Human labels only** — no code identifiers (`is_synced`, `auth.uid`, `user_id`), no backend
  jargon (RLS, sync engine, tombstones, API, 429). Simple, natural, report-style English.
- Scope: user-visible actions only (scope rule in `00_narrative_reference.md`).

## 6. Delivery format

- **Primary:** self-contained **HTML with inline SVG** — no external refs, no CDN, no JavaScript,
  system fonts only. Prints to PDF as crisp black-and-white on A4/Letter.
- **Fallback:** standalone `.svg` per diagram.

## 7. Reviewer checklist (verify each file against this)

1. One notation family across all files; the four symbol shapes match this card; pure #000 on #FFF —
   no color, fills, shadows, gradients, icons.
2. Numbering correct and consistent: Context = process 0; Diagram 0 = 1.0–7.0; each Level 2 = X.1–X.n
   under its stated parent; no skips or duplicates; store IDs D1–D5 identical everywhere.
3. Every process ≥1 input and ≥1 output; every store ≥1 input and ≥1 output overall; no illegal flows
   (entity↔entity, entity↔store, store↔store, entity→process exclusion, etc.); no bidirectional arrows.
4. Each Level-2 diagram balanced with its parent X.0 (boundary flows match).
5. Context diagram = process 0 + the 4 entities + labeled flows only, NO data stores.
6. Every flow carries exactly one short data-name label; branch pairs both labeled; process names are
   verb phrases; no code identifiers or backend jargon anywhere.
7. Page furniture complete: header, heading, diagram, `Figure N. …` caption, "Narrative Flow of Data"
   paragraph, footer `Page N of 9`.
8. Narrative matches the graphic (processes/stores named by ID; nothing contradicted).
9. Scope rule holds: user-visible actions only; only the 4 entities; no Supabase/GitHub/sync internals.
10. Opens and prints at 100% with no clipped text.
