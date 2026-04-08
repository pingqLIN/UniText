(() => {
  const INITIAL_DATA = window.PROJECT_MAP_BOOTSTRAP;
  const { TYPE_ORDER, CORE_DOCS, ROOT_DIRECTORIES, REPO_MARKERS } = window.PROJECT_MAP_CONSTANTS;
  const TYPE_LABELS = { doc: "Docs", directory: "Directories", skill: "Skills", mcp: "MCP", agent: "Agents", workflow: "Workflow" };
  const TYPE_STYLES = {
    doc: { fill: "#fff1c7", stroke: "#d29d21", badge: "#f4e1a2" },
    directory: { fill: "#dff4ee", stroke: "#3b8f81", badge: "#cfe8e1" },
    skill: { fill: "#e1ebff", stroke: "#5679c5", badge: "#d6e2fb" },
    mcp: { fill: "#f0dcff", stroke: "#9254c7", badge: "#e7cef9" },
    agent: { fill: "#ffdcca", stroke: "#d06c45", badge: "#f7cfbf" },
    workflow: { fill: "#e0f1d7", stroke: "#5b9b51", badge: "#d3e8ca" },
  };
  const EDGE_LABELS = { contains: "Contains", references: "References", catalog_entry: "Catalog", maps_to: "Maps To" };
  const EDGE_STYLES = {
    contains: { stroke: "#c4b89e", width: 1.05, opacity: 0.42, dash: "" },
    references: { stroke: "#2563eb", width: 1.6, opacity: 0.75, dash: "5 5" },
    catalog_entry: { stroke: "#0f766e", width: 1.9, opacity: 0.82, dash: "" },
    maps_to: { stroke: "#ca8a04", width: 1.8, opacity: 0.8, dash: "7 4" },
  };
  const SETTINGS_KEY = "unitext-project-map-settings-v2";
  const HANDLE_DB_NAME = "unitext-project-map-db";
  const HANDLE_STORE = "handles";
  const HANDLE_KEY = "repo-root";

  let DATA = JSON.parse(JSON.stringify(INITIAL_DATA));
  let nodeById = new Map((DATA.nodes || []).map((node) => [node.id, node]));
  const state = {
    search: "",
    type: "all",
    mapMode: "grid",
    updateMode: "manual",
    intervalDays: 1,
    intervalHours: 0,
    intervalMinutes: 0,
    selectedId: nodeById.has("doc:INDEX.md") ? "doc:INDEX.md" : DATA.nodes?.[0]?.id ?? null,
    repoHandle: null,
    repoHandleName: null,
    refreshInFlight: false,
    refreshTimerId: null,
    lastUpdatedAt: DATA.meta?.generated_at || null,
    lastRefreshDurationMs: null,
    lastRefreshSource: "bootstrap",
    lastRefreshState: "idle",
    lastRefreshMessage: "目前顯示的是最近一次靜態產出的 MAP。",
    browserCanScan: typeof window.showDirectoryPicker === "function" && typeof indexedDB !== "undefined",
  };

  const summaryEl = document.getElementById("summary");
  const sidebarEl = document.getElementById("sidebar");
  const detailEl = document.getElementById("detail");
  const mapEl = document.getElementById("map");
  const searchEl = document.getElementById("search");
  const typeFilterEl = document.getElementById("type-filter");
  const mapModeEl = document.getElementById("map-mode");
  const updateModeEl = document.getElementById("update-mode");
  const intervalDaysEl = document.getElementById("interval-days");
  const intervalHoursEl = document.getElementById("interval-hours");
  const intervalMinutesEl = document.getElementById("interval-minutes");
  const linkRepoEl = document.getElementById("link-repo");
  const refreshNowEl = document.getElementById("refresh-now");
  const updateStatusEl = document.getElementById("update-status");
  const nodeCountLabelEl = document.getElementById("node-count-label");
  const mapModeNoteEl = document.getElementById("map-mode-note");
  const mapCaptionEl = document.getElementById("map-caption");
  const detailNoteEl = document.getElementById("detail-note");

  const cloneData = (data) => JSON.parse(JSON.stringify(data));
  const escapeHtml = (text) => String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
  function setData(nextData, source) {
    DATA = cloneData(nextData);
    nodeById = new Map((DATA.nodes || []).map((node) => [node.id, node]));
    if (!nodeById.has(state.selectedId)) {
      state.selectedId = nodeById.has("doc:INDEX.md") ? "doc:INDEX.md" : DATA.nodes?.[0]?.id ?? null;
    }
    state.lastUpdatedAt = DATA.meta?.generated_at || new Date().toISOString();
    state.lastRefreshSource = source;
  }

  function setRefreshState(kind, message = "") {
    state.lastRefreshState = kind;
    if (message) state.lastRefreshMessage = message;
  }

  function syncActionButtons() {
    refreshNowEl.disabled = state.refreshInFlight;
    linkRepoEl.disabled = state.refreshInFlight;
    refreshNowEl.textContent = state.refreshInFlight ? "更新中..." : "立即更新";
    linkRepoEl.textContent = state.refreshInFlight ? "目錄鎖定中" : "連結專案目錄";
    refreshNowEl.dataset.state = state.lastRefreshState;
  }

  function loadSettings() {
    try {
      const raw = localStorage.getItem(SETTINGS_KEY);
      if (!raw) return;
      const settings = JSON.parse(raw);
      state.mapMode = settings.mapMode || state.mapMode;
      state.updateMode = settings.updateMode || state.updateMode;
      state.intervalDays = Number.isFinite(settings.intervalDays) ? settings.intervalDays : state.intervalDays;
      state.intervalHours = Number.isFinite(settings.intervalHours) ? settings.intervalHours : state.intervalHours;
      state.intervalMinutes = Number.isFinite(settings.intervalMinutes) ? settings.intervalMinutes : state.intervalMinutes;
    } catch (_error) {}
  }

  function saveSettings() {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify({
      mapMode: state.mapMode,
      updateMode: state.updateMode,
      intervalDays: state.intervalDays,
      intervalHours: state.intervalHours,
      intervalMinutes: state.intervalMinutes,
    }));
  }

  function applySettingsToControls() {
    mapModeEl.value = state.mapMode;
    updateModeEl.value = state.updateMode;
    intervalDaysEl.value = String(state.intervalDays);
    intervalHoursEl.value = String(state.intervalHours);
    intervalMinutesEl.value = String(state.intervalMinutes);
  }

  function intervalMs() {
    const days = Math.max(0, Number(intervalDaysEl.value || state.intervalDays || 0));
    const hours = Math.max(0, Number(intervalHoursEl.value || state.intervalHours || 0));
    const minutes = Math.max(0, Number(intervalMinutesEl.value || state.intervalMinutes || 0));
    return (((days * 24) + hours) * 60 + minutes) * 60 * 1000;
  }

  function rememberIntervalInputs() {
    state.intervalDays = Math.max(0, Number(intervalDaysEl.value || 0));
    state.intervalHours = Math.max(0, Number(intervalHoursEl.value || 0));
    state.intervalMinutes = Math.max(0, Number(intervalMinutesEl.value || 0));
    saveSettings();
    scheduleRefreshTimer();
    updateStatusCard();
  }

  function formatTimestamp(isoText) {
    if (!isoText) return "尚未更新";
    const date = new Date(isoText);
    if (Number.isNaN(date.getTime())) return isoText;
    return new Intl.DateTimeFormat("zh-TW", {
      year: "numeric", month: "2-digit", day: "2-digit",
      hour: "2-digit", minute: "2-digit", second: "2-digit",
    }).format(date);
  }

  function formatDuration(ms) {
    if (ms == null) return "尚無";
    if (ms < 1000) return `${Math.round(ms)} ms`;
    return `${(ms / 1000).toFixed(2)} s`;
  }

  function describeInterval() {
    const parts = [];
    if (state.intervalDays) parts.push(`${state.intervalDays} 天`);
    if (state.intervalHours) parts.push(`${state.intervalHours} 小時`);
    if (state.intervalMinutes) parts.push(`${state.intervalMinutes} 分`);
    return parts.length ? parts.join(" ") : "0 分";
  }

  function computeVisibleNodes() {
    return (DATA.nodes || []).filter((node) => {
      if (state.type !== "all" && node.type !== state.type) return false;
      if (!state.search) return true;
      const haystack = [node.label, node.path, node.logical_path, node.description]
        .filter(Boolean).join(" ").toLowerCase();
      return haystack.includes(state.search);
    });
  }

  function relatedEdges(nodeId, allowedIds = null) {
    return (DATA.edges || []).filter((edge) => {
      const touchesNode = edge.from === nodeId || edge.to === nodeId;
      if (!touchesNode) return false;
      if (!allowedIds) return true;
      return allowedIds.has(edge.from) && allowedIds.has(edge.to);
    });
  }

  function updateSummary() {
    summaryEl.innerHTML = "";
    Object.entries(DATA.counts || {}).forEach(([type, count]) => {
      const chip = document.createElement("div");
      chip.className = "chip";
      chip.textContent = `${TYPE_LABELS[type] || type}: ${count}`;
      summaryEl.appendChild(chip);
    });
    typeFilterEl.innerHTML = '<option value="all">全部類型</option>';
    TYPE_ORDER.forEach((type) => {
      const count = DATA.counts?.[type] || 0;
      if (!count) return;
      const option = document.createElement("option");
      option.value = type;
      option.textContent = `${TYPE_LABELS[type]} (${count})`;
      if (state.type === type) option.selected = true;
      typeFilterEl.appendChild(option);
    });
  }

  function updateStatusCard(errorText = "") {
    const modeLabel = { manual: "手動更新", "on-open": "開啟網頁時自動更新", interval: "定時更新" }[state.updateMode];
    const strategyNote = {
      manual: "不做背景掃描，只有按下「立即更新」才重新解析；執行開銷最低。",
      "on-open": "每次開啟頁面時做一次掃描，能降低 stale 風險，但會增加進頁時間。",
      interval: "頁面開啟期間依頻率重掃；資料較新，但會持續產生檔案 I/O 與重新繪圖成本。",
    }[state.updateMode];
    const repoText = state.repoHandleName ? `已連結：${state.repoHandleName}` : "尚未連結 repo root";
    const intervalText = state.updateMode === "interval" ? `；頻率：${describeInterval()}` : "";
    const supportText = state.browserCanScan
      ? "此瀏覽器支援頁內掃描與更新。"
      : "此瀏覽器不支援頁內掃描；仍可用 Python 腳本重新生成 HTML。";
    const stateText = {
      idle: "待命",
      progress: "更新中",
      success: "更新成功",
      error: "更新失敗",
    }[state.lastRefreshState];
    const safeMessage = escapeHtml(errorText || state.lastRefreshMessage || "目前沒有額外訊息。");
    const cardStateClass = errorText ? " error" : state.lastRefreshState === "progress"
      ? " progress"
      : state.lastRefreshState === "success"
        ? " success"
        : state.lastRefreshState === "error"
          ? " error"
          : "";
    updateStatusEl.className = `status-card${cardStateClass}`;
    updateStatusEl.innerHTML = `
      <div class="status-row">
        <span class="status-pill">${stateText}</span>
        <span class="status-inline-note">${safeMessage}</span>
      </div>
      <div><strong>更新模式</strong>：${modeLabel}${intervalText}</div>
      <div><strong>目錄授權</strong>：${repoText}</div>
      <div><strong>最近更新</strong>：${formatTimestamp(state.lastUpdatedAt)}；來源：${state.lastRefreshSource}；耗時：${formatDuration(state.lastRefreshDurationMs)}</div>
      <div><strong>策略評估</strong>：${strategyNote}</div>
      <div><strong>執行限制</strong>：${supportText} 定時更新只會在頁面保持開啟時生效，不會在頁面關閉時常駐執行。</div>
      ${errorText ? `<div><strong>最近錯誤</strong>：${escapeHtml(errorText)}</div>` : ""}
    `;
    syncActionButtons();
  }

  function renderSidebar(visible) {
    sidebarEl.innerHTML = "";
    const grouped = new Map(TYPE_ORDER.map((type) => [type, []]));
    visible.forEach((node) => grouped.get(node.type)?.push(node));
    TYPE_ORDER.forEach((type) => {
      const items = grouped.get(type) || [];
      if (!items.length) return;
      const title = document.createElement("div");
      title.className = "group-title";
      title.textContent = TYPE_LABELS[type] || type;
      sidebarEl.appendChild(title);
      items.slice().sort((a, b) => a.label.localeCompare(b.label)).forEach((node) => {
        const button = document.createElement("button");
        button.className = "node-button";
        if (node.id === state.selectedId) button.classList.add("active");
        const typeStyle = TYPE_STYLES[node.type] || TYPE_STYLES.directory;
        button.innerHTML = `
          <div class="node-head"><strong>${node.label}</strong><span class="node-type" style="background:${typeStyle.badge}">${node.type}</span></div>
          <span class="node-description">${node.description || "No description"}</span>
          <span class="node-path">${node.path}</span>
        `;
        button.addEventListener("click", () => { state.selectedId = node.id; render(); });
        sidebarEl.appendChild(button);
      });
    });
    nodeCountLabelEl.textContent = `目前顯示 ${visible.length} / ${(DATA.nodes || []).length} 個節點`;
  }

  function renderDetail(visibleIds) {
    const selected = nodeById.get(state.selectedId);
    if (!selected || !visibleIds.has(selected.id)) {
      detailEl.innerHTML = '<p class="empty">從左側或中央地圖選一個節點，即可查看 metadata 與關係。</p>';
      detailNoteEl.textContent = "聚焦節點後，會顯示所有關聯邊";
      return;
    }
    detailNoteEl.textContent = state.mapMode === "grid" ? "欄式視圖會依資源類型分層" : "圓形 / 扇形視圖會以所選節點為中心展開";
    const relatedAll = relatedEdges(selected.id);
    const outgoing = relatedAll.filter((edge) => edge.from === selected.id);
    const incoming = relatedAll.filter((edge) => edge.to === selected.id);
    const detailParts = [
      `<h3>${selected.label}</h3>`,
      `<p>${selected.description || "沒有額外描述。"}</p>`,
      '<div class="meta">',
      `<div class="meta-row"><strong>Type</strong>${selected.type}</div>`,
      `<div class="meta-row"><strong>Path</strong>${selected.path}</div>`,
    ];
    if (selected.logical_path) detailParts.push(`<div class="meta-row"><strong>Logical Path</strong>${selected.logical_path}</div>`);
    if (selected.status) detailParts.push(`<div class="meta-row"><strong>Status</strong>${selected.status}</div>`);
    if (selected.source_path) detailParts.push(`<div class="meta-row"><strong>Source File</strong>${selected.source_path}</div>`);
    detailParts.push("</div>");

    function pushEdgeSection(title, list, mode) {
      if (!list.length) return;
      detailParts.push(`<div class="section-title">${title}</div>`);
      detailParts.push('<div class="edge-list">');
      list.slice().sort((a, b) => (EDGE_LABELS[a.kind] || a.kind).localeCompare(EDGE_LABELS[b.kind] || b.kind)).forEach((edge) => {
        const peerId = mode === "outgoing" ? edge.to : edge.from;
        const peer = nodeById.get(peerId);
        if (!peer) return;
        const directionText = mode === "outgoing" ? `${selected.label} → ${peer.label}` : `${peer.label} → ${selected.label}`;
        const visible = visibleIds.has(peer.id);
        const visibilityText = visible ? "目前可見於地圖與節點清單" : "目前被搜尋或類型篩選隱藏";
        detailParts.push(`<div class="edge-item"><strong>${EDGE_LABELS[edge.kind] || edge.kind}</strong><div class="edge-direction">${directionText}</div><div>${peer.path}</div><div class="edge-visibility">${visibilityText}</div></div>`);
      });
      detailParts.push("</div>");
    }

    if (relatedAll.length) {
      pushEdgeSection("Outgoing", outgoing, "outgoing");
      pushEdgeSection("Incoming", incoming, "incoming");
    } else {
      detailParts.push('<p class="empty">目前沒有關聯邊。</p>');
    }
    detailEl.innerHTML = detailParts.join("");
  }

  function buildVisibleEdges(visibleIds) {
    return (DATA.edges || []).filter((edge) => visibleIds.has(edge.from) && visibleIds.has(edge.to));
  }

  function buildAdjacency(visibleIds) {
    const adjacency = new Map();
    visibleIds.forEach((id) => adjacency.set(id, new Set()));
    buildVisibleEdges(visibleIds).forEach((edge) => {
      adjacency.get(edge.from)?.add(edge.to);
      adjacency.get(edge.to)?.add(edge.from);
    });
    return adjacency;
  }

  function computeDepths(visible) {
    const ids = new Set(visible.map((node) => node.id));
    const adjacency = buildAdjacency(ids);
    const selectedId = state.selectedId;
    const depths = new Map();
    if (selectedId && ids.has(selectedId)) {
      const queue = [[selectedId, 0]];
      depths.set(selectedId, 0);
      while (queue.length) {
        const [current, depth] = queue.shift();
        (adjacency.get(current) || []).forEach((neighbor) => {
          if (!depths.has(neighbor)) {
            depths.set(neighbor, depth + 1);
            queue.push([neighbor, depth + 1]);
          }
        });
      }
    }
    let maxDepth = 0;
    depths.forEach((depth) => { maxDepth = Math.max(maxDepth, depth); });
    visible.map((node) => node.id).filter((id) => !depths.has(id)).sort((a, b) => (nodeById.get(a)?.label || "").localeCompare(nodeById.get(b)?.label || "")).forEach((id, index) => {
      depths.set(id, maxDepth + 1 + Math.floor(index / 10));
    });
    return depths;
  }

  function layoutGrid(visible) {
    const grouped = new Map(TYPE_ORDER.map((type) => [type, []]));
    visible.forEach((node) => grouped.get(node.type)?.push(node));
    const columnWidth = 220;
    const baseX = 90;
    const topPadding = 90;
    const rowGap = 82;
    const boxHeight = 56;
    const positions = new Map();
    let maxRows = 0;
    TYPE_ORDER.forEach((type, index) => {
      const items = (grouped.get(type) || []).slice().sort((a, b) => a.label.localeCompare(b.label));
      maxRows = Math.max(maxRows, items.length);
      items.forEach((node, rowIndex) => {
        positions.set(node.id, { x: baseX + index * columnWidth, y: topPadding + rowIndex * rowGap, width: 188, height: boxHeight, type });
      });
    });
    return { positions, width: baseX + TYPE_ORDER.length * columnWidth + 120, height: Math.max(920, topPadding + maxRows * rowGap + 120) };
  }

  function layoutOrbit(visible, mode) {
    const depths = computeDepths(visible);
    const positions = new Map();
    const selectedId = state.selectedId && nodeById.has(state.selectedId) ? state.selectedId : visible[0]?.id ?? null;
    const width = mode === "fan" ? 1760 : 1500;
    const height = mode === "fan" ? 1120 : 1020;
    const center = mode === "fan" ? { x: 250, y: 560 } : { x: width / 2, y: height / 2 };
    const ringBase = mode === "fan" ? 210 : 180;
    const ringGap = mode === "fan" ? 180 : 150;
    if (selectedId) {
      positions.set(selectedId, { x: center.x - 118, y: center.y - 34, width: 236, height: 68, type: nodeById.get(selectedId)?.type || "directory" });
    }
    const tierGroups = new Map();
    visible.forEach((node) => {
      if (node.id === selectedId) return;
      const depth = depths.get(node.id) || 1;
      if (!tierGroups.has(depth)) tierGroups.set(depth, []);
      tierGroups.get(depth).push(node);
    });
    Array.from(tierGroups.entries()).sort((a, b) => a[0] - b[0]).forEach(([depth, items]) => {
      const radius = ringBase + (depth - 1) * ringGap;
      const sorted = items.slice().sort((a, b) => {
        if (a.type !== b.type) return TYPE_ORDER.indexOf(a.type) - TYPE_ORDER.indexOf(b.type);
        return a.label.localeCompare(b.label);
      });
      const count = sorted.length;
      sorted.forEach((node, index) => {
        const boxWidth = mode === "fan" ? (depth === 1 ? 210 : 184) : (depth === 1 ? 190 : 176);
        const boxHeight = mode === "fan" && depth === 1 ? 60 : 56;
        let angle = -Math.PI / 2;
        if (mode === "radial") {
          angle = count === 1 ? -Math.PI / 2 : (-Math.PI / 2) + ((Math.PI * 2) * index) / count;
        } else {
          const spread = Math.min(Math.PI * 1.22, Math.PI * (0.42 + depth * 0.1));
          const baseAngle = 0;
          const start = baseAngle - spread / 2;
          angle = count === 1 ? baseAngle : start + (spread * index) / (count - 1);
        }
        const depthLift = mode === "fan" ? (depth - 1) * 14 : 0;
        const x = center.x + Math.cos(angle) * radius - boxWidth / 2;
        const y = center.y + Math.sin(angle) * radius - boxHeight / 2 - depthLift;
        positions.set(node.id, { x, y, width: boxWidth, height: boxHeight, type: node.type });
      });
    });
    return { positions, width, height, center, depths };
  }

  function renderMap(visible, visibleIds) {
    const selectedId = state.selectedId;
    const layout = state.mapMode === "grid" ? layoutGrid(visible) : layoutOrbit(visible, state.mapMode);
    const positions = layout.positions;
    mapEl.setAttribute("viewBox", `0 0 ${layout.width} ${layout.height}`);
    mapEl.innerHTML = "";
    const titleLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
    if (state.mapMode === "grid") {
      TYPE_ORDER.forEach((type) => {
        const sample = Array.from(positions.values()).find((entry) => entry.type === type);
        const x = sample ? sample.x : 90 + TYPE_ORDER.indexOf(type) * 220;
        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", String(x));
        label.setAttribute("y", "46");
        label.setAttribute("fill", "#5f5a4b");
        label.setAttribute("font-size", "15");
        label.setAttribute("font-weight", "700");
        label.textContent = TYPE_LABELS[type] || type;
        titleLayer.appendChild(label);
      });
    } else {
      const selected = nodeById.get(selectedId);
      const orbitLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
      const depthValues = Array.from((layout.depths || new Map()).values()).filter((depth) => depth > 0);
      const maxDepth = depthValues.length ? Math.max(...depthValues) : 0;
      for (let depth = 1; depth <= maxDepth; depth += 1) {
        if (state.mapMode === "fan") {
          const guide = document.createElementNS("http://www.w3.org/2000/svg", "path");
          const radius = 210 + ((depth - 1) * 180);
          const spread = Math.min(Math.PI * 1.22, Math.PI * (0.42 + depth * 0.1));
          const startAngle = -spread / 2;
          const endAngle = spread / 2;
          const startX = layout.center.x + Math.cos(startAngle) * radius;
          const startY = layout.center.y + Math.sin(startAngle) * radius - ((depth - 1) * 14);
          const endX = layout.center.x + Math.cos(endAngle) * radius;
          const endY = layout.center.y + Math.sin(endAngle) * radius - ((depth - 1) * 14);
          guide.setAttribute("d", `M ${layout.center.x} ${layout.center.y} L ${startX} ${startY} A ${radius} ${radius} 0 0 1 ${endX} ${endY} L ${layout.center.x} ${layout.center.y}`);
          guide.setAttribute("fill", depth % 2 === 0 ? "rgba(15, 118, 110, 0.03)" : "rgba(202, 138, 4, 0.035)");
          guide.setAttribute("stroke", "rgba(131, 114, 82, 0.16)");
          guide.setAttribute("stroke-width", "1");
          orbitLayer.appendChild(guide);
        } else {
          const ring = document.createElementNS("http://www.w3.org/2000/svg", "circle");
          ring.setAttribute("cx", String(layout.center.x));
          ring.setAttribute("cy", String(layout.center.y));
          ring.setAttribute("r", String(180 + ((depth - 1) * 150)));
          ring.setAttribute("fill", "none");
          ring.setAttribute("stroke", "rgba(131, 114, 82, 0.18)");
          ring.setAttribute("stroke-width", "1");
          ring.setAttribute("stroke-dasharray", "4 8");
          orbitLayer.appendChild(ring);
        }
      }
      mapEl.appendChild(orbitLayer);
      const header = document.createElementNS("http://www.w3.org/2000/svg", "text");
      header.setAttribute("x", "44");
      header.setAttribute("y", "46");
      header.setAttribute("fill", "#5f5a4b");
      header.setAttribute("font-size", "16");
      header.setAttribute("font-weight", "700");
      header.textContent = `${state.mapMode === "radial" ? "圓形" : "扇形"}視圖：以 ${selected?.label || "目前節點"} 為中心`;
      titleLayer.appendChild(header);
      const sub = document.createElementNS("http://www.w3.org/2000/svg", "text");
      sub.setAttribute("x", "44");
      sub.setAttribute("y", "70");
      sub.setAttribute("fill", "#7a705e");
      sub.setAttribute("font-size", "12");
      sub.textContent = "第一圈優先呈現直接相鄰節點；更外圈為較遠或未連通節點。";
      titleLayer.appendChild(sub);
    }
    mapEl.appendChild(titleLayer);

    const edgeLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
    buildVisibleEdges(visibleIds).forEach((edge) => {
      const from = positions.get(edge.from);
      const to = positions.get(edge.to);
      if (!from || !to) return;
      const style = EDGE_STYLES[edge.kind] || EDGE_STYLES.contains;
      const active = edge.from === selectedId || edge.to === selectedId;
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", String(from.x + from.width / 2));
      line.setAttribute("y1", String(from.y + from.height / 2));
      line.setAttribute("x2", String(to.x + to.width / 2));
      line.setAttribute("y2", String(to.y + to.height / 2));
      line.setAttribute("stroke", active ? "#0f766e" : style.stroke);
      line.setAttribute("stroke-width", active ? String(style.width + 0.9) : String(style.width));
      line.setAttribute("stroke-opacity", active ? "0.96" : String(style.opacity));
      if (style.dash) line.setAttribute("stroke-dasharray", style.dash);
      edgeLayer.appendChild(line);
    });
    mapEl.appendChild(edgeLayer);

    const nodeLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
    visible.slice().sort((a, b) => (a.id === selectedId ? 1 : 0) - (b.id === selectedId ? 1 : 0)).forEach((node) => {
      const box = positions.get(node.id);
      if (!box) return;
      const active = node.id === selectedId;
      const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
      group.style.cursor = "pointer";
      const typeStyle = TYPE_STYLES[node.type] || TYPE_STYLES.directory;

      const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", String(box.x));
      rect.setAttribute("y", String(box.y));
      rect.setAttribute("width", String(box.width));
      rect.setAttribute("height", String(box.height));
      rect.setAttribute("rx", active ? "18" : "14");
      rect.setAttribute("fill", active ? "#fffdf7" : typeStyle.fill);
      rect.setAttribute("stroke", active ? "#0f766e" : typeStyle.stroke);
      rect.setAttribute("stroke-width", active ? "2.2" : "1");
      group.appendChild(rect);

      const accent = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      accent.setAttribute("x", String(box.x));
      accent.setAttribute("y", String(box.y));
      accent.setAttribute("width", "6");
      accent.setAttribute("height", String(box.height));
      accent.setAttribute("rx", active ? "18" : "14");
      accent.setAttribute("fill", active ? "#0f766e" : typeStyle.stroke);
      group.appendChild(accent);

      const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("x", String(box.x + 16));
      label.setAttribute("y", String(box.y + (active ? 25 : 22)));
      label.setAttribute("fill", "#1f1f1f");
      label.setAttribute("font-size", active ? "14" : "13");
      label.setAttribute("font-weight", active ? "700" : "600");
      label.textContent = node.label.length > 27 ? `${node.label.slice(0, 26)}…` : node.label;
      group.appendChild(label);

      const sub = document.createElementNS("http://www.w3.org/2000/svg", "text");
      sub.setAttribute("x", String(box.x + 16));
      sub.setAttribute("y", String(box.y + (active ? 45 : 40)));
      sub.setAttribute("fill", "#6f6a5a");
      sub.setAttribute("font-size", active ? "11" : "10.5");
      sub.textContent = `${TYPE_LABELS[node.type] || node.type} · ${node.status || "active"}`;
      group.appendChild(sub);

      group.addEventListener("click", () => {
        state.selectedId = node.id;
        render();
      });
      nodeLayer.appendChild(group);
    });
    mapEl.appendChild(nodeLayer);

    if (state.mapMode === "grid") {
      mapModeNoteEl.textContent = "欄式視圖：依資源類型分欄，適合全域巡覽";
      mapCaptionEl.textContent = "欄式視圖有助於看清每一類資源的總量與大致關係。";
    } else if (state.mapMode === "radial") {
      mapModeNoteEl.textContent = "圓形視圖：以所選節點為圓心向外展開";
      mapCaptionEl.textContent = "第一圈優先是直接關聯節點，越外圈代表越遠或未連通的節點。";
    } else {
      mapModeNoteEl.textContent = "扇形視圖：以所選節點為圓心，朝單側閱讀面擴展";
      mapCaptionEl.textContent = "扇形視圖將第一層關聯壓在視線前方，越外圈越像往右展開的閱讀路徑，更適合沿關聯鏈逐步追蹤。";
    }
  }

  function render() {
    updateSummary();
    const visible = computeVisibleNodes();
    const ids = new Set(visible.map((node) => node.id));
    if (!ids.has(state.selectedId)) state.selectedId = visible[0]?.id ?? null;
    renderSidebar(visible);
    renderMap(visible, ids);
    renderDetail(ids);
  }

  function parseFrontmatter(text) {
    const normalized = text.replace(/\uFEFF/g, "").replace(/\r\n/g, "\n");
    if (!normalized.startsWith("---\n")) return {};
    const end = normalized.indexOf("\n---\n", 4);
    if (end === -1) return {};
    const body = {};
    normalized.slice(4, end).split("\n").forEach((line) => {
      const trimmed = line.trim();
      if (!trimmed || !trimmed.includes(":")) return;
      const [key, ...rest] = trimmed.split(":");
      body[key.trim()] = rest.join(":").trim().replace(/^["']|["']$/g, "");
    });
    return body;
  }

  const extractTitle = (text, fallback) => {
    const match = text.match(/^#\s+(.+)$/m);
    return match ? match[1].trim() : fallback;
  };
  const labelForCoreDoc = (relative, text) => relative === "README.md" ? "README" : extractTitle(text, relative.replace(/\.md$/i, ""));
  const nodeIdFor = (kind, key) => `${kind}:${key}`;

  function normalizeSegments(parts) {
    const out = [];
    parts.forEach((part) => {
      if (!part || part === ".") return;
      if (part === "..") {
        out.pop();
        return;
      }
      out.push(part);
    });
    return out;
  }

  const normalizeRepoPath = (pathText) => "/" + normalizeSegments(pathText.split("/")).join("/");
  function resolveRelativeRepoPath(sourcePath, target) {
    const cleanTarget = target.split("#", 1)[0];
    if (!cleanTarget || cleanTarget.startsWith("http") || cleanTarget.startsWith("mailto:") || cleanTarget.startsWith("#")) return null;
    const sourceSegments = sourcePath.replace(/^\//, "").split("/");
    sourceSegments.pop();
    const targetSegments = cleanTarget.replace(/^\//, "").split("/");
    return normalizeRepoPath([...sourceSegments, ...targetSegments].join("/"));
  }

  async function openHandleDb() {
    return await new Promise((resolve, reject) => {
      const request = indexedDB.open(HANDLE_DB_NAME, 1);
      request.onupgradeneeded = () => request.result.createObjectStore(HANDLE_STORE);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async function saveRepoHandle(handle) {
    const db = await openHandleDb();
    await new Promise((resolve, reject) => {
      const tx = db.transaction(HANDLE_STORE, "readwrite");
      tx.objectStore(HANDLE_STORE).put(handle, HANDLE_KEY);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
    db.close();
  }

  async function loadRepoHandle() {
    const db = await openHandleDb();
    const handle = await new Promise((resolve, reject) => {
      const tx = db.transaction(HANDLE_STORE, "readonly");
      const request = tx.objectStore(HANDLE_STORE).get(HANDLE_KEY);
      request.onsuccess = () => resolve(request.result || null);
      request.onerror = () => reject(request.error);
    });
    db.close();
    return handle;
  }

  async function hasReadPermission(handle, request = false) {
    const options = { mode: "read" };
    if ((await handle.queryPermission(options)) === "granted") return true;
    if (request && (await handle.requestPermission(options)) === "granted") return true;
    return false;
  }

  async function getDirectoryHandle(rootHandle, relativePath) {
    let current = rootHandle;
    const parts = relativePath.split("/").filter(Boolean);
    for (const part of parts) current = await current.getDirectoryHandle(part);
    return current;
  }

  async function readTextFromRepo(rootHandle, relativePath) {
    const parts = relativePath.split("/").filter(Boolean);
    const fileName = parts.pop();
    let current = rootHandle;
    for (const part of parts) current = await current.getDirectoryHandle(part);
    const fileHandle = await current.getFileHandle(fileName);
    const file = await fileHandle.getFile();
    return await file.text();
  }

  async function pathExists(rootHandle, relativePath, kind) {
    try {
      if (kind === "directory") await getDirectoryHandle(rootHandle, relativePath);
      else await readTextFromRepo(rootHandle, relativePath);
      return true;
    } catch (_error) {
      return false;
    }
  }

  async function listChildDirectories(rootHandle, relativePath) {
    const dirHandle = await getDirectoryHandle(rootHandle, relativePath);
    const names = [];
    for await (const [name, handle] of dirHandle.entries()) {
      if (handle.kind === "directory") names.push(name);
    }
    return names.sort((a, b) => a.localeCompare(b));
  }

  async function scanRepo(rootHandle) {
    for (const marker of REPO_MARKERS) {
      const exists = marker.endsWith("/skills") || marker.endsWith("/mcp")
        ? await pathExists(rootHandle, marker, "directory")
        : await pathExists(rootHandle, marker, "file");
      if (!exists) throw new Error(`選取的資料夾缺少 repo marker: ${marker}`);
    }

    const nodes = [];
    const pathToNodeId = new Map();
    const logicalToNodeId = new Map();
    function register(node) {
      nodes.push(node);
      pathToNodeId.set(node.path, node.id);
      if (node.logical_path) logicalToNodeId.set(node.logical_path, node.id);
    }

    register({ id: "repo:root", type: "directory", label: "Repo Root", path: "/", logical_path: "/", status: "repo-root", description: "Repository root directory" });
    ROOT_DIRECTORIES.forEach(([relative, label, logicalPath]) => {
      register({
        id: nodeIdFor("dir", relative),
        type: "directory",
        label,
        path: `/${relative}`,
        logical_path: logicalPath,
        status: "canonical-root",
        description: `Canonical ${label} root`,
        source_path: `/${relative}`,
      });
    });

    for (const relative of CORE_DOCS) {
      if (!(await pathExists(rootHandle, relative, "file"))) continue;
      const text = await readTextFromRepo(rootHandle, relative);
      register({
        id: nodeIdFor("doc", relative),
        type: "doc",
        label: labelForCoreDoc(relative, text),
        path: `/${relative}`,
        logical_path: `/${relative}`,
        status: "core-doc",
        description: extractTitle(text, relative.replace(/\.md$/i, "")),
        source_path: `/${relative}`,
      });
    }

    for (const skillName of await listChildDirectories(rootHandle, "registry/skills")) {
      const skillPath = `registry/skills/${skillName}/SKILL.md`;
      if (!(await pathExists(rootHandle, skillPath, "file"))) continue;
      const text = await readTextFromRepo(rootHandle, skillPath);
      const frontmatter = parseFrontmatter(text);
      const label = frontmatter.name || skillName;
      register({
        id: nodeIdFor("skill", label),
        type: "skill",
        label,
        path: `/registry/skills/${skillName}`,
        logical_path: `/registry/skills/${skillName}`,
        status: "active",
        description: frontmatter.description || null,
        source_path: `/${skillPath}`,
      });
    }

    for (const mcpDir of await listChildDirectories(rootHandle, "registry/mcp")) {
      const definitionPath = `registry/mcp/${mcpDir}/definition.json`;
      if (!(await pathExists(rootHandle, definitionPath, "file"))) continue;
      const definition = JSON.parse(await readTextFromRepo(rootHandle, definitionPath));
      let serverId = mcpDir;
      let notes = null;
      const servers = definition.mcpServers || {};
      const firstKey = Object.keys(servers)[0];
      if (firstKey) {
        serverId = firstKey;
        notes = servers[firstKey]?.notes || null;
      }
      register({
        id: nodeIdFor("mcp", serverId),
        type: "mcp",
        label: serverId,
        path: `/registry/mcp/${mcpDir}`,
        logical_path: `/registry/mcp/${mcpDir}`,
        status: "active-baseline",
        description: notes,
        source_path: `/${definitionPath}`,
      });
    }

    for (const agentDir of await listChildDirectories(rootHandle, "registry/agents")) {
      const agentPath = `registry/agents/${agentDir}/AGENT.md`;
      if (!(await pathExists(rootHandle, agentPath, "file"))) continue;
      const text = await readTextFromRepo(rootHandle, agentPath);
      register({
        id: nodeIdFor("agent", agentDir),
        type: "agent",
        label: agentDir,
        path: `/registry/agents/${agentDir}`,
        logical_path: `/registry/agents/${agentDir}`,
        status: "active",
        description: extractTitle(text, agentDir),
        source_path: `/${agentPath}`,
      });
    }

    for (const workflowDir of await listChildDirectories(rootHandle, "registry/workflow")) {
      let workflowFile = `registry/workflow/${workflowDir}/WORKFLOW.md`;
      if (!(await pathExists(rootHandle, workflowFile, "file"))) workflowFile = `registry/workflow/${workflowDir}/README.md`;
      if (!(await pathExists(rootHandle, workflowFile, "file"))) continue;
      const text = await readTextFromRepo(rootHandle, workflowFile);
      register({
        id: nodeIdFor("workflow", workflowDir),
        type: "workflow",
        label: workflowDir,
        path: `/registry/workflow/${workflowDir}`,
        logical_path: `/registry/workflow/${workflowDir}`,
        status: "draft",
        description: extractTitle(text, workflowDir),
        source_path: `/${workflowFile}`,
      });
    }

    const edges = [];
    const seen = new Set();
    const addEdge = (fromId, toId, kind) => {
      if (!fromId || !toId || fromId === toId) return;
      const key = `${fromId}::${toId}::${kind}`;
      if (seen.has(key)) return;
      seen.add(key);
      edges.push({ from: fromId, to: toId, kind });
    };

    nodes.forEach((node) => {
      if (node.id === "repo:root") return;
      if (node.type === "directory") {
        addEdge("repo:root", node.id, "contains");
        return;
      }
      if (node.path.startsWith("/registry/skills/")) addEdge(nodeIdFor("dir", "registry/skills"), node.id, "contains");
      else if (node.path.startsWith("/registry/mcp/")) addEdge(nodeIdFor("dir", "registry/mcp"), node.id, "contains");
      else if (node.path.startsWith("/registry/agents/")) addEdge(nodeIdFor("dir", "registry/agents"), node.id, "contains");
      else if (node.path.startsWith("/registry/workflow/")) addEdge(nodeIdFor("dir", "registry/workflow"), node.id, "contains");
      else addEdge("repo:root", node.id, "contains");
    });

    const markdownSources = [];
    for (const relative of CORE_DOCS) if (await pathExists(rootHandle, relative, "file")) markdownSources.push(relative);
    for (const agentDir of await listChildDirectories(rootHandle, "registry/agents")) {
      const relative = `registry/agents/${agentDir}/AGENT.md`;
      if (await pathExists(rootHandle, relative, "file")) markdownSources.push(relative);
    }
    for (const workflowDir of await listChildDirectories(rootHandle, "registry/workflow")) {
      for (const relative of [`registry/workflow/${workflowDir}/README.md`, `registry/workflow/${workflowDir}/WORKFLOW.md`]) {
        if (await pathExists(rootHandle, relative, "file")) markdownSources.push(relative);
      }
    }

    const linkPattern = /\[[^\]]+\]\(([^)]+)\)/g;
    for (const relative of markdownSources) {
      const sourcePath = `/${relative}`;
      const sourceId = pathToNodeId.get(sourcePath);
      if (!sourceId) continue;
      const text = await readTextFromRepo(rootHandle, relative);
      let match;
      while ((match = linkPattern.exec(text)) !== null) {
        const targetPath = resolveRelativeRepoPath(sourcePath, match[1]);
        if (!targetPath) continue;
        const targetId = pathToNodeId.get(targetPath);
        if (targetId) addEdge(sourceId, targetId, "references");
      }
    }

    if (await pathExists(rootHandle, "INDEX.md", "file")) {
      const indexId = pathToNodeId.get("/INDEX.md");
      const indexText = await readTextFromRepo(rootHandle, "INDEX.md");
      if (indexId) {
        logicalToNodeId.forEach((targetId, logicalPath) => {
          if (logicalPath.startsWith("/registry/") && indexText.includes(logicalPath)) {
            addEdge(indexId, targetId, "catalog_entry");
          }
        });
      }
    }

    const operationsId = pathToNodeId.get("/OPERATIONS.md");
    if (operationsId) {
      ["/registry/skills", "/registry/mcp", "/registry/agents", "/registry/workflow"].forEach((logicalPath) => {
        const targetId = logicalToNodeId.get(logicalPath);
        if (targetId) addEdge(operationsId, targetId, "maps_to");
      });
    }

    const counts = {};
    nodes.forEach((node) => { counts[node.type] = (counts[node.type] || 0) + 1; });
    return { meta: { generated_at: new Date().toISOString(), source_root: "/", version: 2 }, counts, nodes, edges };
  }

  async function connectRepoDirectory() {
    if (!state.browserCanScan) {
      setRefreshState("error", "目前瀏覽器不支援頁內更新。");
      updateStatusCard("目前瀏覽器不支援 File System Access API，請改用 Python 重新生成。");
      return;
    }
    const handle = await window.showDirectoryPicker({ mode: "read" });
    if (!(await hasReadPermission(handle, true))) throw new Error("沒有取得讀取權限。");
    await saveRepoHandle(handle);
    state.repoHandle = handle;
    state.repoHandleName = handle.name;
    setRefreshState("success", `已連結 ${handle.name}，之後可直接從頁面更新。`);
    updateStatusCard();
  }

  async function ensureRepoHandle(requestInteractive = false) {
    if (state.repoHandle) {
      const allowed = await hasReadPermission(state.repoHandle, requestInteractive);
      if (allowed) return state.repoHandle;
    }
    if (!state.browserCanScan) return null;
    const stored = await loadRepoHandle();
    if (stored && (await hasReadPermission(stored, requestInteractive))) {
      state.repoHandle = stored;
      state.repoHandleName = stored.name;
      return stored;
    }
    if (requestInteractive) {
      await connectRepoDirectory();
      return state.repoHandle;
    }
    return null;
  }

  async function refreshFromRepo(reason, requestInteractive = false) {
    if (state.refreshInFlight) return;
    const handle = await ensureRepoHandle(requestInteractive);
    if (!handle) {
      setRefreshState("error", "尚未連結 repo root。");
      updateStatusCard("尚未連結 repo root，無法執行頁內更新。");
      return;
    }
    state.refreshInFlight = true;
    setRefreshState("progress", "正在重新掃描 repo 並重建節點關係。");
    updateStatusCard();
    const startedAt = performance.now();
    try {
      const payload = await scanRepo(handle);
      setData(payload, reason);
      state.lastRefreshDurationMs = performance.now() - startedAt;
      setRefreshState("success", `已完成 ${reason} 更新，MAP 與關聯資料已刷新。`);
      render();
      updateStatusCard();
    } catch (error) {
      setRefreshState("error", error instanceof Error ? error.message : String(error));
      updateStatusCard(error instanceof Error ? error.message : String(error));
    } finally {
      state.refreshInFlight = false;
      syncActionButtons();
    }
  }

  function scheduleRefreshTimer() {
    if (state.refreshTimerId) {
      clearInterval(state.refreshTimerId);
      state.refreshTimerId = null;
    }
    const ms = intervalMs();
    if (state.updateMode === "interval" && ms > 0) {
      state.refreshTimerId = window.setInterval(() => { refreshFromRepo("interval"); }, ms);
    }
  }

  async function maybeAutoRefreshOnLoad() {
    if (!state.browserCanScan) {
      setRefreshState("idle", "此瀏覽器只支援閱讀靜態 MAP。");
      updateStatusCard();
      return;
    }
    const handle = await ensureRepoHandle(false);
    if (handle) state.repoHandleName = handle.name;
    if (handle) {
      setRefreshState("idle", `已載入 ${handle.name} 的目錄授權，可依設定自動更新。`);
    }
    scheduleRefreshTimer();
    updateStatusCard();
    if (state.updateMode === "on-open") {
      await refreshFromRepo("on-open");
      return;
    }
    if (state.updateMode === "interval") {
      const ms = intervalMs();
      const last = state.lastUpdatedAt ? new Date(state.lastUpdatedAt).getTime() : 0;
      if (ms > 0 && Date.now() - last >= ms) await refreshFromRepo("interval-overdue");
    }
  }

  function setupControls() {
    loadSettings();
    applySettingsToControls();
    searchEl.addEventListener("input", () => { state.search = searchEl.value.trim().toLowerCase(); render(); });
    typeFilterEl.addEventListener("change", () => { state.type = typeFilterEl.value; render(); });
    mapModeEl.addEventListener("change", () => { state.mapMode = mapModeEl.value; saveSettings(); render(); });
    updateModeEl.addEventListener("change", () => { state.updateMode = updateModeEl.value; saveSettings(); scheduleRefreshTimer(); updateStatusCard(); });
    [intervalDaysEl, intervalHoursEl, intervalMinutesEl].forEach((input) => input.addEventListener("change", rememberIntervalInputs));
    linkRepoEl.addEventListener("click", async () => {
      try { await connectRepoDirectory(); }
      catch (error) { updateStatusCard(error instanceof Error ? error.message : String(error)); }
    });
    refreshNowEl.addEventListener("click", () => { refreshFromRepo("manual-button", true); });
  }

  setupControls();
  render();
  maybeAutoRefreshOnLoad();
})();
