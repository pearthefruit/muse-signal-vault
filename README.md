# muse-signal-vault

Signal Vault reimplemented as a **private Muse hosted web artifact** — a competitive-intelligence workbench for job-market signals, company dossiers, financial research, and patent analysis.

This repo holds the project's documentation, architecture, and provider connectors. The running app itself lives in the owner's Muse Library as a private fullstack artifact (`signal-vault`); hosted artifacts can't be exported as source, so this repo is the public record of the project — same pattern as [job-sniper](https://github.com/pearthefruit/job-sniper). The original Flask implementation is at [competitive-intel-agent](https://github.com/pearthefruit/competitive-intel-agent).

## Agent lanes

1. **Job-intelligence pipeline** — per company file: Detect board → Collect jobs → Classify → Hiring analysis. Detect accepts standard ATS boards (Greenhouse / Lever / Ashby) *or* any pasted careers-page URL (e.g. Deloitte's Avature portal). Scrapers match [job-sniper](https://github.com/pearthefruit/job-sniper)'s modules: listing-link extraction, per-posting detail from schema.org JobPosting JSON-LD, up to 150 postings per run. Classification tags department, seniority, skills, and strategic signals per role.
2. **Company dossiers + briefings** — per-company dossiers with change detection, and generated consulting briefings with a Digital Maturity Score.
3. **Financial research** — real SEC EDGAR XBRL filings with citations for public companies, plus a FRED macro backdrop. Private companies take a web-research path (proven on Deloitte: CEO, $74.5B revenue, competitors).
4. **Patent analysis** — per-company patent portfolios via the USPTO (in build).

## LLM cost strategy: free-keys-first, Muse-plan fallback

LLM calls route through the owner's provider keys first, in this order:

**Mistral → Gemini → OpenRouter → Cerebras → Groq**

The Muse plan is a **manual-only** fallback: if the keys fail on a run, the pipeline parks with the exact per-provider reasons and a "Cancel — spend nothing" option. The plan quota is only spent when the owner explicitly presses the fallback button on a failed run — never silently. (This was a repair: the first build auto-ran stages on the plan quota whenever keys hiccuped.)

## Connectors

`connectors/` holds the seven provider connectors: docs (`CONNECTOR.md`), registration (`connector.yaml`), and test helpers (`bin/`). API keys live in the Secure Vault — **never in this repo**. Helpers authenticate through surrogate credentials; the values in these files are inert without the vault.

| Connector | Host | Status (Oct 2026) |
|---|---|---|
| custom.mistral | api.mistral.ai | verified live |
| custom.gemini | generativelanguage.googleapis.com | verified live |
| custom.openrouter | openrouter.ai | 401 — stored credential likely empty, re-entry pending |
| custom.cerebras | api.cerebras.ai | inconclusive — Cloudflare 1010 egress block, not a key verdict |
| custom.groq | api.groq.com | inconclusive — Cloudflare 1010 egress block, not a key verdict |
| custom.uspto | api.uspto.gov | verified live (IBM applicant search: 373,967) |
| custom.fred | api.stlouisfed.org | verified live (v2 release observations) |

## Docs

- `docs/ARCHITECTURE.md` — pipeline stages, data model, provider chain mechanics, repair history.
- `docs/RECREATE.md` — how to recreate the artifact from scratch.

## License

MIT.
