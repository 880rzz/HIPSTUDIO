# Production redirect infrastructure plan

Status: **inactive**. This plan does not alter DNS, Wix, GitHub Pages or the public site.

GitHub Pages cannot emit route-specific HTTP 301 or 410 responses. Its generated HTML aliases remain review fallbacks only. Production redirects therefore require an HTTP layer in front of the static origin, such as a reviewed Cloudflare Worker or equivalent edge proxy.

## Cutover sequence

1. Freeze and re-crawl the Wix URL inventory immediately before migration.
2. Reconcile every source path against `audit/url-mapping.json`; add explicit 410 entries only where no valid replacement exists.
3. Generate edge rules from the reviewed mapping. Each old URL must resolve directly to its final localized HTTPS URL with one hop, while preserving relevant query strings.
4. Test the rules on a non-production hostname for status code, `Location`, loops, chains, language destination and encoded paths.
5. Obtain legal, publication, hosting and DNS approval. Keep Wix available during the controlled cutover and rollback window.
6. Activate the edge layer only after the production build, canonical URLs and sitemap use the final origin.
7. Crawl both the old inventory and the new sitemap from the public internet. Record status, final URL and deployed commit SHA.
8. Monitor 404/410 and redirect traffic, then review rules instead of silently redirecting unknown paths to the home page.

## Rule contract

- Exact path matching is the default; normalise one trailing slash without creating a chain.
- 301 is reserved for a confirmed replacement. 410 is reserved for a confirmed permanent removal.
- No blanket redirect to the home page.
- No redirect may cross to an unverified brand or legal entity.
- The edge implementation must add reviewed security headers and must not inject analytics, cookies or external scripts.

The mapping is data, not deployment configuration. No active Worker, Pages redirect file, DNS record or GitHub workflow is included in this PR.
