/* ═══════════════════════════════════════════════════════════════════
   Retail Intelligence Platform — Frontend Logic v2
   Zero-emoji, class-aligned with style.css v2
   ═══════════════════════════════════════════════════════════════════ */

const API = '';   // same origin — Flask serves index.html

// ── State ─────────────────────────────────────────────────────────────
let allProducts = [];
let currentAnalysis = null;
let currentAnalysisLabel = '';

// ── DOM helpers ────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);

const fmt = n => n == null ? '—' : Number(n).toLocaleString('en-IN');

const fmtPrice = n =>
  n == null ? '—' : '₹' + Number(n).toLocaleString('en-IN', { maximumFractionDigits: 0 });

const fmtDate = s => {
  if (!s) return '—';
  const d = new Date(s);
  return isNaN(d) ? s : d.toLocaleString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
};

const trendBadge = t => {
  const map = { down: 'b-green', up: 'b-rose', stable: 'b-muted' };
  const label = { down: 'Drop', up: 'Rise', stable: 'Stable' };
  return `<span class="badge ${map[t] || 'b-muted'}">${label[t] || t}</span>`;
};

const platformBadge = p => {
  const cl = p === 'AMAZON' ? 'b-amber' : p === 'FLIPKART' ? 'b-blue' : 'b-muted';
  return `<span class="badge ${cl}">${p}</span>`;
};

// ── Clock ─────────────────────────────────────────────────────────────
(function clock() {
  const el = $('topbarTime');
  if (!el) return;
  const tick = () => {
    el.textContent = new Date().toLocaleString('en-IN', {
      weekday: 'short', day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit'
    });
  };
  tick();
  setInterval(tick, 30000);
})();

// ── Toast ─────────────────────────────────────────────────────────────
function toast(msg, type = 'info') {
  const el = document.createElement('div');
  el.className = `toast t-${type}`;
  el.innerHTML = `<span>${msg}</span>`;
  $('toastContainer').appendChild(el);
  setTimeout(() => {
    el.classList.add('hiding');
    setTimeout(() => el.remove(), 250);
  }, 3200);
}

// ── Navigation ─────────────────────────────────────────────────────────
const PAGE_LABELS = {
  dashboard: 'Dashboard', collection: 'Data Collection',
  explorer: 'Product Explorer', analytics: 'Price Analytics',
  insights: 'AI Insights', reports: 'Reports'
};

function navigateTo(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  const pg = $(`page-${page}`);
  const nav = $(`nav-${page}`);
  if (pg) pg.classList.add('active');
  if (nav) nav.classList.add('active');

  $('pageTitle').textContent = PAGE_LABELS[page] || page;

  if (page === 'dashboard') loadDashboard();
  if (page === 'analytics') { loadPriceDrops(); loadAnalyticsData(); }
  if (page === 'reports') loadReports();
  if (page === 'explorer') { loadBrowse(); loadCompareSelects(); }
}

document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', e => { e.preventDefault(); navigateTo(item.dataset.page); });
});

// ── API ────────────────────────────────────────────────────────────────
async function apiFetch(path, opts = {}) {
  const res = await fetch(API + path, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(err.error || res.statusText);
  }
  return res.json();
}

// ── Sidebar / health ───────────────────────────────────────────────────
async function loadSidebarStats() {
  try {
    const s = await apiFetch('/api/stats');
    $('stat-products').textContent = fmt(s.total_products);
    $('stat-platforms').textContent = fmt(s.platforms?.length || 0);
    $('stat-reports').textContent = fmt(s.total_reports);
    $('apiStatusDot').className = 'status-dot online';
    $('apiStatusText').textContent = 'API Connected';
  } catch {
    $('apiStatusDot').className = 'status-dot offline';
    $('apiStatusText').textContent = 'API Offline';
  }
}

