# #22 P5 implement React and Vue deep profiles with routing/state/full-stack boundaries

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/22
- Updated: 2026-08-02T05:40:28Z

## Metadata
- State: ready
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
- [ ] React/Vueをserver web frameworkと同じcohortにしない。
- [ ] Vue 2 repoとVue 3 coreを区別。
- [ ] virtual DOM/reactivity/design lineageはofficial/inferenceを区別。
- [ ] router/state solutionを本体機能として誤記しない。
- [ ] SPA/SSR/server-componentsの未解決境界を記録。
- [ ] kofun-bootとはtyped client/app-shell接点だけをmapping。

## Non-goals
frontend総合ranking、CSS/component library catalog。
