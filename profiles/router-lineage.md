# Router — protocol、matching、state、orchestrationを分ける

確認日: 2026-08-02

GitHubの`router` topicはWeb request matcher、client navigation、network router OS、VPN、security toolを混在させる。そのためtopic一致を分類と同一視しない。

## 比較群

- server request matcher: httprouter、chi、gorilla/mux、Symfony Routing、path-to-regexp
- client state/navigation: Vue Router、TanStack Router、UI-Router、wouter
- application orchestration: single-spa
- framework-integrated routing: Gin、Hono、Elysia、axum、Rails、Django、Laravel
- quarantine: Lantern、RouterSploit、iStoreOS、ARouter

比較軸はmatching algorithmだけではない。route declarationの型、reverse generation、nested/layout state、middleware、data loading、SSR、search parameter、link semantics、conflict diagnosticsを分ける。path matcherという部品とapplication routerを同じ行で比較しない。

## kofun-bootへの抽出

routeはmethod/pathだけでなくinput/output/error/effect/operation IDを持つADTにする。static dispatchを既定にし、conflictと到達不能routeをbuild gateで拒否する。server、client、OpenAPI、typed clientは同じroute algebraの異なるinterpreterとする。

## Sources

- https://github.com/topics/router
- https://github.com/julienschmidt/httprouter
- https://router.vuejs.org/
- https://tanstack.com/router/latest
- https://symfony.com/doc/current/routing.html
