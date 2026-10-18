# Architecture

## Runtime

Private Muse fullstack web artifact (slug `signal-vault`). Hosted on the Muse web runtime with declared actions; the LLM-heavy stages execute through the owner's connected provider keys (Secure Vault) with the Muse plan as manual fallback. Interactive artifacts are private-only — no public link.

## Pipeline (per company file)

Six stages, run on demand from the company file:

1. **Detect board** — probes for Greenhouse / Lever / Ashby APIs; accepts any pasted careers-page URL as a board (job-sniper treats sources the same way). 15s timeouts per probe; JS-only portals (Workday) report plainly that they can't be read.
2. **Collect jobs** — scrapes the board: listing-link extraction with URL-filter rules, per-posting detail from schema.org JobPosting JSON-LD, platform pagination (e.g. Avature `jobOffset`). Up to 150 postings per run.
3. **Classify** — LLM classification per role: department, seniority, skills, strategic signals. Runs in small slices with a model-tier ladder and rate-limit backoff across the provider chain.
4. **Hiring analysis** — strategic hiring report synthesized from classifications: leadership moves, growth bets, competitive posture.
5. **Financial research** — public companies: SEC EDGAR XBRL filings with citations + FRED macro backdrop. Private companies: web-research path (executives, revenue, competitors).
6. **Generate briefing** — consulting briefing with Digital Maturity Score, grounded in the dossier.

## Dossiers and change detection

Per-company dossiers persist filings, job snapshots, and patent records. Change detection diffs new collections against the dossier and logs events (leadership changes, headcount swings, filing updates).

## Provider chain mechanics

Every LLM stage tries providers in order — **Mistral → Gemini → OpenRouter → Cerebras → Groq** — and records which provider served the run. Classification uses a tier ladder within providers (e.g. Mistral large → small) with backoff on 429s. A keys failure parks the run with per-provider reasons; the operator chooses "Cancel — spend nothing" or the manual Muse-plan fallback for that run.

## Report history

Generated outputs (financial reports, hiring analyses, briefings) are append-only per company file. A regenerated report supersedes the previous one; history is preserved.

## Repair history (Oct 2026)

- **Pipeline repair:** the first build silently auto-ran stages on the Muse plan when keys hiccuped (burning quota), wedged the pipeline buttons permanently on a keys failure, filed ITT Inc's EDGAR financials under Deloitte via substring name matching ("deloitte" contains "itt"), and could hang on board detection. Fixed: manual-only fallback, parked runs with reasons + cancel option, private-company path with ticker/CIK self-healing, 15s detection timeouts, sliced classification with backoff.
- **Scraper alignment:** scrapers matched to job-sniper's modules; Detect accepts pasted careers-page URLs (Deloitte's Avature portal verified: 150 postings collected with JSON-LD detail extraction).
