# AgentA (aiproject) — Narrative Reference for DFD Authoring

> **Reference only.** This brief is the single shared context for the researcher, designer,
> humanizer, and reviewer. It is written in plain narrative words so that all the context
> needed to draw the diagrams is properly analyzed in one place.
> **All DFD deliverables are saved in this folder:** `C:\projects\dfd for agenta`

---

## 0. Scope rule (user's decision — overrides everything below when drawing)

- **Draw only what the user can do in the app.** Processes = user actions (login, sign up, chat,
  generate image, download model, edit profile, delete account…). Keep every diagram at the level
  of what a user of the app experiences.
- **No backend-technical machinery** the user never sees: RLS policies, password-hash internals,
  sync-engine internals (tombstones, ghost pruning, pagination, pending badges), update checks,
  deep-link plumbing, foreground-service details, connectivity plumbing, API retry/429 handling.
- Online vs offline may appear only as a simple, user-visible branch (the user sees "offline mode").
- External entities stay minimal and user-facing: **End User**, **AI Service (online)**, **Email**
  (for the password-reset OTP), **Device** (biometric unlock). No GitHub. Supabase is not drawn —
  the user's data is shown in local data stores (accounts, chats, messages, model).
- Keep it SIMPLE, BLACK-AND-WHITE, student-standard.

---

## 1. The system in plain words

AgentA ("AI Skill Coach") is a **mobile AI chat assistant** built with Flutter (Dart), shipped as an
Android app (v1.2.3+6, package `com.agenta.AgentA`). There is **no custom server** — the backend is
**Supabase** (GoTrue authentication + PostgreSQL with Row-Level Security). The app is
**offline-first**: a small AI model (**Gemma 3 1B**, ~529 MB) runs **on the phone**; when the device
is online, chat requests are instead routed to cloud AI providers (**Groq** for text, **Pollinations**
and **HuggingFace** for images). Everything the user does is written **locally first** into an SQLite
database (`agenta.db`) and later **synced** to Supabase when connectivity returns.

The app has a **single role: the End User** (the device owner). There are no admin/teacher/registrar
roles anywhere in the code. Server-side protection comes from **Supabase RLS policies** that tie
every row of data to `auth.uid()`.

---

## 2. Actors (external entities)

| Actor | Role in the flows |
|---|---|
| **End User** | Types messages, logs in, registers, manages profile; the only human actor |
| **Supabase** | Authentication (password, Google exchange, email OTP), PostgreSQL data, recovery of account — *backend internal: not drawn as an entity; its user-facing effects appear as local data stores and the emailed OTP* |
| **Google** | OAuth identity provider for Google Sign-In |
| **Groq** | Online chat AI (`allam-2-7b`, streamed tokens) |
| **Pollinations** | Image generation via URL (no API key) |
| **HuggingFace** | Image-generation fallback (Stable Diffusion 3) + hosts the Gemma model file download |
| **Device OS** | Biometric unlock (fingerprint/face), local notifications (download/foreground service), deep links |

> **Excluded per user decision:** the App Update Check feature (GitHub Releases polling,
> version dialog, APK launch) is **NOT part of any DFD** — the DFD reader does not need it.
> Do not draw it and do not list GitHub Releases as an external entity.

---

## 3. Data stores

**Local SQLite `agenta.db` (version 7)**

| Store | Key contents |
|---|---|
| `chat_sessions` | id, user_id, title, last_message, updated_at, unread, `is_synced`, `is_deleted` (tombstone) |
| `messages` | id, chat_id, text, is_user, timestamp, `is_synced`, `is_deleted` (tombstone) |
| `user_profile` | uid, display_name, email, photo_url, recovery_code |
| `pending_signups` | local_id, email, **salted SHA-256 password hash**, display_name, recovery-code hash, provider, created_at, `is_synced` |
| `offline_model_status` | model_type, status, downloaded_at, file_path, version |

**Device secure storage** (keychain/keystore): `session_uid`, `session_email`, `session_provider`,
`biometric_enabled`, `biometric_uid`.

**Remote Supabase (Postgres)**: `profiles` (id = auth.uid, email, display_name, recovery-code hash),
`chats`, `messages` — all guarded by RLS so a user can only touch their own rows.

---

## 4. How data flows, module by module (narrative)

**Boot & configuration.** The app loads its build-time configuration (endpoints, API keys injected
via `--dart-define`, with a local `.env` fallback for development), initializes Supabase, then the
SQLite database. On the very first run the user is **forced** through a model-download gate: the
Gemma 3 1B file is fetched from HuggingFace with progress, stall watchdog, cancellation, and a
foreground-service notification; its status is recorded in `offline_model_status`. Only after this
does the AuthGate decide between Login and the Dashboard. A "Continue Offline" fallback exists.

**Login & session.** With network: email/password goes to Supabase `signInWithPassword`; the session
is stashed in secure storage. Without network: the password is verified locally against the salted
hash in `pending_signups`, protected by a brute-force guard (5 failures → 5-minute lockout; 10 →
credential wipe). Google Sign-In collects a Google ID token and exchanges it with Supabase. A
biometric quick-unlock path (via the Device OS) can restore the session without retyping the
password. Signing out wipes the session, biometric flag, and stashed secrets.

**Registration & recovery code.** Email/password signup creates the account and returns a **one-time
recovery code** shown exactly once and stored only as a hash (locally and remotely). If the device is
offline, the signup is queued in `pending_signups` and flushed later by the sync engine.

