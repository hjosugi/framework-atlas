#!/usr/bin/env python3
"""Create the initial curated catalog.

This script is intentionally deterministic and dependency-free. Run it only when
bootstrapping a new copy; normal contributions should edit the JSON data files.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-08-02"
FRAMEWORKS: list[dict[str, Any]] = []
RELATIONSHIPS: list[dict[str, Any]] = []


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def src(url: str, title: str, source_type: str = "official") -> dict[str, str]:
    return {"url": url, "title": title, "type": source_type, "accessed": TODAY}


def relation(
    source: str,
    target: str,
    relation_type: str,
    explanation_ja: str,
    *,
    grade: str = "B",
    state: str = "supported",
    source_url: str = "",
    target_kind: str = "framework",
) -> None:
    item = {
        "id": f"{source}--{relation_type}--{target}",
        "source": source,
        "target": target,
        "target_kind": target_kind,
        "relation": relation_type,
        "explanation_ja": explanation_ja,
        "evidence_grade": grade,
        "evidence_state": state,
        "confidence": {"A": 0.95, "B": 0.82, "C": 0.65, "D": 0.35, "U": 0.1}[grade],
        "sources": [src(source_url, "Relationship evidence")] if source_url else [],
        "last_verified": TODAY,
    }
    RELATIONSHIPS.append(item)


def add(
    id: str,
    name: str,
    language: str,
    kind: str,
    domains: list[str],
    repository: str,
    homepage: str,
    summary_ja: str,
    problem_ja: list[str],
    origin_ja: str,
    design_ideas: list[str],
    features: list[str],
    advantages: list[str],
    disadvantages: list[str],
    use_when: list[str],
    avoid_when: list[str],
    alternatives: list[str],
    *,
    aliases: list[str] | None = None,
    languages: list[str] | None = None,
    status: str = "active",
    depth: str = "deep",
    governance: str = "unknown",
    license_name: str = "unknown",
    source_urls: list[tuple[str, str]] | None = None,
    origin_evidence: str = "partial",
    lineage_evidence: str = "partial",
    open_questions: list[str] | None = None,
) -> None:
    urls = source_urls or []
    if repository and not any("github.com" in u for u, _ in urls):
        urls.append((f"https://github.com/{repository}", "Official repository"))
    if homepage and not any(u == homepage for u, _ in urls):
        urls.append((homepage, "Official website"))
    FRAMEWORKS.append(
        {
            "id": id,
            "name": name,
            "aliases": aliases or [],
            "kind": kind,
            "primary_language": language,
            "languages": languages or [language],
            "domains": domains,
            "status": status,
            "research_depth": depth,
            "repository": repository,
            "homepage": homepage,
            "governance": governance,
            "license": license_name,
            "summary_ja": summary_ja,
            "problem_ja": problem_ja,
            "origin_ja": origin_ja,
            "design_ideas": design_ideas,
            "features": features,
            "advantages": advantages,
            "disadvantages": disadvantages,
            "use_when": use_when,
            "avoid_when": avoid_when,
            "alternatives": alternatives,
            "sources": [src(u, t) for u, t in urls],
            "evidence": {
                "identity": "verified" if urls else "unverified",
                "origin": origin_evidence,
                "features": "supported" if urls else "unverified",
                "tradeoffs": "editorial-analysis",
                "lineage": lineage_evidence,
            },
            "open_questions": open_questions or [],
            "last_verified": TODAY,
        }
    )


def standard(
    id: str,
    name: str,
    language: str,
    kind: str,
    domains: list[str],
    repository: str,
    homepage: str,
    summary_ja: str,
    problem: str,
    traits: list[str],
    strengths: list[str],
    weaknesses: list[str],
    alternatives: list[str],
    *,
    status: str = "active",
    aliases: list[str] | None = None,
    origin: str = "起源、初期の設計判断、直接的な影響関係は追加の一次資料調査が必要。",
    source_urls: list[tuple[str, str]] | None = None,
) -> None:
    domain = domains[0] if domains else "application"
    add(
        id,
        name,
        language,
        kind,
        domains,
        repository,
        homepage,
        summary_ja,
        [problem],
        origin,
        traits,
        traits,
        strengths,
        weaknesses,
        [f"{domain}領域で、{traits[0] if traits else '一貫した構造'}を重視するとき"],
        [f"フレームワーク固有の抽象化を避けたいとき", "保守体制や互換性を確認できないとき"],
        alternatives,
        aliases=aliases,
        status=status,
        depth="standard",
        source_urls=source_urls,
        origin_evidence="unverified" if origin.startswith("起源、") else "partial",
        lineage_evidence="unverified",
        open_questions=[
            "最初期の設計文書または発表を確認する",
            "明示された影響元と後続への影響を一次資料で確認する",
            "現在の保守体制、互換性方針、長期サポートを確認する",
        ],
    )


# ---------------------------------------------------------------------------
# Deep profiles: backend and full-stack web frameworks
# ---------------------------------------------------------------------------
add(
    "spring-framework", "Spring Framework", "Java", "application-framework",
    ["web-backend", "enterprise", "reactive"], "spring-projects/spring-framework",
    "https://spring.io/projects/spring-framework",
    "Javaアプリケーションの構成、依存関係、Web、データアクセス、トランザクションを一貫したプログラミングモデルで扱う基盤。",
    ["重量級コンテナや侵入的APIに依存せず企業アプリを組み立てる", "横断的関心事とオブジェクト生成を業務コードから分離する"],
    "Rod Johnsonの著作と2000年代初頭のJ2EE開発への問題意識から始まり、軽量なIoCコンテナとPOJO中心設計を核に成長した。",
    ["IoC/Dependency Injection", "AOP", "POJO中心", "テンプレートと一貫した例外変換", "宣言的トランザクション"],
    ["DIコンテナ", "Spring MVC", "WebFlux", "データアクセス抽象化", "イベントとリソース管理"],
    ["巨大なエコシステムと統合選択肢", "テスト可能な依存関係分離", "企業システム向けの成熟した運用知識"],
    ["抽象化と設定の層が多く学習範囲が広い", "自動構成とプロキシの挙動を理解しないと障害解析が難しい", "小規模用途では過剰になり得る"],
    ["長期保守するJava/Kotlinサービス", "トランザクションやセキュリティを統合したい", "複数インフラを交換可能にしたい"],
    ["極小バイナリと起動時間を最優先する", "フレームワークのライフサイクルを避けたい"],
    ["jakarta-ee", "quarkus", "micronaut", "ktor"],
    governance="Broadcom-backed community", license_name="Apache-2.0",
    source_urls=[
        ("https://docs.spring.io/spring-framework/reference/overview.html", "Spring Framework Overview"),
        ("https://spring.io/blog/2006/11/09/spring-framework-the-origins-of-a-project-and-a-name", "Spring project origins"),
    ], origin_evidence="verified", lineage_evidence="supported",
)
relation("spring-framework", "jakarta-ee", "reaction-against", "初期Springは当時の重量級J2EE/EJB開発への軽量な代替として設計された。", grade="A", state="verified", source_url="https://spring.io/blog/2006/11/09/spring-framework-the-origins-of-a-project-and-a-name")
relation("spring-framework", "dependency-injection", "implements", "IoCコンテナで依存関係の生成と結合を外部化する。", grade="A", state="verified", source_url="https://docs.spring.io/spring-framework/reference/core/beans/introduction.html", target_kind="idea")

add(
    "spring-boot", "Spring Boot", "Java", "meta-framework",
    ["web-backend", "enterprise", "cloud-native"], "spring-projects/spring-boot",
    "https://spring.io/projects/spring-boot",
    "Springアプリケーションの初期設定、依存関係選択、組み込みサーバー、運用機能を統合し、実行可能なサービスを素早く作るための基盤。",
    ["Springの柔軟性を保ちながら定型設定を削減する", "本番運用に必要な監視・設定・パッケージングを標準化する"],
    "Springエコシステムの構成選択が増えた結果生じたセットアップ負担を、規約と条件付き自動構成で軽減する目的で作られた。",
    ["Convention over configuration", "条件付き自動構成", "starter依存関係", "組み込みサーバー", "外部化設定"],
    ["Auto-configuration", "Actuator", "Starter POMs", "Executable JAR/WAR", "設定プロファイル"],
    ["初期構築が速い", "運用機能が標準化される", "Springエコシステムを段階的に利用できる"],
    ["自動構成の条件を知らないと挙動が見えにくい", "依存関係が大きくなりやすい", "起動時間とメモリが厳しい用途では調整が必要"],
    ["Java/KotlinのAPIや業務サービス", "Spring標準に沿ったチーム開発", "監視と設定を早期に整備したい"],
    ["単一関数程度の極小処理", "Spring互換性が不要な低レイヤ用途"],
    ["quarkus", "micronaut", "dropwizard"],
    governance="Broadcom-backed community", license_name="Apache-2.0",
    source_urls=[("https://docs.spring.io/spring-boot/reference/using/auto-configuration.html", "Spring Boot auto-configuration")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("spring-boot", "spring-framework", "built-on", "Spring Frameworkを規約、自動構成、運用機能で包む。", grade="A", state="verified", source_url="https://spring.io/projects/spring-boot")
relation("spring-boot", "convention-over-configuration", "implements", "標準的な選択を自動構成し、明示設定で上書きできる。", grade="A", state="verified", source_url="https://docs.spring.io/spring-boot/reference/using/auto-configuration.html", target_kind="idea")

add(
    "jakarta-ee", "Jakarta EE", "Java", "platform",
    ["web-backend", "enterprise"], "jakartaee/platform", "https://jakarta.ee/",
    "企業Java向けの標準API群と互換実装のエコシステム。Web、永続化、メッセージング、トランザクション、DIなどの移植可能な契約を定義する。",
    ["ベンダーを越えて企業アプリのAPI契約を統一する", "長期互換性と認証済み実装を提供する"],
    "Java EEがEclipse Foundationへ移管され、名称とパッケージ空間を移行して継続した標準プラットフォーム。",
    ["標準仕様", "互換性テスト", "コンテナ管理", "宣言的サービス", "複数ベンダー実装"],
    ["Servlet", "CDI", "Persistence", "REST", "Messaging", "Transactions"],
    ["標準化と移植性", "長期運用の実績", "複数実装から選べる"],
    ["仕様と実装の理解が分かれる", "プラットフォーム全体は大きい", "新機能導入は単一プロジェクトより調整に時間がかかる"],
    ["ベンダー中立な企業Java", "標準準拠が調達や保守条件になる", "既存Java EE資産を継続する"],
    ["極小サービスで必要APIが限定される", "単一ベンダー機能を積極利用する"],
    ["spring-framework", "quarkus", "micronaut"],
    aliases=["Java EE", "J2EE"], governance="Eclipse Foundation / specification committees",
    source_urls=[("https://jakarta.ee/about/", "About Jakarta EE"), ("https://jakarta.ee/specifications/", "Jakarta EE specifications")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("jakarta-ee", "java-ee", "successor-of", "Java EEがEclipse Foundationへ移管されJakarta EEとして継続した。", grade="A", state="verified", source_url="https://jakarta.ee/about/", target_kind="idea")

add(
    "quarkus", "Quarkus", "Java", "application-framework",
    ["web-backend", "cloud-native", "serverless"], "quarkusio/quarkus", "https://quarkus.io/",
    "コンテナ、Kubernetes、ネイティブ実行を意識し、Javaの起動時間とメモリ効率を改善するためにビルド時処理を重視したフレームワーク。",
    ["Javaサービスを短時間起動・低メモリで動かす", "既存標準やライブラリをクラウドネイティブ実行へ適応する"],
    "Red HatがGraalVM Native ImageとKubernetes時代のJava利用を強く意識して開発し、従来実行時に行う解析をビルド時へ移した。",
    ["Build-time augmentation", "Container-first", "Native Image", "Developer mode", "Reactive and imperative unification"],
    ["高速dev mode", "拡張機構", "Kubernetes統合", "REST/DI/persistence", "native executable"],
    ["起動時間とメモリを抑えやすい", "Java標準・既存ライブラリとの接続が豊富", "開発時フィードバックが速い"],
    ["ネイティブ化でreflectionや動的機能に制約が出る", "ビルド時処理の理解が必要", "拡張対応外ライブラリは追加作業が必要"],
    ["Kubernetes上のJavaマイクロサービス", "スケールゼロや短命プロセス", "Java資産を維持しつつ効率化する"],
    ["高度に動的なクラスロードが必須", "ネイティブ化のビルド時間を許容できない"],
    ["spring-boot", "micronaut", "helidon"],
    governance="Red Hat / community", license_name="Apache-2.0",
    source_urls=[("https://quarkus.io/vision/", "Quarkus vision"), ("https://quarkus.io/guides/building-native-image", "Native image guide")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("quarkus", "graalvm-native-image", "built-on", "ネイティブ実行ではGraalVM Native Imageの事前コンパイルを利用する。", grade="A", state="verified", source_url="https://quarkus.io/guides/building-native-image", target_kind="idea")
relation("quarkus", "build-time-augmentation", "implements", "実行時処理をビルド時へ移し、起動とメモリを最適化する。", grade="A", state="verified", source_url="https://quarkus.io/vision/", target_kind="idea")

add(
    "micronaut", "Micronaut", "Java", "application-framework",
    ["web-backend", "cloud-native", "serverless"], "micronaut-projects/micronaut-core", "https://micronaut.io/",
    "コンパイル時DIとAOPを使い、reflectionや実行時スキャンを減らしたJVM向けクラウド・マイクロサービスフレームワーク。",
    ["JVMフレームワークの起動時間・メモリ・reflection依存を減らす", "サーバーレスとマイクロサービス向け統合を標準化する"],
    "Grails開発者を含むチームが、従来の実行時メタプログラミングのコストをコンパイル時処理へ移す方向で設計した。",
    ["Compile-time DI", "Compile-time AOP", "No runtime classpath scanning", "Non-blocking HTTP", "Ahead-of-time optimization"],
    ["HTTP server/client", "DI/AOP", "configuration", "data access", "service discovery"],
    ["起動とメモリを予測しやすい", "サーバーレスに適する", "Java/Kotlin/Groovyを支援"],
    ["コンパイル時生成のデバッグ知識が必要", "Springほど巨大な統合資産はない", "annotation processor設定に依存する"],
    ["低フットプリントJVMサービス", "サーバーレス", "コンパイル時安全性を重視する"],
    ["動的プロキシや実行時拡張を多用する", "Spring固有ライブラリ互換を最優先する"],
    ["quarkus", "spring-boot", "helidon"],
    governance="Object Computing / community", license_name="Apache-2.0",
    source_urls=[("https://docs.micronaut.io/latest/guide/#introduction", "Micronaut introduction")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("micronaut", "compile-time-di", "implements", "DIメタデータをコンパイル時に生成し実行時スキャンを避ける。", grade="A", state="verified", source_url="https://docs.micronaut.io/latest/guide/#introduction", target_kind="idea")

add(
    "aspnet-core", "ASP.NET Core", "C#", "web-framework",
    ["web-backend", "web-fullstack", "cloud-native"], "dotnet/aspnetcore", "https://dotnet.microsoft.com/apps/aspnet",
    "クロスプラットフォーム.NET上でWeb API、MVC、Razor、リアルタイム通信、サーバーUIを構築する統合Webフレームワーク。",
    ["Windows依存を減らした高性能な.NET Web基盤を提供する", "Webの複数プログラミングモデルを一つのホストとDIで統合する"],
    "従来のASP.NETを再設計し、オープンソース、モジュール化、クロスプラットフォーム、統一された.NETランタイムを前提に発展した。",
    ["Middleware pipeline", "Built-in DI", "Unified hosting", "Async I/O", "Multiple UI/API models"],
    ["Minimal APIs", "MVC", "Razor Pages", "Blazor", "SignalR", "gRPC integration"],
    ["高い実行性能と強い型", "Microsoftの長期サポート", "Web APIからサーバーUIまで統合"],
    ["選択肢が多く学習範囲が広い", ".NETのリリース方針に追随が必要", "抽象化を重ねると処理経路が見えにくい"],
    ["C#/.NETを標準とするサービス", "APIとリアルタイム機能を統合する", "企業向け長期保守"],
    ["最小ランタイムや別言語エコシステムが必須", "単純な静的サイトのみ"],
    ["spring-boot", "django", "nestjs"],
    aliases=["ASP.NET 5"], governance="Microsoft / .NET Foundation", license_name="MIT",
    source_urls=[("https://learn.microsoft.com/aspnet/core/introduction-to-aspnet-core", "Introduction to ASP.NET Core")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("aspnet-core", "aspnet", "successor-of", "従来ASP.NETをクロスプラットフォーム・モジュール型に再設計した系譜。", grade="A", state="verified", source_url="https://learn.microsoft.com/aspnet/core/introduction-to-aspnet-core", target_kind="idea")
relation("aspnet-core", "middleware-pipeline", "implements", "要求処理を順序付きmiddlewareとして合成する。", grade="A", state="verified", source_url="https://learn.microsoft.com/aspnet/core/fundamentals/middleware/", target_kind="idea")

add(
    "django", "Django", "Python", "web-framework",
    ["web-fullstack", "web-backend", "cms"], "django/django", "https://www.djangoproject.com/",
    "管理画面、ORM、テンプレート、フォーム、認証、セキュリティを統合したPythonのbatteries-included Webフレームワーク。",
    ["締切の厳しいコンテンツサイトを少人数で安全に構築する", "Web開発の反復的なCRUD・管理・認証を標準化する"],
    "米国の新聞社でニュースサイトを迅速に構築するための内部ツールとして生まれ、再利用可能なWebフレームワークとして公開された。",
    ["MTV architecture", "Batteries included", "Explicit apps", "Secure defaults", "Reusable components"],
    ["ORM", "Admin", "URL routing", "Templates", "Forms", "Authentication", "Migrations"],
    ["業務CRUDの開発が速い", "セキュリティ機能と文書が成熟", "一体化された標準によりチーム判断を減らす"],
    ["非同期中心や極小APIには構造が重い場合がある", "ORMとActive Record風APIに設計が寄りやすい", "標準外アーキテクチャでは摩擦が生じる"],
    ["管理画面を持つ業務システム", "コンテンツ中心サイト", "Pythonで長期保守するモノリス"],
    ["極小・単機能HTTPサービス", "高頻度リアルタイム処理が中心", "ORMを完全に避ける"],
    ["rails", "laravel", "fastapi", "flask"],
    governance="Django Software Foundation", license_name="BSD-3-Clause",
    source_urls=[("https://www.djangoproject.com/start/overview/", "Django overview"), ("https://www.djangoproject.com/foundation/", "Django Software Foundation")],
    origin_evidence="verified", lineage_evidence="partial",
)
relation("django", "batteries-included", "implements", "管理・ORM・フォーム・認証などを標準に含める。", grade="A", state="verified", source_url="https://www.djangoproject.com/start/overview/", target_kind="idea")

add(
    "flask", "Flask", "Python", "web-framework",
    ["web-backend", "microframework"], "pallets/flask", "https://flask.palletsprojects.com/",
    "WerkzeugとJinjaを核に、ルーティングと要求処理の小さな中心だけを提供するPythonマイクロフレームワーク。",
    ["アプリ構造と周辺部品の選択を開発者に委ねる", "小さく理解可能なWeb基盤を提供する"],
    "Armin RonacherがApril Foolsの着想を実用プロジェクトへ発展させ、Pocoo/Palletsの既存ライブラリを薄く統合した。",
    ["Microframework", "WSGI", "Explicit extension model", "Application/request contexts", "Minimal core"],
    ["Routing", "Request/response", "Templates", "CLI", "Extension ecosystem"],
    ["小さく始めやすい", "構成の自由度が高い", "WSGIとPython Webの仕組みを学びやすい"],
    ["大規模化すると独自規約が必要", "拡張の品質と互換性がばらつく", "非同期中心にはASGI系が自然"],
    ["小中規模API", "独自アーキテクチャを組みたい", "学習・プロトタイプ"],
    ["管理画面やORMまで統一したい", "ASGIネイティブを最優先する"],
    ["fastapi", "django", "pyramid"],
    governance="Pallets", license_name="BSD-3-Clause",
    source_urls=[("https://flask.palletsprojects.com/en/stable/design/", "Flask design decisions"), ("https://flask.palletsprojects.com/en/stable/foreword/", "Flask foreword")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("flask", "werkzeug", "built-on", "WSGI要求・応答、ルーティング等をWerkzeugに依存する。", grade="A", state="verified", source_url="https://flask.palletsprojects.com/en/stable/design/", target_kind="idea")
relation("flask", "jinja", "built-on", "テンプレート機能にJinjaを利用する。", grade="A", state="verified", source_url="https://flask.palletsprojects.com/en/stable/design/", target_kind="idea")

add(
    "fastapi", "FastAPI", "Python", "web-framework",
    ["web-backend", "api", "async"], "fastapi/fastapi", "https://fastapi.tiangolo.com/",
    "Python型ヒントから検証、依存関係、OpenAPI、対話的API文書を統合するASGI APIフレームワーク。",
    ["APIスキーマ・検証・文書の重複を減らす", "Pythonの型情報を実行時Web境界で再利用する", "async I/Oを自然に扱う"],
    "既存Pythonフレームワークの使いやすさと、OpenAPI・型安全な検証を組み合わせる目的で作られ、StarletteとPydanticを基盤にした。",
    ["Type-driven API", "ASGI", "Dependency injection", "OpenAPI-first output", "Sync/async interoperability"],
    ["Validation", "Serialization", "OpenAPI/JSON Schema", "Dependency system", "WebSockets", "background tasks"],
    ["API契約とコードのずれを減らす", "文書生成が標準", "高い開発速度とasync対応"],
    ["型・検証モデルと永続化モデルの境界設計が必要", "依存関係注入を過度に使うと追跡しにくい", "CPU負荷処理は別途分離が必要"],
    ["JSON API", "型付きPythonサービス", "OpenAPIを配布する", "async I/Oが多い"],
    ["サーバー描画中心の統合CMS", "型ヒントを使えない古いコードベース"],
    ["django", "flask", "litestar", "falcon"],
    governance="FastAPI project / community", license_name="MIT",
    source_urls=[("https://fastapi.tiangolo.com/alternatives/", "FastAPI alternatives, inspiration and comparisons"), ("https://fastapi.tiangolo.com/features/", "FastAPI features")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("fastapi", "starlette", "built-on", "ASGI Web機能はStarletteを基盤とする。", grade="A", state="verified", source_url="https://fastapi.tiangolo.com/alternatives/")
relation("fastapi", "pydantic", "built-on", "データ検証とスキーマ生成はPydanticを基盤とする。", grade="A", state="verified", source_url="https://fastapi.tiangolo.com/alternatives/")
relation("fastapi", "flask", "inspired-by", "簡潔なパス操作APIなど、公式文書がFlaskを着想元の一つとして説明する。", grade="A", state="verified", source_url="https://fastapi.tiangolo.com/alternatives/")

add(
    "rails", "Ruby on Rails", "Ruby", "web-framework",
    ["web-fullstack", "web-backend"], "rails/rails", "https://rubyonrails.org/",
    "Convention over ConfigurationとDRYを中心に、データベース中心のWebアプリを一貫した構造で高速に作るフルスタックフレームワーク。",
    ["Web開発で繰り返される設定と接着コードを減らす", "一人または小チームが製品全体を扱える生産性を実現する"],
    "Basecampの開発から抽出され、Rubyのメタプログラミングと強い規約を使って当時のJava系企業Web開発とは異なる生産性を示した。",
    ["Convention over Configuration", "DRY", "Active Record", "MVC", "Integrated full stack"],
    ["Active Record", "Action Pack", "Hotwire integration", "Jobs", "Mail", "Migrations", "Generators"],
    ["標準経路での開発速度が高い", "モノリスで製品全体を統合しやすい", "歴史の長いエコシステム"],
    ["規約から外れる設計では摩擦が大きい", "Active Recordに業務ロジックが集中しやすい", "大規模運用では性能と境界の継続的管理が必要"],
    ["SaaSや業務Webを少人数で構築", "CRUD中心で市場投入を優先", "HTML-firstの統合アプリ"],
    ["極端な低レイテンシや小メモリ", "多数サービスを初期から分割する必要がある"],
    ["django", "laravel", "phoenix", "hanami"],
    governance="Rails Foundation / core team", license_name="MIT",
    source_urls=[("https://rubyonrails.org/doctrine", "Rails Doctrine"), ("https://rubyonrails.org/2005/12/13/rails-1-0-party-like-its-one-oh-oh", "Rails 1.0 announcement")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("rails", "mvc", "implements", "モデル、ビュー、コントローラを統合し、Webアプリの標準構造にした。", grade="A", state="verified", source_url="https://guides.rubyonrails.org/getting_started.html", target_kind="idea")
relation("rails", "convention-over-configuration", "implements", "名前と配置の規約によって設定量を削減する。", grade="A", state="verified", source_url="https://rubyonrails.org/doctrine", target_kind="idea")

add(
    "laravel", "Laravel", "PHP", "web-framework",
    ["web-fullstack", "web-backend"], "laravel/framework", "https://laravel.com/",
    "ExpressiveなAPIと統合ツール群で、PHPのWebアプリ、API、ジョブ、イベント、認証、永続化を一貫して構築するフルスタックフレームワーク。",
    ["PHP開発の定型処理を読みやすいAPIで統合する", "初期開発からキュー・通知・認証・運用へ滑らかに拡張する"],
    "Taylor Otwellが当時のPHPフレームワークで不足していた認証などを補い、RailsやSymfony系のアイデアをPHPらしい開発体験へまとめた。",
    ["Expressive API", "Service container", "Facade", "Convention", "Integrated developer experience"],
    ["Eloquent ORM", "Blade", "Queues", "Events", "Authentication", "Artisan", "Testing helpers"],
    ["学習資源とパッケージが豊富", "一般的なWeb機能が統合される", "標準経路の生産性が高い"],
    ["Facadeや暗黙解決を多用すると依存関係が見えにくい", "Eloquent中心設計が複雑なドメインに合わない場合がある", "高負荷ではPHP実行モデルと状態管理を考慮する"],
    ["PHPでSaaS・業務Web・API", "統合された開発体験を重視", "短期間で機能を揃える"],
    ["最小部品だけを組みたい", "強いドメイン境界と永続化独立性が最優先"],
    ["symfony", "rails", "django", "yii"],
    governance="Laravel Holdings / community", license_name="MIT",
    source_urls=[("https://laravel.com/docs", "Laravel documentation"), ("https://github.com/laravel/framework", "Laravel Framework repository")],
    origin_evidence="supported", lineage_evidence="partial",
    open_questions=["Taylor Otwellの初期発表から、影響元を明示した一次資料を追加する"],
)
relation("laravel", "symfony", "built-on", "HTTP、Consoleなど複数のSymfony Componentsを利用する。", grade="A", state="verified", source_url="https://github.com/laravel/framework")
relation("laravel", "rails", "inspired-by", "規約、Active Record風ORM、開発体験にRails系譜の影響が見られるが、明示一次資料を追加確認する。", grade="C", state="hypothesis", target_kind="framework")

add(
    "symfony", "Symfony", "PHP", "application-framework",
    ["web-backend", "web-fullstack", "components"], "symfony/symfony", "https://symfony.com/",
    "再利用可能なPHP Componentsとフルスタックフレームワークを提供し、明示的な依存関係と長期保守を重視する基盤。",
    ["PHPアプリの共通部品を標準化する", "小さなcomponent利用から大規模フルスタックへ同じ設計資産で拡張する"],
    "SensioLabsで企業PHP開発の再利用性と保守性を高める目的で始まり、独立componentが多数のPHPプロジェクトの基盤となった。",
    ["Reusable components", "Dependency injection", "Explicit configuration", "Bundles", "Long-term support"],
    ["HTTP Foundation", "Routing", "Console", "DI", "Messenger", "Security", "Serializer"],
    ["部品単位でも利用できる", "企業向けの互換性とLTS", "依存関係が比較的明示的"],
    ["機能範囲が広く学習量が多い", "設定とコンテナ生成が複雑になり得る", "標準構成でも小規模用途には重い"],
    ["長期保守のPHPシステム", "再利用componentが必要", "明示的アーキテクチャを好む"],
    ["極小APIで数個の関数だけ必要", "Laravel流の統合規約を優先する"],
    ["laravel", "yii", "nette", "slim"],
    governance="Symfony SAS / community", license_name="MIT",
    source_urls=[("https://symfony.com/what-is-symfony", "What is Symfony"), ("https://symfony.com/doc/current/components/index.html", "Symfony Components")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("symfony", "reusable-components", "implements", "フルスタック以外からも使える独立component群を中心にする。", grade="A", state="verified", source_url="https://symfony.com/doc/current/components/index.html", target_kind="idea")

add(
    "express", "Express", "JavaScript", "web-framework",
    ["web-backend", "microframework"], "expressjs/express", "https://expressjs.com/",
    "Node.jsのHTTP機能にルーティングとmiddlewareを加え、WebアプリとAPIを最小限の規約で構築するフレームワーク。",
    ["Node.js HTTPの低レベル処理を簡潔にする", "小さなmiddlewareを組み合わせて要求処理を構成する"],
    "Connectのmiddlewareモデルを取り込み、Node.js初期のWeb開発で事実上の標準的な薄い層として普及した。",
    ["Middleware pipeline", "Minimal core", "Unopinionated composition", "Node HTTP compatibility"],
    ["Routing", "Middleware", "Request/response helpers", "Template integration"],
    ["単純で豊富な知識資産", "middlewareエコシステムが大きい", "既存Nodeライブラリと接続しやすい"],
    ["大規模構造を自動では与えない", "middleware品質とセキュリティを個別評価する必要", "asyncエラー処理や型安全は追加設計が必要"],
    ["小中規模Node API", "独自構成を選びたい", "既存middleware資産を使う"],
    ["強い型付き契約と統一アーキテクチャが必要", "極限性能やWeb標準API互換を最優先"],
    ["fastify", "koa", "nestjs", "hono"],
    governance="OpenJS Foundation", license_name="MIT",
    source_urls=[("https://expressjs.com/en/starter/faq.html", "Express FAQ"), ("https://github.com/expressjs/express", "Express repository")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("express", "connect", "built-on", "初期ExpressはConnectのmiddlewareモデルと実装を基盤に発展した。", grade="B", state="supported", target_kind="idea")
relation("express", "middleware-pipeline", "implements", "要求処理を順序付きmiddlewareとして合成する。", grade="A", state="verified", source_url="https://expressjs.com/en/guide/using-middleware.html", target_kind="idea")

add(
    "nestjs", "NestJS", "TypeScript", "application-framework",
    ["web-backend", "enterprise", "microservices"], "nestjs/nest", "https://nestjs.com/",
    "TypeScriptのdecorator、module、DIを使い、Node.jsサーバーを明確なアーキテクチャで構築するフレームワーク。",
    ["Express/Fastify上の大規模Nodeアプリに統一構造を与える", "HTTP、GraphQL、WebSocket、microservicesを同じDIモデルで扱う"],
    "Angularの構造化された開発体験をサーバー側TypeScriptへ持ち込み、Nodeバックエンドの保守性を高める目的で設計された。",
    ["Angular-like modules", "Dependency injection", "Decorators and metadata", "Platform adapters", "Layered architecture"],
    ["Controllers/providers/modules", "Express/Fastify adapters", "Pipes/guards/interceptors", "GraphQL", "Microservices"],
    ["大規模チームで構造を共有しやすい", "TypeScriptとDIを一貫利用", "複数トランスポートを統合"],
    ["decoratorとreflectionに依存", "小規模APIには定型コードが多い", "抽象化層が実基盤の挙動を隠す場合がある"],
    ["中大規模TypeScriptバックエンド", "Angular経験を共有する組織", "複数通信方式を統一する"],
    ["数個のendpointだけ", "decoratorやDIコンテナを避けたい"],
    ["fastify", "express", "adonisjs", "spring-boot"],
    governance="NestJS / community", license_name="MIT",
    source_urls=[("https://docs.nestjs.com/", "NestJS documentation"), ("https://docs.nestjs.com/first-steps", "NestJS first steps")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("nestjs", "angular", "inspired-by", "module、decorator、DIなどAngularに近い構造をサーバー側へ採用した。", grade="A", state="verified", source_url="https://docs.nestjs.com/")
relation("nestjs", "express", "built-on", "既定HTTP adapterとしてExpressを利用できる。", grade="A", state="verified", source_url="https://docs.nestjs.com/first-steps")
relation("nestjs", "fastify", "built-on", "代替HTTP adapterとしてFastifyを利用できる。", grade="A", state="verified", source_url="https://docs.nestjs.com/techniques/performance")

add(
    "fastify", "Fastify", "JavaScript", "web-framework",
    ["web-backend", "api"], "fastify/fastify", "https://fastify.dev/",
    "低オーバーヘッド、schema駆動の検証・serialization、明確なplugin encapsulationを重視するNode.js Webフレームワーク。",
    ["Node APIの性能と予測可能性を高める", "plugin間の依存とscopeを管理する", "JSON Schemaを境界契約に使う"],
    "Express互換の単純さを保ちながら、性能、schema、plugin構造を設計の中心に置くNodeフレームワークとして作られた。",
    ["Schema-based validation", "Compiled serialization", "Plugin encapsulation", "Lifecycle hooks", "Low overhead"],
    ["Routing", "Plugins", "Hooks", "Validation", "Serialization", "Logging"],
    ["高いthroughputを得やすい", "pluginのscopeが明確", "schemaから検証とserializationを最適化"],
    ["schema管理が追加負担", "Express middlewareをそのまま使えない場合がある", "plugin encapsulationの理解が必要"],
    ["高負荷JSON API", "Nodeでschemaを中心に設計", "plugin単位の分離を重視"],
    ["Express middleware互換を最優先", "HTMLフルスタックが主目的"],
    ["express", "hono", "nestjs", "koa"],
    governance="OpenJS Foundation", license_name="MIT",
    source_urls=[("https://fastify.dev/docs/latest/Reference/Principles/", "Fastify principles"), ("https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/", "Validation and serialization")],
    origin_evidence="supported", lineage_evidence="partial",
)
relation("fastify", "json-schema", "implements", "JSON Schemaを検証と高速serializationの契約として用いる。", grade="A", state="verified", source_url="https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/", target_kind="idea")

add(
    "phoenix", "Phoenix Framework", "Elixir", "web-framework",
    ["web-fullstack", "web-backend", "realtime"], "phoenixframework/phoenix", "https://www.phoenixframework.org/",
    "ElixirとErlang/OTP上で、高並行・耐障害なWeb、リアルタイム通信、HTMLアプリを構築するフレームワーク。",
    ["多数の同時接続とリアルタイム更新を保守可能にする", "OTPのprocessとsupervisionをWeb開発へ統合する"],
    "Rails経験を持つChris McCordが、Erlang VMの並行性と耐障害性を現代的なWeb開発体験へ結び付ける目的で作った。",
    ["Actor-style processes", "Supervision", "Functional core", "Channels", "HTML-over-the-wire with LiveView"],
    ["Router/controllers", "Channels", "PubSub", "Presence", "LiveView ecosystem", "Ecto integration"],
    ["リアルタイムと多数接続に強い", "障害分離と復旧モデルが明確", "サーバー中心で豊かなUIを構築可能"],
    ["BEAM/OTPの学習が必要", "CPU集約処理は分離が必要", "主流Web人材・ライブラリがJS/Javaより少ない"],
    ["チャット、監視、共同編集", "長時間接続", "耐障害な分散Web"],
    ["CPU集約処理が中心", "既存JVM/.NET資産への密結合が必須"],
    ["rails", "django", "aspnet-core"],
    governance="Phoenix core team / community", license_name="MIT",
    source_urls=[("https://www.phoenixframework.org/", "Phoenix Framework"), ("https://hexdocs.pm/phoenix/overview.html", "Phoenix overview")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("phoenix", "rails", "inspired-by", "ルーティングや生産性重視のWeb体験にRails系譜を持つ一方、OTPモデルへ再設計した。", grade="B", state="supported")
relation("phoenix", "erlang-otp", "built-on", "BEAM process、supervision、distributionを基盤とする。", grade="A", state="verified", source_url="https://hexdocs.pm/phoenix/overview.html", target_kind="idea")

add(
    "gin", "Gin", "Go", "web-framework", ["web-backend", "api"], "gin-gonic/gin", "https://gin-gonic.com/",
    "高速ルーティングとmiddlewareを小さなAPIで提供するGoのHTTP Webフレームワーク。",
    ["標準net/httpより簡潔にAPIを記述する", "低い割当と高速ルーティングを維持する"],
    "Goの標準HTTPモデルを保ちながら、Martini風の使いやすさを性能重視で再構成した。",
    ["Radix-tree routing", "Middleware", "Minimal abstraction", "net/http interoperability"],
    ["Routing", "Binding/validation", "Middleware", "Rendering", "Recovery"],
    ["学習しやすく普及している", "高い処理性能", "標準ライブラリと組み合わせやすい"],
    ["アプリ全体の構造は提供しない", "contextに責務を集めすぎやすい", "複雑なAPI契約は追加設計が必要"],
    ["GoのREST API", "軽量サービス", "標準HTTPに近い構成"],
    ["フルスタック機能や強いDIが必要", "標準net/httpだけで十分"],
    ["echo", "fiber", "chi", "go-zero"],
    governance="Community", license_name="MIT",
    source_urls=[("https://gin-gonic.com/docs/", "Gin documentation"), ("https://github.com/gin-gonic/gin", "Gin repository")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("gin", "martini", "inspired-by", "READMEはMartiniに似たAPIを、より高い性能で提供する位置付けを示してきた。", grade="B", state="supported", source_url="https://github.com/gin-gonic/gin", target_kind="idea")

add(
    "axum", "Axum", "Rust", "web-framework", ["web-backend", "api", "async"], "tokio-rs/axum", "https://github.com/tokio-rs/axum",
    "Tokio、Tower、Hyperの型とmiddlewareエコシステムを組み合わせ、ergonomicで型安全なRust HTTPサービスを作るフレームワーク。",
    ["Rust async HTTP部品を一貫したAPIへ統合する", "macroや独自middleware体系への依存を減らす"],
    "Tokioチームが既存のHyperとTowerを直接活用し、共通middleware資産と型駆動extractorを中心に設計した。",
    ["Typed extractors", "Tower Service", "Async/await", "Minimal macro use", "Composable routers"],
    ["Routing", "Extractors", "Responses", "Tower middleware", "WebSockets"],
    ["Rustの型で境界を表現", "Towerエコシステムを再利用", "基盤部品との関係が明確"],
    ["型エラーが長くなりやすい", "Rust asyncとownershipの学習が必要", "統合フルスタック機能は別選択"],
    ["安全性と性能が重要なAPI", "Tower/Hyper資産を使う", "明示的な構成を好む"],
    ["迅速なCRUDでRustの学習コストを許容できない", "統合ORM/管理画面が必須"],
    ["actix-web", "rocket", "warp", "poem"],
    governance="Tokio project", license_name="MIT",
    source_urls=[("https://docs.rs/axum/latest/axum/", "Axum documentation"), ("https://github.com/tokio-rs/axum", "Axum repository")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("axum", "tower", "built-on", "middlewareとservice抽象化にTowerを利用する。", grade="A", state="verified", source_url="https://docs.rs/axum/latest/axum/", target_kind="idea")
relation("axum", "hyper", "built-on", "HTTP実装はHyperエコシステムを基盤とする。", grade="A", state="verified", source_url="https://docs.rs/axum/latest/axum/", target_kind="idea")

add(
    "ktor", "Ktor", "Kotlin", "web-framework", ["web-backend", "client", "async"], "ktorio/ktor", "https://ktor.io/",
    "Kotlin coroutineとDSLを中心に、非同期サーバーとHTTP clientを構築する軽量フレームワーク。",
    ["Kotlinらしい型とcoroutineでHTTPを扱う", "必要なpluginだけを組み合わせる"],
    "JetBrainsがKotlinの言語機能とcoroutineを活かし、JVMの既存Javaフレームワークより軽量でKotlin-nativeなWeb体験を目指した。",
    ["Coroutine-first", "Kotlin DSL", "Plugin pipeline", "Multiplatform client", "Engine abstraction"],
    ["Server routing", "HTTP client", "Authentication", "Content negotiation", "WebSockets"],
    ["Kotlinコードとの一体感", "小さく構成できる", "client/serverで概念を共有"],
    ["統合ORMや管理機能はない", "plugin選択とアーキテクチャを自分で決める", "Spring資産との直接互換は限定的"],
    ["Kotlin中心チーム", "coroutine I/O", "軽量APIとclient共有"],
    ["Spring標準との完全統合が必要", "batteries-includedを求める"],
    ["spring-boot", "http4k", "micronaut"],
    governance="JetBrains / community", license_name="Apache-2.0",
    source_urls=[("https://ktor.io/docs/welcome.html", "Ktor documentation")],
    origin_evidence="supported", lineage_evidence="partial",
)
relation("ktor", "kotlin-coroutines", "built-on", "非同期処理と構造化並行性にKotlin coroutineを利用する。", grade="A", state="verified", source_url="https://ktor.io/docs/welcome.html", target_kind="idea")

add(
    "vapor", "Vapor", "Swift", "web-framework", ["web-backend", "api"], "vapor/vapor", "https://vapor.codes/",
    "SwiftNIO上で型安全なルーティング、middleware、ORM統合を提供するSwiftサーバーフレームワーク。",
    ["Swiftの型安全性をサーバー開発へ持ち込む", "Appleプラットフォームと共有しやすいモデルを提供する"],
    "Swiftのオープンソース化後に、サーバー側Swiftを実用化するコミュニティプロジェクトとして成長した。",
    ["Swift type safety", "Non-blocking I/O", "Async/await", "Middleware", "Package Manager integration"],
    ["Routing", "Content coding", "Fluent ORM", "Authentication", "WebSockets"],
    ["client/serverでSwift型を共有しやすい", "高性能なNIO基盤", "Swift Package Managerで統合"],
    ["サーバー側Swiftの人材とライブラリが少ない", "NIOイベントループの理解が必要", "Linux運用知識が別途必要"],
    ["Swift中心組織のAPI", "iOSとモデル共有", "型安全を重視"],
    ["既存JavaScript/Python資産を大量利用", "最大のサーバーecosystemが必要"],
    ["hummingbird", "ktor", "aspnet-core"],
    governance="Vapor community", license_name="MIT",
    source_urls=[("https://docs.vapor.codes/", "Vapor documentation"), ("https://github.com/vapor/vapor", "Vapor repository")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("vapor", "swift-nio", "built-on", "非同期ネットワークI/OにSwiftNIOを利用する。", grade="A", state="verified", source_url="https://docs.vapor.codes/", target_kind="idea")

# ---------------------------------------------------------------------------
# Deep profiles: frontend and meta-frameworks
# ---------------------------------------------------------------------------
add(
    "react", "React", "JavaScript", "ui-library", ["web-frontend", "ui"], "facebook/react", "https://react.dev/",
    "宣言的componentと一方向データフローでUIを状態の関数として記述するライブラリ。フレームワークではないが、現代の多数のmeta-frameworkの中心基盤。",
    ["状態変化に伴うDOM更新を手作業から切り離す", "再利用可能componentで大規模UIを分割する"],
    "Facebook内部の複雑なUI更新問題から生まれ、2013年に公開。テンプレート分離よりもcomponent内で表示とロジックをco-locateする設計を広めた。",
    ["Declarative UI", "Component model", "One-way data flow", "Reconciliation", "Hooks"],
    ["Components", "Hooks", "Context", "Concurrent rendering primitives", "Server Components integration"],
    ["巨大なecosystem", "UIを合成可能な単位へ分割", "複数rendererとmeta-frameworkが利用"],
    ["routingやdata fetchingは単体で規定しない", "状態・effect設計を誤ると複雑化", "ecosystem変化が速い"],
    ["複雑な対話UI", "React基盤meta-frameworkを使う", "Webとnativeで概念共有"],
    ["極小静的ページ", "依存なしWeb Componentsのみを求める"],
    ["vue", "angular", "svelte", "solidjs"],
    governance="Meta / community", license_name="MIT",
    source_urls=[("https://react.dev/learn/thinking-in-react", "Thinking in React"), ("https://react.dev/blog/2013/06/05/why-react", "Why React")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("react", "declarative-ui", "implements", "UIを状態から導出する宣言的componentモデルを採用する。", grade="A", state="verified", source_url="https://react.dev/learn/thinking-in-react", target_kind="idea")
relation("react", "one-way-data-flow", "implements", "親から子へデータを渡す一方向モデルを中心にする。", grade="A", state="verified", source_url="https://react.dev/learn/thinking-in-react", target_kind="idea")

add(
    "angularjs", "AngularJS", "JavaScript", "ui-framework", ["web-frontend"], "angular/angular.js", "https://code.angularjs.org/",
    "HTMLを拡張するdirective、two-way binding、DIを使ってSPAを構築した初期JavaScriptフレームワーク。現在はサポート終了。",
    ["DOM操作とモデル同期の定型コードを削減する", "ブラウザ内アプリへ構造とDIを導入する"],
    "Googleで開発され、宣言的HTMLとtwo-way data bindingによってjQuery中心の手続き的UIからの転換を促した。大規模化時の性能と複雑性が後継Angular再設計の背景になった。",
    ["Two-way data binding", "Directives", "Dependency injection", "Digest cycle", "MVC/MVVM hybrid"],
    ["Templates", "Controllers", "Services", "Directives", "Routing ecosystem"],
    ["当時のDOM同期を大幅に簡略化", "DIとtestabilityを普及", "SPAフレームワーク史上重要"],
    ["digest cycleの性能と予測が難しい", "scope継承が複雑", "公式サポート終了"],
    ["歴史研究", "既存AngularJSシステムの移行計画"],
    ["新規本番開発"],
    ["angular", "react", "vue"],
    aliases=["Angular 1.x"], status="discontinued", governance="Google (historical)", license_name="MIT",
    source_urls=[("https://docs.angularjs.org/misc/version-support-status", "AngularJS support status"), ("https://github.com/angular/angular.js", "AngularJS repository")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("angularjs", "two-way-data-binding", "implements", "モデルとviewの双方向同期をdigest cycleで実現した。", grade="A", state="verified", source_url="https://docs.angularjs.org/guide/databinding", target_kind="idea")

add(
    "angular", "Angular", "TypeScript", "ui-framework", ["web-frontend", "web-fullstack"], "angular/angular", "https://angular.dev/",
    "TypeScript、component、DI、signals、routing、forms、SSR、toolingを統合する大規模Webアプリ向けフレームワーク。",
    ["大規模SPAに統一アーキテクチャとtoolingを提供する", "型、DI、build、testing、SSRを一つの更新方針で管理する"],
    "AngularJSの大規模化と性能上の課題を受け、componentとTypeScript中心へ互換性を切って再設計された。",
    ["Component architecture", "Dependency injection", "Reactive primitives", "Ahead-of-time compilation", "Integrated platform"],
    ["Router", "Forms", "Signals", "HTTP", "SSR/hydration", "CLI", "Testing support"],
    ["公式の統合選択肢が多い", "大規模チームで規約を共有", "長期更新toolingが整う"],
    ["概念とAPIの学習量が多い", "bundleとruntimeを意識した最適化が必要", "更新migrationが継続的に必要"],
    ["大規模業務SPA", "強い型とDIを標準化", "長期的な公式更新経路を重視"],
    ["極小widget", "自由なlibrary選択を優先"],
    ["react", "vue", "svelte"],
    aliases=["Angular 2+"], governance="Google / community", license_name="MIT",
    source_urls=[("https://angular.dev/overview", "Angular overview"), ("https://blog.angular.dev/angular-2-0-0-7780052f66a3", "Angular 2 release")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("angular", "angularjs", "successor-of", "AngularJSを互換性なしでcomponent/TypeScript中心へ再設計した後継。", grade="A", state="verified", source_url="https://blog.angular.dev/angular-2-0-0-7780052f66a3")
relation("angular", "dependency-injection", "implements", "framework全体のservice構成に階層DIを用いる。", grade="A", state="verified", source_url="https://angular.dev/guide/di", target_kind="idea")

add(
    "vue", "Vue.js", "TypeScript", "ui-framework", ["web-frontend"], "vuejs/core", "https://vuejs.org/",
    "段階的導入、Single-File Components、reactive state、templateを組み合わせる親しみやすいWeb UIフレームワーク。",
    ["既存HTMLへ小さく導入しつつSPAへ拡張する", "宣言的UIとreactivityを低い導入障壁で提供する"],
    "Evan YouがAngularJSの良い部分をより軽く柔軟に再構成する実験から始め、React系component設計も取り込みながら独自のreactivityを発展させた。",
    ["Progressive adoption", "Fine-grained reactivity", "Single-File Components", "Composition API", "Template/compiler integration"],
    ["Components", "Reactivity", "Transitions", "SSR", "Router/store ecosystem", "Devtools"],
    ["導入が段階的", "templateとTypeScriptの均衡", "公式ecosystemがまとまっている"],
    ["Options/Composition APIなど複数流儀が混在", "compiler magicの理解が必要", "大規模設計規約はチームで補う"],
    ["段階的なフロントエンド刷新", "中規模SPA", "HTMLに近い記法を好む"],
    ["React固有ecosystemが必須", "runtimeを極小にしたい"],
    ["react", "angular", "svelte", "solidjs"],
    governance="Vue core team / community", license_name="MIT",
    source_urls=[("https://vuejs.org/guide/introduction.html", "Vue introduction"), ("https://vuejs.org/about/faq.html", "Vue FAQ")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("vue", "angularjs", "inspired-by", "初期VueはAngularJSのdata binding/directive体験を軽量に再考した系譜。", grade="B", state="supported")
relation("vue", "react", "inspired-by", "componentと一方向propsなどReact系の設計と共通点があるが、明示的な一次資料をさらに整理する。", grade="C", state="hypothesis")
relation("vue", "fine-grained-reactivity", "implements", "依存追跡により必要な更新を反応的に伝播する。", grade="A", state="verified", source_url="https://vuejs.org/guide/extras/reactivity-in-depth.html", target_kind="idea")

add(
    "svelte", "Svelte", "JavaScript", "ui-framework", ["web-frontend"], "sveltejs/svelte", "https://svelte.dev/",
    "多くのUI処理をbuild時にコンパイルし、componentコードを効率的なDOM更新へ変換するWeb UIフレームワーク。",
    ["virtual DOMをruntimeで維持するコストを減らす", "HTML/CSS/JavaScriptに近いcomponent記法でreactivityを提供する"],
    "Rich HarrisがRactiveなどでの経験をもとに、frameworkをブラウザへ配るのではなくcompile stepへ移す発想を推し進めた。",
    ["Compiler-first", "Reactive assignments/signals", "Scoped CSS", "Minimal runtime", "Single-file components"],
    ["Components", "Transitions", "Stores", "Actions", "SSR support", "SvelteKit ecosystem"],
    ["出力runtimeが小さくなりやすい", "簡潔なcomponent記法", "compilerによる最適化"],
    ["compiler semanticsを理解する必要", "ecosystemはReactより小さい", "大規模規約はmeta-frameworkやチーム設計に依存"],
    ["高速で軽いWeb UI", "component単位のCSSを重視", "SvelteKitを利用"],
    ["React library資産が必須", "runtime dynamic component生成を極端に多用"],
    ["vue", "react", "solidjs"],
    governance="Svelte team / community", license_name="MIT",
    source_urls=[("https://svelte.dev/docs/svelte/overview", "Svelte overview"), ("https://svelte.dev/blog/frameworks-without-the-framework", "Frameworks without the framework")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("svelte", "ractive", "inspired-by", "作者のRactive経験を背景にcompiler-first UIへ発展した。", grade="B", state="supported", target_kind="idea")
relation("svelte", "compiler-first-ui", "implements", "componentをbuild時にDOM更新コードへ変換する。", grade="A", state="verified", source_url="https://svelte.dev/blog/frameworks-without-the-framework", target_kind="idea")

add(
    "solidjs", "SolidJS", "TypeScript", "ui-library", ["web-frontend"], "solidjs/solid", "https://www.solidjs.com/",
    "JSXとReactに似たcomponent記法を使いながら、virtual DOMではなくfine-grained reactivityでDOMを直接更新するUIライブラリ。",
    ["React風ergonomicsと細粒度更新を両立する", "component再実行を中心としないreactive modelを提供する"],
    "Knockoutなどのreactive primitiveとReactのcomponent表現を組み合わせ、compileとsignal graphで高効率更新を目指した。",
    ["Fine-grained reactivity", "Signals", "JSX compilation", "No virtual DOM", "Component runs once"],
    ["Signals", "Control flow", "Resources", "Context", "SSR/hydration"],
    ["更新範囲が細かい", "JSX/TypeScriptを利用できる", "runtime挙動が比較的直接的"],
    ["Reactと見た目が似ていて意味論を誤解しやすい", "ecosystemが小さい", "reactive ownershipの理解が必要"],
    ["高頻度更新UI", "signalsモデルを好む", "JSXを維持したい"],
    ["React専用libraryへの完全互換が必要", "template中心を好む"],
    ["react", "svelte", "vue"],
    governance="Community", license_name="MIT",
    source_urls=[("https://docs.solidjs.com/concepts/intro-to-reactivity", "Solid reactivity"), ("https://www.solidjs.com/about", "About Solid")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("solidjs", "react", "inspired-by", "JSXとcomponent compositionの表面APIにReact系譜を持つ。", grade="B", state="supported")
relation("solidjs", "fine-grained-reactivity", "implements", "signal依存グラフで更新対象を絞る。", grade="A", state="verified", source_url="https://docs.solidjs.com/concepts/intro-to-reactivity", target_kind="idea")

add(
    "ember", "Ember.js", "JavaScript", "ui-framework", ["web-frontend"], "emberjs/ember.js", "https://emberjs.com/",
    "強い規約、router、data、CLI、長期的なupgrade pathを重視するambitious Web application向けフレームワーク。",
    ["長寿命SPAに一貫した構造を与える", "ecosystem全体を協調して更新可能にする"],
    "SproutCore系譜から発展し、RailsのConvention over Configurationをクライアントアプリへ取り込んだ。",
    ["Convention over configuration", "Integrated router", "Stable upgrade path", "CLI-driven ecosystem", "Autotracking"],
    ["Components", "Router", "Services", "Ember Data", "CLI", "Testing conventions"],
    ["大規模チームで規約が揃う", "長期migration tooling", "統合testingとCLI"],
    ["初期学習と規約が重い", "ecosystem規模が縮小", "framework外の新技術採用が遅れる場合"],
    ["長寿命業務SPA", "強い規約とupgrade pathを優先"],
    ["小さなwidget", "自由なlibrary構成を求める"],
    ["angular", "react", "vue"],
    governance="Ember core teams / community", license_name="MIT",
    source_urls=[("https://emberjs.com/learn/", "Ember learning resources"), ("https://emberjs.com/about/", "About Ember")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("ember", "sproutcore", "successor-of", "SproutCore 2.0の系譜からEmberへ名称と方向性を発展させた。", grade="B", state="supported", target_kind="idea")
relation("ember", "rails", "inspired-by", "規約と一体化された生産性にRailsの影響を受けた。", grade="B", state="supported")

add(
    "nextjs", "Next.js", "TypeScript", "meta-framework", ["web-fullstack", "web-frontend", "serverless"], "vercel/next.js", "https://nextjs.org/",
    "Reactにrouting、server rendering、static generation、server components、data access、build/deploy規約を統合するmeta-framework。",
    ["React単体で未規定のrouting、rendering、data loading、optimizationを統合する", "同一codebaseで静的・動的・edge renderingを選ぶ"],
    "Zeit（現Vercel）がReactのuniversal renderingとfile-based routingを製品化し、hosting platformとの統合を強めながら発展した。",
    ["File-system routing", "Hybrid rendering", "Server Components", "Build-time/runtime integration", "Platform-aware optimization"],
    ["App Router", "SSR/SSG/ISR", "Server Actions", "Image/font optimization", "Route handlers"],
    ["React full-stackの標準的選択肢", "rendering方式をrouteごとに選べる", "deployment ecosystemが大きい"],
    ["cacheとserver/client境界が複雑", "Vercel最適化と他環境の差を理解する必要", "framework更新が速く設計変更が多い"],
    ["ReactでSEOとfull-stackを統合", "Vercelまたは対応platformへdeploy", "静的と動的を混在"],
    ["単純SPAのみ", "platform非依存の小さなruntimeを最優先"],
    ["remix", "nuxt", "sveltekit", "astro"],
    governance="Vercel / community", license_name="MIT",
    source_urls=[("https://nextjs.org/docs", "Next.js documentation"), ("https://nextjs.org/blog/next-1", "Next.js 1.0 announcement")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("nextjs", "react", "built-on", "Reactのrenderingとcomponent modelをfull-stack規約で統合する。", grade="A", state="verified", source_url="https://nextjs.org/docs")
relation("nextjs", "file-system-routing", "implements", "ファイル構造からURL routeとlayoutを導出する。", grade="A", state="verified", source_url="https://nextjs.org/docs/app/getting-started/project-structure", target_kind="idea")

add(
    "nuxt", "Nuxt", "TypeScript", "meta-framework", ["web-fullstack", "web-frontend"], "nuxt/nuxt", "https://nuxt.com/",
    "Vueにfile routing、SSR、static generation、server endpoints、module ecosystemを統合するfull-stack meta-framework。",
    ["Vueアプリのrouting、rendering、build、server構成を標準化する", "SEOとfull-stack機能を一つの開発体験にする"],
    "Next.jsのVue版という初期着想から始まり、Vue ecosystemに合わせたmodule、Nitro server、hybrid renderingへ独自発展した。",
    ["File-system routing", "Hybrid rendering", "Auto imports", "Universal deployment", "Module ecosystem"],
    ["SSR/SSG", "Nitro server", "Layouts/pages", "Data fetching", "Modules", "Devtools"],
    ["Vue full-stackを一体化", "deploy先adapterが多い", "公式module ecosystem"],
    ["auto importとconventionが挙動を隠す場合", "server/client境界とcache設計が必要", "小規模SPAには過剰"],
    ["VueでSEO/full-stack", "複数deploy target", "contentまたはWeb application"],
    ["Vue単体SPAで十分", "明示的importと最小toolingを最優先"],
    ["nextjs", "sveltekit", "astro"],
    governance="NuxtLabs / community", license_name="MIT",
    source_urls=[("https://nuxt.com/docs/getting-started/introduction", "Nuxt introduction"), ("https://github.com/nuxt/nuxt", "Nuxt repository")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("nuxt", "vue", "built-on", "Vue component/reactivityをfull-stack規約へ統合する。", grade="A", state="verified", source_url="https://nuxt.com/docs/getting-started/introduction")
relation("nuxt", "nextjs", "inspired-by", "初期NuxtはNext.jsのVue版という問題設定から始まった。", grade="B", state="supported")

add(
    "remix", "React Router Framework Mode / Remix", "TypeScript", "meta-framework", ["web-fullstack", "web-frontend"], "remix-run/react-router", "https://reactrouter.com/",
    "Web標準のRequest/Response、nested routes、loader/action、progressive enhancementを中心にしたReact full-stack frameworkの系譜。",
    ["client stateへ偏り過ぎずHTTPとbrowser標準を活用する", "route単位にdata loading、mutation、error boundaryをまとめる"],
    "React Routerの作者がRemixとして開始し、Web platformのform/navigation/cacheを再評価。後にframework機能がReact Routerへ統合された。",
    ["Web standards", "Nested routing", "Route modules", "Progressive enhancement", "Server/client symmetry"],
    ["Loaders/actions", "Forms and navigation", "Streaming", "Error boundaries", "Adapters"],
    ["HTTPとbrowser動作に沿う", "JavaScript失敗時も段階的に動作可能", "route単位の責務が明確"],
    ["React Router/Remixの名称・version移行を理解する必要", "cache方針がNext.jsと異なる", "SPAのみにはserver概念が多い"],
    ["formとnavigation中心Web application", "Web標準とprogressive enhancementを重視"],
    ["静的サイトだけ", "React以外を選ぶ"],
    ["nextjs", "tanstack-start", "sveltekit"],
    aliases=["Remix"], governance="Shopify / React Router team", license_name="MIT",
    source_urls=[("https://reactrouter.com/home", "React Router documentation"), ("https://remix.run/blog/merging-remix-and-react-router", "Merging Remix and React Router")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("remix", "react", "built-on", "React UIをroute moduleとWeb標準data flowへ統合する。", grade="A", state="verified", source_url="https://reactrouter.com/home")
relation("remix", "react-router", "successor-of", "Remixのframework機能がReact Routerのframework modeへ統合された系譜。", grade="A", state="verified", source_url="https://remix.run/blog/merging-remix-and-react-router", target_kind="idea")
relation("remix", "progressive-enhancement", "implements", "HTML formとbrowser navigationを基盤にJavaScriptで強化する。", grade="A", state="verified", source_url="https://reactrouter.com/explanation/progressive-enhancement", target_kind="idea")

add(
    "astro", "Astro", "TypeScript", "meta-framework", ["web-frontend", "content", "web-fullstack"], "withastro/astro", "https://astro.build/",
    "content中心サイトでclient JavaScriptを既定で減らし、複数UI frameworkをislandsとして部分的にhydrateするmeta-framework。",
    ["静的content siteで不要なJavaScript配信を減らす", "React/Vue/Svelte等を必要箇所だけ共存させる"],
    "islands architectureとpartial hydrationの流れを、component framework横断のbuild systemとして実用化した。",
    ["Islands architecture", "Zero JS by default", "Partial hydration", "Multi-framework components", "Content collections"],
    ["Static/SSR", "Astro components", "UI integrations", "Content collections", "Server islands"],
    ["content siteの性能設計が明確", "既存componentを混在可能", "JavaScript量を意識しやすい"],
    ["高度なclient application stateには別frameworkが必要", "複数framework混在は保守を難しくする", "island境界設計が必要"],
    ["documentation、blog、marketing、commerce content", "部分的interactivity"],
    ["全画面が高度なSPA", "単一frameworkのclient state共有が中心"],
    ["nextjs", "nuxt", "sveltekit", "eleventy"],
    governance="Astro Technology Company / community", license_name="MIT",
    source_urls=[("https://docs.astro.build/en/concepts/islands/", "Astro islands architecture"), ("https://astro.build/blog/introducing-astro/", "Introducing Astro")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("astro", "islands-architecture", "implements", "独立した対話componentだけをhydrateするislands modelを採用する。", grade="A", state="verified", source_url="https://docs.astro.build/en/concepts/islands/", target_kind="idea")

add(
    "qwik", "Qwik", "TypeScript", "ui-framework", ["web-frontend", "web-fullstack"], "QwikDev/qwik", "https://qwik.dev/",
    "初期hydrateでアプリ全体を再実行せず、serverで中断した状態をresumabilityによってbrowserで必要時に再開するframework。",
    ["大規模Webアプリのhydration costを減らす", "codeをinteraction単位で遅延loadする"],
    "AngularJS/Angularの作者として知られるMiško Heveryらが、hydrationを最適化するのではなく不要にする方向で設計した。",
    ["Resumability", "Fine-grained lazy loading", "Serializable closures", "Optimizer compiler", "Server/client continuation"],
    ["Qwik components", "Signals", "QRL lazy references", "Qwik City", "SSR"],
    ["初期JavaScript実行を抑えやすい", "interaction単位の自動code splitting", "server-rendered stateを再利用"],
    ["serialization制約とcompiler modelの学習が必要", "ecosystemが小さい", "一般的hydration frameworkと異なるdebug model"],
    ["初期表示とinteraction latencyを厳しく管理", "大規模SSR application"],
    ["豊富な既存React plugin互換が必須", "単純SPAでSSR不要"],
    ["react", "solidjs", "astro"],
    governance="Builder.io / community", license_name="MIT",
    source_urls=[("https://qwik.dev/docs/concepts/resumable/", "Qwik resumability"), ("https://qwik.dev/docs/overview/", "Qwik overview")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("qwik", "resumability", "implements", "serverで直列化した実行状態をclientで必要時に再開する。", grade="A", state="verified", source_url="https://qwik.dev/docs/concepts/resumable/", target_kind="idea")
relation("qwik", "angular", "inspired-by", "作者のAngular経験が背景にあるが、直接採用した設計項目は個別に検証する。", grade="D", state="hypothesis")

# ---------------------------------------------------------------------------
# Deep profiles: mobile, desktop, and cross-platform UI
# ---------------------------------------------------------------------------
add(
    "flutter", "Flutter", "Dart", "ui-framework", ["mobile", "desktop", "web-frontend"], "flutter/flutter", "https://flutter.dev/",
    "Dartコードから独自rendering stackでmobile、web、desktopのUIを構築するcross-platform application framework。",
    ["複数platformでUIとbusiness logicを共有する", "platform widget差をframework側で吸収し一貫した描画を行う"],
    "Googleが高い描画一貫性と高速な開発cycleを重視して開発し、Dart VMのhot reloadと独自engineを組み合わせた。",
    ["Widget tree", "Declarative UI", "Own rendering engine", "Hot reload", "Single codebase"],
    ["Material/Cupertino widgets", "Navigation", "Animation", "Accessibility", "Platform channels", "DevTools"],
    ["UIをplatform横断で共有しやすい", "描画の一貫性", "hot reloadとtoolingが強い"],
    ["app sizeとengine cost", "platform-native UIとの細部差", "Dart ecosystemへの依存", "webではDOM中心frameworkと特性が異なる"],
    ["brand UIを複数platformへ展開", "同一teamでmobile/desktop/webを担当", "複雑なcustom animation"],
    ["platform純正UIとAPIへ最大限密着", "小さなWeb content site"],
    ["react-native", "dotnet-maui", "compose-multiplatform"],
    governance="Google / community", license_name="BSD-3-Clause",
    source_urls=[("https://docs.flutter.dev/resources/architectural-overview", "Flutter architectural overview"), ("https://flutter.dev/multi-platform", "Flutter multi-platform")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("flutter", "react", "inspired-by", "宣言的component/widget treeと状態からUIを導出する考えにReact系譜との類似がある。明示範囲は追加検証する。", grade="C", state="hypothesis")
relation("flutter", "declarative-ui", "implements", "immutable widget descriptionからelement/render objectを更新する。", grade="A", state="verified", source_url="https://docs.flutter.dev/resources/architectural-overview", target_kind="idea")

add(
    "react-native", "React Native", "JavaScript", "ui-framework", ["mobile"], "facebook/react-native", "https://reactnative.dev/",
    "Reactのcomponent modelを使い、JavaScript/TypeScriptからnative platform UIと機能を構築するmobile framework。",
    ["Web Reactの知識をnative app開発へ再利用する", "iOS/Android間でUI logicを共有しつつnative moduleへ接続する"],
    "Facebook内部のmobile開発で、WebView hybridではなくReactの宣言的modelをnative UIへ適用するために作られた。",
    ["React renderer", "Native components", "Bridge/JSI", "Declarative UI", "Platform-specific escape hatches"],
    ["Core components", "Native modules", "Fast Refresh", "Hermes", "New Architecture/Fabric"],
    ["React人材と知識を活用", "native UIを利用", "platform間でlogicを共有"],
    ["native build/toolchain知識が必要", "third-party native moduleの互換性", "platform差を完全には隠せない"],
    ["React組織のmobile app", "native UIとcross-platform共有を両立"],
    ["高性能game/graphics中心", "platform固有UXを完全に別実装する"],
    ["flutter", "ionic", "dotnet-maui"],
    governance="Meta / community", license_name="MIT",
    source_urls=[("https://reactnative.dev/docs/intro-react-native-components", "React Native core concepts"), ("https://reactnative.dev/architecture/overview", "React Native architecture")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("react-native", "react", "built-on", "React reconcilerとcomponent modelをnative rendererへ適用する。", grade="A", state="verified", source_url="https://reactnative.dev/docs/intro-react-native-components")

add(
    "expo", "Expo", "TypeScript", "platform", ["mobile", "web-frontend"], "expo/expo", "https://expo.dev/",
    "React Nativeのbuild、native API、update、routing、development client、cloud serviceを統合するapplication platform。",
    ["React Nativeで毎回必要なnative setupとdistributionを簡略化する", "同一toolchainでiOS、Android、Webを扱う"],
    "React Nativeの導入・build・device API利用の摩擦を減らすtoolchainとして始まり、managed/native双方を扱うplatformへ発展した。",
    ["Managed workflow", "Native modules SDK", "Config plugins", "Over-the-air updates", "Universal app tooling"],
    ["Expo Router", "EAS Build/Submit/Update", "Development builds", "Device APIs", "Web support"],
    ["環境構築とdistributionが速い", "一般的device APIが統一", "必要時にnative projectへ移行可能"],
    ["cloud service依存を評価する必要", "特殊native機能はcustom moduleが必要", "Expo SDK更新cycleへの追随"],
    ["React Native製品を迅速に構築", "small teamでbuild/releaseを標準化"],
    ["完全に独自native build pipelineが必須", "React Nativeを使わない"],
    ["react-native", "flutter", "ionic"],
    governance="Expo / community", license_name="MIT",
    source_urls=[("https://docs.expo.dev/core-concepts/", "Expo core concepts"), ("https://github.com/expo/expo", "Expo repository")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("expo", "react-native", "built-on", "React Nativeを中心にbuild、module、distributionを統合する。", grade="A", state="verified", source_url="https://docs.expo.dev/core-concepts/")

add(
    "ionic", "Ionic Framework", "TypeScript", "ui-framework", ["mobile", "web-frontend"], "ionic-team/ionic-framework", "https://ionicframework.com/",
    "Web ComponentsとWeb技術でmobile風UIを作り、Capacitorを通じてnative device機能へ接続するcross-platform UI framework。",
    ["Web開発者がmobile appを構築する", "一つのWeb codebaseをiOS/Android/Webへ展開する"],
    "AngularJSとCordovaを組み合わせたhybrid mobile frameworkとして始まり、後にframework-neutralなWeb ComponentsとCapacitorへ移行した。",
    ["Web Components", "Adaptive UI", "Hybrid app", "Framework integrations", "Native bridge through Capacitor"],
    ["Mobile UI components", "Gestures", "Theming", "React/Vue/Angular integration", "Capacitor ecosystem"],
    ["Web人材をそのまま活用", "PWAとmobileを共有", "UI componentが豊富"],
    ["native UIそのものではない", "高負荷animation/graphicsは制約", "WebViewとnative bridgeの性能・debug理解が必要"],
    ["業務mobile、PWA、content中心app", "Web codebase共有を最優先"],
    ["高度なnative graphics", "platform固有UIを厳密に再現"],
    ["react-native", "flutter", "nativescript"],
    governance="Ionic / community", license_name="MIT",
    source_urls=[("https://ionicframework.com/docs", "Ionic documentation"), ("https://ionicframework.com/docs/reference/glossary", "Ionic glossary")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("ionic", "angularjs", "built-on", "初期IonicはAngularJSを主要UI/application modelとして利用した。", grade="B", state="supported")
relation("ionic", "cordova", "built-on", "初期hybrid native accessはCordova ecosystemを利用し、後にCapacitorへ重点を移した。", grade="B", state="supported", target_kind="idea")
relation("ionic", "web-components", "implements", "現行UI componentのframework-neutralな基盤としてWeb Componentsを採用する。", grade="A", state="verified", source_url="https://ionicframework.com/docs", target_kind="idea")

add(
    "jetpack-compose", "Jetpack Compose", "Kotlin", "ui-framework", ["mobile", "android", "desktop"], "androidx/androidx", "https://developer.android.com/compose",
    "Kotlinの宣言的関数でAndroid UIを構築し、state変化に応じて必要箇所をrecomposeする公式toolkit。",
    ["XML viewとimperative更新の分離を減らす", "UIをstateから導出しKotlin内で合成する"],
    "Android View systemの複雑な状態同期を改善するため、declarative UIとcompiler pluginを採用してGoogleが開発した。",
    ["Declarative UI", "Composition", "Recomposition", "State hoisting", "Compiler-assisted optimization"],
    ["Material components", "Layouts", "Animation", "Navigation integration", "Accessibility", "Preview"],
    ["Kotlin内でUIとlogicを統合", "再利用可能な小component", "公式Androidtoolingとの統合"],
    ["recompositionとstate ownershipの理解が必要", "既存View interoperabilityが移行負担", "頻繁なAPI/toolchain更新"],
    ["新規Android UI", "state-driven UI", "Kotlin標準化"],
    ["既存View大規模資産を変更しない", "特殊なlegacy widget依存"],
    ["swiftui", "flutter", "react-native"],
    governance="Google / Android Open Source Project", license_name="Apache-2.0",
    source_urls=[("https://developer.android.com/compose/mental-model", "Compose mental model"), ("https://developer.android.com/develop/ui/compose/why-adopt", "Why adopt Compose")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("jetpack-compose", "declarative-ui", "implements", "UIをstateの関数として記述し、必要箇所をrecomposeする。", grade="A", state="verified", source_url="https://developer.android.com/compose/mental-model", target_kind="idea")
relation("jetpack-compose", "react", "inspired-by", "declarative componentとreconciliation系の発想にReactとの類似があるが直接関係の一次資料を追加確認する。", grade="D", state="hypothesis")

add(
    "swiftui", "SwiftUI", "Swift", "ui-framework", ["mobile", "desktop", "apple"], "", "https://developer.apple.com/xcode/swiftui/",
    "Swiftの宣言的view記述とdata flowでApple platform全体のUIを構築する公式framework。",
    ["UIKit/AppKitのimperative state同期を減らす", "Apple platform間でUI概念とcodeを共有する"],
    "AppleがSwiftの型、property wrapper、result builderを活かし、declarative UIを各platformへ統合するために導入した。",
    ["Declarative UI", "Value-type views", "Data flow wrappers", "Diffing", "Cross-Apple-platform composition"],
    ["Views/modifiers", "Navigation", "Animation", "Accessibility", "Previews", "UIKit/AppKit interoperability"],
    ["少ないcodeでUIを合成", "Apple ecosystemの公式方向", "platform間共有"],
    ["OS version差と非公開内部挙動", "複雑UIでperformance debugが難しい", "高度なplatform機能はUIKit/AppKitへescapeが必要"],
    ["新規Apple app", "複数Apple platform共有", "state-driven UI"],
    ["古いOSを広範囲に支援", "完全なcross-platformが必要"],
    ["jetpack-compose", "flutter", "react-native"],
    governance="Apple", license_name="proprietary SDK",
    source_urls=[("https://developer.apple.com/documentation/swiftui", "SwiftUI documentation"), ("https://developer.apple.com/videos/play/wwdc2019/204/", "Introducing SwiftUI")],
    origin_evidence="verified", lineage_evidence="partial",
)
relation("swiftui", "declarative-ui", "implements", "value型Viewとstate data flowでUIを宣言的に構成する。", grade="A", state="verified", source_url="https://developer.apple.com/documentation/swiftui", target_kind="idea")

add(
    "electron", "Electron", "JavaScript", "desktop-framework", ["desktop"], "electron/electron", "https://www.electronjs.org/",
    "ChromiumとNode.jsを同梱し、HTML/CSS/JavaScriptでcross-platform desktop applicationを作るframework。",
    ["Web技術でnative desktop appを配布する", "OS差をChromium/Nodeとmain-renderer modelで吸収する"],
    "GitHub Atom editor向けのAtom Shellとして作られ、後に汎用frameworkとしてElectronへ改名した。",
    ["Bundled Chromium", "Node.js integration", "Main/renderer processes", "IPC", "Web technology reuse"],
    ["Window/menu/tray APIs", "Auto update ecosystem", "Packaging", "DevTools", "Native modules"],
    ["Web人材とlibraryを活用", "表示のcross-platform一貫性", "成熟したdistribution ecosystem"],
    ["memory、disk、update sizeが大きい", "renderer security設定が重要", "native look/behaviorの調整"],
    ["複雑なcross-platform desktop UI", "Web applicationをdesktop化", "tooling/editor/chat app"],
    ["極小binaryと低memory", "platform-native UXを最優先"],
    ["tauri", "qt", "neutralinojs"],
    aliases=["Atom Shell"], governance="OpenJS Foundation / maintainers", license_name="MIT",
    source_urls=[("https://www.electronjs.org/docs/latest/tutorial/process-model", "Electron process model"), ("https://www.electronjs.org/blog/electron", "Electron announcement")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("electron", "atom-shell", "successor-of", "GitHub Atom向けAtom ShellからElectronへ改名・汎用化した。", grade="A", state="verified", source_url="https://www.electronjs.org/blog/electron", target_kind="idea")
relation("electron", "chromium", "built-on", "rendererにChromiumを同梱する。", grade="A", state="verified", source_url="https://www.electronjs.org/docs/latest/tutorial/process-model", target_kind="idea")
relation("electron", "nodejs", "built-on", "main processと許可されたcontextでNode.js APIを利用する。", grade="A", state="verified", source_url="https://www.electronjs.org/docs/latest/tutorial/process-model", target_kind="idea")

add(
    "tauri", "Tauri", "Rust", "desktop-framework", ["desktop", "mobile"], "tauri-apps/tauri", "https://tauri.app/",
    "OS標準WebViewとRust backendを組み合わせ、小さくsecurity-consciousなdesktop/mobile appを作るframework。",
    ["Electron型Web desktop appのbundleとmemory overheadを減らす", "frontendからnative capabilityへの権限を明示する"],
    "Web UIの生産性を維持しつつ、Chromiumを同梱せずsystem WebViewとRustを使う代替として成長した。",
    ["System WebView", "Rust core", "Capability security", "Frontend agnostic", "Small bundles"],
    ["Window/menu/tray", "Commands/IPC", "Updater", "Plugins", "Bundling", "Mobile support"],
    ["bundleが小さくなりやすい", "Rustでnative処理を安全に記述", "frontend frameworkを選べる"],
    ["WebView差がplatformごとに残る", "Rust/native build環境が必要", "Electronほどplugin資産が多くない"],
    ["軽量cross-platform desktop", "Web UIとRustを組み合わせる", "capability制御を重視"],
    ["全platformで同一Chromium挙動が必須", "Node native moduleを直接大量利用"],
    ["electron", "wails", "neutralinojs"],
    governance="Tauri Programme within Commons Conservancy", license_name="Apache-2.0/MIT",
    source_urls=[("https://v2.tauri.app/concept/architecture/", "Tauri architecture"), ("https://v2.tauri.app/security/", "Tauri security")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("tauri", "electron", "reaction-against", "Web desktop modelを保ちながらbundled Chromiumとresource costを避ける方向。", grade="B", state="supported")
relation("tauri", "system-webview", "built-on", "platform標準WebViewを利用してfrontendを表示する。", grade="A", state="verified", source_url="https://v2.tauri.app/concept/architecture/", target_kind="idea")

add(
    "qt", "Qt", "C++", "ui-framework", ["desktop", "embedded", "mobile"], "qt/qtbase", "https://www.qt.io/",
    "C++とQMLでcross-platform GUI、networking、multimedia、embedded applicationを構築する長寿命application framework。",
    ["複数OS・deviceでnative application機能を共通API化する", "UIだけでなくapplication infrastructureを統合する"],
    "1990年代にTrolltechでcross-platform GUI toolkitとして始まり、signals/slots、MOC、QMLを含む広範なframeworkへ発展した。",
    ["Signals and slots", "Meta-object system", "Widgets", "Declarative QML", "Cross-platform abstraction"],
    ["GUI", "Networking", "Multimedia", "SQL", "Concurrent", "Embedded tooling"],
    ["非常に広いplatformと機能", "長い実績", "native/embedded用途に強い"],
    ["license選択と商用条件の確認が必要", "buildとbinary sizeが大きくなり得る", "独自MOC/QML/toolingの学習"],
    ["長寿命desktop/embedded製品", "C++ codebase", "複数OSを同一teamで支援"],
    ["Web UIだけで十分", "極小embeddedでresourceが厳しい"],
    ["gtk", "wxwidgets", "avalonia", "flutter"],
    governance="Qt Group / Qt Project", license_name="LGPL/GPL/commercial",
    source_urls=[("https://doc.qt.io/qt-6/qtcore-index.html", "Qt Core"), ("https://wiki.qt.io/Qt_History", "Qt history")],
    origin_evidence="supported", lineage_evidence="partial",
)
relation("qt", "signals-and-slots", "implements", "object間の疎結合event communicationとしてsignals/slotsを中核にする。", grade="A", state="verified", source_url="https://doc.qt.io/qt-6/signalsandslots.html", target_kind="idea")

# ---------------------------------------------------------------------------
# Deep profiles: game frameworks and engines
# ---------------------------------------------------------------------------
add(
    "unity", "Unity", "C#", "game-engine", ["game", "xr", "simulation"], "Unity-Technologies/UnityCsReference", "https://unity.com/",
    "editor、scene/component model、rendering、physics、animation、asset pipeline、multi-platform exportを統合する商用game engine。",
    ["小規模teamでも複数platform向けgameを制作する", "editorとasset workflowをprogrammingと統合する"],
    "2000年代半ばにMac向けgame engineとして登場し、accessibleなeditorとasset ecosystem、広いplatform対応でindieからenterpriseへ拡大した。",
    ["GameObject/component", "Scene graph", "Editor-centric workflow", "Managed scripting", "Asset pipeline"],
    ["2D/3D rendering", "Physics", "Animation", "UI", "Networking ecosystem", "Build targets", "Asset Store"],
    ["学習資料とassetが豊富", "platform対応が広い", "editorで非programmerと協働"],
    ["license/business model変更リスク", "engine version upgrade cost", "低レイヤ制御とbuild sizeに制約"],
    ["mobile/indie/3D/XR", "artistとprogrammerの共同制作", "multi-platform release"],
    ["完全open-source要件", "独自renderer/engine研究が目的"],
    ["unreal-engine", "godot", "defold"],
    governance="Unity Technologies", license_name="proprietary with source reference",
    source_urls=[("https://docs.unity3d.com/Manual/CreatingGameplay.html", "Unity gameplay architecture"), ("https://unity.com/our-company", "Unity company")],
    origin_evidence="supported", lineage_evidence="partial",
)
relation("unity", "component-based-game-object", "implements", "GameObjectへcomponentを組み合わせて挙動を構築する。", grade="A", state="verified", source_url="https://docs.unity3d.com/Manual/CreatingGameplay.html", target_kind="idea")

add(
    "unreal-engine", "Unreal Engine", "C++", "game-engine", ["game", "xr", "simulation", "film"], "EpicGames/UnrealEngine", "https://www.unrealengine.com/",
    "high-end 3D rendering、editor、physics、animation、networking、visual scriptingを統合する大規模game/real-time engine。",
    ["AAA規模のreal-time 3D productionを統合する", "game以外のfilm、architecture、simulationへ高品質renderingを提供する"],
    "Epic GamesのUnreal game開発からengineとして外部提供され、世代ごとにrendererとtoolchainを拡張してきた。",
    ["Actor/component", "Editor-centric production", "C++ plus Blueprints", "High-end renderer", "Integrated networking"],
    ["Nanite/Lumen ecosystem", "Blueprints", "Animation", "Physics", "Replication", "World building"],
    ["高品質3Dと統合tool", "source access", "AAA production実績"],
    ["hardwareとbuild resource要求が高い", "巨大なAPIとtoolchain", "小規模2Dには過剰"],
    ["AAA/高品質3D", "virtual production", "large team simulation"],
    ["低spec PCで軽量2D", "極小runtime"],
    ["unity", "godot", "o3de"],
    governance="Epic Games", license_name="proprietary source-available EULA",
    source_urls=[("https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-for-new-users", "Unreal Engine documentation"), ("https://www.unrealengine.com/en-US/faq", "Unreal Engine FAQ")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("unreal-engine", "unreal-game", "extracted-from", "EpicのUnreal game向けtechnologyから汎用engineとして発展した。", grade="B", state="supported", target_kind="idea")

add(
    "godot", "Godot Engine", "C++", "game-engine", ["game", "2d", "3d"], "godotengine/godot", "https://godotengine.org/",
    "scene/node composition、専用2D/3D engine、editor、scriptingを備えたcommunity-driven open-source game engine。",
    ["license制約の少ない統合game engineを提供する", "sceneを再利用可能なnode treeとして構成する"],
    "Juan LinietskyとAriel Manzurが社内engineとして長年開発したものを2014年にopen source化し、独立foundation/communityへ拡大した。",
    ["Scene tree", "Nodes and signals", "Integrated editor", "Dedicated 2D", "Open-source governance"],
    ["GDScript/C#/C++ extensions", "Rendering", "Physics", "Animation", "UI", "Export templates"],
    ["MIT licenseと公開開発", "軽量editor", "2Dと小中規模3Dに取り組みやすい"],
    ["AAA規模toolingとcommercial supportはUnity/Unrealより小さい", "engine major version migration", "console exportは第三者支援が必要"],
    ["indie 2D/3D", "open-source要件", "engine改造を行う"],
    ["最先端AAA productionを即利用", "特定console向け公式end-to-end supportが必須"],
    ["unity", "unreal-engine", "bevy"],
    governance="Godot Foundation / community", license_name="MIT",
    source_urls=[("https://godotengine.org/article/godot-history-images/", "Godot history"), ("https://docs.godotengine.org/en/stable/getting_started/introduction/key_concepts_overview.html", "Godot key concepts")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("godot", "scene-tree", "implements", "sceneをnode treeとして構成し、scene自体を再利用可能にする。", grade="A", state="verified", source_url="https://docs.godotengine.org/en/stable/getting_started/introduction/key_concepts_overview.html", target_kind="idea")

add(
    "bevy", "Bevy", "Rust", "game-engine", ["game", "simulation"], "bevyengine/bevy", "https://bevyengine.org/",
    "Rustでdata-driven ECS、parallel scheduling、modular plugins、modern rendererを構築するopen-source game engine。",
    ["Rustの安全性と並列性をgame engineへ活かす", "engine機能をECS dataとsystemとして合成する"],
    "既存engineのobject hierarchyやmonolithic architectureに対し、RustとECSを最初から中心に据えたcommunity projectとして開始した。",
    ["Entity Component System", "Data-oriented design", "Parallel schedule", "Plugin architecture", "Rust-first"],
    ["ECS", "Rendering", "Assets", "Input", "Audio", "Scenes", "Hot reload ecosystem"],
    ["並列化しやすいdata model", "modularでsourceを追いやすい", "Rust safety"],
    ["editorとproduction workflowが成熟途中", "API変化が速い", "ECS思考とRust学習が必要"],
    ["Rust game/simulation", "data-oriented design", "engine内部も理解・変更したい"],
    ["完成度の高いvisual editorが必須", "stable APIを長期固定"],
    ["godot", "fyrox", "macroquad"],
    governance="Bevy Foundation / community", license_name="MIT/Apache-2.0",
    source_urls=[("https://bevyengine.org/learn/quick-start/getting-started/ecs/", "Bevy ECS"), ("https://bevyengine.org/news/introducing-bevy/", "Introducing Bevy")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("bevy", "entity-component-system", "implements", "entity、component data、system queryをengine全体の中核にする。", grade="A", state="verified", source_url="https://bevyengine.org/learn/quick-start/getting-started/ecs/", target_kind="idea")

add(
    "phaser", "Phaser", "TypeScript", "game-framework", ["game", "web-frontend", "2d"], "phaserjs/phaser", "https://phaser.io/",
    "Canvas/WebGL renderer、scene、input、physics、asset loadingを統合したHTML5 2D game framework。",
    ["browserで2D gameを迅速に構築する", "Web APIとgame loop周辺の定型処理を統合する"],
    "HTML5 game開発向けに、desktop/mobile browserを跨ぐ実用的な2D frameworkとしてRichard Daveyが開発した。",
    ["Scene lifecycle", "Game loop", "WebGL/Canvas abstraction", "Arcade physics", "Asset pipeline"],
    ["Rendering", "Input", "Physics", "Audio", "Tilemaps", "Tweens", "Plugins"],
    ["browser配布が簡単", "2D機能が統合", "JavaScript/TypeScript ecosystem"],
    ["native mobile/consoleはwrapperや別手段が必要", "大規模3Dには不向き", "browser性能差"],
    ["2D browser game", "教育game", "短期間prototype"],
    ["AAA 3D", "native console中心"],
    ["pixijs", "babylonjs", "love2d"],
    governance="Phaser Studio", license_name="MIT",
    source_urls=[("https://docs.phaser.io/phaser/getting-started/what-is-phaser", "What is Phaser"), ("https://github.com/phaserjs/phaser", "Phaser repository")],
    origin_evidence="supported", lineage_evidence="partial",
)
relation("phaser", "game-loop", "implements", "browser animation frame上でupdate/render lifecycleを管理する。", grade="A", state="verified", source_url="https://docs.phaser.io/phaser/concepts/game", target_kind="idea")

# ---------------------------------------------------------------------------
# Deep profiles: data, machine learning, and AI/agent frameworks
# ---------------------------------------------------------------------------
add(
    "tensorflow", "TensorFlow", "C++", "ml-framework", ["machine-learning", "deep-learning", "distributed-computing"], "tensorflow/tensorflow", "https://www.tensorflow.org/",
    "tensor計算、automatic differentiation、model training、distributed execution、deploymentを統合するmachine learning framework。",
    ["大規模neural networkを複数device/hostでtrainingする", "research modelをmobile、browser、serverへdeploymentする"],
    "Google内部のDistBelief経験を基に、より一般的なdataflow graphとopen-source ecosystemとして2015年に公開された。",
    ["Tensor dataflow", "Automatic differentiation", "Graph/eager execution", "Distributed strategies", "Multi-target deployment"],
    ["Keras integration", "tf.data", "Distributed training", "TensorBoard", "Serving/Lite/JS ecosystem"],
    ["trainingからdeploymentまで広い", "production toolingが成熟", "多様なhardware/backend"],
    ["API世代と抽象化が多い", "debugとperformance tuningが複雑", "research communityの一部はPyTorch中心"],
    ["production ML platform", "mobile/edge deployment", "大規模distributed training"],
    ["小さなclassical MLだけ", "最小限のarray autodiffを求める"],
    ["pytorch", "jax", "keras", "scikit-learn"],
    governance="Google / community", license_name="Apache-2.0",
    source_urls=[("https://www.tensorflow.org/about", "About TensorFlow"), ("https://research.google/pubs/tensorflow-large-scale-machine-learning-on-heterogeneous-distributed-systems/", "TensorFlow paper")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("tensorflow", "distbelief", "successor-of", "Google内部DistBeliefの経験を一般化したdataflow ML systemとして設計された。", grade="A", state="verified", source_url="https://research.google/pubs/tensorflow-large-scale-machine-learning-on-heterogeneous-distributed-systems/", target_kind="idea")
relation("tensorflow", "dataflow-graph", "implements", "operationとtensorをgraphとして配置・実行する設計を中核に持つ。", grade="A", state="verified", source_url="https://research.google/pubs/tensorflow-large-scale-machine-learning-on-heterogeneous-distributed-systems/", target_kind="idea")

add(
    "pytorch", "PyTorch", "Python", "ml-framework", ["machine-learning", "deep-learning", "distributed-computing"], "pytorch/pytorch", "https://pytorch.org/",
    "Python-firstのtensor、automatic differentiation、neural network module、distributed training、compilerを提供するmachine learning framework。",
    ["research codeを自然なPython制御フローで記述する", "prototypeからproductionへ同じmodel abstractionを拡張する"],
    "Torch/Lua系譜とChainerが広めたdefine-by-run型dynamic graphの流れを受け、Facebook AI ResearchがPython中心に開発した。",
    ["Eager execution", "Dynamic autograd", "Python-first modules", "Accelerator dispatch", "Compiler stack"],
    ["Tensors/autograd", "nn modules", "DistributedDataParallel", "torch.compile", "Export", "Ecosystem libraries"],
    ["debugしやすいPython execution", "research ecosystemが大きい", "distributedとcompilerが統合"],
    ["deployment選択肢が複数で複雑", "Python overheadやgraph breakの理解", "version間のcompiler behavior変化"],
    ["deep learning researchとproduction", "custom model/control flow", "GPU distributed training"],
    ["classical MLのみ", "非常に小さなembedded runtimeだけ"],
    ["tensorflow", "jax", "mxnet"],
    governance="Linux Foundation / PyTorch Foundation", license_name="BSD-style",
    source_urls=[("https://pytorch.org/features/", "PyTorch features"), ("https://pytorch.org/blog/pytorch-1.0/", "PyTorch 1.0")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("pytorch", "torch7", "successor-of", "LuaベースTorchのtensor/neural network系譜をPython中心に発展させた。", grade="B", state="supported", target_kind="idea")
relation("pytorch", "define-by-run", "implements", "実行したPython操作からautograd graphを構築する。", grade="A", state="verified", source_url="https://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html", target_kind="idea")
relation("pytorch", "chainer", "inspired-by", "dynamic define-by-runの先行例として影響が広く認識されるが、明示一次資料を追加する。", grade="C", state="hypothesis", target_kind="idea")

add(
    "jax", "JAX", "Python", "ml-framework", ["machine-learning", "scientific-computing"], "jax-ml/jax", "https://docs.jax.dev/",
    "NumPy風APIにautomatic differentiation、vectorization、parallelization、XLA compilationを関数変換として組み合わせるarray computing framework。",
    ["数値Python codeを大きく変えずに微分・batch・compileする", "accelerator上のfunctional numerical programを合成可能にする"],
    "Google ResearchでAutogradの思想とXLA compilerを結び付け、NumPy programへのcomposable transformationsとして発展した。",
    ["Function transformations", "Pure functional style", "JIT/XLA", "Automatic vectorization", "PyTree data structures"],
    ["grad", "jit", "vmap", "pmap/sharding", "NumPy API", "custom derivatives"],
    ["変換を合成できる", "研究用数値codeが簡潔", "accelerator compilerを活用"],
    ["pure function、static shape、tracingの制約", "高level model/training機能は別library", "compile latencyとrecompilation管理"],
    ["custom ML research", "scientific differentiable programming", "functional modelを好む"],
    ["batteries-included training platform", "dynamic side effect中心code"],
    ["pytorch", "tensorflow", "numpy"],
    governance="Google / community", license_name="Apache-2.0",
    source_urls=[("https://docs.jax.dev/en/latest/quickstart.html", "JAX quickstart"), ("https://github.com/jax-ml/jax", "JAX repository")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("jax", "autograd", "successor-of", "Autogradのautomatic differentiationを一般化しcompiler/vectorization変換と統合した。", grade="B", state="supported", target_kind="idea")
relation("jax", "numpy", "inspired-by", "NumPy-compatibleなarray APIをprogramming surfaceにする。", grade="A", state="verified", source_url="https://docs.jax.dev/en/latest/quickstart.html", target_kind="idea")
relation("jax", "xla", "built-on", "JIT compilationとaccelerator executionにXLAを利用する。", grade="A", state="verified", source_url="https://docs.jax.dev/en/latest/jit-compilation.html", target_kind="idea")

add(
    "scikit-learn", "scikit-learn", "Python", "ml-framework", ["machine-learning", "data-science"], "scikit-learn/scikit-learn", "https://scikit-learn.org/",
    "統一したestimator APIでclassical machine learning、preprocessing、model selection、pipeline、metricsを提供するPython library/framework。",
    ["多様なML algorithmを同じfit/predict interfaceで比較する", "前処理から評価まで再現可能なpipelineにする"],
    "SciPy ecosystemのGoogle Summer of Code projectから始まり、NumPy/SciPy上の実用的なclassical ML APIへ発展した。",
    ["Estimator protocol", "Fit/predict/transform", "Pipelines", "Composition", "Consistent model selection"],
    ["Classification/regression", "Clustering", "Preprocessing", "Pipelines", "Cross-validation", "Metrics"],
    ["APIが一貫しalgorithm比較が容易", "documentationとexamplesが成熟", "NumPy ecosystemと統合"],
    ["deep learningは対象外", "out-of-core/distributedは限定", "巨大dataには別engineが必要"],
    ["tabular/classical ML", "baseline比較", "reproducible preprocessing pipeline"],
    ["large-scale deep learning", "streaming distributed training"],
    ["xgboost", "lightgbm", "pytorch", "tensorflow"],
    governance="Community / NumFOCUS affiliated", license_name="BSD-3-Clause",
    source_urls=[("https://scikit-learn.org/stable/about.html", "About scikit-learn"), ("https://scikit-learn.org/stable/getting_started.html", "Getting started")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("scikit-learn", "scipy", "built-on", "NumPy/SciPy scientific Python stack上でalgorithmsを実装する。", grade="A", state="verified", source_url="https://scikit-learn.org/stable/about.html", target_kind="idea")
relation("scikit-learn", "estimator-protocol", "implements", "fit/predict/transformの共通契約でalgorithmを合成する。", grade="A", state="verified", source_url="https://scikit-learn.org/stable/developers/develop.html", target_kind="idea")

add(
    "apache-spark", "Apache Spark", "Scala", "data-framework", ["distributed-computing", "data-engineering", "machine-learning"], "apache/spark", "https://spark.apache.org/",
    "cluster上でbatch、SQL、streaming、machine learning、graph処理を統一engineで実行するdistributed data framework。",
    ["MapReduceの反復処理とinteractive queryの遅さを改善する", "同じdata abstractionで複数analytics workloadを扱う"],
    "UC Berkeley AMPLabで、disk中心MapReduceに対しmemoryを活用したresilient distributed datasetsとして研究・開発された。",
    ["RDD lineage", "Lazy transformations", "DAG scheduling", "In-memory computing", "Unified analytics"],
    ["Spark SQL", "Structured Streaming", "MLlib", "GraphX", "Python/R/Java APIs"],
    ["batchとstreamingを統合", "ecosystemと運用知識が豊富", "大規模dataに適する"],
    ["cluster運用とtuningが複雑", "small dataではoverhead", "shuffle、skew、memory管理の理解が必要"],
    ["large-scale ETL", "lakehouse analytics", "batch/streaming共通platform"],
    ["単一machineの小data", "millisecond event processingのみ"],
    ["apache-flink", "dask", "ray", "apache-beam"],
    governance="Apache Software Foundation", license_name="Apache-2.0",
    source_urls=[("https://spark.apache.org/research.html", "Spark research"), ("https://spark.apache.org/docs/latest/", "Spark documentation")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("apache-spark", "mapreduce", "reaction-against", "反復・interactive workloadでdisk materializationが多いMapReduceの制約を改善した。", grade="A", state="verified", source_url="https://spark.apache.org/research.html", target_kind="idea")
relation("apache-spark", "rdd", "implements", "lineageで再計算可能なimmutable distributed collectionを中核にした。", grade="A", state="verified", source_url="https://spark.apache.org/research.html", target_kind="idea")

add(
    "apache-flink", "Apache Flink", "Java", "data-framework", ["stream-processing", "distributed-computing", "data-engineering"], "apache/flink", "https://flink.apache.org/",
    "event-time、stateful computation、checkpointを中心に、streamを第一級としてbatchも扱うdistributed processing framework。",
    ["低latencyで正確なstateful stream processingを行う", "障害時もstateとprocessing semanticsを回復する"],
    "欧州のStratosphere research projectから発展し、batch engineからstream-first unified processorへ進化した。",
    ["Stream-first", "Event time", "Stateful operators", "Distributed snapshots", "Exactly-once state consistency"],
    ["DataStream", "Table/SQL", "CEP", "State backends", "Checkpoint/savepoint", "Connectors"],
    ["複雑なevent-time処理に強い", "大規模stateと復旧", "stream/batch統合"],
    ["運用とstate tuningが高度", "job graphとwatermark理解が必要", "simple ETLにはoverhead"],
    ["real-time analytics", "fraud detection", "stateful event processing"],
    ["small periodic batchだけ", "broker consumerだけで十分"],
    ["apache-spark", "kafka-streams", "apache-beam"],
    governance="Apache Software Foundation", license_name="Apache-2.0",
    source_urls=[("https://flink.apache.org/what-is-flink/flink-architecture/", "Flink architecture"), ("https://flink.apache.org/what-is-flink/flink-applications/", "Flink applications")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("apache-flink", "stratosphere", "successor-of", "Stratosphere research systemからApache projectへ発展した。", grade="B", state="supported", target_kind="idea")
relation("apache-flink", "chandy-lamport-snapshot", "inspired-by", "distributed checkpointはconsistent snapshot algorithmの系譜を実用化する。", grade="B", state="supported", target_kind="idea")

add(
    "ray", "Ray", "Python", "distributed-framework", ["distributed-computing", "machine-learning", "ai"], "ray-project/ray", "https://www.ray.io/",
    "taskとactor abstractionでPython/AI workloadをclusterへ拡張し、training、tuning、serving、data処理を統合するdistributed computing framework。",
    ["Python codeを大規模clusterへ低摩擦で拡張する", "AI applicationのheterogeneous task、actor、resource schedulingを統一する"],
    "UC Berkeley RISELabでreinforcement learning workloadのdistributed systems要件から生まれ、general-purpose Python distributed runtimeへ拡張した。",
    ["Remote tasks", "Stateful actors", "Dynamic task graphs", "Distributed object store", "Resource-aware scheduling"],
    ["Core tasks/actors", "Ray Data", "Train", "Tune", "Serve", "RLlib"],
    ["Pythonから段階的にscale-out", "AI workload向けlibraryが統合", "動的task graphに強い"],
    ["cluster object lifecycleとmemoryが複雑", "small workloadにはoverhead", "distributed failure semanticsを理解する必要"],
    ["distributed Python/AI", "hyperparameter tuning", "model servingとtraining共通platform"],
    ["SQL中心ETLのみ", "単純queue workerで十分"],
    ["apache-spark", "dask", "celery"],
    governance="Anyscale / community", license_name="Apache-2.0",
    source_urls=[("https://docs.ray.io/en/latest/ray-overview/index.html", "Ray overview"), ("https://www.usenix.org/conference/osdi18/presentation/moritz", "Ray OSDI paper", "primary-paper")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("ray", "actor-model", "implements", "stateful distributed workerをactor abstractionで表現する。", grade="A", state="verified", source_url="https://docs.ray.io/en/latest/ray-core/actors.html", target_kind="idea")
relation("ray", "dynamic-task-graph", "implements", "runtimeでtask依存を生成できる分散execution modelを採用する。", grade="A", state="verified", source_url="https://www.usenix.org/conference/osdi18/presentation/moritz", target_kind="idea")

add(
    "langchain", "LangChain", "Python", "agent-framework", ["llm-agent", "retrieval", "ai-application"], "langchain-ai/langchain", "https://python.langchain.com/",
    "LLM、prompt、retriever、tool、structured output、agent loop、observability integrationを組み合わせるAI application framework。",
    ["model vendorごとの差を吸収しapplication componentを組み合わせる", "LLMを外部dataとtoolへ接続する定型処理を減らす"],
    "LLM application patternが急速に変化した時期に、chain compositionとintegration catalogを中心として登場し、後にrunnable、agent、LangGraphとの分業へ発展した。",
    ["Composable runnables", "Provider abstraction", "Tool calling", "Retrieval augmentation", "Ecosystem integrations"],
    ["Model interfaces", "Prompt/output parsers", "Retrievers", "Tools", "Agents", "Tracing integration"],
    ["integrationが非常に多い", "prototypeを早く組める", "共通interfaceでproviderを交換しやすい"],
    ["抽象化とAPI変化が多い", "単純処理でもlayerが増える", "provider固有機能が隠れる場合"],
    ["複数provider/toolを組み合わせる", "RAG prototype", "LangGraph/LangSmith ecosystemを使う"],
    ["単一API callだけ", "完全に明示的な独自orchestrationを好む"],
    ["llamaindex", "semantic-kernel", "pydantic-ai", "openai-agents-sdk"],
    governance="LangChain Inc. / community", license_name="MIT",
    source_urls=[("https://python.langchain.com/docs/introduction/", "LangChain introduction"), ("https://github.com/langchain-ai/langchain", "LangChain repository")],
    origin_evidence="supported", lineage_evidence="partial",
)
relation("langchain", "chain-of-components", "implements", "model、prompt、retriever、toolを共通runnableとして合成する。", grade="A", state="verified", source_url="https://python.langchain.com/docs/concepts/lcel/", target_kind="idea")

add(
    "llamaindex", "LlamaIndex", "Python", "ai-data-framework", ["llm-agent", "retrieval", "ai-application"], "run-llama/llama_index", "https://www.llamaindex.ai/",
    "private/enterprise dataをLLM applicationへ接続するためのingestion、index、retrieval、query、agent workflow framework。",
    ["unstructured/structured dataをLLMが利用可能なcontextへ変換する", "RAG pipelineのdata lifecycleを標準化する"],
    "GPT Indexとして、外部dataをLLM promptへ効率的に供給するindex abstractionから始まり、RAGとagentic data frameworkへ拡大した。",
    ["Data connectors", "Nodes/indexes", "Retrievers", "Query engines", "Agent workflows"],
    ["Ingestion pipeline", "Vector/graph indexes", "Retrieval", "Evaluation", "Agents", "Provider integrations"],
    ["data/RAG機能が深い", "多数のconnector", "prototypeからcustom retrievalへ拡張"],
    ["abstractionが多く挙動追跡が必要", "version changeが速い", "simple embedding searchには過剰"],
    ["RAG、document intelligence、data agents", "多様なdata source"],
    ["tool orchestrationだけ", "単純なsingle prompt"],
    ["langchain", "haystack", "semantic-kernel"],
    aliases=["GPT Index"], governance="LlamaIndex / community", license_name="MIT",
    source_urls=[("https://docs.llamaindex.ai/en/stable/getting_started/concepts/", "LlamaIndex concepts"), ("https://github.com/run-llama/llama_index", "LlamaIndex repository")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("llamaindex", "gpt-index", "successor-of", "初期名称GPT Indexからdata frameworkへ改名・拡張した。", grade="A", state="verified", source_url="https://github.com/run-llama/llama_index", target_kind="idea")
relation("llamaindex", "retrieval-augmented-generation", "implements", "ingestion/index/retrievalを通じてLLMへexternal contextを与える。", grade="A", state="verified", source_url="https://docs.llamaindex.ai/en/stable/getting_started/concepts/", target_kind="idea")

add(
    "langgraph", "LangGraph", "Python", "agent-framework", ["llm-agent", "workflow", "ai-application"], "langchain-ai/langgraph", "https://langchain-ai.github.io/langgraph/",
    "stateful graph、checkpoint、interrupt、human-in-the-loopを使って長時間実行するagent workflowを制御するframework。",
    ["LLM agent loopを明示的なstate machine/graphとして管理する", "中断・再開・監査・人間承認を組み込む"],
    "LangChainのagent abstractionで複雑な制御flowとpersistent stateを扱う必要から、graph-based orchestrationとして分離された。",
    ["State graph", "Durable execution", "Checkpointing", "Interrupt/resume", "Human-in-the-loop"],
    ["Graph API", "Persistence", "Streaming", "Subgraphs", "Memory", "Prebuilt agents"],
    ["制御flowが明示的", "長時間・stateful agentに適する", "failure recoveryとhuman approvalを設計可能"],
    ["単純chainには複雑", "state schemaとidempotency設計が必要", "LangChain ecosystem変化への追随"],
    ["multi-step agent", "approval workflow", "durable AI process"],
    ["stateless single request", "一般workflow engineだけで十分"],
    ["semantic-kernel", "autogen", "temporal"],
    governance="LangChain Inc. / community", license_name="MIT",
    source_urls=[("https://langchain-ai.github.io/langgraph/concepts/why-langgraph/", "Why LangGraph"), ("https://github.com/langchain-ai/langgraph", "LangGraph repository")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("langgraph", "langchain", "extracted-from", "LangChain ecosystemからstateful agent orchestrationを独立frameworkとして発展させた。", grade="A", state="verified", source_url="https://langchain-ai.github.io/langgraph/concepts/why-langgraph/")
relation("langgraph", "state-machine", "implements", "node、edge、shared stateでagent flowをgraphとして定義する。", grade="A", state="verified", source_url="https://langchain-ai.github.io/langgraph/concepts/low_level/", target_kind="idea")

add(
    "semantic-kernel", "Semantic Kernel", "C#", "agent-framework", ["llm-agent", "ai-application"], "microsoft/semantic-kernel", "https://learn.microsoft.com/semantic-kernel/",
    "model service、plugin/function、prompt、memory、agent、process orchestrationを.NET/Python/Java applicationへ統合するSDK。",
    ["既存enterprise codeとAI model/tool callingを接続する", "model providerを交換しつつfunction orchestrationを構造化する"],
    "MicrosoftがCopilot patternを一般application向けSDKとして抽出し、native codeとsemantic functionをkernelが調停するmodelで開始した。",
    ["Kernel as orchestrator", "Plugins/functions", "Dependency injection integration", "Prompt templates", "Agent/process abstractions"],
    ["Connectors", "Function calling", "Plugins", "Agents", "Memory integrations", "Process framework"],
    [".NET enterpriseとの統合", "provider abstraction", "typed native functionをtoolとして公開しやすい"],
    ["複数言語版で機能差がある", "抽象化変更が速い", "小さなmodel callには過剰"],
    ["Microsoft/.NET中心AI app", "既存serviceをplugin化", "複数provider利用"],
    ["単一vendor SDKだけで十分", "frameworkに依存しない独自loop"],
    ["langchain", "openai-agents-sdk", "autogen"],
    governance="Microsoft / community", license_name="MIT",
    source_urls=[("https://learn.microsoft.com/semantic-kernel/overview/", "Semantic Kernel overview"), ("https://github.com/microsoft/semantic-kernel", "Semantic Kernel repository")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("semantic-kernel", "copilot-pattern", "extracted-from", "Copilot型applicationでmodelとnative capabilityを結合するpatternをSDK化した。", grade="B", state="supported", target_kind="idea")

add(
    "autogen", "Microsoft AutoGen", "Python", "agent-framework", ["llm-agent", "multi-agent", "ai-application"], "microsoft/autogen", "https://microsoft.github.io/autogen/",
    "message-driven agent、tool、model client、team、runtimeを使ってsingle/multi-agent systemを構築するframework。",
    ["複数agentの協調会話とtool executionを構造化する", "agent experimentからevent-driven applicationへ拡張する"],
    "Microsoft Researchのmulti-agent conversation研究・実装から始まり、core runtime、AgentChat、extensionを分離したarchitectureへ再設計された。",
    ["Message-driven agents", "Agent runtime", "Conversation teams", "Extensible model clients", "Distributed runtime direction"],
    ["Core API", "AgentChat", "Tools", "Teams", "Model clients", "Extensions"],
    ["multi-agent patternを試しやすい", "runtimeとhigh-level APIを分離", "research examplesが豊富"],
    ["multi-agentが必ずしも品質・cost改善にならない", "terminationとloop safetyが必要", "API世代移行を確認する必要"],
    ["multi-agent research", "role-based tool workflows", "event-driven agent runtime"],
    ["決定的workflowが中心", "single model callだけ"],
    ["langgraph", "crewai", "semantic-kernel"],
    governance="Microsoft / community", license_name="MIT/CC-BY docs mix",
    source_urls=[("https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/intro.html", "AutoGen design patterns"), ("https://github.com/microsoft/autogen", "AutoGen repository")],
    origin_evidence="supported", lineage_evidence="partial",
)
relation("autogen", "actor-model", "inspired-by", "message-driven agent runtimeはactor-style設計と共通するが、明示された系譜を追加検証する。", grade="D", state="hypothesis", target_kind="idea")

add(
    "openai-agents-sdk", "OpenAI Agents SDK", "Python", "agent-framework", ["llm-agent", "ai-application"], "openai/openai-agents-python", "https://openai.github.io/openai-agents-python/",
    "agent、handoff、guardrail、session、tool、tracingを少数のprimitiveで構築するagent application SDK。",
    ["agent loopとtool callingの定型処理を小さなAPIで提供する", "handoffとguardrailとtraceを同じexecution modelに統合する"],
    "OpenAI Swarm experimentの後継として、production-orientedなagent loopとobservabilityを提供するSDKとして公開された。",
    ["Small primitive set", "Agent loop", "Handoffs", "Guardrails", "Built-in tracing"],
    ["Agents", "Function tools", "Handoffs", "Sessions", "Guardrails", "Tracing"],
    ["API surfaceが比較的小さい", "OpenAI model/tool ecosystemと直接統合", "traceとguardrailが標準"],
    ["OpenAI-oriented defaultを評価する必要", "複雑durable workflowは別基盤が必要", "agent loopのcost/safety設計は利用側責任"],
    ["OpenAI中心agent app", "handoffとtool calling", "明示的で小さなframeworkを求める"],
    ["provider-neutralityを最優先", "長時間durable business workflow"],
    ["langchain", "semantic-kernel", "pydantic-ai"],
    aliases=["Agents SDK"], governance="OpenAI / community", license_name="MIT",
    source_urls=[("https://openai.github.io/openai-agents-python/", "OpenAI Agents SDK documentation"), ("https://github.com/openai/openai-agents-python", "OpenAI Agents SDK repository")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("openai-agents-sdk", "openai-swarm", "successor-of", "experimental Swarmからproduction-oriented SDKへ発展した。", grade="A", state="verified", source_url="https://github.com/openai/openai-agents-python", target_kind="idea")

# ---------------------------------------------------------------------------
# Deep profiles: testing and browser automation
# ---------------------------------------------------------------------------
add(
    "junit", "JUnit", "Java", "test-framework", ["testing", "jvm"], "junit-team/junit5", "https://junit.org/junit5/",
    "Java/JVM testのdiscovery、lifecycle、assertion integration、extension、engine実行を標準化したxUnit系test framework。",
    ["repeatableなunit testを簡潔に記述・自動実行する", "IDE/build tool/test engine間の共通契約を提供する"],
    "Kent BeckとErich GammaがSmalltalkのSUnit/xUnit patternをJavaへ移植したJUnitから始まり、JUnit 5でPlatform/Jupiter/Vintageへ再設計された。",
    ["xUnit lifecycle", "Annotations", "Test discovery", "Extension model", "Launcher/engine separation"],
    ["Jupiter API", "Parameterized tests", "Extensions", "Platform launcher", "Dynamic tests"],
    ["JVM ecosystemの事実上標準", "IDE/build tool統合", "extensionとparameterized testingが成熟"],
    ["大量integration testでは並列・resource管理が必要", "assertion/mockingは別libraryが多い", "annotation lifecycleを誤解しやすい"],
    ["Java/Kotlin unit/integration test", "tooling interoperability", "custom extension"],
    ["non-JVM project", "property-based testだけを独立利用"],
    ["testng", "spock", "kotest"],
    governance="JUnit team / community", license_name="EPL-2.0",
    source_urls=[("https://junit.org/junit5/docs/current/user-guide/", "JUnit user guide"), ("https://junit.org/junit4/faq.html", "JUnit history FAQ")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("junit", "sunit", "inspired-by", "Smalltalk SUnitのxUnit lifecycleをJavaへ移植した。", grade="A", state="verified", source_url="https://junit.org/junit4/faq.html", target_kind="idea")
relation("junit", "xunit", "implements", "setup/test/teardownとtest case/suite/runnerのxUnit familyに属する。", grade="A", state="verified", source_url="https://junit.org/junit4/faq.html", target_kind="idea")

add(
    "pytest", "pytest", "Python", "test-framework", ["testing", "python"], "pytest-dev/pytest", "https://pytest.org/",
    "plain assert、fixture dependency graph、plugin、parameterization、test discoveryを中心とするPython test framework。",
    ["boilerplateの少ないtestを記述する", "reusable fixtureとpluginでunitからintegrationまで構成する"],
    "py.testとしてHolger Krekelらが開発し、Pythonicなassert introspectionとfixture modelでunittest class中心の形式を補完した。",
    ["Plain assert rewriting", "Fixture injection", "Plugin hooks", "Parametrization", "Convention-based discovery"],
    ["Fixtures", "Markers", "Parametrize", "Capture", "Plugins", "Rich failure output"],
    ["testが短く読みやすい", "fixture compositionが強力", "plugin ecosystemが大きい"],
    ["fixture依存が深いと見えにくい", "scope/autouse誤用で隠れた状態", "大量pluginで互換性管理が必要"],
    ["Python unit/integration test", "data-driven test", "custom test tooling"],
    ["標準libraryだけを厳密に使う", "fixture injectionを避けたい"],
    ["unittest", "nose2", "robot-framework"],
    governance="pytest-dev / community", license_name="MIT",
    source_urls=[("https://docs.pytest.org/en/stable/explanation/anatomy.html", "Anatomy of a test"), ("https://docs.pytest.org/en/stable/about.html", "About pytest")],
    origin_evidence="supported", lineage_evidence="partial",
)
relation("pytest", "xunit", "implements", "setup/teardown styleを支援しつつfixture injectionへ拡張する。", grade="A", state="verified", source_url="https://docs.pytest.org/en/stable/how-to/xunit_setup.html", target_kind="idea")
relation("pytest", "fixture-dependency-injection", "implements", "test function引数からfixture graphを解決する。", grade="A", state="verified", source_url="https://docs.pytest.org/en/stable/how-to/fixtures.html", target_kind="idea")

add(
    "jest", "Jest", "TypeScript", "test-framework", ["testing", "javascript"], "jestjs/jest", "https://jestjs.io/",
    "test runner、assertion、mock、snapshot、coverageを統合し、JavaScript/TypeScript application testをzero-config志向で実行するframework。",
    ["JavaScript projectのtest tool選定と設定を減らす", "isolated workerとmock/snapshotを統一する"],
    "FacebookでJavaScript application testing向けに開発され、初期はJasmineを基盤にしつつ独自runner、mock、snapshotへ発展した。",
    ["Integrated test platform", "Worker isolation", "Snapshot testing", "Module mocking", "Watch mode"],
    ["Runner", "Expect assertions", "Mocks", "Snapshots", "Coverage", "Timers"],
    ["一般的機能が一体化", "React ecosystemの実績", "watchとfailure output"],
    ["transform/ESM設定が複雑になり得る", "大規模suiteで起動・memory cost", "snapshot濫用で意図が弱くなる"],
    ["JavaScript/TypeScript unit test", "React component test", "integrated toolを求める"],
    ["browser-native E2Eだけ", "Vite-native速度を最優先"],
    ["vitest", "mocha", "jasmine"],
    governance="OpenJS Foundation / community", license_name="MIT",
    source_urls=[("https://jestjs.io/docs/getting-started", "Jest getting started"), ("https://github.com/jestjs/jest", "Jest repository")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("jest", "jasmine", "built-on", "初期JestはJasmine test frameworkを基盤としていた。", grade="B", state="supported")
relation("jest", "snapshot-testing", "popularized", "serialized outputをreview可能なsnapshotとして保存するtesting styleを広く普及させた。", grade="B", state="supported", target_kind="idea")

add(
    "playwright", "Playwright", "TypeScript", "browser-automation-framework", ["testing", "browser-automation", "e2e"], "microsoft/playwright", "https://playwright.dev/",
    "Chromium、Firefox、WebKitを統一APIで自動化し、auto-wait、isolated context、trace、test runnerを提供するbrowser testing framework。",
    ["modern browser間で信頼できるE2E testを行う", "timing依存のflaky testをauto-waitとactionability checkで減らす"],
    "Puppeteer開発経験を持つteamが、複数browser engineとtesting-specific機能を最初から重視してMicrosoftで開発した。",
    ["Cross-browser protocol control", "Auto-wait", "Browser contexts", "Web-first assertions", "Trace-based debugging"],
    ["Test runner", "Locators", "Network interception", "Emulation", "Parallelism", "Trace viewer"],
    ["複数engineを同じtestで確認", "待機とlocatorが堅牢", "trace/debug toolingが強い"],
    ["browser binary downloadが大きい", "E2E自体のcostとflakinessは残る", "実装detailに依存したtestは保守が重い"],
    ["critical user journey", "cross-browser regression", "browser automation"],
    ["unit testだけ", "実browser不要のDOM logic"],
    ["cypress", "selenium", "puppeteer"],
    governance="Microsoft / community", license_name="Apache-2.0",
    source_urls=[("https://playwright.dev/docs/why-playwright", "Why Playwright"), ("https://github.com/microsoft/playwright", "Playwright repository")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("playwright", "puppeteer", "successor-of", "Puppeteer系browser automation経験を複数engine・testing用途へ拡張した系譜だが、公式の表現を追加検証する。", grade="C", state="hypothesis")
relation("playwright", "auto-waiting", "implements", "action前にelement actionability条件を自動確認する。", grade="A", state="verified", source_url="https://playwright.dev/docs/actionability", target_kind="idea")

add(
    "cypress", "Cypress", "TypeScript", "browser-testing-framework", ["testing", "browser-automation", "e2e"], "cypress-io/cypress", "https://www.cypress.io/",
    "browser内近傍でapplicationを観察・制御し、time travel UI、automatic retry、network stubbingを統合するWeb testing framework。",
    ["Selenium型remote automationの待機・debug摩擦を減らす", "developerがtest実行を視覚的に理解できるようにする"],
    "従来E2E toolのflakinessとdebug難度への反応として、browserと密接に統合した独自architectureを採用した。",
    ["In-browser runner", "Automatic retry", "Time-travel snapshots", "Network control", "Developer-centric UI"],
    ["E2E/component testing", "Command queue", "Intercept", "Dashboard/cloud integration", "Screenshots/video"],
    ["interactive debugが分かりやすい", "retry semanticsで待機codeが減る", "frontend developer体験が良い"],
    ["command queueの非同期modelが独特", "multi-tab/multi-originには制約・設計差", "cloud機能とOSS範囲を確認する必要"],
    ["Web app E2E/component test", "debug体験を優先", "single-browser-flow中心"],
    ["複数browser contextを高度に制御", "general browser automation"],
    ["playwright", "selenium", "webdriverio"],
    governance="Cypress.io / community", license_name="MIT core / commercial services",
    source_urls=[("https://docs.cypress.io/app/core-concepts/trade-offs", "Cypress trade-offs"), ("https://docs.cypress.io/app/core-concepts/retry-ability", "Retry ability")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("cypress", "selenium", "reaction-against", "remote WebDriver型automationの同期・debug課題に対しbrowser近傍architectureを採用した。", grade="A", state="verified", source_url="https://docs.cypress.io/app/core-concepts/trade-offs")

add(
    "selenium", "Selenium", "Java", "browser-automation-framework", ["testing", "browser-automation", "e2e"], "SeleniumHQ/selenium", "https://www.selenium.dev/",
    "WebDriver標準を中心に複数browserと言語からuser操作を自動化する長寿命browser automation project。",
    ["browser vendorを跨いでWeb UIを外部から自動操作する", "testing gridで複数OS/browserを並列実行する"],
    "Jason HugginsのJavaScriptTestRunnerからSelenium Core/RC/WebDriverへ発展し、WebDriverはW3C標準となった。",
    ["WebDriver protocol", "Out-of-process automation", "Multi-language bindings", "Grid", "Browser-vendor drivers"],
    ["WebDriver", "Grid", "IDE", "Language bindings", "BiDi evolution"],
    ["言語とbrowserの対応が広い", "標準protocol", "enterprise gridの長い実績"],
    ["明示waitと環境管理が必要", "driver/browser組合せの問題", "debug体験は新世代toolより低level"],
    ["多言語enterprise automation", "remote/grid execution", "標準WebDriverが要件"],
    ["frontend developer向け一体型runnerを優先", "browser外不要"],
    ["playwright", "cypress", "webdriverio"],
    governance="Selenium project / Software Freedom Conservancy", license_name="Apache-2.0",
    source_urls=[("https://www.selenium.dev/documentation/overview/", "Selenium overview"), ("https://www.selenium.dev/history/", "Selenium history")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("selenium", "selenium-rc", "successor-of", "Core/RCからWebDriver統合へ発展した。", grade="A", state="verified", source_url="https://www.selenium.dev/history/", target_kind="idea")
relation("selenium", "w3c-webdriver", "implements", "browser automationのW3C WebDriver standardを実装する。", grade="A", state="verified", source_url="https://www.selenium.dev/documentation/webdriver/", target_kind="idea")

# ---------------------------------------------------------------------------
# Deep profiles: distributed systems and application infrastructure
# ---------------------------------------------------------------------------
add(
    "akka", "Akka", "Scala", "distributed-framework", ["distributed-computing", "concurrency", "microservices"], "akka/akka", "https://akka.io/",
    "actor、supervision、stream、cluster、persistenceを使ってJVM上にconcurrent/distributed applicationを構築するframework。",
    ["shared mutable stateとthread管理をmessage passingへ置き換える", "障害分離とlocation transparencyを分散applicationへ提供する"],
    "Erlang/OTPのactorとfault toleranceをJVM/Scalaへ持ち込み、reactive systems向けtoolkitとして発展した。",
    ["Actor model", "Supervision", "Message passing", "Location transparency", "Reactive Streams"],
    ["Actors", "Cluster", "Persistence", "Streams", "Distributed Data", "Typed APIs"],
    ["高並行state machineを表現しやすい", "supervisionとcluster機能", "JVM ecosystem"],
    ["message ordering、delivery、serializationが複雑", "debugが通常call stackと異なる", "license条件を用途ごとに確認"],
    ["stateful distributed service", "event-driven system", "actor modelを採用"],
    ["単純stateless HTTP", "licenseまたは運用complexityが許容できない"],
    ["orleans", "erlang-otp", "pekko"],
    governance="Lightbend / Akka", license_name="Business Source License / commercial terms",
    source_urls=[("https://doc.akka.io/docs/akka/current/typed/guide/actors-intro.html", "Akka actor introduction"), ("https://akka.io/about", "About Akka")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("akka", "erlang-otp", "inspired-by", "actor、supervision、let-it-crashの系譜をJVMへ適用した。", grade="B", state="supported", target_kind="idea")
relation("akka", "actor-model", "implements", "isolated actorがmessageを順次処理する。", grade="A", state="verified", source_url="https://doc.akka.io/docs/akka/current/typed/guide/actors-intro.html", target_kind="idea")

add(
    "orleans", "Microsoft Orleans", "C#", "distributed-framework", ["distributed-computing", "actor", "cloud-native"], "dotnet/orleans", "https://learn.microsoft.com/dotnet/orleans/",
    "identityを持つvirtual actor（grain）を必要時に自動activateし、location、lifecycle、distributionをruntimeが管理する.NET framework。",
    ["distributed stateful objectの配置・activation・failure recoveryをapplicationから隠す", "cloud serviceのscale-outをobject-oriented modelで扱う"],
    "Microsoft Researchでcloud programmingを簡単にするvirtual actor modelとして開発され、Haloなど実サービスで利用後open source化された。",
    ["Virtual actors", "Automatic activation", "Location transparency", "Single-threaded grain execution", "Cluster runtime"],
    ["Grains", "Silos", "Streams", "Persistence", "Timers/reminders", "Transactions"],
    ["actor lifecycleをruntimeが管理", "C# interfaceで分散objectを扱える", "stateful cloud service実績"],
    ["distributionを隠し過ぎるとnetwork costを誤解", "grain granularity設計が重要", "runtime/storage provider運用が必要"],
    ["game backend", "IoT/device twin", "stateful entity service"],
    ["stateless request only", "strict low-level placement controlが必要"],
    ["akka", "dapr-actors", "service-fabric-reliable-actors"],
    governance="Microsoft / .NET Foundation", license_name="MIT",
    source_urls=[("https://learn.microsoft.com/dotnet/orleans/overview", "Orleans overview"), ("https://www.microsoft.com/en-us/research/project/orleans-virtual-actors/", "Orleans research project")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("orleans", "virtual-actor-model", "implements", "actor identityとactivation/locationをruntimeが仮想化する。", grade="A", state="verified", source_url="https://www.microsoft.com/en-us/research/project/orleans-virtual-actors/", target_kind="idea")

add(
    "dapr", "Dapr", "Go", "distributed-framework", ["distributed-computing", "cloud-native", "microservices"], "dapr/dapr", "https://dapr.io/",
    "sidecarまたはprocessとしてservice invocation、state、pub/sub、bindings、secrets、workflowなどのdistributed building blocksを提供するruntime。",
    ["microserviceごとに同じdistributed systems codeを再実装するのを減らす", "languageとinfrastructureからapplication APIを分離する"],
    "Microsoftで開始され、cloud-native applicationの共通building blocksをportable APIとsidecar architectureで提供するopen-source projectとしてCNCFへ移管された。",
    ["Sidecar architecture", "Building-block APIs", "Pluggable components", "Language neutrality", "State abstraction"],
    ["Service invocation", "Pub/Sub", "State", "Bindings", "Secrets", "Actors", "Workflows"],
    ["言語を跨いで共通API", "infrastructure providerを交換しやすい", "cross-cutting reliabilityを外部化"],
    ["sidecar/network hopと運用componentが増える", "lowest-common-denominator化の可能性", "component semantics差を理解する必要"],
    ["polyglot microservices", "portable pubsub/state", "platform teamが共通runtimeを運用"],
    ["単一process monolith", "追加sidecarを許容できないlow-latency path"],
    ["service-mesh", "spring-cloud", "temporal"],
    governance="CNCF", license_name="Apache-2.0",
    source_urls=[("https://docs.dapr.io/concepts/overview/", "Dapr overview"), ("https://www.cncf.io/projects/dapr/", "CNCF Dapr")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("dapr", "sidecar-pattern", "implements", "application外processにdistributed building blocksを配置する。", grade="A", state="verified", source_url="https://docs.dapr.io/concepts/dapr-services/sidecar/", target_kind="idea")
relation("dapr", "distributed-building-blocks", "implements", "state、pubsub、invocation等を共通APIとして提供する。", grade="A", state="verified", source_url="https://docs.dapr.io/concepts/overview/", target_kind="idea")

add(
    "temporal", "Temporal", "Go", "workflow-framework", ["distributed-computing", "workflow", "reliability"], "temporalio/temporal", "https://temporal.io/",
    "application codeでdurable workflowを記述し、event history replayによってfailure後も長時間processを継続するplatform/framework。",
    ["service failureやretryを跨ぐbusiness processを確実に完了する", "queue、timer、state machineの接着codeを減らす"],
    "Uber Cadenceのoriginal teamが独立してTemporalを開始し、durable execution modelをmulti-language SDKとplatformへ発展させた。",
    ["Durable execution", "Event sourcing/replay", "Deterministic workflows", "Activities", "Built-in retries and timers"],
    ["Workflow SDKs", "Activities", "Signals/queries", "Schedules", "Visibility", "Worker versioning"],
    ["failure/retryをapplication modelへ統合", "長時間workflowをcodeで表現", "state persistenceを自動化"],
    ["determinism制約", "server clusterまたはcloud service運用", "history growthとversioning設計が必要"],
    ["order/payment/onboarding", "multi-service saga", "hours-to-years workflow"],
    ["短いstateless function", "強いSQL-centric BPM UIが必要"],
    ["cadence", "dapr-workflows", "camunda"],
    governance="Temporal Technologies / community", license_name="MIT server/SDKs with service terms",
    source_urls=[("https://docs.temporal.io/temporal", "Temporal overview"), ("https://temporal.io/blog/temporal-a-brief-history", "Temporal history")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("temporal", "cadence", "successor-of", "Cadenceを作ったteamがTemporalとしてfork/発展させた系譜。", grade="A", state="verified", source_url="https://temporal.io/blog/temporal-a-brief-history", target_kind="idea")
relation("temporal", "event-sourcing", "implements", "workflow event historyをreplayしてdurable stateを復元する。", grade="A", state="verified", source_url="https://docs.temporal.io/workflow-execution/event", target_kind="idea")

# ---------------------------------------------------------------------------
# Deep profiles: CLI/TUI, embedded, robotics, CSS, and CMS
# ---------------------------------------------------------------------------
add(
    "textual", "Textual", "Python", "tui-framework", ["cli-tui", "ui"], "Textualize/textual", "https://textual.textualize.io/",
    "Pythonでwidget、layout、CSS、event、reactive stateを使ってterminal applicationを構築するTUI application framework。",
    ["terminal UIのescape sequence、layout、input処理を高level componentへ抽象化する", "Web UIに近いmental modelをterminalへ提供する"],
    "Richのterminal rendering capabilitiesを基盤に、DOM/CSS風のapplication modelを持つ本格TUI frameworkとしてTextualizeが開発した。",
    ["Reactive state", "Message/event pump", "DOM-like widget tree", "Textual CSS", "Async application model"],
    ["Widgets", "Layouts", "CSS", "Input/events", "Workers", "Testing pilot", "Web delivery ecosystem"],
    ["視覚的TUIをPythonで構築", "layout/CSSとwidget ecosystem", "testingとasync support"],
    ["simple CLIには重い", "terminal差とperformanceを考慮", "Web CSSと同じではない独自概念"],
    ["dashboard、developer tool、terminal IDE", "keyboard-centric app"],
    ["一行CLI", "native desktop GUIが必要"],
    ["bubbletea", "urwid", "prompt-toolkit"],
    governance="Textualize / community", license_name="MIT",
    source_urls=[("https://textual.textualize.io/guide/architecture/", "Textual architecture"), ("https://github.com/Textualize/textual", "Textual repository")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("textual", "rich", "built-on", "Richのterminal renderingとstyle技術を基盤にapplication frameworkへ拡張した。", grade="A", state="verified", source_url="https://textual.textualize.io/guide/architecture/", target_kind="idea")
relation("textual", "dom-css-model", "inspired-by", "widget treeとCSS-like stylingにWeb DOM/CSSのmental modelを取り入れる。", grade="A", state="verified", source_url="https://textual.textualize.io/guide/CSS/", target_kind="idea")

add(
    "bubbletea", "Bubble Tea", "Go", "tui-framework", ["cli-tui", "ui"], "charmbracelet/bubbletea", "https://github.com/charmbracelet/bubbletea",
    "Elm Architectureに基づくModel、Update、View loopでGo terminal applicationを構築するTUI framework。",
    ["terminal input、state update、renderを予測可能なunidirectional loopへ整理する", "concurrent command resultをmessageとして扱う"],
    "CharmbraceletがElm ArchitectureをGo TUIへ適用し、小さなfunctional coreとcomposable componentsを中心に作った。",
    ["Elm Architecture", "Message loop", "Pure-ish update", "Commands", "Composable models"],
    ["Program runtime", "Messages", "Commands", "Alternate screen", "Mouse support", "Bubbles ecosystem"],
    ["state transitionが明確", "Go binaryとして配布しやすい", "component合成が単純"],
    ["complex layout/styleは追加libraryが必要", "functional update styleへの慣れ", "long-running I/Oはcommand設計が必要"],
    ["interactive Go CLI/TUI", "state machine的UI", "single binary distribution"],
    ["mouse-first rich desktop", "simple command only"],
    ["textual", "ratatui", "cursive"],
    governance="Charmbracelet / community", license_name="MIT",
    source_urls=[("https://github.com/charmbracelet/bubbletea", "Bubble Tea repository")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("bubbletea", "elm-architecture", "inspired-by", "Model/Update/Viewとmessage loopをElm Architectureから採用する。", grade="A", state="verified", source_url="https://github.com/charmbracelet/bubbletea", target_kind="idea")

add(
    "ros2", "ROS 2", "C++", "robotics-framework", ["robotics", "distributed-computing", "embedded"], "ros2/ros2", "https://docs.ros.org/en/rolling/",
    "robot process間通信、message/service/action、tooling、package、visualization、simulation integrationを提供するrobotics middleware/framework。",
    ["sensor、actuator、planning、controlを疎結合nodeへ分割する", "research prototypeからproduction/distributed robotへ対応する"],
    "ROS 1のsingle-master、security、real-time、production deployment上の制約を改善するため、DDSを通信基盤として再設計された。",
    ["Node graph", "Publish/subscribe", "Services/actions", "DDS QoS", "Package ecosystem"],
    ["Client libraries", "Launch", "Parameters", "Lifecycle nodes", "rosbag", "RViz/Gazebo integrations"],
    ["robotics component ecosystemが巨大", "language/process分離", "QoSとdistributed deployment"],
    ["DDS設定とnetwork debugが複雑", "version/distribution互換性", "hard real-timeはsystem全体設計が必要"],
    ["robot software integration", "research/industrial robotics", "sensor-actuator distributed system"],
    ["極小MCU単体", "一般Web serviceだけ"],
    ["ros1", "micro-ros", "yarp"],
    aliases=["Robot Operating System 2"], governance="Open Robotics / ROS community", license_name="Apache-2.0/BSD mix",
    source_urls=[("https://docs.ros.org/en/rolling/The-ROS2-Project/Contributing/Contact.html", "ROS 2 project"), ("https://design.ros2.org/articles/why_ros2.html", "Why ROS 2")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("ros2", "ros1", "successor-of", "ROS 1のproduction、security、real-time、multi-robot制約を解決する再設計。", grade="A", state="verified", source_url="https://design.ros2.org/articles/why_ros2.html", target_kind="idea")
relation("ros2", "dds", "built-on", "default communication abstractionにDDS/RTPS implementationsを利用する。", grade="A", state="verified", source_url="https://design.ros2.org/articles/ros_on_dds.html", target_kind="idea")

add(
    "zephyr", "Zephyr RTOS", "C", "embedded-framework", ["embedded", "rtos", "iot"], "zephyrproject-rtos/zephyr", "https://www.zephyrproject.org/",
    "小型MCUから多機能SoCまで、kernel、driver、network、Bluetooth、security、build/configを統合するopen-source RTOS ecosystem。",
    ["多vendor boardでportable embedded applicationを構築する", "kernelとdriver、protocol stack、configurationを一つのprojectで管理する"],
    "Wind RiverのRocket kernelを起点にLinux Foundation projectとして公開され、vendor-neutralなIoT RTOS ecosystemへ拡大した。",
    ["Configurable RTOS", "Device tree", "Kconfig", "West/meta-tool", "Vendor-neutral hardware abstraction"],
    ["Scheduler", "Drivers", "Networking", "Bluetooth", "Security", "File systems", "Testing"],
    ["board/SoC対応が広い", "modern buildとtesting", "foundation governance"],
    ["Kconfig/device tree/buildの学習量", "resource tuningが必要", "vendor SDKとの機能差"],
    ["connected MCU/IoT", "multi-board product family", "open RTOS stack"],
    ["Arduino-levelの単純prototypeだけ", "Linux class application"],
    ["freertos", "riot-os", "nuttx", "esp-idf"],
    governance="Linux Foundation", license_name="Apache-2.0",
    source_urls=[("https://docs.zephyrproject.org/latest/introduction/index.html", "Zephyr introduction"), ("https://www.zephyrproject.org/learn-about/", "About Zephyr")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("zephyr", "rocket-kernel", "successor-of", "Wind River Rocket kernelのcode contributionを起点として公開project化した。", grade="B", state="supported", target_kind="idea")

add(
    "esp-idf", "ESP-IDF", "C", "embedded-framework", ["embedded", "iot"], "espressif/esp-idf", "https://idf.espressif.com/",
    "Espressif SoC向けFreeRTOS、driver、Wi-Fi/Bluetooth、network、security、build、diagnosticsを統合するofficial development framework。",
    ["ESP32 familyのhardware機能とwireless stackを一貫して利用する", "prototypeからproduction firmwareまで同じSDKで管理する"],
    "EspressifがESP32 family向け公式SDKとして、FreeRTOSとchip-specific driver/toolchainを統合して開発している。",
    ["Vendor SDK", "FreeRTOS integration", "Component build system", "Hardware abstraction", "Wireless-first"],
    ["Wi-Fi/Bluetooth", "Drivers", "Networking", "OTA", "Secure boot/flash encryption", "Diagnostics"],
    ["chip機能への最短経路", "examplesとtoolingが豊富", "production security機能"],
    ["Espressif hardwareにlock-in", "version upgradeとcomponent互換性", "Arduinoより低levelで学習量が多い"],
    ["ESP32 production firmware", "Wi-Fi/BLE IoT", "hardware機能を細かく制御"],
    ["vendor-neutral firmware", "簡単なbeginner prototypeのみ"],
    ["arduino", "zephyr", "platformio"],
    governance="Espressif Systems", license_name="Apache-2.0 with component exceptions",
    source_urls=[("https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/index.html", "ESP-IDF get started"), ("https://github.com/espressif/esp-idf", "ESP-IDF repository")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("esp-idf", "freertos", "built-on", "task schedulingとRTOS servicesにEspressifのFreeRTOS integrationを利用する。", grade="A", state="verified", source_url="https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/freertos.html", target_kind="idea")

add(
    "arduino", "Arduino Core / Framework", "C++", "embedded-framework", ["embedded", "education", "iot"], "arduino/ArduinoCore-API", "https://www.arduino.cc/",
    "setup/loop、simple I/O API、board package、IDE/library ecosystemでmicrocontroller programmingの参入障壁を下げるframework。",
    ["electronics初心者がtoolchainとregisterを意識せずprototypeする", "boardごとの差を共通APIで吸収する"],
    "Interaction Design Institute Ivreaで教育・physical computing向けにWiring/Processing系譜から生まれ、open hardware/software ecosystemへ拡大した。",
    ["Simple setup/loop", "Hardware abstraction", "Sketch model", "Board cores", "Library ecosystem"],
    ["Digital/analog I/O", "Serial", "Timing", "Board manager", "Libraries", "IDE/CLI"],
    ["非常に始めやすい", "board/library ecosystemが巨大", "prototypeと教育に強い"],
    ["高度なRTOS/driver制御には抽象化が不足", "library品質差", "hidden global stateとblocking codeが大規模化で問題"],
    ["prototype、education、maker IoT", "短期間hardware experiment"],
    ["strict real-time/large production firmware", "certification-heavy system"],
    ["esp-idf", "zephyr", "platformio"],
    governance="Arduino / open-source community", license_name="LGPL/GPL mix",
    source_urls=[("https://docs.arduino.cc/learn/starting-guide/whats-arduino/", "What is Arduino"), ("https://www.arduino.cc/en/Guide/Introduction", "Arduino introduction")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("arduino", "wiring", "inspired-by", "Wiring language/frameworkとProcessingの教育的modelを継承した。", grade="B", state="supported", target_kind="idea")
relation("arduino", "processing", "inspired-by", "sketchとsetup/draw系のcreative coding experienceをphysical computingへ展開した。", grade="B", state="supported", target_kind="idea")

add(
    "bootstrap", "Bootstrap", "Sass", "css-framework", ["css-ui", "web-frontend"], "twbs/bootstrap", "https://getbootstrap.com/",
    "responsive grid、utility、styled component、JavaScript behaviorを統合したWeb UI/CSS framework。",
    ["Web applicationごとのUI/CSS再実装を減らす", "responsive layoutと共通componentを迅速に揃える"],
    "Twitter内部のtoolkitとしてMark OttoとJacob Thorntonが作り、Twitter Bootstrapとして公開後、Web UI frameworkの標準例となった。",
    ["Responsive grid", "Prebuilt components", "Utility classes", "Design tokens via Sass/CSS variables", "Progressive enhancement"],
    ["Grid", "Forms", "Navigation", "Modal/dropdown", "Utilities", "Theming"],
    ["短時間で整ったUI", "documentationとecosystemが大きい", "accessibility考慮component"],
    ["Bootstrapらしい見た目が出やすい", "unused CSS/JSを管理", "custom design systemではoverrideが増える"],
    ["admin/業務UI", "prototype", "統一componentを早く揃える"],
    ["完全custom visual identity", "utility-only workflowを好む"],
    ["tailwind-css", "foundation-css", "bulma"],
    aliases=["Twitter Bootstrap"], governance="Core team / community", license_name="MIT",
    source_urls=[("https://getbootstrap.com/docs/5.3/about/overview/", "Bootstrap overview"), ("https://blog.getbootstrap.com/2011/08/19/bootstrap-open-sourced/", "Bootstrap open sourced")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("bootstrap", "twitter-toolkit", "extracted-from", "Twitter内部UI toolkitからopen source化された。", grade="A", state="verified", source_url="https://blog.getbootstrap.com/2011/08/19/bootstrap-open-sourced/", target_kind="idea")

add(
    "tailwind-css", "Tailwind CSS", "TypeScript", "css-framework", ["css-ui", "web-frontend"], "tailwindlabs/tailwindcss", "https://tailwindcss.com/",
    "小さなutility classをmarkupで合成し、design tokenとbuild-time generationでcustom UIを構築するutility-first CSS framework。",
    ["component名ごとのcustom CSSと命名負担を減らす", "制約されたspacing/color/type scaleを直接markupで再利用する"],
    "Adam Wathanらがlarge CSS codebaseでのsemantic class抽象化の摩擦からutility-first approachを体系化し、production buildとの統合を進めた。",
    ["Utility-first", "Design tokens", "Content-driven generation", "Responsive/state variants", "Composition in markup"],
    ["Utilities", "Variants", "Theme configuration", "Plugin ecosystem", "Build optimization"],
    ["custom designを作りやすい", "CSS命名とscope問題を減らす", "tokenが一貫する"],
    ["markup classが長くなる", "component abstractionとの境界設計が必要", "build/tool versionへの依存"],
    ["custom design system", "component frameworkと併用", "rapid UI iteration"],
    ["semantic stylesheet中心を厳格に求める", "build stepを使えない"],
    ["bootstrap", "unocss", "bulma"],
    governance="Tailwind Labs", license_name="MIT",
    source_urls=[("https://tailwindcss.com/docs/styling-with-utility-classes", "Styling with utility classes"), ("https://tailwindcss.com/", "Tailwind CSS")],
    origin_evidence="supported", lineage_evidence="supported",
)
relation("tailwind-css", "utility-first-css", "implements", "単一責務utilityをmarkupで合成する。", grade="A", state="verified", source_url="https://tailwindcss.com/docs/styling-with-utility-classes", target_kind="idea")

add(
    "wordpress", "WordPress", "PHP", "cms", ["cms", "web-fullstack"], "WordPress/wordpress-develop", "https://wordpress.org/",
    "theme、plugin、editor、content model、adminを備え、blogから一般Web siteまで構築するopen-source CMS/application platform。",
    ["非programmerもcontentを公開・管理する", "theme/pluginでsite機能を拡張する"],
    "b2/cafelogのforkとしてMatt MullenwegとMike Littleが開始し、GPL plugin/theme ecosystemとcommunity governanceで巨大CMSへ成長した。",
    ["Plugin hooks", "Themes", "Content database", "Admin UI", "Backward compatibility"],
    ["Block editor", "REST API", "Plugin/theme APIs", "Media", "Users", "Multisite"],
    ["hostingとplugin ecosystemが最大級", "content editorに親しみやすい", "長い互換性実績"],
    ["plugin品質・security差", "legacy compatibilityによる設計制約", "高scale/custom domainではarchitecture整理が必要"],
    ["content site、blog、marketing", "編集者主体", "既存pluginを活用"],
    ["厳密なheadless architectureのみ", "複雑domain applicationをCMS modelへ無理に合わせる"],
    ["drupal", "ghost", "strapi"],
    governance="WordPress Foundation / open-source project with Automattic ecosystem", license_name="GPL-2.0-or-later",
    source_urls=[("https://wordpress.org/about/", "About WordPress"), ("https://wordpress.org/documentation/article/history-of-wordpress/", "History of WordPress")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("wordpress", "b2-cafelog", "fork-of", "b2/cafelog codebaseをforkして開始した。", grade="A", state="verified", source_url="https://wordpress.org/documentation/article/history-of-wordpress/", target_kind="idea")

add(
    "drupal", "Drupal", "PHP", "cms", ["cms", "web-fullstack"], "drupal/drupal", "https://www.drupal.org/",
    "structured content、taxonomy、permissions、views、module、configuration managementを備えたflexible enterprise CMS/framework。",
    ["複雑なcontent typeとworkflowを設定・拡張可能にする", "多言語・権限・integrationをenterprise規模で扱う"],
    "Dries Buytaertのstudent community message boardからdrop.orgとして始まり、Drupalと名付けられてmodular CMSへ発展した。",
    ["Structured content", "Hooks/plugins", "Configuration management", "Entity API", "Granular permissions"],
    ["Content types", "Views", "Taxonomy", "Workflow", "Multilingual", "Modules"],
    ["複雑なcontent modeling", "enterprise governanceとsecurity team", "headless/API利用"],
    ["学習・upgrade costが高い", "module組合せとcacheが複雑", "simple blogには過剰"],
    ["government/enterprise content portal", "複雑権限とworkflow", "structured content API"],
    ["小さなlanding page", "minimal hosting"],
    ["wordpress", "strapi", "wagtail"],
    governance="Drupal Association / community", license_name="GPL-2.0-or-later",
    source_urls=[("https://www.drupal.org/about/history", "Drupal history"), ("https://www.drupal.org/about/features", "Drupal features")],
    origin_evidence="verified", lineage_evidence="supported",
)
relation("drupal", "drop-org", "successor-of", "drop.org community softwareからDrupalへ発展した。", grade="A", state="verified", source_url="https://www.drupal.org/about/history", target_kind="idea")

add(
    "strapi", "Strapi", "TypeScript", "headless-cms", ["cms", "web-backend", "api"], "strapi/strapi", "https://strapi.io/",
    "content type builder、admin、REST/GraphQL API、plugin、role/permissionを提供するNode.js headless CMS。",
    ["frontendとcontent backendを分離する", "custom APIをゼロから作らずeditor UIとcontent modelを提供する"],
    "API-first/headless CMS需要に対し、JavaScript ecosystemでself-host可能かつcustomizableなcontent backendとして開発された。",
    ["Headless CMS", "Content-type builder", "API generation", "Plugin architecture", "Self-hosting"],
    ["Admin UI", "REST/GraphQL", "Permissions", "Media", "Internationalization", "Plugins"],
    ["frontendを自由に選べる", "content APIを早く構築", "self-hostとcustom code"],
    ["complex business domainをCMSへ寄せ過ぎる危険", "major upgrade/migration", "enterprise機能のedition差を確認"],
    ["multi-channel content", "Jamstack/headless frontend", "editor UIが必要"],
    ["transaction-heavy core business system", "static markdownだけで十分"],
    ["directus", "payload-cms", "contentful"],
    governance="Strapi company / community", license_name="MIT core with commercial offerings",
    source_urls=[("https://docs.strapi.io/cms/intro", "Strapi documentation"), ("https://github.com/strapi/strapi", "Strapi repository")],
    origin_evidence="supported", lineage_evidence="partial",
)
relation("strapi", "headless-cms", "implements", "content管理とpresentation frontendをAPI境界で分離する。", grade="A", state="verified", source_url="https://docs.strapi.io/cms/intro", target_kind="idea")

add(
    "streamlit", "Streamlit", "Python", "data-app-framework", ["data-app", "machine-learning", "web-fullstack"], "streamlit/streamlit", "https://streamlit.io/",
    "Python scriptを上から再実行するreactive modelで、data/ML dashboardとinteractive appを少ないWeb codeで構築するframework。",
    ["data scientistがHTML/JavaScriptなしでinteractive appを作る", "notebook/prototypeを共有可能なWeb UIへ変える"],
    "ML engineer向けtoolとして、imperative Python scriptとwidget stateをrerun modelで接続する発想から始まった。",
    ["Script rerun model", "Widget state", "Dataframe/chart integration", "Caching", "Python-only authoring"],
    ["Widgets", "Layouts", "Charts", "Session state", "Caching", "Multipage apps"],
    ["data appの開発が非常に速い", "Pythonだけで完結", "data ecosystemとの統合"],
    ["複雑なfrontend state/URL設計に制約", "rerunとcache semanticsの理解", "一般Web application architectureには不向き"],
    ["ML demo、internal dashboard、data exploration", "Python team"],
    ["複雑consumer SaaS frontend", "細かなclient interaction制御"],
    ["gradio", "dash", "panel", "shiny"],
    governance="Snowflake / community", license_name="Apache-2.0",
    source_urls=[("https://docs.streamlit.io/get-started/fundamentals/main-concepts", "Streamlit main concepts"), ("https://github.com/streamlit/streamlit", "Streamlit repository")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("streamlit", "reactive-rerun", "implements", "widget eventごとにPython scriptを再実行しcache/stateで結果を保つ。", grade="A", state="verified", source_url="https://docs.streamlit.io/get-started/fundamentals/main-concepts", target_kind="idea")

add(
    "gradio", "Gradio", "Python", "ml-ui-framework", ["data-app", "machine-learning", "ai-application"], "gradio-app/gradio", "https://www.gradio.app/",
    "Python function/modelへUI componentを接続し、ML/AI demoとapplicationをbrowserで共有するframework。",
    ["model inferenceを迅速にhuman-testableなUIへする", "input/output componentとqueue/sharingを標準化する"],
    "ML modelのdemo作成・共有を容易にする目的で始まり、Hugging Face ecosystemと統合されたAI application UI frameworkへ発展した。",
    ["Function-to-interface", "Component graph", "Event handlers", "Queueing", "Share/embed"],
    ["Blocks", "Chat interfaces", "Media components", "Streaming", "API generation", "Hugging Face integration"],
    ["AI demoを極めて速く作れる", "media input/outputが豊富", "Python中心"],
    ["complex product UIの自由度は一般frontendより低い", "public share/securityを評価", "queueとresource isolation設計が必要"],
    ["model demo、annotation、AI internal tool", "chat/multimodal prototype"],
    ["高度custom consumer frontend", "AI以外の一般業務Web"],
    ["streamlit", "dash", "reflex"],
    governance="Hugging Face / community", license_name="Apache-2.0",
    source_urls=[("https://www.gradio.app/guides/quickstart", "Gradio quickstart"), ("https://github.com/gradio-app/gradio", "Gradio repository")],
    origin_evidence="supported", lineage_evidence="partial",
)
relation("gradio", "function-to-ui", "implements", "Python callableのinput/outputをUI componentへ対応付ける。", grade="A", state="verified", source_url="https://www.gradio.app/guides/quickstart", target_kind="idea")

add(
    "shiny", "Shiny", "R", "data-app-framework", ["data-app", "scientific-computing", "web-fullstack"], "rstudio/shiny", "https://shiny.posit.co/",
    "reactive graphによってR/Pythonのdata analysisとbrowser UIを接続するinteractive Web application framework。",
    ["data analystが一般Web stackを学ばずinteractive appを作る", "input変更に必要な計算だけを再実行する"],
    "RStudio（現Posit）がR analysisをinteractive Webへ公開するために開発し、spreadsheet-like reactive programmingを明示的なdependency graphとして提供した。",
    ["Reactive graph", "Server-driven UI", "Declarative dependencies", "Session-scoped state", "R/Python data integration"],
    ["Inputs/outputs", "Reactive expressions", "Modules", "Async/extended tasks", "Theming", "Deployment ecosystem"],
    ["R data ecosystemと自然に統合", "reactive dependencyが明確", "analysis appの生産性"],
    ["large-scale frontend interactionには制約", "reactive graphの無限loop/invalidations", "session resource管理"],
    ["scientific dashboard、internal analytics", "R/Python analysisを共有"],
    ["offline native app", "complex consumer frontend"],
    ["streamlit", "dash", "panel"],
    governance="Posit / community", license_name="GPL-3.0",
    source_urls=[("https://shiny.posit.co/r/getstarted/shiny-basics/lesson1/", "Shiny basics"), ("https://shiny.posit.co/r/articles/build/reactivity-overview/", "Shiny reactivity")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("shiny", "reactive-programming", "implements", "input-output dependencyをreactive graphとして追跡する。", grade="A", state="verified", source_url="https://shiny.posit.co/r/articles/build/reactivity-overview/", target_kind="idea")

add(
    "scrapy", "Scrapy", "Python", "crawler-framework", ["web-crawling", "data-engineering", "automation"], "scrapy/scrapy", "https://scrapy.org/",
    "asynchronous request scheduling、spider、selector、item pipeline、middlewareを統合したWeb crawling/scraping framework。",
    ["大量pageを並行取得しdata extraction pipelineへ流す", "retry、throttle、deduplication、exportを標準化する"],
    "screen scraping companyでの実務から生まれ、Twisted event-driven networking上のreusable crawling frameworkとして公開された。",
    ["Event-driven crawling", "Spider callbacks", "Request scheduler", "Item pipeline", "Middleware"],
    ["Selectors", "AutoThrottle", "Duplicate filtering", "Pipelines", "Feed exports", "Distributed extensions"],
    ["crawlerの必要機能が統合", "高並行I/O", "middleware/pipelineで拡張"],
    ["JavaScript renderingは別browser統合", "site利用規約・robots・法的確認が必要", "async callback flowのdebug"],
    ["large-scale public Web crawl with permission", "ETL-style extraction"],
    ["single page取得だけ", "browser UI操作が中心"],
    ["colly", "crawlee", "playwright"],
    governance="Scrapy community / Zyte ecosystem", license_name="BSD-3-Clause",
    source_urls=[("https://docs.scrapy.org/en/latest/intro/overview.html", "Scrapy overview"), ("https://scrapy.org/", "Scrapy website")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("scrapy", "twisted", "built-on", "asynchronous networkingとdeferred executionにTwistedを利用する。", grade="A", state="verified", source_url="https://docs.scrapy.org/en/latest/topics/asyncio.html", target_kind="idea")

add(
    "hardhat", "Hardhat", "TypeScript", "smart-contract-framework", ["blockchain", "smart-contract", "testing"], "NomicFoundation/hardhat", "https://hardhat.org/",
    "Ethereum smart contractのcompile、test、local network、deployment、debug、pluginを統合するJavaScript/TypeScript development environment。",
    ["Solidity development toolchainを一貫化する", "local chainとstack traceでcontract failureをdebug可能にする"],
    "Nomic Labs/FoundationがEthereum developer experienceを改善するためBuidlerとして開始し、Hardhatへ改名・拡張した。",
    ["Local development network", "Plugin task system", "Solidity stack traces", "TypeScript integration", "Configurable toolchain"],
    ["Compile/test", "Hardhat Network", "Plugins", "Deployment integrations", "Verification"],
    ["JavaScript ecosystemと統合", "debugしやすいlocal network", "pluginが豊富"],
    ["Node dependency/tool version管理", "plugin compatibility", "chain-specific correctness/securityは別監査が必要"],
    ["Ethereum dApp contract development", "TypeScript test/deploy"],
    ["Rust-only toolchain", "non-EVM chain"],
    ["foundry", "truffle", "brownie"],
    aliases=["Buidler"], governance="Nomic Foundation", license_name="MIT",
    source_urls=[("https://hardhat.org/docs", "Hardhat documentation"), ("https://github.com/NomicFoundation/hardhat", "Hardhat repository")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("hardhat", "buidler", "successor-of", "初期名称BuidlerからHardhatへ改名・発展した。", grade="A", state="verified", source_url="https://github.com/NomicFoundation/hardhat", target_kind="idea")

add(
    "foundry", "Foundry", "Rust", "smart-contract-framework", ["blockchain", "smart-contract", "testing"], "foundry-rs/foundry", "https://getfoundry.sh/",
    "forge、cast、anvil、chiselを含む高速なRust製Ethereum development toolkitで、Solidity testとCLI-first workflowを中心にする。",
    ["contract compile/test/fuzz/deployを高速化する", "JavaScript以外のnative CLI workflowを提供する"],
    "DappToolsのCLI/Unix哲学とSolidity-native testingの流れをRustで再実装・拡張した。",
    ["Solidity-native tests", "Fast native tooling", "Fuzz/invariant testing", "CLI composition", "Local EVM"],
    ["Forge", "Cast", "Anvil", "Chisel", "Fuzzing", "Scripts"],
    ["test実行が速い", "Solidityでtestを書ける", "fuzz/invariant testingが標準"],
    ["Rust/native binary toolchainへの依存", "JavaScript plugin ecosystemはHardhatより小さい", "EVM外には適用不可"],
    ["Ethereum contract security testing", "CLI-first development", "Solidity-native tests"],
    ["TypeScript-centered dApp orchestration", "non-EVM chain"],
    ["hardhat", "dapptools", "truffle"],
    governance="Paradigm / community", license_name="MIT/Apache-2.0",
    source_urls=[("https://getfoundry.sh/introduction/overview/", "Foundry overview"), ("https://github.com/foundry-rs/foundry", "Foundry repository")],
    origin_evidence="supported", lineage_evidence="verified",
)
relation("foundry", "dapptools", "inspired-by", "DappToolsのCLI compositionとSolidity testing workflowを受け継いだ。", grade="B", state="supported", target_kind="idea")

add(
    "polkadot-sdk", "Polkadot SDK", "Rust", "blockchain-framework", ["blockchain", "distributed-computing", "runtime"], "paritytech/polkadot-sdk", "https://paritytech.github.io/polkadot-sdk/",
    "modular runtime、consensus、network、client、parachain toolingを組み合わせてcustom blockchainを構築するRust SDK。",
    ["blockchain runtimeを再利用可能moduleから構築する", "runtime logicをWasmとしてupgrade可能にする"],
    "Substrate、Polkadot、Cumulusなどのrepositoryを統合し、Polkadot ecosystemのblockchain development platformとして再編された。",
    ["FRAME pallets", "Wasm runtime", "Runtime upgrades", "Modular consensus/network", "Shared security ecosystem"],
    ["Runtime framework", "Client/node", "Parachain tooling", "Consensus modules", "Testing"],
    ["custom chainの自由度", "runtime module再利用", "on-chain upgrade model"],
    ["Rust/blockchain internalsの学習が非常に大きい", "compileとnode運用が重い", "ecosystem-specific architecture"],
    ["application-specific blockchain", "Polkadot parachain", "custom runtime research"],
    ["simple smart contractだけ", "centralized appで十分"],
    ["cosmos-sdk", "hyperledger-fabric", "ethereum"],
    aliases=["Substrate ecosystem"], governance="Parity / Web3 Foundation ecosystem", license_name="GPL/Apache/BSD mix",
    source_urls=[("https://paritytech.github.io/polkadot-sdk/master/polkadot_sdk_docs/index.html", "Polkadot SDK docs"), ("https://github.com/paritytech/polkadot-sdk", "Polkadot SDK repository")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("polkadot-sdk", "substrate", "successor-of", "Substrate、Polkadot、Cumulus codebasesを統合したSDK repositoryへ再編された。", grade="A", state="verified", source_url="https://github.com/paritytech/polkadot-sdk", target_kind="idea")
relation("polkadot-sdk", "modular-runtime", "implements", "FRAME palletを組み合わせてWasm runtimeを構築する。", grade="A", state="verified", source_url="https://paritytech.github.io/polkadot-sdk/master/polkadot_sdk_docs/index.html", target_kind="idea")

add(
    "cosmos-sdk", "Cosmos SDK", "Go", "blockchain-framework", ["blockchain", "distributed-computing"], "cosmos/cosmos-sdk", "https://docs.cosmos.network/",
    "state machine module、transaction、query、staking/governance primitivesを組み合わせてapplication-specific blockchainを構築するGo framework。",
    ["consensus/network実装からapplication logicを分離する", "reusable moduleでsovereign chainを構築する"],
    "Tendermint consensus/application interfaceの上に、ABCI applicationをmodularに作るframeworkとしてCosmos ecosystemで開発された。",
    ["ABCI separation", "Modular state machine", "Modules/keepers", "Deterministic execution", "Interchain ecosystem"],
    ["BaseApp", "Modules", "Store", "Transactions", "Governance/staking", "IBC integration"],
    ["consensusとapp logicを分離", "module reuse", "sovereign chainを設計可能"],
    ["distributed consensusとeconomic securityの高度な知識", "chain upgrade/state migration", "simple appには過剰"],
    ["application-specific blockchain", "Cosmos/IBC ecosystem"],
    ["ordinary database app", "smart contractだけで十分"],
    ["polkadot-sdk", "hyperledger-fabric", "ethereum"],
    governance="Interchain / community", license_name="Apache-2.0",
    source_urls=[("https://docs.cosmos.network/main/learn/intro/why-app-specific", "Why application-specific blockchains"), ("https://github.com/cosmos/cosmos-sdk", "Cosmos SDK repository")],
    origin_evidence="verified", lineage_evidence="verified",
)
relation("cosmos-sdk", "tendermint-abci", "built-on", "consensus/networkとapplication state machineをABCI境界で分離する。", grade="A", state="verified", source_url="https://docs.cosmos.network/main/learn/intro/sdk-app-architecture", target_kind="idea")

# ---------------------------------------------------------------------------
# Standard profiles: broad cross-language catalog
# ---------------------------------------------------------------------------
def add_standard_rows(kind: str, domains: list[str], rows: list[tuple[Any, ...]]) -> None:
    for row in rows:
        (
            id, name, language, repository, homepage, summary, problem,
            traits, strengths, weaknesses, alternatives, *rest
        ) = row
        status = rest[0] if rest else "active"
        standard(
            id, name, language, kind, domains, repository, homepage,
            summary, problem,
            list(traits), list(strengths), list(weaknesses), list(alternatives), status=status,
        )


add_standard_rows("web-framework", ["web-backend", "api"], [
    ("starlette", "Starlette", "Python", "encode/starlette", "https://www.starlette.io/", "軽量ASGI toolkitとしてrouting、middleware、WebSocket、background taskを提供する。", "ASGI applicationの共通部品を小さく再利用可能にする。", ("ASGI", "Composable middleware", "Async-first"), ("小さく高速", "FastAPI等の基盤"), ("統合ORMやDIはない", "application規約は利用側が設計"), ("fastapi", "litestar", "quart")),
    ("litestar", "Litestar", "Python", "litestar-org/litestar", "https://litestar.dev/", "型付きrouting、DI、OpenAPI、ORM integrationを備えるASGI framework。", "型安全なPython APIをbatteries-included寄りに構築する。", ("Type-driven", "ASGI", "Dependency injection"), ("統合機能が多い", "async support"), ("FastAPIよりecosystemが小さい", "機能範囲が広い"), ("fastapi", "django-ninja", "falcon")),
    ("django-ninja", "Django Ninja", "Python", "vitalik/django-ninja", "https://django-ninja.dev/", "Django上に型ヒント駆動のAPIとOpenAPI生成を追加するframework。", "Django資産を維持しながらFastAPI風API開発を行う。", ("Django integration", "Type hints", "OpenAPI"), ("Django ORM/adminを再利用", "短いAPI記述"), ("Django lifecycleに依存", "ASGI native設計との差"), ("fastapi", "django-rest-framework", "litestar")),
    ("django-rest-framework", "Django REST framework", "Python", "encode/django-rest-framework", "https://www.django-rest-framework.org/", "Django向けserialization、view、authentication、browsable API framework。", "Django modelを安全で拡張可能なREST APIとして公開する。", ("Serializers", "Class-based views", "Browsable API"), ("Django統合が深い", "権限・認証が成熟"), ("abstractionが多い", "高性能async APIには調整"), ("django-ninja", "fastapi", "tastypie")),
    ("falcon", "Falcon", "Python", "falconry/falcon", "https://falcon.readthedocs.io/", "minimalで高性能なWSGI/ASGI API framework。", "HTTP APIを低overheadかつ明示的に実装する。", ("REST-oriented", "WSGI/ASGI", "Minimal"), ("処理経路が明確", "性能を出しやすい"), ("統合機能が少ない", "周辺選択が必要"), ("fastapi", "flask", "litestar")),
    ("pyramid", "Pyramid", "Python", "Pylons/pyramid", "https://trypyramid.com/", "small startからlarge applicationまで構成を選べるPython Web framework。", "microframeworkの自由度とlarge appの拡張性を両立する。", ("Traversal or URL dispatch", "Explicit configuration", "Flexible"), ("構成自由度", "mature security model"), ("主流ecosystemが縮小", "選択肢が多い"), ("django", "flask", "zope")),
    ("tornado", "Tornado", "Python", "tornadoweb/tornado", "https://www.tornadoweb.org/", "event loop、HTTP server/client、WebSocketを含むPython networking/Web framework。", "多数long-lived connectionを少ないthreadで扱う。", ("Non-blocking I/O", "Integrated server", "WebSockets"), ("長時間接続", "低level control"), ("asyncio時代に役割が重複", "full-stack機能は少ない"), ("aiohttp", "sanic", "starlette")),
    ("aiohttp", "aiohttp", "Python", "aio-libs/aiohttp", "https://docs.aiohttp.org/", "asyncio上のHTTP client/server framework。", "同じasync modelでHTTP clientとserverを構築する。", ("asyncio-native", "Client and server", "Streaming"), ("低level async control", "成熟"), ("高level schema/DIはない", "event loop知識が必要"), ("httpx", "starlette", "sanic")),
    ("sanic", "Sanic", "Python", "sanic-org/sanic", "https://sanic.dev/", "async-firstで高throughputを狙うPython Web server/framework。", "asyncio applicationを簡潔に高並行実行する。", ("Async-first", "Integrated server", "Middleware"), ("高並行I/O", "WebSocket support"), ("ecosystemがDjango/FastAPIより小さい", "architectureは利用側責任"), ("fastapi", "aiohttp", "tornado")),
    ("quart", "Quart", "Python", "pallets/quart", "https://quart.palletsprojects.com/", "Flask互換感を持つASGI async Web framework。", "Flask styleを保ちながらasync/WebSocketへ移行する。", ("Flask-compatible API", "ASGI", "WebSockets"), ("Flask経験を再利用", "async-native"), ("完全互換ではない", "ecosystem規模"), ("flask", "fastapi", "starlette")),
    ("bottle", "Bottle", "Python", "bottlepy/bottle", "https://bottlepy.org/", "single-fileで依存の少ないPython micro Web framework。", "極小deploymentと学習用にrouting/templateを提供する。", ("Single file", "WSGI", "Minimal dependencies"), ("導入が簡単", "embeddingしやすい"), ("large app機能が少ない", "async-nativeではない"), ("flask", "cherrypy", "webpy")),
    ("cherrypy", "CherryPy", "Python", "cherrypy/cherrypy", "https://cherrypy.dev/", "Python objectをHTTP endpointへ公開する長寿命Web framework/server。", "Pythonic object modelでWeb server applicationを構築する。", ("Object publishing", "Embedded server", "Tools"), ("mature", "standalone server"), ("現代的ecosystemが小さい", "API styleが独特"), ("flask", "pyramid", "bottle")),
    ("web2py", "web2py", "Python", "web2py/web2py", "http://www.web2py.com/", "IDE、DAL、admin、securityを統合したfull-stack Python framework。", "install-freeに近い統合環境でdatabase Web appを迅速に作る。", ("Integrated IDE", "DAL", "Batteries included"), ("一体型", "rapid CRUD"), ("主流Python ecosystemとの差", "独自tooling"), ("django", "webpy", "pyramid")),
    ("masonite", "Masonite", "Python", "MasoniteFramework/masonite", "https://docs.masoniteproject.com/", "Laravel/Rails風のdeveloper experienceをPythonへ提供するfull-stack framework。", "Pythonでservice container、ORM、CLIを統合したWeb開発を行う。", ("Convention", "Service container", "Full-stack"), ("統合体験", "読みやすい構造"), ("communityが小さい", "Djangoとの差別化を確認"), ("django", "laravel", "flask")),
    ("blacksheep", "BlackSheep", "Python", "Neoteroi/BlackSheep", "https://www.neoteroi.dev/blacksheep/", "ASGI上の高速で型付きなPython Web framework。", "async APIを低overheadで構築する。", ("ASGI", "Type annotations", "Performance"), ("高速", "OpenAPI integration"), ("ecosystemが小さい", "資料量"), ("fastapi", "litestar", "falcon")),
])

add_standard_rows("web-framework", ["web-backend", "api", "javascript"], [
    ("koa", "Koa", "JavaScript", "koajs/koa", "https://koajs.com/", "async functionと小さなmiddleware coreを中心にするNode Web framework。", "Expressのcallback/legacy baggageを減らし、より小さなcomposition modelを提供する。", ("Async middleware", "Minimal core", "Context"), ("小さく明示的", "middleware composition"), ("routing等は別package", "大規模規約なし"), ("express", "fastify", "hapi")),
    ("hapi", "hapi", "JavaScript", "hapijs/hapi", "https://hapi.dev/", "configuration-drivenでvalidation、auth、plugin lifecycleを重視するNode server framework。", "enterprise APIのpolicyとplugin境界を統一する。", ("Configuration-driven", "Plugin realms", "Lifecycle extensions"), ("security/validation設計", "plugin isolation"), ("学習APIが大きい", "ecosystem規模"), ("fastify", "express", "nestjs")),
    ("adonisjs", "AdonisJS", "TypeScript", "adonisjs/core", "https://adonisjs.com/", "ORM、auth、validation、CLIを統合したTypeScript full-stack backend framework。", "Laravel風の一体型developer experienceをNodeへ提供する。", ("Convention", "IoC", "Full-stack"), ("統合tooling", "TypeScript-first"), ("Express ecosystemとの違い", "小規模には重い"), ("nestjs", "laravel", "redwoodjs")),
    ("feathers", "Feathers", "TypeScript", "feathersjs/feathers", "https://feathersjs.com/", "service abstractionからREST/real-time APIを生成するNode framework。", "同じservice interfaceを複数transportから利用可能にする。", ("Service-oriented", "Transport agnostic", "Hooks"), ("real-time API", "CRUDを短く実装"), ("service modelにdomainを合わせる必要", "custom flowで複雑化"), ("nestjs", "loopback", "meteor")),
    ("meteor", "Meteor", "JavaScript", "meteor/meteor", "https://www.meteor.com/", "client/server data synchronization、build、packageを統合したfull-stack JavaScript platform。", "リアルタイムWeb appを一つのJavaScript stackで迅速に作る。", ("Full-stack reactivity", "Data synchronization", "Integrated build"), ("prototypeが速い", "real-time model"), ("独自data protocolとplatform", "modern modular stackとの差"), ("nextjs", "redwoodjs", "firebase")),
    ("loopback", "LoopBack", "TypeScript", "loopbackio/loopback-next", "https://loopback.io/", "model、repository、DI、OpenAPIからenterprise APIを構築するNode framework。", "data sourceとAPI contractをmetadata-drivenに統合する。", ("OpenAPI", "Dependency injection", "Repository pattern"), ("enterprise integration", "strong metadata"), ("abstractionが多い", "community momentum"), ("nestjs", "feathers", "express")),
    ("sails", "Sails.js", "JavaScript", "balderdashy/sails", "https://sailsjs.com/", "Rails-like MVCとWaterline ORMを持つNode Web framework。", "Nodeでdata-driven full-stack applicationを規約的に作る。", ("MVC", "Convention", "Realtime sockets"), ("CRUD/real-timeが速い", "Rails経験を活用"), ("modern TS ecosystemとの差", "ORM制約"), ("adonisjs", "meteor", "nestjs")),
    ("elysia", "Elysia", "TypeScript", "elysiajs/elysia", "https://elysiajs.com/", "Bunに最適化された型推論重視のTypeScript Web framework。", "runtimeからclientまでend-to-end type safetyを提供する。", ("Bun-first", "Schema/type inference", "Plugin lifecycle"), ("高速", "型推論"), ("Bun ecosystem依存", "Node互換性の差"), ("hono", "fastify", "nestjs")),
    ("hono", "Hono", "TypeScript", "honojs/hono", "https://hono.dev/", "Web Standards APIを使いedge、serverless、Node/Bun/Denoで動くsmall Web framework。", "runtime横断で同じRequest/Response codeを使う。", ("Web Standards", "Multi-runtime", "Small core"), ("edge portable", "軽量"), ("full-stack機能は別選択", "runtime差は残る"), ("elysia", "express", "oak")),
    ("oak", "Oak", "TypeScript", "oakserver/oak", "https://oakserver.org/", "Deno向けmiddleware/router Web framework。", "Deno runtimeでKoa風server applicationを構築する。", ("Deno-first", "Middleware", "Web Standards"), ("Deno統合", "simple composition"), ("Deno ecosystem規模", "full-stackではない"), ("hono", "koa", "fresh")),
    ("fresh", "Fresh", "TypeScript", "denoland/fresh", "https://fresh.deno.dev/", "Deno向けislands、server rendering、zero-build志向のWeb framework。", "client JavaScriptを必要箇所だけ配信しDenoでfull-stackを簡潔にする。", ("Islands", "Deno", "No build by default"), ("低client JS", "simple deployment"), ("Denoに依存", "ecosystemが小さい"), ("astro", "nextjs", "hono")),
    ("nitro", "Nitro", "TypeScript", "nitrojs/nitro", "https://nitro.build/", "universal deployment adapterを持つTypeScript server toolkit。", "server codeをNode、edge、serverlessへ同じinterfaceでdeployする。", ("Universal server", "Storage abstraction", "Deployment presets"), ("deploy portability", "Nuxt基盤"), ("adapter差", "単体利用情報が少ない"), ("hono", "fastify", "serverless-http")),
    ("redwoodjs", "RedwoodSDK / RedwoodJS", "TypeScript", "redwoodjs/redwood", "https://redwoodjs.com/", "React、GraphQL、database、testing、deploymentを統合したfull-stack frameworkの系譜。", "startup向けWeb productのfrontend/backend/toolingを一つの規約にする。", ("Full-stack conventions", "GraphQL", "Cells"), ("統合developer experience", "testing/deploy guidance"), ("project direction変更を確認", "規約が強い"), ("nextjs", "blitz", "remix")),
    ("blitz", "Blitz.js", "TypeScript", "blitz-js/blitz", "https://blitzjs.com/", "Next.js上にauth、RPC/data layer、code generationを追加するfull-stack toolkit。", "Rails-like full-stack productivityをReact/Next.jsへ持ち込む。", ("Zero-API data layer", "Full-stack toolkit", "Convention"), ("auth/data setupが速い", "Next.js資産"), ("Next.js変化に依存", "community規模"), ("nextjs", "redwoodjs", "trpc")),
    ("medusajs", "Medusa", "TypeScript", "medusajs/medusa", "https://medusajs.com/", "modular commerce backend、workflow、admin、pluginを提供するcommerce framework。", "headless commerceのorder、cart、inventory等を再利用可能moduleで構築する。", ("Commerce modules", "Workflows", "Headless"), ("custom commerceに柔軟", "open-source core"), ("domain complexity", "version migration"), ("saleor", "vendure", "shopify")),
])

add_standard_rows("web-framework", ["web-backend", "api", "go"], [
    ("echo", "Echo", "Go", "labstack/echo", "https://echo.labstack.com/", "高速router、middleware、bindingを備えるGo Web framework。", "net/http API開発を簡潔にする。", ("Radix router", "Middleware", "Binding"), ("simple", "high performance"), ("application architectureは未規定", "context中心になりやすい"), ("gin", "fiber", "chi")),
    ("fiber", "Fiber", "Go", "gofiber/fiber", "https://gofiber.io/", "fasthttp上でExpress風APIを提供するGo Web framework。", "Express-like ergonomicsと高性能をGoで両立する。", ("fasthttp", "Express-like", "Middleware"), ("高速", "親しみやすいAPI"), ("net/http互換でない部分", "fasthttp tradeoff"), ("gin", "echo", "chi")),
    ("chi", "chi", "Go", "go-chi/chi", "https://go-chi.io/", "net/http互換を保つ軽量composable router。", "標準HTTP handlerのままrouting/middlewareを構成する。", ("net/http compatible", "Composable routers", "Small"), ("標準libraryとの親和性", "低抽象化"), ("full-stack機能なし", "binding等を自作"), ("gin", "httprouter", "gorilla-mux")),
    ("beego", "Beego", "Go", "beego/beego", "https://beego.vip/", "MVC、ORM、CLI、configurationを統合したGo application framework。", "Goでbatteries-included Web appを規約的に作る。", ("MVC", "ORM", "Integrated tooling"), ("full-stack", "code generation"), ("idiomatic net/httpから距離", "ecosystem地域差"), ("revel", "goframe", "gin")),
    ("revel", "Revel", "Go", "revel/revel", "https://revel.github.io/", "hot reload、MVC、binding、validationを統合するGo Web framework。", "Rails-like developer experienceをGoへ提供する。", ("MVC", "Hot reload", "Convention"), ("rapid full-stack", "integrated tooling"), ("Go標準styleとの差", "community momentum"), ("beego", "goframe", "gin")),
    ("goframe", "GoFrame", "Go", "gogf/gf", "https://goframe.org/", "Web、ORM、CLI、config、loggingを含むmodular Go framework。", "enterprise Go applicationの共通部品を一体化する。", ("Modular full-stack", "Code generation", "Enterprise utilities"), ("機能範囲が広い", "中国語ecosystemが強い"), ("学習量", "標準libraryとの重複"), ("beego", "go-zero", "kratos")),
    ("go-zero", "go-zero", "Go", "zeromicro/go-zero", "https://go-zero.dev/", "code generation、RPC、resilience、observabilityを統合するmicroservice framework。", "large-scale Go microserviceの定型architectureを標準化する。", ("Code generation", "Built-in resilience", "RPC/REST"), ("service scaffolding", "operational patterns"), ("規約が強い", "generated code依存"), ("kratos", "gofr", "go-kit")),
    ("kratos", "Kratos", "Go", "go-kratos/kratos", "https://go-kratos.dev/", "transport、service、data layeringとobservabilityを支援するGo microservice framework。", "clean architecture寄りのservice structureを再利用可能にする。", ("Layered architecture", "Transport abstraction", "Protobuf"), ("明示的構造", "cloud-native integration"), ("boilerplate", "small serviceには重い"), ("go-zero", "go-kit", "gofr")),
    ("gofr", "GoFr", "Go", "gofr-dev/gofr", "https://gofr.dev/", "observability、database、pubsubを組み込んだGo microservice framework。", "production-ready service plumbingを初期から提供する。", ("Observability-first", "Data integrations", "REST/gRPC"), ("運用機能が標準", "rapid setup"), ("若いecosystem", "抽象化選択"), ("go-zero", "kratos", "gin")),
    ("buffalo", "Buffalo", "Go", "gobuffalo/buffalo", "https://gobuffalo.io/", "asset、ORM、generatorを含むRails-like Go Web ecosystem。", "Go full-stack appを統合toolchainで作る。", ("Code generation", "Full-stack", "Convention"), ("初期構築が速い", "integrated assets"), ("community momentum", "generated structure"), ("revel", "beego", "gin")),
    ("go-kit", "Go kit", "Go", "go-kit/kit", "https://gokit.io/", "transport、endpoint、service middlewareを分離するmicroservice toolkit。", "distributed service concernsを明示的なlayerへ分ける。", ("Explicit layers", "Transport agnostic", "Functional middleware"), ("architectureが明確", "vendor neutral"), ("boilerplateが多い", "frameworkよりtoolkit"), ("kratos", "go-zero", "dapr")),
])

add_standard_rows("web-framework", ["web-backend", "api", "rust"], [
    ("actix-web", "Actix Web", "Rust", "actix/actix-web", "https://actix.rs/", "actor project系譜の高性能Rust Web framework。", "型安全かつ高throughputのHTTP serviceを構築する。", ("Async", "Extractor", "Service middleware"), ("performance", "mature ecosystem"), ("API/lifetime学習", "actorとの関係が誤解されやすい"), ("axum", "rocket", "poem")),
    ("rocket", "Rocket", "Rust", "rwf2/Rocket", "https://rocket.rs/", "macroとtyped request guardsでergonomicなRust Web developmentを提供する。", "Rustの型でroute contractとvalidationを表現する。", ("Typed routes", "Request guards", "Macros"), ("読みやすいAPI", "type safety"), ("macro magic", "async ecosystem選択"), ("axum", "actix-web", "loco")),
    ("warp", "warp", "Rust", "seanmonstar/warp", "https://github.com/seanmonstar/warp", "composable filterを使うHyperベースRust Web framework。", "route、validation、extractionを型付きfilter algebraで合成する。", ("Filters", "Hyper", "Type composition"), ("composable", "safe"), ("複雑型error", "maintenance status確認"), ("axum", "poem", "actix-web")),
    ("poem", "Poem", "Rust", "poem-web/poem", "https://poem.rs/", "OpenAPI integrationを持つergonomicなRust Web framework。", "Rust API serverとschema/documentationを統合する。", ("Async", "OpenAPI", "Endpoint composition"), ("API tooling", "clear abstractions"), ("ecosystem規模", "version changes"), ("axum", "actix-web", "salvo")),
    ("salvo", "Salvo", "Rust", "salvo-rs/salvo", "https://salvo.rs/", "handler depot、middleware、OpenAPIを備えるRust Web framework。", "簡潔なRust HTTP applicationを構築する。", ("Handler pipeline", "OpenAPI", "Multi-server"), ("featuresが多い", "ergonomic"), ("community規模", "選択肢比較が必要"), ("poem", "axum", "actix-web")),
    ("loco", "Loco", "Rust", "loco-rs/loco", "https://loco.rs/", "Rails-inspiredなRust full-stack Web framework。", "Rustでconvention、ORM、generatorを持つproduct developmentを行う。", ("Convention", "SeaORM", "Generators"), ("rapid Rust full-stack", "integrated stack"), ("若いframework", "Rust compile/learning cost"), ("rocket", "axum", "rails")),
    ("leptos", "Leptos", "Rust", "leptos-rs/leptos", "https://leptos.dev/", "fine-grained reactivityとSSR/hydrationを持つRust full-stack Web framework。", "Rustだけでreactive client/server Web appを構築する。", ("Signals", "SSR", "Rust/Wasm"), ("end-to-end Rust", "fine-grained updates"), ("Wasm ecosystem", "compile time"), ("dioxus", "yew", "solidjs")),
    ("dioxus", "Dioxus", "Rust", "DioxusLabs/dioxus", "https://dioxuslabs.com/", "React-like component modelでweb、desktop、mobileを扱うRust UI framework。", "一つのRust UI modelを複数rendererへ展開する。", ("RSX", "Multi-platform", "Signals"), ("cross-platform Rust", "familiar component model"), ("platform maturity差", "ecosystemが若い"), ("leptos", "yew", "tauri")),
    ("yew", "Yew", "Rust", "yewstack/yew", "https://yew.rs/", "componentとvirtual DOMでRust/Wasm SPAを構築するframework。", "Rustの型安全性をbrowser UIへ持ち込む。", ("Components", "Virtual DOM", "Wasm"), ("type safety", "mature Rust Web UI"), ("bundle/compile cost", "JS interop"), ("leptos", "dioxus", "sycamore")),
    ("sycamore", "Sycamore", "Rust", "sycamore-rs/sycamore", "https://sycamore-rs.netlify.app/", "fine-grained reactivityを持つRust/Wasm UI framework。", "virtual DOMなしでreactive browser UIを構築する。", ("Signals", "Fine-grained", "Wasm"), ("small updates", "Rust types"), ("ecosystem規模", "project activity確認"), ("leptos", "yew", "solidjs")),
])

add_standard_rows("application-framework", ["web-backend", "jvm", "enterprise"], [
    ("dropwizard", "Dropwizard", "Java", "dropwizard/dropwizard", "https://www.dropwizard.io/", "Jetty、Jersey、Jackson、Metrics等をopinionatedに束ねるJava service framework。", "production HTTP serviceの標準部品選択を減らす。", ("Curated stack", "Configuration", "Operational metrics"), ("simple deployment", "mature components"), ("full Spring ecosystemより限定", "stack変更に制約"), ("spring-boot", "micronaut", "helidon")),
    ("helidon", "Helidon", "Java", "helidon-io/helidon", "https://helidon.io/", "SEとMicroProfile stylesを提供するcloud-native Java framework。", "軽量Java microserviceと標準MicroProfile applicationを構築する。", ("Reactive or declarative", "MicroProfile", "Cloud-native"), ("Oracle support", "small runtime options"), ("ecosystemがSpringより小さい", "edition選択"), ("quarkus", "micronaut", "spring-boot")),
    ("vertx", "Eclipse Vert.x", "Java", "eclipse-vertx/vert.x", "https://vertx.io/", "event loopとverticle modelでpolyglot reactive applicationを作るtoolkit。", "JVM上で高並行・非blocking serviceを構成する。", ("Event loop", "Verticles", "Event bus"), ("high concurrency", "polyglot JVM"), ("callback/event model学習", "full-stack規約なし"), ("akka", "quarkus", "spring-webflux")),
    ("play-framework", "Play Framework", "Scala", "playframework/playframework", "https://www.playframework.com/", "stateless、reactive、hot reloadを重視するScala/Java Web framework。", "JVMでdeveloper-friendlyなnon-blocking Web applicationを作る。", ("Reactive", "MVC", "Hot reload"), ("Scala integration", "full-stack Web"), ("ecosystem momentum", "build/Scala version complexity"), ("spring-boot", "http4s", "akka-http")),
    ("grails", "Grails", "Groovy", "grails/grails-core", "https://grails.org/", "SpringとGroovyを使うConvention over Configuration Web framework。", "JVMでRails-like productivityを提供する。", ("Convention", "Groovy DSL", "Spring integration"), ("rapid JVM development", "Spring ecosystem"), ("dynamic Groovy tradeoff", "community規模"), ("spring-boot", "rails", "micronaut")),
    ("vaadin-flow", "Vaadin Flow", "Java", "vaadin/flow", "https://vaadin.com/flow", "Java componentからserver-driven Web UIを構築するframework。", "frontend JavaScriptを最小化してenterprise UIをJavaで作る。", ("Server-driven UI", "Java components", "State synchronization"), ("Java-only development", "enterprise widgets"), ("server session/resource cost", "client customization理解"), ("jsf", "gwt", "blazor")),
    ("jsf", "Jakarta Faces", "Java", "eclipse-ee4j/mojarra", "https://jakarta.ee/specifications/faces/", "component-based server-side Java Web UI standard。", "form-heavy enterprise UIのlifecycleとcomponentを標準化する。", ("Server-side components", "Managed lifecycle", "Jakarta EE"), ("standard platform", "component libraries"), ("complex lifecycle", "modern client UIとの差"), ("vaadin-flow", "spring-mvc", "thymeleaf")),
    ("struts", "Apache Struts", "Java", "apache/struts", "https://struts.apache.org/", "action-based MVCでJava Web applicationを構築する歴史的framework。", "Servlet/JSP applicationにcontrollerとvalidation構造を与える。", ("Action MVC", "Interceptors", "Configuration"), ("legacy enterprise knowledge", "mature"), ("security/upgrade historyを厳格管理", "new projectsには選択理由が弱い"), ("spring-mvc", "jakarta-faces", "wicket")),
    ("wicket", "Apache Wicket", "Java", "apache/wicket", "https://wicket.apache.org/", "stateful componentとHTML templateを使うJava Web UI framework。", "Java object-oriented component modelでserver-rendered Web UIを作る。", ("Stateful components", "Plain HTML templates", "Server-side"), ("strong Java model", "testable components"), ("session state cost", "SPA ecosystemとの差"), ("vaadin-flow", "jsf", "spring-mvc")),
    ("spark-java", "Spark Java", "Java", "perwendel/spark", "https://sparkjava.com/", "lambda routingを使う小さなJava microframework。", "minimal codeでHTTP endpointを作る。", ("Lambda routes", "Embedded server", "Minimal"), ("簡単", "small footprint"), ("大規模構造なし", "maintenance activity確認"), ("javalin", "jooby", "spring-boot")),
    ("javalin", "Javalin", "Kotlin", "javalin/javalin", "https://javalin.io/", "Java/Kotlin向け軽量Web framework。", "simple handler APIでWebSocket/APIを作る。", ("Simple handlers", "Jetty", "Java/Kotlin"), ("low ceremony", "good docs"), ("full-stack機能なし", "architectureは利用側"), ("ktor", "spark-java", "jooby")),
    ("jooby", "Jooby", "Java", "jooby-project/jooby", "https://jooby.io/", "type-safe routing、DI integration、multiple serverを支援するJVM Web framework。", "small fast Java/Kotlin serviceをmodule compositionで作る。", ("Type-safe routes", "Modules", "Multiple servers"), ("lightweight", "flexible integration"), ("community規模", "choices require design"), ("javalin", "ktor", "micronaut")),
    ("ratpack", "Ratpack", "Java", "ratpack/ratpack", "https://ratpack.io/", "Netty上のnon-blocking Java/Groovy Web toolkit。", "reactive HTTP applicationをsmall handler chainで構築する。", ("Non-blocking", "Handler chain", "Netty"), ("performance", "simple core"), ("project activity確認", "reactive complexity"), ("vertx", "ktor", "spring-webflux")),
    ("finatra", "Finatra", "Scala", "twitter/finatra", "https://twitter.github.io/finatra/", "Finagle上のScala Web/RPC framework。", "Twitter-scale networking componentsでtyped serviceを構築する。", ("Finagle", "Dependency injection", "Thrift/HTTP"), ("production lineage", "strong networking"), ("Twitter stack依存", "ecosystem niche"), ("play-framework", "http4s", "akka-http")),
    ("akka-http", "Akka HTTP", "Scala", "akka/akka-http", "https://doc.akka.io/docs/akka-http/current/", "stream-based server/clientとrouting DSLを提供するJVM HTTP toolkit。", "Reactive Streams上にbackpressure-aware HTTP serviceを構築する。", ("Streams", "Routing DSL", "Backpressure"), ("Akka integration", "streaming"), ("Akka licensing/complexity", "full-stackではない"), ("http4s", "play-framework", "vertx")),
    ("http4s", "http4s", "Scala", "http4s/http4s", "https://http4s.org/", "pure functional HTTP server/client library for Scala。", "effect typeとstreamでcomposable HTTP applicationを作る。", ("Pure functional", "Cats Effect", "Streaming"), ("referential transparency", "composition"), ("FP learning curve", "full-stack features separate"), ("zio-http", "akka-http", "play-framework")),
    ("zio-http", "ZIO HTTP", "Scala", "zio/zio-http", "https://zio.dev/zio-http/", "ZIO effect system上のhigh-performance HTTP framework。", "typed errors、resources、concurrencyとHTTPを統合する。", ("ZIO effects", "Typed channels", "Netty"), ("effect integration", "performance"), ("ZIO learning curve", "ecosystem specialization"), ("http4s", "akka-http", "play-framework")),
])

add_standard_rows("web-framework", ["web-backend", "php"], [
    ("codeigniter", "CodeIgniter", "PHP", "codeigniter4/CodeIgniter4", "https://codeigniter.com/", "small footprintとsimple MVCを重視するPHP framework。", "minimal configurationでtraditional PHP Web appを構築する。", ("MVC", "Small footprint", "Simple setup"), ("学習しやすい", "shared hosting friendly"), ("enterprise component depth", "legacy versions混在"), ("laravel", "slim", "cakephp")),
    ("yii", "Yii", "PHP", "yiisoft/yii2", "https://www.yiiframework.com/", "performance、code generation、Active Recordを備えるPHP full-stack framework。", "database-driven Web appを高速に構築する。", ("MVC", "Gii generation", "Active Record"), ("CRUD productivity", "mature"), ("Yii2/3 transition理解", "global patterns"), ("laravel", "symfony", "cakephp")),
    ("cakephp", "CakePHP", "PHP", "cakephp/cakephp", "https://cakephp.org/", "Convention over Configurationを早期に採用したPHP MVC framework。", "PHP Web appのCRUDと構造を規約化する。", ("Convention", "ORM", "Bake generation"), ("mature", "rapid CRUD"), ("ecosystem smaller than Laravel", "convention constraints"), ("laravel", "yii", "codeigniter")),
    ("slim", "Slim", "PHP", "slimphp/Slim", "https://www.slimframework.com/", "PSR-compatible middleware中心のPHP microframework。", "small APIとHTTP middleware applicationを構築する。", ("PSR-7/15", "Middleware", "Minimal"), ("standards-based", "small core"), ("DI/ORM等は別選択", "large app conventions absent"), ("mezzio", "laravel", "symfony")),
    ("phalcon", "Phalcon", "C", "phalcon/cphalcon", "https://phalcon.io/", "C extensionとして実装されたhigh-performance PHP full-stack framework。", "PHP APIを保ちながらframework overheadをnative extensionで抑える。", ("C extension", "MVC", "ORM"), ("performance", "integrated features"), ("extension deployment", "debug/build complexity"), ("laravel", "yii", "symfony")),
    ("nette", "Nette", "PHP", "nette/application", "https://nette.org/", "securityとcomponent modelを重視するPHP framework ecosystem。", "安全なWeb appをreusable componentとDIで構築する。", ("Components", "DI", "Secure defaults"), ("strong tooling", "Central Europe ecosystem"), ("global community smaller", "package selection"), ("symfony", "laravel", "yii")),
    ("mezzio", "Mezzio", "PHP", "mezzio/mezzio", "https://docs.mezzio.dev/", "PSR-15 middleware application framework。", "standards-based middlewareでmodular PHP applicationを構築する。", ("PSR middleware", "Container agnostic", "Modular"), ("interoperability", "explicit composition"), ("more assembly work", "full-stack features separate"), ("slim", "symfony", "laminas-mvc")),
    ("laminas-mvc", "Laminas MVC", "PHP", "laminas/laminas-mvc", "https://docs.laminas.dev/laminas-mvc/", "Zend Framework後継のenterprise PHP MVC component。", "長期PHP enterprise codebaseをcomponent-basedに維持する。", ("MVC", "Service manager", "Modules"), ("legacy migration path", "mature components"), ("complexity", "new-project momentum"), ("symfony", "mezzio", "laravel")),
    ("octobercms", "October CMS", "PHP", "octobercms/october", "https://octobercms.com/", "Laravel上のdeveloper-oriented CMS platform。", "Laravel skillsでcontent-managed siteとpluginを構築する。", ("Laravel-based", "CMS", "Plugin architecture"), ("developer friendly", "visual/editor tools"), ("license/edition確認", "Laravel version coupling"), ("wordpress", "craft-cms", "strapi")),
    ("sylius", "Sylius", "PHP", "Sylius/Sylius", "https://sylius.com/", "Symfony components上のheadless/customizable e-commerce framework。", "commerce domain componentを組み合わせてcustom shopを構築する。", ("Symfony", "DDD-oriented", "Headless"), ("customization", "modular commerce"), ("implementation complexity", "requires Symfony expertise"), ("medusajs", "saleor", "magento")),
])

add_standard_rows("web-framework", ["web-backend", "ruby"], [
    ("sinatra", "Sinatra", "Ruby", "sinatra/sinatra", "https://sinatrarb.com/", "DSL routingを中心にするRuby microframework。", "small Web serviceを最小codeで作る。", ("Routing DSL", "Rack", "Minimal"), ("simple", "embedding"), ("large app conventions absent", "manual assembly"), ("rails", "hanami", "roda")),
    ("hanami", "Hanami", "Ruby", "hanami/hanami", "https://hanamirb.org/", "modularity、explicit dependencies、clean architectureを重視するRuby framework。", "Railsより疎結合でtestableなRuby applicationを構築する。", ("Explicit architecture", "Slices", "Dependency injection"), ("clear boundaries", "modular"), ("smaller ecosystem", "more concepts"), ("rails", "roda", "dry-rb")),
    ("roda", "Roda", "Ruby", "jeremyevans/roda", "https://roda.jeremyevans.net/", "routing treeとpluginで構成するRuby Web framework。", "routing performanceとsmall composable coreを提供する。", ("Routing tree", "Plugins", "Rack"), ("fast", "flexible"), ("ecosystem smaller", "less convention"), ("sinatra", "rails", "hanami")),
    ("grape", "Grape", "Ruby", "ruby-grape/grape", "https://www.ruby-grape.org/", "Rack上のREST-like API microframework。", "Rubyでversioned、validated APIを簡潔に記述する。", ("API DSL", "Validation", "Mountable"), ("Rails integration", "concise APIs"), ("full-stack absent", "DSL complexity"), ("rails-api", "sinatra", "roda")),
])

add_standard_rows("web-framework", ["web-backend", "dotnet"], [
    ("abp", "ABP Framework", "C#", "abpframework/abp", "https://abp.io/", "DDD、multi-tenancy、module、authorizationを統合するASP.NET Core application framework。", "enterprise SaaSのcross-cutting concernsをmodule化する。", ("Modular monolith", "DDD", "Multi-tenancy"), ("enterprise features", "code generation ecosystem"), ("large abstraction surface", "edition/service coupling"), ("aspnet-core", "aspnet-boilerplate", "orleans")),
    ("aspnet-boilerplate", "ASP.NET Boilerplate", "C#", "aspnetboilerplate/aspnetboilerplate", "https://aspnetboilerplate.com/", "ABP Frameworkの前身となるmulti-layer enterprise application framework。", "authorization、audit、tenant等を再利用する。", ("Layered architecture", "DDD", "Cross-cutting services"), ("legacy enterprise support", "feature-rich"), ("superseded direction", "complexity"), ("abp", "aspnet-core", "orchard-core"), "maintenance"),
    ("orchard-core", "Orchard Core", "C#", "OrchardCMS/OrchardCore", "https://orchardcore.net/", "modular multi-tenant application frameworkとCMS。", "ASP.NET Coreでpluggable SaaS/CMSを構築する。", ("Modules", "Multi-tenancy", "CMS"), ("modular architecture", "content management"), ("learning curve", "complex setup"), ("umbraco", "strapi", "abp")),
    ("umbraco", "Umbraco CMS", "C#", "umbraco/Umbraco-CMS", "https://umbraco.com/", ".NET上のeditor-friendly open-source CMS。", "content editorと.NET extensibilityを両立する。", ("CMS", "Extensible", "ASP.NET Core"), ("editor experience", ".NET ecosystem"), ("CMS-specific architecture", "upgrade planning"), ("orchard-core", "sitecore", "wordpress")),
    ("servicestack", "ServiceStack", "C#", "ServiceStack/ServiceStack", "https://servicestack.net/", "typed services、serialization、ORM、authを統合する.NET framework。", "DTO-first service developmentとclient generationを一体化する。", ("Message-based services", "Typed clients", "Integrated stack"), ("productive", "fast serializers"), ("commercial licensing aspects", "opinionated ecosystem"), ("aspnet-core", "nancy", "grpc-dotnet")),
    ("nancy", "Nancy", "C#", "NancyFx/Nancy", "https://github.com/NancyFx/Nancy", "Sinatra-inspired lightweight .NET Web framework。", "low-ceremony HTTP applicationを.NETで作る。", ("DSL routes", "Self-host", "Minimal"), ("historical influence", "simple API"), ("archived", "not for new production"), ("aspnet-core", "servicestack"), "archived"),
    ("giraffe", "Giraffe", "F#", "giraffe-fsharp/Giraffe", "https://giraffe.wiki/", "ASP.NET Core上でfunctional HttpHandler compositionを提供するF# framework。", "F# function compositionでWeb applicationを構築する。", ("Functional handlers", "ASP.NET Core", "Computation expressions"), ("F# idiomatic", "interop"), ("smaller ecosystem", "functional learning"), ("saturn", "falco", "aspnet-core")),
    ("saturn", "Saturn", "F#", "SaturnFramework/Saturn", "https://saturnframework.org/", "Giraffe上にMVC、DI、routing DSLを追加するF# Web framework。", "Rails-like productivityをfunctional .NETへ提供する。", ("Computation expression DSL", "Giraffe", "MVC"), ("rapid F# development", "clear routing"), ("community size", "layered abstractions"), ("giraffe", "falco", "aspnet-core")),
    ("falco", "Falco", "F#", "pimbrouwers/Falco", "https://www.falcoframework.com/", "toolkit-firstでhigh-performanceなF# Web framework。", "minimal functional handlersでASP.NET Coreを利用する。", ("Functional", "Minimal", "ASP.NET Core"), ("small", "F# idiomatic"), ("ecosystem size", "full-stack absent"), ("giraffe", "saturn", "aspnet-core")),
])

add_standard_rows("web-framework", ["web-backend", "functional-programming"], [
    ("plug", "Plug", "Elixir", "elixir-plug/plug", "https://hexdocs.pm/plug/readme.html", "connection transformation pipelineを定義するElixir Web specification/toolkit。", "Web serverとapplicationをcomposable functionで接続する。", ("Functional pipeline", "Adapter specification", "Composable plugs"), ("Phoenix基盤", "simple contracts"), ("full-stackではない", "BEAM knowledge"), ("phoenix", "cowboy", "bandit")),
    ("phoenix-liveview", "Phoenix LiveView", "Elixir", "phoenixframework/phoenix_live_view", "https://hexdocs.pm/phoenix_live_view/", "server stateとHTML diffをpersistent connectionで同期するPhoenix UI framework。", "大量client JavaScriptを書かずrich real-time UIを構築する。", ("Server-driven UI", "Stateful process", "DOM patches"), ("Elixir/Phoenix統合", "real-time forms"), ("long-lived server state", "offline/client-heavy use cases"), ("hotwire", "htmx", "blazor-server")),
    ("nerves", "Nerves", "Elixir", "nerves-project/nerves", "https://nerves-project.org/", "BEAM/Elixir applicationをembedded Linux firmwareとして構築するframework。", "fault-tolerant networked deviceをElixirで開発・updateする。", ("Embedded Linux", "BEAM", "Firmware tooling"), ("supervision on devices", "reproducible images"), ("Linux-capable hardware required", "ecosystem niche"), ("zephyr", "balena", "yocto")),
    ("chicago-boss", "Chicago Boss", "Erlang", "ChicagoBoss/ChicagoBoss", "https://github.com/ChicagoBoss/ChicagoBoss", "Rails-inspired Erlang Web framework。", "Erlang/OTPでconvention-driven Web appを作る。", ("MVC", "OTP", "Convention"), ("historical BEAM framework", "rapid development"), ("maintenance status", "Phoenix ecosystemに移行"), ("phoenix", "nitrogen"), "maintenance"),
    ("nitrogen", "Nitrogen", "Erlang", "nitrogen/nitrogen", "https://nitrogenproject.com/", "event-driven component-based Erlang Web framework。", "server-side Erlangでinteractive Web UIを構築する。", ("Server-side events", "Components", "Comet/Ajax"), ("BEAM integration", "rapid UI"), ("niche ecosystem", "modern frontend interoperability"), ("phoenix-liveview", "chicago-boss")),
    ("ring", "Ring", "Clojure", "ring-clojure/ring", "https://github.com/ring-clojure/ring", "HTTP request/response mapとhandler functionを定義するClojure Web abstraction。", "server adapterとmiddleware/applicationをsmall data contractで分離する。", ("Data maps", "Handler functions", "Middleware"), ("simple", "composable"), ("full-stack absent", "assembly required"), ("reitit", "compojure", "pedestal")),
    ("compojure", "Compojure", "Clojure", "weavejester/compojure", "https://github.com/weavejester/compojure", "Ring上のrouting DSL。", "Clojure functionとしてroutesを簡潔に定義する。", ("Routing DSL", "Ring", "Macros"), ("concise", "functional"), ("routing focused", "newer alternatives"), ("reitit", "pedestal", "luminus")),
    ("reitit", "Reitit", "Clojure", "metosin/reitit", "https://cljdoc.org/d/metosin/reitit/", "data-drivenで高速なClojure/Script router framework。", "routes、coercion、middleware、OpenAPIをdataとして統合する。", ("Data-driven routes", "Coercion", "Multi-platform"), ("fast", "API tooling"), ("metadata complexity", "ecosystem specialization"), ("compojure", "pedestal", "bidi")),
    ("pedestal", "Pedestal", "Clojure", "pedestal/pedestal", "https://pedestal.io/", "interceptor queueとservice mapでClojure Web/APIを構築するframework。", "cross-cutting request processingをdata-driven interceptor chainへ分離する。", ("Interceptors", "Service maps", "Async"), ("explicit pipeline", "enterprise use"), ("learning model", "smaller community"), ("reitit", "ring", "luminus")),
    ("luminus", "Luminus", "Clojure", "luminus-framework/luminus-template", "https://luminusweb.com/", "Clojure Web librariesを選択可能なproject templateとして統合するmicro-framework。", "Ring ecosystemの部品選定とproject setupを標準化する。", ("Template-driven", "Composable libraries", "Profiles"), ("practical stack", "Clojure ecosystem integration"), ("template versioning", "not a single runtime framework"), ("duct", "pedestal", "reitit")),
    ("duct", "Duct", "Clojure", "duct-framework/duct", "https://github.com/duct-framework/duct", "Integrant configurationを中心にmodular Clojure Web applicationを構築するframework。", "componentsとconfigurationをdataで組み立てる。", ("Integrant", "Configuration as data", "Modules"), ("modular", "REPL workflow"), ("learning ecosystem", "smaller docs"), ("luminus", "pedestal", "component")),
    ("yesod", "Yesod", "Haskell", "yesodweb/yesod", "https://www.yesodweb.com/", "type-safe routes、templates、forms、persistentを統合するHaskell Web framework。", "compile-time safetyをWeb URL、HTML、databaseへ拡張する。", ("Type-safe URLs", "Hamlet templates", "Persistent"), ("strong correctness", "full-stack"), ("Haskell learning curve", "compile complexity"), ("servant", "scotty", "ihp")),
    ("servant", "Servant", "Haskell", "haskell-servant/servant", "https://www.servant.dev/", "APIをtype-level DSLで記述しserver/client/docsを導出するHaskell framework。", "一つの型付きAPI specificationから複数artifactを生成する。", ("Type-level API", "Combinators", "Generated clients"), ("contract consistency", "composable"), ("advanced types", "error messages"), ("yesod", "scotty", "spock-haskell")),
    ("scotty", "Scotty", "Haskell", "scotty-web/scotty", "https://github.com/scotty-web/scotty", "Sinatra-inspired Haskell microframework。", "small Web serviceをsimple routing DSLで作る。", ("Routing DSL", "WAI", "Minimal"), ("easy Haskell Web", "small"), ("limited full-stack", "effect integration choices"), ("servant", "yesod", "spock-haskell")),
    ("ihp", "IHP", "Haskell", "digitallyinduced/ihp", "https://ihp.digitallyinduced.com/", "type-safe full-stack Haskell Web framework with code generation and LiveReload。", "Haskellの安全性とRails-like productivityを両立する。", ("Convention", "Type safety", "Integrated dev environment"), ("rapid Haskell full-stack", "database tooling"), ("opinionated", "small ecosystem"), ("yesod", "rails", "servant")),
    ("dream", "Dream", "OCaml", "aantron/dream", "https://aantron.github.io/dream/", "simple type-safe OCaml Web framework。", "HTTP server、routing、middlewareをminimal OCaml APIで提供する。", ("Middleware", "Typed", "Async"), ("small API", "OCaml integration"), ("ecosystem size", "full-stack absent"), ("opium", "eliom", "cohttp")),
    ("opium", "Opium", "OCaml", "rgrinberg/opium", "https://github.com/rgrinberg/opium", "Sinatra-like OCaml Web framework。", "small OCaml Web applicationをrouting/middlewareで構築する。", ("Routing", "Middleware", "Lwt"), ("simple", "typed"), ("maintenance/activity", "small ecosystem"), ("dream", "eliom")),
    ("eliom", "Eliom", "OCaml", "ocsigen/eliom", "https://ocsigen.org/eliom/", "client/server OCaml codeを統合するtierless Web framework。", "type-safe client-server boundaryとshared codeを提供する。", ("Tierless", "Typed RPC", "OCaml to JS"), ("end-to-end types", "research-rich design"), ("specialized tooling", "ecosystem niche"), ("dream", "reason-react", "urweb")),
    ("genie", "Genie", "Julia", "GenieFramework/Genie.jl", "https://genieframework.com/", "Julia full-stack Web frameworkとdata app ecosystem。", "scientific Julia codeをWeb API/UIとして提供する。", ("MVC", "Julia", "Reactive UI ecosystem"), ("Julia integration", "rapid data apps"), ("ecosystem size", "deployment knowledge"), ("dash", "streamlit", "oxygen-jl")),
    ("oxygen-jl", "Oxygen.jl", "Julia", "OxygenFramework/Oxygen.jl", "https://github.com/OxygenFramework/Oxygen.jl", "lightweight Julia Web/API framework。", "Julia functionをHTTP endpointへ簡潔に公開する。", ("Routing macros", "Julia", "Minimal"), ("simple API", "scientific integration"), ("young ecosystem", "full-stack absent"), ("genie", "http-jl")),
    ("plumber", "plumber", "R", "rstudio/plumber", "https://www.rplumber.io/", "R function annotationからWeb APIを生成するframework。", "analysis/model codeをHTTP serviceとして公開する。", ("Annotation routes", "R", "OpenAPI"), ("R code reuse", "easy APIs"), ("production scaling", "general Web features limited"), ("shiny", "vetiver", "fiery")),
    ("dash", "Dash", "Python", "plotly/dash", "https://dash.plotly.com/", "Plotly componentとreactive callbackでanalytical Web appを構築するframework。", "Python/R data visualizationをinteractive dashboardへする。", ("Reactive callbacks", "Plotly", "Component tree"), ("rich charts", "data app ecosystem"), ("callback graph complexity", "custom frontend limits"), ("streamlit", "shiny", "panel")),
    ("panel", "Panel", "Python", "holoviz/panel", "https://panel.holoviz.org/", "Python objects、widgets、visualizationをdashboard/appへ組み立てるHoloViz framework。", "notebook/data ecosystemをdeployable interactive appへする。", ("Reactive parameters", "Multiple plotting libs", "Server/static"), ("scientific ecosystem", "flexible layouts"), ("complex dependency graph", "smaller community"), ("streamlit", "dash", "voila")),
])

add_standard_rows("web-framework", ["web-backend", "systems-languages"], [
    ("drogon", "Drogon", "C++", "drogonframework/drogon", "https://drogon.org/", "async high-performance C++ Web application framework。", "C++でfull-featured HTTP/WebSocket/ORM serviceを構築する。", ("Async", "ORM", "Controllers"), ("performance", "feature-rich"), ("C++ build complexity", "memory safety responsibility"), ("oatpp", "crow", "pistache")),
    ("crow", "Crow", "C++", "CrowCpp/Crow", "https://crowcpp.org/", "Flask-like routingを持つC++ microframework。", "concise C++ HTTP APIを作る。", ("Routing macros", "Header-oriented", "WebSocket"), ("simple", "fast"), ("C++ ecosystem integration", "full-stack absent"), ("drogon", "oatpp", "restinio")),
    ("oatpp", "oat++", "C++", "oatpp/oatpp", "https://oatpp.io/", "object mapping、API controller、OpenAPIを備えるC++ Web framework。", "typed C++ service contractとserializationを統合する。", ("Object mapping", "Codegen macros", "Async options"), ("typed APIs", "modular"), ("macro/build complexity", "community size"), ("drogon", "crow", "pistache")),
    ("pistache", "Pistache", "C++", "pistacheio/pistache", "https://pistacheio.github.io/pistache/", "modern C++ REST framework。", "low-level controlを保ちながらHTTP serviceを構築する。", ("REST", "Async", "C++"), ("native performance", "clear API"), ("maintenance maturity", "feature set"), ("drogon", "oatpp", "crow")),
    ("restinio", "RESTinio", "C++", "Stiffstream/restinio", "https://stiffstream.com/en/products/restinio.html", "Asioベースのembedded C++ HTTP/WebSocket server framework。", "C++ applicationへHTTP endpointを組み込む。", ("Asio", "Embedded server", "WebSocket"), ("control", "performance"), ("manual assembly", "smaller ecosystem"), ("oatpp", "drogon", "boost-beast")),
    ("wt", "Wt", "C++", "emweb/wt", "https://www.webtoolkit.eu/wt", "C++ widget modelからserver-side Web applicationを生成するframework。", "desktop GUI風component modelでWeb UIを構築する。", ("Server-side widgets", "C++", "Stateful sessions"), ("single language", "rich widgets"), ("server resource cost", "licensing considerations"), ("qt", "vaadin-flow", "blazor")),
    ("ulfius", "Ulfius", "C", "babelouest/ulfius", "https://github.com/babelouest/ulfius", "C向けHTTP framework。", "embedded/native C applicationにREST/WebSocket endpointを追加する。", ("C", "REST", "WebSocket"), ("small native integration", "portable"), ("manual memory safety", "smaller ecosystem"), ("libmicrohttpd", "civetweb", "onion")),
    ("facil-io", "facil.io", "C", "boazsegev/facil.io", "https://facil.io/", "evented C Web application framework。", "high-concurrency HTTP/WebSocket servicesをCで構築する。", ("Evented I/O", "WebSocket", "C"), ("performance", "low-level"), ("memory safety", "maintenance/activity"), ("ulfius", "libevent", "civetweb")),
    ("vibe-d", "vibe.d", "D", "vibe-d/vibe.d", "https://vibed.org/", "D言語のasync I/O、Web、serialization framework。", "Dでhigh-performance network/Web applicationを作る。", ("Async", "D", "Web framework"), ("language integration", "broad features"), ("D ecosystem size", "maintenance"), ("hunt-framework", "arsd")),
    ("hunt-framework", "Hunt Framework", "D", "huntlabs/hunt-framework", "https://github.com/huntlabs/hunt-framework", "D向けhigh-performance Web framework。", "enterprise-style D Web applicationを構築する。", ("Async", "MVC", "DI"), ("feature-rich", "D performance"), ("small community", "documentation"), ("vibe-d",)),
    ("kemal", "Kemal", "Crystal", "kemalcr/kemal", "https://kemalcr.com/", "Sinatra-inspired Crystal Web framework。", "compiled Crystalでsmall Web APIを簡潔に作る。", ("Routing DSL", "Middleware", "Crystal"), ("fast", "simple"), ("ecosystem size", "full-stack absent"), ("lucky", "amber")),
    ("lucky", "Lucky", "Crystal", "luckyframework/lucky", "https://luckyframework.org/", "type-safe full-stack Crystal Web framework。", "compile-time safetyとproductive conventionsを両立する。", ("Type safety", "Full-stack", "Code generation"), ("safe HTML/queries", "integrated tooling"), ("small ecosystem", "compile times"), ("kemal", "amber")),
    ("amber", "Amber", "Crystal", "amberframework/amber", "https://amberframework.org/", "MVC、ORM、generatorを持つCrystal Web framework。", "Rails-like productivityをCrystalへ提供する。", ("MVC", "ORM", "Generators"), ("rapid compiled Web", "familiar architecture"), ("maintenance momentum", "small ecosystem"), ("lucky", "kemal")),
    ("jester", "Jester", "Nim", "dom96/jester", "https://github.com/dom96/jester", "Sinatra-like Nim Web framework。", "Nimでsmall fast HTTP applicationを作る。", ("Routing DSL", "Async", "Nim"), ("simple", "native binary"), ("small ecosystem", "full-stack absent"), ("prologue", "happyx")),
    ("prologue", "Prologue", "Nim", "planety/prologue", "https://planety.github.io/prologue/", "async、middleware、sessionを備えるNim Web framework。", "Nimでstructured Web applicationを構築する。", ("Async", "Middleware", "Nim"), ("ergonomic", "native performance"), ("ecosystem size", "documentation depth"), ("jester", "happyx")),
    ("jetzig", "Jetzig", "Zig", "jetzig-framework/jetzig", "https://jetzig.dev/", "Zig向けfull-stack Web framework。", "Zigのperformanceとcompile-time featuresでWeb appを構築する。", ("Zig", "Routing", "Templates"), ("native performance", "integrated development"), ("very young", "ecosystem/toolchain churn"), ("http-zig", "zap")),
    ("zap", "zap", "Zig", "zigzap/zap", "https://github.com/zigzap/zap", "facil.ioを利用するZig Web framework。", "Zigでhigh-performance HTTP/WebSocket serviceを作る。", ("Zig", "facil.io", "HTTP/WebSocket"), ("performance", "small API"), ("C dependency", "young ecosystem"), ("jetzig", "http-zig")),
])

add_standard_rows("ui-framework", ["web-frontend", "ui"], [
    ("preact", "Preact", "TypeScript", "preactjs/preact", "https://preactjs.com/", "React-like APIを小さなruntimeで提供するUI library。", "React component modelをsize-sensitive Webへ適用する。", ("Small runtime", "Virtual DOM", "React compatibility layer"), ("small bundles", "familiar API"), ("compatibility edge cases", "smaller ecosystem"), ("react", "solidjs", "inferno")),
    ("lit", "Lit", "TypeScript", "lit/lit", "https://lit.dev/", "standards-based Web Componentsをreactive templateで構築するlibrary。", "custom elementのboilerplateとefficient updateを減らす。", ("Web Components", "Tagged templates", "Reactive properties"), ("standards-based", "framework-neutral components"), ("application routing/stateは別", "shadow DOM styling concepts"), ("stencil", "haunted", "native-web-components")),
    ("stencil", "Stencil", "TypeScript", "ionic-team/stencil", "https://stenciljs.com/", "Web Componentsをcompilerで生成するtoolchain/framework。", "framework-neutral design system componentをTypeScript/JSXで作る。", ("Compiler", "Web Components", "JSX"), ("cross-framework components", "lazy loading"), ("compiler/toolchain", "app frameworkではない"), ("lit", "svelte", "solid-element")),
    ("alpinejs", "Alpine.js", "JavaScript", "alpinejs/alpine", "https://alpinejs.dev/", "HTML attributesでsmall interactive behaviorを追加するlightweight framework。", "server-rendered HTMLへ低costなreactivityを加える。", ("HTML-first", "Declarative attributes", "Small"), ("progressive enhancement", "low setup"), ("large SPA stateに不向き", "markup logicが増える"), ("htmx", "stimulus", "petite-vue")),
    ("htmx", "htmx", "JavaScript", "bigskysoftware/htmx", "https://htmx.org/", "HTML attributesからHTTP requestを発行しserver-returned HTMLでDOMを更新するlibrary/framework。", "SPA JavaScriptなしにdynamic hypermedia interactionを作る。", ("Hypermedia", "HTML over the wire", "Progressive enhancement"), ("small client", "server framework agnostic"), ("complex client stateに制約", "server fragment design"), ("hotwire", "alpinejs", "unpoly")),
    ("hotwire", "Hotwire", "JavaScript", "hotwired/hotwire-rails", "https://hotwired.dev/", "TurboとStimulusでHTML-over-the-wireとmodest JavaScriptを実現するWeb approach/framework family。", "server-rendered appにSPA-like navigationとpartial updatesを追加する。", ("HTML over the wire", "Turbo frames/streams", "Modest JS"), ("Rails integration", "less client state"), ("server coupling", "offline-rich appに不向き"), ("htmx", "phoenix-liveview", "unpoly")),
    ("stimulus", "Stimulus", "JavaScript", "hotwired/stimulus", "https://stimulus.hotwired.dev/", "existing HTMLへcontroller behaviorを付与するmodest JavaScript framework。", "server-rendered markupを置き換えずinteractionを構造化する。", ("HTML annotations", "Controllers", "Progressive enhancement"), ("small and explicit", "server HTML friendly"), ("complex client state not primary", "controller proliferation"), ("alpinejs", "lit", "vanilla-js")),
    ("backbone", "Backbone.js", "JavaScript", "jashkenas/backbone", "https://backbonejs.org/", "models、collections、views、routerを小さく提供した初期SPA library。", "jQuery-era applicationにclient-side structureを与える。", ("Models/collections", "Events", "Router"), ("historically influential", "small"), ("manual DOM/state sync", "maintenance-mode usage"), ("angularjs", "ember", "marionette"), "maintenance"),
    ("knockout", "Knockout", "JavaScript", "knockout/knockout", "https://knockoutjs.com/", "observableとdeclarative bindingを使うMVVM JavaScript library。", "model-view synchronizationを手作業から解放する。", ("Observables", "MVVM", "Two-way bindings"), ("simple data binding", "historical importance"), ("large app structure absent", "modern ecosystem smaller"), ("vue", "angularjs", "mobx"), "maintenance"),
    ("aurelia", "Aurelia", "TypeScript", "aurelia/aurelia", "https://aurelia.io/", "standards-oriented、DI、templating、routingを備えるWeb application framework。", "clean conventionsとnative-like syntaxでSPAを構築する。", ("Convention", "Dependency injection", "Standards-oriented"), ("clean templates", "full framework"), ("ecosystem size", "v1/v2 distinctions"), ("angular", "vue", "ember")),
    ("mithril", "Mithril.js", "JavaScript", "MithrilJS/mithril.js", "https://mithril.js.org/", "small virtual DOM、routing、XHRを統合するUI framework。", "small dependencyでSPAに必要な中心機能を提供する。", ("Small", "Virtual DOM", "Integrated router"), ("tiny", "fast"), ("ecosystem small", "less tooling"), ("preact", "hyperapp", "riot")),
    ("riot", "Riot.js", "JavaScript", "riot/riot", "https://riot.js.org/", "custom tag/component syntaxを持つlightweight UI framework。", "少ないAPIでcomponent-based UIを作る。", ("Custom components", "Compiler", "Small runtime"), ("simple", "compact"), ("small ecosystem", "toolchain differences"), ("vue", "mithril", "svelte")),
    ("hyperapp", "Hyperapp", "JavaScript", "hyperapp/hyperapp", "https://github.com/jorgebucaran/hyperapp", "Elm-like state/action/viewを極小runtimeで提供するUI library。", "small functional application architectureをJavaScriptで実現する。", ("Elm-like", "Tiny", "Functional state"), ("very small", "predictable"), ("minimal ecosystem", "manual integrations"), ("elm", "redux", "mithril")),
    ("cyclejs", "Cycle.js", "TypeScript", "cyclejs/cyclejs", "https://cycle.js.org/", "applicationをsourcesからsinksへのreactive dataflowとして記述するframework。", "side effectsをdriver境界へ分離する。", ("Functional reactive", "Drivers", "Streams"), ("explicit effects", "composable"), ("FRP learning curve", "small community"), ("elm", "rxjs", "react")),
    ("marko", "Marko", "JavaScript", "marko-js/marko", "https://markojs.com/", "eBay発のcompiler-based UI framework with streaming SSR and partial hydration/resumability research。", "large commerce pagesを高速にserver renderし必要箇所だけinteractiveにする。", ("Compiler", "Streaming", "Fine-grained updates"), ("performance", "production lineage"), ("ecosystem small", "tooling specialization"), ("svelte", "qwik", "react")),
    ("inferno", "Inferno", "TypeScript", "infernojs/inferno", "https://www.infernojs.org/", "performance-focused React-like virtual DOM library。", "React-like UIをsmall fast runtimeで実行する。", ("Virtual DOM", "React-like", "Performance"), ("fast", "small"), ("ecosystem/momentum", "compatibility gaps"), ("preact", "react", "solidjs")),
    ("petite-vue", "petite-vue", "TypeScript", "vuejs/petite-vue", "https://github.com/vuejs/petite-vue", "progressive enhancement向けの小さなVue-like runtime。", "server HTMLへVue reactivityを軽量に追加する。", ("Progressive enhancement", "Vue reactivity", "Small"), ("low bundle", "simple"), ("not full Vue", "limited features"), ("alpinejs", "vue", "stimulus")),
    ("ember", "Ember.js duplicate guard", "JavaScript", "", "", "", "", (), (), (), (), "archived-placeholder"),
])
# Remove the intentional duplicate placeholder used to validate seed authoring discipline.
FRAMEWORKS.pop()

add_standard_rows("meta-framework", ["web-fullstack", "web-frontend"], [
    ("sveltekit", "SvelteKit", "TypeScript", "sveltejs/kit", "https://svelte.dev/docs/kit/introduction", "Svelteのrouting、SSR、data loading、forms、adaptersを統合するmeta-framework。", "Svelte applicationをfull-stack/production deploymentへ標準化する。", ("File routing", "SSR", "Adapters"), ("Svelte integration", "Web standards"), ("server/client boundary", "ecosystem size"), ("nextjs", "nuxt", "remix")),
    ("gatsby", "Gatsby", "TypeScript", "gatsbyjs/gatsby", "https://www.gatsbyjs.com/", "ReactとGraphQL data layerを使うstatic/site framework。", "多様なcontent sourceから高速static siteをbuildする。", ("GraphQL data layer", "Static generation", "Plugin ecosystem"), ("content plugins", "historical Jamstack influence"), ("large builds", "project momentum/ownership changes"), ("nextjs", "astro", "eleventy"), "maintenance"),
    ("eleventy", "Eleventy", "JavaScript", "11ty/eleventy", "https://www.11ty.dev/", "template-language agnosticなsimple static site generator。", "contentを小さなbuild systemでHTMLへ変換する。", ("Multiple templates", "Data cascade", "Zero client JS"), ("simple", "flexible"), ("interactive app features separate", "custom build conventions"), ("astro", "hugo", "jekyll")),
    ("docusaurus", "Docusaurus", "TypeScript", "facebook/docusaurus", "https://docusaurus.io/", "documentation site向けReact static site framework。", "versioned docs、search、blog、localizationを標準化する。", ("Docs-first", "Versioning", "React"), ("documentation features", "plugin ecosystem"), ("general app not primary", "React build stack"), ("mkdocs", "vitepress", "nextra")),
    ("vitepress", "VitePress", "TypeScript", "vuejs/vitepress", "https://vitepress.dev/", "ViteとVueを使うdocumentation-focused static site generator。", "Markdown docsを高速dev/buildでsite化する。", ("Markdown", "Vite", "Vue themes"), ("fast", "simple docs"), ("custom app features limited", "Vue-specific"), ("docusaurus", "mkdocs", "nextra")),
    ("nextra", "Nextra", "TypeScript", "shuding/nextra", "https://nextra.site/", "Next.js上のMarkdown/MDX documentation framework。", "React/Next.js ecosystemでdocs/blogを構築する。", ("MDX", "Next.js", "Themes"), ("React component embedding", "modern docs"), ("Next.js coupling", "theme conventions"), ("docusaurus", "vitepress", "fumadocs")),
    ("tanstack-start", "TanStack Start", "TypeScript", "TanStack/router", "https://tanstack.com/start/latest", "TanStack Routerを中心にfull-stack React applicationを構築するframework。", "type-safe routing/data loadingとserver functionsを統合する。", ("Type-safe routing", "Server functions", "Vite"), ("strong types", "router integration"), ("young framework", "ecosystem churn"), ("nextjs", "remix", "redwoodjs")),
    ("analog", "Analog", "TypeScript", "analogjs/analog", "https://analogjs.org/", "Angular向けVite-based full-stack meta-framework。", "Angularにfile routing、SSR、content、server endpointsを追加する。", ("Angular", "Vite", "File routing"), ("Angular full-stack", "modern tooling"), ("young ecosystem", "Angular updates"), ("angular", "nextjs", "nuxt")),
    ("quasar", "Quasar Framework", "TypeScript", "quasarframework/quasar", "https://quasar.dev/", "Vue componentとCLIでSPA、SSR、PWA、mobile、desktopをbuildするframework。", "一つのVue codebaseを多数platformへ展開する。", ("Vue", "Multi-mode build", "UI components"), ("broad targets", "integrated UI"), ("large framework", "platform-specific tradeoffs"), ("ionic", "nuxt", "vuetify")),
    ("umi", "Umi", "TypeScript", "umijs/umi", "https://umijs.org/", "enterprise React application向けrouting、build、plugin framework。", "large React projectのconventionsとtoolingを統一する。", ("Plugin system", "Convention routing", "Enterprise presets"), ("integrated tooling", "China ecosystem"), ("global docs/community gap", "opinionated"), ("nextjs", "ice", "modernjs")),
    ("modernjs", "Modern.js", "TypeScript", "web-infra-dev/modern.js", "https://modernjs.dev/", "ByteDance発のmodern Web engineering meta-framework/toolchain。", "React application、SSR、module、monorepoを統一する。", ("Modular solutions", "Rspack ecosystem", "Full-stack"), ("large-scale tooling", "performance"), ("ecosystem complexity", "regional adoption"), ("nextjs", "umi", "nx")),
    ("icejs", "ICE.js", "TypeScript", "alibaba/ice", "https://v3.ice.work/", "Alibaba発のReact application framework。", "enterprise frontendのrouting、data、buildを規約化する。", ("React", "Convention", "Enterprise"), ("integrated stack", "plugin ecosystem"), ("documentation/version shifts", "regional ecosystem"), ("umi", "nextjs", "modernjs")),
])

add_standard_rows("ui-framework", ["mobile", "desktop", "cross-platform"], [
    ("dotnet-maui", ".NET MAUI", "C#", "dotnet/maui", "https://dotnet.microsoft.com/apps/maui", "C#とXAMLでAndroid、iOS、macOS、Windows appを構築するcross-platform framework。", "Xamarin.Forms系譜を統一.NET toolchainへ移行する。", ("Single project", "Native controls", "XAML"), (".NET sharing", "native access"), ("platform/tooling differences", "app size"), ("flutter", "react-native", "avalonia")),
    ("xamarin-forms", "Xamarin.Forms", "C#", "xamarin/Xamarin.Forms", "https://github.com/xamarin/Xamarin.Forms", "C#/XAML cross-platform mobile UI framework。.NET MAUIへ移行済み。", "iOS/Android間でUIとlogicを共有する。", ("Native renderers", "XAML", "Shared code"), ("historical .NET mobile base", "native APIs"), ("support ended", "migration required"), ("dotnet-maui", "flutter", "react-native"), "superseded"),
    ("avalonia", "Avalonia", "C#", "AvaloniaUI/Avalonia", "https://avaloniaui.net/", "cross-platform .NET desktop UI framework with XAML and own rendering。", "WPF-like architectureをWindows以外へ拡張する。", ("XAML", "Own renderer", "MVVM"), ("cross-platform .NET", "WPF familiarity"), ("platform integration gaps", "ecosystem smaller than WPF"), ("wpf", "uno-platform", "qt")),
    ("uno-platform", "Uno Platform", "C#", "unoplatform/uno", "https://platform.uno/", "WinUI APIをWebAssembly、mobile、desktopへ展開するcross-platform framework。", "Windows UI codeとskillsを複数platformで再利用する。", ("WinUI-compatible", "Multi-platform", "XAML"), ("Microsoft stack reuse", "WebAssembly target"), ("compatibility matrix", "large toolchain"), ("avalonia", "dotnet-maui", "flutter")),
    ("wpf", "Windows Presentation Foundation", "C#", "dotnet/wpf", "https://learn.microsoft.com/dotnet/desktop/wpf/", "XAML、binding、retained-mode graphicsを備えるWindows desktop UI framework。", "rich Windows desktop UIとdata bindingを統合する。", ("XAML", "Dependency properties", "Data binding"), ("mature Windows ecosystem", "rich controls"), ("Windows-only", "legacy patterns/complexity"), ("winui", "avalonia", "qt")),
    ("winui", "WinUI", "C++", "microsoft/microsoft-ui-xaml", "https://learn.microsoft.com/windows/apps/winui/", "modern Windows application向けnative UI framework。", "Windows design systemと最新UI controlをOS releaseから一部分離して提供する。", ("Windows App SDK", "XAML", "Native"), ("modern Windows integration", "official"), ("Windows-only", "deployment/tooling complexity"), ("wpf", "avalonia", "uno-platform")),
    ("javafx", "JavaFX / OpenJFX", "Java", "openjdk/jfx", "https://openjfx.io/", "Java desktop UI、scene graph、CSS、media framework。", "modern rich clientをJavaでcross-platformに構築する。", ("Scene graph", "FXML", "CSS"), ("Java ecosystem", "hardware-accelerated UI"), ("desktop distribution", "ecosystem smaller than Web"), ("swing", "qt", "compose-multiplatform")),
    ("swing", "Java Swing", "Java", "openjdk/jdk", "https://docs.oracle.com/javase/tutorial/uiswing/", "JDK標準のretained-mode desktop GUI toolkit。", "platform-independent Java desktop UIを提供する。", ("Widgets", "Event dispatch thread", "Pluggable look and feel"), ("ubiquitous legacy", "no extra dependency"), ("aging UI model", "threading pitfalls"), ("javafx", "swt", "compose-multiplatform"), "maintenance"),
    ("compose-multiplatform", "Compose Multiplatform", "Kotlin", "JetBrains/compose-multiplatform", "https://www.jetbrains.com/lp/compose-multiplatform/", "Jetpack Compose modelをdesktop、iOS、Webへ拡張するKotlin UI framework。", "Kotlin declarative UIをplatform横断で共有する。", ("Compose", "Kotlin Multiplatform", "Declarative UI"), ("shared UI/code", "JetBrains tooling"), ("target maturity differences", "Kotlin ecosystem"), ("flutter", "jetpack-compose", "dotnet-maui")),
    ("nativescript", "NativeScript", "TypeScript", "NativeScript/NativeScript", "https://nativescript.org/", "JavaScript/TypeScriptからnative UI/APIへdirect accessするmobile framework。", "Web developer languageでnative mobile appを構築する。", ("Native UI", "JS runtime", "Direct native APIs"), ("native controls", "framework integrations"), ("ecosystem size", "native tooling/debug"), ("react-native", "ionic", "flutter")),
    ("capacitor", "Capacitor", "TypeScript", "ionic-team/capacitor", "https://capacitorjs.com/", "Web appをnative containerへ組み込みpluginでdevice APIへ接続するruntime/framework。", "existing Web codebaseをmobile appとして配布する。", ("Web-native bridge", "Plugins", "Native projects"), ("Web reuse", "modern Cordova alternative"), ("WebView limits", "plugin/native work"), ("cordova", "ionic", "tauri")),
    ("cordova", "Apache Cordova", "JavaScript", "apache/cordova", "https://cordova.apache.org/", "WebViewとplugin bridgeでhybrid mobile appを作るframework。", "HTML/JSをnative packageとしてdevice APIへ接続する。", ("WebView", "Plugin bridge", "Cross-platform"), ("historical ecosystem", "Web skill reuse"), ("older architecture", "plugin maintenance"), ("capacitor", "ionic", "nativescript"), "maintenance"),
    ("framework7", "Framework7", "JavaScript", "framework7io/framework7", "https://framework7.io/", "iOS/Android風componentを持つmobile-first Web/hybrid framework。", "native-like mobile UIをWeb technologiesで構築する。", ("Mobile UI", "Router", "Multiple framework integrations"), ("rich components", "PWA/hybrid"), ("native fidelity limits", "large framework"), ("ionic", "onsen-ui", "quasar")),
    ("onsen-ui", "Onsen UI", "JavaScript", "OnsenUI/OnsenUI", "https://onsen.io/", "hybrid/PWA向けmobile UI component framework。", "platform-adaptive mobile UIをWeb technologiesで作る。", ("Web Components", "Adaptive styling", "Hybrid"), ("framework neutral", "mobile components"), ("ecosystem momentum", "WebView limits"), ("ionic", "framework7", "quasar")),
    ("kivy", "Kivy", "Python", "kivy/kivy", "https://kivy.org/", "OpenGL-based cross-platform Python application UI framework。", "Pythonでtouch-oriented desktop/mobile appを構築する。", ("Own widgets", "OpenGL", "Multi-touch"), ("Python-only", "cross-platform"), ("native look differences", "packaging complexity"), ("beeware", "flutter", "pygame")),
    ("beeware", "BeeWare", "Python", "beeware/toga", "https://beeware.org/", "Python codeをnative widget applicationとして複数platformへdeployするtool suite。", "Pythonでnative-looking desktop/mobile appを作る。", ("Native widgets", "Python", "Packaging tools"), ("native controls", "Python reuse"), ("platform coverage maturity", "packaging"), ("kivy", "flutter", "qt-for-python")),
    ("slint", "Slint", "Rust", "slint-ui/slint", "https://slint.dev/", "declarative UI languageとnative rendererを持つdesktop/embedded framework。", "resource-conscious deviceとdesktopにcross-platform UIを提供する。", ("Declarative DSL", "Rust/C++", "Embedded focus"), ("small footprint", "tooling"), ("custom language", "ecosystem size"), ("iced", "egui", "qt")),
    ("iced", "Iced", "Rust", "iced-rs/iced", "https://iced.rs/", "Elm-inspired cross-platform Rust GUI framework。", "message/update/view modelでsafe native GUIを構築する。", ("Elm architecture", "Rust", "Cross-platform"), ("predictable state", "native binary"), ("API evolution", "widget ecosystem"), ("slint", "egui", "druid")),
    ("egui", "egui", "Rust", "emilk/egui", "https://www.egui.rs/", "immediate-mode GUIをnative/Webで提供するRust library/framework。", "tool UIとdebug UIをsmall state modelで迅速に作る。", ("Immediate mode", "Rust", "Native/Wasm"), ("simple dynamic UI", "great for tools"), ("traditional app semantics differ", "accessibility/layout tradeoffs"), ("imgui", "iced", "slint")),
    ("dear-imgui", "Dear ImGui", "C++", "ocornut/imgui", "https://github.com/ocornut/imgui", "immediate-mode GUI library for tools and engine interfaces。", "state synchronization boilerplateなしにdeveloper-facing UIを作る。", ("Immediate mode", "Renderer agnostic", "Tooling UI"), ("easy integration", "mature"), ("not ideal for consumer/accessibility UI", "custom styling"), ("egui", "nuklear", "qt")),
    ("gtk", "GTK", "C", "GNOME/gtk", "https://www.gtk.org/", "GNOME系cross-platform desktop GUI toolkit。", "native-style widgets、accessibility、internationalizationを提供する。", ("Widget toolkit", "GObject", "GNOME"), ("Linux integration", "language bindings"), ("cross-platform polish differences", "GObject model"), ("qt", "wxwidgets", "libadwaita")),
    ("wxwidgets", "wxWidgets", "C++", "wxWidgets/wxWidgets", "https://www.wxwidgets.org/", "native platform controlsをwrapするcross-platform C++ GUI framework。", "one C++ codebaseでnative-looking desktop UIを作る。", ("Native widgets", "C++", "Cross-platform"), ("native appearance", "long history"), ("API age/complexity", "mobile not primary"), ("qt", "gtk", "fltk")),
])

add_standard_rows("game-framework", ["game"], [
    ("monogame", "MonoGame", "C#", "MonoGame/MonoGame", "https://monogame.net/", "XNA-compatible cross-platform game framework。", "C#でgame loop、graphics、input、content pipelineを扱う。", ("XNA API", "Code-first", "Cross-platform"), ("low overhead", "C# ecosystem"), ("editor not integrated", "engine features self-built"), ("unity", "fna", "libgdx")),
    ("libgdx", "libGDX", "Java", "libgdx/libgdx", "https://libgdx.com/", "Java/Kotlin cross-platform game development framework。", "desktop/mobile/Webで2D/3D game codeを共有する。", ("Code-first", "OpenGL", "Multi-platform"), ("lightweight", "mature"), ("editor/tooling separate", "Web target constraints"), ("monogame", "unity", "korge")),
    ("defold", "Defold", "Lua", "defold/defold", "https://defold.com/", "small runtimeとeditorを持つcross-platform game engine。", "mobile/Web向け2D中心gameを効率的にbuildする。", ("Lua", "Component model", "Small runtime"), ("fast builds", "free source-available engine"), ("3D/tool ecosystem smaller", "editor conventions"), ("godot", "love2d", "unity")),
    ("love2d", "LÖVE", "Lua", "love2d/love", "https://love2d.org/", "Luaで2D gameを作るlightweight framework。", "simple callbacksとgraphics/audio/input APIでgame prototypeを作る。", ("Lua", "2D", "Callback loop"), ("easy", "small"), ("editor/scene systemなし", "distribution work"), ("phaser", "defold", "solar2d")),
    ("raylib", "raylib", "C", "raysan5/raylib", "https://www.raylib.com/", "educationとsimple game programming向けC multimedia library/framework。", "minimal dependenciesでgraphics/audio/inputを学び使う。", ("Simple C API", "No editor", "Multi-platform"), ("very lightweight", "many bindings"), ("engine systems self-built", "large game tooling absent"), ("sdl", "love2d", "macroquad")),
    ("macroquad", "Macroquad", "Rust", "not-fl3/macroquad", "https://macroquad.rs/", "simple cross-platform Rust game framework。", "async mainとsmall APIで2D game/Web buildを行う。", ("Rust", "Simple API", "Wasm"), ("easy Rust games", "fast compile relative"), ("engine tooling limited", "small ecosystem"), ("bevy", "raylib", "ggez")),
    ("ebitengine", "Ebitengine", "Go", "hajimehoshi/ebiten", "https://ebitengine.org/", "Goのsimple 2D game engine/framework。", "single Update/Draw modelでdesktop/mobile/Web gameを作る。", ("Go", "2D", "Cross-platform"), ("simple", "pure Go workflow"), ("3D/editor absent", "manual systems"), ("raylib", "love2d", "pixel")),
    ("pygame", "Pygame", "Python", "pygame/pygame", "https://www.pygame.org/", "SDL上のPython multimedia/game library。", "Pythonで2D game programmingを学びprototypeする。", ("Python", "SDL", "2D"), ("beginner friendly", "huge tutorials"), ("performance", "engine systems absent"), ("arcade-python", "panda3d", "godot")),
    ("panda3d", "Panda3D", "C++", "panda3d/panda3d", "https://www.panda3d.org/", "Python/C++ 3D game and simulation engine。", "scriptable 3D rendering、scene、physicsを提供する。", ("Python scripting", "3D", "Scene graph"), ("open source", "simulation use"), ("tooling/visibility smaller", "learning docs"), ("godot", "ursina", "ogre")),
    ("renpy", "Ren'Py", "Python", "renpy/renpy", "https://www.renpy.org/", "visual novel向けscript language、UI、save、distribution engine。", "narrative gameのdialogue、branch、asset管理を標準化する。", ("Narrative DSL", "Python extension", "Cross-platform"), ("genre productivity", "mature"), ("genre-specific", "custom gameplay requires work"), ("ink", "godot", "visual-novel-maker")),
    ("cocos2d-x", "Cocos2d-x", "C++", "cocos2d/cocos2d-x", "https://www.cocos.com/en/cocos2d-x", "cross-platform C++ 2D game framework。", "mobile 2D gameのscene、sprite、animationを共有する。", ("Scene graph", "C++", "Mobile"), ("performance", "historical mobile ecosystem"), ("toolchain/version fragmentation", "community shift to Cocos Creator"), ("cocos-creator", "libgdx", "unity"), "maintenance"),
    ("cocos-creator", "Cocos Creator", "TypeScript", "cocos/cocos-engine", "https://www.cocos.com/en/creator", "editorとTypeScript component modelを持つ2D/3D game engine。", "mobile/Web gameをvisual editorとscriptで構築する。", ("Editor", "TypeScript", "2D/3D"), ("mobile/Web", "integrated workflow"), ("ecosystem regional", "engine upgrades"), ("unity", "godot", "defold")),
    ("babylonjs", "Babylon.js", "TypeScript", "BabylonJS/Babylon.js", "https://www.babylonjs.com/", "WebGL/WebGPU 3D engine for browser experiences。", "browserでscene、materials、physics、XRを統合する。", ("WebGPU/WebGL", "Scene graph", "XR"), ("feature-rich Web 3D", "Microsoft support"), ("bundle/complexity", "browser GPU variance"), ("threejs", "playcanvas", "phaser")),
    ("threejs", "three.js", "JavaScript", "mrdoob/three.js", "https://threejs.org/", "WebGL abstraction and 3D rendering library。", "raw WebGL complexityをscene/camera/material APIで隠す。", ("Scene graph", "WebGL/WebGPU", "Renderer"), ("huge ecosystem", "flexible"), ("game systems absent", "API evolution"), ("babylonjs", "playcanvas", "react-three-fiber")),
    ("playcanvas", "PlayCanvas Engine", "JavaScript", "playcanvas/engine", "https://playcanvas.com/", "Web-first 3D engine with browser editor ecosystem。", "collaborative Web 3D/game developmentを行う。", ("WebGL/WebGPU", "Entity-component", "Cloud editor"), ("browser-native", "collaboration"), ("service/editor coupling", "ecosystem size"), ("babylonjs", "threejs", "unity")),
    ("pixijs", "PixiJS", "TypeScript", "pixijs/pixijs", "https://pixijs.com/", "high-performance 2D Web rendering library。", "Canvas/WebGL/WebGPUのsprite renderingを抽象化する。", ("2D renderer", "GPU", "Scene graph"), ("fast rendering", "large ecosystem"), ("not a full game engine", "game systems separate"), ("phaser", "konva", "threejs")),
    ("flame", "Flame", "Dart", "flame-engine/flame", "https://flame-engine.org/", "Flutter上の2D game engine/framework。", "Flutter/Dart applicationへgame loop、component、collisionを追加する。", ("Flutter", "Component system", "2D"), ("Dart/Flutter reuse", "mobile friendly"), ("Flutter renderer constraints", "small ecosystem"), ("flutter", "ebitengine", "love2d")),
    ("korge", "KorGE", "Kotlin", "korlibs/korge", "https://korge.org/", "Kotlin Multiplatform 2D game engine。", "Kotlin codeをJVM、native、Webへ展開する。", ("Kotlin Multiplatform", "2D", "Coroutines"), ("Kotlin sharing", "multi-target"), ("ecosystem size", "toolchain complexity"), ("libgdx", "flame", "defold")),
    ("solar2d", "Solar2D", "Lua", "coronalabs/corona", "https://solar2d.com/", "Lua-based cross-platform 2D mobile game framework。", "mobile app/gameをsmall Lua codebaseでbuildする。", ("Lua", "2D", "Mobile"), ("easy", "open source"), ("ecosystem momentum", "3D limitations"), ("love2d", "defold", "cocos2d-x")),
    ("fyrox", "Fyrox", "Rust", "FyroxEngine/Fyrox", "https://fyrox.rs/", "editorを持つRust 2D/3D game engine。", "Rustでscene、physics、animation、editor-driven gameを作る。", ("Rust", "Scene graph", "Editor"), ("integrated engine", "open source"), ("young ecosystem", "API evolution"), ("bevy", "godot", "o3de")),
    ("ggez", "ggez", "Rust", "ggez/ggez", "https://ggez.rs/", "LÖVE-inspired Rust 2D game framework。", "simple event loopでRust game programmingを学ぶ。", ("Rust", "2D", "Callback loop"), ("simple", "learning friendly"), ("engine features limited", "ecosystem size"), ("macroquad", "bevy", "love2d")),
])
