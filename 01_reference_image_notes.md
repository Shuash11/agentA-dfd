# Reference image notes (analyzed ONE image per isolated task, sequentially)

## Image 1 — `205b07d7-4663-40dc-bcd2-dd4028c9a640.jpeg`
- **Notation family:** Gane & Sarson (Level-0 / Context Diagram), not Yourdon.
- **Shapes:** Process = rectangle with a horizontal divider band across the top; the ID ("0") sits in that band, process name ("TCGC ROTC MANUAL PROCESS") in ALL CAPS below. External entities = 3D/shaded boxes ("Cadet," "Staff") each with a small "Id" corner tag. Data store = none shown (context diagrams omit stores). Data flow = simple straight black arrows.
- **Flow labeling:** plain lowercase phrase above each arrow ("fill-up form," "submit form," "validate form," "approve reject application"); paired arrows for two-way exchange. Numbering: single process "0."
- **Layout:** horizontal, symmetric — central process, Cadet left, Staff right; 2 external entities, 1 process, 4 flows.
- **Style:** pure black-and-white, thin lines, Times-style serif text; only flourish is the 3D entity boxes.
- **College-standard touches worth copying:** preceding "Narrative Flow of Data" paragraph; bold centered heading ("CONTEXT DIAGRAM: ..."); formal italic caption "Figure 2. Context Diagram of the Current System"; bordered thesis page with school header. Simple, readable, no decorative clutter.

## Image 2 — `3cb35168-1b89-4777-9ee3-bced01bdae43.jpeg`
- **Notation family:** Gane & Sarson. Process = plain rectangle; external entity = open-sided "3D box" (rectangle with left bar), labeled "Id | Staff" / "Id | Cadet"; data store = open-ended rectangle with ID box, "D1 | User Accounts"; flow = thin line, solid arrowhead.
- **Flows/labels:** Arrows are unlabeled — all text sits inside symbols. Numbering: processes 2.1–2.5 (decimal child numbering), store D1.
- **Layout:** Level-2 decompositions titled "Level 2 DFD Process 2.0": two variants (Staff, Cadet). Each is a horizontal left-to-right chain of 5 processes — Click Log-in → Input Email Address → Input Password → Verify Credentials → Click Log-in Button; entity far left; D1 sits above, feeding process 2.4 via a down arrow.
- **Style:** pure black-and-white, thin uniform line weights, hard-edged boxes, no color, no shadows (entity "box" is line-drawn), small sans-serif labels, white background.
- **Student-standard markers:** college header (Tangub City Global College — same thesis as image 1), formal figure captions, a "Narrative Flow of Data" paragraph preceding each diagram, consistent box sizing, standard decimal process/store numbering.

## Image 3 — `5eb1e4d6-9906-4cf7-8456-d88bbd20345b.jpeg`
- **Notation family:** Classic Yourdon/DeMarco-style context diagram, but process drawn as a plain rectangle (no rounded corners). External entities = 3D "tabbed" boxes (draw.io/MS-Word style).
- **Shapes:** Process = rectangle, ID "0" in top-left corner, name centered: "TCGC ROTC: A web-based online enrollment system". External entities = 3D boxes with small "Id" tab — "Cadet" (left), "Staff" (right). Data stores NOT shown on context diagram (narrative names them: "User Accounts", "Enrollment Applications"). Flows = thin single-line arrows with inline labels.
- **Labels/numbering:** Flow labels are verb phrases in sentence case ("Register Log-in account", "Submit Enrollment", "Approve Reject Applications", "Generate Reports"). Context process = 0; text states Level 1 numbers processes 1.0–9.0.
- **Layout:** Horizontal — Cadet left, Staff right, single system process center; several parallel arrows stacked on the staff side.
- **Style:** Pure black-and-white; gray shading only on the 3D entity boxes; clean thin lines.
- **Student/college markers:** School header + logo ("Tangub City Global College Institute of Computer Studies"), page number, "Figure 3." caption, "Narrative Flow of Data" paragraph tying processes/data stores to the diagram.

