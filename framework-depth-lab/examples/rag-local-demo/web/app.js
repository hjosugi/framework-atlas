/* Debug UI logic. Vanilla JS, no libraries.
   State flows one way: fetch -> state -> render everything. */

"use strict";

const DOC_COLORS = ["#0e7c7b", "#b07d2b", "#4a6fa5", "#8a4f7d", "#5e7b3b", "#946458"];

const EXAMPLE_QUERIES = [
  "45日前に買った年間サブスクは返金できますか？",
  "返金はいつ届きますか？",
  "返金の条件を教えて",
  "メールアドレスを変えたい",
];

const PAIR_PRESETS = [
  {
    label: "否定（できます / できません）",
    a: "管理者はアーカイブ済みのプロジェクトを削除できます。",
    b: "管理者はアーカイブ済みのプロジェクトを削除できません。",
  },
  {
    label: "数値（30日 / 60日）",
    a: "年間サブスクリプションは30日以内であれば返金できます。",
    b: "年間サブスクリプションは60日以内であれば返金できます。",
  },
  {
    label: "エンティティ（住所 / メール）",
    a: "請求先住所を変更する方法を説明します。",
    b: "メールアドレスを変更する方法を説明します。",
  },
  {
    label: "関連はするが答えていない",
    a: "承認された返金が届くまでどのくらいかかりますか？",
    b: "年間サブスクリプションは、購入日から30日以内に申請した場合のみ返金できます。",
  },
];

const state = {
  chunks: [],
  manifest: null,
  colorByDoc: {},
  search: null, // last /api/search response
  selected: null, // chunk index
  scale: "auto", // "auto" | "full"
};

const $ = (id) => document.getElementById(id);

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

/* ---------- data loading ---------- */

async function loadState() {
  const response = await fetch("/api/state");
  const data = await response.json();
  state.chunks = data.chunks;
  state.manifest = data.manifest;

  const docs = [...new Set(data.chunks.map((c) => c.doc))];
  docs.forEach((doc, i) => {
    state.colorByDoc[doc] = DOC_COLORS[i % DOC_COLORS.length];
  });

  const m = state.manifest;
  $("manifest-line").textContent =
    `model: ${m.model_name} / ${m.dimensions}次元 / ${m.num_chunks}チャンク / 正規化: ${m.normalization}`;

  renderExamples();
  renderPresets();
  renderMap();
  renderLegend();
}

async function runSearch() {
  const query = $("query").value.trim();
  if (!query) return;

  const button = $("search-btn");
  button.disabled = true;
  button.textContent = "計算中…";

  const params = new URLSearchParams({ q: query, k: $("k").value });
  if ($("filter-current").checked) params.append("filter", "status=current");

  try {
    const response = await fetch("/api/search?" + params.toString());
    state.search = await response.json();
  } finally {
    button.disabled = false;
    button.textContent = "検索";
  }

  renderVerdict();
  renderBars();
  renderMap();
  renderPrompt();
  renderDetail();
}

/* ---------- controls ---------- */

function renderExamples() {
  const html = ['<span class="label">例:</span>'];
  for (const q of EXAMPLE_QUERIES) {
    html.push(`<button class="ghost" data-q="${escapeHtml(q)}">${escapeHtml(q)}</button>`);
  }
  $("examples").innerHTML = html.join("");
  $("examples").addEventListener("click", (event) => {
    const target = event.target.closest("[data-q]");
    if (!target) return;
    $("query").value = target.dataset.q;
    runSearch();
  });
}

/* ---------- verdict strip ---------- */

function renderVerdict() {
  const search = state.search;
  const box = $("verdict");
  if (!search || search.error) {
    box.hidden = true;
    return;
  }

  const top = search.top_ids.map((i) => state.chunks[i]);
  const parts = [];
  if (top.length > 0) {
    const first = top[0];
    parts.push(`#1 <span class="mono">${escapeHtml(first.chunk_id)}</span> ` +
      `score ${search.scores[first.i].toFixed(4)}`);
  }
  if (top.length > 1) {
    const delta = search.scores[top[0].i] - search.scores[top[1].i];
    parts.push(`#2 との差 Δ ${delta.toFixed(4)}`);
  }

  const hasDeprecated = top.some((c) => c.meta.status === "deprecated");
  let warning = "";
  if (hasDeprecated) {
    warning = ' <span class="warn-text">注意: top-k に status=deprecated が入っています。' +
      "このまま LLM に渡すと旧ポリシーで答える恐れがあります。</span>";
  }

  box.className = hasDeprecated ? "verdict warn" : "verdict";
  box.innerHTML = parts.join(" ／ ") + warning;
  box.hidden = false;
}

