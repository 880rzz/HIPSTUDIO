# HIPStudio external release runbook

This runbook covers the remaining checks that cannot be proven by repository CI alone.

## Final architecture

- `hipstudio.hu` is published from `880rzz/HIPSTUDIO` through GitHub Pages.
- The repository is the single source of truth for the HIPStudio site.
- No HIPStudio Vercel project is part of the target architecture.
- `flugos.hu` will use a separate Vercel project at the final cutover as the specialist Flúgos entry-domain layer.
- DNS, redirects and indexing are activated only after their release gates are green.

## 1. GitHub Pages review publication

Use the manual workflow `Publish HIPStudio review to GitHub Pages` on `main` before connecting `hipstudio.hu`.

The review workflow is intentionally fail-safe:

- review build only;
- `noindex,nofollow`;
- quote submission disabled;
- temporary `/HIPSTUDIO/` project-path asset and navigation rewrite;
- root entry point included;
- refuses deployment when a custom GitHub Pages domain is already active;
- may enable GitHub Pages when the repository has not been configured yet.

Verify on the published review URL:

1. `/HIPSTUDIO/` opens successfully and enters the Hungarian site.
2. HU/EN/DE navigation works.
3. CSS, JS and local images return successfully under the project path.
4. Quote pages open but cannot submit in review mode.
5. Privacy pages render correctly in HU/EN/DE.
6. Robots/meta remain `noindex,nofollow`.
7. Canonical URLs still point to `https://www.hipstudio.hu/...` as the future production origin.
8. A non-existent path has acceptable GitHub Pages 404 behaviour and does not masquerade as a valid page.

Do not connect the custom domain from the review workflow itself.

## 2. Quote backend storage: exact source-backed behaviour

Source: `apps-script/HIPStudioQuoteRequest.gs`.

The Apps Script `setup()` function uses Script Properties key `SHEET_ID`.

- If `SHEET_ID` exists, it opens that spreadsheet by ID.
- If `SHEET_ID` does not exist, it creates a new Google Sheet file named **`HIPStudio - Ajánlatkérések`** and stores the resulting spreadsheet ID in Script Properties as `SHEET_ID`.
- Inside that spreadsheet, the operative tab is **`Ajánlatkérések`**.
- `appendRecord_()` reads `SHEET_ID`, opens the spreadsheet by ID, takes a ScriptLock and appends the normalized record to that tab.

Therefore a Drive search for a file named only `Ajánlatkérések` is not authoritative. The file title is `HIPStudio - Ajánlatkérések`; `Ajánlatkérések` is the tab name. If the connected Drive account still cannot see the file, the most likely operational explanation is that the Apps Script deployment/setup belongs to another Google account or Drive context. This must be verified in the account that owns the web-app deployment before live activation.

## 3. Quote E2E acceptance

The current web-app candidate endpoint is configured externally and must be tested from a real browser/network environment.

Before testing:

1. Open the Apps Script project that owns the deployed web app.
2. Run `setup()` once if necessary.
3. Confirm the returned `sheetUrl` opens the expected `HIPStudio - Ajánlatkérések` spreadsheet.
4. Confirm the `Ajánlatkérések` tab exists and its first row matches the current backend headers.
5. Confirm `info@hipstudio.hu` is available as a Gmail Send-As alias if production mail should use that From address. If the alias is unavailable, the code intentionally falls back to the executing account as From while keeping Reply-To as `info@hipstudio.hu`.

Run one clearly labelled internal E2E submission from the website review/controlled production candidate. Use non-customer test data and explicitly state that it is a test.

Verify all of the following from the same request ID:

- browser receives `{ok:true, requestId:...}`;
- one row is appended to `Ajánlatkérések`;
- `page_url`, normalized payload and routing fields are present as designed;
- internal notification reaches the configured internal recipients;
- customer confirmation reaches the test mailbox;
- Reply-To is `info@hipstudio.hu`;
- From is `info@hipstudio.hu` only when the verified alias is available;
- routing remains an operational suggestion with human review, not an automated acceptance/rejection or price decision;
- no duplicate row or duplicate mail set is generated from one submission.

Only after this succeeds may the `quote-e2e` release gate be changed from blocked to ready.

## 4. Flúgos URL inventory

Do not activate `flugos.hu` redirects or its separate Vercel project until the remaining legacy URL inventory is authoritative enough to classify every known path.

For each legacy URL choose exactly one behaviour:

- preserve as historical/archive content;
- permanent redirect to a genuinely equivalent HIPStudio destination;
- 410 only for content that is intentionally removed and has no useful replacement.

Do not blanket-redirect historical Flúgos material to a current sales page.

## 5. HIPStudio cutover

Only after GitHub Pages review verification, quote E2E and the relevant migration checks are green:

1. prepare the production build with release gates explicitly updated and documented;
2. connect `hipstudio.hu` to GitHub Pages;
3. verify HTTPS and canonical host;
4. verify HU/EN/DE production routes;
5. verify privacy and quote flow again on the custom domain;
6. only then remove review `noindex`, publish the production sitemap and allow indexing.

Merge is not deploy. Deploy is not DNS. DNS is not indexing.
