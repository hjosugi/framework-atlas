# #22 P5 implement React and Vue deep profiles with routing/state/full-stack boundaries

- State: closed
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/22
- Updated: 2026-08-02T07:00:54Z

## Metadata
- State: complete
- Tracker role: bounded implementation
- Parent: [E3 #4](https://github.com/hjosugi/framework-atlas/issues/4)
- Blocked on: D1-D3

## Official inputs
react.dev、vuejs.org、Vue Router、React Router/TanStack Routerのofficial docs/repositories。

## Artifacts
`profiles/react.md`, `vue.md`, routing/state ecosystem relations。

## Implementation
ReactをUI library、Vueをprogressive frameworkとして正しく分類し、component/state/reactivity/rendering、router、SSR/full-stack meta-framework境界、build/runtimeを比較する。

## Acceptance
- [x] React/Vueをserver web frameworkと同じcohortにしない。
- [x] Vue 2 repoとVue 3 coreを区別。
- [x] virtual DOM/reactivity/design lineageはofficial/inferenceを区別。
- [x] router/state solutionを本体機能として誤記しない。
- [x] SPA/SSR/server-componentsの未解決境界を記録。
- [x] kofun-bootとはtyped client/app-shell接点だけをmapping。

## Non-goals
frontend総合ranking、CSS/component library catalog。