**Password reset & change.** "Forgot password" asks Supabase to email a **6-digit OTP**; the user
verifies it and sets a new password (deep link `com.agenta.agenta://reset`). The recovery code can
also unlock a password change after its hash is verified. An already-authenticated user must
re-authenticate before changing the password.

**Chat messaging (the core).** The user sends a message; a router decides the engine — **Groq**
(streaming, retry/429 handling) when online, **on-device Gemma** when offline (with an 8-message
history cap), and **Pollinations/HuggingFace** for image requests. Tokens stream to the screen; every
message and chat session is persisted locally first (`is_synced = false`), and each chat is checked
for ownership before it opens.

**Local↔remote sync.** When connectivity returns, the sync engine flushes unsynced
chats/messages/signups to Supabase, pushes tombstone deletes, pulls paginated refreshes, prunes
ghost rows, and updates the pending-count badge.

**Profile & security.** Display name/email are edited on the Supabase profile and auth metadata. The
Security page explains the hash-only recovery-code policy and offers **Delete Account**, which wipes
the remote profile and local credentials.

**Cross-cutting:** a connectivity detector switches online/offline behavior everywhere; Supabase RLS
is the server-side access-control boundary on every remote flow.

---

## 5. Deliverable plan (what will be drawn, and where)

**Student/college-standard DFDs.** NOT one big page — **each diagram is its own separate file**, e.g.
the Login DFD is its own document, the Chat DFD its own, and so on.

| # | Deliverable (separate file each) | Covers |
|---|---|---|
| 1 | Context Diagram (Level 0) | Whole system as one process + all external entities |
| 2 | Diagram 0 (Level-0 decomposition) | The major processes of the system |
| 3 | Login DFD | Sign in online/offline, biometric quick unlock, sign out |
| 4 | Registration DFD | Sign up + one-time recovery code |
| 5 | Forgot Password DFD | Email OTP → set new password |
| 6 | Chat DFD | Chat list, send message, AI reply (online/offline), delete chat |
| 7 | Image Generation DFD | Generate an image inside chat |
| 8 | Model Download DFD | First-run AI model download with progress |
| 9 | Profile & Account DFD | Edit profile, change password, delete account |

**Design phases (strict order, one at a time — never bulk):**
Phase 1 = Context Diagram → Phase 2 = Diagram 0 → Phases 3–9 = one module DFD per phase.

**Style targets:** simple, black-and-white, human-readable, standard student notation
(processes numbered 1.0, 2.0…; stores labeled D1, D2…; external entities as squares; flows as
labeled arrows). Exact notation to be confirmed by the researcher from the reference images.

---

## 6. Reference images in this folder (READ ONE BY ONE)

Nine JPEG reference images of student/college DFD standards live here:

1. `205b07d7-4663-40dc-bcd2-dd4028c9a640.jpeg`
2. `3cb35168-1b89-4777-9ee3-bced01bdae43.jpeg`
3. `5eb1e4d6-9906-4cf7-8456-d88bbd20345b.jpeg`
4. `62a75648-294a-4965-aa5c-f929800d02bd.jpeg`
5. `c960d1b5-ea24-4dc7-bd82-f01c1a180160.jpeg`
6. `e8fea786-9106-4110-8ae2-a69ce0acf7b2.jpeg`
7. `ebb755b8-03ab-4485-9ccf-dd24c4ed3b4d.jpeg`
8. `feaa10c9-529e-4291-9854-cf68d482a9c1.jpeg`
9. `fed903f5-7304-4c3f-b1b4-cde8e5b490bf.jpeg`

**HARD RULE:** these are **reference only**. Read **at most ONE image per tool call**, sequentially —
never batch them, never load them all at once (payload must stay under 26,214,400 bytes).

---

## 7. Deliverable status — COMPLETE (all nine figures reviewed & PASSed)

All files live in `C:\projects\dfd for agenta`:

| File | Contents |
|---|---|
| `Figure 1 - Context Diagram.html` | Whole system as process 0 + 4 entities (no stores) |
| `Figure 2 - Level 1 DFD (Diagram 0).html` | The combined Level 1 — all 7 user processes (1.0–7.0), stores D1–D5 |
| `Figure 3 - Login DFD.html` | Level 2 Process 1.0 — login only |
| `Figure 4 - Registration DFD.html` | Level 2 Process 2.0 — registration only |
| `Figure 5 - Forgot Password DFD.html` | Level 2 Process 3.0 — forgot password only |
| `Figure 6 - Chat DFD.html` | Level 2 Process 4.0 — chat only |
| `Figure 7 - Image Generation DFD.html` | Level 2 Process 5.0 — image generation only |
| `Figure 8 - Model Download DFD.html` | Level 2 Process 6.0 — model download only |
| `Figure 9 - Profile & Account DFD.html` | Level 2 Process 7.0 — profile & account only |

**Notes:** each figure is its own separate file; per-module isolation holds at Level 2 (login = login
only, chat = chat only, etc.); every Level-2 figure is balanced against its parent process on
Figure 2; Figure 2 received two balance additions along the way (sign-out clearing the session;
deleting a chat); every figure passed the independent reviewer, is black-and-white, and carries the
header, heading, caption, "Narrative Flow of Data" paragraph, and page footer.

**Word version (for printing & editing):** `AgentA - Data Flow Diagrams.docx` — 9 pages, one figure
per page. Each page = the captured figure image (title + diagram + caption) with the
"Narrative Flow of Data" paragraph below as real, editable text (Times New Roman 12, justified).