/* ---------- score bars ---------- */

function scaleRange() {
  const scores = state.search.scores;
  if (state.scale === "full") return [0, 1];
  const lo = Math.min(...scores);
  const hi = Math.max(...scores);
  const pad = Math.max((hi - lo) * 0.15, 0.005);
  return [lo - pad, Math.min(hi + pad, 1)];
}

function renderBars() {
  const search = state.search;
  if (!search || search.error) return;

  const [lo, hi] = scaleRange();
  const width = (s) => Math.max(((s - lo) / (hi - lo)) * 100, 2).toFixed(1);
  const rankOf = new Map(search.top_ids.map((id, r) => [id, r + 1]));

  const rows = [];
  for (const i of search.order) {
    const chunk = state.chunks[i];
    const score = search.scores[i];
    const excluded = !search.passes[i];
    const rank = rankOf.get(i);
    const color = state.colorByDoc[chunk.doc];

    const badges = [];
    if (chunk.meta.status === "deprecated") badges.push('<span class="badge dep">deprecated</span>');
    if (excluded) badges.push('<span class="badge">フィルタで除外</span>');

    rows.push(
      `<div class="bar-row${excluded ? " excluded" : ""}${state.selected === i ? " selected" : ""}" data-i="${i}">` +
        `<span class="rank${rank ? "" : " out"}">${rank ?? "・"}</span>` +
        `<div class="bar-main">` +
          `<div class="bar-head"><span class="cid">${escapeHtml(chunk.chunk_id)}</span>` +
            badges.join("") +
            `<span class="score">${score.toFixed(4)}</span></div>` +
          `<div class="track"><div class="fill" style="width:${width(score)}%;background:${color}"></div></div>` +
        `</div>` +
      `</div>`
    );
  }
  $("bars").innerHTML = rows.join("");

  const note = $("axis-note");
  note.hidden = false;
  note.textContent = state.scale === "full"
    ? "目盛り: 0 – 1（実スケール。スコアが右端に密集する＝『関連』はどれも高く出る）"
    : `目盛り: ${lo.toFixed(3)} – ${hi.toFixed(3)}（拡大表示。差を見やすくしている）`;
}

/* ---------- vector map ---------- */

