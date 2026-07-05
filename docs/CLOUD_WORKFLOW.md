# Cloud Workflow

How to research on any device, keep conversations accessible on iOS, and integrate findings into the archive on Windows.

## What Lives Where

| Layer | Tool | Cloud? | Visible on iOS? |
| --- | --- | --- | --- |
| Research conversations | ChatGPT project **Main Street** | Yes (OpenAI) | Yes — ChatGPT app |
| Archive records | Git repository (GitHub) | Yes (when pushed) | Yes — GitHub app, browser, Working Copy |
| Integration / validation | Cursor (desktop) | Agent runs in cloud; chat history local | Cursor iOS for cloud agents only, not full desktop chat sync |

**The archive repository is the source of truth.** ChatGPT produces handoffs; Cursor integrates them.

Cursor desktop chat history does **not** sync to iPhone like ChatGPT. For mobile-readable research dialogue, use the ChatGPT project.

## Daily Workflow

```text
1. ChatGPT (Main Street project)  →  research
2. Say "handoff"                  →  copy markdown output
3. Save to registers/research-intake/YYYY-MM-DD-topic.md
4. git push                         →  archive readable on iOS via GitHub
5. Cursor (Windows)               →  "Integrate [file] per WORKFLOW.md"
6. python scripts/validate_archive.py
```

## ChatGPT Setup (once)

1. Open ChatGPT project **Main Street**.
2. Paste short project instructions (see below).
3. Upload [`CHATGPT_PROJECT.md`](CHATGPT_PROJECT.md) as the project knowledge file.
4. Start every research chat **inside** the project.

### Project instructions (paste in ChatGPT)

```text
You support The Main Street Archive (503–507 Main Street, Oregon City, Oregon).

Follow the uploaded file CHATGPT_PROJECT.md for all rules, ID prefixes, accuracy rules, and handoff format.

Trigger commands:
- "handoff" → output ONLY the Research Session Handoff markdown file, no extra commentary
- "research: [topic]" → research with evidence types and confidence
- "check rules" → restate accuracy rules for the current topic

Never renumber IDs. Never invent certainty. Never merge The Wheel and The 505 without proof.
```

Re-upload `CHATGPT_PROJECT.md` when archive rules change.

## ChatGPT Commands

| Command | Action |
| --- | --- |
| `research: [topic]` | Start structured research |
| `handoff` | Output archive-ready intake file only |
| `check rules` | Restate accuracy rules for current topic |

Handoff filename format: `registers/research-intake/YYYY-MM-DD-short-topic.md`

## Cursor Integration Prompt

After saving a handoff file:

```text
Integrate registers/research-intake/YYYY-MM-DD-topic.md into the archive per WORKFLOW.md
```

Then validate:

```bash
pip install -r requirements.txt
python scripts/validate_archive.py
```

## iOS Access

- **Research chats:** ChatGPT iOS app → **Main Street** project
- **Archive content:** GitHub (or any Git client) → `main-street-archives`
- **Optional:** Cursor iOS app → cloud agents on this repo for integration tasks from your phone (not a full mirror of desktop chat history)

## File Checklist After a Session

- [ ] Handoff markdown saved under `registers/research-intake/`
- [ ] PDFs/images downloaded from ChatGPT and committed (or marked pending in handoff)
- [ ] Pushed to GitHub if you want phone access
- [ ] Integrated in Cursor and validator passed

## Related Docs

- [`CHATGPT_PROJECT.md`](CHATGPT_PROJECT.md) — upload to ChatGPT project
- [`WORKFLOW.md`](WORKFLOW.md) — how Cursor integrates findings
- [`registers/research-intake/README.md`](../registers/research-intake/README.md) — intake folder
