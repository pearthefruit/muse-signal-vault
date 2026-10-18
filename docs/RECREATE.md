# Recreate

How to recreate the Signal Vault artifact from scratch. Written for the owner; assumes a Muse account with web artifacts enabled.

## 1. Connect provider keys

For each provider (Mistral, Gemini, OpenRouter, Cerebras, Groq, USPTO, FRED): store the API key in the Secure Vault via the API-access flow, then author a connector doc following the `custom_connector_setup` skill. Keep one value per connector — multi-key rotation needs one connector per key. Verify each with a live call before relying on it:

- Mistral: list models (`GET /v1/models`, Bearer auth).
- Gemini: list models (`GET /v1beta/models`, `X-Goog-Api-Key` header).
- OpenRouter: `GET /v1/auth/key` (Bearer). A 401 "Missing Authentication header" with a verified surrogate mechanism means the stored credential is empty — re-enter it.
- Cerebras / Groq: `GET /v1/models` (Bearer). A Cloudflare 403/1010 is an egress-fingerprint block, not a key verdict.
- USPTO: `POST /api/v1/patent/applications/search` with `X-API-Key` header; body uses `q` / `sort` / `pagination` / `fields` (not `size` / `page`).
- FRED: `GET /fred/v2/release/observations?release_id=52&format=json` (v2 is release-oriented; responses nest under `release` / `series`).

Reference implementations: `connectors/custom.<provider>/bin/`.

## 2. Create the artifact

Create a private fullstack web artifact (`public_web_read` for research fetches; no public link — interactive artifacts are private-only). Data model: companies, jobs, classifications, dossiers, dossier events, runs, reports, hiring snapshots, provider test results.

## 3. Build the six stages

Declared actions per company file: `detectBoard`, `collectJobs`, `classifyJobs`, `hiringAnalysis`, `financialResearch`, `generateBriefing`, plus `runFallback` (manual Muse-plan fallback per failed run), `cancelRun`, `updateCompany`, `testLlmChain`, `listCompanies`.

- **Scrapers:** mirror [job-sniper](https://github.com/pearthefruit/job-sniper)'s `scraper/` modules — `career_page.py` (JSON-LD → CSS selectors → LLM fallback, httpx only), `ats_api.py` (Greenhouse/Lever/Ashby), `extractors.py`, `selectors.py`, `dedup.py`.
- **LLM stages:** route through the provider chain (Mistral → Gemini → OpenRouter → Cerebras → Groq), record the serving provider per run, park with per-provider reasons on total failure, never fall back to plan quota silently.
- **Financials:** SEC EDGAR XBRL for public companies (cite filings); FRED v2 release observations for the macro backdrop; web-research path for private companies. Match tickers/CIKs exactly — never substring-match company names against EDGAR.
- **Patents:** USPTO ODP application search by assignee; store portfolio summaries on the dossier; feed into briefings.

## 4. Verify end-to-end

Provider chain test (expect mixed results on free tiers), a real board collection (e.g. Stripe's Greenhouse board), a private-company financial run (e.g. Deloitte), and a regeneration self-healing check. Confirm a failed keys run parks with reasons and the pipeline buttons stay usable.
