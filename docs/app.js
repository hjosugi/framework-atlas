"use strict";

const state = { data: null, filtered: [], invalidFilter: null };
const $ = (selector) => document.querySelector(selector);
const svgNS = "http://www.w3.org/2000/svg";

function element(tag, options = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(options).forEach(([key, value]) => {
    if (key === "className") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (key === "href") node.setAttribute("href", value);
    else node.setAttribute(key, value);
  });
  children.filter(Boolean).forEach((child) => node.append(child));
  return node;
}

function unique(values) { return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b)); }
function label(value) { return String(value).replaceAll("-", " "); }
function entityById(id) { return state.data.entities.find((entity) => entity.id === id); }

function fillSelect(selector, values) {
  const select = $(selector);
  values.forEach((value) => select.append(element("option", { value, text: label(value) })));
}

function syncFiltersFromUrl() {
  const params = new URLSearchParams(location.search);
  state.invalidFilter = null;
  ["search", "kind", "cohort", "profile", "evidence", "disposition"].forEach((id) => {
    const key = id === "search" ? "q" : id;
    if (params.has(key)) {
      const value = params.get(key);
      if (id !== "search" && ![...$(`#${id}`).options].some((option) => option.value === value)) state.invalidFilter = `${key}=${value}`;
      else $(`#${id}`).value = value;
    }
  });
}

function syncUrl(mode = "replace") {
  const params = new URLSearchParams();
  const values = { q: $("#search").value, kind: $("#kind").value, cohort: $("#cohort").value, profile: $("#profile").value, evidence: $("#evidence").value, disposition: $("#disposition").value };
  Object.entries(values).forEach(([key, value]) => { if (value) params.set(key, value); });
  const query = params.toString();
  if (mode !== "none") history[mode === "push" ? "pushState" : "replaceState"](null, "", `${location.pathname}${query ? `?${query}` : ""}${location.hash}`);
}

function applyFilters(historyMode = "replace") {
  const query = $("#search").value.trim().toLocaleLowerCase();
  const fields = ["kind", "cohort", "profile", "disposition"];
  state.filtered = state.invalidFilter ? [] : state.data.entities.filter((entity) => {
    const haystack = [entity.name, entity.summary, entity.language, ...(entity.traits || []), ...(entity.topicHits || [])].join(" ").toLocaleLowerCase();
    const evidence = $("#evidence").value;
    const evidenceKinds = state.data.claims.filter((claim) => claim.entity === entity.id).map((claim) => claim.evidenceKind);
    const evidenceMatch = !evidence || (evidence === "seed-only" ? evidenceKinds.length === 0 : evidenceKinds.includes(evidence));
    return (!query || haystack.includes(query)) && evidenceMatch && fields.every((field) => !$(`#${field}`).value || entity[field] === $(`#${field}`).value);
  });
  syncUrl(historyMode);
  renderCards();
}

function renderCards() {
  const cards = $("#cards");
  cards.replaceChildren();
  $("#result-count").textContent = state.invalidFilter ? `不明なfilter: ${state.invalidFilter} · 0件` : `${state.filtered.length} / ${state.data.entities.length} 件`;
  state.filtered.forEach((entity) => {
    const claimKinds = unique(state.data.claims.filter((claim) => claim.entity === entity.id).map((claim) => claim.evidenceKind));
    const tags = element("div", { className: "tags" }, [
      element("span", { className: "tag", text: entity.kind }),
      element("span", { className: "tag", text: entity.language || "language n/a" }),
      ...(entity.traits || []).slice(0, 3).map((trait) => element("span", { className: "tag", text: trait })),
      element("span", { className: "tag", text: claimKinds.length ? `evidence: ${claimKinds.join("+")}` : "evidence: seed only" })
    ]);
    const button = element("button", { type: "button", text: "根拠と詳細" });
    button.addEventListener("click", () => openDetail(entity.id));
    cards.append(element("article", { className: `card ${entity.disposition}` }, [
      element("div", { className: "card-top" }, [
        element("div", {}, [element("p", { className: "eyebrow", text: entity.cohort }), element("h3", { text: entity.name })]),
        element("span", { className: `badge ${entity.profile}`, text: entity.profile })
      ]),
      element("p", { text: entity.summary }),
      tags,
      entity.quarantineReason ? element("p", { text: `隔離理由: ${entity.quarantineReason}` }) : null,
      button
    ]));
  });
}

