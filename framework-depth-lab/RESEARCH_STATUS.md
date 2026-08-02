# Research Status

## Completed

- 2026-08-02時点のstable versionとruntime requirementを公式sourceで確認
- 3 frameworkのrelease tagを固定して主要内部codeを確認
- frameworkの抽象度、request lifecycle、DI、validation、data、concurrency、security、testing、operationsを横断比較
- official influenceとinferenceを分離したdirected graph dataを作成
- `modular-monolith-with-ddd` のREADME、主要ADR、outbox/module実装位置をGitHubで確認
- 同じOpenAPI contractを使う3つの最小実装を作成
- GitHub Pages用dependency-free siteを作成
- 追加調査をGitHub Issue用Markdownとして整理
- repository validator、manifest、ZIP整合性check

## Not executed

- Spring Boot exampleのMaven compile/test: Mavenが環境にない
- Gin exampleの`go test`: Go toolchainが環境にない
- 3 serverを同時起動したend-to-end contract test
- k6 load testとCPU/RSS計測
- GraalVM native image、JVM CDS/AOT、Python free-threaded build、Go PGOの比較
- browserによるPagesのvisual regression

## Interpretation rule

未実行項目は成功したとは扱いません。`issues/` に再現条件とacceptance criteriaを登録しています。
