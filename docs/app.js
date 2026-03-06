/* global initSqlJs */

const DEFAULT_PROFILE_WEIGHT = 0.9;
const DEFAULT_CONTEXT_WEIGHT = 0.1;
const PROFILE_RESULT_MIN_SCORE = 0.2;
const MINILM_MODEL_ID = "onnx-community/all-MiniLM-L6-v2-ONNX";
const MINILM_MODEL_NAME = "sentence-transformers_all-MiniLM-L6-v2@float16";
const state = {
  db: null,
  currentPage: 1,
  pageSize: 50,
  totalRows: 0,
  profiles: [],
  miniLmExtractor: null,
  miniLmStatus: "idle",
  loadProgress: {
    db: { ratio: 0, text: "Waiting" },
    model: { ratio: 0, text: "Waiting" },
  },
};

const el = {
  tabHome: document.getElementById("tabHome"),
  tabRaw: document.getElementById("tabRaw"),
  tabMethods: document.getElementById("tabMethods"),
  tabAbout: document.getElementById("tabAbout"),
  panelHome: document.getElementById("panelHome"),
  panelRaw: document.getElementById("panelRaw"),
  panelMethods: document.getElementById("panelMethods"),
  panelAbout: document.getElementById("panelAbout"),
  countPapers: document.getElementById("countPapers"),
  countPapersDetail: document.getElementById("countPapersDetail"),
  countMarkers: document.getElementById("countMarkers"),
  countMarkersDetail: document.getElementById("countMarkersDetail"),
  countProfiles: document.getElementById("countProfiles"),
  countProfilesDetail: document.getElementById("countProfilesDetail"),
  loadStrip: document.getElementById("loadStrip"),
  loadStatusText: document.getElementById("loadStatusText"),
  loadStatusMeta: document.getElementById("loadStatusMeta"),
  loadBarFill: document.getElementById("loadBarFill"),
  profileQueryMode: document.getElementById("profileQueryMode"),
  profileQueryInput: document.getElementById("profileQueryInput"),
  profileQueryButton: document.getElementById("profileQueryButton"),
  profileQueryLoader: document.getElementById("profileQueryLoader"),
  profileQueryLoaderText: document.getElementById("profileQueryLoaderText"),
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
  const isRaw = name === "raw";
  const isMethods = name === "methods";
  const isAbout = name === "about";
  el.tabHome.classList.toggle("is-active", isHome);
  el.tabRaw.classList.toggle("is-active", isRaw);
  el.tabMethods.classList.toggle("is-active", isMethods);
  el.tabAbout.classList.toggle("is-active", isAbout);
  el.tabHome.setAttribute("aria-pressed", String(isHome));
  el.tabRaw.setAttribute("aria-pressed", String(isRaw));
  el.tabMethods.setAttribute("aria-pressed", String(isMethods));
  el.tabAbout.setAttribute("aria-pressed", String(isAbout));
  el.panelHome.hidden = !isHome;
  el.panelRaw.hidden = !isRaw;
  el.panelMethods.hidden = !isMethods;
  el.panelAbout.hidden = !isAbout;
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

function blobToFloat16Array(blob) {
  if (!blob) return null;
  const bytes = blob instanceof Uint8Array ? blob : new Uint8Array(blob);
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const out = new Float32Array(bytes.byteLength / 2);
  for (let i = 0; i < out.length; i += 1) {
    const uint16 = view.getUint16(i * 2, true);
    const sign = (uint16 & 0x8000) >> 15;
    const exponent = (uint16 & 0x7c00) >> 10;
    const fraction = uint16 & 0x03ff;
    let value;
    if (exponent === 0) {
      value = fraction === 0 ? 0 : (fraction / 1024) * Math.pow(2, -14);
    } else if (exponent === 0x1f) {
      value = fraction === 0 ? Infinity : Number.NaN;
    } else {
      value = (1 + fraction / 1024) * Math.pow(2, exponent - 15);
    }
    out[i] = sign ? -value : value;
  }
  return out;
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

function clamp01(value) {
  return Math.max(0, Math.min(1, value || 0));
}

function setLoadProgress(key, ratio, text) {
  state.loadProgress[key] = {
    ratio: clamp01(ratio),
    text: text || state.loadProgress[key]?.text || "",
  };
  updateLoadUi();
}

function updateLoadUi() {
  const db = state.loadProgress.db;
  const model = state.loadProgress.model;
  const overall = ((db.ratio || 0) + (model.ratio || 0)) / 2;
  const dbText = `DB ${Math.round((db.ratio || 0) * 100)}%`;
  const modelText = `MiniLM ${Math.round((model.ratio || 0) * 100)}%`;

  el.loadStatusText.textContent = `${db.text}. ${model.text}.`;
  el.loadStatusMeta.textContent = `${dbText} | ${modelText}`;
  el.loadBarFill.style.width = `${Math.round(overall * 100)}%`;
  el.loadStrip.querySelector(".load-bar").setAttribute("aria-valuenow", String(Math.round(overall * 100)));

  if (db.ratio >= 1 && model.ratio >= 1 && state.miniLmStatus !== "failed") {
    el.loadStatusText.textContent = "Database and MiniLM ready.";
    el.loadStatusMeta.textContent = "100%";
    window.setTimeout(() => {
      el.loadStrip.classList.add("is-hidden");
    }, 1200);
  }
}

async function fetchWithProgress(url, onProgress) {
  const response = await fetch(url, { cache: "no-cache" });
  if (!response.ok) {
    throw new Error(`Could not load ${url} (HTTP ${response.status})`);
  }

  const contentLength = Number(response.headers.get("content-length")) || 0;
  if (!response.body || !contentLength) {
    const buffer = await response.arrayBuffer();
    onProgress?.(1, "Database downloaded");
    return buffer;
  }

  const reader = response.body.getReader();
  const chunks = [];
  let received = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    if (value) {
      chunks.push(value);
      received += value.length;
      onProgress?.(received / contentLength, "Downloading database");
    }
  }

  const merged = new Uint8Array(received);
  let offset = 0;
  for (const chunk of chunks) {
    merged.set(chunk, offset);
    offset += chunk.length;
  }
  onProgress?.(1, "Database downloaded");
  return merged.buffer;
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
  const totalPapers = runScalar("SELECT COUNT(*) AS n FROM papers");
  const benchmarkPapers = runScalar(
    `SELECT COUNT(*) AS n FROM papers p
     WHERE EXISTS (
       SELECT 1 FROM markers m
       WHERE m.paper_id = p.paper_id
       AND m.data_id IS NOT NULL
       AND m.data_id <> ''
     )`
  );
  const biorxivPapers = runScalar(
    `SELECT COUNT(*) AS n FROM papers p
     WHERE NOT EXISTS (
       SELECT 1 FROM markers m
       WHERE m.paper_id = p.paper_id
       AND m.data_id IS NOT NULL
       AND m.data_id <> ''
     )`
  );
  const totalMarkers = runScalar("SELECT COUNT(*) AS n FROM markers");
  const uniqueCellTypes = runScalar("SELECT COUNT(DISTINCT group_name) AS n FROM markers");
  const uniqueGenes = runScalar(
    "SELECT COUNT(DISTINCT CASE WHEN feature_id IS NOT NULL AND feature_id <> '' THEN feature_id ELSE feature_name END) AS n FROM markers"
  );
  const totalProfiles = runScalar("SELECT COUNT(*) AS n FROM profiles");
  const benchmarkProfiles = runScalar("SELECT COUNT(*) AS n FROM profiles WHERE collection = 'benchmark'");
  const biorxivProfiles = runScalar("SELECT COUNT(*) AS n FROM profiles WHERE collection = 'biorxiv'");

  el.countPapers.textContent = fmtInt(totalPapers);
  el.countPapersDetail.textContent = `(${fmtInt(benchmarkPapers)} benchmark, ${fmtInt(biorxivPapers)} bioRxiv)`;
  el.countMarkers.textContent = fmtInt(totalMarkers);
  el.countMarkersDetail.textContent = `(${fmtInt(uniqueCellTypes)} cell types, ${fmtInt(uniqueGenes)} genes)`;
  el.countProfiles.textContent = fmtInt(totalProfiles);
  el.countProfilesDetail.textContent = `(${fmtInt(benchmarkProfiles)} benchmark, ${fmtInt(biorxivProfiles)} bioRxiv)`;
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
      emb.text_embedding_blob,
      emb.context_embedding_blob,
      pr.n_genes,
      pr.n_gene_ids,
      pr.n_sentences,
      p.title,
      p.doi,
      p.year
    FROM profiles pr
    JOIN papers p ON p.paper_id = pr.paper_id
    LEFT JOIN profile_embeddings_biomed emb
      ON emb.profile_id = pr.profile_id
      AND emb.model_name = '${MINILM_MODEL_NAME}'
    ORDER BY p.year DESC, pr.profile_id`
  );

  state.profiles = rows.map((row) => {
    const geneNames = parseJsonArray(row.gene_names_json);
    const geneIds = parseJsonArray(row.gene_ids_json);
    const evidenceSentences = parseJsonArray(row.evidence_sentences_json);
    const miniLmTextEmbedding = blobToFloat16Array(row.text_embedding_blob);
    const miniLmContextEmbedding = blobToFloat16Array(row.context_embedding_blob);
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
      miniLmTextEmbedding,
      miniLmContextEmbedding,
      geneTokenSet: new Set([...geneNames, ...geneIds.filter(Boolean)]),
      nGenes: Number(row.n_genes) || geneNames.length,
      nGeneIds: Number(row.n_gene_ids) || geneIds.length,
      nSentences: Number(row.n_sentences) || evidenceSentences.length,
    };
  });
}

async function ensureMiniLmExtractor() {
  if (state.miniLmExtractor) return state.miniLmExtractor;
  if (state.miniLmStatus === "loading") {
    while (state.miniLmStatus === "loading") {
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
    return state.miniLmExtractor;
  }

  state.miniLmStatus = "loading";
  setLoadProgress("model", 0.02, "Starting MiniLM download");
  try {
    const mod = await import("https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1");
    mod.env.allowLocalModels = false;
    mod.env.useBrowserCache = true;
    state.miniLmExtractor = await mod.pipeline("feature-extraction", MINILM_MODEL_ID, {
      pooling: "mean",
      normalize: true,
      progress_callback: (item) => {
        const loaded = Number(item?.loaded);
        const total = Number(item?.total);
        const rawProgress = Number(item?.progress);
        let ratio = Number.isFinite(rawProgress)
          ? (rawProgress > 1 ? rawProgress / 100 : rawProgress)
          : 0;
        if (Number.isFinite(loaded) && Number.isFinite(total) && total > 0) {
          ratio = loaded / total;
        }
        const status = item?.status || item?.file || "Loading MiniLM";
        setLoadProgress("model", Math.max(0.02, clamp01(ratio)), status);
      },
    });
    state.miniLmStatus = "ready";
    setLoadProgress("model", 1, "MiniLM ready");
    return state.miniLmExtractor;
  } catch (error) {
    state.miniLmStatus = "failed";
    setLoadProgress("model", 1, "MiniLM unavailable");
    throw error;
  }
}

async function embedMiniLmQuery(query) {
  const extractor = await ensureMiniLmExtractor();
  const output = await extractor(query, { pooling: "mean", normalize: true });
  return Float32Array.from(output.data ?? output.tolist?.() ?? output);
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

function renderProfileResults(results, mode, query) {
  if (!query) {
    el.profileQuerySummary.textContent = "";
    el.profileResults.innerHTML = "";
    return;
  }

  if (!results.length) {
    el.profileQuerySummary.textContent = "No profile matches found.";
    el.profileResults.innerHTML =
      '<article class="profile-empty">No profiles matched the current query. Try a broader phrase or a longer gene list.</article>';
    return;
  }

  const scoreLabel = mode === "genes" ? "Jaccard" : "Hybrid";
  const metricText = mode === "genes"
    ? `${PROFILE_RESULT_MIN_SCORE.toFixed(1)} Jaccard similarity`
    : `${PROFILE_RESULT_MIN_SCORE.toFixed(1)} cosine similarity`;
  el.profileQuerySummary.textContent = `${results.length} matches >= ${metricText}.`;

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

function setProfileQueryLoading(isLoading, text = "Running search...") {
  el.profileQueryLoader.hidden = !isLoading;
  el.profileQueryLoaderText.textContent = text;
}

function searchProfilesWithMiniLm(query, candidates, queryEmbedding) {
  return candidates
    .filter((profile) => profile.miniLmTextEmbedding && profile.miniLmContextEmbedding)
    .map((profile) => ({
      ...profile,
      score:
        (DEFAULT_PROFILE_WEIGHT * cosineSimilarity(queryEmbedding, profile.miniLmTextEmbedding)) +
        (DEFAULT_CONTEXT_WEIGHT * cosineSimilarity(queryEmbedding, profile.miniLmContextEmbedding)),
      sharedMatches: [],
    }))
    .filter((profile) => profile.score >= PROFILE_RESULT_MIN_SCORE)
    .sort((a, b) => b.score - a.score || b.nSentences - a.nSentences || b.nGenes - a.nGenes);
}

async function searchProfiles() {
  const query = el.profileQueryInput.value.trim();
  const mode = el.profileQueryMode.value;
  const candidates = state.profiles;

  if (!query) {
    setProfileQueryLoading(false);
    renderProfileResults([], mode, "");
    return;
  }

  let results = [];
  if (mode === "genes") {
    setProfileQueryLoading(true, "Matching marker sets...");
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
      .filter((profile) => profile.score >= PROFILE_RESULT_MIN_SCORE)
      .sort((a, b) =>
        b.score - a.score ||
        b.sharedMatches.length - a.sharedMatches.length ||
        a.nGenes - b.nGenes
      );
    setProfileQueryLoading(false);
  } else {
    el.profileQueryButton.disabled = true;
    setProfileQueryLoading(true, state.miniLmExtractor ? "Embedding and ranking..." : "Loading MiniLM...");
    try {
      el.profileQuerySummary.textContent = state.miniLmExtractor
        ? "Embedding query..."
        : "Loading MiniLM query model...";
      const queryEmbedding = await embedMiniLmQuery(query);
      results = searchProfilesWithMiniLm(query, candidates, queryEmbedding);
    } catch (error) {
      console.error("MiniLM query embedding failed.", error);
      el.profileQuerySummary.textContent = "MiniLM query model is unavailable.";
      results = [];
    } finally {
      el.profileQueryButton.disabled = false;
      setProfileQueryLoading(false);
    }
  }

  renderProfileResults(results, mode, query);
}

function wireEvents() {
  const rerenderFromFirstPage = () => {
    state.currentPage = 1;
    refreshTable();
  };

  el.tabHome.addEventListener("click", () => setActiveTab("home"));
  el.tabRaw.addEventListener("click", () => setActiveTab("raw"));
  el.tabMethods.addEventListener("click", () => setActiveTab("methods"));
  el.tabAbout.addEventListener("click", () => setActiveTab("about"));

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
    setLoadProgress("db", 0.01, "Preparing database");
    setLoadProgress("model", 0.01, "Preparing MiniLM");
    el.statusNote.textContent = "Loading database...";

    const modelWarmup = ensureMiniLmExtractor().catch((error) => {
      console.error("MiniLM warmup failed.", error);
      return null;
    });

    const sqlPromise = initSqlJs({
      locateFile: (file) => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.2/${file}`,
    });
    const dbFetchPromise = fetchWithProgress("llmarkers.sqlite", (ratio, text) => {
      setLoadProgress("db", ratio, text);
    });

    const [SQL, buffer] = await Promise.all([sqlPromise, dbFetchPromise]);
    setLoadProgress("db", 1, "Database ready");

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
    await modelWarmup;
  } catch (err) {
    console.error(err);
    setLoadProgress("db", 1, "Database unavailable");
    el.statusNote.textContent = `Failed to load database: ${err.message}`;
  }
}

init();