function openDetail(id) {
  const entity = entityById(id);
  if (!entity) return;
  $("#detail-title").textContent = entity.name;
  const body = $("#detail-body");
  const claims = state.data.claims.filter((claim) => claim.entity === id);
  const sources = element("ul");
  entity.sources.forEach((url) => sources.append(element("li", {}, [element("a", { href: url, text: url, target: "_blank", rel: "noreferrer" })])));
  const claimList = element("ul");
  claims.forEach((claim) => claimList.append(element("li", {}, [document.createTextNode(`${claim.claim} `), element("a", { href: claim.source, text: `[${claim.evidenceKind}]`, target: "_blank", rel: "noreferrer" })])));
  const profile = entity.profileDoc && state.data.profiles[entity.profileDoc];
  body.replaceChildren(
    element("p", { text: entity.summary }),
    element("p", { text: `${entity.kind} · ${entity.cohort} · ${entity.language || "n/a"} · ${entity.profile}` }),
    element("h3", { text: "検証済みclaim" }),
    claims.length ? claimList : element("p", { text: "詳細claimは未収録です。seedとして境界だけを記録しています。" }),
    element("h3", { text: "一次資料" }), sources,
    profile ? element("pre", { className: "profile-text", text: profile }) : null
  );
  $("#detail-dialog").showModal();
}

function filteredRelations() {
  const type = $("#relation-type").value;
  const evidence = $("#relation-evidence").value;
  const confidence = $("#relation-confidence").value;
  const cohort = $("#relation-cohort").value;
  return state.data.relations.filter((relation) => {
    const source = entityById(relation.from);
    const target = relation.to && entityById(relation.to);
    return (!type || relation.type === type) && (!evidence || relation.evidenceKind === evidence) && (!confidence || relation.confidence === confidence) && (!cohort || source?.cohort === cohort || target?.cohort === cohort);
  });
}