## Image 4 — `62a75648-294a-4965-aa5c-f929800d02bd.jpeg`
- **Notation family:** Hybrid (college style) — rectangular "module-style" process boxes, 3D external entity, tabbed data store. Figure 14, thesis page 17.
- **Shapes:** Process = plain rectangle, number in a top band (6.5.1–6.5.4) with name below ("View Deleted records", "Select Record to View", "Retrieve", "Display confirmation message", "Cancel"). External entity = 3D shadowed box ("Staff", with "Id" tab). Data store = rectangle with left tab: "D1 | Reports" (D-number + name). Flow = thin straight black arrow, horizontal, mostly unlabeled; branch flows labeled "if yes" / "if no".
- **Numbering:** Decimal decomposition 6.5.1–6.5.4 (Level 3 of process 6.5); store D1.
- **Layout:** Left-to-right sequence: Staff → 6.5.1 → 6.5.2 → 6.5.3 → 6.5.4 (yes) / Cancel (no); D1 above feeding 6.5.4. Explicitly titled as a Level-3 DFD of process 6.5.
- **Style:** Black-and-white, thin lines, light 3D shadow only on entity box.
- **Student-standard markers:** College letterhead ("Tangub City Global College Institute of Computer Studies"), page number, numbered figure caption, aligned balanced boxes — classic capstone-thesis DFD.

## Image 5 — `c960d1b5-ea24-4dc7-bd82-f01c1a180160.jpeg`
- **Notation family:** Hybrid — Gane & Sarson influence (process = rounded rectangle), external entities use the 3D "box with corner tab" symbol. Classic college/SSADM textbook mix. Same TCGC ROTC enrollment system, Figure 3 variant.
- **Symbols:** Process = single rounded rectangle, numbered "0", labeled "TCGC ROTC: A web-based online enrollment system" (context). External entities = 3D boxes with tab, "Cadet" (left) and "Staff" (right). Data store = none drawn (narrative mentions "User Accounts", "Enrollment Applications"). Flows = plain straight arrows with text labels above them.
- **Labeling:** verb-phrase flows ("Register-Log-in account", "Upload Requirements", "Approve/Reject Applications"). Context process = 0; narrative references Level-1 processes 1.0–9.0 and stores D1–D2.
- **Layout:** Horizontal — inputs left→right, outputs right→left, arrows fanned vertically on the right. Clear, symmetric, few crossings.
- **Style:** Pure black-and-white line art, no color, no shadows, no decoration.
- **Why it's good student standard:** clean fan-out routing, verb-labeled arrows, one named system process, figure caption + paragraph narrative tying diagram to text.

## Image 6 — `e8fea786-9106-4110-8ae2-a69ce0acf7b2.jpeg`
- **Notation family:** Gane & Sarson. Processes = plain rectangles with a small number compartment in the top-left corner. Figure 12.
- **Process:** rectangle, number in top-left box (6.1–6.4 / 7.1–7.4), action label centered ("Click View", "Select Specific Records").
- **External entity:** 3D/folder-style square with a small ID box — "Staff", placed left.
- **Data store:** open-ended rectangle with small ID square on the left — "D1 Reports", right/top.
- **Flows:** single-headed thin arrows labeled with short verb phrases ("Select Application to Manage", "Click Delete"); store flows labeled ("Reports").
- **Numbering:** hierarchical Level-2 decomposition of processes 6.0 and 7.0 → 6.1–6.4, 7.1–7.4; store D1.
- **Layout:** left-to-right; entity → processes → branch to data store; ~4 processes per figure. Titled "Level 2 DFD".
- **Style:** pure black-and-white, thin uniform lines, no shadows, no color.
- **Student/college markers:** college letterhead + page number, numbered figure captions ("Figure 12. Level 2 DFD Process 6.0…"), "Narrative Flow of Data" paragraph under each diagram, consistent symbol reuse across figures.

## Image 7 — `ebb755b8-03ab-4485-9ccf-dd24c4ed3b4d.jpeg`
- **Notation family:** Gane & Sarson-style — sharp-cornered rectangles (no circles, no rounded corners).
- **Shapes:** Process = rectangle holding "6.x + verb" text (6.1 Click Manage Enrollees … 6.8 Notify Students). External entity = small rectangle "Staff". Data store = small rectangle prefixed **D1 Enrollment Status**, **D2 Reports**. Flow = thin black orthogonal arrows with arrowheads.
- **Flows/numbering:** Arrows sparsely labeled with condition words ("approved", "if reject"); processes decimal-numbered 6.1–6.9 (decomposition of Process 6.0); stores D1/D2.
- **Layout/structure:** Two Level-2 DFDs (Figures 10 & 11) decomposing Process 6.0; left-to-right: Staff → 6.1 → 6.2 → branch → 6.4 Select → confirmation/notify branch → D1/D2. ~7–9 processes each.
- **Style:** Pure black-and-white, thin lines, no shadows/fills/color; serif captions.
- **College-standard markers:** Captions "Level 2 DFD Process 6.0", "Narrative Flow of Data" paragraph above each figure, decimal process IDs, D-prefixed stores, school letterhead with logo and page number.

