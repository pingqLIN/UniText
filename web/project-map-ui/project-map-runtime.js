(() => {
  const INITIAL_DATA = window.PROJECT_MAP_BOOTSTRAP;
  const PAGE_MODE = window.PROJECT_MAP_PAGE_MODE || "interactive";
  const {
    TYPE_ORDER,
    CORE_DOCS,
    ROOT_DIRECTORIES,
    REPO_MARKERS,
    PROJECT_MAP_ADAPTERS,
    ACTIVE_PROJECT_MAP_ADAPTER,
  } = window.PROJECT_MAP_CONSTANTS;
  const TYPE_LABELS = {
    doc: "文件",
    directory: "根目錄",
    runtime: "執行面",
    skill: "技能註冊",
    mcp: "MCP 註冊",
    agent: "代理註冊",
    workflow: "流程註冊",
  };
  const QUICK_FILTER_SPECS = [
    { kind: "type", value: "agent", label: "代理註冊", colorVar: "--type-agent-fill", colorFallback: "#efddd3" },
    { kind: "type", value: "directory", label: "根目錄", colorVar: "--type-directory-fill", colorFallback: "#dce9e1" },
    { kind: "type", value: "doc", label: "文件", colorVar: "--type-doc-fill", colorFallback: "#f3e6bf" },
    { kind: "type", value: "mcp", label: "MCP 註冊", colorVar: "--type-mcp-fill", colorFallback: "#e7deeb" },
    { kind: "type", value: "runtime", label: "執行面", colorVar: "--type-runtime-fill", colorFallback: "#d9ebef" },
    { kind: "type", value: "skill", label: "技能註冊", colorVar: "--type-skill-fill", colorFallback: "#dee4ef" },
    { kind: "type", value: "workflow", label: "流程註冊", colorVar: "--type-workflow-fill", colorFallback: "#dce5d4" },
    { kind: "diagnostic", value: "broken-source", label: "失效引用", colorFallback: "#f3d9a0" },
    { kind: "diagnostic", value: "orphan", label: "孤立資源", colorFallback: "#edd3a5" },
  ];
  const TYPE_STYLE_FALLBACKS = {
    doc: { fill: "#f3e6bf", stroke: "#b28a44", badge: "#eadbb0" },
    directory: { fill: "#dce9e1", stroke: "#5d8370", badge: "#d0dfd6" },
    runtime: { fill: "#d9ebef", stroke: "#3c7f8f", badge: "#cfe2e7" },
    skill: { fill: "#dee4ef", stroke: "#667da4", badge: "#d4dbea" },
    mcp: { fill: "#e7deeb", stroke: "#806b8f", badge: "#ddd1e4" },
    agent: { fill: "#efddd3", stroke: "#aa6b52", badge: "#e6d0c2" },
    workflow: { fill: "#dce5d4", stroke: "#6d8660", badge: "#d2dcc8" },
  };
  const EDGE_LABELS = { contains: "包含", references: "引用", catalog_entry: "目錄對應", maps_to: "正式來源對應" };
  const EDGE_STYLES = {
    contains: { stroke: "#c4b89e", width: 1.05, opacity: 0.42, dash: "" },
    references: { stroke: "#2563eb", width: 1.6, opacity: 0.75, dash: "5 5" },
    catalog_entry: { stroke: "#0f766e", width: 1.9, opacity: 0.82, dash: "" },
    maps_to: { stroke: "#ca8a04", width: 1.8, opacity: 0.8, dash: "7 4" },
  };
  const MAP_MODES = new Set(["grid", "radial"]);
  const VISUAL_TONE_ORDER = ["mono", "muted", "vivid"];
  const VISUAL_TONES = new Set(VISUAL_TONE_ORDER);
  const VISUAL_THEME_ORDER = ["light", "dark"];
  const VISUAL_THEMES = new Set(VISUAL_THEME_ORDER);
  const TEXT_SCALE_ORDER = ["xs", "sm", "md", "lg", "xl"];
  const TEXT_SCALES = new Set(TEXT_SCALE_ORDER);
  const TEXT_SCALE_FACTORS = { xs: 0.84, sm: 0.92, md: 1, lg: 1.12, xl: 1.24 };
  const SETTINGS_KEY = "unitext-project-map-settings-v2";
  const TOUR_STORAGE_KEY = "unitext-project-map-tour-v1";
  const PANEL_FOCUS_COOLDOWN_MS = 700;
  const TEMP_PANEL_AUTO_COMPACT = true;
  const TEMP_TOUR_ENTRY_CUE = false;
  const HANDLE_DB_NAME = "unitext-project-map-db";
  const HANDLE_STORE = "handles";
  const HANDLE_KEY = "repo-root";
  const STRUCTURAL_EDGE_KINDS = new Set(["contains"]);
  const DEFAULT_NODE_IDS = ["doc:RUNTIME.md", "doc:runtime/START.md", "doc:INDEX.md"];
  const WORKSPACE_PAGES = [
    {
      id: "browse",
      label: "主巡覽",
      note: "節點清單、地圖與細節。",
    },
    {
      id: "ops",
      label: "診斷與交付",
      note: "健康度、分享輸出與交接摘要。",
    },
    {
      id: "governance",
      label: "維護與治理",
      note: "更新策略、治理解析與報告寫出。",
    },
  ];
  const WORKSPACE_PAGE_IDS = new Set(WORKSPACE_PAGES.map((page) => page.id));

  let DATA = JSON.parse(JSON.stringify(INITIAL_DATA));
  let nodeById = new Map((DATA.nodes || []).map((node) => [node.id, node]));
  const pickDefaultNodeId = (lookup) => DEFAULT_NODE_IDS.find((id) => lookup.has(id)) || DATA.nodes?.[0]?.id || null;
  const state = {
    search: "",
    type: "all",
    diagnosticsFilter: "all",
    mapMode: "grid",
    visualTone: "muted",
    visualTheme: "light",
    textScale: "md",
    updateMode: "manual",
    intervalDays: 1,
    intervalHours: 0,
    intervalMinutes: 0,
    selectedId: pickDefaultNodeId(nodeById),
    repoHandle: null,
    repoHandleName: null,
    refreshInFlight: false,
    refreshTimerId: null,
    lastUpdatedAt: DATA.meta?.generated_at || null,
    lastRefreshDurationMs: null,
    lastRefreshSource: "bootstrap",
    lastRefreshState: "idle",
    lastRefreshMessage: "目前顯示的是最近一次靜態產出的 MAP。",
    browserCanScan: PAGE_MODE === "interactive" && typeof window.showDirectoryPicker === "function" && typeof indexedDB !== "undefined",
    workspacePage: "browse",
    workspaceEngaged: false,
    panelFocus: TEMP_PANEL_AUTO_COMPACT ? "masthead" : "all",
    mastheadCompact: false,
    workspaceCompact: TEMP_PANEL_AUTO_COMPACT,
    autoCollapsedLatch: false,
    mastheadManualOpen: false,
    lastPanelFocusAt: -PANEL_FOCUS_COOLDOWN_MS,
    panelManualFocusUntil: 0,
    mapZoom: 1,
    governanceAnalysisPath: "",
    governanceSourceOverrides: {},
    activeGovernanceLayer: "runtime",
    suppressNextMapClick: false,
    lastMapLayout: null,
    minimapFramePending: false,
    minimapEligible: false,
    minimapDismissed: false,
    tourOpen: false,
    tourStepIndex: 0,
    tourSteps: [],
    tourAutoStarted: false,
    activeTourTarget: null,
  };

  const summaryEl = document.getElementById("summary");
  const mastheadEl = document.querySelector(".masthead");
  const mastheadToggleEl = document.getElementById("masthead-toggle");
  const workspaceShellEl = document.querySelector(".workspace-shell");
  const workspaceToggleEl = document.getElementById("workspace-toggle");
  const sidebarEl = document.getElementById("sidebar");
  const detailEl = document.getElementById("detail");
  const mapEl = document.getElementById("map");
  const mapWrapEl = document.getElementById("map-wrap");
  const mapStageEl = document.getElementById("map-stage");
  const mapMinimapEl = document.getElementById("map-minimap");
  const mapMinimapFrameEl = document.getElementById("map-minimap-frame");
  const mapMinimapViewportEl = document.getElementById("map-minimap-viewport");
  const mapMinimapCopyEl = document.getElementById("map-minimap-copy");
  const mapMinimapToggleEl = document.getElementById("map-minimap-toggle");
  const mapPanLeftEl = document.getElementById("map-pan-left");
  const mapPanRightEl = document.getElementById("map-pan-right");
  const mapPanUpEl = document.getElementById("map-pan-up");
  const mapPanDownEl = document.getElementById("map-pan-down");
  const mapZoomInEl = document.getElementById("map-zoom-in");
  const mapZoomOutEl = document.getElementById("map-zoom-out");
  const mapFitEl = document.getElementById("map-fit");
  const mapResetEl = document.getElementById("map-reset");
  const mapZoomLabelEl = document.getElementById("map-zoom-label");
  const searchEl = document.getElementById("search");
  const typeFilterEl = document.getElementById("type-filter");
  const mapModeEl = document.getElementById("map-mode");
  const visualToneOptionEls = Array.from(document.querySelectorAll("[data-visual-tone-option]"));
  const visualThemeOptionEls = Array.from(document.querySelectorAll("[data-visual-theme-option]"));
  const textScaleOptionEls = Array.from(document.querySelectorAll("[data-text-scale-option]"));
  const visualToneSliderEl = document.querySelector("[data-visual-tone-slider]");
  const visualThemeSliderEl = document.querySelector("[data-visual-theme-slider]");
  const textScaleSliderEl = document.querySelector("[data-text-scale-slider]");
  const updateModeEl = document.getElementById("update-mode");
  const intervalDaysEl = document.getElementById("interval-days");
  const intervalHoursEl = document.getElementById("interval-hours");
  const intervalMinutesEl = document.getElementById("interval-minutes");
  const linkRepoEl = document.getElementById("link-repo");
  const refreshNowEl = document.getElementById("refresh-now");
  const updateStatusEl = document.getElementById("update-status");
  const diagnosticsCardEl = document.getElementById("diagnostics-card");
  const exportCardEl = document.getElementById("export-card");
  const governanceModelEl = document.getElementById("governance-model");
  const governanceEnvironmentEl = document.getElementById("governance-environment");
  const governanceProfileEl = document.getElementById("governance-profile");
  const governanceOutputPathEl = document.getElementById("governance-output-path");
  const governanceResolveEl = document.getElementById("governance-resolve");
  const governanceWriteEl = document.getElementById("governance-write");
  const governanceResultEl = document.getElementById("governance-result");
  const governanceSourceNoteEl = document.getElementById("governance-source-note");
  const governanceAnalysisPathEl = document.getElementById("governance-analysis-path");
  const governanceGlobalPathEl = document.getElementById("governance-global-path");
  const governanceWorkspacePathEl = document.getElementById("governance-workspace-path");
  const governanceRepoPathEl = document.getElementById("governance-repo-path");
  const governanceSourceStatusEl = document.getElementById("governance-source-status");
  const governanceFunnelEl = document.getElementById("governance-funnel");
  const governanceLayerDetailEl = document.getElementById("governance-layer-detail");
  const nodeCountLabelEl = document.getElementById("node-count-label");
  const mapModeNoteEl = document.getElementById("map-mode-note");
  const mapCaptionEl = document.getElementById("map-caption");
  const detailNoteEl = document.getElementById("detail-note");
  const workspaceTabs = Array.from(document.querySelectorAll("[data-workspace-tab]"));
  const workspacePanels = Array.from(document.querySelectorAll("[data-workspace-page-panel]"));
  const workspacePreviewCards = Array.from(document.querySelectorAll("[data-workspace-preview]"));
  const workspacePrevEl = document.getElementById("workspace-prev");
  const workspaceNextEl = document.getElementById("workspace-next");
  const workspacePageNoteEl = document.getElementById("workspace-page-note");
  const tourStartEl = document.getElementById("tour-start");
  const tourCtaCueEl = document.getElementById("tour-cta-cue");
  const tourLayerEl = document.getElementById("tour-layer");
  const tourBackdropEl = document.getElementById("tour-backdrop");
  const tourSpotlightEl = document.getElementById("tour-spotlight");
  const tourCardEl = document.getElementById("tour-card");
  const tourStepLabelEl = document.getElementById("tour-step-label");
  const tourTitleEl = document.getElementById("tour-title");
  const tourBodyEl = document.getElementById("tour-body");
  const tourMetaEl = document.getElementById("tour-meta");
  const tourPrevEl = document.getElementById("tour-prev");
  const tourNextEl = document.getElementById("tour-next");
  const tourSkipEl = document.getElementById("tour-skip");
  const tourCloseEl = document.getElementById("tour-close");

  const cloneData = (data) => JSON.parse(JSON.stringify(data));
  const escapeHtml = (text) => String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
  const cssVar = (name, fallback) => {
    const value = getComputedStyle(document.body).getPropertyValue(name).trim();
    return value || fallback;
  };
  const normalizeLegacyTone = (value) => {
    const normalized = String(value || "").trim();
    if (VISUAL_TONES.has(normalized)) return normalized;
    if (["balanced", "bright", "dense"].includes(normalized)) return "muted";
    return "";
  };
  const normalizeTheme = (value) => {
    const normalized = String(value || "").trim();
    return VISUAL_THEMES.has(normalized) ? normalized : "";
  };
  const normalizeTextScale = (value) => {
    const normalized = String(value || "").trim();
    return TEXT_SCALES.has(normalized) ? normalized : "";
  };
  const visualToneLabel = (tone) => ({
    mono: "結構灰",
    muted: "柔霧色",
    vivid: "高彩度",
  }[tone] || tone);
  const visualThemeLabel = (theme) => ({
    light: "日間",
    dark: "夜間",
  }[theme] || theme);
  const textScaleLabel = (scale) => ({
    xs: "極小",
    sm: "緊湊",
    md: "標準",
    lg: "放大",
    xl: "極大",
  }[scale] || scale);
  const getTypeStylesTheme = () => ({
    doc: {
      fill: cssVar("--type-doc-fill", TYPE_STYLE_FALLBACKS.doc.fill),
      stroke: cssVar("--type-doc-stroke", TYPE_STYLE_FALLBACKS.doc.stroke),
      badge: cssVar("--type-doc-badge", TYPE_STYLE_FALLBACKS.doc.badge),
    },
    directory: {
      fill: cssVar("--type-directory-fill", TYPE_STYLE_FALLBACKS.directory.fill),
      stroke: cssVar("--type-directory-stroke", TYPE_STYLE_FALLBACKS.directory.stroke),
      badge: cssVar("--type-directory-badge", TYPE_STYLE_FALLBACKS.directory.badge),
    },
    runtime: {
      fill: cssVar("--type-runtime-fill", TYPE_STYLE_FALLBACKS.runtime.fill),
      stroke: cssVar("--type-runtime-stroke", TYPE_STYLE_FALLBACKS.runtime.stroke),
      badge: cssVar("--type-runtime-badge", TYPE_STYLE_FALLBACKS.runtime.badge),
    },
    skill: {
      fill: cssVar("--type-skill-fill", TYPE_STYLE_FALLBACKS.skill.fill),
      stroke: cssVar("--type-skill-stroke", TYPE_STYLE_FALLBACKS.skill.stroke),
      badge: cssVar("--type-skill-badge", TYPE_STYLE_FALLBACKS.skill.badge),
    },
    mcp: {
      fill: cssVar("--type-mcp-fill", TYPE_STYLE_FALLBACKS.mcp.fill),
      stroke: cssVar("--type-mcp-stroke", TYPE_STYLE_FALLBACKS.mcp.stroke),
      badge: cssVar("--type-mcp-badge", TYPE_STYLE_FALLBACKS.mcp.badge),
    },
    agent: {
      fill: cssVar("--type-agent-fill", TYPE_STYLE_FALLBACKS.agent.fill),
      stroke: cssVar("--type-agent-stroke", TYPE_STYLE_FALLBACKS.agent.stroke),
      badge: cssVar("--type-agent-badge", TYPE_STYLE_FALLBACKS.agent.badge),
    },
    workflow: {
      fill: cssVar("--type-workflow-fill", TYPE_STYLE_FALLBACKS.workflow.fill),
      stroke: cssVar("--type-workflow-stroke", TYPE_STYLE_FALLBACKS.workflow.stroke),
      badge: cssVar("--type-workflow-badge", TYPE_STYLE_FALLBACKS.workflow.badge),
    },
  });
  const getTextScaleFactor = () => TEXT_SCALE_FACTORS[state.textScale] || TEXT_SCALE_FACTORS.md;
  const formatSvgFontSize = (size) => Number(size * getTextScaleFactor()).toFixed(1).replace(/\.0$/, "");
  async function copyText(text) {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      return true;
    }
    const scratch = document.createElement("textarea");
    scratch.value = text;
    scratch.setAttribute("readonly", "");
    scratch.style.position = "absolute";
    scratch.style.left = "-9999px";
    document.body.appendChild(scratch);
    scratch.select();
    const copied = document.execCommand("copy");
    document.body.removeChild(scratch);
    return copied;
  }

  function syncPanelCompactClasses() {
    if (!mastheadEl || !workspaceShellEl) return;
    if (!TEMP_PANEL_AUTO_COMPACT || state.tourOpen) {
      state.panelFocus = "all";
      state.mastheadCompact = false;
      state.workspaceCompact = false;
      state.autoCollapsedLatch = false;
      state.mastheadManualOpen = true;
      document.body.classList.remove("masthead-compact", "workspace-compact");
      if (mastheadToggleEl) {
        mastheadToggleEl.setAttribute("aria-expanded", "true");
        mastheadToggleEl.textContent = "上方說明已展開";
      }
      if (workspaceToggleEl) {
        workspaceToggleEl.setAttribute("aria-expanded", "true");
        workspaceToggleEl.textContent = "工作區已展開";
      }
      return;
    }
    const tourTargetInMasthead = Boolean(state.tourOpen && state.activeTourTarget && mastheadEl.contains(state.activeTourTarget));
    const tourTargetInWorkspace = Boolean(state.tourOpen && state.activeTourTarget && workspaceShellEl.contains(state.activeTourTarget));
    const activeFocus = tourTargetInMasthead ? "masthead" : tourTargetInWorkspace ? "workspace" : state.panelFocus;
    const shouldCompactMasthead = activeFocus !== "masthead";
    const shouldCompactWorkspace = activeFocus !== "workspace";
    state.mastheadCompact = shouldCompactMasthead;
    state.workspaceCompact = shouldCompactWorkspace;
    state.autoCollapsedLatch = shouldCompactMasthead;
    state.mastheadManualOpen = activeFocus === "masthead";
    document.body.classList.toggle("masthead-compact", shouldCompactMasthead);
    document.body.classList.toggle("workspace-compact", shouldCompactWorkspace);
    if (mastheadToggleEl) {
      mastheadToggleEl.setAttribute("aria-expanded", shouldCompactMasthead ? "false" : "true");
      mastheadToggleEl.textContent = shouldCompactMasthead ? "展開上方說明" : "收合上方說明";
    }
    if (workspaceToggleEl) {
      workspaceToggleEl.setAttribute("aria-expanded", shouldCompactWorkspace ? "false" : "true");
      workspaceToggleEl.textContent = shouldCompactWorkspace ? "展開工作區" : "縮小工作區";
    }
  }

  function requestPanelFocus(nextFocus, { force = false, manual = false } = {}) {
    if (!TEMP_PANEL_AUTO_COMPACT || state.tourOpen) {
      syncPanelCompactClasses();
      return false;
    }
    if (!["masthead", "workspace"].includes(nextFocus)) return false;
    if (state.panelFocus === nextFocus) {
      syncPanelCompactClasses();
      return true;
    }
    const now = performance.now();
    if (!force && now - state.lastPanelFocusAt < PANEL_FOCUS_COOLDOWN_MS) {
      return false;
    }
    state.panelFocus = nextFocus;
    state.lastPanelFocusAt = now;
    if (manual) {
      state.panelManualFocusUntil = now + PANEL_FOCUS_COOLDOWN_MS;
    }
    syncPanelCompactClasses();
    return true;
  }

  function inferPanelFocusFromViewport() {
    const workspaceTop = workspaceShellEl.getBoundingClientRect().top;
    const mapMoved = Boolean(mapWrapEl && (mapWrapEl.scrollLeft > 12 || mapWrapEl.scrollTop > 12));
    if (!state.autoCollapsedLatch && window.scrollY < 8 && workspaceTop > 148 && (!mapWrapEl || (mapWrapEl.scrollLeft <= 12 && mapWrapEl.scrollTop <= 12))) {
      state.workspaceEngaged = false;
    }
    if (window.scrollY < 8 && !state.workspaceEngaged) {
      return "masthead";
    }
    if (state.workspaceEngaged || window.scrollY > 24 || workspaceTop <= window.innerHeight * 0.62 || mapMoved) {
      return "workspace";
    }
    return "masthead";
  }

  function syncMastheadCompactState({ force = false } = {}) {
    if (!mastheadEl || !workspaceShellEl) return;
    if (!TEMP_PANEL_AUTO_COMPACT || state.tourOpen) {
      syncPanelCompactClasses();
      return;
    }
    if (!force && performance.now() < state.panelManualFocusUntil) {
      syncPanelCompactClasses();
      return;
    }
    requestPanelFocus(inferPanelFocusFromViewport(), { force });
  }

  function toggleMastheadCompact() {
    requestPanelFocus(state.panelFocus === "masthead" ? "workspace" : "masthead", { manual: true });
  }

  function toggleWorkspaceCompact() {
    requestPanelFocus(state.panelFocus === "workspace" ? "masthead" : "workspace", { manual: true });
  }

  function getMinimapMetrics() {
    if (!mapWrapEl || !mapMinimapFrameEl) return null;
    const contentWidth = Math.max(mapWrapEl.scrollWidth, state.lastMapLayout?.width || 0);
    const contentHeight = Math.max(mapWrapEl.scrollHeight, state.lastMapLayout?.height || 0);
    const frameWidth = mapMinimapFrameEl.clientWidth;
    const frameHeight = mapMinimapFrameEl.clientHeight;
    if (!contentWidth || !contentHeight || !frameWidth || !frameHeight) return null;

    const widthRatio = contentWidth / Math.max(mapWrapEl.clientWidth, 1);
    const heightRatio = contentHeight / Math.max(mapWrapEl.clientHeight, 1);
    const scale = Math.min(frameWidth / contentWidth, frameHeight / contentHeight);
    const renderedWidth = contentWidth * scale;
    const renderedHeight = contentHeight * scale;
    const offsetX = (frameWidth - renderedWidth) / 2;
    const offsetY = (frameHeight - renderedHeight) / 2;
    return {
      contentWidth,
      contentHeight,
      frameWidth,
      frameHeight,
      widthRatio,
      heightRatio,
      scale,
      renderedWidth,
      renderedHeight,
      offsetX,
      offsetY,
    };
  }

  function syncMinimapVisibility(metrics = getMinimapMetrics()) {
    if (!mapStageEl || !mapMinimapToggleEl || !mapMinimapFrameEl || !metrics) return;
    const eligible = metrics.heightRatio > 2;
    state.minimapEligible = eligible;
    mapStageEl.classList.toggle("minimap-eligible", eligible);
    mapStageEl.classList.toggle("minimap-hidden", eligible && state.minimapDismissed);
    mapMinimapToggleEl.hidden = !eligible;
    if (!eligible) {
      mapMinimapToggleEl.disabled = true;
      mapMinimapToggleEl.textContent = "縮圖未啟用";
      mapMinimapToggleEl.setAttribute("aria-pressed", "false");
      mapMinimapFrameEl.tabIndex = -1;
      if (mapMinimapCopyEl) {
        mapMinimapCopyEl.textContent = "只有圖面高度相對目前視窗超過 2 倍時，才會顯示縮圖導覽。";
      }
      return;
    }
    mapMinimapToggleEl.disabled = false;
    mapMinimapToggleEl.textContent = state.minimapDismissed ? "顯示縮圖" : "隱藏縮圖";
    mapMinimapToggleEl.setAttribute("aria-pressed", state.minimapDismissed ? "false" : "true");
    mapMinimapFrameEl.tabIndex = state.minimapDismissed ? -1 : 0;
  }

  function updateMinimapViewport() {
    if (!mapWrapEl || !mapMinimapFrameEl || !mapMinimapViewportEl) return;
    const metrics = getMinimapMetrics();
    if (!metrics) return;
    syncMinimapVisibility(metrics);
    if (!state.minimapEligible || state.minimapDismissed) return;

    const viewportWidth = Math.max(14, mapWrapEl.clientWidth * metrics.scale);
    const viewportHeight = Math.max(12, mapWrapEl.clientHeight * metrics.scale);
    const maxLeft = Math.max(metrics.offsetX, metrics.offsetX + metrics.renderedWidth - viewportWidth);
    const maxTop = Math.max(metrics.offsetY, metrics.offsetY + metrics.renderedHeight - viewportHeight);
    const left = clamp(metrics.offsetX + (mapWrapEl.scrollLeft * metrics.scale), metrics.offsetX, maxLeft);
    const top = clamp(metrics.offsetY + (mapWrapEl.scrollTop * metrics.scale), metrics.offsetY, maxTop);

    mapMinimapViewportEl.style.width = `${viewportWidth}px`;
    mapMinimapViewportEl.style.height = `${viewportHeight}px`;
    mapMinimapViewportEl.style.left = `${left}px`;
    mapMinimapViewportEl.style.top = `${top}px`;

    if (mapMinimapCopyEl) {
      const horizontalCenter = Math.round(((mapWrapEl.scrollLeft + (mapWrapEl.clientWidth / 2)) / metrics.contentWidth) * 100);
      const verticalCenter = Math.round(((mapWrapEl.scrollTop + (mapWrapEl.clientHeight / 2)) / metrics.contentHeight) * 100);
      mapMinimapCopyEl.textContent = `維持等比例縮小；只在圖面高度超過目前視窗 2 倍時顯示。現在焦點約在寬度 ${horizontalCenter}% / 高度 ${verticalCenter}% 。`;
    }
  }

  function scheduleMinimapViewportUpdate() {
    if (state.minimapFramePending) return;
    state.minimapFramePending = true;
    requestAnimationFrame(() => {
      state.minimapFramePending = false;
      updateMinimapViewport();
      syncMastheadCompactState();
    });
  }

  function jumpMapViewportFromMinimap(clientX, clientY) {
    if (!mapWrapEl || !mapMinimapFrameEl) return;
    const rect = mapMinimapFrameEl.getBoundingClientRect();
    const metrics = getMinimapMetrics();
    if (!metrics || !state.minimapEligible || state.minimapDismissed) return;
    const ratioX = clamp((clientX - rect.left - metrics.offsetX) / Math.max(metrics.renderedWidth, 1), 0, 1);
    const ratioY = clamp((clientY - rect.top - metrics.offsetY) / Math.max(metrics.renderedHeight, 1), 0, 1);
    const targetLeft = clamp((ratioX * metrics.contentWidth) - (mapWrapEl.clientWidth / 2), 0, Math.max(0, metrics.contentWidth - mapWrapEl.clientWidth));
    const targetTop = clamp((ratioY * metrics.contentHeight) - (mapWrapEl.clientHeight / 2), 0, Math.max(0, metrics.contentHeight - mapWrapEl.clientHeight));
    mapWrapEl.scrollTo({
      left: targetLeft,
      top: targetTop,
      behavior: "smooth",
    });
    scheduleMinimapViewportUpdate();
  }

  function toggleMinimapVisibility() {
    if (!state.minimapEligible) return;
    state.minimapDismissed = !state.minimapDismissed;
    syncMinimapVisibility();
    if (!state.minimapDismissed) {
      scheduleMinimapViewportUpdate();
      mapMinimapFrameEl?.focus();
    }
  }

  function getWorkspacePage(pageId = state.workspacePage) {
    return WORKSPACE_PAGES.find((page) => page.id === pageId) || WORKSPACE_PAGES[0];
  }

  function syncWorkspacePages() {
    const activePage = getWorkspacePage();
    const activeIndex = WORKSPACE_PAGES.findIndex((page) => page.id === activePage.id);
    workspaceTabs.forEach((button) => {
      const isActive = button.dataset.workspaceTab === activePage.id;
      button.classList.toggle("active", isActive);
      button.setAttribute("aria-selected", isActive ? "true" : "false");
      button.tabIndex = isActive ? 0 : -1;
    });
    workspacePanels.forEach((panel) => {
      panel.hidden = panel.dataset.workspacePagePanel !== activePage.id;
    });
    workspacePreviewCards.forEach((card) => {
      card.classList.toggle("active", card.dataset.workspacePreview === activePage.id);
    });
    if (workspacePageNoteEl) {
      workspacePageNoteEl.textContent = `目前聚焦：${activePage.label}。${activePage.note}`;
    }
    if (workspacePrevEl) workspacePrevEl.disabled = activeIndex <= 0;
    if (workspaceNextEl) workspaceNextEl.disabled = activeIndex >= WORKSPACE_PAGES.length - 1;
  }

  function setWorkspacePage(pageId, options = {}) {
    if (!WORKSPACE_PAGE_IDS.has(pageId)) return;
    const changed = state.workspacePage !== pageId;
    state.workspacePage = pageId;
    syncWorkspacePages();
    if ((changed || options.forceSync) && options.persist !== false) {
      saveSettings();
    }
    if (changed && state.tourOpen && options.updateTour !== false) {
      requestAnimationFrame(() => updateTourLayout());
    }
    scheduleMinimapViewportUpdate();
    syncMastheadCompactState();
  }

  function moveWorkspacePage(delta) {
    const currentIndex = WORKSPACE_PAGES.findIndex((page) => page.id === state.workspacePage);
    const nextPage = WORKSPACE_PAGES[currentIndex + delta];
    if (!nextPage) return;
    setWorkspacePage(nextPage.id);
  }

  function hasSeenTour() {
    try {
      return localStorage.getItem(TOUR_STORAGE_KEY) === "seen";
    } catch {
      return false;
    }
  }

  function markTourSeen() {
    try {
      localStorage.setItem(TOUR_STORAGE_KEY, "seen");
    } catch {
      // Ignore storage failures and keep the tour manually accessible.
    }
    document.body.classList.remove("tour-entry-cue");
    if (tourCtaCueEl) tourCtaCueEl.hidden = true;
    if (tourStartEl) tourStartEl.textContent = "重新導覽";
  }

  function syncTourEntryCue() {
    const shouldPrompt = TEMP_TOUR_ENTRY_CUE && !hasSeenTour() && !state.tourOpen;
    document.body.classList.toggle("tour-entry-cue", shouldPrompt);
    if (tourCtaCueEl) tourCtaCueEl.hidden = !shouldPrompt;
    if (tourStartEl) tourStartEl.textContent = hasSeenTour() ? "重新導覽" : "開始導覽";
  }

  function isElementVisible(element) {
    if (!element) return false;
    if (!element.getClientRects().length) return false;
    const style = window.getComputedStyle(element);
    return style.display !== "none" && style.visibility !== "hidden";
  }

  function getTourSteps() {
    const baseSteps = [
      {
        id: "operation-focus",
        selector: ".masthead-aside",
        page: "browse",
        title: "操作重點",
        body: [
          "`runtime/*` 顯示目前執行面投影，`registry/*` 保留正式來源定義。",
          "依序檢查現行投影、來源對應、診斷狀態與交接輸出。",
        ],
        meta: ["導覽模式會保持上方說明與工作區同時展開。"],
      },
      {
        id: "search",
        selector: "#search",
        page: "browse",
        title: "搜尋節點",
        body: [
          "搜尋會同時比對節點名稱、描述與路徑。你可以直接打 `runtime/skills`、`catalog`、`governance` 這類關鍵詞。",
          "只知道執行面名稱時，先搜尋 `runtime/*`，再沿著對應關係回查來源。",
        ],
        meta: ["適用於交接、排錯，以及比對技能、代理、流程是否已投影到執行面。"],
      },
      {
        id: "primary-controls",
        selector: ".control-band.primary",
        page: "browse",
        title: "篩選與視角",
        body: [
          "類型篩選可以把視野先縮成執行面、技能註冊、文件等單一層面。",
          "地圖視角決定你是用欄式閱讀結構，還是用圓形閱讀關聯。欄式適合盤點，圓形適合追單點關係。",
        ],
        meta: ["先看執行面，再加回註冊類型，可檢查投影結果與正式來源是否一致。"],
      },
      {
        id: "sidebar",
        selector: "#sidebar",
        page: "browse",
        title: "節點清單",
        body: [
          "這裡會列出目前符合搜尋與篩選條件的節點，適合快速切換檢查不同的執行面投影或核心文件。",
          "清單與地圖是同步的，從左欄進入通常比直接在地圖上找點更快。",
        ],
        meta: ["當節點很多時，先從左欄選定一個起點，再讓中間地圖與右欄細節跟著聚焦。"],
      },
      {
        id: "map",
        selector: "#map-wrap",
        page: "browse",
        title: "關聯地圖",
        body: [
          "地圖會把 `contains`、`catalog_entry`、`maps_to`、`references` 這些關係畫出來，讓你知道執行面節點是從哪裡投影而來。",
          "它是資源拓樸，不是文件目錄；重點在追查節點之間的關係。",
        ],
        meta: ["若你想確認某個執行面技能是否真的對回正式來源，請特別看「正式來源對應」與「目錄對應」這兩種邊。"],
      },
      {
        id: "detail",
        selector: "#detail",
        page: "browse",
        title: "節點細節",
        body: [
          "選到任何節點後，右欄會顯示描述、路徑、來源與相關邊。",
          "如果你要寫報告或交接，先在這裡確認路徑、類型、連結對象都合理，再輸出內容。",
        ],
        meta: ["輸出交接前，先確認路徑、類型與連結對象。"],
      },
      {
        id: "operations",
        selector: ".operations-grid",
        page: "ops",
        title: "診斷與交付",
        body: [
          "診斷檢查會提示目前地圖是否有缺漏、漂移或結構異常。交付輸出提供分享頁與交接摘要。",
          "日常巡覽時先看診斷檢查，有明顯落差再回去查 `runtime/*` 與 `registry/*` 的對映。",
        ],
        meta: ["診斷數字可判斷目前地圖是否適合作為交接依據。"],
      },
      {
        id: "maintenance",
        selector: "#maintenance-controls",
        page: "governance",
        title: "維護控制",
        body: [
          "維護控制只在互動版顯示。這裡可以連結本機專案目錄、設定自動更新模式，或立即重新掃描目前工作樹。",
          "修改 `runtime/catalog.json`、`registry/*` 文件或治理檔案後，可從這裡重新同步資料。",
        ],
        meta: ["重掃只更新目前瀏覽器資料；交付前仍需重新生成靜態輸出。"],
      },
      {
        id: "governance",
        selector: ".governance-panel",
        page: "governance",
        title: "治理解析",
        body: [
          "治理層疊解析會依目前模型、環境與設定組合出實際生效的治理結果，並能把結果寫回專案目錄內指定位置。",
          "用於交接控制台、確認指令層疊，或追查規則來源層級。",
        ],
        meta: ["解析結果可寫回專案目錄內指定位置。"],
      },
    ];

    return baseSteps.filter((step) => {
      if (step.id === "maintenance" && PAGE_MODE !== "interactive") return false;
      return Boolean(document.querySelector(step.selector));
    });
  }

  function clearTourTargetHighlight() {
    if (!state.activeTourTarget) return;
    state.activeTourTarget.classList.remove("tour-target-active");
    state.activeTourTarget = null;
  }

  function getCurrentTourStep() {
    return state.tourSteps[state.tourStepIndex] || null;
  }

  function shouldUseStackedTourLayout(targetRect) {
    if (!targetRect) return window.innerWidth <= 980;
    const viewportRatio = window.innerWidth / Math.max(window.innerHeight, 1);
    const estimatedFloatingWidth = clamp(Math.min(380, window.innerWidth - 32), 280, window.innerWidth - 24);
    const sideRoom = Math.max(targetRect.left - 24, window.innerWidth - targetRect.right - 24);
    if (window.innerWidth <= 980) return true;
    if (viewportRatio < 1.16) return true;
    if (sideRoom < estimatedFloatingWidth && window.innerWidth < 1280) return true;
    return false;
  }

  function updateTourLayout({ scrollTarget = false } = {}) {
    if (!state.tourOpen || !tourCardEl || !tourSpotlightEl || !tourLayerEl) return;
    const step = getCurrentTourStep();
    if (step?.page) {
      setWorkspacePage(step.page, { persist: false, updateTour: false });
    }
    const target = step ? document.querySelector(step.selector) : null;
    if (!step || !isElementVisible(target)) {
      finishTour({ markSeen: false });
      return;
    }

    clearTourTargetHighlight();
    state.activeTourTarget = target;
    target.classList.add("tour-target-active");
    syncMastheadCompactState();
    const initialRect = target.getBoundingClientRect();
    const useStackedLayout = shouldUseStackedTourLayout(initialRect);
    if (scrollTarget) {
      target.scrollIntoView({
        behavior: "smooth",
        block: useStackedLayout ? "start" : "center",
        inline: "nearest",
      });
    }

    const rect = target.getBoundingClientRect();
    const layoutMode = shouldUseStackedTourLayout(rect) ? "stacked" : "floating";
    tourLayerEl.dataset.layout = layoutMode;

    const floatingWidth = clamp(Math.min(380, window.innerWidth - 32), 280, window.innerWidth - 24);
    const stackedWidth = clamp(Math.min(680, window.innerWidth - 24), 300, window.innerWidth - 20);
    const cardWidth = layoutMode === "stacked" ? stackedWidth : floatingWidth;
    tourCardEl.style.width = `${cardWidth}px`;
    tourCardEl.style.maxHeight = layoutMode === "stacked"
      ? `${Math.max(240, Math.min(window.innerHeight - 20, Math.round(window.innerHeight * 0.52)))}px`
      : `${Math.max(240, window.innerHeight - 32)}px`;
    const cardRect = tourCardEl.getBoundingClientRect();

    const pad = 14;
    let cardLeft = 16;
    let cardTop = 16;
    let spotlightBottomLimit = window.innerHeight - 10;

    if (layoutMode === "stacked") {
      cardLeft = clamp((window.innerWidth - cardRect.width) / 2, 10, window.innerWidth - cardRect.width - 10);
      cardTop = Math.max(10, window.innerHeight - cardRect.height - 10);
      spotlightBottomLimit = Math.max(96, cardTop - 16);
    } else {
      cardLeft = rect.right + 24;
      if (cardLeft + cardRect.width > window.innerWidth - 16) {
        cardLeft = rect.left - cardRect.width - 24;
      }
      if (cardLeft < 16) {
        cardLeft = clamp(rect.left, 16, window.innerWidth - cardRect.width - 16);
      }

      cardTop = rect.top;
      if (cardTop + cardRect.height > window.innerHeight - 16) {
        cardTop = window.innerHeight - cardRect.height - 16;
      }
      if (cardTop < 16) {
        cardTop = 16;
      }
    }

    const spotlightLeft = clamp(rect.left - pad, 10, window.innerWidth - 10);
    const spotlightTop = clamp(rect.top - pad, 10, Math.max(10, spotlightBottomLimit - 72));
    const spotlightWidth = clamp(rect.width + pad * 2, 140, window.innerWidth - spotlightLeft - 10);
    const spotlightHeight = clamp(rect.height + pad * 2, 72, Math.max(72, spotlightBottomLimit - spotlightTop));

    tourSpotlightEl.style.left = `${spotlightLeft}px`;
    tourSpotlightEl.style.top = `${spotlightTop}px`;
    tourSpotlightEl.style.width = `${spotlightWidth}px`;
    tourSpotlightEl.style.height = `${spotlightHeight}px`;
    tourCardEl.style.left = `${cardLeft}px`;
    tourCardEl.style.top = `${cardTop}px`;
  }

  function renderTourStep(options = {}) {
    if (!state.tourOpen || !tourLayerEl || !tourCardEl) return;
    const step = getCurrentTourStep();
    if (!step) {
      finishTour({ markSeen: false });
      return;
    }
    if (step.page) {
      setWorkspacePage(step.page, { persist: false, updateTour: false });
    }

    tourLayerEl.hidden = false;
    tourLayerEl.setAttribute("aria-hidden", "false");
    tourStepLabelEl.textContent = `第 ${state.tourStepIndex + 1} 步 / 共 ${state.tourSteps.length} 步`;
    tourTitleEl.textContent = step.title;
    tourBodyEl.innerHTML = step.body.map((line) => `<p>${escapeHtml(line.trim())}</p>`).join("");
    tourMetaEl.innerHTML = step.meta.map((line) => `<p>${escapeHtml(line.trim())}</p>`).join("");
    tourPrevEl.disabled = state.tourStepIndex === 0;
    tourNextEl.textContent = state.tourStepIndex === state.tourSteps.length - 1 ? "完成導覽" : "下一步";
    tourCardEl.scrollTop = 0;
    requestAnimationFrame(() => updateTourLayout(options));
  }

  function startTour(startStepId = null) {
    if (!tourLayerEl || !tourCardEl) return;
    state.tourSteps = getTourSteps();
    if (!state.tourSteps.length) return;
    const preferredIndex = startStepId ? state.tourSteps.findIndex((step) => step.id === startStepId) : 0;
    state.tourStepIndex = preferredIndex >= 0 ? preferredIndex : 0;
    state.tourOpen = true;
    document.body.classList.remove("tour-entry-cue");
    if (tourCtaCueEl) tourCtaCueEl.hidden = true;
    document.body.classList.add("tour-active");
    const initialStep = getCurrentTourStep();
    if (initialStep?.page) {
      setWorkspacePage(initialStep.page, { persist: false, updateTour: false });
    }
    renderTourStep({ scrollTarget: true });
  }

  function finishTour({ markSeen = true } = {}) {
    if (!tourLayerEl) return;
    clearTourTargetHighlight();
    state.tourOpen = false;
    state.tourSteps = [];
    state.tourStepIndex = 0;
    tourLayerEl.hidden = true;
    tourLayerEl.setAttribute("aria-hidden", "true");
    delete tourLayerEl.dataset.layout;
    document.body.classList.remove("tour-active");
    syncMastheadCompactState();
    if (markSeen) markTourSeen();
    else syncTourEntryCue();
  }

  function moveTour(delta) {
    if (!state.tourOpen) return;
    const nextIndex = state.tourStepIndex + delta;
    if (nextIndex < 0) return;
    if (nextIndex >= state.tourSteps.length) {
      finishTour();
      return;
    }
    state.tourStepIndex = nextIndex;
    renderTourStep({ scrollTarget: true });
  }

  function maybeStartTourOnFirstVisit() {
    if (hasSeenTour() || state.tourAutoStarted) {
      syncTourEntryCue();
      return;
    }
    state.tourAutoStarted = true;
    window.setTimeout(() => {
      syncTourEntryCue();
    }, 720);
  }

  function handleTourKeydown(event) {
    if (!state.tourOpen) return;
    if (event.key === "Escape") {
      event.preventDefault();
      finishTour();
      return;
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      moveTour(1);
      return;
    }
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      moveTour(-1);
    }
  }

  window.addEventListener("resize", () => {
    if (state.tourOpen) updateTourLayout();
    scheduleMinimapViewportUpdate();
    syncMastheadCompactState();
  }, { passive: true });
  window.addEventListener("scroll", () => {
    if (state.tourOpen) updateTourLayout();
    syncMastheadCompactState();
  }, { passive: true, capture: true });
  window.addEventListener("wheel", (event) => {
    if (Math.abs(event.deltaY) < 12) return;
    if (event.deltaY > 0) {
      requestPanelFocus("workspace");
      return;
    }
    if (window.scrollY < 180) {
      requestPanelFocus("masthead");
    }
  }, { passive: true });
  document.addEventListener("keydown", handleTourKeydown);

  function normalizeWindowsPath(pathText) {
    return String(pathText || "").trim().replaceAll("/", "\\").replace(/\\+$/, "");
  }

  function lowerComparablePath(pathText) {
    return normalizeWindowsPath(pathText).toLowerCase();
  }

  function isPathWithin(childPath, parentPath) {
    const child = lowerComparablePath(childPath);
    const parent = lowerComparablePath(parentPath);
    return Boolean(child && parent && (child === parent || child.startsWith(`${parent}\\`)));
  }

  function formatRepoRelativePath(pathText) {
    const normalizedPath = normalizeWindowsPath(pathText);
    const repoRoot = normalizeWindowsPath(DATA.meta?.repo_root_native || "");
    if (repoRoot && normalizedPath.startsWith(`${repoRoot}\\`)) {
      return normalizedPath.slice(repoRoot.length + 1);
    }
    return normalizedPath;
  }

  function defaultGovernanceOutputPath() {
    const repoRoot = DATA.meta?.repo_root_native || "";
    return repoRoot ? `${normalizeWindowsPath(repoRoot)}\\ops\\agent-governance` : "ops\\agent-governance";
  }

  function getGovernanceSources() {
    return DATA.governance?.sources || [];
  }

  function getSourceByScope(scope) {
    return getGovernanceSources().find((source) => source.scope === scope) || null;
  }

  function setGovernanceInputDefaults() {
    if (governanceAnalysisPathEl && !governanceAnalysisPathEl.value) {
      governanceAnalysisPathEl.value = state.governanceAnalysisPath || DATA.governance?.analysis_path || DATA.meta?.repo_root_native || "";
    }
    const pathInputs = {
      "global-home": governanceGlobalPathEl,
      workspace: governanceWorkspacePathEl,
      repo: governanceRepoPathEl,
    };
    Object.entries(pathInputs).forEach(([scope, inputEl]) => {
      if (!inputEl || inputEl.value) return;
      const source = getSourceByScope(scope);
      inputEl.value = state.governanceSourceOverrides[scope] || source?.suggested_path || source?.path || "";
    });
  }

  function rememberGovernanceSettings() {
    state.governanceAnalysisPath = governanceAnalysisPathEl?.value?.trim() || "";
    state.governanceSourceOverrides = {
      "global-home": governanceGlobalPathEl?.value?.trim() || "",
      workspace: governanceWorkspacePathEl?.value?.trim() || "",
      repo: governanceRepoPathEl?.value?.trim() || "",
    };
    saveSettings();
    const resolution = resolveGovernanceInPage();
    renderGovernanceResolution(resolution, "已更新治理設定。");
  }

  function classifyGovernanceAnalysisPath(pathText) {
    const analysisPath = normalizeWindowsPath(pathText || DATA.governance?.analysis_path || DATA.meta?.repo_root_native || "");
    const repoRoot = normalizeWindowsPath(DATA.meta?.repo_root_native || "");
    const workspaceSource = getSourceByScope("workspace");
    const workspaceRoot = normalizeWindowsPath((workspaceSource?.path || "").replace(/\\AGENTS\.md$/i, ""));
    if (!analysisPath) {
      return { path: "", scope_hint: "unknown", note: "尚未指定任意操作路徑。", verified: false, unverified_path_classification: true };
    }
    if (repoRoot && isPathWithin(analysisPath, repoRoot)) {
      return { path: analysisPath, scope_hint: "repo", note: "路徑落在目前 repo 內，global-home、workspace、repo-local 皆可作為檔案治理候選。", verified: false, unverified_path_classification: true };
    }
    if (workspaceRoot && isPathWithin(analysisPath, workspaceRoot)) {
      return { path: analysisPath, scope_hint: "workspace", note: "路徑落在工作區層級但不一定落在目前 repo 內；repo-local 規則只作為 evidence，不推定適用。", verified: false, unverified_path_classification: true };
    }
    return { path: analysisPath, scope_hint: "external", note: "路徑不在目前 repo/workspace 判定範圍內，只能保留 global-home 與手動來源路徑作為可檢查候選。", verified: false, unverified_path_classification: true };
  }

  function sourceAppliesToPath(source, pathClassification) {
    if (!source) return false;
    if (source.scope === "global-home") return true;
    if (!pathClassification?.path) return Boolean(source.applies_to_path);
    if (source.scope === "repo") return pathClassification.scope_hint === "repo";
    if (source.scope === "workspace") return pathClassification.scope_hint === "repo" || pathClassification.scope_hint === "workspace";
    return Boolean(source.applies_to_path);
  }

  function getConfiguredGovernanceSources(pathClassification = classifyGovernanceAnalysisPath(state.governanceAnalysisPath)) {
    return getGovernanceSources().map((source) => {
      const manualPath = state.governanceSourceOverrides[source.scope] || "";
      const configuredPath = normalizeWindowsPath(manualPath || source.path || source.suggested_path || "");
      const manualExternal = Boolean(manualPath && configuredPath !== normalizeWindowsPath(source.path || ""));
      const applies = sourceAppliesToPath(source, pathClassification);
      return {
        ...source,
        path: configuredPath,
        manual_path: manualPath,
        source_kind: manualExternal ? "manual-path" : source.source_kind,
        readable: manualExternal ? false : Boolean(source.readable),
        inspectable: manualExternal ? false : Boolean(source.inspectable),
        handle_bound: manualExternal ? false : Boolean(source.handle_bound),
        permission_state: manualExternal ? "manual-path-only" : source.permission_state,
        applies_to_path: applies,
        evidence_only: !applies,
        unresolved_reason: manualExternal
          ? "手動外部路徑只記錄指向；靜態輸出不讀取專案外內容。"
          : source.unresolved_reason,
      };
    });
  }

  function collectGovernanceOptions() {
    const policyLayers = window.AGENT_GOVERNANCE_POLICY?.layers || [];
    const valuesByKey = {
      models: [],
      environments: [],
      instruction_profiles: [],
    };
    const seenByKey = {
      models: new Set(),
      environments: new Set(),
      instruction_profiles: new Set(),
    };
    policyLayers.forEach((layer) => {
      const match = layer.match || {};
      Object.keys(valuesByKey).forEach((key) => {
        if (!Array.isArray(match[key])) return;
        match[key].forEach((value) => {
          const normalizedValue = String(value || "").trim();
          if (!normalizedValue || seenByKey[key].has(normalizedValue)) return;
          seenByKey[key].add(normalizedValue);
          valuesByKey[key].push(normalizedValue);
        });
      });
    });
    return valuesByKey;
  }

  function populateGovernanceSelect(selectEl, options, fallbackValue) {
    if (!selectEl) return;
    const currentValue = String(selectEl.value || fallbackValue || "").trim();
    const normalizedFallback = String(fallbackValue || "").trim();
    const normalizedOptions = Array.from(new Set(
      (Array.isArray(options) ? options : [])
        .map((value) => String(value || "").trim())
        .filter(Boolean),
    ));
    if (normalizedFallback && !normalizedOptions.includes(normalizedFallback)) {
      normalizedOptions.unshift(normalizedFallback);
    }
    if (!normalizedOptions.length) return;

    selectEl.innerHTML = "";
    normalizedOptions.forEach((value) => {
      const optionEl = document.createElement("option");
      optionEl.value = value;
      optionEl.textContent = value;
      selectEl.appendChild(optionEl);
    });

    const nextValue = normalizedOptions.includes(currentValue) ? currentValue : normalizedOptions[0];
    selectEl.value = nextValue;
  }

  function initializeGovernanceSelectors() {
    const { models, environments, instruction_profiles: instructionProfiles } = collectGovernanceOptions();
    populateGovernanceSelect(governanceModelEl, models, "gpt-5.4");
    populateGovernanceSelect(governanceEnvironmentEl, environments, "codex-local-dev");
    populateGovernanceSelect(governanceProfileEl, instructionProfiles, "mapping");
  }

  function resolveGovernanceInPage() {
    const policyLayers = window.AGENT_GOVERNANCE_POLICY?.layers || [];
    const precedence = window.AGENT_GOVERNANCE_POLICY?.meta?.precedence || ["base", "model", "environment", "instruction_profile"];
    const inputs = {
      model: governanceModelEl?.value?.trim() || "gpt-5.4",
      environment: governanceEnvironmentEl?.value?.trim() || "codex-local-dev",
        instruction_profile: governanceProfileEl?.value?.trim() || "mapping",
      };
    const pathClassification = classifyGovernanceAnalysisPath(state.governanceAnalysisPath || governanceAnalysisPathEl?.value || "");
    const agentsSources = getConfiguredGovernanceSources(pathClassification);
    const sourcesByScope = new Map(agentsSources.map((source) => [source.scope, source]));
    const matchesLayer = (layer) => {
      const match = layer.match || {};
      if (Array.isArray(match.models) && !match.models.includes(inputs.model)) return false;
      if (Array.isArray(match.environments) && !match.environments.includes(inputs.environment)) return false;
      if (Array.isArray(match.instruction_profiles) && !match.instruction_profiles.includes(inputs.instruction_profile)) return false;
      return true;
    };
    const matchedLayers = [];
    precedence.forEach((scope) => {
      policyLayers.forEach((layer) => {
        if (layer.scope === scope && matchesLayer(layer)) matchedLayers.push(layer);
      });
    });
    const effectiveConfig = {};
    const provenance = {};
    matchedLayers.forEach((layer) => {
      Object.entries(layer.config || {}).forEach(([key, value]) => {
        effectiveConfig[key] = value;
        provenance[key] = { value, source_layer: layer.id, scope: layer.scope };
      });
    });
    const effectiveFileRules = (DATA.governance?.effective_file_rules || []).map((item) => {
      const source = sourcesByScope.get(item.scope);
      const sourceMatches = source
        ? normalizeWindowsPath(source.path || "") === normalizeWindowsPath(item.source_path || "") && Boolean(source.inspectable)
        : true;
      const applies = Boolean(source?.applies_to_path) && sourceMatches;
      const unresolvedReason = sourceMatches
        ? item.unresolved_reason
        : "Configured source is manual, unreadable, or path-mismatched; bundled rules are stale evidence only.";
      return { ...item, effective: applies, evidence_only: !applies, unresolved_reason: unresolvedReason };
    });
    const effectiveHardRules = effectiveFileRules.filter((item) => item.effective && item.rule_category !== "operational_guidance");
    const operationalGuidance = effectiveFileRules.filter((item) => item.effective && item.rule_category === "operational_guidance");
    return {
      generated_at: new Date().toISOString(),
      inputs,
      analysis_path: pathClassification.path,
      path_classification: pathClassification,
      policy_meta: window.AGENT_GOVERNANCE_POLICY?.meta || {},
      matched_layers: matchedLayers.map((layer) => ({
        id: layer.id,
        scope: layer.scope,
        description: layer.description,
        config: layer.config || {},
      })),
      effective_config: effectiveConfig,
      provenance,
      agents_hierarchy_note: DATA.governance?.hierarchy_note || "",
      agents_sources: agentsSources,
      effective_file_rules: effectiveFileRules,
      effective_hard_rules: effectiveHardRules,
      operational_guidance: operationalGuidance,
      instruction_evaluation: [
        "來自 runtime、system、developer 與全域家目錄的指令仍屬於更高優先層級，靜態輸出只呈現檔案層級證據。",
        "檔案層級優先採用結構化治理規則檔；缺少結構化來源時，才退回工作區與 repo-local AGENTS 的文字解析。",
        `目前納入檔案層級檢查的來源數量：${agentsSources.filter((source) => source.applies_to_path).length}`,
      ],
    };
  }

  function formatGovernanceSourceLine(source) {
    const definitionSuffix = source.definition_path ? `（規則檔：${source.definition_path}）` : "";
    const modeSuffix = source.evidence_only ? "（不適用目前路徑，僅作證據）" : "";
    const permissionSuffix = source.permission_state ? `；${source.permission_state}` : "";
    return `- [${source.scope}] ${source.path}${definitionSuffix}${modeSuffix}${permissionSuffix}`;
  }

  function renderGovernanceSourceStatus(resolution) {
    if (!governanceSourceStatusEl) return;
    const sources = resolution.agents_sources || [];
    governanceSourceStatusEl.innerHTML = sources.map((source) => {
      const appliesText = source.applies_to_path ? "適用目前路徑" : "不適用目前路徑，僅保留為 evidence";
      const inspectText = source.inspectable ? "內容已納入解析" : "未讀取內容";
      const reason = source.unresolved_reason ? `<span>${escapeHtml(source.unresolved_reason)}</span>` : "";
      return [
        `<article class="governance-source-card">`,
        `<strong>${escapeHtml(source.scope)} · ${escapeHtml(appliesText)}</strong>`,
        `<code>${escapeHtml(formatRepoRelativePath(source.path || source.suggested_path || ""))}</code>`,
        `<span>${escapeHtml(inspectText)}；${escapeHtml(source.permission_state || "unknown")}</span>`,
        reason,
        `</article>`,
      ].join("");
    }).join("");
  }

  function governanceLayerDetailText(resolution, layerId) {
    const source = (resolution.agents_sources || []).find((item) => item.scope === layerId);
    const detailByLayer = {
      runtime: [
        "Runtime / Platform / System 是最上層硬邊界。",
        "這部分包含平台、安全、工具與 developer 指令；靜態頁只能列為不可覆寫前提，不能宣稱已完整解析。",
      ].join("\n"),
      "global-home": source
        ? `global-home 來源會對多數工作目錄產生影響。\n路徑：${source.path}\n狀態：${source.inspectable ? "已納入解析" : source.unresolved_reason || "未讀取內容"}`
        : "未找到 global-home 來源。",
      workspace: source
        ? `workspace 來源用於工作區層級覆寫。\n路徑：${source.path}\n目前路徑：${source.applies_to_path ? "適用" : "僅作 evidence"}`
        : "未找到 workspace 來源。",
      repo: source
        ? `repo-local 來源是專案內可控規則。\n路徑：${source.path}\n目前路徑：${source.applies_to_path ? "適用" : "僅作 evidence"}`
        : "未找到 repo-local 來源。",
      request: [
        "Current User Request 是本輪任務意圖。",
        "它會在不違反上層規則的前提下決定實作方向；若與上層安全或 repo policy 衝突，以上層為準。",
      ].join("\n"),
    };
    return detailByLayer[layerId] || "選擇一個漏斗層級查看說明。";
  }

  function renderGovernanceFunnel(resolution) {
    if (!governanceFunnelEl || !governanceLayerDetailEl) return;
    const layerButtons = Array.from(governanceFunnelEl.querySelectorAll("[data-governance-layer]"));
    layerButtons.forEach((button) => {
      const active = (button.dataset.governanceLayer || "") === state.activeGovernanceLayer;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });
    governanceLayerDetailEl.textContent = governanceLayerDetailText(resolution, state.activeGovernanceLayer);
  }

  function renderGovernanceResolution(resolution, statusText = "") {
    if (!governanceResultEl) return;
    renderGovernanceSourceStatus(resolution);
    renderGovernanceFunnel(resolution);
    const layerLines = resolution.matched_layers.length
      ? resolution.matched_layers.map((layer) => `- ${layer.id} [${layer.scope}]`).join("\n")
      : "- 無";
    const configLines = Object.keys(resolution.effective_config).length
      ? Object.entries(resolution.effective_config)
        .sort((a, b) => a[0].localeCompare(b[0]))
        .map(([key, value]) => `- ${key}: ${value} (${resolution.provenance[key].source_layer})`)
        .join("\n")
      : "- 無";
    const sourceLines = resolution.agents_sources.length
      ? resolution.agents_sources.map((source) => formatGovernanceSourceLine(source)).join("\n")
      : "- 無";
    const hardRuleLines = resolution.effective_hard_rules.length
      ? resolution.effective_hard_rules.slice(0, 12).map((rule) => `- [${rule.scope}] ${rule.section}: ${rule.rule}`).join("\n")
      : "- 無";
    const guidanceLines = resolution.operational_guidance.length
      ? resolution.operational_guidance.slice(0, 8).map((rule) => `- [${rule.scope}] ${rule.section}: ${rule.rule}`).join("\n")
      : "- 無";
    governanceResultEl.textContent = [
      statusText ? `${statusText}\n` : "",
      "治理解析結果",
      `模型：${resolution.inputs.model}`,
      `環境：${resolution.inputs.environment}`,
      `指令設定：${resolution.inputs.instruction_profile}`,
      `任意操作路徑：${resolution.analysis_path || "未指定"}`,
      `路徑判定：${resolution.path_classification?.scope_hint || "unknown"} - ${resolution.path_classification?.note || ""}`,
      "",
      "符合條件的層級",
      layerLines,
      "",
      "實際生效的設定",
      configLines,
      "",
      "檔案治理層級說明",
      resolution.agents_hierarchy_note || "無",
      "",
      "檔案治理來源",
      sourceLines,
      "",
      "實際生效的硬性規則",
      hardRuleLines,
      resolution.effective_hard_rules.length > 12 ? `\n... 其餘 ${resolution.effective_hard_rules.length - 12} 條硬性規則會寫入報告。` : "",
      "",
      "作業指引",
      guidanceLines,
      resolution.operational_guidance.length > 8 ? `\n... 其餘 ${resolution.operational_guidance.length - 8} 條作業指引會寫入報告。` : "",
    ].join("\n");
  }

  function governanceMarkdown(resolution) {
    const lines = [
      "# 治理解析報告",
      "",
      `- 產生時間：\`${resolution.generated_at}\``,
      `- 模型：\`${resolution.inputs.model}\``,
      `- 環境：\`${resolution.inputs.environment}\``,
      `- 指令設定：\`${resolution.inputs.instruction_profile}\``,
      `- 任意操作路徑：\`${resolution.analysis_path || "未指定"}\``,
      `- 路徑判定：\`${resolution.path_classification?.scope_hint || "unknown"}\` ${resolution.path_classification?.note || ""}`,
      "",
      "## 符合條件的層級",
      "",
    ];
    if (resolution.matched_layers.length) {
      resolution.matched_layers.forEach((layer) => {
        lines.push(`- \`${layer.id}\``);
        lines.push(`  - 範圍：\`${layer.scope}\``);
        lines.push(`  - 說明：${layer.description || "無說明"}`);
      });
    } else {
      lines.push("- 無");
    }
    lines.push("", "## 實際生效的設定", "");
    Object.entries(resolution.effective_config).sort((a, b) => a[0].localeCompare(b[0])).forEach(([key, value]) => {
      lines.push(`- \`${key}\` = \`${value}\`（來自 \`${resolution.provenance[key].source_layer}\`）`);
    });
    lines.push("", "## 檔案治理來源", "");
    resolution.agents_sources.forEach((source) => {
      lines.push(formatGovernanceSourceLine(source));
    });
    lines.push("", "## 實際生效的硬性規則", "");
    resolution.effective_hard_rules.forEach((rule) => {
      lines.push(`- [${rule.scope}] \`${rule.section}\` — ${rule.rule}`);
    });
    lines.push("", "## 作業指引", "");
    resolution.operational_guidance.forEach((rule) => {
      lines.push(`- [${rule.scope}] \`${rule.section}\` — ${rule.rule}`);
    });
    lines.push("", "## 評估備註", "");
    resolution.instruction_evaluation.forEach((note) => lines.push(`- ${note}`));
    return `${lines.join("\n")}\n`;
  }

  function governanceJson(resolution) {
    return `${JSON.stringify(resolution, null, 2)}\n`;
  }

  function splitRelativeSegments(pathText) {
    return normalizeWindowsPath(pathText).split("\\").filter(Boolean);
  }

  function repoRelativeSegmentsFromNativePath(outputPath) {
    const repoRoot = normalizeWindowsPath(DATA.meta?.repo_root_native || "");
    const target = normalizeWindowsPath(outputPath);
    if (!repoRoot || !target) return null;
    const repoRootLower = repoRoot.toLowerCase();
    const targetLower = target.toLowerCase();
    if (targetLower === repoRootLower) return [];
    if (!isPathWithin(target, repoRoot)) return null;
    return splitRelativeSegments(target.slice(repoRoot.length + 1));
  }

  async function ensureDirectoryFromSegments(rootHandle, segments) {
    let current = rootHandle;
    for (const segment of segments) {
      current = await current.getDirectoryHandle(segment, { create: true });
    }
    return current;
  }

  async function writeTextFile(directoryHandle, filename, text) {
    const fileHandle = await directoryHandle.getFileHandle(filename, { create: true });
    const writable = await fileHandle.createWritable();
    await writable.write(text);
    await writable.close();
  }
  function setData(nextData, source) {
    DATA = cloneData(nextData);
    if (!DATA.meta) DATA.meta = {};
    if (!DATA.meta.repo_root_native && INITIAL_DATA?.meta?.repo_root_native) {
      DATA.meta.repo_root_native = INITIAL_DATA.meta.repo_root_native;
    }
    if (!DATA.governance && INITIAL_DATA?.governance) {
      DATA.governance = cloneData(INITIAL_DATA.governance);
    }
    nodeById = new Map((DATA.nodes || []).map((node) => [node.id, node]));
    if (!nodeById.has(state.selectedId)) {
      state.selectedId = pickDefaultNodeId(nodeById);
    }
    state.lastUpdatedAt = DATA.meta?.generated_at || new Date().toISOString();
    state.lastRefreshSource = source;
  }

  function setRefreshState(kind, message = "") {
    state.lastRefreshState = kind;
    if (message) state.lastRefreshMessage = message;
  }

  function syncActionButtons() {
    if (refreshNowEl) {
      refreshNowEl.disabled = state.refreshInFlight;
      refreshNowEl.textContent = state.refreshInFlight ? "更新中..." : "立即更新";
      refreshNowEl.dataset.state = state.lastRefreshState;
    }
    if (linkRepoEl) {
      linkRepoEl.disabled = state.refreshInFlight;
      linkRepoEl.textContent = state.refreshInFlight ? "目錄鎖定中" : "連結專案目錄";
    }
  }

  function loadSettings() {
    try {
      const raw = localStorage.getItem(SETTINGS_KEY);
      if (!raw) return;
      const settings = JSON.parse(raw);
      state.mapMode = MAP_MODES.has(settings.mapMode) ? settings.mapMode : state.mapMode;
      state.visualTone = normalizeLegacyTone(settings.visualTone) || state.visualTone;
      state.visualTheme = normalizeTheme(settings.visualTheme) || state.visualTheme;
      state.textScale = normalizeTextScale(settings.textScale) || state.textScale;
      state.updateMode = settings.updateMode || state.updateMode;
      state.intervalDays = Number.isFinite(settings.intervalDays) ? settings.intervalDays : state.intervalDays;
      state.intervalHours = Number.isFinite(settings.intervalHours) ? settings.intervalHours : state.intervalHours;
      state.intervalMinutes = Number.isFinite(settings.intervalMinutes) ? settings.intervalMinutes : state.intervalMinutes;
      state.workspacePage = WORKSPACE_PAGE_IDS.has(settings.workspacePage) ? settings.workspacePage : state.workspacePage;
      state.mapZoom = Number.isFinite(settings.mapZoom) ? clamp(settings.mapZoom, 0.72, 1.6) : state.mapZoom;
      state.governanceAnalysisPath = settings.governanceAnalysisPath || state.governanceAnalysisPath;
      state.governanceSourceOverrides = settings.governanceSourceOverrides && typeof settings.governanceSourceOverrides === "object"
        ? settings.governanceSourceOverrides
        : state.governanceSourceOverrides;
    } catch (_error) {}
  }

  function saveSettings() {
    try {
      localStorage.setItem(SETTINGS_KEY, JSON.stringify({
        mapMode: state.mapMode,
        visualTone: state.visualTone,
        visualTheme: state.visualTheme,
        textScale: state.textScale,
        updateMode: state.updateMode,
        intervalDays: state.intervalDays,
        intervalHours: state.intervalHours,
        intervalMinutes: state.intervalMinutes,
        workspacePage: state.workspacePage,
        mapZoom: state.mapZoom,
        governanceAnalysisPath: state.governanceAnalysisPath,
        governanceSourceOverrides: state.governanceSourceOverrides,
      }));
    } catch (_error) {}
  }

  function applyVisualTone() {
    if (!VISUAL_TONES.has(state.visualTone)) state.visualTone = "muted";
    document.documentElement.dataset.visualTone = state.visualTone;
    document.body.dataset.visualTone = state.visualTone;
    visualToneOptionEls.forEach((button) => {
      const tone = button.dataset.visualToneOption || "";
      const isActive = tone === state.visualTone;
      button.classList.toggle("active", isActive);
      button.setAttribute("aria-checked", isActive ? "true" : "false");
      button.tabIndex = isActive ? 0 : -1;
    });
    if (visualToneSliderEl) {
      visualToneSliderEl.value = String(Math.max(0, VISUAL_TONE_ORDER.indexOf(state.visualTone)));
      visualToneSliderEl.setAttribute("aria-valuetext", visualToneLabel(state.visualTone));
    }
  }

  function applyVisualTheme() {
    if (!VISUAL_THEMES.has(state.visualTheme)) state.visualTheme = "light";
    document.documentElement.dataset.theme = state.visualTheme;
    document.body.dataset.theme = state.visualTheme;
    visualThemeOptionEls.forEach((button) => {
      const theme = button.dataset.visualThemeOption || "";
      const isActive = theme === state.visualTheme;
      button.classList.toggle("active", isActive);
      button.setAttribute("aria-checked", isActive ? "true" : "false");
      button.tabIndex = isActive ? 0 : -1;
    });
    if (visualThemeSliderEl) {
      visualThemeSliderEl.value = String(Math.max(0, VISUAL_THEME_ORDER.indexOf(state.visualTheme)));
      visualThemeSliderEl.setAttribute("aria-valuetext", visualThemeLabel(state.visualTheme));
    }
  }

  function applyTextScale() {
    if (!TEXT_SCALES.has(state.textScale)) state.textScale = "md";
    document.documentElement.dataset.textScale = state.textScale;
    document.body.dataset.textScale = state.textScale;
    textScaleOptionEls.forEach((button) => {
      const scale = button.dataset.textScaleOption || "";
      const isActive = scale === state.textScale;
      button.classList.toggle("active", isActive);
      button.setAttribute("aria-checked", isActive ? "true" : "false");
      button.tabIndex = isActive ? 0 : -1;
    });
    if (textScaleSliderEl) {
      textScaleSliderEl.value = String(Math.max(0, TEXT_SCALE_ORDER.indexOf(state.textScale)));
      textScaleSliderEl.setAttribute("aria-valuetext", textScaleLabel(state.textScale));
    }
  }

  function setVisualTone(nextTone, options = {}) {
    if (!VISUAL_TONES.has(nextTone)) return;
    if (nextTone === state.visualTone) {
      if (options.focus) {
        const activeButton = visualToneOptionEls.find((button) => (button.dataset.visualToneOption || "") === nextTone);
        (visualToneSliderEl || activeButton)?.focus();
      }
      return;
    }
    state.visualTone = nextTone;
    applyVisualTone();
    render();
    if (options.focus) {
      const activeButton = visualToneOptionEls.find((button) => (button.dataset.visualToneOption || "") === nextTone);
      (visualToneSliderEl || activeButton)?.focus();
    }
  }

  function setVisualTheme(nextTheme, options = {}) {
    if (!VISUAL_THEMES.has(nextTheme)) return;
    if (nextTheme === state.visualTheme) {
      if (options.focus) {
        const activeButton = visualThemeOptionEls.find((button) => (button.dataset.visualThemeOption || "") === nextTheme);
        (visualThemeSliderEl || activeButton)?.focus();
      }
      return;
    }
    state.visualTheme = nextTheme;
    applyVisualTheme();
    render();
    if (options.focus) {
      const activeButton = visualThemeOptionEls.find((button) => (button.dataset.visualThemeOption || "") === nextTheme);
      (visualThemeSliderEl || activeButton)?.focus();
    }
  }

  function setTextScale(nextScale, options = {}) {
    if (!TEXT_SCALES.has(nextScale)) return;
    if (nextScale === state.textScale) {
      if (options.focus) {
        const activeButton = textScaleOptionEls.find((button) => (button.dataset.textScaleOption || "") === nextScale);
        (textScaleSliderEl || activeButton)?.focus();
      }
      return;
    }
    state.textScale = nextScale;
    applyTextScale();
    render();
    if (options.focus) {
      const activeButton = textScaleOptionEls.find((button) => (button.dataset.textScaleOption || "") === nextScale);
      (textScaleSliderEl || activeButton)?.focus();
    }
  }

  function getMapToneTheme() {
    return {
      guideSoft: cssVar("--map-guide-stroke-soft", "rgba(131, 114, 82, 0.12)"),
      guide: cssVar("--map-guide-stroke", "rgba(131, 114, 82, 0.14)"),
      orbit: cssVar("--map-orbit-stroke", "rgba(131, 114, 82, 0.18)"),
      title: cssVar("--map-title-ink", "#5f5a4b"),
      copy: cssVar("--map-copy-ink", "#7a705e"),
      activeFill: cssVar("--map-node-active-fill", "#fcfbf5"),
      activeStroke: cssVar("--map-node-active-stroke", "#176b66"),
      label: cssVar("--map-node-label", "#201c16"),
      sub: cssVar("--map-node-sub", "#6b6256"),
    };
  }

  function applySettingsToControls() {
    if (!MAP_MODES.has(state.mapMode)) state.mapMode = "radial";
    if (mapModeEl) mapModeEl.value = state.mapMode;
    applyVisualTone();
    applyVisualTheme();
    applyTextScale();
    if (updateModeEl) updateModeEl.value = state.updateMode;
    if (intervalDaysEl) intervalDaysEl.value = String(state.intervalDays);
    if (intervalHoursEl) intervalHoursEl.value = String(state.intervalHours);
    if (intervalMinutesEl) intervalMinutesEl.value = String(state.intervalMinutes);
    if (governanceAnalysisPathEl) governanceAnalysisPathEl.value = state.governanceAnalysisPath || "";
    syncWorkspacePages();
    setGovernanceInputDefaults();
    applyMapZoom();
  }

  function intervalMs() {
    const days = Math.max(0, Number(intervalDaysEl?.value || state.intervalDays || 0));
    const hours = Math.max(0, Number(intervalHoursEl?.value || state.intervalHours || 0));
    const minutes = Math.max(0, Number(intervalMinutesEl?.value || state.intervalMinutes || 0));
    return (((days * 24) + hours) * 60 + minutes) * 60 * 1000;
  }

  function rememberIntervalInputs() {
    state.intervalDays = Math.max(0, Number(intervalDaysEl?.value || 0));
    state.intervalHours = Math.max(0, Number(intervalHoursEl?.value || 0));
    state.intervalMinutes = Math.max(0, Number(intervalMinutesEl?.value || 0));
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

  function syncPrimaryBrowseControls(options = {}) {
    if (options.syncSearch !== false && searchEl) searchEl.value = state.search || "";
    if (typeFilterEl) typeFilterEl.value = state.type || "all";
  }

  function resetPrimaryBrowseFilters() {
    state.search = "";
    state.type = "all";
    state.diagnosticsFilter = "all";
    syncPrimaryBrowseControls();
  }

  function getQuickFilterCount(spec) {
    if (spec.kind === "type") return Number(DATA.counts?.[spec.value] || 0);
    if (spec.value === "broken-source") return Number(DATA.diagnostics?.broken_reference_count || 0);
    if (spec.value === "orphan") return Number(DATA.diagnostics?.orphan_node_count || 0);
    return 0;
  }

  function isQuickFilterActive(spec) {
    if (spec.kind === "type") return state.type === spec.value && state.diagnosticsFilter === "all";
    return state.diagnosticsFilter === spec.value;
  }

  function applyQuickFilter(kind, value) {
    const isActive = kind === "type"
      ? state.type === value && state.diagnosticsFilter === "all"
      : state.diagnosticsFilter === value;
    if (isActive) {
      resetPrimaryBrowseFilters();
      setWorkspacePage("browse", { persist: false, updateTour: false });
      render();
      return;
    }
    state.search = "";
    if (kind === "type") {
      state.type = value;
      state.diagnosticsFilter = "all";
    } else {
      state.type = "all";
      state.diagnosticsFilter = value;
    }
    syncPrimaryBrowseControls();
    setWorkspacePage("browse", { persist: false, updateTour: false });
    render();
  }

  function renderQuickFilterRail(containerEl, { showCounts = true } = {}) {
    if (!containerEl) return;
    containerEl.innerHTML = "";
    QUICK_FILTER_SPECS.forEach((spec) => {
      const count = getQuickFilterCount(spec);
      if (spec.kind === "type" && count <= 0) return;
      const button = document.createElement("button");
      button.type = "button";
      button.className = "chip quick-filter-chip";
      if (spec.kind === "diagnostic") button.classList.add("is-diagnostic");
      if (isQuickFilterActive(spec)) button.classList.add("active");
      button.setAttribute("aria-pressed", isQuickFilterActive(spec) ? "true" : "false");
      button.dataset.filterKind = spec.kind;
      button.dataset.filterValue = spec.value;

      const dotEl = document.createElement("span");
      dotEl.className = "chip-dot";
      dotEl.style.background = spec.kind === "type"
        ? cssVar(spec.colorVar, spec.colorFallback)
        : spec.value === "broken-source"
          ? "rgba(165, 106, 23, 0.72)"
          : "rgba(165, 128, 51, 0.66)";

      const labelEl = document.createElement("span");
      labelEl.className = "chip-label";
      labelEl.textContent = spec.label;
      button.appendChild(dotEl);
      button.appendChild(labelEl);

      if (showCounts) {
        const countEl = document.createElement("span");
        countEl.className = "chip-count";
        countEl.textContent = String(count);
        button.appendChild(countEl);
      }

      button.addEventListener("click", () => applyQuickFilter(spec.kind, spec.value));
      containerEl.appendChild(button);
    });
  }

  function computeVisibleNodes() {
    return (DATA.nodes || []).filter((node) => nodeMatchesFilters(node));
  }

  function nodeMatchesFilters(node) {
    const diagnostics = DATA.diagnostics || {};
    const orphanNodeIds = new Set(diagnostics.orphan_node_ids || []);
    const brokenSourceIds = new Set(diagnostics.broken_source_ids || []);
    if (state.type !== "all" && node.type !== state.type) return false;
    if (state.diagnosticsFilter === "orphan" && !orphanNodeIds.has(node.id)) return false;
    if (state.diagnosticsFilter === "broken-source" && !brokenSourceIds.has(node.id)) return false;
    if (!state.search) return true;
    const haystack = [node.label, node.path, node.logical_path, node.description]
      .filter(Boolean).join(" ").toLowerCase();
    return haystack.includes(state.search);
  }

  function jumpToNode(nodeId, reveal = false) {
    const target = nodeById.get(nodeId);
    if (!target) return;
    if (reveal && !nodeMatchesFilters(target)) {
      resetPrimaryBrowseFilters();
    }
    if (reveal) setWorkspacePage("browse", { persist: false, updateTour: false });
    state.selectedId = nodeId;
    render();
  }

  function applyDiagnosticsFilter(mode) {
    if (mode === "all") {
      resetPrimaryBrowseFilters();
      setWorkspacePage("browse", { persist: false, updateTour: false });
      render();
      return;
    }
    applyQuickFilter("diagnostic", mode);
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
    renderQuickFilterRail(summaryEl, { showCounts: true });
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
    syncPrimaryBrowseControls();
  }

  function renderGovernanceSourceNote() {
    if (!governanceSourceNoteEl) return;
    const { models, environments, instruction_profiles: instructionProfiles } = collectGovernanceOptions();
    const sourceList = getConfiguredGovernanceSources();
    const definitionPath = formatRepoRelativePath(
      sourceList.find((source) => source.definition_path)?.definition_path || "local/config/agent-governance-layers.json",
    );
    const sourceTargets = sourceList.length
      ? sourceList.map((source) => `${source.scope}: ${formatRepoRelativePath(source.path)}`).join("；")
      : "目前沒有結構化檔案治理來源";
    governanceSourceNoteEl.innerHTML = [
      "<strong>預先帶入來源</strong>",
      `模型 / 工作環境 / 指令配置的選項來自 <code>local/config/agent-governance-layers.json</code> 的 <code>layers.match</code>。`,
      `目前帶入：模型 <code>${escapeHtml(models.join(" / ") || "gpt-5.4")}</code>；環境 <code>${escapeHtml(environments.join(" / ") || "codex-local-dev")}</code>；指令配置 <code>${escapeHtml(instructionProfiles.join(" / ") || "mapping")}</code>。`,
      `檔案治理來源優先讀取 <code>${escapeHtml(definitionPath)}</code>；目前映射到 ${escapeHtml(sourceTargets)}。缺少結構化規則檔時，改讀 workspace / repo 的 <code>AGENTS.md</code>。`,
    ].join("<br>");
  }

  function updateStatusCard(errorText = "") {
    if (!updateStatusEl) {
      syncActionButtons();
      return;
    }
    const modeLabel = { manual: "手動更新", "on-open": "開啟網頁時自動更新", interval: "定時更新" }[state.updateMode];
    const strategyNote = {
      manual: "不做背景掃描，只有按下「立即更新」才重新解析；執行開銷最低。",
      "on-open": "開啟時掃描一次，降低資料過期風險，但會增加載入時間。",
      interval: "開啟期間依頻率重掃；資料較新，但會持續產生檔案 I/O 與重新繪圖成本。",
    }[state.updateMode];
    const repoText = state.repoHandleName ? `已連結：${state.repoHandleName}` : "尚未連結專案根目錄";
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
      <div><strong>執行限制</strong>：${supportText} 定時更新只在目前分頁開啟時生效，不會常駐執行。</div>
      ${errorText ? `<div><strong>最近錯誤</strong>：${escapeHtml(errorText)}</div>` : ""}
    `;
    syncActionButtons();
  }

  function getBrokenSources() {
    return DATA.diagnostics?.broken_sources || [];
  }

  function buildHandoffSummary() {
    const diagnostics = DATA.diagnostics || {};
    const counts = DATA.counts || {};
    const topBrokenSources = getBrokenSources().slice(0, 5)
      .map((item) => `- ${item.source_label} (${item.count}) — ${item.source_path}`)
      .join("\n");
    return [
      "# UniText 專案地圖交接摘要",
      "",
      `- 產生時間：${state.lastUpdatedAt || DATA.meta?.generated_at || "未知"}`,
      `- 輸出模式：${PAGE_MODE}`,
      `- 節點數量：${Object.values(counts).reduce((sum, value) => sum + Number(value || 0), 0)}`,
      `- 關聯數量：${(DATA.edges || []).length}`,
      `- 失效引用：${diagnostics.broken_reference_count || 0}`,
      `- 孤立資源：${diagnostics.orphan_node_count || 0}`,
      "",
      "## 執行面閱讀重點",
      "",
      "- 先看執行面文件與執行面投影，再回到 `registry/*` 的正式來源。",
      "- 把執行面對應回註冊來源的關聯邊，視為理解結構時最主要的追查路徑。",
      "",
      "## 資源數量",
      "",
      ...Object.entries(counts).sort((a, b) => a[0].localeCompare(b[0])).map(([key, value]) => `- ${key}: ${value}`),
      "",
      "## 主要失效來源",
      "",
      topBrokenSources || "- 無",
      "",
      "## 可交付檔案",
      "",
      "- site/project-map.html",
      "- site/project-map-share.html",
      "- site/project-map-handoff.md",
      "- site/project-map-handoff.json",
    ].join("\n");
  }

  function updateDiagnosticsCard() {
    const diagnostics = DATA.diagnostics || {};
    const brokenCount = diagnostics.broken_reference_count || 0;
    const orphanCount = diagnostics.orphan_node_count || 0;
    const brokenSources = getBrokenSources();
    const diagnosticRows = [
      {
        level: brokenCount ? "WARN" : "INFO",
        tone: brokenCount ? "warn" : "",
        message: brokenCount
          ? `${brokenCount} 個引用尚未映射，優先檢查失效來源清單。`
          : "引用關係目前沒有明顯缺口。",
      },
      {
        level: orphanCount ? "WARN" : "INFO",
        tone: orphanCount ? "warn" : "",
        message: orphanCount
          ? `${orphanCount} 個孤立資源未連回主要圖譜。`
          : "孤立資源檢查目前正常。",
      },
      {
        level: state.lastRefreshState === "error" ? "ERR" : "SYS_OK",
        tone: state.lastRefreshState === "error" ? "error" : "",
        message: `${state.lastRefreshMessage || "目前顯示的是最近一次靜態產出的 MAP。"} 最近更新：${formatTimestamp(state.lastUpdatedAt)}。`,
      },
    ];
    const activeFilterLabel = state.diagnosticsFilter === "orphan"
      ? "目前只顯示孤立資源"
      : state.diagnosticsFilter === "broken-source"
        ? "目前只顯示失效引用來源"
        : "目前顯示全部節點";
    const diagnosticLogMarkup = `
      <div class="diagnostic-ledger" aria-label="診斷事件摘要">
        ${diagnosticRows.map((row) => `
          <div class="diagnostic-row ${row.tone}">
            <span class="diagnostic-level">${row.level}</span>
            <span class="diagnostic-message">${escapeHtml(row.message)}</span>
          </div>
        `).join("")}
      </div>
    `;
    const sourceMarkup = brokenSources.length
      ? `
        <div class="section-title" style="margin-top:12px;">失效來源下鑽檢查</div>
        <div class="source-list">
          ${brokenSources.slice(0, 8).map((item) => `
            <button type="button" class="source-item diagnostics-source-jump" data-source-id="${escapeHtml(item.source_id)}">
              <strong>${escapeHtml(item.source_label)}</strong>
              <div class="source-meta">${escapeHtml(item.source_path)}；${item.count} 個尚未映射的目標；點擊可跳到來源節點</div>
            </button>
          `).join("")}
        </div>
        ${brokenSources.length > 8 ? `<div class="edge-visibility">其餘 ${brokenSources.length - 8} 個來源可於 JSON / 交接檔查看。</div>` : ""}
      `
      : `<div class="edge-visibility">目前沒有失效引用來源。</div>`;
    diagnosticsCardEl.innerHTML = `
      <span class="card-title">診斷檢查</span>
      <div><strong>失效引用</strong>：${brokenCount}</div>
      <div><strong>孤立資源</strong>：${orphanCount}</div>
      <div class="edge-visibility">這兩個數字可判斷執行面與正式來源的對應是否有明顯落差。</div>
      <div class="edge-visibility">${activeFilterLabel}</div>
      ${diagnosticLogMarkup}
      <div class="card-actions">
        <button type="button" class="mini-action secondary" id="filter-broken-sources" ${brokenCount ? "" : "disabled"}>只看失效來源</button>
        <button type="button" class="mini-action secondary" id="filter-orphans" ${orphanCount ? "" : "disabled"}>只看孤立資源</button>
        <button type="button" class="mini-action" id="filter-clear-diagnostics" ${state.diagnosticsFilter === "all" ? "disabled" : ""}>清除診斷篩選</button>
      </div>
      ${sourceMarkup}
    `;
    diagnosticsCardEl.querySelector("#filter-broken-sources")?.addEventListener("click", () => applyDiagnosticsFilter("broken-source"));
    diagnosticsCardEl.querySelector("#filter-orphans")?.addEventListener("click", () => applyDiagnosticsFilter("orphan"));
    diagnosticsCardEl.querySelector("#filter-clear-diagnostics")?.addEventListener("click", () => applyDiagnosticsFilter("all"));
    diagnosticsCardEl.querySelectorAll(".diagnostics-source-jump").forEach((button) => {
      button.addEventListener("click", () => {
        jumpToNode(button.dataset.sourceId, true);
      });
    });
  }

  function updateExportCard() {
    if (!exportCardEl) return;
    const shareHref = new URL("./project-map-share.html", window.location.href).href;
    const handoffMdHref = new URL("./project-map-handoff.md", window.location.href).href;
    const handoffJsonHref = new URL("./project-map-handoff.json", window.location.href).href;
    const staticArtifactNote = state.lastRefreshSource !== "bootstrap"
      ? `<div class="edge-visibility"><strong>Static artifacts:</strong> 頁內重掃只更新目前瀏覽器中的 MAP。交付前請執行 <code>python local/scripts/build-project-map.py</code> 重新生成分享頁與交接檔。</div>`
      : `<div class="edge-visibility"><strong>Static artifacts:</strong> 分享頁與交接檔對齊目前載入的靜態 bootstrap 輸出。</div>`;
    exportCardEl.innerHTML = `
      <span class="card-title">交付輸出</span>
      <div><strong>分享用輸出</strong>：可直接打開唯讀分享版快照。</div>
      <div class="edge-visibility">分享頁與交接檔保留目前狀態、診斷數字與主要來源資訊。</div>
      ${staticArtifactNote}
      <div class="card-actions">
        <a class="mini-action" href="${shareHref}" target="_blank" rel="noopener noreferrer">開啟分享版</a>
        <a class="mini-action secondary" href="${handoffMdHref}" target="_blank" rel="noopener noreferrer">開啟交接摘要.md</a>
        <a class="mini-action secondary" href="${handoffJsonHref}" target="_blank" rel="noopener noreferrer">開啟交接摘要.json</a>
        <button type="button" class="mini-action" id="copy-handoff-summary">複製交接摘要</button>
      </div>
    `;
    exportCardEl.querySelector("#copy-handoff-summary")?.addEventListener("click", async () => {
      const button = exportCardEl.querySelector("#copy-handoff-summary");
      if (!(button instanceof HTMLButtonElement)) return;
      const original = button.textContent;
      try {
        await copyText(buildHandoffSummary());
        button.textContent = "已複製摘要";
        window.setTimeout(() => { button.textContent = original; }, 1400);
      } catch (_error) {
        button.textContent = "複製失敗";
        window.setTimeout(() => { button.textContent = original; }, 1600);
      }
    });
  }

  async function resolveGovernanceAction() {
    const resolution = resolveGovernanceInPage();
    renderGovernanceResolution(resolution, "已重新解析治理配置。");
    return resolution;
  }

  async function writeGovernanceReports() {
    const resolution = await resolveGovernanceAction();
    const handle = await ensureRepoHandle(true);
    if (!handle) {
      renderGovernanceResolution(resolution, "尚未連結專案根目錄，無法寫出治理報告。");
      return;
    }
    const outputPath = governanceOutputPathEl?.value?.trim() || defaultGovernanceOutputPath();
    const relativeSegments = repoRelativeSegmentsFromNativePath(outputPath);
    if (!relativeSegments) {
      renderGovernanceResolution(resolution, `輸出位置必須位於目前專案目錄之內：${DATA.meta?.repo_root_native || "未知專案根目錄"}`);
      return;
    }
    const outputDirHandle = await ensureDirectoryFromSegments(handle, relativeSegments);
    await writeTextFile(outputDirHandle, "agent-governance-resolution.md", governanceMarkdown(resolution));
    await writeTextFile(outputDirHandle, "agent-governance-resolution.json", governanceJson(resolution));
    renderGovernanceResolution(resolution, `已寫出治理報告到 ${outputPath}`);
  }

  function renderSidebar(visible) {
    sidebarEl.innerHTML = "";
    const typeStyles = getTypeStylesTheme();
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
        const typeStyle = typeStyles[node.type] || typeStyles.directory;
        button.innerHTML = `
          <div class="node-head"><strong>${node.label}</strong><span class="node-type" style="background:${typeStyle.badge}">${TYPE_LABELS[node.type] || node.type}</span></div>
          <span class="node-description">${node.description || "沒有額外描述"}</span>
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
    detailNoteEl.textContent = state.mapMode === "grid" ? "欄式視圖會依資源類型由上往下排列" : "圓形視圖會以所選節點為中心展開";
    const relatedAll = relatedEdges(selected.id);
    const outgoing = relatedAll.filter((edge) => edge.from === selected.id);
    const incoming = relatedAll.filter((edge) => edge.to === selected.id);
    const brokenSource = getBrokenSources().find((item) => item.source_id === selected.id) || null;
    const detailParts = [
      `<div class="detail-kicker">${TYPE_LABELS[selected.type] || escapeHtml(selected.type)} / Inspector</div>`,
      `<h3>${escapeHtml(selected.label)}</h3>`,
      `<p>${escapeHtml(selected.description || "沒有額外描述。")}</p>`,
      `<div class="detail-urn">${escapeHtml(selected.id)}</div>`,
      '<div class="meta">',
      `<div class="meta-row"><strong>資源類型</strong>${TYPE_LABELS[selected.type] || escapeHtml(selected.type)}</div>`,
      `<div class="meta-row"><strong>路徑</strong>${escapeHtml(selected.path)}</div>`,
    ];
    if (selected.logical_path) detailParts.push(`<div class="meta-row"><strong>邏輯路徑</strong>${escapeHtml(selected.logical_path)}</div>`);
    if (selected.status) detailParts.push(`<div class="meta-row"><strong>狀態</strong>${escapeHtml(selected.status)}</div>`);
    if (selected.source_path) detailParts.push(`<div class="meta-row"><strong>來源檔案</strong>${escapeHtml(selected.source_path)}</div>`);
    detailParts.push("</div>");

    function pushEdgeSection(title, list, mode) {
      if (!list.length) return;
      detailParts.push(`<div class="section-title">${title}</div>`);
      detailParts.push('<div class="edge-list">');
      list.slice().sort((a, b) => (EDGE_LABELS[a.kind] || a.kind).localeCompare(EDGE_LABELS[b.kind] || b.kind)).forEach((edge) => {
        const peerId = mode === "outgoing" ? edge.to : edge.from;
        const peer = nodeById.get(peerId);
        if (!peer) return;
        const directionText = mode === "outgoing" ? `${selected.label} -> ${peer.label}` : `${peer.label} -> ${selected.label}`;
        const visible = visibleIds.has(peer.id);
        const visibilityText = visible ? "目前可見於地圖與節點清單" : "目前被搜尋或類型篩選隱藏";
        detailParts.push(`<button type="button" class="edge-item edge-jump" data-peer-id="${escapeHtml(peer.id)}"><strong>${EDGE_LABELS[edge.kind] || escapeHtml(edge.kind)}</strong><div class="edge-direction">${escapeHtml(directionText)}</div><div>${escapeHtml(peer.path)}</div><div class="edge-visibility">${visibilityText}；點擊可跳轉</div></button>`);
      });
      detailParts.push("</div>");
    }

    if (relatedAll.length) {
      pushEdgeSection("向外關聯", outgoing, "outgoing");
      pushEdgeSection("向內關聯", incoming, "incoming");
    } else {
      detailParts.push('<p class="empty">目前沒有關聯邊。</p>');
    }
    if (brokenSource) {
      detailParts.push('<div class="section-title">失效引用</div>');
      detailParts.push(`<p class="empty">這個來源節點目前有 ${brokenSource.count} 個連結解析到專案目錄內的檔案，但那些目標尚未被納入目前的地圖範圍。</p>`);
      detailParts.push('<div class="edge-list">');
      brokenSource.targets.forEach((item) => {
        detailParts.push(`
          <div class="edge-item">
            <strong>未映射目標</strong>
            <div class="edge-direction">${escapeHtml(item.target)}</div>
            <div>${escapeHtml(item.resolved_path)}</div>
            <div class="broken-target-meta">來源檔已引用此路徑，但產生器目前沒有把它建成節點。這通常代表它是專案目錄內尚未納入的文件、模板，或超出目前執行面與正式來源集合的資源。</div>
          </div>
        `);
      });
      detailParts.push("</div>");
    }
    detailEl.innerHTML = detailParts.join("");
    detailEl.querySelectorAll(".edge-jump").forEach((button) => {
      button.addEventListener("click", () => {
        jumpToNode(button.dataset.peerId, true);
      });
    });
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
    const labelColumnWidth = 140;
    const baseX = labelColumnWidth + 48;
    const topPadding = 86;
    const rowGap = 94;
    const columnWidth = 214;
    const boxWidth = 194;
    const boxHeight = 60;
    const positions = new Map();
    let maxColumns = 1;
    TYPE_ORDER.forEach((type, index) => {
      const items = (grouped.get(type) || []).slice().sort((a, b) => a.label.localeCompare(b.label));
      maxColumns = Math.max(maxColumns, items.length || 1);
      items.forEach((node, columnIndex) => {
        positions.set(node.id, {
          nodeId: node.id,
          x: baseX + columnIndex * columnWidth,
          y: topPadding + index * rowGap,
          width: boxWidth,
          height: boxHeight,
          type,
        });
      });
    });
    return {
      positions,
      width: Math.max(1380, baseX + maxColumns * columnWidth + 120),
      height: Math.max(780, topPadding + TYPE_ORDER.length * rowGap + 86),
      labelX: 40,
      labelColumnWidth,
      rowYByType: new Map(TYPE_ORDER.map((type, index) => [type, topPadding + index * rowGap])),
    };
  }

  function layoutOrbit(visible, mode) {
    const depths = computeDepths(visible);
    const positions = new Map();
    const selectedId = state.selectedId && nodeById.has(state.selectedId) ? state.selectedId : visible[0]?.id ?? null;
    const width = 1500;
    const height = 1020;
    const center = { x: width / 2, y: height / 2 };
    const ringBase = 180;
    const ringGap = 150;
    if (selectedId) {
      positions.set(selectedId, { nodeId: selectedId, x: center.x - 118, y: center.y - 34, width: 236, height: 68, type: nodeById.get(selectedId)?.type || "directory" });
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
        const boxWidth = depth === 1 ? 190 : 176;
        const boxHeight = 56;
        let angle = -Math.PI / 2;
        angle = count === 1 ? -Math.PI / 2 : (-Math.PI / 2) + ((Math.PI * 2) * index) / count;
        const x = center.x + Math.cos(angle) * radius - boxWidth / 2;
        const y = center.y + Math.sin(angle) * radius - boxHeight / 2;
        positions.set(node.id, { nodeId: node.id, x, y, width: boxWidth, height: boxHeight, type: node.type });
      });
    });
    return { positions, width, height, center, depths };
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function unionBoxes(boxes) {
    const available = boxes.filter(Boolean);
    if (!available.length) return null;
    const left = Math.min(...available.map((box) => box.x));
    const top = Math.min(...available.map((box) => box.y));
    const right = Math.max(...available.map((box) => box.x + box.width));
    const bottom = Math.max(...available.map((box) => box.y + box.height));
    return {
      x: left,
      y: top,
      width: right - left,
      height: bottom - top,
    };
  }

  function getFocusBox(selectedId, positions) {
    const selected = positions.get(selectedId);
    if (!selected) return null;
    if (state.mapMode === "grid") return selected;
    const neighborBoxes = (DATA.edges || [])
      .filter((edge) => edge.from === selectedId || edge.to === selectedId)
      .map((edge) => positions.get(edge.from === selectedId ? edge.to : edge.from))
      .filter(Boolean);
    return unionBoxes([selected, ...neighborBoxes.slice(0, 8)]) || selected;
  }

  function focusSelectedNode(box) {
    if (!mapWrapEl || !box) return;
    const paddingX = state.mapMode === "grid" ? 64 : 96;
    const paddingY = state.mapMode === "grid" ? 56 : 84;
    const targetLeft = clamp(
      ((box.x + (box.width / 2)) * state.mapZoom) - (mapWrapEl.clientWidth / 2),
      0,
      Math.max(0, mapWrapEl.scrollWidth - mapWrapEl.clientWidth),
    );
    const targetTop = clamp(
      ((box.y + (box.height / 2)) * state.mapZoom) - (mapWrapEl.clientHeight / 2),
      0,
      Math.max(0, mapWrapEl.scrollHeight - mapWrapEl.clientHeight),
    );
    mapWrapEl.scrollTo({
      left: Math.max(0, targetLeft - paddingX),
      top: Math.max(0, targetTop - paddingY),
      behavior: "smooth",
    });
  }

  function applyMapZoom() {
    state.mapZoom = clamp(Number(state.mapZoom) || 1, 0.72, 1.6);
    if (mapZoomLabelEl) mapZoomLabelEl.textContent = `${Math.round(state.mapZoom * 100)}%`;
    if (!mapEl || !state.lastMapLayout) return;
    mapEl.style.width = `${Math.round(state.lastMapLayout.width * state.mapZoom)}px`;
    mapEl.style.height = `${Math.round(state.lastMapLayout.height * state.mapZoom)}px`;
    scheduleMinimapViewportUpdate();
  }

  function setMapZoom(nextZoom) {
    if (!mapWrapEl) return;
    const beforeCenterX = mapWrapEl.scrollLeft + (mapWrapEl.clientWidth / 2);
    const beforeCenterY = mapWrapEl.scrollTop + (mapWrapEl.clientHeight / 2);
    const previousZoom = state.mapZoom || 1;
    state.mapZoom = clamp(nextZoom, 0.72, 1.6);
    applyMapZoom();
    const ratio = state.mapZoom / previousZoom;
    mapWrapEl.scrollTo({
      left: Math.max(0, (beforeCenterX * ratio) - (mapWrapEl.clientWidth / 2)),
      top: Math.max(0, (beforeCenterY * ratio) - (mapWrapEl.clientHeight / 2)),
      behavior: "auto",
    });
    saveSettings();
  }

  function panMapViewport(deltaX, deltaY) {
    mapWrapEl?.scrollBy({ left: deltaX, top: deltaY, behavior: "smooth" });
  }

  function centerMapViewport() {
    if (!mapWrapEl) return;
    mapWrapEl.scrollTo({
      left: Math.max(0, (mapWrapEl.scrollWidth - mapWrapEl.clientWidth) / 2),
      top: Math.max(0, (mapWrapEl.scrollHeight - mapWrapEl.clientHeight) / 2),
      behavior: "smooth",
    });
  }

  function resetMapViewport() {
    state.mapZoom = 1;
    applyMapZoom();
    mapWrapEl?.scrollTo({ left: 0, top: 0, behavior: "smooth" });
    saveSettings();
  }

  function renderMinimap(layout, visible, visibleIds, selectedId) {
    if (!mapMinimapEl) return;
    const positions = layout.positions;
    const mapTone = getMapToneTheme();
    const typeStyles = getTypeStylesTheme();
    mapMinimapEl.setAttribute("viewBox", `0 0 ${layout.width} ${layout.height}`);
    mapMinimapEl.setAttribute("preserveAspectRatio", "xMidYMid meet");
    mapMinimapEl.innerHTML = "";

    const backdropLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
    if (state.mapMode === "grid") {
      TYPE_ORDER.forEach((type) => {
        const y = layout.rowYByType?.get(type);
        if (typeof y !== "number") return;
        const guide = document.createElementNS("http://www.w3.org/2000/svg", "line");
        guide.setAttribute("x1", String((layout.labelColumnWidth || 140) + 12));
        guide.setAttribute("y1", String(y + 30));
        guide.setAttribute("x2", String(layout.width - 12));
        guide.setAttribute("y2", String(y + 30));
        guide.setAttribute("stroke", mapTone.guideSoft);
        guide.setAttribute("stroke-width", "1");
        guide.setAttribute("stroke-dasharray", "5 8");
        backdropLayer.appendChild(guide);
      });
    } else {
      const depthValues = Array.from((layout.depths || new Map()).values()).filter((depth) => depth > 0);
      const maxDepth = depthValues.length ? Math.max(...depthValues) : 0;
      for (let depth = 1; depth <= maxDepth; depth += 1) {
        const ring = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        ring.setAttribute("cx", String(layout.center.x));
        ring.setAttribute("cy", String(layout.center.y));
        ring.setAttribute("r", String(180 + ((depth - 1) * 150)));
        ring.setAttribute("fill", "none");
        ring.setAttribute("stroke", mapTone.guideSoft);
        ring.setAttribute("stroke-width", "1");
        ring.setAttribute("stroke-dasharray", "4 8");
        backdropLayer.appendChild(ring);
      }
    }
    mapMinimapEl.appendChild(backdropLayer);

    const edgeLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
    buildVisibleEdges(visibleIds).forEach((edge) => {
      const from = positions.get(edge.from);
      const to = positions.get(edge.to);
      if (!from || !to) return;
      const style = EDGE_STYLES[edge.kind] || EDGE_STYLES.contains;
      const active = edge.from === selectedId || edge.to === selectedId;
      const edgeShape = document.createElementNS("http://www.w3.org/2000/svg", "line");
      edgeShape.setAttribute("x1", String(from.x + from.width / 2));
      edgeShape.setAttribute("y1", String(from.y + from.height / 2));
      edgeShape.setAttribute("x2", String(to.x + to.width / 2));
      edgeShape.setAttribute("y2", String(to.y + to.height / 2));
      edgeShape.setAttribute("stroke", active ? mapTone.activeStroke : style.stroke);
      edgeShape.setAttribute("stroke-width", active ? "1.4" : "1");
      edgeShape.setAttribute("stroke-opacity", active ? "0.78" : String(Math.min(style.opacity, 0.42)));
      if (style.dash) edgeShape.setAttribute("stroke-dasharray", style.dash);
      edgeLayer.appendChild(edgeShape);
    });
    mapMinimapEl.appendChild(edgeLayer);

    const nodeLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
    visible.forEach((node) => {
      const box = positions.get(node.id);
      if (!box) return;
      const typeStyle = typeStyles[node.type] || typeStyles.directory;
      const active = node.id === selectedId;
      const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", String(box.x));
      rect.setAttribute("y", String(box.y));
      rect.setAttribute("width", String(box.width));
      rect.setAttribute("height", String(box.height));
      rect.setAttribute("rx", active ? "16" : "12");
      rect.setAttribute("fill", active ? mapTone.activeFill : typeStyle.fill);
      rect.setAttribute("stroke", active ? mapTone.activeStroke : typeStyle.stroke);
      rect.setAttribute("stroke-width", active ? "2" : "0.9");
      rect.setAttribute("fill-opacity", active ? "0.98" : "0.78");
      nodeLayer.appendChild(rect);
    });
    mapMinimapEl.appendChild(nodeLayer);

    state.lastMapLayout = { width: layout.width, height: layout.height };
    syncMinimapVisibility();
    scheduleMinimapViewportUpdate();
  }

  function renderMap(visible, visibleIds) {
    const selectedId = state.selectedId;
    const layout = state.mapMode === "grid" ? layoutGrid(visible) : layoutOrbit(visible, state.mapMode);
    const mapTone = getMapToneTheme();
    const typeStyles = getTypeStylesTheme();
    const positions = layout.positions;
    mapEl.setAttribute("viewBox", `0 0 ${layout.width} ${layout.height}`);
    state.lastMapLayout = layout;
    mapEl.style.width = `${Math.round(layout.width * state.mapZoom)}px`;
    mapEl.style.height = `${Math.round(layout.height * state.mapZoom)}px`;
    mapEl.innerHTML = "";
    const titleLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
    if (state.mapMode === "grid") {
      const helper = document.createElementNS("http://www.w3.org/2000/svg", "text");
      helper.setAttribute("x", "40");
      helper.setAttribute("y", "42");
      helper.setAttribute("fill", mapTone.copy);
      helper.setAttribute("font-size", formatSvgFontSize(11.4));
      helper.textContent = "欄式視圖改為由上往下看類型，橫向拖移看完整列。";
      titleLayer.appendChild(helper);

      TYPE_ORDER.forEach((type) => {
        const y = layout.rowYByType?.get(type) ?? 86 + TYPE_ORDER.indexOf(type) * 94;
        const guide = document.createElementNS("http://www.w3.org/2000/svg", "line");
        guide.setAttribute("x1", String((layout.labelColumnWidth || 140) + 16));
        guide.setAttribute("y1", String(y + 30));
        guide.setAttribute("x2", String(layout.width - 28));
        guide.setAttribute("y2", String(y + 30));
        guide.setAttribute("stroke", mapTone.guide);
        guide.setAttribute("stroke-width", "1");
        guide.setAttribute("stroke-dasharray", "5 8");
        titleLayer.appendChild(guide);

        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", String(layout.labelX || 40));
        label.setAttribute("y", String(y + 34));
        label.setAttribute("fill", mapTone.title);
        label.setAttribute("font-size", formatSvgFontSize(14.2));
        label.setAttribute("font-weight", "700");
        label.setAttribute("dominant-baseline", "middle");
        label.textContent = TYPE_LABELS[type] || type;
        titleLayer.appendChild(label);
      });
    } else {
      const selected = nodeById.get(selectedId);
      const orbitLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
      const depthValues = Array.from((layout.depths || new Map()).values()).filter((depth) => depth > 0);
      const maxDepth = depthValues.length ? Math.max(...depthValues) : 0;
      for (let depth = 1; depth <= maxDepth; depth += 1) {
        const ring = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        ring.setAttribute("cx", String(layout.center.x));
        ring.setAttribute("cy", String(layout.center.y));
        ring.setAttribute("r", String(180 + ((depth - 1) * 150)));
        ring.setAttribute("fill", "none");
        ring.setAttribute("stroke", mapTone.orbit);
        ring.setAttribute("stroke-width", "1");
        ring.setAttribute("stroke-dasharray", "4 8");
        orbitLayer.appendChild(ring);
      }
      mapEl.appendChild(orbitLayer);
      const header = document.createElementNS("http://www.w3.org/2000/svg", "text");
      header.setAttribute("x", "44");
      header.setAttribute("y", "46");
      header.setAttribute("fill", mapTone.title);
      header.setAttribute("font-size", formatSvgFontSize(15.2));
      header.setAttribute("font-weight", "700");
      header.textContent = `圓形視圖：以 ${selected?.label || "目前節點"} 為中心`;
      titleLayer.appendChild(header);
      const sub = document.createElementNS("http://www.w3.org/2000/svg", "text");
      sub.setAttribute("x", "44");
      sub.setAttribute("y", "70");
      sub.setAttribute("fill", mapTone.copy);
      sub.setAttribute("font-size", formatSvgFontSize(11.2));
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
      const edgeShape = document.createElementNS("http://www.w3.org/2000/svg", "line");
      edgeShape.setAttribute("x1", String(from.x + from.width / 2));
      edgeShape.setAttribute("y1", String(from.y + from.height / 2));
      edgeShape.setAttribute("x2", String(to.x + to.width / 2));
      edgeShape.setAttribute("y2", String(to.y + to.height / 2));
      edgeShape.setAttribute("stroke", active ? mapTone.activeStroke : style.stroke);
      edgeShape.setAttribute("stroke-width", active ? String(style.width + 0.9) : String(style.width));
      edgeShape.setAttribute("stroke-opacity", active ? "0.96" : String(style.opacity));
      if (style.dash) edgeShape.setAttribute("stroke-dasharray", style.dash);
      edgeLayer.appendChild(edgeShape);
    });
    mapEl.appendChild(edgeLayer);

    const nodeLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
    visible.slice().sort((a, b) => (a.id === selectedId ? 1 : 0) - (b.id === selectedId ? 1 : 0)).forEach((node) => {
      const box = positions.get(node.id);
      if (!box) return;
      const active = node.id === selectedId;
      const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
      group.style.cursor = "pointer";
      group.dataset.mapNode = node.id;
      group.setAttribute("role", "button");
      group.setAttribute("tabindex", "0");
      group.setAttribute("aria-label", `選取 ${node.label}`);
      const typeStyle = typeStyles[node.type] || typeStyles.directory;

      const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", String(box.x));
      rect.setAttribute("y", String(box.y));
      rect.setAttribute("width", String(box.width));
      rect.setAttribute("height", String(box.height));
      rect.setAttribute("rx", active ? "18" : "14");
      rect.setAttribute("fill", active ? mapTone.activeFill : typeStyle.fill);
      rect.setAttribute("stroke", active ? mapTone.activeStroke : typeStyle.stroke);
      rect.setAttribute("stroke-width", active ? "2.1" : "1.1");
      group.appendChild(rect);

      const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("x", String(box.x + 16));
      label.setAttribute("y", String(box.y + 23));
      label.setAttribute("fill", mapTone.label);
      label.setAttribute("font-size", formatSvgFontSize(active ? 13.4 : 12.4));
      label.setAttribute("font-weight", active ? "700" : "600");
      label.textContent = node.label.length > 27 ? `${node.label.slice(0, 26)}…` : node.label;
      group.appendChild(label);

      const typeTag = document.createElementNS("http://www.w3.org/2000/svg", "text");
      typeTag.setAttribute("x", String(box.x + box.width - 14));
      typeTag.setAttribute("y", String(box.y + 23));
      typeTag.setAttribute("fill", active ? mapTone.activeStroke : typeStyle.stroke);
      typeTag.setAttribute("font-size", formatSvgFontSize(9.8));
      typeTag.setAttribute("font-weight", "700");
      typeTag.setAttribute("text-anchor", "end");
      typeTag.textContent = (TYPE_LABELS[node.type] || node.type).toUpperCase();
      group.appendChild(typeTag);

      const sub = document.createElementNS("http://www.w3.org/2000/svg", "text");
      sub.setAttribute("x", String(box.x + 16));
      sub.setAttribute("y", String(box.y + 42));
      sub.setAttribute("fill", mapTone.sub);
      sub.setAttribute("font-size", formatSvgFontSize(active ? 10.6 : 10.2));
      sub.textContent = node.status || "active";
      group.appendChild(sub);

      group.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        state.suppressNextMapClick = false;
        state.selectedId = node.id;
        render();
      });
      group.addEventListener("keydown", (event) => {
        if (event.key !== "Enter" && event.key !== " ") return;
        event.preventDefault();
        state.selectedId = node.id;
        render();
      });
      nodeLayer.appendChild(group);
    });
    mapEl.appendChild(nodeLayer);
    renderMinimap(layout, visible, visibleIds, selectedId);
    applyMapZoom();

    if (state.mapMode === "grid") {
      mapModeNoteEl.textContent = "欄式視圖：類型由上往下，橫向拖移看完整列";
      mapCaptionEl.textContent = "欄式視圖依資源類型分列；同列節點可左右拖移查看。";
    } else {
      mapModeNoteEl.textContent = "圓形視圖：以所選節點為圓心向外展開";
      mapCaptionEl.textContent = "第一圈優先呈現直接關聯節點，其中最有價值的是執行面投影與正式來源之間的對應。";
    }
    const selectedBox = getFocusBox(selectedId, positions);
    if (selectedBox) {
      requestAnimationFrame(() => focusSelectedNode(selectedBox));
    }
  }

  function render() {
    syncWorkspacePages();
    updateSummary();
    renderGovernanceSourceNote();
    updateDiagnosticsCard();
    updateExportCard();
    const visible = computeVisibleNodes();
    const ids = new Set(visible.map((node) => node.id));
    if (!ids.has(state.selectedId)) state.selectedId = visible[0]?.id ?? null;
    renderSidebar(visible);
    renderMap(visible, ids);
    renderDetail(ids);
    syncMastheadCompactState();
    if (state.tourOpen) {
      requestAnimationFrame(() => updateTourLayout());
    }
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

  async function hasHandlePermission(handle, mode = "read", request = false) {
    const options = { mode };
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

  function markerKind(relativePath) {
    return relativePath.endsWith("/skills")
      || relativePath.endsWith("/mcp")
      || relativePath.endsWith("/agents")
      || relativePath.endsWith("/workflow")
      ? "directory"
      : "file";
  }

  async function inspectRootMarkers(rootHandle, markers) {
    const present = [];
    const missing = [];
    for (const marker of markers) {
      const exists = await pathExists(rootHandle, marker, markerKind(marker));
      if (exists) present.push(marker);
      else missing.push(marker);
    }
    return { present, missing };
  }

  async function selectRootAdapter(rootHandle) {
    const fallbackAdapter = ACTIVE_PROJECT_MAP_ADAPTER || {
      adapter_id: "legacy",
      root_markers: REPO_MARKERS,
      core_docs: CORE_DOCS,
      root_directories: ROOT_DIRECTORIES,
    };
    const adapters = PROJECT_MAP_ADAPTERS?.length ? PROJECT_MAP_ADAPTERS : [fallbackAdapter];
    const checks = {};

    for (const adapter of adapters) {
      const inspection = await inspectRootMarkers(rootHandle, adapter.root_markers || []);
      checks[adapter.adapter_id] = {
        markers_present: inspection.present,
        markers_missing: inspection.missing,
      };
      if (adapter.adapter_id === "unitext" && inspection.present.length === (adapter.root_markers || []).length) {
        return { adapter, inspection, checks };
      }
    }

    const governanceAdapter = adapters.find((adapter) => adapter.adapter_id === "governance-folder");
    const governanceCheck = governanceAdapter ? checks[governanceAdapter.adapter_id] : null;
    if (governanceAdapter && governanceCheck?.markers_present?.length) {
      return {
        adapter: governanceAdapter,
        inspection: {
          present: governanceCheck.markers_present,
          missing: governanceCheck.markers_missing,
        },
        checks,
      };
    }

    for (const adapter of adapters) {
      if (adapter.adapter_id === "unitext" || adapter.adapter_id === "governance-folder") continue;
      const check = checks[adapter.adapter_id];
      if (check?.markers_present?.length) {
        return {
          adapter,
          inspection: {
            present: check.markers_present,
            missing: check.markers_missing,
          },
          checks,
        };
      }
    }

    return { adapter: null, inspection: { present: [], missing: [] }, checks };
  }

  async function scanRepo(rootHandle) {
    const adapterSelection = await selectRootAdapter(rootHandle);
    const scanAdapter = adapterSelection.adapter;
    const markerInspection = adapterSelection.inspection;
    if (!scanAdapter) {
      const markerChoices = (PROJECT_MAP_ADAPTERS || [])
        .flatMap((adapter) => adapter.root_markers || [])
        .join(", ");
      throw new Error(`選取的資料夾缺少治理 root marker: ${markerChoices || REPO_MARKERS.join(", ")}`);
    }
    const scanCoreDocs = scanAdapter.core_docs || CORE_DOCS;
    const scanRootDirectories = scanAdapter.root_directories || ROOT_DIRECTORIES;

    const nodes = [];
    const pathToNodeId = new Map();
    const logicalToNodeId = new Map();
    const sourceToRegistryNodeId = new Map();
    function register(node) {
      nodes.push(node);
      pathToNodeId.set(node.path, node.id);
      if (node.logical_path) logicalToNodeId.set(node.logical_path, node.id);
      if (["skill", "mcp", "agent", "workflow"].includes(node.type) && node.source_path) {
        sourceToRegistryNodeId.set(node.source_path, node.id);
      }
    }

    register({ id: "repo:root", type: "directory", label: "專案根目錄", path: "/", logical_path: "/", status: "repo-root", description: "專案根目錄" });
    for (const [relative, label, logicalPath] of scanRootDirectories) {
      if (!(await pathExists(rootHandle, relative, "directory"))) continue;
      register({
        id: nodeIdFor("dir", relative),
        type: "directory",
        label,
        path: `/${relative}`,
        logical_path: logicalPath,
        status: relative.startsWith("runtime/") ? "runtime-root" : "canonical-root",
        description: `${label}根目錄`,
        source_path: `/${relative}`,
      });
    }

    for (const relative of scanCoreDocs) {
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

    if (await pathExists(rootHandle, "runtime/catalog.json", "file")) {
      const catalogText = await readTextFromRepo(rootHandle, "runtime/catalog.json");
      const catalog = JSON.parse(catalogText);
      register({
        id: nodeIdFor("doc", "runtime/catalog.json"),
        type: "doc",
        label: "執行面目錄",
        path: "/runtime/catalog.json",
        logical_path: "/runtime/catalog.json",
        status: "runtime-doc",
        description: catalog.meta?.description || "記錄目前執行面投影結果的目錄檔。",
        source_path: "/runtime/catalog.json",
      });

      for (const entry of catalog.entries || []) {
        if (!entry?.runtime_path || !entry?.source_of_truth) continue;
        const entryType = entry.type || "resource";
        const descriptionParts = [
          `執行面${entryType}入口`,
          entry.hot_path ? "高頻路徑" : null,
          `正式來源：${entry.source_of_truth}`,
        ].filter(Boolean);
        register({
          id: nodeIdFor("runtime", `${entryType}:${entry.id}`),
          type: "runtime",
          label: entry.id,
          path: `/${entry.runtime_path}`,
          logical_path: `/${entry.runtime_path}`,
          status: entry.hot_path ? "runtime-hot-path" : "runtime-projection",
          description: descriptionParts.join(" · "),
          source_path: `/${entry.source_of_truth}`,
        });
      }
    }

    if (await pathExists(rootHandle, "registry/skills", "directory")) {
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
    }

    if (await pathExists(rootHandle, "registry/mcp", "directory")) {
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
    }

    if (await pathExists(rootHandle, "registry/agents", "directory")) {
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
    }

    if (await pathExists(rootHandle, "registry/workflow", "directory")) {
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
    }

    const edges = [];
    const brokenReferences = [];
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
      if (node.path.startsWith("/runtime/skills/")) addEdge(nodeIdFor("dir", "runtime/skills"), node.id, "contains");
      else if (node.path.startsWith("/runtime/agents/")) addEdge(nodeIdFor("dir", "runtime/agents"), node.id, "contains");
      else if (node.path.startsWith("/runtime/workflow/")) addEdge(nodeIdFor("dir", "runtime/workflow"), node.id, "contains");
      else if (node.path.startsWith("/registry/skills/")) addEdge(nodeIdFor("dir", "registry/skills"), node.id, "contains");
      else if (node.path.startsWith("/registry/mcp/")) addEdge(nodeIdFor("dir", "registry/mcp"), node.id, "contains");
      else if (node.path.startsWith("/registry/agents/")) addEdge(nodeIdFor("dir", "registry/agents"), node.id, "contains");
      else if (node.path.startsWith("/registry/workflow/")) addEdge(nodeIdFor("dir", "registry/workflow"), node.id, "contains");
      else addEdge("repo:root", node.id, "contains");
    });

    const markdownSources = [];
    for (const relative of scanCoreDocs) if (await pathExists(rootHandle, relative, "file")) markdownSources.push(relative);
    if (await pathExists(rootHandle, "registry/agents", "directory")) {
      for (const agentDir of await listChildDirectories(rootHandle, "registry/agents")) {
        const relative = `registry/agents/${agentDir}/AGENT.md`;
        if (await pathExists(rootHandle, relative, "file")) markdownSources.push(relative);
      }
    }
    if (await pathExists(rootHandle, "registry/workflow", "directory")) {
      for (const workflowDir of await listChildDirectories(rootHandle, "registry/workflow")) {
        for (const relative of [`registry/workflow/${workflowDir}/README.md`, `registry/workflow/${workflowDir}/WORKFLOW.md`]) {
          if (await pathExists(rootHandle, relative, "file")) markdownSources.push(relative);
        }
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
        else brokenReferences.push({
          source_id: sourceId,
          source_path: sourcePath,
          target: match[1],
          resolved_path: targetPath,
        });
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

    const runtimeCatalogId = pathToNodeId.get("/runtime/catalog.json");
    nodes.forEach((node) => {
      if (node.type !== "runtime") return;
      if (runtimeCatalogId) addEdge(runtimeCatalogId, node.id, "catalog_entry");
      const registryTargetId = sourceToRegistryNodeId.get(node.source_path);
      if (registryTargetId) addEdge(node.id, registryTargetId, "maps_to");
    });

    const counts = {};
    nodes.forEach((node) => { counts[node.type] = (counts[node.type] || 0) + 1; });
    const nonStructuralTouches = {};
    edges.forEach((edge) => {
      if (STRUCTURAL_EDGE_KINDS.has(edge.kind)) return;
      nonStructuralTouches[edge.from] = (nonStructuralTouches[edge.from] || 0) + 1;
      nonStructuralTouches[edge.to] = (nonStructuralTouches[edge.to] || 0) + 1;
    });
    const orphanNodeIds = nodes
      .filter((node) => node.type !== "directory" && node.id !== "repo:root" && !nonStructuralTouches[node.id])
      .map((node) => node.id)
      .sort();
    const brokenSourceIds = [...new Set(brokenReferences.map((item) => item.source_id))].sort();
    const nodeIndex = new Map(nodes.map((node) => [node.id, node]));
    const brokenSources = brokenSourceIds.map((sourceId) => {
      const sourceNode = nodeIndex.get(sourceId);
      const targets = brokenReferences
        .filter((item) => item.source_id === sourceId)
        .sort((a, b) => `${a.resolved_path} ${a.target}`.localeCompare(`${b.resolved_path} ${b.target}`))
        .map((item) => ({
          target: item.target,
          resolved_path: item.resolved_path,
        }));
      return {
        source_id: sourceId,
        source_label: sourceNode?.label || sourceId,
        source_path: sourceNode?.path || brokenReferences.find((item) => item.source_id === sourceId)?.source_path || "",
        count: targets.length,
        targets,
      };
    });
    return {
      meta: {
        generated_at: new Date().toISOString(),
        source_root: "/",
        version: 3,
        project_map_adapter: scanAdapter,
        project_map_adapters: PROJECT_MAP_ADAPTERS || [],
        root_validation: {
          valid: true,
          validation_mode: "project-map-adapter-marker",
          selected_adapter: scanAdapter.adapter_id || null,
          adapter_checks: adapterSelection.checks,
          governance_markers_present: markerInspection.present,
          governance_markers_missing: markerInspection.missing,
        },
      },
      counts,
      diagnostics: {
        broken_reference_count: brokenReferences.length,
        orphan_node_count: orphanNodeIds.length,
        broken_references: brokenReferences,
        broken_sources: brokenSources,
        broken_source_ids: brokenSourceIds,
        orphan_node_ids: orphanNodeIds,
      },
      nodes,
      edges,
    };
  }

  async function connectRepoDirectory() {
    if (!state.browserCanScan) {
      setRefreshState("error", "目前瀏覽器不支援頁內更新。");
      updateStatusCard("目前瀏覽器不支援 File System Access API，請改用 Python 重新生成。");
      return;
    }
    const handle = await window.showDirectoryPicker({ mode: "readwrite" });
    if (!(await hasHandlePermission(handle, "readwrite", true))) throw new Error("沒有取得讀寫權限。");
    await saveRepoHandle(handle);
    state.repoHandle = handle;
    state.repoHandleName = handle.name;
    setRefreshState("success", `已連結 ${handle.name}，可直接更新目前資料。`);
    updateStatusCard();
  }

  async function ensureRepoHandle(requestInteractive = false) {
    if (state.repoHandle) {
      const allowed = await hasHandlePermission(state.repoHandle, "readwrite", requestInteractive);
      if (allowed) return state.repoHandle;
    }
    if (!state.browserCanScan) return null;
    const stored = await loadRepoHandle();
    if (stored && (await hasHandlePermission(stored, "readwrite", requestInteractive))) {
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
      setRefreshState("error", "尚未連結專案根目錄。");
      updateStatusCard("尚未連結專案根目錄，無法執行頁內更新。");
      return;
    }
    state.refreshInFlight = true;
    setRefreshState("progress", "正在重新掃描專案並重建節點關係。");
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
      setRefreshState("idle", PAGE_MODE === "share-safe" ? "分享版僅提供唯讀瀏覽，不包含頁內重掃。" : "此瀏覽器只支援閱讀靜態 MAP。");
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

  function setupMapDragPan() {
    if (!mapWrapEl) return;
    let dragState = null;
    mapWrapEl.addEventListener("pointerdown", (event) => {
      if (event.button !== 0) return;
      if (event.target?.closest?.("button, a, input, select, textarea")) return;
      if (event.target?.closest?.("[data-map-node]")) return;
      dragState = {
        pointerId: event.pointerId,
        startX: event.clientX,
        startY: event.clientY,
        scrollLeft: mapWrapEl.scrollLeft,
        scrollTop: mapWrapEl.scrollTop,
        moved: false,
      };
      mapWrapEl.setPointerCapture?.(event.pointerId);
    });
    mapWrapEl.addEventListener("pointermove", (event) => {
      if (!dragState || dragState.pointerId !== event.pointerId) return;
      const deltaX = event.clientX - dragState.startX;
      const deltaY = event.clientY - dragState.startY;
      if (!dragState.moved && Math.hypot(deltaX, deltaY) < 4) return;
      dragState.moved = true;
      state.suppressNextMapClick = true;
      mapWrapEl.classList.add("is-dragging");
      mapWrapEl.scrollLeft = dragState.scrollLeft - deltaX;
      mapWrapEl.scrollTop = dragState.scrollTop - deltaY;
      event.preventDefault();
    });
    const finishDrag = (event) => {
      if (!dragState || dragState.pointerId !== event.pointerId) return;
      mapWrapEl.releasePointerCapture?.(event.pointerId);
      mapWrapEl.classList.remove("is-dragging");
      dragState = null;
    };
    mapWrapEl.addEventListener("pointerup", finishDrag);
    mapWrapEl.addEventListener("pointercancel", finishDrag);
    mapWrapEl.addEventListener("click", (event) => {
      if (!state.suppressNextMapClick) return;
      event.preventDefault();
      event.stopPropagation();
      state.suppressNextMapClick = false;
    }, true);
  }

  function setupControls() {
    loadSettings();
    applySettingsToControls();
    initializeGovernanceSelectors();
    if (governanceOutputPathEl) governanceOutputPathEl.value = defaultGovernanceOutputPath();
    setGovernanceInputDefaults();
    mastheadToggleEl?.addEventListener("click", () => { toggleMastheadCompact(); });
    workspaceToggleEl?.addEventListener("click", () => { toggleWorkspaceCompact(); });
    workspaceTabs.forEach((button) => {
      button.addEventListener("click", () => {
        state.workspaceEngaged = true;
        requestPanelFocus("workspace");
        setWorkspacePage(button.dataset.workspaceTab || "browse");
      });
    });
    workspacePreviewCards.forEach((button) => {
      button.addEventListener("click", () => {
        state.workspaceEngaged = true;
        requestPanelFocus("workspace");
        setWorkspacePage(button.dataset.workspacePreview || "browse");
      });
    });
    workspacePrevEl?.addEventListener("click", () => {
      state.workspaceEngaged = true;
      requestPanelFocus("workspace");
      moveWorkspacePage(-1);
    });
    workspaceNextEl?.addEventListener("click", () => {
      state.workspaceEngaged = true;
      requestPanelFocus("workspace");
      moveWorkspacePage(1);
    });
    workspaceShellEl?.addEventListener("pointerdown", (event) => {
      if (event.target?.closest?.("#workspace-toggle")) return;
      state.workspaceEngaged = true;
      requestPanelFocus("workspace");
    }, { passive: true });
    workspaceShellEl?.addEventListener("focusin", () => {
      state.workspaceEngaged = true;
      requestPanelFocus("workspace");
    });
    workspaceShellEl?.addEventListener("wheel", (event) => {
      if (Math.abs(event.deltaY) < 12) return;
      state.workspaceEngaged = true;
      requestPanelFocus(event.deltaY < 0 && window.scrollY < 180 ? "masthead" : "workspace");
    }, { passive: true });
    mapWrapEl?.addEventListener("scroll", () => {
      scheduleMinimapViewportUpdate();
      syncMastheadCompactState();
    }, { passive: true });
    setupMapDragPan();
    const panStepX = () => Math.max(120, mapWrapEl?.clientWidth ? mapWrapEl.clientWidth * 0.34 : 160);
    const panStepY = () => Math.max(80, mapWrapEl?.clientHeight ? mapWrapEl.clientHeight * 0.34 : 120);
    mapPanLeftEl?.addEventListener("click", () => { panMapViewport(-panStepX(), 0); });
    mapPanRightEl?.addEventListener("click", () => { panMapViewport(panStepX(), 0); });
    mapPanUpEl?.addEventListener("click", () => { panMapViewport(0, -panStepY()); });
    mapPanDownEl?.addEventListener("click", () => { panMapViewport(0, panStepY()); });
    mapZoomInEl?.addEventListener("click", () => { setMapZoom(state.mapZoom + 0.08); });
    mapZoomOutEl?.addEventListener("click", () => { setMapZoom(state.mapZoom - 0.08); });
    mapFitEl?.addEventListener("click", () => { centerMapViewport(); });
    mapResetEl?.addEventListener("click", () => { resetMapViewport(); });
    mapMinimapFrameEl?.addEventListener("click", (event) => {
      jumpMapViewportFromMinimap(event.clientX, event.clientY);
    });
    mapMinimapFrameEl?.addEventListener("keydown", (event) => {
      const horizontalStep = Math.max(80, mapWrapEl?.clientWidth ? mapWrapEl.clientWidth * 0.3 : 120);
      const verticalStep = Math.max(48, mapWrapEl?.clientHeight ? mapWrapEl.clientHeight * 0.3 : 72);
      if (event.key === "ArrowRight") {
        event.preventDefault();
        mapWrapEl?.scrollBy({ left: horizontalStep, top: 0, behavior: "smooth" });
        return;
      }
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        mapWrapEl?.scrollBy({ left: -horizontalStep, top: 0, behavior: "smooth" });
        return;
      }
      if (event.key === "ArrowDown") {
        event.preventDefault();
        mapWrapEl?.scrollBy({ left: 0, top: verticalStep, behavior: "smooth" });
        return;
      }
      if (event.key === "ArrowUp") {
        event.preventDefault();
        mapWrapEl?.scrollBy({ left: 0, top: -verticalStep, behavior: "smooth" });
      }
    });
    searchEl.addEventListener("input", () => { state.search = searchEl.value.trim().toLowerCase(); render(); });
    typeFilterEl.addEventListener("change", () => { state.type = typeFilterEl.value; render(); });
    mapModeEl.addEventListener("change", () => { state.mapMode = mapModeEl.value; saveSettings(); render(); });
    visualToneSliderEl?.addEventListener("input", () => {
      const nextTone = VISUAL_TONE_ORDER[Number(visualToneSliderEl.value)] || state.visualTone;
      setVisualTone(nextTone);
      saveSettings();
    });
    visualThemeSliderEl?.addEventListener("input", () => {
      const nextTheme = VISUAL_THEME_ORDER[Number(visualThemeSliderEl.value)] || state.visualTheme;
      setVisualTheme(nextTheme);
      saveSettings();
    });
    textScaleSliderEl?.addEventListener("input", () => {
      const nextScale = TEXT_SCALE_ORDER[Number(textScaleSliderEl.value)] || state.textScale;
      setTextScale(nextScale);
      saveSettings();
    });
    visualToneOptionEls.forEach((button) => {
      button.addEventListener("click", () => {
        const nextTone = button.dataset.visualToneOption || "";
        if (!VISUAL_TONES.has(nextTone)) return;
        setVisualTone(nextTone);
        saveSettings();
      });
      button.addEventListener("keydown", (event) => {
        const currentIndex = VISUAL_TONE_ORDER.indexOf(state.visualTone);
        if (event.key === "ArrowRight" || event.key === "ArrowDown") {
          event.preventDefault();
          const nextTone = VISUAL_TONE_ORDER[(currentIndex + 1) % VISUAL_TONE_ORDER.length];
          setVisualTone(nextTone, { focus: true });
          saveSettings();
          return;
        }
        if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
          event.preventDefault();
          const nextTone = VISUAL_TONE_ORDER[(currentIndex - 1 + VISUAL_TONE_ORDER.length) % VISUAL_TONE_ORDER.length];
          setVisualTone(nextTone, { focus: true });
          saveSettings();
          return;
        }
        if (event.key === "Home") {
          event.preventDefault();
          setVisualTone(VISUAL_TONE_ORDER[0], { focus: true });
          saveSettings();
          return;
        }
        if (event.key === "End") {
          event.preventDefault();
          setVisualTone(VISUAL_TONE_ORDER[VISUAL_TONE_ORDER.length - 1], { focus: true });
          saveSettings();
        }
      });
    });
    visualThemeOptionEls.forEach((button) => {
      button.addEventListener("click", () => {
        const nextTheme = button.dataset.visualThemeOption || "";
        if (!VISUAL_THEMES.has(nextTheme)) return;
        setVisualTheme(nextTheme);
        saveSettings();
      });
      button.addEventListener("keydown", (event) => {
        const currentIndex = VISUAL_THEME_ORDER.indexOf(state.visualTheme);
        if (event.key === "ArrowRight" || event.key === "ArrowDown") {
          event.preventDefault();
          const nextTheme = VISUAL_THEME_ORDER[(currentIndex + 1) % VISUAL_THEME_ORDER.length];
          setVisualTheme(nextTheme, { focus: true });
          saveSettings();
          return;
        }
        if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
          event.preventDefault();
          const nextTheme = VISUAL_THEME_ORDER[(currentIndex - 1 + VISUAL_THEME_ORDER.length) % VISUAL_THEME_ORDER.length];
          setVisualTheme(nextTheme, { focus: true });
          saveSettings();
          return;
        }
        if (event.key === "Home") {
          event.preventDefault();
          setVisualTheme(VISUAL_THEME_ORDER[0], { focus: true });
          saveSettings();
          return;
        }
        if (event.key === "End") {
          event.preventDefault();
          setVisualTheme(VISUAL_THEME_ORDER[VISUAL_THEME_ORDER.length - 1], { focus: true });
          saveSettings();
        }
      });
    });
    textScaleOptionEls.forEach((button) => {
      button.addEventListener("click", () => {
        const nextScale = button.dataset.textScaleOption || "";
        if (!TEXT_SCALES.has(nextScale)) return;
        setTextScale(nextScale);
        saveSettings();
      });
      button.addEventListener("keydown", (event) => {
        const currentIndex = TEXT_SCALE_ORDER.indexOf(state.textScale);
        if (event.key === "ArrowRight" || event.key === "ArrowDown") {
          event.preventDefault();
          const nextScale = TEXT_SCALE_ORDER[(currentIndex + 1) % TEXT_SCALE_ORDER.length];
          setTextScale(nextScale, { focus: true });
          saveSettings();
          return;
        }
        if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
          event.preventDefault();
          const nextScale = TEXT_SCALE_ORDER[(currentIndex - 1 + TEXT_SCALE_ORDER.length) % TEXT_SCALE_ORDER.length];
          setTextScale(nextScale, { focus: true });
          saveSettings();
          return;
        }
        if (event.key === "Home") {
          event.preventDefault();
          setTextScale(TEXT_SCALE_ORDER[0], { focus: true });
          saveSettings();
          return;
        }
        if (event.key === "End") {
          event.preventDefault();
          setTextScale(TEXT_SCALE_ORDER[TEXT_SCALE_ORDER.length - 1], { focus: true });
          saveSettings();
        }
      });
    });
    updateModeEl?.addEventListener("change", () => { state.updateMode = updateModeEl.value; saveSettings(); scheduleRefreshTimer(); updateStatusCard(); });
    [intervalDaysEl, intervalHoursEl, intervalMinutesEl].forEach((input) => input?.addEventListener("change", rememberIntervalInputs));
    [governanceAnalysisPathEl, governanceGlobalPathEl, governanceWorkspacePathEl, governanceRepoPathEl].forEach((input) => {
      input?.addEventListener("change", rememberGovernanceSettings);
      input?.addEventListener("blur", rememberGovernanceSettings);
    });
    governanceFunnelEl?.addEventListener("click", (event) => {
      const button = event.target?.closest?.("[data-governance-layer]");
      if (!button) return;
      state.activeGovernanceLayer = button.dataset.governanceLayer || "runtime";
      renderGovernanceFunnel(resolveGovernanceInPage());
    });
    linkRepoEl?.addEventListener("click", async () => {
      try { await connectRepoDirectory(); }
      catch (error) { updateStatusCard(error instanceof Error ? error.message : String(error)); }
    });
    refreshNowEl?.addEventListener("click", () => { refreshFromRepo("manual-button", true); });
    governanceResolveEl?.addEventListener("click", () => { void resolveGovernanceAction(); });
    governanceWriteEl?.addEventListener("click", () => { void writeGovernanceReports(); });
    mapMinimapToggleEl?.addEventListener("click", () => { toggleMinimapVisibility(); });
    tourStartEl?.addEventListener("click", () => { startTour(); });
    tourPrevEl?.addEventListener("click", () => { moveTour(-1); });
    tourNextEl?.addEventListener("click", () => { moveTour(1); });
    tourSkipEl?.addEventListener("click", () => { finishTour(); });
    tourCloseEl?.addEventListener("click", () => { finishTour(); });
    tourBackdropEl?.addEventListener("click", () => { finishTour(); });
  }

  setupControls();
  render();
  renderGovernanceResolution(resolveGovernanceInPage(), "已載入預設治理解析。");
  maybeAutoRefreshOnLoad();
  maybeStartTourOnFirstVisit();
})();
