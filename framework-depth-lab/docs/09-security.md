# Security review

## 共通baseline

- 認証はOIDC/OAuth 2.0 Authorization Code + PKCE等の現行flowを使う。
- authorizationはrouteの有無ではなくresource/action policyで確認する。
- request size、header、timeout、rate、upload、JSON depthを制限する。
- error responseへstack trace、query、token、PIIを出さない。
- SSRF、open redirect、path traversal、mass assignmentを境界で防ぐ。
- dependencyとcontainer imageを継続更新し、SBOM/署名/secret scanを導入する。

## Spring Boot

Spring Securityのfilter chain、method security、OAuth2 resource server/clientを統合できます。defaultが強い一方、複数`SecurityFilterChain`のmatcher順、CSRF、CORS、actuator exposureを明示的にtestします。Boot 4.1のHTTP client address filteringはSSRF defense-in-depthですが、allow-listやURL ownershipの設計を不要にはしません。

auto-configurationは便利ですが「何が有効か」をcondition reportとActuatorで確認します。management endpointは別port/networkへ分離し、公開範囲を最小化します。

## FastAPI

OpenAPI security schemeとdependencyを組み合わせます。JWTのsignatureだけでなくissuer、audience、expiry、algorithmを検証します。Python objectやPydantic modelをauthorizationの代わりに信頼せず、resource ownerをDB/command境界で確認します。

interactive docsは開発に有用ですが、production公開の必要性を判断します。proxy headerを信頼する範囲、CORS origin、upload spooling、worker timeoutをASGI server/reverse proxyまで含めて設定します。

## Gin

Ginはpolicy engineや認証providerを内蔵しません。middlewareでtoken検証結果をtyped keyまたは明示contextへ格納し、handler/application serviceでpermissionを確認します。`SetTrustedProxies`を正しく設定しないとclient IPを偽装され得ます。

`gin.Default()`はlogger/recoveryを入れますがsecurity middlewareではありません。secure headers、CORS、body limit、rate limitは選択・設定します。productionではdebug modeを避けます。

## ケーススタディのmodernization

`modular-monolith-with-ddd`のPermission単位RBACとcontroller-level checkは良い出発点です。一方、sampleのIdentityServer4はarchivedで、Resource Owner Password Credentials grantは新規設計に採用しません。現在のIdP、Authorization Code + PKCE、service間client credentials、token exchange等へuse case別に置換します。module内でもcommand handlerでresource-level authorizationを再確認し、HTTP以外の呼び出し経路を保護します。