## Image 8 — `feaa10c9-529e-4291-9854-cf68d482a9c1.jpeg`
- **Notation family:** Gane & Sarson. Processes = rounded rectangles with number + verb name (1.0 Create Account … 9.0 Retrieve Cadet Records). External entities = small 3D-corner boxes ("Cadet", "Staff"). Data stores = open-ended rectangles D1–D4 (D1 User Accounts, D2 Enrollment Applications, D3 Enrollment Status, D4 Reports). Flows = plain arrows labeled with the data name they carry.
- **Numbering:** Level 1 uses 1.0–9.0; decomposition uses 1.1–1.9. Stores D1–D4. Arrows unnumbered, labeled only with data names.
- **Layout:** Two B&W diagrams on one thesis page: "Diagram 0 / Figure 4 Level 1 DFD" (≈9 processes, left-to-right with Cadet and Staff surrounding) and "Figure 4 Level 2 DFD Process 1.0 (Create Account)" — horizontal chain 1.1 → 1.9 that loops back into D1 User Accounts.
- **Style:** Pure black line art on white; no color, no drop shadows; small sans labels.
- **Student-standard markers:** School header (Tangub City Global College, page, logo), numbered figure captions, "Narrative Flow of Data" prose, balanced 7±2 decomposition, short human-readable labels.
- **KEY TAKEAWAY:** this is the exact hierarchy to mirror — Context Diagram → Level 1 DFD (Diagram 0, processes 1.0–9.0) → "Level 2 DFD Process X.0" per module (e.g., X.1–X.n).

## Image 9 — `fed903f5-7304-4c3f-b1b4-cde8e5b490bf.jpeg`
- **Notation:** Gane & Sarson-flavored. Processes = plain rectangles split by a top compartment holding the number (4.1–4.19, 5.1); external entities = 3D perspective boxes labeled "Cadet"; data stores = open-ended rectangles with the ID in a left compartment ("D3 Enrollment Applications", "D3 Enrollment Status"). Page 14.
- **Flows:** thin plain black arrows; almost all unlabeled. A single arrow joins 4.19 to D3; Figure 9 shows Cadet → 5.1 and D3 → 5.1.
- **Numbering:** hierarchical parent.child (4.0 → 4.1–4.19; 5.0 → 5.1); stores D-prefixed.
- **Layout:** Level 2 decompositions; Figure 8 is boustrophedon (serpentine, row drops to fit the page); Figure 9 is a simple top-down mini-flow.
- **Style:** pure black-and-white line art, no color/fill/shadows, uniform thin strokes; college letterhead with logo and page number.
- **Student-standard markers:** formal captions ("Figure 8. Level 2 DFD Process 4.0 (Submit Enrollment)"), italic "Narrative Flow of Data" paragraph per figure, consistent hierarchical numbering and D-IDs.

---

## Consolidated pattern (all 9 images, same capstone thesis)
- **Family:** Gane & Sarson-flavored hybrid, consistently reused: process = rectangle w/ number compartment (top band / top-left box); external entity = 3D tabbed box; data store = open-ended rectangle with left "D# | Name" tab; flows = thin black arrows.
- **Hierarchy:** Context Diagram (process 0) → Level 1 DFD ("Diagram 0", processes 1.0–9.0) → Level 2 DFD per process ("Level 2 DFD Process X.0 (Name)", processes X.1–X.n).
- **Page furniture per figure:** college letterhead + page number, bold centered heading, formal caption "Figure N. Level 2 DFD Process X.0 (Name)", italic-伴 "Narrative Flow of Data" paragraph (prose explaining the flows), pure black-and-white, thin uniform lines, serif captions, small sans labels.
- **Layout:** left-to-right; entities on the edges; balanced loads (~5–9 processes); avoid line crossings; condition branches labeled "if yes" / "if no" / "approved" / "if reject".
- **Deliverable rule (ours):** ONE diagram per separate file (user requirement) — unlike the thesis which put multiple figures per page.
