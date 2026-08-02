# Frameworkを改善・新規設計するための原則

## 1. 責任範囲を先に固定する

HTTP toolkit、API framework、application platformのどれかを宣言します。Ginの小ささとSpring Bootの統合範囲を同時に約束すると、coreが不安定になります。core contract、official extension、community adapterを階層化します。

## 2. 宣言を一度にする

type/schema metadataをvalidation、serialization、documentation、client generationへ再利用します。FastAPIの強さはこの一貫性です。ただしdomain modelまでtransport metadataへ従属させず、境界でmapできるようにします。

## 3. defaultを説明可能にする

Spring Boot型auto-configurationは強力ですが、適用条件、除外理由、選ばれたproviderを診断出力できなければmagicになります。すべての自動判断に`why enabled / why not / how override`を持たせます。

## 4. hot pathを小さくする

route matching、context生成、serializationへ不要なreflection/allocationを入れません。Ginのように頻出objectをpoolする場合は、lifetime misuseをAPI/documentation/testで防ぎます。optional featureはpay-for-playにします。

## 5. structured lifetimeを第一級にする

request scope、cancellation、deadline、resource cleanup、background task ownershipをcore abstractionに含めます。FastAPIの`yield` dependency、Go `context.Context`、Spring scope/transactionから長短を学べます。cleanup failureの観測方法も定義します。

## 6. sync/asyncを色分けする

async keywordだけでなく、blocking boundary、thread pool、event loop、backpressure、CPU workの扱いを明示します。混在時のsafe defaultとdiagnosticsを提供します。

## 7. standardへ戻れるようにする

Servlet/HTTP、ASGI、`net/http`など下位標準を完全に隠しません。framework固有APIが足りないときのescape hatchが、長期採用の保険になります。

## 8. extension pointを狭く安定させる

middleware、dependency provider、message converter、repository portのように責任別のextension pointを設けます。巨大plugin interface、global registry、order不明のhookを避けます。

## 9. security/observabilityを後付けにしない

request ID、trace propagation、safe error、input limit、proxy trust、secret redactionをdefault pathへ含めます。auth providerは差し替え可能にし、authorization decision pointをapplication boundaryに残します。

## 10. benchmark contractを公開する

fixture、version、hardware、command、raw resultを残し、micro/end-to-end、warm/coldを分けます。勝者の数字ではなく再現手順を製品にします。

## 11. migrationをfeatureとして設計する

deprecation warning、codemod、compatibility window、release cadence、LTS policyを用意します。ecosystem adapterの互換matrixも公開します。

## 12. frameworkがdomain architectureを装わない

module annotationやfolder generatorはbounded contextを保証しません。dependency direction、data ownership、transaction boundaryをarchitecture testで検証できる補助を提供し、business rule自体は利用者へ委ねます。

## 採用前のframework作者向け質問

1. 最小request pathに何個の抽象化があるか。
2. configurationの最終値と由来を機械的に説明できるか。
3. cancellationとcleanupはどこまで伝播するか。
4. coreなしでadapterを更新できるか。
5. invalid input、partial failure、duplicate deliveryのdefaultは何か。
6. standard libraryとの相互運用はlosslessか。
7. observabilityを切ったbenchmarkだけを宣伝していないか。
