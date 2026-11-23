# 008 — Identity Resolution Across CRM, Support and Product Data (dbt)

**Status: planned, not started.** This README is the brief. An agent picking this up should read it end to end before writing anything.

## Goal

Build one account-level and one person-level view of a B2B SaaS customer from three sources that **do not share an identifier**:

| Source | Fivetran dbt package | What it says about the customer |
|---|---|---|
| HubSpot (CRM) | [`fivetran/dbt_hubspot`](https://github.com/fivetran/dbt_hubspot) | companies, contacts, deals, engagements, lifecycle stage history |
| Intercom (support) | [`fivetran/dbt_intercom`](https://github.com/fivetran/dbt_intercom) | companies, contacts, conversations (history mode, SCD2) |
| Amplitude (product) | [`fivetran/dbt_amplitude`](https://github.com/fivetran/dbt_amplitude) | product events per user and group |

The question the final mart must answer: *which accounts use the product less, write to support more, and are close to renewal?*

## Data

No connectors and no API calls. Raw tables come from the synthetic seed CSVs that Fivetran ships in each package under `integration_tests/seeds/` (same schema as a real Fivetran sync, a handful of rows each). Copy the needed files into `seeds/`, pin the package version they came from in this README.

Useful columns already in the seeds (checked 2026-11-23):

- HubSpot `contact_data.csv`: `id`, `property_email`, `property_company`; `company_data.csv`: `id`, `property_name`, `property_address`, `property_city`.
- Intercom `company_history_data.csv`: `id`, `company_id` (external id), `website`, `name`, `_fivetran_active/_start/_end`; `contact_history_data.csv`: `id`, `email`, `external_id`, `custom_organisation_id`, history columns; `contact_company_history_data.csv`: contact ↔ company bridge.
- Amplitude `amplitude_event_data.csv`: `user_id`, `device_id`, `amplitude_id`, `groups`, `event_type`, `event_time`.

## Step 0 — make the ids disagree on purpose

The seeds come from different packages, so their ids never match. Generate **additional rows** (a small Python script with a fixed random seed, output to `seeds/`) that describe the same ~20 fictional companies and ~60 people across all three sources, with realistic drift:

- emails differ by case, `+alias`, or a personal address in one system (`Anna.Kowalska+trial@shop.pl` vs `anna.kowalska@shop.pl` vs `ania.k@gmail.com`);
- company names differ in legal suffix and spelling (`Sklep Kowalski sp. z o.o.` vs `sklep kowalski` vs `SklepKowalski`), website with/without `www.` and trailing slash;
- Amplitude knows only an internal `user_id` and an account group; a share of users is anonymous (`device_id` only) before login;
- some HubSpot contacts are merged duplicates (`property_hs_merged_object_ids`);
- a few true negatives: two different companies with similar names.

Write the ground truth (which rows are the same person/company) to a separate seed, `seeds/truth_identity.csv`. It is used only by tests, never by models.

## Steps

1. **Staging** (`stg_*`): one model per source table, rename, cast, normalise keys (lowercase email, strip `+alias`, extract email domain, normalise website to bare domain, strip legal suffixes). For Intercom history tables keep only `_fivetran_active = true` in a `*_current` model.
2. **Identity graph** (`int_identity_edges`): candidate matches as pairs `(key_a, key_b, rule)`, rules in order of confidence: exact normalised email → email domain = company website domain → normalised company name. Personal domains (gmail, wp, onet…) never match on domain.
3. **Clustering** (`int_person_map`, `int_account_map`): connected components over the edges, giving a surrogate `person_key` and `account_key`. Keep the rule that produced each link (auditability).
4. **Aggregate before joining**: `int_account_usage` (Amplitude, 30-day active users and events), `int_account_support` (Intercom, open/closed conversations, time to first assignment from history), `int_account_crm` (HubSpot lifecycle stage, deal amount, renewal date). Each at account grain.
5. **Marts**: `dim_account`, `dim_person`, `fct_product_events` (event grain with `account_key`), `mart_account_health` (one row per account, the question from Goal).
6. **Tests**: `unique` + `not_null` on keys of every mart; a singular test comparing `int_person_map` / `int_account_map` to `truth_identity` with reported precision and recall; a test that no personal email domain produced an account link.

## Done when

- `dbt build` passes on BigQuery (sandbox is enough).
- `mart_account_health` has exactly one row per true company, no fan-out.
- Matching precision and recall versus `truth_identity` are printed in this README, with the false matches explained.

## Extension — internal delivery data (Jira, GitHub)

Optional, after the main brief is done. Goal: link a shipped change to customer impact: issue → PR → commit sha → `app_version` on events → affected accounts.

- Seeds from [`fivetran/dbt_jira`](https://github.com/fivetran/dbt_jira) and [`fivetran/dbt_github`](https://github.com/fivetran/dbt_github) (`integration_tests/seeds/`), version pinned.
- Step 0: add synthetic PRs and commits where ~80% carry a Jira key in branch/title/message and 20% have none or a wrong key. Add `app_version` (= commit sha) to the Amplitude events.
- Staging: extract the key with regex `[A-Z][A-Z0-9]+-\d+`; verify the real PK columns in the seeds before modelling.
- `int_change_map`: sha → PR → issue key. `mart_change_impact`: per issue, accounts exposed after the first event with that sha and support conversations in the next 7 days (aggregate to account grain before joining).
- Tests: unique issue key, PR-to-key coverage reported in this README, no event with an unknown sha.

## Starting prompt for an agent

> Read `008-fivetran-identity-resolution-dbt/README.md` in the data-pipeline repo. Start with Step 0: copy the listed seed files from the pinned Fivetran package versions, then write the generator for drifted rows and `truth_identity.csv`. Stop after Step 0 and show me sample rows of each source for the same three companies before writing any dbt model.
