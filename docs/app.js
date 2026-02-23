/* global initSqlJs */

const state = {
  db: null,
  currentPage: 1,
  pageSize: 50,
  totalRows: 0,
};

const el = {
  countPapers: document.getElementById("countPapers"),
  countBenchmarkPapers: document.getElementById("countBenchmarkPapers"),
  countBiorxivPapers: document.getElementById("countBiorxivPapers"),
  countMarkers: document.getElementById("countMarkers"),
  countCellTypes: document.getElementById("countCellTypes"),
  countGenes: document.getElementById("countGenes"),
  collectionFilter: document.getElementById("collectionFilter"),
  sourceTypeFilter: document.getElementById("sourceTypeFilter"),
  paperFilter: document.getElementById("paperFilter"),
  pageSizeFilter: document.getElementById("pageSizeFilter"),
  searchInput: document.getElementById("searchInput"),
  tableBody: document.querySelector("#markerTable tbody"),
  tableCount: document.getElementById("tableCount"),
  pageLabel: document.getElementById("pageLabel"),
  prevPage: document.getElementById("prevPage"),
  nextPage: document.getElementById("nextPage"),
  statusNote: document.getElementById("statusNote"),
};

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
  return `${text.slice(0, n - 1)}…`;
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

function buildWhere() {
  const clauses = [];
  const params = [];

  const collection = el.collectionFilter.value;
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

  const paperId = el.paperFilter.value;
  if (paperId !== "all") {
    clauses.push("p.paper_id = ?");
    params.push(Number(paperId));
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
    runScalar(`\n      SELECT COUNT(*) AS n FROM papers p\n      WHERE EXISTS (\n        SELECT 1 FROM markers m\n        WHERE m.paper_id = p.paper_id\n        AND m.data_id IS NOT NULL\n        AND m.data_id <> ''\n      )\n    `)
  );
  el.countBiorxivPapers.textContent = fmtInt(
    runScalar(`\n      SELECT COUNT(*) AS n FROM papers p\n      WHERE NOT EXISTS (\n        SELECT 1 FROM markers m\n        WHERE m.paper_id = p.paper_id\n        AND m.data_id IS NOT NULL\n        AND m.data_id <> ''\n      )\n    `)
  );
  el.countMarkers.textContent = fmtInt(runScalar("SELECT COUNT(*) AS n FROM markers"));
  el.countCellTypes.textContent = fmtInt(
    runScalar("SELECT COUNT(DISTINCT group_name) AS n FROM markers")
  );
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

  refreshPaperFilter();
}

function refreshPaperFilter() {
  const collection = el.collectionFilter.value;
  let where = "";
  if (collection === "benchmark") {
    where = `WHERE EXISTS (
      SELECT 1 FROM markers m
      WHERE m.paper_id = papers.paper_id
      AND m.data_id IS NOT NULL
      AND m.data_id <> ''
    )`;
  } else if (collection === "biorxiv") {
    where = `WHERE NOT EXISTS (
      SELECT 1 FROM markers m
      WHERE m.paper_id = papers.paper_id
      AND m.data_id IS NOT NULL
      AND m.data_id <> ''
    )`;
  }

  const papers = runRows(
    `SELECT paper_id, title, doi, year FROM papers ${where} ORDER BY year DESC, title ASC`
  );

  const current = el.paperFilter.value;
  el.paperFilter.innerHTML = '<option value="all">All</option>';

  for (const paper of papers) {
    const opt = document.createElement("option");
    opt.value = String(paper.paper_id);
    const year = paper.year ? ` (${paper.year})` : "";
    const title = paper.title || paper.doi || `paper ${paper.paper_id}`;
    opt.textContent = `${truncate(title, 90)}${year}`;
    el.paperFilter.appendChild(opt);
  }

  const found = [...el.paperFilter.options].some((o) => o.value === current);
  el.paperFilter.value = found ? current : "all";
}

function renderRows(rows) {
  if (!rows.length) {
    el.tableBody.innerHTML =
      '<tr><td colspan="7" class="small">No rows match the current filters.</td></tr>';
    return;
  }

  const html = rows
    .map((row) => {
      const title = row.title || "";
      const doi = row.doi || "";
      const doiUrl = toDoiUrl(doi);
      const rationale = row.source_rationale || "";

      return `
        <tr>
          <td title="${esc(title)}">${esc(truncate(title, 80))}</td>
          <td class="doi">${doi ? `<a href="${esc(doiUrl)}" target="_blank" rel="noopener">${esc(doi)}</a>` : ""}</td>
          <td>${row.year ?? ""}</td>
          <td>${esc(row.group_name)}</td>
          <td>${esc(row.feature_name)}</td>
          <td class="small">${esc(row.feature_id || "")}</td>
          <td class="rationale" title="${esc(rationale)}">${esc(truncate(rationale, 140))}</td>
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

function wireEvents() {
  const rerenderFromFirstPage = () => {
    state.currentPage = 1;
    refreshTable();
  };

  el.collectionFilter.addEventListener("change", () => {
    refreshPaperFilter();
    rerenderFromFirstPage();
  });

  el.sourceTypeFilter.addEventListener("change", rerenderFromFirstPage);
  el.paperFilter.addEventListener("change", rerenderFromFirstPage);

  el.pageSizeFilter.addEventListener("change", () => {
    state.pageSize = Number(el.pageSizeFilter.value);
    rerenderFromFirstPage();
  });

  let searchTimer = null;
  el.searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(rerenderFromFirstPage, 220);
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
    el.statusNote.textContent = "Loading SQLite engine…";
    const SQL = await initSqlJs({
      locateFile: (file) => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.2/${file}`,
    });

    el.statusNote.textContent = "Loading database file…";
    const response = await fetch("llmarkers.sqlite", { cache: "no-cache" });
    if (!response.ok) {
      throw new Error(`Could not load llmarkers.sqlite (HTTP ${response.status})`);
    }
    const buffer = await response.arrayBuffer();

    state.db = new SQL.Database(new Uint8Array(buffer));
    updateSummaryCards();
    loadFilterOptions();
    wireEvents();
    refreshTable();

    el.statusNote.textContent =
      "Database loaded. Tip: run a local web server (not file://) when previewing this page.";
  } catch (err) {
    console.error(err);
    el.statusNote.textContent = `Failed to load database: ${err.message}`;
  }
}

init();