// ── Dashboard ──────────────────────────────────────────────────────────
async function loadDashboard() {
  try {
    const [stats, recent] = await Promise.all([
      apiFetch('/api/stats'),
      apiFetch('/api/dashboard/recent?limit=15'),
    ]);

    $('d-total-products').textContent = fmt(stats.total_products);
    $('d-price-drops').textContent = fmt(stats.price_drops);
    $('d-price-increases').textContent = fmt(stats.price_increases);
    $('d-platforms').textContent = fmt(stats.platforms?.length || 0);

    $('stat-products').textContent = fmt(stats.total_products);
    $('stat-platforms').textContent = fmt(stats.platforms?.length || 0);
    $('stat-reports').textContent = fmt(stats.total_reports);

    if (!recent.length) {
      $('recentActivity').innerHTML = notice('info', 'No activity yet. Start by collecting data from the Data Collection page.');
      return;
    }

    $('recentActivity').innerHTML = `
      <div class="tbl-wrap">
        <table>
          <thead><tr>
            <th>Platform</th><th>Product</th><th>Price</th><th>Trend</th><th>Last Updated</th>
          </tr></thead>
          <tbody>${recent.map(p => `<tr>
            <td>${platformBadge(p.platform)}</td>
            <td class="td-title">${p.title}</td>
            <td>${fmtPrice(p.current_price)}</td>
            <td>${trendBadge(p.price_trend)}</td>
            <td class="dimmed">${fmtDate(p.last_seen)}</td>
          </tr>`).join('')}</tbody>
        </table>
      </div>`;
  } catch (e) {
    $('recentActivity').innerHTML = notice('error', `Failed to load: ${e.message}`);
  }
}

