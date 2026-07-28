/* global initSqlJs */

const state = {
  db: null,
  currentPage: 1,
  pageSize: 40,
  totalRows: 0,
  cellTypeIndex: null,
  geneAliases: null,
  searchCellTypes: new Map(),
  searchMatches: new Map(),
};

const el = {
  tabs: Array.from(document.querySelectorAll(".tab")),
  panels: {
    search: document.getElementById("panelSearch"),
    data: document.getElementById("panelData"),
    methods: document.getElementById("panelMethods"),
    about: document.getElementById("panelAbout"),
  },
  countPapers: document.getElementById("countPapers"),
  countClaims: document.getElementById("countClaims"),
  countCellTypes: document.getElementById("countCellTypes"),
  medianGenesPerCellType: document.getElementById("medianGenesPerCellType"),
  loadStrip: document.getElementById("loadStrip"),
  loadStatusText: document.getElementById("loadStatusText"),
  loadStatusMeta: document.getElementById("loadStatusMeta"),
  loadBar: document.querySelector(".load-bar"),
  loadBarFill: document.getElementById("loadBarFill"),
  queryInput: document.getElementById("queryInput"),
  queryButton: document.getElementById("queryButton"),
  querySummary: document.getElementById("querySummary"),
  searchResults: document.getElementById("searchResults"),
  examples: Array.from(document.querySelectorAll(".examples button")),
  collectionFilter: document.getElementById("collectionFilter"),
  directionFilter: document.getElementById("directionFilter"),
  groundingFilter: document.getElementById("groundingFilter"),
  organismFilter: document.getElementById("organismFilter"),
  tableSearchInput: document.getElementById("tableSearchInput"),
  tableBody: document.querySelector("#evidenceTable tbody"),
  tableCount: document.getElementById("tableCount"),
  pageLabel: document.getElementById("pageLabel"),
  prevPage: document.getElementById("prevPage"),
  nextPage: document.getElementById("nextPage"),
  statusNote: document.getElementById("statusNote"),
};