function renderGraph() {
  const graph = $("#lineage-graph");
  [...graph.querySelectorAll(".dynamic")].forEach((node) => node.remove());
  const relations = filteredRelations();
  const names = new Map(state.data.entities.map((entity) => [entity.id, entity.name]));
  relations.forEach((relation) => { if (relation.toExternal) names.set(`external:${relation.toExternal}`, relation.toExternal); });
  const cohort = $("#relation-cohort").value;
  const catalogIds = state.data.entities.filter((entity) => entity.disposition === "included" && (!cohort || entity.cohort === cohort)).map((entity) => entity.id);
  const ids = unique([...catalogIds, ...relations.flatMap((relation) => [relation.from, relation.to || `external:${relation.toExternal}`])]);
  const radius = Math.min(245, 120 + ids.length * 5);
  const positions = new Map(ids.map((id, index) => {
    const angle = (Math.PI * 2 * index / Math.max(ids.length, 1)) - Math.PI / 2;
    return [id, { x: 500 + Math.cos(angle) * radius, y: 300 + Math.sin(angle) * radius }];
  }));
  relations.forEach((relation) => {
    const start = positions.get(relation.from);
    const targetId = relation.to || `external:${relation.toExternal}`;
    const end = positions.get(targetId);
    if (!start || !end) return;
    const line = document.createElementNS(svgNS, "line");
    line.setAttribute("x1", start.x); line.setAttribute("y1", start.y); line.setAttribute("x2", end.x); line.setAttribute("y2", end.y);
    line.setAttribute("class", `dynamic edge ${relation.evidenceKind}`);
    line.setAttribute("tabindex", "0"); line.setAttribute("role", "link");
    line.setAttribute("aria-label", `${names.get(relation.from)} to ${names.get(targetId)}: ${relation.type}, ${relation.evidenceKind}, ${relation.confidence}`);
    const title = document.createElementNS(svgNS, "title"); title.textContent = `${relation.type}: ${relation.summary}`; line.append(title); graph.append(line);
    line.addEventListener("keydown", (event) => { if (event.key === "Enter") window.open(relation.source, "_blank", "noopener"); });
  });
  ids.forEach((id) => {
    const position = positions.get(id);
    const group = document.createElementNS(svgNS, "g"); group.setAttribute("class", "dynamic node"); group.setAttribute("transform", `translate(${position.x},${position.y})`);
    group.setAttribute("tabindex", "0"); group.setAttribute("role", "button"); group.setAttribute("aria-label", names.get(id));
    const circle = document.createElementNS(svgNS, "circle"); circle.setAttribute("r", id.startsWith("external:") ? "7" : "10");
    const text = document.createElementNS(svgNS, "text"); text.setAttribute("y", "25"); text.textContent = names.get(id);
    group.append(circle, text);
    if (!id.startsWith("external:")) {
      const activate = (event) => { if (event.type === "click" || event.key === "Enter" || event.key === " ") openDetail(id); };
      group.addEventListener("click", activate); group.addEventListener("keydown", activate);
    }
    graph.append(group);
  });
  const list = $("#relation-list"); list.replaceChildren();
  relations.forEach((relation) => {
    const source = entityById(relation.from)?.name || relation.from;
    const target = relation.to ? entityById(relation.to)?.name : relation.toExternal;
    list.append(element("div", { className: "relation-row" }, [
      element("strong", { text: `${source} → ${target}` }),
      element("span", { text: relation.summary }),
      element("span", { className: "relation-meta" }, [element("a", { href: relation.source, text: `${relation.type} · ${relation.evidenceKind} · ${relation.confidence} · observed ${relation.observedAt || state.data.asOf}`, target: "_blank", rel: "noreferrer" })])
    ]));
  });
}

function renderTimeline() {
  const target = $("#timeline-list"); target.replaceChildren();
  state.data.generations.forEach((generation) => target.append(element("article", { className: "timeline-item" }, [
    element("div", { className: "timeline-year", text: `${generation.from}—${generation.to}` }),
    element("div", {}, [element("h3", { text: generation.label }), element("p", { text: generation.shift }), element("p", { text: generation.entities.map((id) => entityById(id)?.name || id).join(" · ") }), element("a", { href: generation.source, text: `source · observed ${state.data.asOf} · grouping does not assert exact same-year order`, target: "_blank", rel: "noreferrer" })])
  ])));
}

function renderMatrix() {
  const matrix = state.data.matrices.find((item) => item.id === $("#matrix-select").value) || state.data.matrices[0];
  const ids = matrix.targets;
  const table = $("#comparison-table");
  const headRow = element("tr", {}, [element("th", { scope: "col", text: "dimension" }), ...ids.map((id) => element("th", { scope: "col", text: entityById(id).name }))]);
  const body = element("tbody");
  matrix.rows.forEach((matrixRow) => {
    const row = element("tr", {}, [element("th", { scope: "row", text: matrixRow.dimension })]);
    ids.forEach((id) => {
      const cellData = matrixRow.cells[id];
      const cell = element("td");
      cell.append(element("strong", { text: cellData.state }), document.createTextNode(` — ${cellData.strength}`), element("br"), element("span", { text: `cost: ${cellData.cost}` }));
      (cellData.claimIds || []).forEach((claimId) => {
        const claim = state.data.claims.find((item) => item.id === claimId);
        if (claim) cell.append(element("a", { className: "cell-source", href: claim.source, text: `${claim.id} · ${claim.evidenceKind}`, target: "_blank", rel: "noreferrer" }));
      });
      if (cellData.unresolvedId) {
        const unresolved = state.data.unresolved.find((item) => item.id === cellData.unresolvedId);
        if (unresolved) cell.append(element("a", { className: "cell-source", href: unresolved.resolutionIssue, text: `${unresolved.id} · ${unresolved.status}`, target: "_blank", rel: "noreferrer" }));
      }
      row.append(cell);
    });
    body.append(row);
  });
  table.replaceChildren(element("caption", { text: `${matrix.label}。unknown、unmeasured、not-applicableを区別します。` }), element("thead", {}, [headRow]), body);
}

