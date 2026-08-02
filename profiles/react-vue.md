# React・Vue — component UIとframework境界

確認日: 2026-08-02

ReactとVueはいずれも状態からUIを宣言するcomponent modelを提供するが、更新追跡と公式ecosystemの境界が異なる。ReactはUI libraryとしてcomponent/functionとone-way data flowを核に周辺選択をecosystemへ委ねる。Vueはprogressive frameworkとしてreactivity system、template/SFC、公式Router/Piniaとの段階的採用を一つの導線にする。GitHub Topicsの `vuejs/vue` はVue 2のrelease lineであり、Vue 3の正準repository `vuejs/core` と別entityにしている。

| 軸 | React | Vue |
|---|---|---|
| update model | render時のstate snapshotと明示的state update | reactive dependency tracking |
| component form | JavaScript/JSX中心 | templateまたはrender function、SFC |
| routing/state | ecosystem/framework選択 | official router/state options |
| adoption | UI libraryとしてhostへ組込み可能 | progressive adoptionを明示 |

SPA、SSR、React Server Components、Vue server renderingはどこでstate/effectを所有するかが異なり、単一の「frontend性能」欄に潰せない未解決境界として扱う。`kofun-boot` に直接持ち込むのはVDOMの実装ではなく、typed client/app-shell接点で状態遷移をdataとして観測し、effect commandを分離し、同じmodelをTUI/Web/desktop adapterへ解釈できる構造である。Elm Architecture/Bubble Teaの`model -> update -> command`も合わせて検証する。UI libraryとserver Web frameworkを同じ比較軸で順位付けしない。

## Sources

- https://react.dev/learn
- https://vuejs.org/guide/introduction.html
- https://router.vuejs.org/
- https://github.com/charmbracelet/bubbletea
