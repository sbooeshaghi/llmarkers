/* global initSqlJs */

const PROFILE_EMBED_DIM = 96;
const DEFAULT_PROFILE_WEIGHT = 0.9;
const DEFAULT_CONTEXT_WEIGHT = 0.1;
const state = {
  db: null,
  currentPage: 1,
  pageSize: 50,
  totalRows: 0,
  profiles: [],
};

const textEncoder = new TextEncoder();

const el = {
  tabHome: document.getElementById("tabHome"),
  tabMethods: document.getElementById("tabMethods"),
  tabRaw: document.getElementById("tabRaw"),
  panelHome: document.getElementById("panelHome"),
  panelMethods: document.getElementById("panelMethods"),
  panelRaw: document.getElementById("panelRaw"),
  countPapers: document.getElementById("countPapers"),
  countBenchmarkPapers: document.getElementById("countBenchmarkPapers"),
  countBiorxivPapers: document.getElementById("countBiorxivPapers"),
  countMarkers: document.getElementById("countMarkers"),
  countCellTypes: document.getElementById("countCellTypes"),
  countGenes: document.getElementById("countGenes"),
  profileQueryMode: document.getElementById("profileQueryMode"),
  profileQueryInput: document.getElementById("profileQueryInput"),
  profileQueryButton: document.getElementById("profileQueryButton"),
  profileQuerySummary: document.getElementById("profileQuerySummary"),
  profileResults: document.getElementById("profileResults"),
  profileExamples: Array.from(document.querySelectorAll(".profile-example")),
  collectionFilter: document.getElementById("collectionFilter"),
  sourceTypeFilter: document.getElementById("sourceTypeFilter"),
  pageSizeFilter: document.getElementById("pageSizeFilter"),
  searchInput: document.getElementById("searchInput"),
  tableBody: document.querySelector("#markerTable tbody"),
  tableCount: document.getElementById("tableCount"),
  pageLabel: document.getElementById("pageLabel"),
  prevPage: document.getElementById("prevPage"),
  nextPage: document.getElementById("nextPage"),
  statusNote: document.getElementById("statusNote"),
};

function setActiveTab(name) {
  const isHome = name === "home";
  const isMethods = name === "methods";
  const isRaw = name === "raw";
  el.tabHome.classList.toggle("is-active", isHome);
  el.tabMethods.classList.toggle("is-active", isMethods);
  el.tabRaw.classList.toggle("is-active", isRaw);
  el.tabHome.setAttribute("aria-pressed", String(isHome));
  el.tabMethods.setAttribute("aria-pressed", String(isMethods));
  el.tabRaw.setAttribute("aria-pressed", String(isRaw));
  el.panelHome.hidden = !isHome;
  el.panelMethods.hidden = !isMethods;
  el.panelRaw.hidden = !isRaw;
}

function fmtInt(value) {
  return new Intl.NumberFormat("en-US").format(value ?? 0);
}