function renderCaseStudy() {
  const study = state.data.caseStudy;
  $("#case-scope").textContent = study.scope;
  const manifest = study.sourceManifest;
  $("#case-evidence").replaceChildren(
    element("strong", { text: `Pinned revision ${manifest.revision.slice(0, 12)} · observed ${manifest.observedAt}` }),
    element("p", { text: manifest.authorScope }),
    element("a", { href: `https://github.com/kgrzybek/modular-monolith-with-ddd/commit/${manifest.revision}`, text: "pinned source", target: "_blank", rel: "noreferrer" }),
    element("ul", {}, manifest.historicalCaveats.map((caveat) => element("li", { text: caveat })))
  );
  const patterns = $("#patterns"); patterns.replaceChildren();
  study.patterns.forEach((pattern) => {
    const definition = element("dl");
    [["問題", pattern.problem], ["機構", pattern.mechanism], ["不変条件", pattern.invariant], ["失敗形", pattern.failureMode]].forEach(([term, value]) => definition.append(element("dt", { text: term }), element("dd", { text: value })));
    patterns.append(element("article", { className: "pattern" }, [element("h3", { text: pattern.name }), definition]));
  });
  const fields = [["moduleBoundary", "Module"], ["commandQuery", "Command/Query"], ["effects", "Effects"], ["outboxInbox", "Outbox/Inbox"], ["eventSourcing", "Event Sourcing"], ["testing", "Testing"], ["lifecycle", "Lifecycle"], ["architectureGate", "Architecture gate"], ["patternDecisions", "Adopt / adapt / reject"], ["warning", "Warning"]];
  const table = $("#mapping-table");
  const head = element("tr", {}, [element("th", { scope: "col", text: "decision" }), ...study.mappings.map((mapping) => element("th", { scope: "col", text: mapping.targetLabel }))]);
  const body = element("tbody");
  fields.forEach(([key, title]) => body.append(element("tr", {}, [element("th", { scope: "row", text: title }), ...study.mappings.map((mapping) => {
    const value = key === "patternDecisions" ? mapping.patternDecisions.map((decision) => `${decision.pattern}: ${decision.decision} — ${decision.reason}`).join("\n") : mapping[key];
    return element("td", { text: value });
  })])));
  table.replaceChildren(element("caption", { text: "pattern名の翻訳ではなく、守る不変条件から各targetへ対応付ける" }), element("thead", {}, [head]), body);
}

function renderUnresolved() {
  const target = $("#unresolved-list"); target.replaceChildren();
  const cohort = $("#unresolved-cohort").value;
  const dimension = $("#unresolved-dimension").value;
  const status = $("#unresolved-status").value;
  state.data.unresolved.filter((item) => (!cohort || item.cohort === cohort) && (!dimension || item.dimension === dimension) && (!status || item.status === status)).forEach((item) => target.append(element("article", { className: "unresolved" }, [
    element("p", { className: "status", text: `${item.status} · ${entityById(item.ownerEntity)?.name || item.ownerEntity}` }), element("h3", { text: item.question }),
    element("p", { text: `${item.cohort} · ${item.dimension}` }), element("p", { text: item.reason }), element("strong", { text: "次の証拠" }), element("p", { text: item.nextEvidence }),
    element("a", { href: item.resolutionIssue, text: "実装Issue", target: "_blank", rel: "noreferrer" })
  ])));
}

