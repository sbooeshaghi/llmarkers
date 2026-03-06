/* global initSqlJs */

const MODEL_ID = 'onnx-community/all-MiniLM-L6-v2-ONNX';
const MODEL_NAME = 'sentence-transformers_all-MiniLM-L6-v2@float16';

const el = {
  query: document.getElementById('query'),
  run: document.getElementById('run'),
  status: document.getElementById('status'),
  results: document.getElementById('results'),
};

let db;
let extractor;
let profiles = [];

function rowsFromExec(result) {
  if (!result.length) return [];
  const { columns, values } = result[0];
  return values.map((row) => Object.fromEntries(columns.map((c, i) => [c, row[i]])));
}

function cosine(a, b) {
  let dot = 0;
  let an = 0;
  let bn = 0;
  for (let i = 0; i < a.length; i += 1) {
    dot += a[i] * b[i];
    an += a[i] * a[i];
    bn += b[i] * b[i];
  }
  return an && bn ? dot / Math.sqrt(an * bn) : 0;
}

function blobToFloat16Array(blob) {
  const bytes = blob instanceof Uint8Array ? blob : new Uint8Array(blob);
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const out = new Float32Array(bytes.byteLength / 2);
  for (let i = 0; i < out.length; i += 1) {
    const uint16 = view.getUint16(i * 2, true);
    const s = (uint16 & 0x8000) >> 15;
    const e = (uint16 & 0x7C00) >> 10;
    const f = uint16 & 0x03FF;
    let value;
    if (e === 0) {
      value = f === 0 ? 0 : (f / 1024) * Math.pow(2, -14);
    } else if (e === 0x1F) {
      value = f === 0 ? Infinity : NaN;
    } else {
      value = (1 + f / 1024) * Math.pow(2, e - 15);
    }
    out[i] = s ? -value : value;
  }
  return out;
}

async function ensureExtractor() {
  if (extractor) return extractor;
  el.status.textContent = 'Loading MiniLM query model...';
  const mod = await import('https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1');
  mod.env.allowLocalModels = false;
  mod.env.useBrowserCache = true;
  extractor = await mod.pipeline('feature-extraction', MODEL_ID, {
    pooling: 'mean',
    normalize: true,
  });
  return extractor;
}

async function loadDb() {
  el.status.textContent = 'Loading SQLite database...';
  const SQL = await initSqlJs({
    locateFile: (file) => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.2/${file}`,
  });
  const response = await fetch('llmarkers.sqlite', { cache: 'no-cache' });
  const buffer = await response.arrayBuffer();
  db = new SQL.Database(new Uint8Array(buffer));
  const rows = rowsFromExec(db.exec(`
    SELECT
      pr.profile_id,
      pr.group_name,
      p.title,
      p.doi,
      emb.text_embedding_blob
    FROM profile_embeddings_biomed emb
    JOIN profiles pr ON pr.profile_id = emb.profile_id
    JOIN papers p ON p.paper_id = pr.paper_id
    WHERE emb.model_name = '${MODEL_NAME}'
    ORDER BY pr.profile_id
  `));
  profiles = rows.map((row) => ({
    profileId: Number(row.profile_id),
    groupName: row.group_name,
    title: row.title || '',
    doi: row.doi || '',
    embedding: blobToFloat16Array(row.text_embedding_blob),
  }));
  el.status.textContent = `Loaded ${profiles.length.toLocaleString()} MiniLM profile vectors.`;
}

function render(results) {
  el.results.innerHTML = results.map((row) => `
    <div class="result">
      <div><strong>${row.groupName}</strong> <span class="muted">score ${row.score.toFixed(3)}</span></div>
      <div>${row.title || ''}</div>
      <div class="muted"><code>${row.doi || ''}</code></div>
    </div>
  `).join('');
}

async function runQuery() {
  const query = el.query.value.trim();
  if (!query) return;
  const pipe = await ensureExtractor();
  el.status.textContent = `Embedding query: ${query}`;
  const output = await pipe(query, { pooling: 'mean', normalize: true });
  const queryVec = Float32Array.from(output.data ?? output.tolist?.() ?? output);
  const results = profiles
    .map((profile) => ({ ...profile, score: cosine(queryVec, profile.embedding) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 8);
  render(results);
  el.status.textContent = `Top ${results.length} MiniLM results for "${query}".`;
}

await loadDb();
el.run.addEventListener('click', runQuery);