function esc(value) {
  if (value == null) return "";
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function fmtInt(value) {
  return new Intl.NumberFormat("en-US").format(Number(value) || 0);
}

function formatOrganism(value) {
  return String(value || "")
    .split("_")
    .map((part, index) => {
      const lower = part.toLowerCase();
      return index === 0 ? lower.charAt(0).toUpperCase() + lower.slice(1) : lower;
    })
    .join(" ");
}

function runRows(sql, params = []) {
  const result = state.db.exec(sql, params);
  if (!result.length) return [];
  const { columns, values } = result[0];
  return values.map((row) => Object.fromEntries(columns.map((column, index) => [column, row[index]])));
}

function runScalar(sql, params = []) {
  const rows = runRows(sql, params);
  if (!rows.length) return 0;
  return Number(rows[0][Object.keys(rows[0])[0]]) || 0;
}

function setActiveTab(name) {
  el.tabs.forEach((button) => {
    const active = button.dataset.tab === name;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  Object.entries(el.panels).forEach(([panelName, panel]) => {
    panel.hidden = panelName !== name;
  });
}

function identifierUrl(curie) {
  if (!curie) return "";
  if (/^ENSG\d+$/i.test(curie)) {
    return `https://www.ensembl.org/id/${encodeURIComponent(curie)}`;
  }
  return `https://identifiers.org/${encodeURIComponent(curie)}`;
}

function identifierHtml(curie) {
  if (!curie) return '<span class="unresolved">unresolved</span>';
  const database = /^ENSG\d+$/i.test(curie) ? "Ensembl" : "Identifiers.org";
  return `<a class="identifier" href="${identifierUrl(curie)}" target="_blank" rel="noopener" title="Open ${esc(curie)} in ${database}">${esc(curie)}</a>`;
}

function paperUrl(row) {
  if (row.doi) {
    const encodedDoi = row.doi.split("/").map(encodeURIComponent).join("/");
    return `https://doi.org/${encodedDoi}`;
  }
  return row.source_url;
}

function parseTerms(value) {
  if (!value) return [];
  try {
    const terms = JSON.parse(value);
    return Array.isArray(terms) ? terms : [];
  } catch (_error) {
    return [];
  }
}

function termKey(term) {
  return `${term.curie || ""}\t${String(term.label || "").toLowerCase()}`;
}

function uniqueTerms(terms) {
  const seen = new Set();
  return terms.filter((term) => {
    const key = termKey(term);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function renderTermLabels(terms, missingText) {
  const values = uniqueTerms(terms);
  if (!values.length) return `<span class="missing-context">${esc(missingText)}</span>`;
  return values.map((term) => esc(term.label)).join(", ");
}

function setLoadProgress(ratio, text) {
  const bounded = Math.max(0, Math.min(1, ratio));
  const percent = Math.round(bounded * 100);
  el.loadStatusText.textContent = text;
  el.loadStatusMeta.textContent = `${percent}%`;
  el.loadBarFill.style.width = `${percent}%`;
  el.loadBar.setAttribute("aria-valuenow", String(percent));
}

async function fetchWithProgress(url, onProgress) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status} while loading ${url}`);
  const total = Number(response.headers.get("content-length")) || 0;
  if (!response.body || !total) {
    onProgress(0.45, "Reading database");
    return response.arrayBuffer();
  }
  const reader = response.body.getReader();
  const chunks = [];
  let received = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    received += value.length;
    onProgress(received / total, `Loading database · ${fmtInt(received)} of ${fmtInt(total)} bytes`);
  }
  const merged = new Uint8Array(received);
  let offset = 0;
  chunks.forEach((chunk) => {
    merged.set(chunk, offset);
    offset += chunk.length;
  });
  return merged.buffer;
}

function updateSummaryCards() {
  const papers = runScalar("SELECT COUNT(*) FROM papers");
  const claims = runScalar("SELECT COUNT(*) FROM claims");
  const panelSizes = runRows(
    `WITH evidence AS (
       SELECT CASE
                WHEN target_curie IS NOT NULL THEN 'id:' || target_curie
                ELSE 'label:' || lower(trim(target_label))
              END AS celltype_key,
              COALESCE(gene_curie, upper(gene_symbol)) AS gene_key
       FROM web_marker_evidence
       WHERE trim(target_label)<>'' AND trim(gene_symbol)<>''
     ), panel_sizes AS (
       SELECT celltype_key, COUNT(DISTINCT gene_key) AS gene_count
       FROM evidence
       GROUP BY celltype_key
     )
     SELECT gene_count
     FROM panel_sizes
     ORDER BY gene_count`,
  ).map((row) => Number(row.gene_count));
  const midpoint = Math.floor(panelSizes.length / 2);
  const medianGenes = panelSizes.length % 2
    ? panelSizes[midpoint]
    : (panelSizes[midpoint - 1] + panelSizes[midpoint]) / 2;

  el.countPapers.textContent = fmtInt(papers);
  el.countClaims.textContent = fmtInt(claims);
  el.countCellTypes.textContent = fmtInt(panelSizes.length);
  el.medianGenesPerCellType.textContent = Number.isInteger(medianGenes)
    ? fmtInt(medianGenes)
    : Number(medianGenes).toFixed(1);
  document.querySelectorAll('[data-stat="papers"]').forEach((node) => {
    node.textContent = fmtInt(papers);
  });
}

function loadOrganismOptions() {
  const rows = runRows(
    `SELECT normalized_label AS label, ontology_term AS curie
     FROM terms
     WHERE term_type='organism'
     GROUP BY normalized_label, ontology_term
     ORDER BY normalized_label COLLATE NOCASE`,
  );
  rows.forEach((row) => {
    const option = document.createElement("option");
    option.value = row.curie || row.label;
    option.textContent = row.label;
    el.organismFilter.appendChild(option);
  });
}

function textPredicate(alias, query) {
  const like = `%${query.toLowerCase()}%`;
  const fields = [
    "title",
    "doi",
    "organism_label",
    "organism_curie",
    "target_label",
    "target_curie",
    "gene_symbol",
    "gene_curie",
    "summary",
    "span_literal",
  ];
  const fieldSql = fields.map((field) => `lower(COALESCE(${alias}.${field}, '')) LIKE ?`);
  const sql = `(
    ${fieldSql.join(" OR ")}
    OR EXISTS (
      SELECT 1 FROM terms search_term
      WHERE search_term.claim_key=${alias}.claim_key
        AND (
          lower(search_term.normalized_label) LIKE ?
          OR (
            lower(COALESCE(search_term.ontology_term, '')) LIKE ?
            AND (
              search_term.term_type NOT IN ('celltype','comparison')
              OR EXISTS (
                SELECT 1 FROM cell_ontology_label_audit accepted_term
                WHERE accepted_term.term_type=search_term.term_type
                  AND accepted_term.curie=search_term.ontology_term
                  AND accepted_term.observed_label=search_term.normalized_label
                  AND accepted_term.semantic_exact=1
              )
            )
          )
        )
    )
  )`;
  return { sql, params: Array(fields.length + 2).fill(like) };
}

function mainSearchPredicate(alias, query) {
  const like = `%${query.toLowerCase()}%`;
  const fields = ["target_label", "target_canonical_label", "target_curie", "gene_symbol", "gene_curie"];
  return {
    sql: `(${fields.map((field) => `lower(COALESCE(${alias}.${field}, '')) LIKE ?`).join(" OR ")})`,
    params: Array(fields.length).fill(like),
  };
}

function tableWhere() {
  const clauses = [];
  const params = [];
  if (el.collectionFilter.value !== "all") {
    clauses.push("w.collection=?");
    params.push(el.collectionFilter.value);
  }
  if (el.directionFilter.value !== "all") {
    clauses.push("w.direction=?");
    params.push(el.directionFilter.value);
  }
  if (el.groundingFilter.value === "verified") clauses.push("w.target_semantic_exact=1");
  if (el.groundingFilter.value === "unverified") clauses.push("w.target_semantic_exact=0");
  if (el.organismFilter.value !== "all") {
    clauses.push("COALESCE(w.organism_curie, w.organism_label)=?");
    params.push(el.organismFilter.value);
  }
  const query = el.tableSearchInput.value.trim();
  if (query) {
    const predicate = textPredicate("w", query);
    clauses.push(predicate.sql);
    params.push(...predicate.params);
  }
  return { sql: clauses.length ? `WHERE ${clauses.join(" AND ")}` : "", params };
}

function renderTarget(row) {
  const identifier = row.target_curie ? `<div>${identifierHtml(row.target_curie)}</div>` : "";
  return `
    <strong>${esc(row.target_label)}</strong>
    ${identifier}
  `;
}

function renderGene(row) {
  const sign = row.direction === "negative" ? "−" : "+";
  const identifier = row.gene_curie ? `<div>${identifierHtml(row.gene_curie)}</div>` : "";
  return `
    <span class="direction direction-${esc(row.direction)}" title="${esc(row.direction)} marker">${sign}</span>
    <strong>${esc(row.gene_symbol)}</strong>
    ${identifier}
  `;
}

function renderTableRows(rows) {
  el.tableBody.innerHTML = rows
    .map((row) => {
      const comparisons = parseTerms(row.comparison_terms_json);
      const tissues = parseTerms(row.tissue_terms_json);
      return `
        <tr>
          <td class="paper-cell">
            <a href="${esc(paperUrl(row))}" target="_blank" rel="noopener">${esc(row.title)}</a>
          </td>
          <td class="entity-cell">${renderTarget(row)}</td>
          <td class="entity-cell">${renderGene(row)}</td>
          <td class="context-cell">${renderTermLabels(comparisons, "Not reported")}</td>
          <td class="context-cell">${renderTermLabels(tissues, "Not reported")}</td>
          <td class="statement-cell">${esc(row.summary)}</td>
        </tr>`;
    })
    .join("");
}

function updatePager() {
  const pages = Math.max(1, Math.ceil(state.totalRows / state.pageSize));
  state.currentPage = Math.min(state.currentPage, pages);
  el.pageLabel.textContent = `Page ${state.currentPage} of ${pages}`;
  el.prevPage.disabled = state.currentPage <= 1;
  el.nextPage.disabled = state.currentPage >= pages;
}

function refreshTable() {
  if (!state.db) return;
  const where = tableWhere();
  state.totalRows = runScalar(`SELECT COUNT(*) FROM web_marker_evidence w ${where.sql}`, where.params);
  const offset = (state.currentPage - 1) * state.pageSize;
  const rows = runRows(
    `SELECT * FROM web_marker_evidence w
     ${where.sql}
     ORDER BY w.title COLLATE NOCASE, w.target_label COLLATE NOCASE,
              w.gene_symbol COLLATE NOCASE, w.claim_key
     LIMIT ? OFFSET ?`,
    [...where.params, state.pageSize, offset],
  );
  renderTableRows(rows);
  el.tableCount.textContent = `${fmtInt(state.totalRows)} evidence rows`;
  updatePager();
}

function parseGeneQuery(value) {
  return new Set(
    String(value || "")
      .split(/[\s,;]+/)
      .map((item) => item.trim().toUpperCase())
      .filter(Boolean),
  );
}

function cellTypeKeySql(alias) {
  return `CASE
    WHEN ${alias}.target_curie IS NOT NULL THEN 'id:' || ${alias}.target_curie
    ELSE 'label:' || lower(trim(${alias}.target_label))
  END`;
}

function loadCellTypeIndex() {
  if (state.cellTypeIndex) return state.cellTypeIndex;
  const cellTypes = new Map();
  const geneAliases = new Set();
  const rows = runRows(
    `SELECT ${cellTypeKeySql("w")} AS celltype_key,
            w.target_label, w.target_curie, w.target_canonical_label,
            w.gene_symbol, w.gene_curie, w.direction
     FROM web_marker_evidence w
     ORDER BY celltype_key, w.gene_symbol COLLATE NOCASE`,
  );
  rows.forEach((row) => {
    if (!cellTypes.has(row.celltype_key)) {
      cellTypes.set(row.celltype_key, {
        cellTypeKey: row.celltype_key,
        targetLabel: row.target_label,
        targetCurie: row.target_curie,
        canonicalLabel: row.target_canonical_label,
        labels: new Set(),
        markers: new Map(),
      });
    }
    const cellType = cellTypes.get(row.celltype_key);
    cellType.labels.add(row.target_label);
    if (row.gene_symbol) {
      const markerKey = row.gene_curie || row.gene_symbol.toUpperCase();
      const marker = cellType.markers.get(markerKey) || {
        symbol: row.gene_symbol,
        curie: row.gene_curie,
        directions: new Set(),
        aliases: new Set(),
      };
      marker.aliases.add(row.gene_symbol.toUpperCase());
      if (row.gene_curie) marker.aliases.add(row.gene_curie.toUpperCase());
      marker.aliases.forEach((alias) => geneAliases.add(alias));
      if (row.direction) marker.directions.add(row.direction);
      cellType.markers.set(markerKey, marker);
    }
  });
  state.cellTypeIndex = cellTypes;
  state.geneAliases = geneAliases;
  return cellTypes;
}

function loadCellTypeEvidence(cellTypeKeys) {
  if (!cellTypeKeys.length) return [];
  const placeholders = cellTypeKeys.map(() => "?").join(",");
  const rows = runRows(
    `SELECT w.*, ${cellTypeKeySql("w")} AS celltype_key
     FROM web_marker_evidence w
     WHERE ${cellTypeKeySql("w")} IN (${placeholders})
     ORDER BY celltype_key, w.title COLLATE NOCASE, w.claim_key, w.gene_symbol COLLATE NOCASE`,
    cellTypeKeys,
  );
  const grouped = new Map();
  rows.forEach((row) => {
    if (!grouped.has(row.celltype_key)) grouped.set(row.celltype_key, []);
    grouped.get(row.celltype_key).push(row);
  });
  return cellTypeKeys
    .filter((key) => grouped.has(key))
    .map((key) => ({ cellTypeKey: key, rows: grouped.get(key) }));
}

function textSearchCellTypeKeys(query) {
  const normalized = query.toLowerCase();
  const like = `%${normalized}%`;
  const predicate = mainSearchPredicate("w", query);
  const rankSql = `CASE
    WHEN lower(COALESCE(w.target_label, ''))=?
      OR lower(COALESCE(w.target_canonical_label, ''))=?
      OR lower(COALESCE(w.target_curie, ''))=?
      OR lower(COALESCE(w.gene_symbol, ''))=?
      OR lower(COALESCE(w.gene_curie, ''))=? THEN 0
    WHEN lower(COALESCE(w.target_label, '')) LIKE ?
      OR lower(COALESCE(w.target_canonical_label, '')) LIKE ?
      OR lower(COALESCE(w.target_curie, '')) LIKE ?
      OR lower(COALESCE(w.gene_symbol, '')) LIKE ?
      OR lower(COALESCE(w.gene_curie, '')) LIKE ? THEN 1
    ELSE 2 END`;
  const rankParams = [
    normalized, normalized, normalized, normalized, normalized,
    like, like, like, like, like,
  ];
  const total = runScalar(
    `SELECT COUNT(DISTINCT ${cellTypeKeySql("w")})
     FROM web_marker_evidence w
     WHERE ${predicate.sql}`,
    predicate.params,
  );
  const ranked = runRows(
    `SELECT ${cellTypeKeySql("w")} AS celltype_key,
            MIN(${rankSql}) AS rank,
            MIN(COALESCE(w.target_canonical_label, w.target_label)) AS display_label
     FROM web_marker_evidence w
     WHERE ${predicate.sql}
     GROUP BY celltype_key
     ORDER BY rank, display_label COLLATE NOCASE
     LIMIT 12`,
    [...rankParams, ...predicate.params],
  );
  return { ranked, total };
}

function cellTypeMarkers(rows) {
  const markers = new Map();
  rows.forEach((row) => {
    const key = row.gene_curie || row.gene_symbol.toUpperCase();
    if (!markers.has(key)) {
      markers.set(key, { ...row, directions: new Set(), claimKeys: new Set() });
    }
    markers.get(key).directions.add(row.direction);
    markers.get(key).claimKeys.add(row.claim_key);
  });
  return Array.from(markers.values())
    .map((row) => ({
      ...row,
      direction: row.directions.size > 1 ? "mixed" : Array.from(row.directions)[0],
      supportCount: row.claimKeys.size,
    }))
    .sort((a, b) => a.gene_symbol.localeCompare(b.gene_symbol));
}

function contextRecords(rows) {
  const records = new Map();
  rows.forEach((row) => {
    if (!records.has(row.claim_key)) {
      records.set(row.claim_key, { row, markers: new Map() });
    }
    const key = row.gene_curie || row.gene_symbol.toUpperCase();
    if (!records.get(row.claim_key).markers.has(key)) {
      records.get(row.claim_key).markers.set(key, row);
    }
  });
  return Array.from(records.values()).sort((a, b) => (
    a.row.title.localeCompare(b.row.title) || a.row.summary.localeCompare(b.row.summary)
  ));
}

function markerMatches(row, sharedGenes) {
  if (!sharedGenes) return false;
  return [row.gene_symbol, row.gene_curie]
    .filter(Boolean)
    .some((value) => sharedGenes.has(value.toUpperCase()));
}

function markerKey(row) {
  return row.gene_curie || row.gene_symbol.toUpperCase();
}

function markerLabel(row) {
  if (row.direction === "negative") return `−${row.gene_symbol}`;
  if (row.direction === "mixed") return `±${row.gene_symbol}`;
  return row.gene_symbol;
}

function renderMarkerButton(row, sharedGenes) {
  const shared = markerMatches(row, sharedGenes);
  const directionClass = row.direction === "negative" ? " marker-negative" : "";
  const mixedClass = row.direction === "mixed" ? " marker-mixed" : "";
  const sharedClass = shared ? " marker-shared" : "";
  const directionNote = row.direction === "mixed" ? " Reported in both directions." : "";
  const title = `${fmtInt(row.supportCount)} supporting normalized ${row.supportCount === 1 ? "statement" : "statements"}.${directionNote}`;
  return `<button class="marker-chip${directionClass}${mixedClass}${sharedClass}" type="button" data-gene-key="${esc(markerKey(row))}" aria-label="${esc(markerLabel(row))}, ${esc(title)}" aria-pressed="false" title="${esc(title)}"><span>${esc(markerLabel(row))}</span><strong>+${fmtInt(row.supportCount)}</strong></button>`;
}

function sortMarkers(markers) {
  const directionRank = { positive: 0, negative: 1, mixed: 2 };
  return [...markers].sort((a, b) => {
    const directionOrder = (directionRank[a.direction] ?? 3) - (directionRank[b.direction] ?? 3);
    return directionOrder
      || b.supportCount - a.supportCount
      || a.gene_symbol.localeCompare(b.gene_symbol);
  });
}

function renderGeneEvidenceRecord(record) {
  const row = record.row;
  return `
    <section class="evidence-record">
      <a class="evidence-paper" href="${esc(paperUrl(row))}" target="_blank" rel="noopener">${esc(row.title)}</a>
      <p class="evidence-statement">${esc(row.summary)}</p>
      <details class="evidence-source">
        <summary>Exact source text</summary>
        <blockquote>${esc(row.span_literal)}</blockquote>
      </details>
    </section>`;
}

function renderGeneEvidence(cellType, geneKey) {
  const rows = cellType.rows.filter((row) => markerKey(row) === geneKey);
  if (!rows.length) return "";
  const marker = cellTypeMarkers(rows)[0];
  const contexts = contextRecords(rows);
  const papers = new Set(rows.map((row) => row.paper_key));
  const shownContexts = contexts.slice(0, 5);
  const remainingContexts = contexts.length - shownContexts.length;
  return `
    <section class="gene-evidence">
      <header>
        <h4>${esc(marker.gene_symbol)}${marker.gene_curie ? ` <span class="inline-id">(${identifierHtml(marker.gene_curie)})</span>` : ""}</h4>
        <p>${fmtInt(contexts.length)} ${contexts.length === 1 ? "statement" : "statements"} · ${fmtInt(papers.size)} ${papers.size === 1 ? "paper" : "papers"}</p>
      </header>
      <div data-evidence-records>
        ${shownContexts.map(renderGeneEvidenceRecord).join("")}
      </div>
      ${remainingContexts > 0 ? `<button class="show-evidence" type="button" data-expand-evidence="${esc(geneKey)}">Show ${fmtInt(remainingContexts)} more evidence statements</button>` : ""}
    </section>`;
}

function renderCellTypeCard(cellType, match) {
  const rows = cellType.rows;
  const first = rows[0];
  const sharedGenes = match ? match.sharedGenes : null;
  const markers = sortMarkers(cellTypeMarkers(rows));
  const displayLabel = first.target_curie && first.target_canonical_label
    ? first.target_canonical_label
    : first.target_label;
  const inlineId = first.target_curie
    ? ` <span class="inline-id">(${identifierHtml(first.target_curie)})</span>`
    : "";
  return `
    <article class="panel-card" data-celltype-card="${esc(cellType.cellTypeKey)}">
      <header>
        <h3>${esc(displayLabel)}${inlineId}</h3>
      </header>
      <section class="aggregate-panel">
        <div class="marker-list" aria-label="Marker panel">
          ${markers.map((row) => renderMarkerButton(row, sharedGenes)).join("")}
        </div>
      </section>
      <div class="gene-evidence-slot" aria-live="polite"></div>
    </article>`;
}

function renderSearchResults(cellTypes, matches = new Map()) {
  if (!cellTypes.length) {
    el.searchResults.innerHTML = '<div class="empty-state">No cell types matched this query.</div>';
    return;
  }
  state.searchCellTypes = new Map(cellTypes.map((cellType) => [cellType.cellTypeKey, cellType]));
  state.searchMatches = matches;
  el.searchResults.innerHTML = cellTypes
    .map((cellType) => renderCellTypeCard(cellType, matches.get(cellType.cellTypeKey)))
    .join("");
}

function searchByText(query) {
  const result = textSearchCellTypeKeys(query);
  const keys = result.ranked.map((row) => row.celltype_key);
  const cellTypes = loadCellTypeEvidence(keys);
  renderSearchResults(cellTypes);
  const suffix = result.total > cellTypes.length
    ? ` Showing the first ${fmtInt(cellTypes.length)}.`
    : "";
  const unit = result.total === 1 ? "cell type" : "cell types";
  el.querySummary.textContent = `${fmtInt(result.total)} ${unit} matched “${query}”.${suffix}`;
}

function searchByGenes(query) {
  const queryGenes = parseGeneQuery(query);
  if (!queryGenes.size) {
    throw new Error("Enter one or more gene symbols or Ensembl IDs.");
  }
  const ranked = [];
  loadCellTypeIndex().forEach((cellType) => {
    const sharedGenes = new Set();
    queryGenes.forEach((token) => {
      if (Array.from(cellType.markers.values()).some((marker) => marker.aliases.has(token))) {
        sharedGenes.add(token);
      }
    });
    if (!sharedGenes.size) return;
    const unionSize = queryGenes.size + cellType.markers.size - sharedGenes.size;
    ranked.push({
      cellTypeKey: cellType.cellTypeKey,
      score: sharedGenes.size / unionSize,
      sharedGenes,
      sharedCount: sharedGenes.size,
      querySize: queryGenes.size,
      panelSize: cellType.markers.size,
    });
  });
  ranked.sort((a, b) => b.sharedCount - a.sharedCount || b.score - a.score || a.panelSize - b.panelSize);
  const selected = ranked.slice(0, 12);
  const cellTypes = loadCellTypeEvidence(selected.map((row) => row.cellTypeKey));
  const matches = new Map(selected.map((row) => [row.cellTypeKey, row]));
  renderSearchResults(cellTypes, matches);
  const unit = ranked.length === 1 ? "cell type shares" : "cell types share";
  el.querySummary.textContent = `${fmtInt(ranked.length)} ${unit} at least one queried gene; showing the top ${fmtInt(cellTypes.length)}.`;
}

function isGeneSetQuery(query) {
  const genes = parseGeneQuery(query);
  if (genes.size < 2) return false;
  loadCellTypeIndex();
  const recognized = Array.from(genes).filter((gene) => state.geneAliases.has(gene)).length;
  return /[,;]/.test(query) || recognized >= 2;
}

function runSearch() {
  if (!state.db) return;
  const query = el.queryInput.value.trim();
  if (!query) {
    el.querySummary.textContent = "";
    el.searchResults.innerHTML = "";
    return;
  }
  el.queryButton.disabled = true;
  el.querySummary.textContent = "Searching...";
  window.setTimeout(() => {
    try {
      if (isGeneSetQuery(query)) searchByGenes(query);
      else searchByText(query);
    } catch (error) {
      console.error(error);
      el.querySummary.textContent = error.message;
      el.searchResults.innerHTML = "";
    } finally {
      el.queryButton.disabled = false;
    }
  }, 0);
}

function debounce(fn, delay) {
  let timer = null;
  return (...args) => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => fn(...args), delay);
  };
}

function wireEvents() {
  el.tabs.forEach((button) => button.addEventListener("click", () => setActiveTab(button.dataset.tab)));
  el.queryButton.addEventListener("click", runSearch);
  el.queryInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") runSearch();
  });
  el.examples.forEach((button) => button.addEventListener("click", () => {
    el.queryInput.value = button.dataset.query;
    runSearch();
  }));
  el.searchResults.addEventListener("click", (event) => {
    const expandButton = event.target.closest("[data-expand-evidence]");
    if (expandButton) {
      const card = expandButton.closest("[data-celltype-card]");
      const cellType = card ? state.searchCellTypes.get(card.dataset.celltypeCard) : null;
      const records = expandButton.closest(".gene-evidence").querySelector("[data-evidence-records]");
      if (!cellType || !records) return;
      const matchingRows = cellType.rows.filter((row) => markerKey(row) === expandButton.dataset.expandEvidence);
      records.innerHTML = contextRecords(matchingRows).map(renderGeneEvidenceRecord).join("");
      expandButton.remove();
      return;
    }
    const button = event.target.closest("[data-gene-key]");
    if (!button) return;
    const card = button.closest("[data-celltype-card]");
    const cellType = card ? state.searchCellTypes.get(card.dataset.celltypeCard) : null;
    if (!cellType) return;
    const slot = card.querySelector(".gene-evidence-slot");
    const wasActive = button.classList.contains("is-active");
    card.querySelectorAll("[data-gene-key]").forEach((geneButton) => {
      geneButton.classList.remove("is-active");
      geneButton.setAttribute("aria-pressed", "false");
    });
    if (wasActive) {
      slot.innerHTML = "";
      return;
    }
    button.classList.add("is-active");
    button.setAttribute("aria-pressed", "true");
    slot.innerHTML = renderGeneEvidence(cellType, button.dataset.geneKey);
  });

  const resetTable = () => {
    state.currentPage = 1;
    refreshTable();
  };
  [el.collectionFilter, el.directionFilter, el.groundingFilter, el.organismFilter]
    .forEach((control) => control.addEventListener("change", resetTable));
  el.tableSearchInput.addEventListener("input", debounce(resetTable, 220));
  el.prevPage.addEventListener("click", () => {
    state.currentPage = Math.max(1, state.currentPage - 1);
    refreshTable();
  });
  el.nextPage.addEventListener("click", () => {
    state.currentPage += 1;
    refreshTable();
  });
}

async function init() {
  try {
    setLoadProgress(0.01, "Preparing SQLite");
    const sqlPromise = initSqlJs({
      locateFile: (file) => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.2/${file}`,
    });
    const databasePromise = fetchWithProgress("llmarkers.sqlite", setLoadProgress);
    const [SQL, buffer] = await Promise.all([sqlPromise, databasePromise]);
    state.db = new SQL.Database(new Uint8Array(buffer));

    const schema = runRows("SELECT value FROM metadata WHERE key='website_schema_version'");
    if (!schema.length || schema[0].value !== "llmarkers.web-db.v1") {
      throw new Error("The website database does not use llmarkers.web-db.v1.");
    }

    updateSummaryCards();
    loadOrganismOptions();
    wireEvents();
    refreshTable();
    setActiveTab("search");
    setLoadProgress(1, "Database ready");
    el.statusNote.textContent = "Database loaded. Searches run locally in this browser.";
    window.setTimeout(() => el.loadStrip.classList.add("is-hidden"), 450);
  } catch (error) {
    console.error(error);
    setLoadProgress(1, "Database unavailable");
    el.statusNote.textContent = `Failed to load database: ${error.message}`;
  }
}

init();