function renderIssues() {
  const issues = state.data.issues || [];
  const open = issues.filter((issue) => issue.state === "open").length;
  $("#issue-stats").textContent = `${issues.length} issues · open ${open} · closed ${issues.length - open}`;
  const list = $("#issue-list"); list.replaceChildren();
  issues.forEach((issue) => list.append(element("li", {}, [element("a", { href: issue.url, text: `#${issue.number} ${issue.title}`, target: "_blank", rel: "noreferrer" })])));
}

async function initialize() {
  try {
    const response = await fetch("atlas-data.json", { cache: "no-cache" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.data = await response.json();
    fillSelect("#kind", unique(state.data.entities.map((entity) => entity.kind)));
    fillSelect("#cohort", unique(state.data.entities.map((entity) => entity.cohort)));
    fillSelect("#profile", unique(state.data.entities.map((entity) => entity.profile)));
    fillSelect("#relation-type", unique(state.data.relations.map((relation) => relation.type)));
    fillSelect("#relation-cohort", unique(state.data.entities.map((entity) => entity.cohort)));
    state.data.matrices.forEach((matrix) => $("#matrix-select").append(element("option", { value: matrix.id, text: matrix.label })));
    fillSelect("#unresolved-cohort", unique(state.data.unresolved.map((item) => item.cohort)));
    fillSelect("#unresolved-dimension", unique(state.data.unresolved.map((item) => item.dimension)));
    fillSelect("#unresolved-status", unique(state.data.unresolved.map((item) => item.status)));
    syncFiltersFromUrl();
    $("#dataset-summary").textContent = `${state.data.entities.length} entities · ${state.data.relations.length} relations · ${state.data.claims.length} claims · verified ${state.data.asOf}`;
    $("#search").addEventListener("input", () => applyFilters("replace"));
    ["#kind", "#cohort", "#profile", "#evidence", "#disposition"].forEach((selector) => $(selector).addEventListener("change", () => { state.invalidFilter = null; applyFilters("push"); }));
    $("#relation-type").addEventListener("change", renderGraph);
    $("#relation-evidence").addEventListener("change", renderGraph);
    $("#relation-confidence").addEventListener("change", renderGraph);
    $("#relation-cohort").addEventListener("change", renderGraph);
    $("#matrix-select").addEventListener("change", renderMatrix);
    ["#unresolved-cohort", "#unresolved-dimension", "#unresolved-status"].forEach((selector) => $(selector).addEventListener("change", renderUnresolved));
    $("#dialog-close").addEventListener("click", () => $("#detail-dialog").close());
    $("#detail-dialog").addEventListener("click", (event) => { if (event.target === $("#detail-dialog")) $("#detail-dialog").close(); });
    window.addEventListener("popstate", () => { syncFiltersFromUrl(); applyFilters("none"); });
    applyFilters("none"); renderGraph(); renderTimeline(); renderMatrix(); renderCaseStudy(); renderUnresolved(); renderIssues();
    try {
      const sourceResponse = await fetch("source.json", { cache: "no-cache" });
      if (sourceResponse.ok) {
        const source = await sourceResponse.json();
        const link = element("a", { href: `https://github.com/hjosugi/framework-atlas/commit/${source.commit}`, text: source.commit.slice(0, 12), target: "_blank", rel: "noreferrer" });
        $("#source-revision").replaceChildren(document.createTextNode("deployed source: "), link);
      } else $("#source-revision").textContent = "local build: deployment revision is supplied by GitHub Pages";
    } catch (_error) {
      $("#source-revision").textContent = "local build: deployment revision is supplied by GitHub Pages";
    }
  } catch (error) {
    $("#dataset-summary").textContent = `データを読み込めませんでした: ${error.message}`;
  }
}

initialize();