function esc(value) {
  if (value == null) return "";
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function toDoiUrl(doi) {
  if (!doi) return "";
  return `https://doi.org/${doi}`;
}

function truncate(value, n = 140) {
  if (!value) return "";
  const text = String(value);
  if (text.length <= n) return text;
  return `${text.slice(0, n - 1)}...`;
}

function runRows(sql, params = []) {
  const result = state.db.exec(sql, params);
  if (!result.length) return [];
  const { columns, values } = result[0];
  return values.map((row) => {
    const obj = {};
    for (let i = 0; i < columns.length; i += 1) {
      obj[columns[i]] = row[i];
    }
    return obj;
  });
}

function runScalar(sql, params = []) {
  const rows = runRows(sql, params);
  if (!rows.length) return 0;
  const first = rows[0];
  return Number(first[Object.keys(first)[0]]) || 0;
}

function normalizeProfileText(value) {
  return String(value || "")
    .toUpperCase()
    .replaceAll("+", " PLUS ")
    .replaceAll("-", " MINUS ")
    .replace(/[^A-Z0-9\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function profileTokens(value) {
  const normalized = normalizeProfileText(value);
  const tokens = normalized.match(/[A-Z0-9]+/g) || [];
  const bigrams = [];
  for (let i = 0; i < tokens.length - 1; i += 1) {
    bigrams.push(`${tokens[i]}_${tokens[i + 1]}`);
  }
  return tokens.concat(bigrams);
}

function expandedTokenSet(tokens) {
  const out = new Set();
  for (const token of tokens) {
    if (!token) continue;
    out.add(token);
    if (token.length > 4 && token.endsWith("S")) {
      out.add(token.slice(0, -1));
    }
  }
  return out;
}

function fnv1a32(text) {
  const bytes = textEncoder.encode(text);
  let hash = 0x811c9dc5;
  for (const byte of bytes) {
    hash ^= byte;
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return hash >>> 0;
}

function embedProfileText(text, dim = PROFILE_EMBED_DIM) {
  const counts = new Map();
  for (const token of profileTokens(text)) {
    counts.set(token, (counts.get(token) || 0) + 1);
  }

  const vec = new Float32Array(dim);
  for (const [token, count] of counts.entries()) {
    const base = fnv1a32(token);
    const weight = 1 + Math.log(count);
    for (let j = 0; j < 4; j += 1) {
      const salt = (((j + 1) * 0x9e3779b9) >>> 0);
      const mixed = (base ^ salt) >>> 0;
      const idx = mixed % dim;
      const sign = ((mixed >>> 31) & 1) === 0 ? 1 : -1;
      vec[idx] += sign * weight;
    }
  }

  let norm = 0;
  for (let i = 0; i < vec.length; i += 1) norm += vec[i] * vec[i];
  norm = Math.sqrt(norm);
  if (!norm) return vec;
  for (let i = 0; i < vec.length; i += 1) vec[i] /= norm;
  return vec;
}

function cosineSimilarity(a, b) {
  let dot = 0;
  let an = 0;
  let bn = 0;
  for (let i = 0; i < a.length; i += 1) {
    dot += a[i] * b[i];
    an += a[i] * a[i];
    bn += b[i] * b[i];
  }
  if (!an || !bn) return 0;
  return dot / Math.sqrt(an * bn);
}

function parseJsonArray(value) {
  if (!value) return [];
  try {
    const parsed = JSON.parse(value);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function parseGeneQuery(value) {
  return new Set(
    String(value || "")
      .toUpperCase()
      .split(/[,;\s]+/)
      .map((part) => part.trim())
      .filter(Boolean)
  );
}

function intersectionSize(a, b) {
  let n = 0;
  for (const item of a) {
    if (b.has(item)) n += 1;
  }
  return n;
}

function jaccardSimilarity(a, b) {
  if (!a.size && !b.size) return 0;
  const shared = intersectionSize(a, b);
  const union = a.size + b.size - shared;
  return union ? shared / union : 0;
}

function lexicalCoverage(queryTokens, profileTokensSet) {
  if (!queryTokens.size) return 0;
  return intersectionSize(queryTokens, profileTokensSet) / queryTokens.size;
}

function currentCollection() {
  return el.collectionFilter.value;
}

function buildWhere() {
  const clauses = [];
  const params = [];

  const collection = currentCollection();
  if (collection === "biorxiv") {
    clauses.push(`NOT EXISTS (
      SELECT 1 FROM markers mx
      WHERE mx.paper_id = p.paper_id
      AND mx.data_id IS NOT NULL
      AND mx.data_id <> ''
    )`);
  } else if (collection === "benchmark") {
    clauses.push(`EXISTS (
      SELECT 1 FROM markers mx
      WHERE mx.paper_id = p.paper_id
      AND mx.data_id IS NOT NULL
      AND mx.data_id <> ''
    )`);
  }

  const sourceType = el.sourceTypeFilter.value;
  if (sourceType !== "all") {
    clauses.push("m.source_type = ?");
    params.push(sourceType);
  }

  const query = el.searchInput.value.trim().toLowerCase();
  if (query) {
    clauses.push(`(
      lower(coalesce(p.title, '')) LIKE ? OR
      lower(coalesce(p.doi, '')) LIKE ? OR
      lower(coalesce(m.group_name, '')) LIKE ? OR
      lower(coalesce(m.feature_name, '')) LIKE ? OR
      lower(coalesce(m.feature_id, '')) LIKE ? OR
      lower(coalesce(m.source_rationale, '')) LIKE ?
    )`);
    const like = `%${query}%`;
    params.push(like, like, like, like, like, like);
  }

  return {
    whereSql: clauses.length ? `WHERE ${clauses.join(" AND ")}` : "",
    params,
  };
}

function updateSummaryCards() {
  el.countPapers.textContent = fmtInt(runScalar("SELECT COUNT(*) AS n FROM papers"));
  el.countBenchmarkPapers.textContent = fmtInt(
    runScalar(
      `SELECT COUNT(*) AS n FROM papers p
       WHERE EXISTS (
         SELECT 1 FROM markers m
         WHERE m.paper_id = p.paper_id
         AND m.data_id IS NOT NULL
         AND m.data_id <> ''
       )`
    )
  );
  el.countBiorxivPapers.textContent = fmtInt(
    runScalar(
      `SELECT COUNT(*) AS n FROM papers p
       WHERE NOT EXISTS (
         SELECT 1 FROM markers m
         WHERE m.paper_id = p.paper_id
         AND m.data_id IS NOT NULL
         AND m.data_id <> ''
       )`
    )
  );
  el.countMarkers.textContent = fmtInt(runScalar("SELECT COUNT(*) AS n FROM markers"));
  el.countCellTypes.textContent = fmtInt(runScalar("SELECT COUNT(DISTINCT group_name) AS n FROM markers"));
  el.countGenes.textContent = fmtInt(
    runScalar(
      "SELECT COUNT(DISTINCT CASE WHEN feature_id IS NOT NULL AND feature_id <> '' THEN feature_id ELSE feature_name END) AS n FROM markers"
    )
  );
}

function loadFilterOptions() {
  const sourceTypes = runRows(
    "SELECT source_type, COUNT(*) AS n FROM markers GROUP BY source_type ORDER BY source_type"
  );

  el.sourceTypeFilter.innerHTML = '<option value="all">All</option>';
  for (const row of sourceTypes) {
    const opt = document.createElement("option");
    opt.value = row.source_type;
    opt.textContent = `${row.source_type} (${fmtInt(row.n)})`;
    el.sourceTypeFilter.appendChild(opt);
  }
}

function loadProfiles() {
  const rows = runRows(
    `SELECT
      pr.profile_id,
      pr.paper_id,
      pr.collection,
      pr.group_name,
      pr.text_blob,
      pr.paper_context_blob,
      pr.gene_names_json,
      pr.gene_ids_json,
      pr.evidence_sentences_json,
      pr.text_embedding_json,
      pr.context_embedding_json,
      pr.n_genes,
      pr.n_gene_ids,
      pr.n_sentences,
      p.title,
      p.doi,
      p.year
    FROM profiles pr
    JOIN papers p ON p.paper_id = pr.paper_id
    ORDER BY p.year DESC, pr.profile_id`
  );

  state.profiles = rows.map((row) => {
    const geneNames = parseJsonArray(row.gene_names_json);
    const geneIds = parseJsonArray(row.gene_ids_json);
    const evidenceSentences = parseJsonArray(row.evidence_sentences_json);
    const embeddingRaw = parseJsonArray(row.text_embedding_json);
    const contextEmbeddingRaw = parseJsonArray(row.context_embedding_json);
    const labelTokens = expandedTokenSet(normalizeProfileText(row.group_name).match(/[A-Z0-9]+/g) || []);
    const textTokens = expandedTokenSet(normalizeProfileText(row.text_blob).match(/[A-Z0-9]+/g) || []);
    return {
      profileId: Number(row.profile_id),
      paperId: Number(row.paper_id),
      collection: row.collection,
      groupName: row.group_name,
      textBlob: row.text_blob,
      paperContextBlob: row.paper_context_blob || "",
      title: row.title || "",
      doi: row.doi || "",
      year: row.year,
      geneNames,
      geneIds,
      evidenceSentences,
      embedding: Float32Array.from(embeddingRaw),
      contextEmbedding: Float32Array.from(contextEmbeddingRaw),
      geneTokenSet: new Set([...geneNames, ...geneIds.filter(Boolean)]),
      labelTokenSet: labelTokens,
      textTokenSet: textTokens,
      nGenes: Number(row.n_genes) || geneNames.length,
      nGeneIds: Number(row.n_gene_ids) || geneIds.length,
      nSentences: Number(row.n_sentences) || evidenceSentences.length,
    };
  });
}

function renderRows(rows) {
  if (!rows.length) {
    el.tableBody.innerHTML =
      '<tr><td colspan="6" class="small">No rows match the current filters.</td></tr>';
    return;
  }

  const html = rows
    .map((row) => {
      const title = row.title || "";
      const doi = row.doi || "";
      const doiUrl = toDoiUrl(doi);
      const rationale = row.source_rationale || "";
      const paperText = esc(title || doi);
      const paperCell = doi
        ? `<a href="${esc(doiUrl)}" target="_blank" rel="noopener">${paperText}</a>`
        : paperText;
      const fullContext = esc(rationale);
      const contextCell = rationale
        ? `<details class="context-details"><summary>Show context</summary><div class="context-full">${fullContext}</div></details>`
        : "";

      return `
        <tr>
          <td title="${esc(title || doi)}">${paperCell}</td>
          <td>${row.year ?? ""}</td>
          <td>${esc(row.group_name)}</td>
          <td>${esc(row.feature_name)}</td>
          <td class="small">${esc(row.feature_id || "")}</td>
          <td class="rationale">${contextCell}</td>
        </tr>
      `;
    })
    .join("");

  el.tableBody.innerHTML = html;
}

function updatePager() {
  const maxPage = Math.max(1, Math.ceil(state.totalRows / state.pageSize));
  if (state.currentPage > maxPage) state.currentPage = maxPage;
  el.pageLabel.textContent = `Page ${state.currentPage} of ${maxPage}`;
  el.prevPage.disabled = state.currentPage <= 1;
  el.nextPage.disabled = state.currentPage >= maxPage;

  const start = state.totalRows === 0 ? 0 : (state.currentPage - 1) * state.pageSize + 1;
  const end = Math.min(state.currentPage * state.pageSize, state.totalRows);
  el.tableCount.textContent = `${fmtInt(state.totalRows)} results${state.totalRows ? ` (${fmtInt(start)}-${fmtInt(end)})` : ""}`;
}

function refreshTable() {
  const { whereSql, params } = buildWhere();

  state.totalRows = runScalar(
    `SELECT COUNT(*) AS n
     FROM markers m
     JOIN papers p ON p.paper_id = m.paper_id
     ${whereSql}`,
    params
  );

  const offset = (state.currentPage - 1) * state.pageSize;
  const rows = runRows(
    `SELECT
      p.title,
      p.doi,
      p.year,
      m.group_name,
      m.feature_name,
      m.feature_id,
      m.source_rationale
    FROM markers m
    JOIN papers p ON p.paper_id = m.paper_id
    ${whereSql}
    ORDER BY p.year DESC, p.paper_id, m.marker_id
    LIMIT ? OFFSET ?`,
    [...params, state.pageSize, offset]
  );

  renderRows(rows);
  updatePager();
}

function updateProfilePlaceholder() {
  if (el.profileQueryMode.value === "genes") {
    el.profileQueryInput.placeholder = "IL7R LTB MALAT1 or ENSG00000168685 ENSG00000105374";
  } else {
    el.profileQueryInput.placeholder = "t cells, cytotoxic lymphocytes, stromal fibroblasts";
  }
}

function renderProfileResults(results, mode, query, collectionLabel) {
  if (!query) {
    el.profileQuerySummary.textContent = "";
    el.profileResults.innerHTML = "";
    return;
  }

  if (!results.length) {
    el.profileQuerySummary.textContent = `No profile matches found in ${collectionLabel}.`;
    el.profileResults.innerHTML =
      '<article class="profile-empty">No profiles matched the current query. Try a broader phrase or a longer gene list.</article>';
    return;
  }

  const scoreLabel = mode === "genes" ? "Jaccard" : "Hybrid";
  el.profileQuerySummary.textContent = `${results.length} profile matches in ${collectionLabel}. Top result ${scoreLabel.toLowerCase()} = ${results[0].score.toFixed(3)}.`;

  el.profileResults.innerHTML = results
    .map((result) => {
      const doiUrl = toDoiUrl(result.doi);
      const paperText = esc(result.title || result.doi || `Paper ${result.paperId}`);
      const paperHtml = result.doi
        ? `<a href="${esc(doiUrl)}" target="_blank" rel="noopener">${paperText}</a>`
        : paperText;
      const evidence = result.evidenceSentences.length
        ? truncate(result.evidenceSentences[0], 210)
        : "No evidence sentence stored.";
      const genesPreview = result.geneNames.slice(0, 10).join(", ");
      const sharedHtml = mode === "genes" && result.sharedMatches.length
        ? `<div class="profile-shared">Shared matches: ${esc(result.sharedMatches.join(", "))}</div>`
        : "";

      return `
        <article class="profile-card">
          <div class="profile-card-head">
            <h3>${esc(result.groupName)}</h3>
            <span class="profile-score">${scoreLabel} ${result.score.toFixed(3)}</span>
          </div>
          <div class="profile-card-meta">
            <span>${esc(result.collection)}</span>
            <span>${result.year ?? ""}</span>
            <span>${fmtInt(result.nGenes)} genes</span>
          </div>
          <div class="profile-paper">${paperHtml}</div>
          <div class="profile-genes"><strong>Markers:</strong> <code>${esc(genesPreview)}</code></div>
          ${sharedHtml}
          <div class="profile-evidence"><strong>Evidence:</strong> ${esc(evidence)}</div>
        </article>
      `;
    })
    .join("");
}

function searchProfiles() {
  const query = el.profileQueryInput.value.trim();
  const mode = el.profileQueryMode.value;
  const candidates = state.profiles;
  const collectionLabel = "all collections";

  if (!query) {
    renderProfileResults([], mode, "", collectionLabel);
    return;
  }

  let results = [];
  if (mode === "genes") {
    const querySet = parseGeneQuery(query);
    results = candidates
      .map((profile) => {
        const score = jaccardSimilarity(querySet, profile.geneTokenSet);
        return {
          ...profile,
          score,
          sharedMatches: [...querySet].filter((token) => profile.geneTokenSet.has(token)),
        };
      })
      .filter((profile) => profile.score > 0)
      .sort((a, b) =>
        b.score - a.score ||
        b.sharedMatches.length - a.sharedMatches.length ||
        a.nGenes - b.nGenes
      )
      .slice(0, 8);
  } else {
    const queryVec = embedProfileText(query);
    const contextQueryVec = embedProfileText(query);
    const queryTokens = expandedTokenSet(normalizeProfileText(query).match(/[A-Z0-9]+/g) || []);
    const normalizedQuery = normalizeProfileText(query);

    results = candidates
      .map((profile) => {
        const profileCosine = cosineSimilarity(queryVec, profile.embedding);
        const contextCosine = cosineSimilarity(contextQueryVec, profile.contextEmbedding);
        const labelCoverage = lexicalCoverage(queryTokens, profile.labelTokenSet);
        const textCoverage = lexicalCoverage(queryTokens, profile.textTokenSet);
        const labelHit = normalizeProfileText(profile.groupName).includes(normalizedQuery) ? 0.12 : 0;
        return {
          ...profile,
          score:
            (DEFAULT_PROFILE_WEIGHT * profileCosine) +
            (DEFAULT_CONTEXT_WEIGHT * contextCosine) +
            (0.22 * labelCoverage) +
            (0.05 * textCoverage) +
            labelHit,
          sharedMatches: [],
        };
      })
      .filter((profile) => profile.score > 0)
      .sort((a, b) => b.score - a.score || b.nSentences - a.nSentences || b.nGenes - a.nGenes)
      .slice(0, 8);
  }

  renderProfileResults(results, mode, query, collectionLabel);
}

function wireEvents() {
  const rerenderFromFirstPage = () => {
    state.currentPage = 1;
    refreshTable();
  };

  el.tabHome.addEventListener("click", () => setActiveTab("home"));
  el.tabMethods.addEventListener("click", () => setActiveTab("methods"));
  el.tabRaw.addEventListener("click", () => setActiveTab("raw"));

  el.collectionFilter.addEventListener("change", () => {
    rerenderFromFirstPage();
  });

  el.sourceTypeFilter.addEventListener("change", rerenderFromFirstPage);

  el.pageSizeFilter.addEventListener("change", () => {
    state.pageSize = Number(el.pageSizeFilter.value);
    rerenderFromFirstPage();
  });

  let searchTimer = null;
  el.searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(rerenderFromFirstPage, 220);
  });

  el.profileQueryButton.addEventListener("click", searchProfiles);
  el.profileQueryMode.addEventListener("change", () => {
    updateProfilePlaceholder();
    searchProfiles();
  });
  for (const button of el.profileExamples) {
    button.addEventListener("click", () => {
      el.profileQueryMode.value = button.dataset.mode || "text";
      el.profileQueryInput.value = button.dataset.query || "";
      updateProfilePlaceholder();
      searchProfiles();
    });
  }
  el.profileQueryInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      searchProfiles();
    }
  });

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
    el.statusNote.textContent = "Loading SQLite engine...";
    const SQL = await initSqlJs({
      locateFile: (file) => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.2/${file}`,
    });

    el.statusNote.textContent = "Loading database file...";
    const response = await fetch("llmarkers.sqlite", { cache: "no-cache" });
    if (!response.ok) {
      throw new Error(`Could not load llmarkers.sqlite (HTTP ${response.status})`);
    }
    const buffer = await response.arrayBuffer();

    state.db = new SQL.Database(new Uint8Array(buffer));
    updateSummaryCards();
    loadFilterOptions();
    loadProfiles();
    updateProfilePlaceholder();
    setActiveTab("home");
    wireEvents();
    refreshTable();
    searchProfiles();

    el.statusNote.textContent = "Database loaded.";
  } catch (err) {
    console.error(err);
    el.statusNote.textContent = `Failed to load database: ${err.message}`;
  }
}

init();