function renderMap() {
  const chunks = state.chunks;
  if (chunks.length === 0) return;

  const search = state.search && !state.search.error ? state.search : null;

  // Extent over chunk coords + query point, with padding.
  const xs = chunks.map((c) => c.x);
  const ys = chunks.map((c) => c.y);
  if (search) {
    xs.push(search.query_xy[0]);
    ys.push(search.query_xy[1]);
  }
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const minY = Math.min(...ys), maxY = Math.max(...ys);
  const padX = (maxX - minX || 1) * 0.14;
  const padY = (maxY - minY || 1) * 0.14;

  const W = 640, H = 430;
  const sx = (x) => ((x - minX + padX) / (maxX - minX + 2 * padX)) * W;
  const sy = (y) => H - ((y - minY + padY) / (maxY - minY + 2 * padY)) * H;

  const svg = [`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="ベクトル空間マップ">`];

  // Chart-paper grid.
  for (let g = 1; g < 8; g++) {
    const gx = (W / 8) * g, gy = (H / 8) * g;
    svg.push(`<line x1="${gx}" y1="0" x2="${gx}" y2="${H}" stroke="#e3e7df" stroke-width="1"/>`);
    svg.push(`<line x1="0" y1="${gy}" x2="${W}" y2="${gy}" stroke="#e3e7df" stroke-width="1"/>`);
  }

  // Tether lines from the query to top-k.
  if (search) {
    const qx = sx(search.query_xy[0]), qy = sy(search.query_xy[1]);
    for (const i of search.top_ids) {
      svg.push(`<line x1="${qx}" y1="${qy}" x2="${sx(chunks[i].x)}" y2="${sy(chunks[i].y)}"` +
        ` stroke="#6d28d9" stroke-width="1.4" opacity="0.45"/>`);
    }
  }

  // Chunk dots.
  const topSet = new Set(search ? search.top_ids : []);
  for (const chunk of chunks) {
    const i = chunk.i;
    const cx = sx(chunk.x), cy = sy(chunk.y);
    const color = state.colorByDoc[chunk.doc];
    const excluded = search && !search.passes[i];
    const isTop = topSet.has(i);
    const isSelected = state.selected === i;

    const fill = excluded ? "#fbfcfa" : color;
    const stroke = isSelected ? "#6d28d9" : (isTop ? "#22303a" : color);
    const strokeWidth = isSelected || isTop ? 2.2 : 1;
    const dash = excluded ? ' stroke-dasharray="3 2"' : "";
    const radius = isTop ? 9 : 7;

    svg.push(`<circle data-i="${i}" cx="${cx}" cy="${cy}" r="${radius}"` +
      ` fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}"${dash}>` +
      `<title>${escapeHtml(chunk.chunk_id)} / ${escapeHtml(chunk.section)}</title></circle>`);

    if (isTop) {
      const rank = search.top_ids.indexOf(i) + 1;
      svg.push(`<text x="${cx + 11}" y="${cy - 8}" font-size="11.5" fill="#22303a" font-weight="600">${rank}</text>`);
    }
    if (chunk.meta.status === "deprecated") {
      svg.push(`<text x="${cx + 11}" y="${cy + 13}" font-size="10" fill="#b3261e">deprecated</text>`);
    }
  }

  // Query crosshair.
  if (search) {
    const qx = sx(search.query_xy[0]), qy = sy(search.query_xy[1]);
    svg.push(`<circle cx="${qx}" cy="${qy}" r="6.5" fill="none" stroke="#6d28d9" stroke-width="2"/>`);
    svg.push(`<line x1="${qx - 11}" y1="${qy}" x2="${qx + 11}" y2="${qy}" stroke="#6d28d9" stroke-width="1.4"/>`);
    svg.push(`<line x1="${qx}" y1="${qy - 11}" x2="${qx}" y2="${qy + 11}" stroke="#6d28d9" stroke-width="1.4"/>`);
    svg.push(`<text x="${qx + 13}" y="${qy + 4}" font-size="11.5" fill="#6d28d9" font-weight="600">query</text>`);
  }

  svg.push("</svg>");
  $("map").innerHTML = svg.join("");
}

function renderLegend() {
  const items = Object.entries(state.colorByDoc).map(([doc, color]) =>
    `<span><span class="sw" style="background:${color}"></span>${escapeHtml(doc)}</span>`);
  items.push('<span><span class="sw" style="background:#fbfcfa;border:1px dashed #5c6b74"></span>フィルタで除外</span>');
  $("legend").innerHTML = items.join("");
}

/* ---------- detail panel ---------- */

function renderDetail() {
  const i = state.selected;
  if (i === null || i === undefined) return;
  const chunk = state.chunks[i];
  const search = state.search && !state.search.error ? state.search : null;

  const rows = [
    ["chunk_id", `<span class="mono">${escapeHtml(chunk.chunk_id)}</span>`],
    ["ドキュメント", `${escapeHtml(chunk.meta.title ?? chunk.doc)}（${escapeHtml(chunk.doc)}）`],
    ["セクション", escapeHtml(chunk.section)],
    ["version / date", `${escapeHtml(chunk.meta.version ?? "-")} / ${escapeHtml(chunk.meta.date ?? "-")}`],
    ["status", chunk.meta.status === "deprecated"
      ? '<span class="badge dep">deprecated</span>' : escapeHtml(chunk.meta.status ?? "-")],
    ["content_hash", `<span class="mono">${escapeHtml(chunk.content_hash)}</span>`],
  ];
  if (search) {
    const rank = search.top_ids.indexOf(i);
    const rankLabel = rank >= 0 ? `#${rank + 1}` : (search.passes[i] ? "top-k 圏外" : "フィルタで除外");
    rows.push(["このクエリでの評価", `score ${search.scores[i].toFixed(4)}（${rankLabel}）`]);
  }

  const dl = rows.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join("");
  $("detail").innerHTML =
    `<dl class="detail-grid">${dl}</dl>` +
    `<div class="chunk-text">${escapeHtml(chunk.text)}</div>` +
    `<details><summary>埋め込みモデルに渡した実際の文字列（タイトル + セクションを前置）</summary>` +
    `<pre>passage: ${escapeHtml(chunk.embed_text)}</pre></details>`;
}

