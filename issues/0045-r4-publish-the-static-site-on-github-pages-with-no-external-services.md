# #45 R4 publish the static site on GitHub Pages with no external services

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/45
- Updated: 2026-08-02T07:01:36Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E6 #7](https://github.com/hjosugi/framework-atlas/issues/7)
- Blocked on: S1-S5, R3

## Artifacts
Pages configuration、`docs/.nojekyll`、published endpoint evidence。

## Implementation
main/docs または公式Pages workflowの一方を選び、source SHAと公開deploymentを結ぶ。外部backend/CDN/searchを使わない。

## Acceptance
- [x] index、JS、CSS、atlas-data JSONがHTTP 200。
- [x] deep URL/query/hash動作。
- [x] content-type/cache behaviorを確認。
- [x] source commit SHAをsiteに表示。
- [x] anonymous browser/curl read-back。
- [x] CI greenだけでなくlive endpointを検証。

## Non-goals
独自domain、Cloudflare/Vercel、analytics。