// ── Data Collection ────────────────────────────────────────────────────
async function startCollection() {
  const query = $('col-query').value.trim();
  const platform = $('col-platform').value;
  const category = $('col-category').value;
  const max = parseInt($('col-max').value) || 10;
  const btn = $('btnCollect');
  const result = $('collectionResult');

  if (!query) { toast('Enter a search query', 'warn'); return; }

  btn.disabled = true;
  btn.textContent = 'Collecting…';
  result.className = '';
  result.innerHTML = spinner(`Scraping ${platform.toUpperCase()} for "${query}"…`);

  try {
    const data = await apiFetch('/api/collect', {
      method: 'POST',
      body: JSON.stringify({ search_query: query, platform, category, max_results: max }),
    });

    if (data.error) throw new Error(data.error);

    const products = data.products || [];
    const stats = data.stats || {};

    result.innerHTML = `
      ${notice('success', `Collection complete — ${data.total} products processed`)}
      <div class="kpi-grid" style="grid-template-columns:repeat(3,1fr);margin-bottom:14px">
        ${kpiMini('New Products', stats.inserted ?? 0, '--blue')}
        ${kpiMini('Updated', stats.updated ?? 0, '--violet')}
        ${kpiMini('Errors', stats.errors ?? 0, '--amber')}
      </div>
      ${products.length ? `
        <div class="card">
          <div class="card-title">Collected Products (${products.length})</div>
          <div class="tbl-wrap">
            <table>
              <thead><tr><th>Title</th><th>Price</th><th>Rating</th><th>Platform</th></tr></thead>
              <tbody>${products.map(p => `<tr>
                <td class="td-title">${p.title}</td>
                <td>${fmtPrice(p.price)}</td>
                <td>${p.rating ? p.rating.toFixed(1) : '—'}</td>
                <td>${platformBadge(p.platform)}</td>
              </tr>`).join('')}</tbody>
            </table>
          </div>
        </div>` : ''}`;

    loadSidebarStats();
    toast('Data collected successfully', 'success');
  } catch (e) {
    result.innerHTML = notice('error', `Collection failed: ${e.message}`);
    toast('Collection failed', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>Start Collection`;
  }
}

// ── Explorer · Multi-search ────────────────────────────────────────────
async function runMultiSearch() {
  const query = $('ms-query').value.trim();
  const max = parseInt($('ms-max').value) || 5;
  const category = $('ms-category').value;
  const platforms = [];
  if ($('ms-amazon').checked) platforms.push('amazon');
  if ($('ms-flipkart').checked) platforms.push('flipkart');
  const btn = $('btnMultiSearch');
  const result = $('multiSearchResult');

  if (!query) { toast('Enter a search query', 'warn'); return; }
  if (!platforms.length) { toast('Select at least one platform', 'warn'); return; }

  btn.disabled = true;
  btn.textContent = 'Searching…';
  result.innerHTML = spinner('Searching ' + platforms.join(' & ') + '…');

  try {
    const data = await apiFetch('/api/products/search', {
      method: 'POST',
      body: JSON.stringify({ search_query: query, max_results: max, category, platforms }),
    });

    const sum = data.summary || {};
    let html = notice('success', `Found ${sum.total || 0} products across ${sum.platforms_searched || 0} platform(s)`);

    if (sum.min_price != null) {
      html += `<div class="kpi-grid" style="grid-template-columns:repeat(3,1fr);margin-bottom:14px">
        ${kpiMini('Lowest Price', fmtPrice(sum.min_price), '--green')}
        ${kpiMini('Highest Price', fmtPrice(sum.max_price), '--amber')}
        ${kpiMini('Average Price', fmtPrice(sum.avg_price), '--blue')}
      </div>`;
    }

    for (const [pl, products] of Object.entries(data.results || {})) {
      html += `<div class="card mt-3">
        <div class="card-title">${pl.toUpperCase()} — ${products.length} results</div>
        <div class="tbl-wrap">
          <table>
            <thead><tr><th>Title</th><th>Price</th><th>Rating</th></tr></thead>
            <tbody>${products.map(p => `<tr>
              <td class="td-title">${p.title}</td>
              <td>${fmtPrice(p.price)}</td>
              <td>${p.rating ? p.rating.toFixed(1) : '—'}</td>
            </tr>`).join('')}</tbody>
          </table>
        </div>
      </div>`;
    }

    for (const [pl, err] of Object.entries(data.errors || {})) {
      html += notice('error', `${pl.toUpperCase()} search failed: ${err}`);
    }

    result.innerHTML = html;
    loadSidebarStats();
    toast('Search complete', 'success');
  } catch (e) {
    result.innerHTML = notice('error', e.message);
    toast('Search failed', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>Search All Platforms`;
  }
}

// ── Explorer · Browse ──────────────────────────────────────────────────
async function loadBrowse() {
  const platform = $('br-platform').value;
  const view = $('br-view').value;
  const result = $('browseResult');
  result.innerHTML = spinner('Loading products…');

  try {
    const products = await apiFetch(`/api/products?platform=${platform}&view=${view}&limit=100`);
    allProducts = products;
    updateCompareSelects();

    if (!products.length) {
      result.innerHTML = notice('info', 'No products found for the selected filters.');
      return;
    }

    result.innerHTML = `
      <div class="card">
        <div class="card-title">Results — ${products.length} products</div>
        <div class="tbl-wrap">
          <table>
            <thead><tr><th>Product</th><th>Platform</th><th>Price</th><th>Rating</th><th>Trend</th><th>Change</th><th>Scrapes</th></tr></thead>
            <tbody>${products.map(p => `<tr>
              <td class="td-title">${p.title || '—'}</td>
              <td>${platformBadge((p.platform || '?').toUpperCase())}</td>
              <td>${fmtPrice(p.current_price)}</td>
              <td>${p.current_rating ? p.current_rating.toFixed(1) : '—'}</td>
              <td>${trendBadge(p.price_trend || 'stable')}</td>
              <td>${p.price_change_percent != null ? p.price_change_percent.toFixed(1) + '%' : '0%'}</td>
              <td class="dimmed">${p.times_scraped || 0}</td>
            </tr>`).join('')}</tbody>
          </table>
        </div>
      </div>`;
  } catch (e) {
    result.innerHTML = notice('error', e.message);
  }
}

// ── Explorer · Compare Selects ─────────────────────────────────────────
async function loadCompareSelects() {
  try {
    if (!allProducts.length) allProducts = await apiFetch('/api/products?limit=200');
    updateCompareSelects();
  } catch { /* ignore */ }
}

function updateCompareSelects() {
  const opts = allProducts.map((p, i) =>
    `<option value="${i}">${(p.platform || '?').toUpperCase()} — ${(p.title || '?').slice(0, 55)}</option>`
  ).join('');
  $('cmp-p1').innerHTML = opts;
  $('cmp-p2').innerHTML = opts;
  if (allProducts.length > 1) $('cmp-p2').selectedIndex = 1;
}

function compareProducts() {
  const i1 = parseInt($('cmp-p1').value);
  const i2 = parseInt($('cmp-p2').value);
  const p1 = allProducts[i1];
  const p2 = allProducts[i2];
  const result = $('compareResult');

  if (!p1 || !p2) { result.innerHTML = notice('warn', 'Products not loaded'); return; }
  if (i1 === i2) { result.innerHTML = notice('warn', 'Select two different products'); return; }

  const price1 = p1.current_price, price2 = p2.current_price;
  let priceSummary = '';
  if (price1 && price2) {
    const cheaper = price1 < price2 ? 'Product 1' : 'Product 2';
    const diff = Math.abs(price1 - price2);
    const pct = (diff / Math.max(price1, price2) * 100).toFixed(1);
    priceSummary = `
      <div class="kpi-grid" style="grid-template-columns:repeat(3,1fr);margin:14px 0">
        ${kpiMini('Cheaper Option', cheaper, '--green')}
        ${kpiMini('Price Difference', fmtPrice(diff), '--blue')}
        ${kpiMini('Saving', pct + '%', '--violet')}
      </div>
      ${notice('info', `${cheaper} is ${fmtPrice(diff)} cheaper (${pct}% saving)`)}`;
  }

  const rows = [
    ['Platform', (p1.platform || '?').toUpperCase(), (p2.platform || '?').toUpperCase()],
    ['Current Price', fmtPrice(price1), fmtPrice(price2)],
    ['Rating', p1.current_rating ? p1.current_rating.toFixed(1) : '—', p2.current_rating ? p2.current_rating.toFixed(1) : '—'],
    ['Trend', trendBadge(p1.price_trend || 'stable'), trendBadge(p2.price_trend || 'stable')],
    ['Times Scraped', p1.times_scraped || 0, p2.times_scraped || 0],
    ['First Seen', fmtDate(p1.first_seen), fmtDate(p2.first_seen)],
  ];

  result.innerHTML = `<div class="card">
    <div class="card-title">Comparison</div>
    <div class="tbl-wrap">
      <table class="cmp-table">
        <thead><tr><th></th><th>Product 1</th><th>Product 2</th></tr></thead>
        <tbody>
          <tr><td class="cmp-attr">Title</td><td>${(p1.title || '?').slice(0, 65)}</td><td>${(p2.title || '?').slice(0, 65)}</td></tr>
          ${rows.map(([a, v1, v2]) => `<tr><td class="cmp-attr">${a}</td><td>${v1}</td><td>${v2}</td></tr>`).join('')}
        </tbody>
      </table>
    </div>
    ${priceSummary}
  </div>`;
}

// ── Explorer · Tab Switch ──────────────────────────────────────────────
function switchExplorerTab(btn, targetId) {
  document.querySelectorAll('#page-explorer .tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('#page-explorer .tab-content').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  $(targetId).classList.add('active');
  if (targetId === 'tab-browse') loadBrowse();
  if (targetId === 'tab-compare') loadCompareSelects();
}

// ── Analytics · Tab Switch ─────────────────────────────────────────────
function switchAnalyticsTab(btn, targetId) {
  document.querySelectorAll('#page-analytics .tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('#page-analytics .tab-content').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  $(targetId).classList.add('active');
  if (targetId === 'tab-drops') loadPriceDrops();
  if (targetId === 'tab-increases') loadPriceIncreases();
  if (targetId === 'tab-distribution') loadDistribution();
}

// ── Analytics · Price Drops ────────────────────────────────────────────
async function loadPriceDrops() {
  const minDrop = parseFloat($('drop-min').value) || 10;
  const result = $('priceDropsResult');
  result.innerHTML = spinner('Loading price drops…');

  try {
    const products = await apiFetch(`/api/products/price-drops?min_percent=${minDrop}`);

    if (!products.length) {
      result.innerHTML = notice('info', `No products with >${minDrop}% price drop found.`);
      return;
    }

    result.innerHTML = `
      ${notice('success', `${products.length} opportunity${products.length !== 1 ? 'ies' : 'y'} found`)}
      <div class="drop-list">
        ${products.slice(0, 25).map(p => {
      const savings = (p.highest_price || 0) - (p.current_price || 0);
      return `<div class="drop-card">
            <div class="drop-card-hd">
              <div class="drop-card-title">${p.title || '—'}</div>
              <div class="drop-pct">${Math.abs(p.price_change_percent || 0).toFixed(1)}% off</div>
            </div>
            <div class="drop-card-meta">
              <span>${platformBadge((p.platform || '?').toUpperCase())}</span>
              <span>Now: <strong>${fmtPrice(p.current_price)}</strong></span>
              <span>Was: <strong>${fmtPrice(p.highest_price)}</strong></span>
              <span style="color:var(--green)">Save: <strong>${fmtPrice(savings)}</strong></span>
              ${p.current_rating ? `<span>Rating: <strong>${p.current_rating.toFixed(1)}</strong></span>` : ''}
            </div>
          </div>`;
    }).join('')}
      </div>`;
  } catch (e) {
    result.innerHTML = notice('error', e.message);
  }
}

async function loadAnalyticsData() {
  loadPriceIncreases();
  loadDistribution();
}

async function loadPriceIncreases() {
  const result = $('priceIncreasesResult');
  if (!result) return;
  result.innerHTML = spinner('Loading…');

  try {
    const data = await apiFetch('/api/products/price-analytics');
    const products = data.price_increases || [];

    if (!products.length) {
      result.innerHTML = notice('info', 'No price increases detected.');
      return;
    }

    result.innerHTML = `
      ${notice('warn', `${data.price_increases_count} product${data.price_increases_count !== 1 ? 's' : ''} with price increases`)}
      <div class="card">
        <div class="tbl-wrap">
          <table>
            <thead><tr><th>Product</th><th>Platform</th><th>Current</th><th>Previous Low</th><th>Increase</th></tr></thead>
            <tbody>${products.slice(0, 20).map(p => `<tr>
              <td class="td-title">${p.title || '—'}</td>
              <td>${platformBadge((p.platform || '?').toUpperCase())}</td>
              <td>${fmtPrice(p.current_price)}</td>
              <td>${fmtPrice(p.lowest_price)}</td>
              <td><span class="badge b-rose">+${(p.price_change_percent || 0).toFixed(1)}%</span></td>
            </tr>`).join('')}</tbody>
          </table>
        </div>
      </div>`;
  } catch (e) {
    result.innerHTML = notice('error', e.message);
  }
}

async function loadDistribution() {
  const result = $('priceDistributionResult');
  if (!result) return;
  result.innerHTML = spinner('Loading…');

  try {
    const data = await apiFetch('/api/products/price-analytics');
    const prices = data.price_distribution || [];

    if (!prices.length) {
      result.innerHTML = notice('info', 'No pricing data available.');
      return;
    }

    // Bucket into ₹2k ranges
    const buckets = {};
    prices.forEach(p => {
      const key = Math.floor(p / 2000) * 2000;
      const label = `₹${fmt(key)} – ₹${fmt(key + 2000)}`;
      buckets[label] = (buckets[label] || 0) + 1;
    });

    const maxBucket = Math.max(...Object.values(buckets));

    result.innerHTML = `
      <div class="kpi-grid" style="grid-template-columns:repeat(3,1fr);margin-bottom:20px">
        ${kpiMini('Average Price', fmtPrice(data.avg_price), '--blue')}
        ${kpiMini('Lowest', fmtPrice(data.min_price), '--green')}
        ${kpiMini('Highest', fmtPrice(data.max_price), '--amber')}
      </div>
      <div class="card-title" style="margin-bottom:12px">Distribution by Price Range</div>
      <div class="bar-chart">
        ${Object.entries(buckets).slice(0, 20).map(([label, count]) => `
          <div class="bar-row">
            <div class="bar-lbl">${label}</div>
            <div class="bar-track">
              <div class="bar-fill" style="width:${(count / maxBucket * 100).toFixed(1)}%"></div>
            </div>
            <div class="bar-val">${count} products</div>
          </div>`).join('')}
      </div>`;
  } catch (e) {
    result.innerHTML = notice('error', e.message);
  }
}

// ── AI Insights ────────────────────────────────────────────────────────
async function runAnalysis() {
  const type = document.querySelector('input[name="analysis-type"]:checked')?.value || 'quick';
  const platform = $('ai-platform').value;
  const category = $('ai-category').value;
  const btn = $('btnAnalyze');
  const result = $('analysisResult');

  btn.disabled = true;
  btn.textContent = type === 'deep' ? 'Running deep analysis…' : 'Analyzing…';

  result.innerHTML = spinner(type === 'deep'
    ? 'Multi-agent deep analysis in progress — this may take 5–6 minutes'
    : 'Generating AI insights…');

  try {
    const endpoint = type === 'deep' ? '/api/analysis/deep' : '/api/analysis/quick';
    const data = await apiFetch(endpoint, {
      method: 'POST',
      body: JSON.stringify({ platform, category }),
    });

    if (data.error) throw new Error(data.error);

    currentAnalysis = data.analysis;
    currentAnalysisLabel = `${platform.toUpperCase()} — ${category.toUpperCase()}`;

    result.innerHTML = renderAnalysis(data.analysis, type, data.products_analyzed, platform, category);
    toast('Analysis complete', 'success');
  } catch (e) {
    result.innerHTML = notice('error', `Analysis failed: ${e.message}`);
    toast('Analysis failed', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>Run Analysis`;
  }
}

function renderAnalysis(analysis, type, productsAnalyzed, platform, category) {
  if (type === 'quick') {
    const pr = analysis.price_range || {};
    const insights = analysis.price_insights || [];
    const recs = analysis.recommendations || [];
    const topP = analysis.top_rated_product || {};
    const bestV = analysis.best_value_product || {};

    return `<div class="analysis-wrap">
      <div class="analysis-scope">${platform.toUpperCase()} · ${category.toUpperCase()} · ${productsAnalyzed} products</div>

      <div class="kpi-grid" style="grid-template-columns:repeat(3,1fr);margin-bottom:20px">
        ${kpiMini('Products Analysed', productsAnalyzed, '--blue')}
        ${kpiMini('Avg Price', fmtPrice(pr.average), '--violet')}
        ${kpiMini('Price Range', `${fmtPrice(pr.min)} – ${fmtPrice(pr.max)}`, '--amber')}
      </div>

      ${topP.title ? `<div class="mb-4">
        <div class="card-title" style="margin-bottom:8px">Top Rated Product</div>
        <div style="padding:12px 14px;background:var(--violet-s);border:1px solid rgba(124,58,237,.15);border-radius:var(--r-md);font-size:13px">
          <strong>${topP.title}</strong>
          ${topP.rating ? `<span class="dimmed" style="margin-left:10px">${topP.rating} stars · ${fmtPrice(topP.price)}</span>` : ''}
        </div>
      </div>` : ''}

      ${bestV.title ? `<div class="mb-4">
        <div class="card-title" style="margin-bottom:8px">Best Value</div>
        <div style="padding:12px 14px;background:var(--green-s);border:1px solid rgba(5,150,105,.15);border-radius:var(--r-md);font-size:13px">
          <strong>${bestV.title}</strong>
          ${bestV.reason ? `<div class="dimmed" style="margin-top:4px;font-size:12px">${bestV.reason}</div>` : ''}
        </div>
      </div>` : ''}

      ${insights.length ? `<div class="mb-4">
        <div class="card-title" style="margin-bottom:10px">Key Insights</div>
        <ul class="insight-list">${insights.map(i => `<li>${i}</li>`).join('')}</ul>
      </div>` : ''}

      ${recs.length ? `<div class="mb-4">
        <div class="card-title" style="margin-bottom:10px">Recommendations</div>
        <ul class="rec-list">${recs.map(r => `<li>${r}</li>`).join('')}</ul>
      </div>` : ''}

      <hr class="divider" />
      <button class="btn btn-secondary" onclick="downloadAnalysisPDF()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        Download PDF Report
      </button>
    </div>`;
  }

  // Deep analysis
  const finalReport = analysis.final_report || 'No report generated';
  const details = analysis.detailed_results || [];

  return `<div class="analysis-wrap">
    <div class="analysis-scope">${platform.toUpperCase()} · ${category.toUpperCase()} · ${productsAnalyzed} products · ${analysis.tasks_completed || 0} tasks</div>

    <div class="mb-4">
      <div class="card-title" style="margin-bottom:10px">Executive Report</div>
      <div style="font-size:13px;color:var(--text-2);line-height:1.7;padding:16px;background:var(--bg-raised);border-radius:var(--r-md);border:1px solid var(--border)">
        ${finalReport.replace(/\n/g, '<br/>')}
      </div>
    </div>

    ${details.length ? `<div>
      <div class="card-title" style="margin-bottom:10px">Agent Outputs</div>
      ${details.map(d => `<div class="expander" onclick="toggleExpander(this)">
        <div class="expander-hd">
          ${d.agent || 'Agent'}
          <svg class="expander-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="expander-bd">${(d.output || '').replace(/\n/g, '<br/>')}</div>
      </div>`).join('')}
    </div>` : ''}

    <hr class="divider" />
    <p class="dimmed" style="font-size:12px">Deep analysis reports are automatically saved to the database.</p>
  </div>`;
}

async function downloadAnalysisPDF() {
  if (!currentAnalysis) { toast('No analysis to download', 'warn'); return; }
  try {
    const res = await fetch(API + '/api/analysis/pdf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ analysis: currentAnalysis, label: currentAnalysisLabel }),
    });
    if (!res.ok) throw new Error('PDF generation failed');
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `analysis_${Date.now()}.pdf`; a.click();
    URL.revokeObjectURL(url);
    toast('PDF downloaded', 'success');
  } catch (e) {
    toast('PDF download failed: ' + e.message, 'error');
  }
}

// ── Reports ────────────────────────────────────────────────────────────
async function loadReports() {
  const result = $('reportsResult');
  result.innerHTML = spinner('Loading reports…');

  try {
    const reports = await apiFetch('/api/reports');

    if (!reports.length) {
      result.innerHTML = notice('info', 'No reports found. Generate one from the AI Insights page.');
      return;
    }

    result.innerHTML = `
      ${notice('info', `${reports.length} report${reports.length !== 1 ? 's' : ''} in database`)}
      ${reports.slice(0, 30).map(r => {
      const rtype = (r.report_type || '').replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase());
      const pl = r.platform === 'all' ? 'All Platforms' : (r.platform || '?').toUpperCase();
      const cat = r.category === 'all' ? 'All Categories' : (r.category || '?').replace(/\b\w/g, c => c.toUpperCase());
      const date = fmtDate(r.generated_at);
      const cnt = r.products_analyzed || 0;
      const rid = r._id;

      let summary = '';
      const an = r.analysis || {};
      if (r.report_type === 'quick_analysis' && an.price_range) {
        const pr = an.price_range;
        summary = `<div class="dimmed" style="font-size:12px;margin-top:8px">
            Price range: ${fmtPrice(pr.min)} — ${fmtPrice(pr.max)} · Avg: ${fmtPrice(pr.average)}
          </div>`;
        if ((an.price_insights || []).length) {
          summary += `<ul style="margin-top:6px;font-size:12px;color:var(--text-2);padding-left:16px">
              ${an.price_insights.slice(0, 3).map(i => `<li>${i}</li>`).join('')}
            </ul>`;
        }
      } else if (r.report_type === 'deep_analysis' && an.final_report) {
        summary = `<div class="dimmed" style="font-size:12px;margin-top:8px">${(an.final_report || '').slice(0, 220)}…</div>`;
      }

      return `<div class="expander" onclick="toggleExpander(this)">
          <div class="expander-hd">
            <span>${rtype} &mdash; ${pl} · ${cat} · ${cnt} products · ${date}</span>
            <svg class="expander-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="expander-bd" onclick="event.stopPropagation()">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px">
              <div>
                <div class="strong">${rtype}</div>
                <div class="dimmed" style="font-size:12px">Platform: ${pl} · Category: ${cat} · ${cnt} products</div>
                ${summary}
              </div>
              ${rid ? `<button class="btn btn-secondary btn-sm" style="flex-shrink:0" onclick="downloadReport('${rid}')">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                Download PDF
              </button>` : ''}
            </div>
          </div>
        </div>`;
    }).join('')}`;
  } catch (e) {
    result.innerHTML = notice('error', e.message);
  }
}

async function downloadReport(rid) {
  try {
    const res = await fetch(API + `/api/reports/${rid}/pdf`);
    if (!res.ok) throw new Error('PDF generation failed');
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `report_${rid}.pdf`; a.click();
    URL.revokeObjectURL(url);
    toast('PDF downloaded', 'success');
  } catch (e) {
    toast('PDF download failed: ' + e.message, 'error');
  }
}

// ── Expander ───────────────────────────────────────────────────────────
function toggleExpander(el) { el.classList.toggle('open'); }

// ── Render helpers ─────────────────────────────────────────────────────
function spinner(msg = 'Loading…') {
  return `<div class="spinner-wrap"><div class="spinner"></div><span>${msg}</span></div>`;
}

function notice(type, msg) {
  const n = { info: 'n-info', success: 'n-success', warn: 'n-warn', error: 'n-error' };
  return `<div class="notice ${n[type] || 'n-info'}">${msg}</div>`;
}

function kpiMini(label, value, variant = '--blue') {
  return `<div class="kpi-card kpi-card${variant}">
    <div class="kpi-top"><div class="kpi-label">${label}</div></div>
    <div class="kpi-value" style="font-size:20px">${value}</div>
  </div>`;
}

// ── Init ───────────────────────────────────────────────────────────────
(async function init() {
  await loadSidebarStats();
  loadDashboard();
})();