function selectChunk(i) {
  state.selected = i;
  renderBars();
  renderMap();
  renderDetail();
  $("detail").scrollIntoView({ behavior: "smooth", block: "nearest" });
}

/* ---------- prompt panel ---------- */

function renderPrompt() {
  const search = state.search;
  if (!search || search.error) return;
  $("prompt").innerHTML = `<pre id="prompt-text">${escapeHtml(search.prompt)}</pre>`;
  $("copy-btn").hidden = false;
}

async function copyPrompt() {
  const text = document.getElementById("prompt-text");
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text.textContent);
    $("copy-btn").textContent = "コピーしました";
    setTimeout(() => { $("copy-btn").textContent = "プロンプトをコピー"; }, 1500);
  } catch {
    // Clipboard can fail outside secure contexts. Select the text instead.
    const range = document.createRange();
    range.selectNodeContents(text);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
  }
}

/* ---------- pair lab ---------- */

function renderPresets() {
  $("presets").innerHTML = PAIR_PRESETS.map((preset, i) =>
    `<button class="ghost" data-p="${i}">${escapeHtml(preset.label)}</button>`).join("");
  $("presets").addEventListener("click", (event) => {
    const target = event.target.closest("[data-p]");
    if (!target) return;
    const preset = PAIR_PRESETS[Number(target.dataset.p)];
    $("pair-a").value = preset.a;
    $("pair-b").value = preset.b;
    runPair();
  });
}

async function runPair() {
  const a = $("pair-a").value.trim();
  const b = $("pair-b").value.trim();
  if (!a || !b) return;

  const button = $("pair-btn");
  button.disabled = true;
  const params = new URLSearchParams({ a, b });
  let data;
  try {
    const response = await fetch("/api/pair?" + params.toString());
    data = await response.json();
  } finally {
    button.disabled = false;
  }
  if (data.error) return;

  let comment = "意味は近いと判定される。";
  if (data.cosine >= 0.95) {
    comment = "ほぼ同一ベクトル扱い。否定や数値の違いは埋め込みからは見えない。";
  } else if (data.cosine < 0.7) {
    comment = "モデルはこの2文を別の話題と見ている。";
  }

  $("pair-result").innerHTML =
    `cosine = <strong>${data.cosine.toFixed(4)}</strong> — ${comment}` +
    `<div class="gauge"><div class="gfill" style="width:${(data.cosine * 100).toFixed(1)}%"></div></div>` +
    `<div class="gauge-labels"><span>0</span><span>1</span></div>`;
}

/* ---------- wiring ---------- */

function wire() {
  $("search-btn").addEventListener("click", runSearch);
  $("query").addEventListener("keydown", (event) => {
    if (event.key === "Enter") runSearch();
  });
  $("filter-current").addEventListener("change", () => {
    if (state.search) runSearch();
  });
  $("k").addEventListener("change", () => {
    if (state.search) runSearch();
  });

  document.querySelector(".scale-toggle").addEventListener("click", (event) => {
    const target = event.target.closest("[data-scale]");
    if (!target) return;
    state.scale = target.dataset.scale;
    document.querySelectorAll("[data-scale]").forEach((b) =>
      b.classList.toggle("on", b.dataset.scale === state.scale));
    if (state.search) renderBars();
  });

  // One delegated click handler for bars and map dots.
  for (const id of ["bars", "map"]) {
    $(id).addEventListener("click", (event) => {
      const target = event.target.closest("[data-i]");
      if (target) selectChunk(Number(target.dataset.i));
    });
  }

  $("pair-btn").addEventListener("click", runPair);
  $("copy-btn").addEventListener("click", copyPrompt);
}

wire();
loadState();
