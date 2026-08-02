(() => {
  'use strict';

  const atlas = window.FRAMEWORK_ATLAS;
  if (!atlas) {
    document.body.innerHTML = '<main class="page-width"><div class="detail-box"><h1>データを読み込めませんでした</h1><p><code>make build</code> を実行してください。</p></div></main>';
    return;
  }

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

  const frameworks = atlas.frameworks || [];
  const concepts = atlas.concepts || [];
  const relations = atlas.relations || [];
  const families = atlas.families || [];
  const timeline = atlas.timeline || [];
  const researchGaps = atlas.research_gaps || [];
  const issueFiles = new Map((atlas.issue_files || []).map((item) => [item.id, item.file]));
  const stats = atlas.meta?.stats || {};

  const CATEGORY_LABELS = {
    'backend-web': 'バックエンドWeb',
    'frontend-framework': 'フロントエンドFramework',
    'frontend-library': 'フロントエンドLibrary',
    'meta-framework': 'Meta-framework',
    router: 'Routing',
    'data-model': 'Data model / ORM',
    tui: 'Terminal UI',
    cli: 'CLI',
    'mobile-desktop': 'Mobile / Desktop',
    testing: 'Testing',
    'ai-data': 'AI / Data',
    'data-framework': 'Data framework',
    'distributed-framework': 'Distributed',
    game: 'Game',
    runtime: 'Runtime',
    'application-framework': 'Application framework',
    'css-ui': 'CSS / UI',
    'static-site': 'Static site',
    'embedded-framework': 'Embedded',
    'network-product': 'Network product（別枠）',
    'security-framework': 'Security framework（別枠）',
    concept: '設計概念・標準',
  };

  const RELATION_LABELS = {
    'built-on': '上に構築',
    'direct-influence': '直接的な影響',
    'design-influence': '設計上の影響',
    'design-foundation': '設計の土台',
    'platform-foundation': 'platform の土台',
    'runtime-foundation': 'runtime の土台',
    'server-foundation': 'server の土台',
    'standards-foundation': '標準仕様の土台',
    'language-platform': '言語/platform',
    'pattern-lineage': 'pattern の系譜',
    'design-lineage': '設計の系譜',
    'design-relative': '設計上の近縁',
    'design-response': '同じ問題への別解',
    'design-contrast': '対照的な設計',
    'rendering-model': '描画 model',
    'api-inspiration': 'API の着想',
    'api-lineage': 'API の系譜',
    'api-affinity': 'API の近さ',
    'successor-rewrite': '後継 rewrite',
    'successor-experiment': '後継実験',
    evolution: '世代進化',
    'evolved-into': '発展先',
    origin: '起源',
    ecosystem: '公式・周辺 ecosystem',
    'ecosystem-evolution': 'ecosystem の進化',
    'ecosystem-foundation': 'ecosystem の基盤',
    'backend-ecosystem': 'backend ecosystem',
    'testing-ecosystem': 'testing ecosystem',
    complement: '補完関係',
    'component-of': '構成要素',
    'uses-components': 'component を利用',
    implements: '実装',
    'implementation-layer': '実装 layer',
    'common-implementation': '主要実装',
    'built-with': 'これで構築',
    'renderer-extension': 'renderer への展開',
    'platform-extension': 'platform への展開',
    'platform-adapter': 'platform adapter',
    'application-platform': 'application platform',
    'framework-integration': 'framework 統合',
    'tooling-foundation': 'tooling の土台',
    'same-problem': '同じ問題への別解',
    classification: '同じ topic 内の分類',
  };

  const nodeMap = new Map();
  frameworks.forEach((item) => nodeMap.set(item.id, { ...item, node_class: 'framework' }));
  concepts.forEach((item) => nodeMap.set(item.id, {
    ...item,
    node_class: 'concept',
    category: 'concept',
    subcategory: item.kind || 'concept',
    maturity: 'concept',
    status: 'historical',
    first_release: item.year || '',
    languages: [],
    summary_ja: item.summary_ja || '',
    problem_ja: item.summary_ja || '',
    history_ja: '',
    design_ja: '',
    data_model_ja: '',
    strengths_ja: [],
    tradeoffs_ja: [],
    best_for_ja: [],
    avoid_when_ja: [],
    sources: [],
  }));

  // Virtual nodes exist only to explain a family tree, for example “router topic”.
  families.forEach((family) => {
    family.generations.forEach((generation) => {
      generation.nodes.forEach((node) => {
        if (node.virtual && !nodeMap.has(node.id)) {
          nodeMap.set(node.id, {
            ...node,
            node_class: 'virtual',
            category: 'concept',
            subcategory: node.kind || 'idea',
            maturity: 'virtual',
            status: 'conceptual',
            first_release: node.year || '',
            languages: [],
            problem_ja: node.summary_ja || '',
            history_ja: '',
            design_ja: '',
            data_model_ja: '',
            strengths_ja: [],
            tradeoffs_ja: [],
            best_for_ja: [],
            avoid_when_ja: [],
            sources: [],
          });
        }
      });
    });
  });

  frameworks.forEach((item) => {
    item.__search = normalize([
      item.id,
      item.name,
      ...(item.aliases || []),
      ...(item.languages || []),
      item.category,
      item.subcategory,
      item.summary_ja,
      item.problem_ja,
      item.history_ja,
      item.design_ja,
      item.data_model_ja,
      ...(item.tags || []),
    ].join(' '));
    const mapped = nodeMap.get(item.id);
    if (mapped) mapped.__search = item.__search;
  });

  const familyNodeRoles = new Map();
  families.forEach((family) => {
    family.generations.forEach((generation, generationIndex) => {
      generation.nodes.forEach((node) => {
        familyNodeRoles.set(`${family.id}:${node.id}`, {
          ...node,
          generationIndex,
          generationLabel: generation.label_ja,
          era: generation.era_ja || '',
        });
      });
    });
  });

  const state = {
    currentView: 'family',
    activeFamilyId: families.find((item) => item.id === 'rails-laravel')?.id || families[0]?.id || '',
    graphScale: 1,
    graphNaturalWidth: 1200,
    graphNaturalHeight: 700,
    showEdgeLabels: false,
    showAllRelations: false,
    selectedNodeId: '',
    catalogPage: 1,
    catalogPageSize: 24,
    compareIds: ['spring-boot', 'laravel', 'ruby-on-rails', 'gin'].filter((id) => nodeMap.has(id)),
    lastFocusedElement: null,
    toastTimer: null,
  };

  function escapeHTML(value) {
    return String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function escapeAttribute(value) {
    return escapeHTML(value).replaceAll('`', '&#096;');
  }

  function normalize(value) {
    return String(value ?? '').normalize('NFKC').toLocaleLowerCase('ja').trim();
  }

  function asArray(value) {
    if (Array.isArray(value)) return value.filter(Boolean);
    return value ? [value] : [];
  }

  function unique(values) {
    return [...new Set(values.filter(Boolean))];
  }

  function truncate(value, max = 140) {
    const text = String(value ?? '').replace(/\s+/g, ' ').trim();
    return text.length > max ? `${text.slice(0, max).trim()}…` : text;
  }

  function categoryLabel(value) {
    return CATEGORY_LABELS[value] || value || '未分類';
  }

  function relationLabel(value) {
    return RELATION_LABELS[value] || value || '関係';
  }

  function nodeName(id) {
    return nodeMap.get(id)?.name || id;
  }

  function safeURL(value) {
    try {
      const url = new URL(value);
      return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
    } catch {
      return '';
    }
  }

  function depthRank(value) {
    return { deep: 0, standard: 1, seed: 2 }[value] ?? 3;
  }

  function showToast(message) {
    const toast = $('#toast');
    toast.textContent = message;
    toast.hidden = false;
    window.clearTimeout(state.toastTimer);
    state.toastTimer = window.setTimeout(() => { toast.hidden = true; }, 2200);
  }

  function listHTML(values, empty = '追加調査中') {
    const list = asArray(values);
    if (!list.length) return `<p>${escapeHTML(empty)}</p>`;
    return `<ul>${list.map((value) => `<li>${escapeHTML(value)}</li>`).join('')}</ul>`;
  }

  function fillSelect(selector, values, labeler = (value) => value) {
    const select = $(selector);
    const first = select.options[0]?.outerHTML || '<option value="">すべて</option>';
    select.innerHTML = first + values
      .slice()
      .sort((a, b) => String(labeler(a)).localeCompare(String(labeler(b)), 'ja'))
      .map((value) => `<option value="${escapeAttribute(value)}">${escapeHTML(labeler(value))}</option>`)
      .join('');
  }

  // ---------------------------------------------------------------------------
  // Navigation and global search
  // ---------------------------------------------------------------------------

  function showView(view, updateHash = true) {
    const valid = ['family', 'catalog', 'compare', 'history', 'issues'];
    if (!valid.includes(view)) view = 'family';
    state.currentView = view;
    $$('[data-view]').forEach((panel) => {
      const active = panel.dataset.view === view;
      panel.hidden = !active;
      panel.classList.toggle('is-active', active);
    });
    $$('[data-view-target]').forEach((button) => {
      const active = button.dataset.viewTarget === view;
      button.classList.toggle('is-active', active);
      if (button.classList.contains('nav-button')) button.setAttribute('aria-current', active ? 'page' : 'false');
    });
    if (updateHash) history.replaceState(null, '', `#${view}`);
    window.scrollTo({ top: 0, behavior: 'auto' });
    if (view === 'family') requestAnimationFrame(applyGraphScale);
  }

  function globalSearchResults(query) {
    const normalized = normalize(query);
    if (!normalized) return [];
    return [...nodeMap.values()]
      .filter((item) => {
        if (item.node_class === 'framework') return item.__search?.includes(normalized);
        return normalize([item.id, item.name, item.summary_ja, item.kind].join(' ')).includes(normalized);
      })
      .sort((a, b) => depthRank(a.maturity) - depthRank(b.maturity) || a.name.localeCompare(b.name, 'ja'))
      .slice(0, 10);
  }

  function renderGlobalSearch() {
    const input = $('#global-search');
    const popover = $('#global-search-results');
    const results = globalSearchResults(input.value);
    if (!input.value.trim()) {
      popover.hidden = true;
      return;
    }
    popover.hidden = false;
    popover.innerHTML = results.length ? results.map((item) => `
      <button type="button" class="search-result-button" data-detail-id="${escapeAttribute(item.id)}">
        <span><strong>${escapeHTML(item.name)}</strong><small>${escapeHTML(categoryLabel(item.category))} · ${escapeHTML(truncate(item.summary_ja || item.problem_ja, 70))}</small></span>
        <span class="badge ${escapeAttribute(item.maturity || '')}">${escapeHTML(item.maturity || item.node_class)}</span>
      </button>
    `).join('') : '<div class="filter-note">該当項目はありません。</div>';
  }

  function setupNavigation() {
    $$('[data-view-target]').forEach((button) => {
      button.addEventListener('click', () => showView(button.dataset.viewTarget));
    });
    $$('[data-family-jump]').forEach((button) => {
      button.addEventListener('click', () => {
        showView('family');
        setActiveFamily(button.dataset.familyJump, true);
      });
    });
    const hash = location.hash.replace('#', '');
    showView(['family', 'catalog', 'compare', 'history', 'issues'].includes(hash) ? hash : 'family', false);
    window.addEventListener('hashchange', () => {
      const next = location.hash.replace('#', '');
      if (['family', 'catalog', 'compare', 'history', 'issues'].includes(next)) showView(next, false);
    });

    $('#global-search').addEventListener('input', renderGlobalSearch);
    $('#global-search').addEventListener('focus', renderGlobalSearch);
    document.addEventListener('click', (event) => {
      if (!event.target.closest('.global-search-wrap')) $('#global-search-results').hidden = true;
    });
  }

  // ---------------------------------------------------------------------------
  // Stats
  // ---------------------------------------------------------------------------

  function renderStats() {
    const items = [
      [stats.frameworks ?? frameworks.length, 'framework / library / tool'],
      [stats.deep_profiles ?? frameworks.filter((item) => item.maturity === 'deep').length, 'deep profiles'],
      [stats.relations ?? relations.length, '根拠レベル付き関係'],
      [stats.families ?? families.length, '分野別の家系図'],
      [stats.research_gaps ?? researchGaps.length, '追加調査 Issue'],
    ];
    $('#stats-strip').innerHTML = items.map(([value, label]) => `
      <div class="stat-item"><strong>${Number(value).toLocaleString()}</strong><span>${escapeHTML(label)}</span></div>
    `).join('');
  }

  // ---------------------------------------------------------------------------
  // Family tree
  // ---------------------------------------------------------------------------

  function familyNodeCount(family) {
    return family.generations.reduce((count, generation) => count + generation.nodes.length, 0);
  }

  function renderFamilyChooser() {
    $('#family-select').innerHTML = families.map((family) => `<option value="${escapeAttribute(family.id)}">${escapeHTML(family.name_ja)}</option>`).join('');
    $('#family-card-list').innerHTML = families.map((family) => `
      <button type="button" class="family-card" data-family-id="${escapeAttribute(family.id)}">
        <span class="family-count">${familyNodeCount(family)}</span>
        <small>${escapeHTML(family.short_ja || family.question_ja || 'Family tree')}</small>
        <strong>${escapeHTML(family.name_ja)}</strong>
        <small>${escapeHTML(truncate(family.summary_ja, 105))}</small>
      </button>
    `).join('');

    $('#family-select').addEventListener('change', (event) => setActiveFamily(event.target.value, true));
    $('#family-card-list').addEventListener('click', (event) => {
      const button = event.target.closest('[data-family-id]');
      if (button) setActiveFamily(button.dataset.familyId, true);
    });
  }

  function activeFamily() {
    return families.find((item) => item.id === state.activeFamilyId) || families[0];
  }

  function setActiveFamily(id, scrollToGraph = false) {
    const family = families.find((item) => item.id === id) || families[0];
    if (!family) return;
    state.activeFamilyId = family.id;
    state.selectedNodeId = '';
    state.graphScale = 1;
    state.showAllRelations = false;
    $('#family-select').value = family.id;
    $$('.family-card').forEach((card) => card.classList.toggle('is-active', card.dataset.familyId === family.id));
    renderFamily();
    if (scrollToGraph) {
      $('.family-stage')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function familyNodeRecord(family, generationNode) {
    const canonical = nodeMap.get(generationNode.id) || {};
    return { ...canonical, ...generationNode, id: generationNode.id, name: canonical.name || generationNode.name || generationNode.id };
  }

  function splitText(value, maxChars = 20, maxLines = 2) {
    const text = String(value || '').trim();
    if (!text) return [];
    const words = text.split(/\s+/);
    const lines = [];
    let current = '';
    if (words.length > 1) {
      words.forEach((word) => {
        const candidate = current ? `${current} ${word}` : word;
        if (candidate.length <= maxChars || !current) current = candidate;
        else {
          lines.push(current);
          current = word;
        }
      });
      if (current) lines.push(current);
    } else {
      for (let index = 0; index < text.length; index += maxChars) lines.push(text.slice(index, index + maxChars));
    }
    if (lines.length > maxLines) {
      lines.length = maxLines;
      lines[maxLines - 1] = `${lines[maxLines - 1].slice(0, Math.max(1, maxChars - 1))}…`;
    }
    return lines;
  }

  function svgTextLines(lines, x, y, className, lineHeight = 16, anchor = 'start') {
    return `<text x="${x}" y="${y}" class="${className}" text-anchor="${anchor}">${lines.map((line, index) => `<tspan x="${x}" dy="${index === 0 ? 0 : lineHeight}">${escapeHTML(line)}</tspan>`).join('')}</text>`;
  }

  function edgeClass(edge) {
    if (edge.verification === 'verified') return 'verified';
    if (edge.verification === 'grouping') return 'grouping';
    return 'hypothesis';
  }

  function buildGraphModel(family) {
    const NODE_W = 190;
    const NODE_H = 104;
    const X_GAP = 28;
    const BAND_H = 188;
    const TOP = 44;
    const SIDE = 80;
    const maxCount = Math.max(...family.generations.map((generation) => generation.nodes.length), 1);
    const naturalWidth = Math.max(1120, SIDE * 2 + maxCount * NODE_W + Math.max(0, maxCount - 1) * X_GAP);
    const naturalHeight = TOP + family.generations.length * BAND_H + 36;
    const positions = new Map();

    family.generations.forEach((generation, generationIndex) => {
      const rowWidth = generation.nodes.length * NODE_W + Math.max(0, generation.nodes.length - 1) * X_GAP;
      const startX = (naturalWidth - rowWidth) / 2;
      const y = TOP + generationIndex * BAND_H + 48;
      generation.nodes.forEach((generationNode, nodeIndex) => {
        positions.set(generationNode.id, {
          x: startX + nodeIndex * (NODE_W + X_GAP),
          y,
          w: NODE_W,
          h: NODE_H,
          generationIndex,
          generationNode,
        });
      });
    });
    return { naturalWidth, naturalHeight, positions, nodeWidth: NODE_W, nodeHeight: NODE_H, bandHeight: BAND_H, top: TOP };
  }

  function renderEdgePath(edge, model) {
    const from = model.positions.get(edge.from);
    const to = model.positions.get(edge.to);
    if (!from || !to) return '';
    const kind = edgeClass(edge);
    let path;
    let labelX;
    let labelY;

    if (from.generationIndex === to.generationIndex) {
      const leftToRight = from.x < to.x;
      const x1 = leftToRight ? from.x + from.w : from.x;
      const x2 = leftToRight ? to.x : to.x + to.w;
      const y = from.y + from.h / 2;
      const arcY = Math.max(18, from.y - 36);
      path = `M ${x1} ${y} C ${(x1 + x2) / 2} ${arcY}, ${(x1 + x2) / 2} ${arcY}, ${x2} ${y}`;
      labelX = (x1 + x2) / 2;
      labelY = arcY - 5;
    } else {
      const x1 = from.x + from.w / 2;
      const y1 = from.y + from.h;
      const x2 = to.x + to.w / 2;
      const y2 = to.y;
      const middle = y1 + Math.max(30, (y2 - y1) / 2);
      path = `M ${x1} ${y1} C ${x1} ${middle}, ${x2} ${middle}, ${x2} ${y2}`;
      labelX = (x1 + x2) / 2;
      labelY = middle - 6;
    }

    const label = truncate(edge.label_ja || relationLabel(edge.type), 34);
    const labelWidth = Math.max(74, Math.min(260, label.length * 7 + 18));
    const labelMarkup = state.showEdgeLabels ? `
      <g class="edge-label-group">
        <rect class="edge-label-bg" x="${labelX - labelWidth / 2}" y="${labelY - 14}" rx="7" width="${labelWidth}" height="20"></rect>
        <text class="edge-label-text" x="${labelX}" y="${labelY}" text-anchor="middle">${escapeHTML(label)}</text>
      </g>
    ` : '';
    return `
      <g class="edge-group" data-edge-from="${escapeAttribute(edge.from)}" data-edge-to="${escapeAttribute(edge.to)}">
        <path class="edge-path ${kind}" d="${path}" marker-end="url(#arrow-${kind})"><title>${escapeHTML(`${nodeName(edge.from)} → ${nodeName(edge.to)}: ${edge.label_ja || relationLabel(edge.type)}`)}</title></path>
        ${labelMarkup}
      </g>
    `;
  }

  function renderGraphNode(family, generationNode, position) {
    const item = familyNodeRecord(family, generationNode);
    const classes = ['graph-node'];
    if (item.node_class === 'concept') classes.push('concept');
    if (item.node_class === 'virtual' || generationNode.virtual) classes.push('virtual');
    if (item.maturity === 'deep') classes.push('deep');
    if (state.selectedNodeId === item.id) classes.push('is-selected');

    const nameLines = splitText(item.name, 22, 2);
    const roleLines = splitText(generationNode.role_ja || item.summary_ja || '', 29, 2);
    const meta = [item.first_release || item.year, ...(item.languages || []).slice(0, 2)].filter(Boolean).join(' · ');
    const pill = item.node_class === 'concept' ? 'concept' : item.node_class === 'virtual' ? 'idea' : item.maturity || item.kind || 'item';
    return `
      <g class="${classes.join(' ')}" tabindex="0" role="button" aria-label="${escapeAttribute(item.name)} の詳細" data-graph-node-id="${escapeAttribute(item.id)}" transform="translate(${position.x} ${position.y})">
        <rect class="node-box" width="${position.w}" height="${position.h}" rx="13"></rect>
        <rect class="node-depth-pill" x="${position.w - 54}" y="10" width="44" height="18" rx="9"></rect>
        <text class="node-depth-text" x="${position.w - 32}" y="22.5" text-anchor="middle">${escapeHTML(truncate(pill, 9))}</text>
        ${svgTextLines(nameLines, 14, 28, 'node-name', 16)}
        <text class="node-meta" x="14" y="62">${escapeHTML(meta || categoryLabel(item.category))}</text>
        ${svgTextLines(roleLines, 14, 80, 'node-role', 13)}
      </g>
    `;
  }

  function renderFamilyGraph(family) {
    const svg = $('#family-graph');
    const model = buildGraphModel(family);
    state.graphNaturalWidth = model.naturalWidth;
    state.graphNaturalHeight = model.naturalHeight;

    const bands = family.generations.map((generation, index) => {
      const y = model.top + index * model.bandHeight;
      return `
        <g class="generation-layer">
          <rect class="generation-band" x="24" y="${y}" rx="16" width="${model.naturalWidth - 48}" height="${model.bandHeight - 16}"></rect>
          <text class="generation-title" x="46" y="${y + 25}">${escapeHTML(generation.label_ja)}</text>
          <text class="generation-era" x="${model.naturalWidth - 46}" y="${y + 25}" text-anchor="end">${escapeHTML(generation.era_ja || '')}</text>
        </g>
      `;
    }).join('');

    const edges = family.edges.map((edge) => renderEdgePath(edge, model)).join('');
    const nodes = family.generations.flatMap((generation) => generation.nodes.map((node) => renderGraphNode(family, node, model.positions.get(node.id)))).join('');

    svg.setAttribute('viewBox', `0 0 ${model.naturalWidth} ${model.naturalHeight}`);
    svg.innerHTML = `
      <defs>
        <marker id="arrow-verified" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 z" fill="#2357d8"></path></marker>
        <marker id="arrow-hypothesis" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 z" fill="#b86216"></path></marker>
        <marker id="arrow-grouping" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 z" fill="#6b7280"></path></marker>
      </defs>
      ${bands}
      <g class="edge-layer">${edges}</g>
      <g class="node-layer">${nodes}</g>
    `;
    applyGraphScale();
  }

  function applyGraphScale() {
    const svg = $('#family-graph');
    if (!svg) return;
    svg.style.width = `${Math.round(state.graphNaturalWidth * state.graphScale)}px`;
    svg.style.height = `${Math.round(state.graphNaturalHeight * state.graphScale)}px`;
  }

  function fitGraph() {
    const scroll = $('#graph-scroll');
    const available = Math.max(320, scroll.clientWidth - 24);
    state.graphScale = Math.max(0.36, Math.min(1, available / state.graphNaturalWidth));
    applyGraphScale();
    scroll.scrollLeft = 0;
  }

  function zoomGraph(delta) {
    state.graphScale = Math.max(0.35, Math.min(1.5, Math.round((state.graphScale + delta) * 10) / 10));
    applyGraphScale();
  }

  function renderRelationshipList(family) {
    const items = state.showAllRelations ? family.edges : family.edges.slice(0, 9);
    $('#relationship-list').innerHTML = items.map((edge) => {
      const kind = edgeClass(edge);
      const reason = edge.label_ja || relationLabel(edge.type);
      return `
        <div class="relationship-item ${kind}">
          <button class="relationship-node relationship-node-button" type="button" data-detail-id="${escapeAttribute(edge.from)}">${escapeHTML(nodeName(edge.from))}</button>
          <span class="relationship-arrow">→</span>
          <button class="relationship-node relationship-node-button" type="button" data-detail-id="${escapeAttribute(edge.to)}">${escapeHTML(nodeName(edge.to))}</button>
          <span class="relationship-reason">${escapeHTML(reason)} <span class="relation-state">${kind === 'verified' ? '確認済み' : kind === 'grouping' ? '分類上のまとまり' : '要追加調査'}</span></span>
        </div>
      `;
    }).join('');
    $('#show-all-relations').textContent = state.showAllRelations ? '先頭だけ表示' : `すべて表示（${family.edges.length}）`;
  }

  function renderFamily() {
    const family = activeFamily();
    if (!family) return;
    $('#family-select').value = family.id;
    $$('.family-card').forEach((card) => card.classList.toggle('is-active', card.dataset.familyId === family.id));
    $('#family-question').textContent = family.question_ja || family.short_ja || 'Family tree';
    $('#family-title').textContent = family.name_ja;
    $('#family-summary').textContent = family.summary_ja || '';
    $('#family-takeaways').innerHTML = (family.takeaways_ja || []).map((item) => `<li>${escapeHTML(item)}</li>`).join('');
    renderFamilyGraph(family);
    renderRelationshipList(family);
    requestAnimationFrame(fitGraph);
  }

  function highlightGraphNode(id) {
    state.selectedNodeId = id;
    const family = activeFamily();
    const connected = new Set([id]);
    family.edges.forEach((edge) => {
      if (edge.from === id) connected.add(edge.to);
      if (edge.to === id) connected.add(edge.from);
    });
    $$('[data-graph-node-id]').forEach((element) => {
      element.classList.toggle('is-selected', element.dataset.graphNodeId === id);
      element.classList.toggle('is-dimmed', !connected.has(element.dataset.graphNodeId));
    });
  }

  function setupFamily() {
    renderFamilyChooser();
    $('#edge-label-toggle').addEventListener('change', (event) => {
      state.showEdgeLabels = event.target.checked;
      renderFamilyGraph(activeFamily());
    });
    $('#graph-zoom-in').addEventListener('click', () => zoomGraph(0.1));
    $('#graph-zoom-out').addEventListener('click', () => zoomGraph(-0.1));
    $('#graph-fit').addEventListener('click', fitGraph);
    $('#show-all-relations').addEventListener('click', () => {
      state.showAllRelations = !state.showAllRelations;
      renderRelationshipList(activeFamily());
    });
    $('#family-graph').addEventListener('click', (event) => {
      const node = event.target.closest('[data-graph-node-id]');
      if (!node) return;
      highlightGraphNode(node.dataset.graphNodeId);
      openDrawer(node.dataset.graphNodeId, activeFamily());
    });
    $('#family-graph').addEventListener('keydown', (event) => {
      const node = event.target.closest('[data-graph-node-id]');
      if (node && (event.key === 'Enter' || event.key === ' ')) {
        event.preventDefault();
        highlightGraphNode(node.dataset.graphNodeId);
        openDrawer(node.dataset.graphNodeId, activeFamily());
      }
    });
    setActiveFamily(state.activeFamilyId);
  }

  // ---------------------------------------------------------------------------
  // Detail drawer
  // ---------------------------------------------------------------------------

  function relationsForNode(id, family = null) {
    const global = relations.filter((edge) => edge.from === id || edge.to === id).map((edge) => ({ ...edge, graph_source: 'global' }));
    const local = family ? family.edges.filter((edge) => edge.from === id || edge.to === id).map((edge) => ({ ...edge, graph_source: family.id })) : [];
    const map = new Map();
    [...global, ...local].forEach((edge) => {
      const key = `${edge.from}|${edge.to}|${edge.type || edge.label_ja}`;
      if (!map.has(key)) map.set(key, edge);
    });
    return [...map.values()];
  }

  function familiesForNode(id) {
    return families.filter((family) => family.generations.some((generation) => generation.nodes.some((node) => node.id === id)));
  }

  function renderArchitecture(item) {
    const fields = [
      ['中心 abstraction', item.primary_abstraction_ja],
      ['Control flow', item.control_flow_ja],
      ['Rendering', item.rendering_ja],
      ['Routing', item.routing_ja],
      ['DI', item.dependency_injection_ja],
      ['State', item.state_model_ja],
      ['Concurrency', item.concurrency_ja],
      ['Deployment', item.deployment_ja],
      ['Extension', item.extension_model_ja],
      ['Testing', item.testing_ja],
    ].filter(([, value]) => value);
    if (!fields.length) return '<p>追加調査中です。</p>';
    return `<div class="detail-two-col">${fields.map(([label, value]) => `<div class="detail-box"><h4>${escapeHTML(label)}</h4><p>${escapeHTML(value)}</p></div>`).join('')}</div>`;
  }

  function openDrawer(id, family = null) {
    const item = nodeMap.get(id);
    if (!item) return;
    state.lastFocusedElement = document.activeElement;
    const drawer = $('#detail-drawer');
    const verification = item.verification || {};
    const badges = [
      item.maturity || item.node_class,
      categoryLabel(item.category),
      item.first_release || item.year,
      ...(item.languages || []).slice(0, 2),
      item.status,
    ].filter(Boolean);
    $('#detail-badges').innerHTML = badges.map((value, index) => `<span class="badge ${index === 0 ? escapeAttribute(item.maturity || '') : ''}">${escapeHTML(value)}</span>`).join('');

    const nodeRelations = relationsForNode(id, family);
    const relationMarkup = nodeRelations.length ? nodeRelations.map((edge) => {
      const kind = edgeClass(edge);
      const otherId = edge.from === id ? edge.to : edge.from;
      const arrow = edge.from === id ? '→' : '←';
      return `<div class="detail-relation ${kind}"><strong>${escapeHTML(edge.label_ja || relationLabel(edge.type))}</strong><br>${arrow} ${escapeHTML(nodeName(otherId))} · ${kind === 'verified' ? '確認済み' : kind === 'grouping' ? '分類関係' : '要追加調査'}</div>`;
    }).join('') : '<p>記録済みの関係はありません。</p>';

    const sources = asArray(item.sources).map((source) => {
      const url = safeURL(source.url);
      return url ? `<li><a href="${escapeAttribute(url)}" target="_blank" rel="noreferrer">${escapeHTML(source.label || source.kind || 'Source')}</a></li>` : '';
    }).join('');
    const repository = safeURL(item.repository);
    const website = safeURL(item.website);
    const familyMemberships = familiesForNode(id);

    $('#detail-content').innerHTML = `
      <p class="eyebrow">${escapeHTML(categoryLabel(item.category))}</p>
      <h2 id="detail-title" class="drawer-title">${escapeHTML(item.name)}</h2>
      <p class="drawer-subtitle">${escapeHTML(item.summary_ja || item.problem_ja || '概要を追加調査中です。')}</p>

      <div class="drawer-actions">
        ${repository ? `<a class="button button-secondary" href="${escapeAttribute(repository)}" target="_blank" rel="noreferrer">Repository</a>` : ''}
        ${website && website !== repository ? `<a class="button button-secondary" href="${escapeAttribute(website)}" target="_blank" rel="noreferrer">Official site</a>` : ''}
        ${item.node_class === 'framework' ? `<button class="button button-primary" type="button" data-compare-add="${escapeAttribute(id)}">比較に追加</button>` : ''}
        ${familyMemberships.slice(0, 3).map((membership) => `<button class="button button-secondary" type="button" data-family-open="${escapeAttribute(membership.id)}" data-family-node="${escapeAttribute(id)}">${escapeHTML(membership.name_ja)}で見る</button>`).join('')}
      </div>

      <section class="detail-section"><h3>何を解決しようとしたか</h3><p>${escapeHTML(item.problem_ja || item.summary_ja || '追加調査中です。')}</p></section>
      <section class="detail-section"><h3>歴史・背景</h3><p>${escapeHTML(item.history_ja || '追加調査中です。')}</p></section>
      <section class="detail-section"><h3>設計の中心</h3><p>${escapeHTML(item.design_ja || item.primary_abstraction_ja || '追加調査中です。')}</p></section>
      <section class="detail-section"><h3>Data model</h3><p>${escapeHTML(item.data_model_ja || '永続化 model を内蔵しない、または追加調査中です。')}</p></section>
      <section class="detail-section"><h3>Architecture map</h3>${renderArchitecture(item)}</section>
      <section class="detail-section"><div class="detail-two-col"><div class="detail-box"><h4>メリット</h4>${listHTML(item.strengths_ja)}</div><div class="detail-box"><h4>デメリット / Trade-off</h4>${listHTML(item.tradeoffs_ja)}</div></div></section>
      <section class="detail-section"><div class="detail-two-col"><div class="detail-box"><h4>向いている用途</h4>${listHTML(item.best_for_ja)}</div><div class="detail-box"><h4>避ける場面</h4>${listHTML(item.avoid_when_ja)}</div></div></section>
      <section class="detail-section"><h3>影響・依存・派生関係</h3><div class="detail-relations">${relationMarkup}</div></section>
      <section class="detail-section"><h3>一次資料・公式資料</h3>${sources ? `<ul class="source-list">${sources}</ul>` : '<p>source の追加調査中です。</p>'}</section>
      <section class="detail-section"><h3>Verification</h3><p>level: <strong>${escapeHTML(verification.level || item.node_class || 'unknown')}</strong> / as of: <strong>${escapeHTML(verification.as_of || stats.as_of || 'unknown')}</strong></p></section>
    `;

    drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    $('.drawer-close')?.focus();
  }

  function closeDrawer() {
    const drawer = $('#detail-drawer');
    drawer.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    state.lastFocusedElement?.focus?.();
  }

  function setupDrawer() {
    $$('[data-close-drawer]').forEach((element) => element.addEventListener('click', closeDrawer));
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && $('#detail-drawer').classList.contains('is-open')) closeDrawer();
    });
  }

  // ---------------------------------------------------------------------------
  // Catalog
  // ---------------------------------------------------------------------------

  function setupCatalog() {
    fillSelect('#filter-category', unique(frameworks.map((item) => item.category)), categoryLabel);
    fillSelect('#filter-language', unique(frameworks.flatMap((item) => item.languages || [])));
    fillSelect('#filter-status', unique(frameworks.map((item) => item.status)));
    ['#catalog-search', '#filter-category', '#filter-language', '#filter-maturity', '#filter-status', '#catalog-sort'].forEach((selector) => {
      $(selector).addEventListener('input', () => {
        state.catalogPage = 1;
        renderCatalog();
      });
    });
    $('#clear-filters').addEventListener('click', () => {
      $('#catalog-search').value = '';
      $('#filter-category').value = '';
      $('#filter-language').value = '';
      $('#filter-maturity').value = '';
      $('#filter-status').value = '';
      $('#catalog-sort').value = 'name';
      state.catalogPage = 1;
      renderCatalog();
    });
    renderCatalog();
  }

  function catalogQueryRank(item, query) {
    if (!query) return 0;
    const name = normalize(item.name);
    const aliases = asArray(item.aliases).map(normalize);
    if (name === query || aliases.includes(query)) return 0;
    if (name.startsWith(query) || aliases.some((alias) => alias.startsWith(query))) return 1;
    if (name.includes(query) || aliases.some((alias) => alias.includes(query))) return 2;
    return 3;
  }

  function filteredCatalog() {
    const query = normalize($('#catalog-search').value);
    const category = $('#filter-category').value;
    const language = $('#filter-language').value;
    const maturity = $('#filter-maturity').value;
    const status = $('#filter-status').value;
    const sort = $('#catalog-sort').value;
    const result = frameworks
      .filter((item) => !query || item.__search.includes(query))
      .filter((item) => !category || item.category === category)
      .filter((item) => !language || (item.languages || []).includes(language))
      .filter((item) => !maturity || item.maturity === maturity)
      .filter((item) => !status || item.status === status);

    result.sort((a, b) => {
      const relevance = catalogQueryRank(a, query) - catalogQueryRank(b, query);
      if (relevance) return relevance;
      if (sort === 'year') {
        const yearA = Number.parseInt(a.first_release, 10) || 9999;
        const yearB = Number.parseInt(b.first_release, 10) || 9999;
        return yearA - yearB || a.name.localeCompare(b.name, 'ja');
      }
      if (sort === 'depth') return depthRank(a.maturity) - depthRank(b.maturity) || a.name.localeCompare(b.name, 'ja');
      return a.name.localeCompare(b.name, 'ja');
    });
    return result;
  }

  function frameworkCard(item) {
    return `
      <article class="framework-card">
        <div class="card-top">
          <div><h3>${escapeHTML(item.name)}</h3><div class="card-meta">${escapeHTML(categoryLabel(item.category))} · ${escapeHTML(item.first_release || 'year不明')}</div></div>
          <span class="badge ${escapeAttribute(item.maturity)}">${escapeHTML(item.maturity)}</span>
        </div>
        <p class="framework-summary">${escapeHTML(truncate(item.problem_ja || item.summary_ja, 185))}</p>
        <div class="badge-row">
          ${(item.languages || []).slice(0, 3).map((language) => `<span class="badge">${escapeHTML(language)}</span>`).join('')}
          <span class="badge status-${escapeAttribute(item.status || '')}">${escapeHTML(item.status || 'unknown')}</span>
          <span class="badge">${escapeHTML(item.kind || 'framework')}</span>
        </div>
        <div class="card-actions">
          <button class="primary-mini" type="button" data-detail-id="${escapeAttribute(item.id)}">背景・メリデメ</button>
          <button type="button" data-compare-add="${escapeAttribute(item.id)}">比較に追加</button>
          ${familiesForNode(item.id).length ? `<button type="button" data-family-open="${escapeAttribute(familiesForNode(item.id)[0].id)}" data-family-node="${escapeAttribute(item.id)}">家系図</button>` : ''}
        </div>
      </article>
    `;
  }

  function renderPagination(total) {
    const pages = Math.max(1, Math.ceil(total / state.catalogPageSize));
    state.catalogPage = Math.min(state.catalogPage, pages);
    if (pages <= 1) {
      $('#catalog-pagination').innerHTML = '';
      return;
    }
    const candidates = unique([1, pages, state.catalogPage - 2, state.catalogPage - 1, state.catalogPage, state.catalogPage + 1, state.catalogPage + 2])
      .filter((page) => page >= 1 && page <= pages)
      .sort((a, b) => a - b);
    const parts = [];
    let previous = 0;
    candidates.forEach((page) => {
      if (previous && page - previous > 1) parts.push('<span>…</span>');
      parts.push(`<button type="button" data-catalog-page="${page}" class="${page === state.catalogPage ? 'is-active' : ''}">${page}</button>`);
      previous = page;
    });
    $('#catalog-pagination').innerHTML = parts.join('');
  }

  function renderCatalog() {
    const result = filteredCatalog();
    const start = (state.catalogPage - 1) * state.catalogPageSize;
    const items = result.slice(start, start + state.catalogPageSize);
    $('#catalog-count').textContent = `${result.length.toLocaleString()}件中 ${result.length ? start + 1 : 0}–${Math.min(start + items.length, result.length)}件を表示`;
    $('#catalog-grid').innerHTML = items.map(frameworkCard).join('') || '<div class="detail-box"><p>条件に一致する項目はありません。</p></div>';
    renderPagination(result.length);
  }

  // ---------------------------------------------------------------------------
  // Compare
  // ---------------------------------------------------------------------------

  const COMPARE_ROWS = [
    ['分類', (item) => `${categoryLabel(item.category)} / ${item.subcategory || item.kind || ''}`],
    ['何を解決するか', (item) => item.problem_ja],
    ['歴史・背景', (item) => item.history_ja],
    ['中核設計', (item) => item.design_ja || item.primary_abstraction_ja],
    ['中心 abstraction', (item) => item.primary_abstraction_ja],
    ['Control flow', (item) => item.control_flow_ja],
    ['Data model', (item) => item.data_model_ja],
    ['Routing', (item) => item.routing_ja],
    ['DI', (item) => item.dependency_injection_ja],
    ['State model', (item) => item.state_model_ja],
    ['Concurrency', (item) => item.concurrency_ja],
    ['Deployment', (item) => item.deployment_ja],
    ['Testing', (item) => item.testing_ja],
    ['メリット', (item) => item.strengths_ja],
    ['Trade-off', (item) => item.tradeoffs_ja],
    ['向いている用途', (item) => item.best_for_ja],
    ['避ける場面', (item) => item.avoid_when_ja],
    ['Migration cost', (item) => item.migration_cost_ja],
  ];

  function compareSearchResults(query) {
    const normalized = normalize(query);
    if (!normalized) return [];
    return frameworks
      .filter((item) => item.__search.includes(normalized) && !state.compareIds.includes(item.id))
      .sort((a, b) => depthRank(a.maturity) - depthRank(b.maturity) || a.name.localeCompare(b.name, 'ja'))
      .slice(0, 8);
  }

  function renderCompareSearch() {
    const input = $('#compare-search');
    const results = compareSearchResults(input.value);
    const box = $('#compare-search-results');
    if (!input.value.trim()) {
      box.hidden = true;
      return;
    }
    box.hidden = false;
    box.innerHTML = results.length ? results.map((item) => `
      <button type="button" class="search-result-button" data-compare-add="${escapeAttribute(item.id)}"><span><strong>${escapeHTML(item.name)}</strong><small>${escapeHTML(categoryLabel(item.category))} · ${(item.languages || []).map(escapeHTML).join(' / ')}</small></span><span class="badge ${escapeAttribute(item.maturity)}">${escapeHTML(item.maturity)}</span></button>
    `).join('') : '<div class="filter-note">該当項目はありません。</div>';
  }

  function addToCompare(id, navigate = false) {
    if (!nodeMap.has(id) || nodeMap.get(id).node_class !== 'framework') return;
    if (state.compareIds.includes(id)) {
      showToast('すでに比較に入っています');
      if (navigate) showView('compare');
      return;
    }
    if (state.compareIds.length >= 4) {
      showToast('比較は最大4件です。1件外してから追加してください');
      return;
    }
    state.compareIds.push(id);
    renderCompare();
    showToast(`${nodeName(id)} を比較に追加しました`);
    if (navigate) {
      closeDrawer();
      showView('compare');
    }
  }

  function removeFromCompare(id) {
    state.compareIds = state.compareIds.filter((value) => value !== id);
    renderCompare();
  }

  function renderCompareCell(value) {
    if (Array.isArray(value)) return value.length ? `<ul>${value.map((item) => `<li>${escapeHTML(item)}</li>`).join('')}</ul>` : '追加調査中';
    return escapeHTML(value || '追加調査中');
  }

  function renderCompare() {
    $('#compare-selection').innerHTML = state.compareIds.map((id) => `<span class="compare-chip">${escapeHTML(nodeName(id))}<button type="button" data-compare-remove="${escapeAttribute(id)}" aria-label="${escapeAttribute(nodeName(id))}を比較から外す">×</button></span>`).join('');
    const items = state.compareIds.map((id) => nodeMap.get(id)).filter(Boolean);
    if (!items.length) {
      $('#compare-table').innerHTML = '<tbody><tr><td class="compare-empty">上の検索欄から比較する framework を追加してください。</td></tr></tbody>';
      return;
    }
    $('#compare-table').innerHTML = `
      <thead><tr><th>比較軸</th>${items.map((item) => `<th><button class="relationship-node-button" type="button" data-detail-id="${escapeAttribute(item.id)}">${escapeHTML(item.name)}</button><div class="card-meta">${escapeHTML((item.languages || []).join(' / '))} · ${escapeHTML(item.first_release || '')}</div></th>`).join('')}</tr></thead>
      <tbody>${COMPARE_ROWS.map(([label, getter]) => `<tr><th scope="row">${escapeHTML(label)}</th>${items.map((item) => `<td>${renderCompareCell(getter(item))}</td>`).join('')}</tr>`).join('')}</tbody>
    `;
  }

  function setupCompare() {
    $('#compare-search').addEventListener('input', renderCompareSearch);
    $('#compare-search').addEventListener('focus', renderCompareSearch);
    document.addEventListener('click', (event) => {
      if (!event.target.closest('.compare-add')) $('#compare-search-results').hidden = true;
    });
    renderCompare();
  }

  // ---------------------------------------------------------------------------
  // Timeline
  // ---------------------------------------------------------------------------

  function setupHistory() {
    fillSelect('#history-category', unique(timeline.map((item) => item.category)));
    $('#history-category').addEventListener('change', renderTimeline);
    $('#history-search').addEventListener('input', renderTimeline);
    renderTimeline();
  }

  function renderTimeline() {
    const category = $('#history-category').value;
    const query = normalize($('#history-search').value);
    const items = timeline
      .filter((item) => !category || item.category === category)
      .filter((item) => !query || normalize([item.date, item.title, item.category, item.summary_ja, ...(item.nodes || []).map(nodeName)].join(' ')).includes(query))
      .slice()
      .sort((a, b) => String(a.date).localeCompare(String(b.date)));
    $('#timeline').innerHTML = items.map((item) => `
      <article class="timeline-event">
        <time class="timeline-date" datetime="${escapeAttribute(item.date)}">${escapeHTML(item.date)}</time>
        <span class="timeline-dot" aria-hidden="true"></span>
        <div class="timeline-card">
          <p class="eyebrow">${escapeHTML(item.category || 'history')}</p>
          <h3>${escapeHTML(item.title)}</h3>
          <p>${escapeHTML(item.summary_ja || '')}</p>
          <div class="timeline-nodes">
            ${(item.nodes || []).map((id) => `<button class="badge" type="button" data-detail-id="${escapeAttribute(id)}">${escapeHTML(nodeName(id))}</button>`).join('')}
            ${item.source_url ? `<a class="badge" href="${escapeAttribute(item.source_url)}" target="_blank" rel="noreferrer">Source</a>` : ''}
          </div>
        </div>
      </article>
    `).join('') || '<div class="detail-box"><p>条件に一致する歴史イベントはありません。</p></div>';
  }

  // ---------------------------------------------------------------------------
  // Research issues
  // ---------------------------------------------------------------------------

  function issueMarkdown(item) {
    const labels = (item.labels || []).join(',');
    const acceptance = asArray(item.acceptance_ja).map((line) => `- [ ] ${line}`).join('\n');
    return `---\ntitle: "[${item.id}] ${item.title}"\nlabels: "${labels}"\n---\n\n## 背景\n\n${item.body_ja || ''}\n\n## 完了条件\n\n${acceptance || '- [ ] 調査結果と一次資料を記録する'}\n\n## 証拠の扱い\n\n- 公式文書・maintainer-authored source・一次資料を優先する\n- 直接の影響が確認できない場合は \`needs-evidence\` のままにする\n- 類似性だけで影響や後継を断定しない\n- 確認日と source URL を記録する\n`;
  }

  async function copyText(text, message) {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.append(textarea);
      textarea.select();
      document.execCommand('copy');
      textarea.remove();
    }
    showToast(message);
  }

  function setupIssues() {
    $('#issue-priority').addEventListener('change', renderIssues);
    $('#issue-search').addEventListener('input', renderIssues);
    $('#copy-issue-command').addEventListener('click', () => copyText('python scripts/create_issues.py --repo OWNER/REPO --dry-run', 'command をコピーしました'));
    renderIssues();
  }

  function renderIssues() {
    const priority = $('#issue-priority').value;
    const query = normalize($('#issue-search').value);
    const items = researchGaps
      .filter((item) => !priority || item.priority === priority)
      .filter((item) => !query || normalize([item.id, item.title, item.body_ja, ...(item.labels || []), ...asArray(item.acceptance_ja)].join(' ')).includes(query))
      .sort((a, b) => a.priority.localeCompare(b.priority) || a.id.localeCompare(b.id));
    $('#issue-grid').innerHTML = items.map((item) => {
      const file = issueFiles.get(item.id);
      return `
        <article class="issue-card">
          <span class="priority ${escapeAttribute(item.priority.toLocaleLowerCase())}">${escapeHTML(item.priority)}</span>
          <h3>${escapeHTML(item.title)}</h3>
          <p>${escapeHTML(item.body_ja || '')}</p>
          <strong>完了条件</strong>
          ${listHTML(item.acceptance_ja)}
          <div class="badge-row">${(item.labels || []).map((label) => `<span class="badge">${escapeHTML(label)}</span>`).join('')}</div>
          <div class="issue-card-footer">
            <button class="button button-secondary" type="button" data-copy-issue="${escapeAttribute(item.id)}">Markdown をコピー</button>
            ${file ? `<a class="button button-secondary" href="research-issues/${escapeAttribute(file)}">.md を開く</a>` : ''}
          </div>
        </article>
      `;
    }).join('') || '<div class="detail-box"><p>条件に一致する Issue はありません。</p></div>';
  }

  // ---------------------------------------------------------------------------
  // Delegated actions
  // ---------------------------------------------------------------------------

  function setupActions() {
    document.addEventListener('click', (event) => {
      const detail = event.target.closest('[data-detail-id]');
      if (detail) {
        $('#global-search-results').hidden = true;
        $('#compare-search-results').hidden = true;
        openDrawer(detail.dataset.detailId, activeFamily());
        return;
      }

      const compareAdd = event.target.closest('[data-compare-add]');
      if (compareAdd) {
        addToCompare(compareAdd.dataset.compareAdd, compareAdd.closest('.drawer-content') !== null);
        $('#compare-search').value = '';
        $('#compare-search-results').hidden = true;
        return;
      }

      const compareRemove = event.target.closest('[data-compare-remove]');
      if (compareRemove) {
        removeFromCompare(compareRemove.dataset.compareRemove);
        return;
      }

      const familyOpen = event.target.closest('[data-family-open]');
      if (familyOpen) {
        closeDrawer();
        showView('family');
        setActiveFamily(familyOpen.dataset.familyOpen, true);
        window.setTimeout(() => {
          highlightGraphNode(familyOpen.dataset.familyNode || '');
          const node = $(`[data-graph-node-id="${CSS.escape(familyOpen.dataset.familyNode || '')}"]`);
          node?.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
        }, 250);
        return;
      }

      const page = event.target.closest('[data-catalog-page]');
      if (page) {
        state.catalogPage = Number(page.dataset.catalogPage) || 1;
        renderCatalog();
        $('.catalog-results')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        return;
      }

      const issue = event.target.closest('[data-copy-issue]');
      if (issue) {
        const item = researchGaps.find((gap) => gap.id === issue.dataset.copyIssue);
        if (item) copyText(issueMarkdown(item), `${item.id} の Markdown をコピーしました`);
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Init
  // ---------------------------------------------------------------------------

  renderStats();
  setupNavigation();
  setupFamily();
  setupCatalog();
  setupCompare();
  setupHistory();
  setupIssues();
  setupDrawer();
  setupActions();
})();
