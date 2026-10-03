// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

const portholeWebState = {
  loading: false,
  error: null,
  notice: null,
  mode: "view",
  bootstrap: null,
  selectedLabel: null,
  renderer: null,
  rendererRoot: null,
  skeletonSignature: null,
  ws: null,
  wsSessionId: null,
  wsConnected: false,
  wsReconnectTimer: null,
  wsReconnectDelayMs: 1000,
  wsReconnectAttempt: 0,
  wsHeartbeatTimer: null,
  wsHeartbeatInFlight: false,
  wsLastConnectedAt: "",
  wsLastPongAt: "",
  wsLastClose: null,
  wsLastError: null,
  socketRefreshTimer: null,
  socketRefreshSuppressUntil: 0,
  fastParticipantAgendaUpdatedAt: 0,
  orderingSequence: 0,
  bootstrapSeq: 0,
  actionSeq: 0,
  lastActionSeq: {},
  lastActionKeypath: {},
  socketRequestSequence: 0,
  socketPendingRequests: {},
  actionSequence: 0,
  fieldActionTimers: {},
  fieldValueMemory: {},
  refreshInFlight: false,
  refreshQueued: false,
  refreshPromise: null,
  shellSignature: null,
  expandedMenus: {},
  compactMenusActive: false,
  menuPreferences: {
    topExpansionStyle: "auto",
    bottomExpansionStyle: "auto",
    showTitles: true,
    criteriaText: "",
  },
  menuSettingsOpen: false,
  toolsPanelOpen: false,
  toolbarOverflowOpen: false,
  libraryOpen: false,
  libraryQuery: "",
  libraryMenuFilter: "",
  armedComponent: null,
  panelLayouts: {},
  activePanelDrag: null,
  activePanelResize: null,
  panelVisibility: {},
  panelCollapsed: {},
  inspectorDrafts: {},
  agentSetupDrafts: {},
  pendingLoad: null,
  // Settes naar Butler svarte uten at en modell var koblet til. Se
  // updateAssistantDegradationFromResult(). Overlever handlinger (i motsetning
  // til `notice`) fordi tilstanden gjelder hele oekta, ikke én melding.
  assistantDegradation: null,
  initialConfigurationLoadPayload: null,
  pendingAction: null,
  navigationStack: [],
  navigationPending: null,
  toolbarDetailsExpanded: false,
  productChromeRevealed: initialProductChromeRevealed(),
  edgeMenusSuppressed: true,
  configurationJSONOpen: false,
  notificationsExpanded: false,
  liveNotifications: [],
};

const bootstrapURL = "/browserhead/porthole/bootstrap";
const actionURL = "/browserhead/porthole/action";
const compactMenuViewportQuery = "(max-width: 980px)";
const menuPreferencesPersistenceKey = "porthole-webo-menu-preferences.v1";
const edgeMenuVisibilityPersistenceKey = "porthole-webo-edge-menus-visible.v1";
const edgeMenuPresentationLimit = 10;
const menuExpansionStyleOptions = ["auto", "stack", "radial"];
const websocketHeartbeatIntervalMs = 25000;
const websocketHeartbeatTimeoutMs = 7000;
const menuKeys = [
  "upperLeftMenu",
  "upperMidMenu",
  "upperRightMenu",
  "lowerLeftMenu",
  "lowerMidMenu",
  "lowerRightMenu",
];

const conferenceLibraryHighlights = [
  { name: "Conference Public Surface Claude", badge: "Claude", tone: "core" },
  { name: "Conference Participant Portal Claude", badge: "Claude", tone: "core" },
  { name: "Conference Participant Chat Claude", badge: "Claude", tone: "support" },
  { name: "Conference Control Tower Claude", badge: "Claude", tone: "core" },
  { name: "Conference Sponsor Follow-up Claude", badge: "Claude", tone: "support" },
  { name: "Conference Nearby Radar Claude", badge: "Claude", tone: "support" },
  { name: "Conference Control Tower", badge: "Kjerneflyt", tone: "core" },
  { name: "Conference Participant Portal Dashboard", badge: "Kjerneflyt", tone: "core" },
  { name: "Conference Demo Launcher", badge: "Demo-steg", tone: "support" },
  { name: "Conference Skeleton Component Library", badge: "Designsystem", tone: "support" },
  { name: "Conference Registration Setup", badge: "Cold start", tone: "support" },
  { name: "Conference Public Surface", badge: "Public opener", tone: "support" },
  { name: "Conference Participant Chat", badge: "Chat", tone: "support" },
  { name: "Conference Sponsor Follow-up", badge: "Sponsor", tone: "support" },
  { name: "Conference Participant Portal Preview", badge: "Advanced", tone: "support" },
  { name: "Conference Public Profile Editor", badge: "Profile", tone: "support" },
  { name: "Conference Public Profile", badge: "Profile", tone: "support" },
];
const conferenceHighlightByName = new Map(
  conferenceLibraryHighlights.map((entry, index) => [entry.name, { ...entry, rank: index }]),
);
const conferencePersonaOptions = [
  { id: "conference-admin-observer", label: "Organizer demo" },
  { id: "conference-participant", label: "Participant demo" },
  { id: "", label: "Live requester" },
];

function truthyQueryParam(value) {
  return ["1", "true", "yes"].includes(String(value || "").trim().toLowerCase());
}

function initialProductChromeRevealed() {
  try {
    return truthyQueryParam(new URLSearchParams(window.location.search).get("showProductChrome"));
  } catch {
    return false;
  }
}

function initializePendingLoadFromLocation() {
  let params;
  try {
    params = new URLSearchParams(window.location.search);
  } catch {
    return;
  }

  const configurationName = String(params.get("configurationName") || "").trim();
  const configurationEndpoint = String(params.get("configurationEndpoint") || "").trim();
  const configurationUUID = String(params.get("configurationUUID") || "").trim();
  const surfaceID = String(params.get("surfaceID") || "").trim();
  if (surfaceID) {
    const hasCompetingLookup = Boolean(configurationName || configurationEndpoint || configurationUUID);
    portholeWebState.initialConfigurationLoadPayload = {
      surfaceLaunch: {
        schema: "haven.surface-launch.v1",
        surfaceID,
        intent: "view",
        ...(hasCompetingLookup ? { ambiguous: true } : {}),
      },
    };
    return;
  }
  if (!configurationName && !configurationEndpoint && !configurationUUID) {
    return;
  }

  const lookup = {};
  if (configurationUUID) lookup.uuid = configurationUUID;
  if (configurationName) lookup.name = configurationName;
  if (configurationEndpoint) lookup.sourceCellEndpoint = configurationEndpoint;
  portholeWebState.initialConfigurationLoadPayload = {
    configurationLookup: lookup,
  };
}

async function initializePorthole() {
  await refreshBootstrap({ silent: false, shellOnly: true });
  const initialPayload = portholeWebState.initialConfigurationLoadPayload;
  portholeWebState.initialConfigurationLoadPayload = null;
  if (initialPayload) {
    await requestConfigurationNavigation(initialPayload, {
      closeMenus: true,
      closeLibrary: true,
      navigationMode: "push",
    });
  } else {
    // Keep the first paint independent of the comparatively expensive default
    // workbench projection. The ordinary bootstrap below restores the exact
    // same default workspace through the existing Resolver-authorized reads.
    void refreshBootstrap({ silent: true });
  }
}

const menuVisuals = {
  upperLeftMenu: { anchor: "upper-left", icon: "MENY", label: "Hovedmeny", centerAngle: 45 },
  upperMidMenu: { anchor: "upper-mid", icon: "FLAT", label: "Flater", centerAngle: 90 },
  upperRightMenu: { anchor: "upper-right", icon: "FLER", label: "Flere flater", centerAngle: 135 },
  lowerLeftMenu: { anchor: "lower-left", icon: "STYR", label: "Kontroll", centerAngle: -45 },
  lowerMidMenu: { anchor: "lower-mid", icon: "FAV", label: "Favoritter", centerAngle: -90 },
  lowerRightMenu: { anchor: "lower-right", icon: "ÅPNE", label: "Åpne og last inn", centerAngle: -135 },
};

const floatingPanelDefinitions = {
  components: { title: "Components", width: 300, height: 320, minWidth: 240, minHeight: 220 },
  elements: { title: "Elements", width: 340, height: 430, minWidth: 260, minHeight: 260 },
  inspector: { title: "Inspector", width: 380, height: 520, minWidth: 300, minHeight: 300 },
  agentSetup: { title: "Agent Setup", width: 380, height: 500, minWidth: 300, minHeight: 280 },
};
const floatingPanelPersistenceKey = "porthole-webo-floating-panels.v1";

document.addEventListener("DOMContentLoaded", () => {
  restoreFloatingPanelState();
  restoreMenuPreferences();
  restoreEdgeMenuVisibility();
  initializePendingLoadFromLocation();
  portholeWebState.compactMenusActive = usesCompactConvenienceMenus();
  wireHandlers();
  void initializePorthole();
});
window.addEventListener("beforeunload", closeWebSocket);
window.addEventListener("pageshow", handlePortholePageShow);
window.addEventListener("online", handlePortholePageShow);
document.addEventListener("visibilitychange", handlePortholeVisibilityChange);
window.addEventListener("resize", () => {
  refreshSkeletonLayoutContext();
  scheduleChatViewportLayout();
  const compactMenusActive = usesCompactConvenienceMenus();
  const compactModeChanged = compactMenusActive !== portholeWebState.compactMenusActive;
  portholeWebState.compactMenusActive = compactMenusActive;

  if (!isEditModeActive()) {
    if (compactModeChanged || hasExpandedMenus()) {
      render({ forceShell: true, preserveSkeletonDOM: true });
    }
    return;
  }
  clampFloatingPanelLayouts();
  persistFloatingPanelState();
  render({ forceShell: true, preserveSkeletonDOM: true });
});

function wireHandlers() {
  const root = document.getElementById("porthole-webo-app");
  if (!root) {
    return;
  }

  root.addEventListener("click", (event) => {
    const rawTarget = event.target;
    if (!(rawTarget instanceof HTMLElement)) {
      return;
    }

    const target = rawTarget.closest("[data-action]");
    if (!(target instanceof HTMLElement)) {
      if (rawTarget.closest(".menu-settings-popover, .toolbar-popover, .tools-panel")) {
        return;
      }
      if (handleCanvasSelectionClick(rawTarget)) {
        return;
      }
      const hadExpandedMenus = hasExpandedMenus();
      const hadMenuSettings = portholeWebState.menuSettingsOpen;
      const hadToolsPanel = portholeWebState.toolsPanelOpen;
      const hadToolbarOverflow = portholeWebState.toolbarOverflowOpen;
      collapseAllMenus({ render: false });
      closeMenuSettings({ render: false });
      portholeWebState.toolsPanelOpen = false;
      portholeWebState.toolbarOverflowOpen = false;
      if (hadExpandedMenus || hadMenuSettings || hadToolsPanel || hadToolbarOverflow) {
        render({ forceShell: true, preserveSkeletonDOM: true });
      }
      return;
    }

    const action = target.getAttribute("data-action") || "";

    if (action === "refresh") {
      void refreshBootstrap({ silent: false, reason: "manual-refresh" });
      return;
    }

    if (action === "toggle-toolbar-details") {
      portholeWebState.toolbarDetailsExpanded = !portholeWebState.toolbarDetailsExpanded;
      portholeWebState.toolbarOverflowOpen = false;
      render({ forceShell: true, preserveSkeletonDOM: true });
      return;
    }

    if (action === "toggle-tools-panel") {
      collapseAllMenus({ render: false });
      closeMenuSettings({ render: false });
      portholeWebState.toolbarOverflowOpen = false;
      portholeWebState.toolsPanelOpen = !portholeWebState.toolsPanelOpen;
      render({ forceShell: true, preserveSkeletonDOM: true });
      return;
    }

    if (action === "toggle-toolbar-overflow") {
      collapseAllMenus({ render: false });
      closeMenuSettings({ render: false });
      portholeWebState.toolsPanelOpen = false;
      portholeWebState.toolbarOverflowOpen = !portholeWebState.toolbarOverflowOpen;
      render({ forceShell: true, preserveSkeletonDOM: true });
      return;
    }

    if (action === "toggle-edge-menu-visibility") {
      setEdgeMenusVisible(portholeWebState.edgeMenusSuppressed);
      portholeWebState.toolsPanelOpen = false;
      render({ forceShell: true, preserveSkeletonDOM: true });
      return;
    }

    if (action === "close-configuration-json") {
      portholeWebState.configurationJSONOpen = false;
      render({ forceShell: true, preserveSkeletonDOM: true });
      return;
    }

    if (action === "open-copilot-chat") {
      const configuration = findCoPilotChatConfiguration();
      if (configuration) {
        void loadConfiguration(configuration, { closeMenus: true, closeLibrary: true });
      } else {
        portholeWebState.notice = null;
        portholeWebState.error = "Fant ikke Butler Chat i tilgjengelig katalog.";
        render({ forceShell: true, preserveSkeletonDOM: true });
      }
      return;
    }

    if (action === "toggle-notifications") {
      portholeWebState.notificationsExpanded = !portholeWebState.notificationsExpanded;
      render({ forceShell: true, preserveSkeletonDOM: true });
      return;
    }

    if (action === "navigation-back") {
      void navigateBackInHistory();
      return;
    }

    if (action === "navigation-jump") {
      const index = Number(target.getAttribute("data-navigation-index") || "-1");
      void navigateToHistoryIndex(index);
      return;
    }

    if (action === "switch-conference-persona") {
      const personaId = target.getAttribute("data-conference-persona-id") || "";
      switchConferencePersona(personaId);
      return;
    }

    if (action === "toggle-library") {
      collapseAllMenus({ render: false });
      closeMenuSettings({ render: false });
      portholeWebState.toolsPanelOpen = false;
      portholeWebState.toolbarOverflowOpen = false;
      portholeWebState.libraryOpen = !portholeWebState.libraryOpen;
      if (!portholeWebState.libraryOpen) {
        portholeWebState.libraryQuery = "";
        portholeWebState.libraryMenuFilter = "";
      } else {
        portholeWebState.libraryMenuFilter = "";
      }
      render({ forceShell: true, preserveSkeletonDOM: true });
      if (portholeWebState.libraryOpen) {
        focusLibraryQuerySoon();
      }
      return;
    }

    if (action === "close-library") {
      closeMenuSettings({ render: false });
      portholeWebState.libraryOpen = false;
      portholeWebState.libraryQuery = "";
      portholeWebState.libraryMenuFilter = "";
      render({ forceShell: true, preserveSkeletonDOM: true });
      return;
    }

    if (action === "open-library") {
      collapseAllMenus({ render: false });
      closeMenuSettings({ render: false });
      portholeWebState.libraryOpen = true;
      portholeWebState.libraryMenuFilter = "";
      render({ forceShell: true, preserveSkeletonDOM: true });
      focusLibraryQuerySoon();
      return;
    }

    if (action === "toggle-menu-settings") {
      toggleMenuSettings();
      return;
    }

    if (action === "arm-component") {
      const source = target.getAttribute("data-component-source") || "";
      const index = Number(target.getAttribute("data-component-index") || "-1");
      const item = resolveComponentItem(source, index);
      if (item) {
        portholeWebState.armedComponent = item;
        portholeWebState.libraryOpen = false;
        portholeWebState.libraryQuery = "";
        collapseAllMenus({ render: false });
        closeMenuSettings({ render: false });
        render({ forceShell: true, preserveSkeletonDOM: true });
      }
      return;
    }

    if (action === "cancel-armed-component") {
      portholeWebState.armedComponent = null;
      render({ forceShell: true, preserveSkeletonDOM: true });
      return;
    }

    if (action === "mode-view") {
      void runAction("editor.mode.set", { mode: "view" });
      return;
    }

    if (action === "mode-edit") {
      const accessNotice = resolveEditorAccessNotice();
      if (accessNotice && accessNotice.blocked) {
        portholeWebState.notice = null;
        portholeWebState.error = accessNotice.message;
        render({ forceShell: true, preserveSkeletonDOM: true });
        return;
      }
      void runAction("editor.mode.set", { mode: "edit" });
      return;
    }

    if (action === "editor-undo") {
      void runAction("editor.undo", null);
      return;
    }

    if (action === "editor-redo") {
      void runAction("editor.redo", null);
      return;
    }

    if (action === "editor-discard") {
      void runAction("editor.discard", null);
      return;
    }

    if (action === "editor-apply") {
      void runAction("editor.apply", null);
      return;
    }

    if (action === "reset-panel-layout") {
      resetFloatingPanelLayouts();
      render({ forceShell: true, preserveSkeletonDOM: true });
      return;
    }

    if (action === "toggle-panel-visibility") {
      const panelKey = target.getAttribute("data-panel-key") || "";
      togglePanelVisibility(panelKey);
      render({ forceShell: true, preserveSkeletonDOM: true });
      return;
    }

    if (action === "toggle-panel-collapse") {
      const panelKey = target.getAttribute("data-panel-key") || "";
      togglePanelCollapsed(panelKey);
      render({ forceShell: true, preserveSkeletonDOM: true });
      return;
    }

    if (action === "menu-toggle") {
      const menuKey = target.getAttribute("data-menu-key") || "";
      handleMenuPrimaryAction(menuKey);
      return;
    }

    if (action === "menu-add") {
      const menuKey = target.getAttribute("data-menu-key") || "";
      const index = Number(target.getAttribute("data-menu-index") || "-1");
      const config = getMenuConfiguration(menuKey, index);
      if (config) {
        void loadConfiguration(config, { closeMenus: true, closeLibrary: true });
      }
      return;
    }

    if (action === "menu-show-all") {
      const menuKey = target.getAttribute("data-menu-key") || "";
      openLibraryForMenu(menuKey);
      return;
    }

    if (action === "clear-library-menu-filter") {
      portholeWebState.libraryMenuFilter = "";
      render({ forceShell: true, preserveSkeletonDOM: true });
      focusLibraryQuerySoon();
      return;
    }

    if (action === "compact-load") {
      const index = Number(target.getAttribute("data-compact-index") || "-1");
      const configuration = getCompactConvenienceConfigurations()[index] || null;
      if (configuration) {
        void loadConfiguration(configuration, { closeMenus: true, closeLibrary: true });
      }
      return;
    }

    if (action === "library-load") {
      const index = Number(target.getAttribute("data-library-index") || "-1");
      const entry = getFilteredLibraryEntries()[index] || null;
      if (entry && entry.configuration) {
        void loadConfiguration(entry.configuration, { closeMenus: true, closeLibrary: true });
      }
      return;
    }

    if (action === "insert-component-slot") {
      const targetPath = target.getAttribute("data-target-path") || "root";
      if (portholeWebState.armedComponent) {
        void runAction("editor.component.insert", {
          component: portholeWebState.armedComponent,
          placement: { targetPath },
        });
      }
      return;
    }

    if (action === "select-reference") {
      const label = target.getAttribute("data-label") || "";
      portholeWebState.selectedLabel = label || null;
      render();
      return;
    }

    if (action === "select-node") {
      const path = target.getAttribute("data-path") || "";
      if (path) {
        void runAction("editor.selection.set", { path });
      }
      return;
    }

    if (action === "remove-reference") {
      if (portholeWebState.selectedLabel) {
        void runAction("removeReference", { label: portholeWebState.selectedLabel });
      }
      return;
    }

    if (action === "delete-selected-node") {
      void deleteSelectedNodeFromWorkingSkeleton();
      return;
    }

    if (action === "copy-working-configuration") {
      void copyCurrentCellConfiguration("working");
      return;
    }

    if (action === "copy-committed-configuration") {
      void copyCurrentCellConfiguration("committed");
      return;
    }

    if (action === "copy-debug-snapshot") {
      void copyCurrentDebugSnapshot();
      return;
    }

    if (action === "copy-selected-node-raw") {
      const path = target.getAttribute("data-path") || "";
      if (path) {
        void copySelectedNodeRaw(path);
      }
      return;
    }

    if (action === "copy-selected-reference-state") {
      const label = target.getAttribute("data-label") || "";
      if (label) {
        void copySelectedReferenceState(label);
      }
      return;
    }

    if (action === "set-parameter") {
      const path = target.getAttribute("data-path") || "";
      const fieldKey = target.getAttribute("data-field-key") || "";
      const valueKind = target.getAttribute("data-value-kind") || "string";
      if (path && fieldKey) {
        void applyInspectorFieldDraft({
          path,
          fieldKey,
          valueKind,
          scope: "parameter",
        });
      }
      return;
    }

    if (action === "clear-parameter") {
      const path = target.getAttribute("data-path") || "";
      const fieldKey = target.getAttribute("data-field-key") || "";
      if (path && fieldKey) {
        void clearInspectorField({
          path,
          fieldKey,
          scope: "parameter",
        });
      }
      return;
    }

    if (action === "add-parameter") {
      const path = target.getAttribute("data-path") || "";
      const fieldKey = target.getAttribute("data-field-key") || "";
      const valueKind = target.getAttribute("data-value-kind") || "string";
      const defaultValue = target.getAttribute("data-default-value") || "";
      if (path && fieldKey) {
        void addInspectorField({
          path,
          fieldKey,
          valueKind,
          scope: "parameter",
          defaultValue,
        });
      }
      return;
    }

    if (action === "set-modifier") {
      const path = target.getAttribute("data-path") || "";
      const fieldKey = target.getAttribute("data-field-key") || "";
      const valueKind = target.getAttribute("data-value-kind") || "string";
      if (path && fieldKey) {
        void applyInspectorFieldDraft({
          path,
          fieldKey,
          valueKind,
          scope: "modifier",
        });
      }
      return;
    }

    if (action === "clear-modifier") {
      const path = target.getAttribute("data-path") || "";
      const fieldKey = target.getAttribute("data-field-key") || "";
      if (path && fieldKey) {
        void clearInspectorField({
          path,
          fieldKey,
          scope: "modifier",
        });
      }
      return;
    }

    if (action === "add-modifier") {
      const path = target.getAttribute("data-path") || "";
      const fieldKey = target.getAttribute("data-field-key") || "";
      const valueKind = target.getAttribute("data-value-kind") || "string";
      const defaultValue = target.getAttribute("data-default-value") || "";
      if (path && fieldKey) {
        void addInspectorField({
          path,
          fieldKey,
          valueKind,
          scope: "modifier",
          defaultValue,
        });
      }
      return;
    }

    if (action === "agent-setup-apply-route") {
      const label = target.getAttribute("data-label") || "";
      if (label) {
        void syncAgentSetupRoute(label);
      }
      return;
    }

    if (action === "agent-setup-apply-prompts") {
      const label = target.getAttribute("data-label") || "";
      if (label) {
        void syncAgentSetupPrompts(label);
      }
      return;
    }

    if (action === "agent-setup-load-session-key") {
      const label = target.getAttribute("data-label") || "";
      if (label) {
        void syncAgentSetupSessionKey(label, { persist: false });
      }
      return;
    }

    if (action === "agent-setup-save-key") {
      const label = target.getAttribute("data-label") || "";
      if (label) {
        void syncAgentSetupSessionKey(label, { persist: true });
      }
      return;
    }

    if (action === "agent-setup-clear-key") {
      const label = target.getAttribute("data-label") || "";
      if (label) {
        void clearAgentSetupSessionKey(label);
      }
      return;
    }

    if (action === "agent-setup-invoke") {
      const label = target.getAttribute("data-label") || "";
      if (label) {
        void invokeAgentSetup(label);
      }
      return;
    }
  });

  root.addEventListener("input", (event) => {
    handleEditorInputEvent(event.target);
  });

  root.addEventListener("change", (event) => {
    handleEditorInputEvent(event.target);
  });

  root.addEventListener("pointerdown", (event) => {
    const rawTarget = event.target;
    if (!(rawTarget instanceof HTMLElement)) {
      return;
    }
    if (rawTarget.closest("[data-action]")) {
      return;
    }
    const resizeHandle = rawTarget.closest("[data-panel-resize-handle='true']");
    if (resizeHandle instanceof HTMLElement) {
      const panelKey = resizeHandle.getAttribute("data-panel-key") || "";
      if (!panelKey || !floatingPanelDefinitions[panelKey]) {
        return;
      }
      const panelElement = root.querySelector(`.floating-panel-window[data-panel-key="${cssEscape(panelKey)}"]`);
      if (!(panelElement instanceof HTMLElement)) {
        return;
      }
      beginFloatingPanelResize(event, panelKey, panelElement);
      return;
    }
    const handle = rawTarget.closest("[data-panel-drag-handle='true']");
    if (!(handle instanceof HTMLElement)) {
      return;
    }
    const panelKey = handle.getAttribute("data-panel-key") || "";
    if (!panelKey || !floatingPanelDefinitions[panelKey]) {
      return;
    }
    const panelElement = root.querySelector(`.floating-panel-window[data-panel-key="${cssEscape(panelKey)}"]`);
    if (!(panelElement instanceof HTMLElement)) {
      return;
    }
    beginFloatingPanelDrag(event, panelKey, panelElement);
  });

  root.addEventListener("keydown", (event) => {
    const rawTarget = event.target;
    if (!(rawTarget instanceof HTMLElement)) {
      return;
    }

    const edgeMenu = rawTarget.closest("[role='menu'][data-edge-menu-key]");
    if (edgeMenu instanceof HTMLElement) {
      const menuKey = edgeMenu.getAttribute("data-edge-menu-key") || "";
      const items = Array.from(edgeMenu.querySelectorAll("[role='menuitem']:not(:disabled)"))
        .filter((item) => item instanceof HTMLElement);
      const currentIndex = items.indexOf(rawTarget);
      if (["ArrowRight", "ArrowDown", "ArrowLeft", "ArrowUp", "Home", "End"].includes(event.key) && items.length > 0) {
        event.preventDefault();
        let nextIndex = currentIndex;
        if (event.key === "Home") {
          nextIndex = 0;
        } else if (event.key === "End") {
          nextIndex = items.length - 1;
        } else {
          const direction = event.key === "ArrowRight" || event.key === "ArrowDown" ? 1 : -1;
          nextIndex = currentIndex < 0 ? 0 : (currentIndex + direction + items.length) % items.length;
        }
        items[nextIndex].focus({ preventScroll: true });
        return;
      }
      if (event.key === "Escape") {
        event.preventDefault();
        collapseAllMenus({ render: false });
        render({ forceShell: true, preserveSkeletonDOM: true });
        focusEdgeMenuTriggerSoon(menuKey);
        return;
      }
    }

    if (event.key === "Escape") {
      const hadOpenUI = hasExpandedMenus() || portholeWebState.menuSettingsOpen ||
        portholeWebState.toolsPanelOpen || portholeWebState.toolbarOverflowOpen;
      if (hadOpenUI) {
        event.preventDefault();
        collapseAllMenus({ render: false });
        closeMenuSettings({ render: false });
        portholeWebState.toolsPanelOpen = false;
        portholeWebState.toolbarOverflowOpen = false;
        render({ forceShell: true, preserveSkeletonDOM: true });
      }
      return;
    }

    if (event.key !== "Enter" && event.key !== " ") {
      return;
    }

    const card = rawTarget.closest("[data-action-card='library-load']");
    if (!(card instanceof HTMLElement)) {
      return;
    }

    event.preventDefault();
    card.click();
  });
}

function handleEditorInputEvent(rawTarget) {
  if (!(rawTarget instanceof HTMLInputElement || rawTarget instanceof HTMLSelectElement || rawTarget instanceof HTMLTextAreaElement)) {
    return;
  }
  if (rawTarget.getAttribute("data-menu-setting") === "topExpansionStyle") {
    updateMenuPreference("topExpansionStyle", rawTarget.value || "auto");
    return;
  }
  if (rawTarget.getAttribute("data-menu-setting") === "bottomExpansionStyle") {
    updateMenuPreference("bottomExpansionStyle", rawTarget.value || "auto");
    return;
  }
  if (rawTarget.getAttribute("data-menu-setting-toggle") === "showTitles") {
    updateMenuPreference("showTitles", rawTarget instanceof HTMLInputElement ? rawTarget.checked : true);
    return;
  }
  if (rawTarget.getAttribute("data-menu-setting-text") === "criteriaText") {
    updateMenuPreference("criteriaText", rawTarget.value || "");
    return;
  }
  if (rawTarget.getAttribute("data-library-query") === "true") {
    portholeWebState.libraryQuery = rawTarget.value || "";
    render({ forceShell: true, preserveSkeletonDOM: true });
    return;
  }
  if (rawTarget.getAttribute("data-inspector-draft") === "true") {
    const draftKey = rawTarget.getAttribute("data-draft-key") || "";
    if (draftKey) {
      portholeWebState.inspectorDrafts[draftKey] = rawTarget.value || "";
    }
    return;
  }
  if (rawTarget.getAttribute("data-agent-setup-draft") === "true") {
    const label = rawTarget.getAttribute("data-agent-label") || "";
    const fieldKey = rawTarget.getAttribute("data-agent-field") || "";
    if (label && fieldKey) {
      setAgentSetupDraft(label, fieldKey, rawTarget.value || "");
    }
  }
}

function nextPortholeOrderingSequence(kind) {
  // Bootstrap and action IDs share one monotonic clock; independent counters
  // cannot tell which operation actually started first.
  const sequence = (Number(portholeWebState.orderingSequence) || 0) + 1;
  portholeWebState.orderingSequence = sequence;
  if (kind === "bootstrap") {
    portholeWebState.bootstrapSeq = sequence;
  } else if (kind === "action") {
    portholeWebState.actionSeq = sequence;
  }
  return sequence;
}

async function refreshBootstrap({ silent, shellOnly = false }) {
  if (portholeWebState.refreshInFlight) {
    portholeWebState.refreshQueued = true;
    if (portholeWebState.refreshPromise && typeof portholeWebState.refreshPromise.then === "function") {
      await portholeWebState.refreshPromise;
    }
    return;
  }

  const bootstrapSeq = nextPortholeOrderingSequence("bootstrap");
  portholeWebState.refreshInFlight = true;
  const refreshPromise = (async () => {
    if (!silent) {
      portholeWebState.loading = true;
      portholeWebState.error = null;
      // Refresh progress belongs to the targeted live region/status badge.
      // It must not invalidate the shell signature or rebuild shell chrome.
      render({ forceShell: false, preserveSkeletonDOM: true });
    }

    try {
      const previousShellSignature = buildShellSignature();
      const refreshStartedAt = Date.now();
      const payload = await requestBootstrapPayload({ shellOnly });
      const nextBootstrap = preserveRecentCellActionStatesDuringRefresh(
        portholeWebState.bootstrap,
        preserveFastParticipantAgendaStateDuringRefresh(
          portholeWebState.bootstrap,
          normalizeBootstrap(payload),
          refreshStartedAt
        ),
        bootstrapSeq
      );
      assertValidBootstrapSkeleton(nextBootstrap);
      portholeWebState.bootstrap = nextBootstrap;
      const requesterWarning = resolveRequesterPersonaWarning(portholeWebState.bootstrap);
      if (requesterWarning) {
        portholeWebState.notice = requesterWarning;
      }
      if (portholeWebState.pendingLoad) {
        portholeWebState.pendingLoad = null;
        if (!requesterWarning) {
          portholeWebState.notice = null;
        }
      }
      if (portholeWebState.pendingAction) {
        portholeWebState.pendingAction = null;
      }
      portholeWebState.mode = portholeWebState.bootstrap.editorState.mode;
      if (portholeWebState.mode !== "edit") {
        portholeWebState.armedComponent = null;
        portholeWebState.activePanelDrag = null;
      } else {
        ensureFloatingPanelLayouts();
        ensureFloatingPanelPresentationState();
      }
      portholeWebState.error = null;
      clearSkeletonValidationDiagnostic();
      ensureWebSocket();

      const references = getReferences();
      if (references.length > 0) {
        const selectedExists = references.some((entry) => entry.label === portholeWebState.selectedLabel);
        if (!selectedExists) {
          portholeWebState.selectedLabel = references[0].label;
        }
      } else {
        portholeWebState.selectedLabel = null;
      }

      const nextShellSignature = buildShellSignature();
      const shellChanged = previousShellSignature !== nextShellSignature;
      if (silent && !shellChanged) {
        renderSkeletonCanvas();
      } else {
        render({ forceShell: shellChanged, preserveSkeletonDOM: true });
      }
    } catch (error) {
      portholeWebState.error = error instanceof Error ? error.message : String(error);
      if (portholeWebState.pendingLoad) {
        portholeWebState.pendingLoad = null;
      }
      if (error && error.preserveRenderedSkeleton === true && portholeWebState.bootstrap) {
        renderSkeletonValidationDiagnostic(portholeWebState.error);
      } else {
        render({ forceShell: true, preserveSkeletonDOM: true });
      }
    } finally {
      portholeWebState.loading = false;
      if (portholeWebState.error && !portholeWebState.bootstrap) {
        render({ forceShell: true, preserveSkeletonDOM: true });
      }
      portholeWebState.refreshInFlight = false;
      if (!portholeWebState.error && portholeWebState.bootstrap) {
        render({ forceShell: false, preserveSkeletonDOM: true });
      }
      if (portholeWebState.refreshQueued) {
        portholeWebState.refreshQueued = false;
        await refreshBootstrap({ silent: true });
      }
    }
  })();

  portholeWebState.refreshPromise = refreshPromise;
  try {
    await refreshPromise;
  } finally {
    if (portholeWebState.refreshPromise === refreshPromise) {
      portholeWebState.refreshPromise = null;
    }
  }
}

async function runAction(keypath, payload) {
  const normalizedKeypath = normalizeActionKeypath(keypath);
  const beforeOpenAction = normalizedKeypath === "addConfiguration"
    ? normalizeConfigurationBeforeOpenAction(payload)
    : null;
  const actionPayload = beforeOpenAction
    ? payloadWithoutConfigurationBeforeOpenAction(payload)
    : payload;
  if (shouldDeferActionWhileLoading(normalizedKeypath)) {
    portholeWebState.notice = pendingLoadActionNotice();
    portholeWebState.error = null;
    updateStatusLiveRegion();
    await waitForPendingLoadCompletion();
    return runAction(keypath, payload);
  }
  const actionSequence = portholeWebState.actionSequence + 1;
  portholeWebState.actionSequence = actionSequence;
  const actionIsCurrent = () => portholeWebState.actionSequence === actionSequence;
  const navigationContext = normalizedKeypath === "addConfiguration"
    ? prepareConfigurationNavigationContext(actionPayload)
    : null;
  const pendingAction = createPendingActionDescriptor(normalizedKeypath, actionPayload);
  const rollbackState = captureOptimisticRollbackState(normalizedKeypath);
  portholeWebState.notice = null;
  portholeWebState.error = null;
  if (pendingAction) {
    portholeWebState.pendingAction = pendingAction;
  }
  applyOptimisticActionState(normalizedKeypath, actionPayload);
  render({ forceShell: true, preserveSkeletonDOM: true });

  try {
    if (beforeOpenAction) {
      const beforeOpenResult = await requestActionPayload(
        beforeOpenAction.keypath,
        beforeOpenAction.payload,
        resolveActionTimeoutMs(beforeOpenAction.keypath)
      );
      if (!actionIsCurrent()) {
        return;
      }
      const beforeOpenFeedback = resolveActionFeedback(
        beforeOpenAction.keypath,
        beforeOpenAction.payload,
        beforeOpenResult
      );
      if (beforeOpenFeedback.error) {
        throw new Error(beforeOpenFeedback.error);
      }
    }
    const actionResult = await requestActionPayload(
      keypath,
      actionPayload,
      resolveActionTimeoutMs(normalizedKeypath)
    );
    if (!actionIsCurrent()) {
      return;
    }
    // Sequence the committed result, not the request start. A bootstrap that
    // began while the action was still on the wire may contain pre-action
    // state and must therefore sort before this result.
    const actionSeq = nextPortholeOrderingSequence("action");
    const appliedActionState = applyActionResultState(normalizedKeypath, actionResult, actionPayload, actionSeq);
    const actionFeedback = resolveActionFeedback(normalizedKeypath, actionPayload, actionResult);
    if (actionFeedback.error) {
      throw new Error(actionFeedback.error);
    }
    applyPostActionFieldState(normalizedKeypath, actionResult, actionPayload);
    const portholeUINotice = applyPortholeUIRequest(actionResult);
    if (actionResult && typeof actionResult === "object" && actionResult.editorState) {
      const current = portholeWebState.bootstrap || {};
      const nextEditorState = normalizeEditorState(actionResult.editorState, current.editor || {});
      const nextBootstrap = {
        ...current,
        editorState: nextEditorState,
        editor: normalizeLegacyEditor(nextEditorState),
      };
      assertValidBootstrapSkeleton(nextBootstrap);
      portholeWebState.bootstrap = nextBootstrap;
      portholeWebState.mode = nextEditorState.mode;
      if (portholeWebState.mode !== "edit") {
        portholeWebState.armedComponent = null;
      }
    }
    if (normalizedKeypath === "editor.component.insert") {
      portholeWebState.armedComponent = null;
    }
    if (normalizedKeypath === "addConfiguration") {
      commitConfigurationNavigationContext(navigationContext);
    }
    if (appliedActionState && isResponsiveParticipantAgendaMutation(normalizedKeypath, actionPayload)) {
      const now = Date.now();
      portholeWebState.fastParticipantAgendaUpdatedAt = now;
      portholeWebState.socketRefreshSuppressUntil = Math.max(
        portholeWebState.socketRefreshSuppressUntil || 0,
        now + 5000
      );
    }
    portholeWebState.pendingAction = null;
    portholeWebState.notice = portholeUINotice || actionFeedback.notice;
    // State-only actions update the mounted renderer in place. Replacing the
    // host after their HTTP response can detach the next control before a
    // caller awaiting that response gets to click it. Configuration navigation
    // is the explicit action boundary that may install a new skeleton host.
    const replaceSkeleton = shouldReplaceSkeletonAfterAction(normalizedKeypath);
    render({
      forceShell: true,
      preserveSkeletonDOM: !replaceSkeleton,
      replaceSkeleton,
    });
    if (
      shouldForceBootstrapReload(normalizedKeypath, actionPayload, appliedActionState) ||
      (!portholeWebState.wsConnected && !appliedActionState && !isEventDrivenRuntimeAction(normalizedKeypath))
    ) {
      await refreshBootstrap({ silent: true });
      if (normalizedKeypath === "addConfiguration") {
        window.setTimeout(() => {
          void refreshBootstrap({ silent: true });
        }, 750);
      }
    }
  } catch (error) {
    if (!actionIsCurrent()) {
      return;
    }
    restoreOptimisticRollbackState(rollbackState);
    portholeWebState.error = error instanceof Error ? error.message : String(error);
    portholeWebState.pendingAction = null;
    if (normalizedKeypath === "addConfiguration") {
      portholeWebState.pendingLoad = null;
      portholeWebState.navigationPending = null;
    }
    if (error && error.preserveRenderedSkeleton === true && portholeWebState.bootstrap) {
      try {
        renderSkeletonCanvas();
      } catch (_) {
        // Preserve the current last-known-good DOM and report the rejected update.
      }
      renderSkeletonValidationDiagnostic(portholeWebState.error);
    } else {
      render({ forceShell: true, preserveSkeletonDOM: true });
    }
  }
}

function shouldReplaceSkeletonAfterAction(normalizedKeypath) {
  return normalizedKeypath === "addConfiguration";
}

function shouldDeferActionWhileLoading(normalizedKeypath) {
  if (!portholeWebState.pendingLoad) {
    return false;
  }
  return normalizedKeypath !== "addConfiguration";
}

function pendingLoadActionNotice() {
  const pendingName = portholeWebState.pendingLoad && portholeWebState.pendingLoad.name
    ? portholeWebState.pendingLoad.name
    : "preview";
  return `Venter paa at ${pendingName} er oppdatert via flow foer handlingen kan kjoeres.`;
}

async function waitForPendingLoadCompletion(timeoutMs = 15000) {
  const startedAt = Date.now();
  while (portholeWebState.pendingLoad) {
    if (Date.now() - startedAt >= timeoutMs) {
      throw new Error(pendingLoadActionNotice());
    }
    await new Promise((resolve) => window.setTimeout(resolve, 25));
  }
}

function applyPostActionFieldState(keypath, actionResult, _payload) {
  const renderer = portholeWebState.renderer;
  if (!renderer || typeof renderer.setFieldValueByTarget !== "function") {
    return;
  }

  if (keypath === "chatHub.clearComposer" || keypath === "clearComposer") {
    forgetPersistentFieldValue("chatHub.setComposer");
    renderer.setFieldValueByTarget("chatHub.setComposer", "", false);
    return;
  }

  if (
    keypath === "chatHub.assistant.analyzeDraft" ||
    keypath === "assistant.analyzeDraft" ||
    keypath === "chatHub.prompt.submit" ||
    keypath === "prompt.submit"
  ) {
    const result = actionResultPayload(actionResult);
    const ok = result && typeof result === "object" && result.ok === true && result.status !== "prompt_required";
    if (ok) {
      forgetPersistentFieldValue("chatHub.setComposer");
      renderer.setFieldValueByTarget("chatHub.setComposer", "", false);
    }
    return;
  }

  if ((keypath === "chatHub.sendComposedMessage" || keypath === "sendComposedMessage") && actionResult && typeof actionResult === "object") {
    const ok = actionResult.ok === true || actionResult.status === "message_sent";
    if (ok) {
      forgetPersistentFieldValue("chatHub.setComposer");
      renderer.setFieldValueByTarget("chatHub.setComposer", "", false);
    }
  }
}

function applyPortholeUIRequest(actionResult) {
  const normalizedResult = normalizeActionResultValue(
    actionResult && typeof actionResult === "object" && Object.prototype.hasOwnProperty.call(actionResult, "result")
      ? actionResult.result
      : actionResult
  );
  const request = normalizedResult && typeof normalizedResult === "object" && normalizedResult.portholeUI && typeof normalizedResult.portholeUI === "object"
    ? normalizedResult.portholeUI
    : null;
  if (!request) {
    return null;
  }

  if (request.showProductChrome === true || request.showChrome === true || request.revealChrome === true) {
    portholeWebState.productChromeRevealed = true;
  }
  if (request.hideProductChrome === true || request.hideChrome === true) {
    portholeWebState.productChromeRevealed = false;
  }
  if (request.showToolbarDetails === true || request.expandToolbar === true) {
    portholeWebState.productChromeRevealed = true;
    portholeWebState.toolbarDetailsExpanded = true;
  }
  if (request.hideToolbarDetails === true || request.collapseToolbar === true) {
    portholeWebState.toolbarDetailsExpanded = false;
  }
  if (request.toggleToolbarDetails === true) {
    portholeWebState.productChromeRevealed = true;
    portholeWebState.toolbarDetailsExpanded = !portholeWebState.toolbarDetailsExpanded;
  }
  if (request.openMenuSettings === true) {
    portholeWebState.productChromeRevealed = true;
    portholeWebState.toolbarDetailsExpanded = true;
    portholeWebState.menuSettingsOpen = true;
  }
  if (request.closeMenuSettings === true) {
    portholeWebState.menuSettingsOpen = false;
  }
  if (request.showEdgeMenus === true || request.showMenus === true) {
    portholeWebState.productChromeRevealed = true;
    setEdgeMenusVisible(true);
  }
  if (request.hideEdgeMenus === true || request.hideMenus === true) {
    setEdgeMenusVisible(false);
  }
  if (request.toggleEdgeMenus === true) {
    portholeWebState.productChromeRevealed = true;
    setEdgeMenusVisible(portholeWebState.edgeMenusSuppressed);
  }
  if (typeof request.menuCriteria === "string") {
    updateMenuPreference("criteriaText", request.menuCriteria);
  }
  if (request.loadConfiguration === true || request.autoLoadConfiguration === true) {
    const configuration = resolveConfigurationForPortholeUIRequest(request);
    if (configuration) {
      void loadConfiguration(configuration, { closeMenus: true, closeLibrary: true });
      return typeof request.notice === "string" && request.notice.trim()
        ? request.notice.trim()
        : `Laster ${resolveConfigurationDisplayName(configuration)} i Porthole.`;
    }
    const lookupPayload = resolveConfigurationNavigationPayloadForPortholeUIRequest(request);
    if (lookupPayload) {
      const lookupName = resolveConfigurationLookupDisplayName(request, lookupPayload);
      void requestConfigurationNavigation(lookupPayload, {
        closeMenus: true,
        closeLibrary: true,
        navigationMode: "push",
      });
      return typeof request.notice === "string" && request.notice.trim()
        ? request.notice.trim()
        : `Laster ${lookupName} i Porthole.`;
    }
    portholeWebState.productChromeRevealed = true;
    portholeWebState.libraryOpen = true;
    if (typeof request.libraryQuery === "string") {
      portholeWebState.libraryQuery = request.libraryQuery;
    } else if (typeof request.configurationName === "string") {
      portholeWebState.libraryQuery = request.configurationName;
    }
    focusLibraryQuerySoon();
    return "Jeg fant ikke en entydig flate å laste direkte, så Library er åpnet med samme søk.";
  }
  if (request.openLibrary === true) {
    portholeWebState.productChromeRevealed = true;
    portholeWebState.libraryOpen = true;
    if (typeof request.libraryQuery === "string") {
      portholeWebState.libraryQuery = request.libraryQuery;
    }
    focusLibraryQuerySoon();
  }
  if (request.closeLibrary === true) {
    portholeWebState.libraryOpen = false;
    portholeWebState.libraryQuery = "";
  }
  if (typeof request.openURL === "string" && request.openURL.trim()) {
    const url = request.openURL.trim();
    if (isSafePortholeInternalURL(url)) {
      window.location.assign(url);
      return typeof request.notice === "string" && request.notice.trim()
        ? request.notice.trim()
        : "Åpner dokumentasjon.";
    }
    return "Kun interne Porthole-lenker kan åpnes direkte fra chatten.";
  }
  if (request.collapseMenus === true) {
    portholeWebState.expandedMenus = {};
  }
  if (Array.isArray(request.expandMenus) && request.expandMenus.length > 0) {
    portholeWebState.productChromeRevealed = true;
    setEdgeMenusVisible(true);
    const next = {};
    request.expandMenus.forEach((menuKey) => {
      const normalizedMenuKey = String(menuKey || "").trim();
      if (menuKeys.includes(normalizedMenuKey)) {
        next[normalizedMenuKey] = true;
      }
    });
    if (Object.keys(next).length > 0) {
      portholeWebState.expandedMenus = next;
    }
  }
  if (request.showConfigurationJSON === true || request.openConfigurationJSON === true) {
    portholeWebState.productChromeRevealed = true;
    portholeWebState.toolbarDetailsExpanded = true;
    portholeWebState.configurationJSONOpen = true;
  }
  if (typeof request.notice === "string" && request.notice.trim()) {
    return request.notice.trim();
  }
  return null;
}

function isSafePortholeInternalURL(url) {
  return url.startsWith("/") && !url.startsWith("//") && !url.includes("\\");
}

function resolveConfigurationForPortholeUIRequest(request) {
  if (!request || typeof request !== "object") {
    return null;
  }
  const name = typeof request.configurationName === "string" ? request.configurationName.trim().toLowerCase() : "";
  const endpoint = typeof request.sourceCellEndpoint === "string" ? request.sourceCellEndpoint.trim().toLowerCase() : "";
  const query = typeof request.libraryQuery === "string" ? request.libraryQuery.trim().toLowerCase() : "";
  const configurations = getLibraryConfigurations();
  const exactNameAndEndpoint = configurations.filter((configuration) => {
    const configurationName = typeof configuration.name === "string" ? configuration.name.trim().toLowerCase() : "";
    const discovery = configuration.discovery && typeof configuration.discovery === "object" ? configuration.discovery : {};
    const configurationEndpoint = typeof discovery.sourceCellEndpoint === "string" ? discovery.sourceCellEndpoint.trim().toLowerCase() : "";
    return (!name || configurationName === name) && (!endpoint || configurationEndpoint === endpoint);
  });
  if (exactNameAndEndpoint.length === 1) {
    return exactNameAndEndpoint[0];
  }
  if (name) {
    const exactName = configurations.filter((configuration) =>
      typeof configuration.name === "string" && configuration.name.trim().toLowerCase() === name
    );
    if (exactName.length === 1) {
      return exactName[0];
    }
  }
  if (endpoint) {
    const exactEndpoint = configurations.filter((configuration) => {
      const discovery = configuration.discovery && typeof configuration.discovery === "object" ? configuration.discovery : {};
      return typeof discovery.sourceCellEndpoint === "string" && discovery.sourceCellEndpoint.trim().toLowerCase() === endpoint;
    });
    if (exactEndpoint.length === 1) {
      return exactEndpoint[0];
    }
  }
  if (query) {
    const previousQuery = portholeWebState.libraryQuery;
    portholeWebState.libraryQuery = query;
    const entries = getFilteredLibraryEntries();
    portholeWebState.libraryQuery = previousQuery;
    if (entries.length === 1 && entries[0].configuration) {
      return entries[0].configuration;
    }
  }
  return null;
}

function resolveConfigurationNavigationPayloadForPortholeUIRequest(request) {
  if (!request || typeof request !== "object") {
    return null;
  }
  const explicitLookup = normalizeConfigurationNavigationPayload(request);
  if (explicitLookup) {
    return explicitLookup;
  }
  const lookup = {};
  if (typeof request.configurationName === "string" && request.configurationName.trim().length > 0) {
    lookup.name = request.configurationName.trim();
  }
  if (typeof request.sourceCellEndpoint === "string" && request.sourceCellEndpoint.trim().length > 0) {
    lookup.sourceCellEndpoint = request.sourceCellEndpoint.trim();
  }
  return Object.keys(lookup).length > 0 ? { configurationLookup: lookup } : null;
}

function resolveConfigurationLookupDisplayName(request, payload) {
  if (request && typeof request.notice === "string" && request.notice.trim()) {
    return request.notice.trim();
  }
  const lookup = payload && typeof payload === "object" && payload.configurationLookup && typeof payload.configurationLookup === "object"
    ? payload.configurationLookup
    : null;
  if (lookup && typeof lookup.name === "string" && lookup.name.trim().length > 0) {
    return lookup.name.trim();
  }
  if (request && typeof request.configurationName === "string" && request.configurationName.trim().length > 0) {
    return request.configurationName.trim();
  }
  return "Konfigurasjon";
}

function removeRenderedEdgeMenus() {
  if (typeof document === "undefined") {
    return;
  }
  document.querySelectorAll(".edge-menu-anchor").forEach((node) => {
    node.remove();
  });
}

function captureOptimisticRollbackState(keypath) {
  const normalized = String(keypath || "").trim();
  if (!normalized.startsWith("editor.")) {
    return null;
  }
  return {
    bootstrap: portholeWebState.bootstrap ? deepCloneValue(portholeWebState.bootstrap) : null,
    mode: portholeWebState.mode,
    armedComponent: portholeWebState.armedComponent ? deepCloneValue(portholeWebState.armedComponent) : null,
    activePanelDrag: portholeWebState.activePanelDrag ? { ...portholeWebState.activePanelDrag } : null,
  };
}

function restoreOptimisticRollbackState(snapshot) {
  if (!snapshot) {
    return;
  }
  portholeWebState.bootstrap = snapshot.bootstrap;
  portholeWebState.mode = snapshot.mode || "view";
  portholeWebState.armedComponent = snapshot.armedComponent;
  portholeWebState.activePanelDrag = snapshot.activePanelDrag;
}

function normalizeActionKeypath(keypath) {
  return String(keypath || "").trim();
}

function normalizeConfigurationBeforeOpenAction(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    return null;
  }
  const action = payload.beforeOpenAction;
  if (!action || typeof action !== "object" || Array.isArray(action)) {
    return null;
  }
  const keypath = typeof action.keypath === "string" ? action.keypath.trim() : "";
  if (!keypath || keypath === "addConfiguration") {
    return null;
  }
  return {
    keypath,
    payload: Object.prototype.hasOwnProperty.call(action, "payload") ? action.payload : null,
  };
}

function payloadWithoutConfigurationBeforeOpenAction(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    return payload;
  }
  if (!Object.prototype.hasOwnProperty.call(payload, "beforeOpenAction")) {
    return payload;
  }
  const next = { ...payload };
  delete next.beforeOpenAction;
  return next;
}

function resolveNestedDispatchActionKeypath(keypath, payload) {
  const normalized = String(keypath || "").trim();
  if (!normalized.endsWith(".dispatchAction") || !payload || typeof payload !== "object" || Array.isArray(payload)) {
    return "";
  }
  return typeof payload.keypath === "string" ? payload.keypath.trim() : "";
}

function isFastParticipantAgendaAction(keypath) {
  const normalized = String(keypath || "").trim();
  return (
    normalized.startsWith("conferenceParticipantShell.agenda.") ||
    normalized.startsWith("conferenceParticipantPreviewShell.agenda.")
  );
}

function isFastParticipantAgendaDispatchAction(keypath, payload) {
  const normalized = String(keypath || "").trim();
  if (
    normalized !== "conferenceParticipantShell.dispatchAction" &&
    normalized !== "conferenceParticipantPreviewShell.dispatchAction"
  ) {
    return false;
  }
  const nestedKeypath = resolveNestedDispatchActionKeypath(normalized, payload);
  return nestedKeypath === "agenda.toggleSavedSession" || nestedKeypath === "agenda.toggleSelectedSessionSaved";
}

function isFastParticipantAgendaMutation(keypath, payload = null) {
  return isFastParticipantAgendaAction(keypath) || isFastParticipantAgendaDispatchAction(keypath, payload);
}

function isArendalsukaParticipantAgendaMutation(keypath) {
  return String(keypath || "").trim() === "arendalsukaParticipant.participant.toggleSavedSession";
}

function isResponsiveParticipantAgendaMutation(keypath, payload = null) {
  const normalized = String(keypath || "").trim();
  return isFastParticipantAgendaMutation(normalized, payload) ||
    isArendalsukaParticipantAgendaMutation(normalized);
}

function isChatHubRuntimeAction(keypath) {
  const normalized = String(keypath || "").trim();
  if (!normalized) {
    return false;
  }
  if (normalized.startsWith("chatHub.")) {
    return true;
  }
  const firstSegment = normalized.split(".")[0];
  return [
    "assistant",
    "ui",
    "poll",
    "meeting",
    "idea",
    "todo",
    "project",
    "reminder",
    "agent",
    "capability",
    "capabilityRequest",
    "drop",
  ].includes(firstSegment) ||
    [
      "setComposer",
      "clearComposer",
      "sendComposedMessage",
      "invite",
      "acceptInvite",
      "declineInvite",
      "reportMessage",
      "blockUser",
      "unblockUser",
      "absorbChat",
      "releaseAbsorbedChat",
    ].includes(normalized);
}

function isEventDrivenRuntimeAction(keypath) {
  const normalized = String(keypath || "").trim();
  return isChatHubRuntimeAction(normalized) ||
    isFastParticipantAgendaMutation(normalized) ||
    isArendalsukaParticipantAgendaMutation(normalized) ||
    isAIAssistantThreadRuntimeAction(normalized);
}

function isAIAssistantThreadRuntimeAction(keypath) {
  const normalized = String(keypath || "").trim();
  return normalized === "aiAssistantThread.postUserMessage" ||
    normalized === "aiAssistantThread.receiveAssistantTurn" ||
    normalized === "aiAssistantThread.submitUserDecision" ||
    normalized === "aiAssistantThread.dismissPendingRequest" ||
    normalized === "aiAssistantThread.refresh";
}

function resolveStateLabelForAction(keypath, state) {
  const normalized = String(keypath || "").trim();
  const label = normalized.split(".")[0];
  if (label && state && typeof state === "object" && state[label]) {
    return label;
  }
  if (isChatHubRuntimeAction(normalized) && state && typeof state === "object" && state.chatHub) {
    return "chatHub";
  }
  return label;
}

function resolveFastParticipantAgendaResult(keypath, actionResult, payload = null) {
  const envelopeResult = actionResult && typeof actionResult === "object" && Object.prototype.hasOwnProperty.call(actionResult, "result")
    ? actionResult.result
    : actionResult;

  if (isFastParticipantAgendaDispatchAction(keypath, payload) &&
      envelopeResult &&
      typeof envelopeResult === "object" &&
      !Array.isArray(envelopeResult) &&
      Object.prototype.hasOwnProperty.call(envelopeResult, "result")) {
    return envelopeResult.result;
  }

  return envelopeResult;
}

function applyActionResultState(keypath, actionResult, payload = null, actionSeq = null) {
  const bootstrap = portholeWebState.bootstrap;
  if (!bootstrap || !bootstrap.state || typeof bootstrap.state !== "object") {
    return false;
  }

  const label = resolveStateLabelForAction(keypath, bootstrap.state);
  if (!label) {
    return false;
  }

  const labelState = bootstrap.state[label];
  if (!labelState || typeof labelState !== "object") {
    return false;
  }

  const normalizedActionSeq = Number(actionSeq);
  const latestActionSeq = Number(portholeWebState.lastActionSeq[label]) || 0;
  if (
    shouldPreserveRecentCellActionState(actionResult) &&
    normalizedActionSeq > 0 &&
    normalizedActionSeq < latestActionSeq
  ) {
    return false;
  }

  if (label === "chatHub") {
    const didApply = applyChatHubActionResult(labelState, actionResult, keypath);
    if (didApply) {
      rememberRecentCellActionState(label, keypath, actionResult, actionSeq);
    }
    return didApply;
  }

  if (label === "aiAssistantThread") {
    return false;
  }

  const cellState = labelState.state;
  if (!cellState || typeof cellState !== "object") {
    return false;
  }

  if (applyConferenceParticipantPartialActionResult(label, cellState, keypath, actionResult)) {
    rememberRecentCellActionState(label, keypath, actionResult, actionSeq);
    return true;
  }

  if (applyArendalsukaParticipantAgendaResult(label, cellState, keypath, actionResult)) {
    rememberRecentCellActionState(label, keypath, actionResult, actionSeq);
    return true;
  }

  if (!isFastParticipantAgendaMutation(keypath, payload)) {
    if (isMermaidRenderKeypath(keypath)) {
      const didApply = applyMermaidActionResultState(labelState, actionResult, payload);
      if (didApply) {
        rememberRecentCellActionState(label, keypath, actionResult, actionSeq);
      }
      return didApply;
    }
    const didApply = applyFullShellStateActionResult(labelState, actionResult, keypath);
    if (didApply) {
      rememberRecentCellActionState(label, keypath, actionResult, actionSeq);
    }
    return didApply;
  }

  const normalizedResult = normalizeActionResultValue(
    resolveFastParticipantAgendaResult(keypath, actionResult, payload)
  );
  if (!normalizedResult || typeof normalizedResult !== "object" || Array.isArray(normalizedResult)) {
    return false;
  }

  cellState.program = normalizedResult;
  if (label === "conferenceParticipantShell" || label === "conferenceParticipantPreviewShell") {
    if (!cellState.navigation || typeof cellState.navigation !== "object") {
      cellState.navigation = {};
    }
    cellState.navigation.activeTab = "agenda";
  }
  rememberRecentCellActionState(label, keypath, actionResult, actionSeq);
  return true;
}

function applyArendalsukaParticipantAgendaResult(label, cellState, keypath, actionResult) {
  if (label !== "arendalsukaParticipant" || !isArendalsukaParticipantAgendaMutation(keypath)) {
    return false;
  }
  const result = actionResultPayload(actionResult);
  if (!result || typeof result !== "object" || Array.isArray(result) || result.responseMode !== "ack") {
    return false;
  }
  const sessionID = String(result.sessionID || "").trim();
  if (!sessionID || typeof result.isSaved !== "boolean") {
    return false;
  }

  const savedSessionIDs = Array.isArray(result.savedSessionIDs)
    ? result.savedSessionIDs.map(String)
    : [];
  cellState.agenda = mergeObjects(cellState.agenda, {
    savedSessionIDs,
    savedSessionCount: Number(result.savedSessionCount || savedSessionIDs.length),
  });

  if (cellState.program && Array.isArray(cellState.program.visibleSessionCards)) {
    cellState.program.visibleSessionCards = cellState.program.visibleSessionCards.map((card) => (
      card && String(card.id || "") === sessionID
        ? {
            ...card,
            isSaved: result.isSaved,
            savedLabel: String(result.savedLabel || (result.isSaved ? "Lagret" : "Ikke lagret")),
            agendaActionLabel: String(result.agendaActionLabel || (result.isSaved ? "Fjern fra agenda" : "Legg til agenda")),
          }
        : card
    ));
  }

  const privateRows = cellState.agenda && Array.isArray(cellState.agenda.timelineRows)
    ? cellState.agenda.timelineRows.filter((row) => row && row.agendaKind !== "official-session")
    : [];
  const existingOfficialRows = cellState.agenda && Array.isArray(cellState.agenda.timelineRows)
    ? cellState.agenda.timelineRows.filter((row) => row && row.agendaKind === "official-session" && String(row.id || "") !== sessionID)
    : [];
  const officialRows = result.isSaved && result.timelineRow && typeof result.timelineRow === "object"
    ? [...existingOfficialRows, result.timelineRow]
    : existingOfficialRows;
  cellState.agenda.timelineRows = [...officialRows, ...privateRows].sort((left, right) => {
    const leftTime = String(left?.timeLine || left?.subtitle || "");
    const rightTime = String(right?.timeLine || right?.subtitle || "");
    return leftTime.localeCompare(rightTime, "nb") || String(left?.title || "").localeCompare(String(right?.title || ""), "nb");
  });
  return true;
}

function applyConferenceParticipantPartialActionResult(label, cellState, keypath, actionResult) {
  if (label !== "conferenceParticipantShell" && label !== "conferenceParticipantPreviewShell") {
    return false;
  }
  const normalizedKeypath = String(keypath || "").trim();
  const normalizedResult = actionResultPayload(actionResult);
  if (!normalizedResult || typeof normalizedResult !== "object" || Array.isArray(normalizedResult)) {
    return false;
  }

  if (normalizedKeypath.includes(".matchmaking.")) {
    cellState.matches = normalizedResult;
    ensureConferenceParticipantActiveTab(cellState, "people");
    return true;
  }

  return false;
}

function ensureConferenceParticipantActiveTab(cellState, activeTab) {
  if (!cellState || typeof cellState !== "object" || !activeTab) {
    return;
  }
  if (!cellState.navigation || typeof cellState.navigation !== "object" || Array.isArray(cellState.navigation)) {
    cellState.navigation = {};
  }
  cellState.navigation.activeTab = activeTab;
}

function actionResultPayload(actionResult) {
  return normalizeActionResultValue(
    actionResult && typeof actionResult === "object" && Object.prototype.hasOwnProperty.call(actionResult, "result")
      ? actionResult.result
      : actionResult
  );
}

function applyChatHubActionResult(labelState, actionResult, keypath) {
  const normalizedResult = actionResultPayload(actionResult);
  if (!normalizedResult || typeof normalizedResult !== "object" || Array.isArray(normalizedResult)) {
    return false;
  }
  if (normalizedResult.ok === false) {
    return false;
  }

  if (!labelState.state || typeof labelState.state !== "object" || Array.isArray(labelState.state)) {
    labelState.state = {};
  }
  const cellState = labelState.state;
  if (!cellState || typeof cellState !== "object") {
    return false;
  }

  let didApply = false;
  const normalizedKeypath = String(keypath || "").trim();

  const thread = normalizedResult.thread && typeof normalizedResult.thread === "object"
    ? normalizedResult.thread
    : looksLikeChatThread(normalizedResult)
      ? normalizedResult
      : null;
  if (thread) {
    applyChatHubThreadState(cellState, thread);
    didApply = true;
  }

  if (normalizedResult.ui && typeof normalizedResult.ui === "object") {
    applyChatHubUIState(cellState, normalizedResult.ui);
    didApply = true;
  }

  const surface = normalizedResult.surface && typeof normalizedResult.surface === "object"
    ? normalizedResult.surface
    : normalizedResult.componentSurface && typeof normalizedResult.componentSurface === "object"
      ? normalizedResult.componentSurface
      : null;
  if (surface) {
    applyChatHubSurfaceState(cellState, surface);
    didApply = true;
  }

  if (normalizedResult.suggestion && typeof normalizedResult.suggestion === "object") {
    applyChatHubSuggestionState(cellState, normalizedResult.suggestion);
    didApply = true;
  }

  if (normalizedResult.assistantState && typeof normalizedResult.assistantState === "object") {
    cellState.assistantState = mergeObjects(cellState.assistantState, normalizedResult.assistantState);
    cellState.assistant = mergeObjects(cellState.assistant, normalizedResult.assistantState);
    didApply = true;
  }

  if (normalizedResult.composer && typeof normalizedResult.composer === "object") {
    cellState.composer = mergeObjects(cellState.composer, normalizedResult.composer);
    didApply = true;
  }

  if (Array.isArray(normalizedResult.intentCandidates)) {
    cellState.assistant = mergeObjects(cellState.assistant, { intentCandidates: normalizedResult.intentCandidates });
    didApply = true;
  }
  if (Array.isArray(normalizedResult.resourceMatches)) {
    cellState.assistant = mergeObjects(cellState.assistant, { resourceMatches: normalizedResult.resourceMatches });
    didApply = true;
  }
  if (Array.isArray(normalizedResult.assistantProviders) || Array.isArray(normalizedResult.providers)) {
    cellState.assistant = mergeObjects(cellState.assistant, {
      providerMatches: normalizedResult.assistantProviders || normalizedResult.providers,
    });
    didApply = true;
  }
  if (normalizedResult.providerRecommendation && typeof normalizedResult.providerRecommendation === "object") {
    cellState.assistant = mergeObjects(cellState.assistant, {
      providerRecommendation: normalizedResult.providerRecommendation,
    });
    updateAssistantDegradationFromResult(normalizedResult);
    didApply = true;
  }
  if (normalizedResult.resourceQuery && typeof normalizedResult.resourceQuery === "object") {
    cellState.assistant = mergeObjects(cellState.assistant, {
      resourceQuery: normalizedResult.resourceQuery,
    });
    didApply = true;
  } else if (
    Object.prototype.hasOwnProperty.call(normalizedResult, "answer") ||
    Object.prototype.hasOwnProperty.call(normalizedResult, "citations")
  ) {
    cellState.assistant = mergeObjects(cellState.assistant, {
      resourceQuery: {
        query: normalizedResult.query || "",
        answer: normalizedResult.answer || "",
        citations: Array.isArray(normalizedResult.citations) ? normalizedResult.citations : [],
        resource: normalizedResult.resource || null,
      },
    });
    didApply = true;
  }

  if (normalizedResult.docsRAG && typeof normalizedResult.docsRAG === "object") {
    cellState.docsRAG = mergeObjects(cellState.docsRAG, normalizedResult.docsRAG);
    didApply = true;
  } else if (
    normalizedKeypath === "chatHub.docsRAG.askRAG" &&
    (Object.prototype.hasOwnProperty.call(normalizedResult, "answer") ||
      Object.prototype.hasOwnProperty.call(normalizedResult, "citations") ||
      Object.prototype.hasOwnProperty.call(normalizedResult, "status"))
  ) {
    const docsRAG = cellState.docsRAG && typeof cellState.docsRAG === "object" ? { ...cellState.docsRAG } : {};
    docsRAG.resourceQuery = mergeObjects(docsRAG.resourceQuery, {
      query: normalizedResult.query || docsRAG.query || "",
      answer: normalizedResult.answer || "",
      citations: Array.isArray(normalizedResult.citations) ? normalizedResult.citations : [],
      resource: normalizedResult.resource || null,
      status: normalizedResult.status || "",
    });
    docsRAG.answer = normalizedResult.answer || "";
    docsRAG.citations = Array.isArray(normalizedResult.citations) ? normalizedResult.citations : [];
    docsRAG.summary = normalizedResult.answer
      ? "RAG svarte på spørsmålet."
      : normalizedResult.status === "query_required"
        ? "Skriv et spørsmål først."
        : (docsRAG.summary || "Ingen RAG-svar ennå.");
    cellState.docsRAG = docsRAG;
    didApply = true;
  }

  if (normalizedResult.pollDraft && typeof normalizedResult.pollDraft === "object") {
    cellState.pollDraft = normalizedResult.pollDraft;
    didApply = true;
  }
  if (Array.isArray(normalizedResult.polls)) {
    cellState.polls = normalizedResult.polls;
    didApply = true;
  } else if (normalizedResult.poll && typeof normalizedResult.poll === "object") {
    cellState.polls = upsertById(Array.isArray(cellState.polls) ? cellState.polls : [], normalizedResult.poll);
    didApply = true;
  }

  if (normalizedResult.inviteDraft && typeof normalizedResult.inviteDraft === "object") {
    cellState.inviteDraft = normalizedResult.inviteDraft;
    didApply = true;
  }

  if (normalizedResult.blockedUsers) {
    cellState.blockedUsers = normalizedResult.blockedUsers;
    didApply = true;
  }
  if (normalizedResult.moderationStatus) {
    cellState.moderationStatus = typeof normalizedResult.moderationStatus === "object"
      ? normalizedResult.moderationStatus
      : mergeObjects(cellState.moderationStatus, { status: String(normalizedResult.moderationStatus) });
    didApply = true;
  }

  if (normalizedResult.module && typeof normalizedResult.module === "object") {
    const workbench = cellState.workbench && typeof cellState.workbench === "object" ? { ...cellState.workbench } : {};
    workbench.modules = upsertById(Array.isArray(workbench.modules) ? workbench.modules : [], normalizedResult.module);
    workbench.moduleCount = workbench.modules.length;
    cellState.workbench = workbench;
    cellState.workbenchModules = upsertById(Array.isArray(cellState.workbenchModules) ? cellState.workbenchModules : [], normalizedResult.module);
    didApply = true;
  }

  if (normalizedResult.draft && typeof normalizedResult.draft === "object") {
    applyChatHubDraftResult(cellState, normalizedKeypath, normalizedResult.draft);
    didApply = true;
  }

  if (applyChatHubOnboardingResult(cellState, normalizedKeypath, normalizedResult)) {
    didApply = true;
  }

  return didApply;
}

function applyChatHubOnboardingResult(cellState, keypath, normalizedResult) {
  if (!String(keypath || "").trim().startsWith("chatHub.onboarding.")) {
    return false;
  }

  const nestedState = normalizedResult.state && typeof normalizedResult.state === "object" && !Array.isArray(normalizedResult.state)
    ? normalizedResult.state
    : null;
  if (nestedState) {
    cellState.onboarding = deepCloneValue(nestedState);
    return true;
  }

  const onboardingKeys = [
    "schema",
    "status",
    "dialogMode",
    "script",
    "availableScripts",
    "serviceAssociations",
    "targetCellEndpoint",
    "actorReceivesPrivateValues",
    "sideEffectsRequireClick",
    "privacySummary",
    "currentStep",
    "missingFields",
    "progress",
    "lastDryRun",
    "answerDraft",
  ];
  const patch = {};
  onboardingKeys.forEach((key) => {
    if (Object.prototype.hasOwnProperty.call(normalizedResult, key)) {
      patch[key] = deepCloneValue(normalizedResult[key]);
    }
  });
  if (!Object.keys(patch).length) {
    return false;
  }

  cellState.onboarding = mergeObjects(cellState.onboarding, patch);
  return true;
}

function applyChatHubThreadState(cellState, thread) {
  cellState.currentThread = thread;
  if (Array.isArray(thread.messages)) {
    cellState.messages = thread.messages;
  }
  if (thread.composer && typeof thread.composer === "object") {
    cellState.composer = thread.composer;
  } else if (thread.composerBody != null) {
    cellState.composer = mergeObjects(cellState.composer, { body: String(thread.composerBody) });
  } else if (thread.requesterComposer != null) {
    cellState.composer = mergeObjects(cellState.composer, { body: String(thread.requesterComposer) });
  } else if (thread.id) {
    cellState.composer = mergeObjects(cellState.composer, { threadID: thread.id });
  }
  if (Array.isArray(cellState.threads)) {
    cellState.threads = upsertById(cellState.threads, thread);
  } else {
    cellState.threads = [thread];
  }
}

function applyChatHubUIState(cellState, ui) {
  cellState.ui = mergeObjects(cellState.ui, ui);
  [
    "componentSurfaces",
    "activeComponentSurfaceID",
    "minimizedComponentSurfaces",
    "lastMotionEvent",
    "absorbedChats",
    "activeAbsorbedChatID",
    "combinedChatView",
  ].forEach((key) => {
    if (Object.prototype.hasOwnProperty.call(ui, key)) {
      cellState[key] = ui[key];
    }
  });
}

function applyChatHubSurfaceState(cellState, surface) {
  const ui = cellState.ui && typeof cellState.ui === "object" ? { ...cellState.ui } : {};
  ui.componentSurfaces = upsertById(Array.isArray(ui.componentSurfaces) ? ui.componentSurfaces : [], surface);
  if (surface.state === "expanded" || surface.state === "pinned") {
    ui.activeComponentSurfaceID = surface.id || ui.activeComponentSurfaceID;
  }
  if (surface.state === "minimized") {
    const ids = Array.isArray(ui.minimizedComponentSurfaceIDs) ? ui.minimizedComponentSurfaceIDs.slice() : [];
    if (surface.id && !ids.includes(surface.id)) {
      ids.push(surface.id);
    }
    ui.minimizedComponentSurfaceIDs = ids;
  }
  applyChatHubUIState(cellState, ui);
}

function applyChatHubSuggestionState(cellState, suggestion) {
  const assistant = cellState.assistant && typeof cellState.assistant === "object" ? { ...cellState.assistant } : {};
  assistant.latestSuggestion = suggestion;
  cellState.assistant = assistant;
  cellState.assistantState = mergeObjects(cellState.assistantState, { latestSuggestion: suggestion });
  cellState.assistantSuggestions = upsertById(Array.isArray(cellState.assistantSuggestions) ? cellState.assistantSuggestions : [], suggestion);
}

function applyChatHubDraftResult(cellState, keypath, draft) {
  const workbench = cellState.workbench && typeof cellState.workbench === "object" ? { ...cellState.workbench } : {};
  if (keypath.endsWith(".idea.title") || keypath.endsWith(".idea.content")) {
    workbench.ideaDraft = mergeObjects(workbench.ideaDraft, draft);
  } else if (keypath.endsWith(".todo.title") || keypath.endsWith(".todo.note") || keypath.endsWith(".todo.dueAtText") || keypath.endsWith(".todo.assigneeUUID")) {
    workbench.todoDraft = mergeObjects(workbench.todoDraft, draft);
  } else if (keypath.endsWith(".project.title") || keypath.endsWith(".project.description") || keypath.endsWith(".project.membersText")) {
    workbench.projectDraft = mergeObjects(workbench.projectDraft, draft);
  } else if (keypath.endsWith(".reminder.title") || keypath.endsWith(".reminder.scheduledAtText") || keypath.endsWith(".reminder.scope")) {
    workbench.reminderDraft = mergeObjects(workbench.reminderDraft, draft);
  } else if (keypath.endsWith(".agent.review.actionID") || keypath.endsWith(".agent.review.reason") || keypath.endsWith(".agent.review.argumentsText") || keypath.endsWith(".agent.review.signatureBase64")) {
    workbench.agentReviewDraft = mergeObjects(workbench.agentReviewDraft, draft);
  } else if (keypath.endsWith(".meeting.title") || keypath.endsWith(".meeting.targetProfileID") || keypath.endsWith(".meeting.proposedTimesText")) {
    workbench.meetingDraft = mergeObjects(workbench.meetingDraft, draft);
  }
  cellState.workbench = workbench;
}

function looksLikeChatThread(value) {
  return Boolean(
    value &&
    typeof value === "object" &&
    typeof value.id === "string" &&
    (Array.isArray(value.messages) || Array.isArray(value.participants) || value.invitationStatusByUUID)
  );
}

function mergeObjects(current, update) {
  const base = current && typeof current === "object" && !Array.isArray(current) ? current : {};
  const next = update && typeof update === "object" && !Array.isArray(update) ? update : {};
  return { ...base, ...next };
}

function upsertById(list, item) {
  if (!item || typeof item !== "object") {
    return Array.isArray(list) ? list : [];
  }
  const id = typeof item.id === "string" ? item.id : null;
  if (!id) {
    return Array.isArray(list) ? list.concat([item]) : [item];
  }
  const next = Array.isArray(list) ? list.slice() : [];
  const index = next.findIndex((entry) => entry && entry.id === id);
  if (index >= 0) {
    next[index] = item;
  } else {
    next.push(item);
  }
  return next;
}

function applyFullShellStateActionResult(labelState, actionResult, keypath = "") {
  const normalizedResult = normalizeActionResultValue(
    actionResult && typeof actionResult === "object" && Object.prototype.hasOwnProperty.call(actionResult, "result")
      ? actionResult.result
      : actionResult
  );
  if (!normalizedResult || typeof normalizedResult !== "object" || Array.isArray(normalizedResult)) {
    return false;
  }
  if (isActionAckResult(normalizedResult)) {
    return false;
  }
  if (isActionErrorResult(normalizedResult)) {
    return false;
  }
  if (!normalizedResult.source && !normalizedResult.navigation) {
    const label = String(keypath || "").trim().split(".")[0];
    if (label && labelState && typeof labelState === "object") {
      labelState.state = normalizedResult;
      return true;
    }
    return false;
  }
  labelState.state = normalizedResult;
  return true;
}

function isActionAckResult(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return false;
  }
  if (isWorkMutationAckResult(value)) {
    return true;
  }
  const responseMode = normalizedAckResponseMode(value);
  if (responseMode === "ack") {
    return !Object.prototype.hasOwnProperty.call(value, "source") &&
      !Object.prototype.hasOwnProperty.call(value, "navigation");
  }
  return isGenericMutationAckResult(value);
}

function isActionErrorResult(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return false;
  }
  if (value.ok === false || value.error === true) {
    return true;
  }
  const status = typeof value.status === "string" ? value.status.trim().toLowerCase() : "";
  if (status === "error" || status === "failed" || status === "denied") {
    return true;
  }
  return typeof value.error === "string" && value.error.trim().length > 0;
}

function isWorkMutationAckResult(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return false;
  }
  const status = typeof value.status === "string" ? value.status.trim().toLowerCase() : "";
  return status === "ok" &&
    typeof value.operation === "string" &&
    Object.prototype.hasOwnProperty.call(value, "eventID") &&
    Number.isFinite(Number(value.stateVersion)) &&
    Array.isArray(value.changedKeys) &&
    typeof value.entityType === "string" &&
    typeof value.entityID === "string" &&
    !Object.prototype.hasOwnProperty.call(value, "source") &&
    !Object.prototype.hasOwnProperty.call(value, "navigation");
}

function normalizedAckResponseMode(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return "";
  }
  const raw = typeof value.responseMode === "string"
    ? value.responseMode
    : typeof value.response_mode === "string"
      ? value.response_mode
      : "";
  return raw.trim().toLowerCase();
}

function isGenericMutationAckResult(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return false;
  }
  const status = typeof value.status === "string" ? value.status.trim().toLowerCase() : "";
  if (status !== "ok") {
    return false;
  }
  if (typeof value.operation !== "string" || value.operation.trim().length === 0) {
    return false;
  }
  if (!Array.isArray(value.changedKeys) && !Array.isArray(value.changed_keys)) {
    return false;
  }
  return !Object.prototype.hasOwnProperty.call(value, "source") &&
    !Object.prototype.hasOwnProperty.call(value, "navigation");
}

function applyMermaidActionResultState(labelState, actionResult, payload = null) {
  const normalizedResult = normalizeActionResultValue(
    actionResult && typeof actionResult === "object" && Object.prototype.hasOwnProperty.call(actionResult, "result")
      ? actionResult.result
      : actionResult
  );
  if (!normalizedResult || typeof normalizedResult !== "object" || Array.isArray(normalizedResult)) {
    return false;
  }

  if (!labelState.state || typeof labelState.state !== "object" || Array.isArray(labelState.state)) {
    labelState.state = {};
  }

  const diagnostics = normalizedResult.diagnostics && typeof normalizedResult.diagnostics === "object"
    ? normalizedResult.diagnostics
    : {};
  const errors = Array.isArray(diagnostics.errors) ? diagnostics.errors.map(String) : [];
  const warnings = Array.isArray(diagnostics.warnings) ? diagnostics.warnings.map(String) : [];
  const renderedHTML = typeof normalizedResult.rendered_html === "string"
    ? normalizedResult.rendered_html
    : typeof normalizedResult.renderedHTML === "string"
      ? normalizedResult.renderedHTML
      : mermaidFallbackPreviewHTML(errors);
  const renderedImageKind = String(
    normalizedResult.rendered_image_kind ||
    normalizedResult.renderedImageKind ||
    (errors.length ? "fallback" : normalizedResult.output || "svg")
  );
  const renderedImageAvailable = Boolean(
    normalizedResult.rendered_image_available === true ||
    normalizedResult.renderedImageAvailable === true ||
    (!errors.length && (normalizedResult.svgText || normalizedResult.pngBytes || normalizedResult.rendered_html || normalizedResult.renderedHTML))
  );
  const source = payload && typeof payload === "object" && typeof payload.source === "string"
    ? payload.source
    : "";
  const correlationId = payload && typeof payload === "object" && typeof payload.correlationId === "string"
    ? payload.correlationId
    : "";
  const lastRender = {
    hasResult: true,
    has_result: true,
    correlationId,
    correlation_id: correlationId,
    sourcePreview: source.slice(0, 600),
    source_preview: source.slice(0, 600),
    backend: String(normalizedResult.backend || ""),
    output: String(normalizedResult.output || ""),
    cacheHit: Boolean(normalizedResult.cacheHit),
    cache_hit: Boolean(normalizedResult.cacheHit),
    renderTimeMs: Number.isFinite(Number(diagnostics.renderTimeMs)) ? Number(diagnostics.renderTimeMs) : 0,
    render_time_ms: Number.isFinite(Number(diagnostics.renderTimeMs)) ? Number(diagnostics.renderTimeMs) : 0,
    engineVersion: String(diagnostics.engineVersion || ""),
    engine_version: String(diagnostics.engineVersion || ""),
    contentHash: String(diagnostics.contentHash || ""),
    content_hash: String(diagnostics.contentHash || ""),
    warningsText: warnings.join(" | "),
    warnings_text: warnings.join(" | "),
    errorsText: errors.join(" | "),
    errors_text: errors.join(" | "),
    svgTextPreview: typeof normalizedResult.svgText === "string" ? normalizedResult.svgText.slice(0, 1200) : "",
    svg_text_preview: typeof normalizedResult.svgText === "string" ? normalizedResult.svgText.slice(0, 1200) : "",
    pngBytesCount: mermaidPNGByteCount(normalizedResult.pngBytes),
    png_bytes_count: mermaidPNGByteCount(normalizedResult.pngBytes),
    renderedImageAvailable: renderedImageAvailable,
    rendered_image_available: renderedImageAvailable,
    renderedImageKind: renderedImageKind,
    rendered_image_kind: renderedImageKind,
    renderedHTML: renderedHTML,
    rendered_html: renderedHTML,
    renderedFallbackText: String(normalizedResult.rendered_fallback_text || normalizedResult.renderedFallbackText || errors.join(" | ") || "Rendered Mermaid preview is available."),
    rendered_fallback_text: String(normalizedResult.rendered_fallback_text || normalizedResult.renderedFallbackText || errors.join(" | ") || "Rendered Mermaid preview is available."),
  };

  const current = labelState.state && typeof labelState.state === "object" ? labelState.state : {};
  labelState.state = {
    ...current,
    status: "ready",
    endpoint: current.endpoint || "cell:///MermaidRenderer",
    capability: current.capability || "render.mermaid",
    totalRenders: Number.isFinite(Number(current.totalRenders)) ? Number(current.totalRenders) + 1 : 1,
    total_renders: Number.isFinite(Number(current.total_renders)) ? Number(current.total_renders) + 1 : 1,
    lastError: errors.join(" | "),
    last_error: errors.join(" | "),
    lastRender,
    last_render: lastRender,
  };
  return true;
}

function mermaidFallbackPreviewHTML(errors) {
  const text = errors && errors.length
    ? `Mermaid diagram could not be rendered: ${errors.join(" | ")}`
    : "Mermaid render completed, but no inline preview HTML was returned.";
  return `<div class="mermaid-render-preview mermaid-render-preview-fallback" role="img" aria-label="Mermaid diagram preview unavailable">${escapeHTML(text)}</div>`;
}

function mermaidPNGByteCount(value) {
  if (typeof value === "string") {
    return value.length;
  }
  if (value && typeof value === "object" && typeof value.data === "string") {
    return value.data.length;
  }
  return 0;
}

function createPendingActionDescriptor(keypath, payload) {
  switch (keypath) {
    case "editor.mode.set": {
      const mode = payload && typeof payload.mode === "string" ? normalizeMode(payload.mode) : "view";
      return {
        keypath,
        label: mode === "edit" ? "Bytter til edit mode…" : "Bytter til view mode…",
      };
    }
    case "editor.undo":
      return { keypath, label: "Angrer siste editorendring…" };
    case "editor.redo":
      return { keypath, label: "Gjenoppretter editorendring…" };
    case "editor.apply":
      return { keypath, label: "Bruker endringer i Porthole…" };
    case "editor.discard":
      return { keypath, label: "Forkaster lokale endringer…" };
    case "editor.component.insert":
      return { keypath, label: "Setter inn komponent i working copy…" };
    case "removeReference":
      return { keypath, label: "Fjerner reference fra Porthole…" };
    default:
      break;
  }

  if (keypath.endsWith(".applyDraftProfile")) {
    return { keypath, label: "Oppdaterer agent-route…" };
  }
  if (keypath.endsWith(".invokeDraft")) {
    return { keypath, label: "Synkroniserer og invokerer agent…" };
  }
  if (keypath.endsWith(".persistDraftAPIKey")) {
    return { keypath, label: "Lagrer API-nøkkel i session…" };
  }
  if (keypath.endsWith(".clearDraftAPIKey")) {
    return { keypath, label: "Fjerner lagret API-nøkkel…" };
  }
  return null;
}

// En avbrutt fetch gir INGEN response-hendelse. Da ser hverken Playwright eller
// en ventende klient forskjell paa «serveren svarte ikke» og «vi ga oss» - og
// standardverdien paa 10 s var i praksis en skjult oevre grense for hvor lenge
// en cellehandling fikk lov til aa ta. Den felte Thursday-gaten: CI bygger med
// `swift build` uten `-c release`, og en debug-build er 4-5 ganger tregere enn
// den vi maaler lokalt, saa `chatHub.prompt.submit` gikk over 10 s der og under
// lokalt. Testen ventet 45 s paa et svar klienten alt hadde avbrutt.
//
// Rettelsen er ikke en lengre liste over unntak, men en aerligere standard: en
// cellehandling kan lovlig ta tid, og kostnaden ved aa vente er mye mindre enn
// kostnaden ved aa avbryte noe som var i ferd med aa lykkes. Korte budsjetter
// beholdes bare der handlingen er kjent billig og responsen skal foeles kjapp.
const PORTHOLE_ACTION_TIMEOUT_MS = {
  // Handlinger som kan naa en spraakmodell, en katalogskanning eller et
  // RAG-soek. Disse er trege av natur, ikke fordi noe er galt.
  modelBacked: 90000,
  // Alt annet som gaar mot en celle.
  cellAction: 45000,
  // Redigering i et aapent felt skal svare med én gang eller si fra.
  editorApply: 12000,
  editor: 8000,
};

function isModelBackedActionKeypath(keypath) {
  return keypath === "prompt.submit"
    || keypath === "sendComposedMessage"
    || keypath === "demo.ask"
    || keypath.startsWith("chatHub.")
    || keypath.startsWith("onboarding.")
    || keypath.startsWith("assistant.")
    || keypath.endsWith(".invokeDraft")
    || keypath.endsWith(".scan")
    || keypath.endsWith(".search")
    || keypath.endsWith(".ask");
}

function resolveActionTimeoutMs(keypath) {
  if (isMermaidRenderKeypath(keypath)) {
    return PORTHOLE_ACTION_TIMEOUT_MS.cellAction;
  }
  if (isModelBackedActionKeypath(keypath)) {
    return PORTHOLE_ACTION_TIMEOUT_MS.modelBacked;
  }
  // The advisor runs retrieval, the capability index and a model call in one
  // action. A capable remote model is fast; a local one is not.
  if (keypath === "advisor.ask") {
    return 180000;
  }
  if (keypath === "editor.apply" || keypath === "editor.discard") {
    return PORTHOLE_ACTION_TIMEOUT_MS.editorApply;
  }
  if (keypath.startsWith("editor.")) {
    return PORTHOLE_ACTION_TIMEOUT_MS.editor;
  }
  return PORTHOLE_ACTION_TIMEOUT_MS.cellAction;
}

// Butler faller stille tilbake til den deterministiske regelmotoren
// `chat.local-rules` naar ingen modell er registrert for forespoerreren
// (se ChatScopedAIProviderRouter.route). Uten dette ser brukeren en robotaktig
// samtale og tror modellen er daarlig, ikke at den er fravaerende.
const localRulesProviderID = "chat.local-rules";
const localRulesProviderKind = "local_rules";

function providerIsLocalRules(provider) {
  if (!provider || typeof provider !== "object") {
    return false;
  }
  return provider.id === localRulesProviderID || provider.kind === localRulesProviderKind;
}

function providerCanAnswerAsModel(provider) {
  if (!provider || typeof provider !== "object") {
    return false;
  }
  if (providerIsLocalRules(provider)) {
    return false;
  }
  return provider.canInvokeFromChat === true;
}

function updateAssistantDegradationFromResult(result) {
  if (!result || typeof result !== "object") {
    return;
  }

  const recommendation = result.providerRecommendation;
  const candidates = Array.isArray(result.assistantProviders)
    ? result.assistantProviders
    : Array.isArray(result.providers)
      ? result.providers
      : [];

  const anyModelCandidate = candidates.some(providerCanAnswerAsModel);
  const recommendedIsLocalRules = providerIsLocalRules(recommendation);

  if (anyModelCandidate || (recommendation && !recommendedIsLocalRules)) {
    portholeWebState.assistantDegradation = null;
    return;
  }

  if (!recommendedIsLocalRules) {
    return;
  }

  portholeWebState.assistantDegradation = {
    state: "no_model_connected",
    title: "Ingen modell er koblet til",
    message: "Butler svarer naa med lokale regler, ikke en spraakmodell. Koble til en modell for aa faa ekte samtale.",
  };
}

function renderAssistantDegradationBanner() {
  const degradation = portholeWebState.assistantDegradation;
  if (!degradation) {
    return "";
  }
  return `<p class="notice notice--degraded" role="status">`
    + `<strong>${escapeHTML(degradation.title)}</strong> ${escapeHTML(degradation.message)}`
    + `</p>`;
}

function applyOptimisticActionState(keypath, payload) {
  const bootstrap = portholeWebState.bootstrap;
  if (!bootstrap || !bootstrap.state || typeof bootstrap.state !== "object") {
    return;
  }

  if (applyOptimisticNavigationActionState(keypath, payload, bootstrap.state)) {
    return;
  }

  if (!bootstrap || !bootstrap.editorState || typeof bootstrap.editorState !== "object") {
    return;
  }

  if (keypath === "editor.mode.set" && payload && typeof payload.mode === "string") {
    const nextMode = normalizeMode(payload.mode);
    bootstrap.editorState.mode = nextMode;
    bootstrap.editorState.isEditing = nextMode === "edit";
    bootstrap.editor = normalizeLegacyEditor(bootstrap.editorState);
    portholeWebState.mode = nextMode;
    if (nextMode !== "edit") {
      portholeWebState.armedComponent = null;
      portholeWebState.activePanelDrag = null;
    } else {
      ensureFloatingPanelLayouts();
      ensureFloatingPanelPresentationState();
    }
    return;
  }

  if (keypath === "editor.selection.set" && payload && typeof payload.path === "string") {
    bootstrap.editorState.selectionPath = payload.path;
    bootstrap.editor = normalizeLegacyEditor(bootstrap.editorState);
  }
}

function applyOptimisticNavigationActionState(keypath, payload, rootState) {
  const normalized = String(keypath || "").trim();
  if (!normalized.endsWith(".navigation.setActiveTab")) {
    return false;
  }

  const label = normalized.split(".")[0];
  const selectedTabID = selectedIDFromActionPayload(payload);
  if (!label || !selectedTabID) {
    return false;
  }

  const labelState = rootState[label];
  if (!labelState || typeof labelState !== "object") {
    return false;
  }

  const cellState = labelState.state;
  if (!cellState || typeof cellState !== "object") {
    return false;
  }

  if (!cellState.navigation || typeof cellState.navigation !== "object") {
    cellState.navigation = {};
  }
  cellState.navigation.activeTab = selectedTabID;
  return true;
}

function selectedIDFromActionPayload(payload) {
  if (typeof payload === "string") {
    return payload;
  }
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    return "";
  }
  return String(payload.selectedValue || payload.id || payload.selected || "");
}

function shouldForceBootstrapReload(keypath, payload, appliedActionState = false) {
  const normalized = String(keypath || "").trim();
  if (!normalized) {
    return false;
  }
  if (shouldAlwaysRefreshAfterAction(normalized)) {
    return true;
  }
  if (appliedActionState && isFastParticipantAgendaMutation(normalized, payload)) {
    return false;
  }
  if (shouldRefreshChatHubActionState(normalized)) {
    return !appliedActionState;
  }
  if (appliedActionState) {
    return false;
  }
  if (normalized === "addConfiguration" || normalized === "removeReference") {
    return true;
  }
  if (normalized.startsWith("editor.")) {
    return true;
  }
  if (isEventDrivenRuntimeAction(normalized)) {
    return false;
  }
  if (normalized.includes(".") && payload !== undefined) {
    return true;
  }
  return false;
}

function shouldAlwaysRefreshAfterAction(keypath) {
  const normalized = String(keypath || "").trim();
  return normalized === "ownerSetup.seedOwnerWorkbench" ||
    normalized === "workItems.select" ||
    normalized === "workItems.clearSelection" ||
    normalized === "workItems.capture" ||
    normalized === "workItems.captureDraft" ||
    normalized.startsWith("workItems.board.") ||
    normalized === "projectPortfolio.captureDraft";
}

function shouldRefreshChatHubActionState(keypath) {
  const normalized = String(keypath || "").trim();
  return normalized === "chatHub.assistant.analyzeDraft" ||
    normalized === "assistant.analyzeDraft" ||
    normalized === "chatHub.prompt.submit" ||
    normalized === "prompt.submit" ||
    normalized === "chatHub.ui.openSuggestedHelper" ||
    normalized === "ui.openSuggestedHelper";
}

function normalizeBootstrap(payload) {
  const portholeState = payload && typeof payload.portholeState === "object" ? payload.portholeState : payload;
  const legacyEditor = payload && typeof payload.editor === "object" ? payload.editor : {};
  const editorState = normalizeEditorState(
    payload && typeof payload.editorState === "object" ? payload.editorState : null,
    legacyEditor
  );

  const result = {
    contractVersion: typeof payload.contractVersion === "string" ? payload.contractVersion : "legacy",
    sessionId: typeof portholeState.sessionId === "string" ? portholeState.sessionId : "",
    configuration: unwrapCellConfiguration(portholeState.configuration),
    localizationContext: portholeState.localizationContext || payload.localizationContext || null,
    state: portholeState && typeof portholeState.state === "object" ? portholeState.state : {},
    notifications: normalizeNotificationCenter(
      portholeState.notifications ||
      (portholeState.state &&
      portholeState.state.$porthole &&
      typeof portholeState.state.$porthole === "object"
        ? portholeState.state.$porthole.notifications
        : null)
    ),
    requester: portholeState && typeof portholeState.requester === "object"
      ? portholeState.requester
      : (payload && typeof payload.requester === "object" ? payload.requester : null),
    availableConfigurations: [],
    componentPalette: [],
    editorState,
    editor: normalizeLegacyEditor(editorState),
    menus: {},
  };

  const menus = portholeState && typeof portholeState.menus === "object" ? portholeState.menus : {};
  menuKeys.forEach((key) => {
    const list = unwrapConfigurationList(menus[key]);
    result.menus[key] = list.map((entry) => unwrapCellConfiguration(entry)).filter((entry) => entry && typeof entry === "object");
  });

  const availableConfigurations = unwrapConfigurationList(portholeState.availableConfigurations)
    .concat(unwrapConfigurationList(payload.availableConfigurations));
  result.availableConfigurations = availableConfigurations
    .map((entry) => unwrapCellConfiguration(entry))
    .filter((entry) => entry && typeof entry === "object");
  result.componentPalette = normalizeComponentPalette(
    portholeState.componentPalette || payload.componentPalette
  );

  return result;
}

function preserveFastParticipantAgendaStateDuringRefresh(currentBootstrap, nextBootstrap, refreshStartedAt) {
  if (!currentBootstrap || !nextBootstrap) {
    return nextBootstrap;
  }

  const now = Date.now();
  const lastAgendaUpdate = Number(portholeWebState.fastParticipantAgendaUpdatedAt) || 0;
  const refreshMayBeStale = lastAgendaUpdate > 0 && Number(refreshStartedAt) <= lastAgendaUpdate;
  const refreshIsSuppressed = now < (Number(portholeWebState.socketRefreshSuppressUntil) || 0);
  if (!refreshMayBeStale && !refreshIsSuppressed) {
    return nextBootstrap;
  }

  const currentState = currentBootstrap.state && typeof currentBootstrap.state === "object"
    ? currentBootstrap.state
    : {};
  const nextState = nextBootstrap.state && typeof nextBootstrap.state === "object"
    ? nextBootstrap.state
    : {};

  ["conferenceParticipantShell", "conferenceParticipantPreviewShell"].forEach((label) => {
    const currentCellState = cellStateForBootstrapLabel(currentState, label);
    const nextCellState = cellStateForBootstrapLabel(nextState, label);
    if (!currentCellState || !nextCellState || !looksLikeParticipantAgendaProgram(currentCellState.program)) {
      return;
    }

    nextCellState.program = deepCloneValue(currentCellState.program);
  });

  const currentArendalsukaState = cellStateForBootstrapLabel(currentState, "arendalsukaParticipant");
  const nextArendalsukaState = cellStateForBootstrapLabel(nextState, "arendalsukaParticipant");
  if (currentArendalsukaState && nextArendalsukaState) {
    const currentAgenda = currentArendalsukaState.agenda;
    const nextAgenda = nextArendalsukaState.agenda;
    if (currentAgenda && typeof currentAgenda === "object" && !Array.isArray(currentAgenda) &&
        nextAgenda && typeof nextAgenda === "object" && !Array.isArray(nextAgenda)) {
      nextArendalsukaState.agenda = {
        ...nextAgenda,
        savedSessionIDs: deepCloneValue(currentAgenda.savedSessionIDs),
        savedSessionCount: currentAgenda.savedSessionCount,
        timelineRows: deepCloneValue(currentAgenda.timelineRows),
      };
    }

    const currentProgram = currentArendalsukaState.program;
    const nextProgram = nextArendalsukaState.program;
    if (currentProgram && typeof currentProgram === "object" && !Array.isArray(currentProgram) &&
        nextProgram && typeof nextProgram === "object" && !Array.isArray(nextProgram) &&
        Array.isArray(currentProgram.visibleSessionCards)) {
      nextArendalsukaState.program = {
        ...nextProgram,
        visibleSessionCards: deepCloneValue(currentProgram.visibleSessionCards),
      };
    }
  }

  return nextBootstrap;
}

function rememberRecentCellActionState(label, keypath, actionResult, actionSeq = null) {
  const normalizedKeypath = String(keypath || "").trim();
  if (!label || !shouldPreserveRecentCellActionState(actionResult)) {
    return;
  }

  const requestedSequence = Number(actionSeq);
  const sequence = Number.isFinite(requestedSequence) && requestedSequence > 0
    ? requestedSequence
    : nextPortholeOrderingSequence("action");
  if (sequence < (Number(portholeWebState.lastActionSeq[label]) || 0)) {
    return;
  }
  portholeWebState.lastActionSeq[label] = sequence;
  portholeWebState.lastActionKeypath[label] = normalizedKeypath;
}

function shouldPreserveRecentCellActionState(actionResult) {
  const state = actionResultPayload(actionResult);
  if (!state || typeof state !== "object" || Array.isArray(state)) {
    return false;
  }
  // Preservation is selected by the returned state contract, never by a
  // keypath allow-list. Cells return source+navigation for a full snapshot;
  // chat actions return their authoritative renderer projection under ui.
  const hasFullCellState = Object.prototype.hasOwnProperty.call(state, "source") &&
    state.navigation &&
    typeof state.navigation === "object" &&
    !Array.isArray(state.navigation);
  const hasAuthoritativeUIState = state.ui &&
    typeof state.ui === "object" &&
    !Array.isArray(state.ui);
  return Boolean(hasFullCellState || hasAuthoritativeUIState);
}

function preserveRecentCellActionStatesDuringRefresh(
  currentBootstrap,
  nextBootstrap,
  bootstrapSeq
) {
  if (!currentBootstrap || !nextBootstrap) {
    return nextBootstrap;
  }

  const currentState = currentBootstrap.state && typeof currentBootstrap.state === "object"
    ? currentBootstrap.state
    : {};
  const nextState = nextBootstrap.state && typeof nextBootstrap.state === "object"
    ? nextBootstrap.state
    : {};
  const normalizedBootstrapSeq = Number(bootstrapSeq) || 0;
  const entries = portholeWebState.lastActionSeq || {};

  Object.entries(entries).forEach(([label, rawActionSeq]) => {
    const actionSeq = Number(rawActionSeq) || 0;
    if (!actionSeq) {
      delete entries[label];
      delete portholeWebState.lastActionKeypath[label];
      return;
    }
    if (normalizedBootstrapSeq > actionSeq) {
      delete entries[label];
      delete portholeWebState.lastActionKeypath[label];
      return;
    }
    const currentLabelState = currentState[label];
    if (!currentLabelState || typeof currentLabelState !== "object") {
      return;
    }
    nextState[label] = deepCloneValue(currentLabelState);
  });

  return nextBootstrap;
}

function cellStateForBootstrapLabel(rootState, label) {
  const labelState = rootState && typeof rootState === "object" ? rootState[label] : null;
  return labelState && typeof labelState === "object" && labelState.state && typeof labelState.state === "object"
    ? labelState.state
    : null;
}

function looksLikeParticipantAgendaProgram(program) {
  return Boolean(
    program &&
    typeof program === "object" &&
    !Array.isArray(program) &&
    (
      Array.isArray(program.trackOptions) ||
      Array.isArray(program.sessions) ||
      Array.isArray(program.focusedTrackIDs) ||
      Object.prototype.hasOwnProperty.call(program, "selectedTrackID") ||
      Object.prototype.hasOwnProperty.call(program, "activeView")
    )
  );
}

function normalizeEditorState(editorState, legacyEditor) {
  const source = editorState && typeof editorState === "object" ? editorState : {};
  const legacy = legacyEditor && typeof legacyEditor === "object" ? legacyEditor : {};
  const mode = normalizeMode(source.mode || legacy.mode || "view");
  const sourceBacked = Boolean(source.sourceBacked);
  const canEdit = source.canEdit == null ? true : Boolean(source.canEdit);
  return {
    mode,
    isEditing: Boolean(source.isEditing != null ? source.isEditing : mode === "edit"),
    isDirty: Boolean(source.isDirty != null ? source.isDirty : legacy.isDirty),
    selectionPath: typeof source.selectionPath === "string" ? source.selectionPath : null,
    canUndo: Boolean(source.canUndo != null ? source.canUndo : legacy.canUndo),
    canRedo: Boolean(source.canRedo != null ? source.canRedo : legacy.canRedo),
    undoDepth: Number.isFinite(source.undoDepth) ? Number(source.undoDepth) : 0,
    redoDepth: Number.isFinite(source.redoDepth) ? Number(source.redoDepth) : 0,
    revision: Number.isFinite(source.revision) ? Number(source.revision) : 0,
    workingSkeleton: source.workingSkeleton && typeof source.workingSkeleton === "object" ? source.workingSkeleton : null,
    committedSkeleton: source.committedSkeleton && typeof source.committedSkeleton === "object" ? source.committedSkeleton : null,
    workingReferences: normalizeReferenceList(source.workingReferences),
    committedReferences: normalizeReferenceList(source.committedReferences),
    sourceBacked,
    canEdit,
    sourceCellEndpoint: typeof source.sourceCellEndpoint === "string" ? source.sourceCellEndpoint : "",
    sourceCellName: typeof source.sourceCellName === "string" ? source.sourceCellName : "",
    accessSummary: typeof source.accessSummary === "string" ? source.accessSummary : "",
    accessInstruction: typeof source.accessInstruction === "string" ? source.accessInstruction : "",
  };
}

function resolveEditorAccessNotice(editorState = null) {
  const state = editorState ||
    (portholeWebState.bootstrap && portholeWebState.bootstrap.editorState
      ? portholeWebState.bootstrap.editorState
      : null);
  if (!state || !state.sourceBacked) {
    return null;
  }

  const sourceName = state.sourceCellName || state.sourceCellEndpoint || "source-cellen";
  const fallback = state.canEdit
    ? `Endringer lagres til ${sourceName} når du trykker Apply.`
    : `Denne CellConfigurationen kan leses, men ikke redigeres av nåværende requester. Åpne Porthole som eier av ${sourceName}, eller be eier gi en Agreement-grant med rw-- for applyEditableCellConfiguration.`;
  const message = (state.accessInstruction || state.accessSummary || fallback).trim();
  return {
    blocked: state.canEdit === false,
    message,
    sourceName,
  };
}

function normalizeLegacyEditor(editorState) {
  return {
    mode: editorState.mode,
    panels: ["elements", "inspector"],
    selectionPath: editorState.selectionPath,
    isDirty: editorState.isDirty,
    canUndo: editorState.canUndo,
    canRedo: editorState.canRedo,
    notes: "Porthole web editor contract v2",
  };
}

function normalizeReferenceList(value) {
  if (!Array.isArray(value)) {
    return [];
  }
  return value
    .filter((entry) => entry && typeof entry === "object")
    .map((entry) => ({
      label: typeof entry.label === "string" ? entry.label : "",
      endpoint: typeof entry.endpoint === "string" ? entry.endpoint : "",
    }))
    .filter((entry) => entry.label);
}

function normalizeNotificationCenter(value) {
  const source = unwrapValueType(value);
  const objectSource = source && typeof source === "object" && !Array.isArray(source) ? source : {};
  const rawItems = unwrapValueType(objectSource.items);
  const items = Array.isArray(rawItems)
    ? rawItems.map((entry) => normalizeNotificationItem(entry)).filter(Boolean)
    : [];
  const latest = normalizeNotificationItem(unwrapValueType(objectSource.latest));
  const connectedValue = unwrapValueType(objectSource.connected);
  const totalTicketsValue = unwrapValueType(objectSource.totalTickets);
  const queuedTicketsValue = unwrapValueType(objectSource.queuedTickets);
  const openTicketsValue = unwrapValueType(objectSource.openTickets);
  const ackedTicketsValue = unwrapValueType(objectSource.ackedTickets);
  return {
    connected: Boolean(connectedValue),
    totalTickets: Number.isFinite(totalTicketsValue) ? Number(totalTicketsValue) : items.length,
    queuedTickets: Number.isFinite(queuedTicketsValue) ? Number(queuedTicketsValue) : 0,
    openTickets: Number.isFinite(openTicketsValue) ? Number(openTicketsValue) : 0,
    ackedTickets: Number.isFinite(ackedTicketsValue) ? Number(ackedTicketsValue) : 0,
    items,
    latest,
  };
}

function normalizeNotificationItem(value) {
  const source = unwrapValueType(value);
  if (!source || typeof source !== "object" || Array.isArray(source)) {
    return null;
  }
  const titleValue = unwrapValueType(source.title);
  const subtitleValue = unwrapValueType(source.subtitle);
  const detailValue = unwrapValueType(source.detail);
  const statusValue = unwrapValueType(source.status);
  const idValue = unwrapValueType(source.id);
  const createdAtValue = unwrapValueType(source.createdAt);
  const title = typeof titleValue === "string" && titleValue.trim()
    ? titleValue.trim()
    : "";
  const subtitle = typeof subtitleValue === "string" && subtitleValue.trim()
    ? subtitleValue.trim()
    : "";
  const detail = typeof detailValue === "string" && detailValue.trim()
    ? detailValue.trim()
    : "";
  const status = typeof statusValue === "string" && statusValue.trim()
    ? statusValue.trim()
    : "";
  const id = typeof idValue === "string" && idValue.trim()
    ? idValue.trim()
    : `${title}:${subtitle}:${detail}`;
  const createdAt = Number.isFinite(createdAtValue) ? Number(createdAtValue) : null;
  if (!title && !detail) {
    return null;
  }
  return {
    id,
    title: title || "Notification",
    subtitle,
    detail,
    status,
    createdAt,
  };
}

function normalizeComponentPalette(value) {
  if (!Array.isArray(value)) {
    return [];
  }
  return value
    .filter((entry) => entry && typeof entry === "object" && entry.recipe && typeof entry.recipe === "object")
    .map((entry) => ({
      id: typeof entry.id === "string" ? entry.id : "",
      title: typeof entry.title === "string" ? entry.title : "Komponent",
      subtitle: typeof entry.subtitle === "string" ? entry.subtitle : "",
      icon: typeof entry.icon === "string" ? entry.icon : "square.stack.3d.up.fill",
      sourceKind: typeof entry.sourceKind === "string" ? entry.sourceKind : "palette",
      recipe: {
        id: typeof entry.recipe.id === "string" ? entry.recipe.id : "",
        displayName: typeof entry.recipe.displayName === "string" ? entry.recipe.displayName : (typeof entry.title === "string" ? entry.title : "Komponent"),
        subtitle: typeof entry.recipe.subtitle === "string" ? entry.recipe.subtitle : "",
        icon: typeof entry.recipe.icon === "string" ? entry.recipe.icon : (typeof entry.icon === "string" ? entry.icon : "square.stack.3d.up.fill"),
        referenceTemplate: Array.isArray(entry.recipe.referenceTemplate) ? entry.recipe.referenceTemplate : [],
        skeletonTemplate: entry.recipe.skeletonTemplate && typeof entry.recipe.skeletonTemplate === "object"
          ? entry.recipe.skeletonTemplate
          : null,
        supportedTargetKinds: Array.isArray(entry.recipe.supportedTargetKinds) ? entry.recipe.supportedTargetKinds : [],
        preferredDropBehavior: typeof entry.recipe.preferredDropBehavior === "string"
          ? entry.recipe.preferredDropBehavior
          : "appendIntoContainer",
      },
    }))
    .filter((entry) => entry.id && entry.recipe && entry.recipe.skeletonTemplate);
}

function normalizeMode(value) {
  const lower = String(value || "").toLowerCase().trim();
  return lower === "edit" ? "edit" : "view";
}

function isProductSurfaceConfigurationName(name) {
  const normalized = String(name || "").trim();
  if (normalized === "Idea Task Workspace"
    || normalized === "Co-Pilot Chat"
    || normalized === "Invite Chat"
    || normalized === "Questionnaire Campaign"
    || normalized === "Arendalsuka Participant Program") {
    return true;
  }
  const configuration = portholeWebState
    && portholeWebState.bootstrap
    && portholeWebState.bootstrap.configuration
    && typeof portholeWebState.bootstrap.configuration === "object"
    ? portholeWebState.bootstrap.configuration
    : null;
  const references = configuration && Array.isArray(configuration.cellReferences)
    ? configuration.cellReferences
    : [];
  const hasChatHubReference = references.some((reference) => {
    const label = String(reference && reference.label || "").trim();
    const endpoint = String(reference && reference.endpoint || "").trim();
    return label === "chatHub" || endpoint === "cell:///PersonalChatHub";
  });
  if (!hasChatHubReference) {
    return false;
  }
  const skeleton = configuration && configuration.skeleton && typeof configuration.skeleton === "object"
    ? configuration.skeleton
    : null;
  const tabs = skeleton && skeleton.Tabs && typeof skeleton.Tabs === "object"
    ? skeleton.Tabs
    : null;
  const panels = tabs && Array.isArray(tabs.panels) ? tabs.panels : [];
  const panelIDs = panels
    .map((panel) => String(panel && panel.id || "").trim())
    .filter(Boolean);
  return panelIDs.includes("samtale") && panelIDs.includes("aktivt") && panelIDs.includes("mer");
}

function findCoPilotChatConfiguration() {
  const configurations = getLibraryConfigurations();
  return configurations.find((configuration) => String(configuration && configuration.name || "").trim() === "Co-Pilot Chat")
    || configurations.find((configuration) => {
      const discovery = configuration && typeof configuration === "object" && configuration.discovery && typeof configuration.discovery === "object"
        ? configuration.discovery
        : null;
      return discovery && String(discovery.sourceCellEndpoint || "").trim() === "cell:///PersonalChatHub";
    })
    || configurations.find((configuration) => String(configuration && configuration.name || "").trim() === "Invite Chat")
    || null;
}

function unwrapCellConfiguration(value) {
  return unwrapCellConfigurationCandidate(value, 0);
}

function unwrapConfigurationList(value) {
  if (Array.isArray(value)) {
    return value;
  }

  if (!value || typeof value !== "object") {
    return [];
  }

  const nestedKeys = ["&list", "list", "value", "items", "entries", "configurations", "availableConfigurations"];
  for (let index = 0; index < nestedKeys.length; index += 1) {
    const nestedValue = value[nestedKeys[index]];
    if (Array.isArray(nestedValue)) {
      return nestedValue;
    }
  }

  const unwrappedConfiguration = unwrapCellConfigurationCandidate(value, 0);
  if (unwrappedConfiguration && typeof unwrappedConfiguration === "object" && looksLikeCellConfiguration(unwrappedConfiguration)) {
    return [unwrappedConfiguration];
  }

  return [];
}

function unwrapCellConfigurationCandidate(value, depth) {
  if (!value || typeof value !== "object") {
    return null;
  }

  if (looksLikeCellConfiguration(value)) {
    return value;
  }

  if (depth >= 4) {
    return value;
  }

  const nestedKeys = ["&cellConfiguration", "cellConfiguration", "configuration", "goal"];
  for (let index = 0; index < nestedKeys.length; index += 1) {
    const key = nestedKeys[index];
    const nestedValue = value[key];
    if (nestedValue && typeof nestedValue === "object") {
      const unwrapped = unwrapCellConfigurationCandidate(nestedValue, depth + 1);
      if (unwrapped && typeof unwrapped === "object") {
        return unwrapped;
      }
    }
  }

  return value;
}

function looksLikeCellConfiguration(value) {
  if (!value || typeof value !== "object") {
    return false;
  }

  if (typeof value.name !== "string" || value.name.trim().length === 0) {
    return false;
  }

  if (value.skeleton && typeof value.skeleton === "object") {
    return true;
  }

  if (Array.isArray(value.cellReferences)) {
    return true;
  }

  return typeof value.uuid === "string" && value.uuid.trim().length > 0;
}

function resolveActionFeedback(keypath, payload, actionResult, { sourceAction = false } = {}) {
  const normalizedKeypath = String(keypath || "").trim();
  const isChatHubAction = !sourceAction && normalizedKeypath.startsWith("chatHub.");
  if (!sourceAction && normalizedKeypath.endsWith(".navigation.setActiveTab")) {
    return { notice: null, error: null };
  }
  if (!sourceAction && isFastParticipantAgendaMutation(normalizedKeypath, payload)) {
    const normalizedResult = normalizeActionResultValue(
      resolveFastParticipantAgendaResult(normalizedKeypath, actionResult, payload)
    );
    if (typeof normalizedResult === "string") {
      const trimmedResult = normalizedResult.trim();
      if (trimmedResult.length > 0) {
        const lowered = trimmedResult.toLowerCase();
        if (lowered === "denied" || lowered.startsWith("error")) {
          return { notice: null, error: trimmedResult };
        }
      }
    }
    return { notice: null, error: null };
  }
  const normalizedResult = normalizeActionResultValue(
    actionResult && typeof actionResult === "object" && Object.prototype.hasOwnProperty.call(actionResult, "result")
      ? actionResult.result
      : actionResult
  );

  if (!sourceAction && isMermaidRenderKeypath(normalizedKeypath)) {
    const mermaidFeedback = resolveMermaidActionFeedback(normalizedResult);
    if (mermaidFeedback) {
      return mermaidFeedback;
    }
  }

  if (normalizedResult && typeof normalizedResult === "object" && isActionErrorResult(normalizedResult)) {
    const message = typeof normalizedResult.reason === "string" && normalizedResult.reason.trim()
      ? normalizedResult.reason.trim()
      : typeof normalizedResult.error === "string" && normalizedResult.error.trim()
        ? normalizedResult.error.trim()
        : typeof normalizedResult.message === "string" && normalizedResult.message.trim()
        ? normalizedResult.message.trim()
        : typeof normalizedResult.code === "string" && normalizedResult.code.trim()
          ? normalizedResult.code.trim()
          : typeof normalizedResult.status === "string" && normalizedResult.status.trim()
          ? normalizedResult.status.trim()
          : `Klarte ikke å kjøre ${normalizedKeypath}.`;
    return { notice: null, error: message };
  }

  if (typeof normalizedResult === "string") {
    const trimmedResult = normalizedResult.trim();
    const lowered = trimmedResult.toLowerCase();
    if (lowered === "denied" || lowered.startsWith("error")) {
      return { notice: null, error: trimmedResult };
    }
    if (!isChatHubAction && trimmedResult.length > 0 && lowered !== "ok" && lowered !== "applied" && lowered !== "noop") {
      return { notice: trimmedResult, error: null };
    }
  }

  if (sourceAction) {
    return { notice: "Handlingen er utført.", error: null };
  }

  if (isChatHubAction) {
    return { notice: null, error: null };
  }

  if (normalizedKeypath === "addConfiguration") {
    const configuration = unwrapCellConfiguration(payload);
    const name = configuration && typeof configuration.name === "string" ? configuration.name.trim() : "";
    return { notice: name ? `La til ${name}.` : "La til konfigurasjon.", error: null };
  }

  if (normalizedKeypath === "removeReference") {
    const label = payload && typeof payload === "object" && typeof payload.label === "string" ? payload.label.trim() : "";
    return { notice: label ? `Fjernet ${label}.` : "Fjernet referanse.", error: null };
  }

  if (normalizedKeypath === "editor.component.insert") {
    const result = actionResult && typeof actionResult === "object" && actionResult.result && typeof actionResult.result === "object"
      ? actionResult.result
      : {};
    const name = typeof result.componentName === "string" ? result.componentName.trim() : "Komponent";
    const targetPath = typeof result.targetPath === "string" ? result.targetPath.trim() : "root";
    const pathLabel = targetPath === "root" ? "rotnivå" : targetPath;
    return { notice: `${name} ble lagt til i ${pathLabel}. Trykk Apply for å aktivere referanser.`, error: null };
  }

  return { notice: humanActionNotice(normalizedKeypath), error: null };
}

function humanActionNotice(normalizedKeypath) {
  switch (normalizedKeypath) {
    case "trustPacketWorkbench.previewReceipt":
      return "Forhåndsvisning oppdatert.";
    case "trustPacketWorkbench.sendBasicTrustPacket":
      return "Trust packet sendt.";
    case "trustPacketWorkbench.verifyReceiptSignature":
      return "Signatur verifisert.";
    case "trustPacketWorkbench.extractPurposeCandidates":
      return "Formålsforslag hentet.";
    case "trustPacketWorkbench.confirmSelectedPurposeCandidate":
      return "Formålsforslag bekreftet.";
    case "trustPacketWorkbench.evaluatePerspectiveMatch":
      return "Perspective-match forklart.";
    case "trustPacketWorkbench.exportOwnReceipt":
      return "Kvittering eksportert.";
    case "trustPacketWorkbench.revokeGrant":
      return "Kvittering trukket tilbake.";
    case "trustPacketWorkbench.shareWithProjectRoom":
      return "Deling med prosjektrom behandlet.";
    default:
      return "Handlingen er utført.";
  }
}

function resolveMermaidActionFeedback(normalizedResult) {
  if (!normalizedResult || typeof normalizedResult !== "object" || Array.isArray(normalizedResult)) {
    return null;
  }

  const diagnostics = normalizedResult.diagnostics && typeof normalizedResult.diagnostics === "object"
    ? normalizedResult.diagnostics
    : null;
  const errors = diagnostics && Array.isArray(diagnostics.errors)
    ? diagnostics.errors.map((entry) => String(entry || "").trim()).filter(Boolean)
    : [];
  if (errors.length > 0) {
    return {
      notice: null,
      error: `Mermaid render feilet: ${errors.join(" | ")}`,
    };
  }

  const hasSVG = typeof normalizedResult.svgText === "string" && normalizedResult.svgText.trim().length > 0;
  const hasPNG = normalizedResult.pngBytes != null;
  if (!hasSVG && !hasPNG) {
    return {
      notice: null,
      error: "Mermaid render fullforte uten SVG- eller PNG-output.",
    };
  }

  const output = typeof normalizedResult.output === "string" ? normalizedResult.output.trim() : "";
  const backend = typeof normalizedResult.backend === "string" ? normalizedResult.backend.trim() : "";
  const outputLabel = output === "pngBytes"
    ? "PNG"
    : output === "platformImage"
      ? "platform image"
      : "SVG";
  const backendLabel = backend ? ` via ${backend}` : "";
  return {
    notice: `Renderte Mermaid ${outputLabel}${backendLabel}.`,
    error: null,
  };
}

function normalizeActionResultValue(value) {
  if (value == null) {
    return value;
  }

  if (typeof value === "string") {
    return value;
  }

  if (typeof value === "object") {
    if (typeof value.string === "string") {
      return value.string;
    }
    if (typeof value["&string"] === "string") {
      return value["&string"];
    }
  }

  return value;
}

function getReferences() {
  const bootstrap = portholeWebState.bootstrap;
  const configuration = bootstrap && bootstrap.configuration;
  const editorState = bootstrap && bootstrap.editorState ? bootstrap.editorState : null;
  const committed = configuration && Array.isArray(configuration.cellReferences)
    ? normalizeReferenceList(configuration.cellReferences)
    : [];
  const working = editorState && editorState.mode === "edit"
    ? normalizeReferenceList(editorState.workingReferences)
    : committed;
  const committedKeys = new Set(committed.map((entry) => `${entry.label}::${entry.endpoint}`));
  return working.map((entry) => ({
    ...entry,
    draft: !committedKeys.has(`${entry.label}::${entry.endpoint}`),
  }));
}

function getComponentPaletteItems() {
  const bootstrap = portholeWebState.bootstrap;
  return bootstrap && Array.isArray(bootstrap.componentPalette) ? bootstrap.componentPalette : [];
}

function availableFloatingPanelKeys(agentPanelContext = null) {
  const keys = ["components", "elements", "inspector"];
  if (agentPanelContext) {
    keys.push("agentSetup");
  }
  return keys;
}

function isAIGatewayReference(entry) {
  if (!entry || typeof entry.endpoint !== "string") {
    return false;
  }
  return entry.endpoint.trim().toLowerCase() === "cell:///aigateway";
}

function componentUsesAIGateway(component) {
  if (!component || !component.recipe || !Array.isArray(component.recipe.referenceTemplate)) {
    return false;
  }
  return component.recipe.referenceTemplate.some((entry) => isAIGatewayReference(entry));
}

function resolveAIGatewayPanelContext(references, selectedReference, armedComponent) {
  const aiReferences = Array.isArray(references) ? references.filter((entry) => isAIGatewayReference(entry)) : [];
  const activeReference = isAIGatewayReference(selectedReference) ? selectedReference : (aiReferences[0] || null);
  const armedAgentComponent = componentUsesAIGateway(armedComponent) ? armedComponent : null;

  if (!activeReference && !armedAgentComponent) {
    return null;
  }

  const referenceState = activeReference ? resolveAIGatewayReferenceState(activeReference.label) : {};
  return {
    reference: activeReference,
    state: referenceState,
    selectedReferenceActive: Boolean(activeReference && selectedReference && activeReference.label === selectedReference.label),
    availableReferenceCount: aiReferences.length,
    armedComponent: armedAgentComponent,
    armedOnly: !activeReference && Boolean(armedAgentComponent),
  };
}

function resolveAIGatewayReferenceState(label) {
  const referenceState = resolveReferenceState(label);
  if (referenceState && typeof referenceState.state === "object" && referenceState.state) {
    return referenceState.state;
  }
  return referenceState && typeof referenceState === "object" ? referenceState : {};
}

function composeAgentSetupDraftKey(label, fieldKey) {
  return `${String(label || "").trim()}::${String(fieldKey || "").trim()}`;
}

function setAgentSetupDraft(label, fieldKey, value) {
  const draftKey = composeAgentSetupDraftKey(label, fieldKey);
  if (!draftKey || draftKey === "::") {
    return;
  }
  portholeWebState.agentSetupDrafts[draftKey] = String(value ?? "");
}

function clearAgentSetupDraft(label, fieldKey) {
  delete portholeWebState.agentSetupDrafts[composeAgentSetupDraftKey(label, fieldKey)];
}

function agentSetupStateValue(label, fieldKey) {
  const state = resolveAIGatewayReferenceState(label);
  const draft = state && typeof state.draft === "object" ? state.draft : {};
  const setup = state && typeof state.setup === "object" ? state.setup : {};
  const normalizedField = String(fieldKey || "").trim();

  switch (normalizedField) {
    case "providerID":
    case "model":
    case "baseURL":
    case "apiKeyAlias":
    case "systemPrompt":
    case "prompt":
    case "temperatureText":
    case "maxTokensText":
      return typeof draft[normalizedField] === "string" ? draft[normalizedField] : "";
    case "requiresAPIKey":
    case "deterministicMode":
      return draft[normalizedField] === true ? "true" : "false";
    case "cachePolicy":
      return typeof draft.cachePolicy === "string" ? draft.cachePolicy : "useCache";
    case "apiKey":
      return "";
    case "statusLabel":
    case "nextStep":
    case "credentialStatus":
    case "storageHint":
    case "activeCredentialSource":
      return typeof setup[normalizedField] === "string" ? setup[normalizedField] : "";
    default:
      return "";
  }
}

function currentAgentSetupDraftValue(label, fieldKey) {
  const draftKey = composeAgentSetupDraftKey(label, fieldKey);
  if (Object.prototype.hasOwnProperty.call(portholeWebState.agentSetupDrafts, draftKey)) {
    return portholeWebState.agentSetupDrafts[draftKey];
  }
  return agentSetupStateValue(label, fieldKey);
}

function syncAgentSetupDraftsFromDOM(label) {
  const normalizedLabel = String(label || "").trim();
  if (!normalizedLabel) {
    return;
  }

  const selector = `[data-agent-setup-draft="true"][data-agent-label="${cssEscape(normalizedLabel)}"]`;
  document.querySelectorAll(selector).forEach((element) => {
    if (!(element instanceof HTMLInputElement || element instanceof HTMLTextAreaElement || element instanceof HTMLSelectElement)) {
      return;
    }
    const fieldKey = element.getAttribute("data-agent-field") || "";
    if (!fieldKey) {
      return;
    }
    setAgentSetupDraft(normalizedLabel, fieldKey, element.value || "");
  });
}

function readAgentSetupBoolean(label, fieldKey) {
  return currentAgentSetupDraftValue(label, fieldKey) === "true";
}

function buildAgentSetupRoutePayload(label) {
  return {
    providerID: currentAgentSetupDraftValue(label, "providerID").trim(),
    model: currentAgentSetupDraftValue(label, "model").trim(),
    baseURL: currentAgentSetupDraftValue(label, "baseURL").trim(),
    apiKeyAlias: currentAgentSetupDraftValue(label, "apiKeyAlias").trim(),
    requiresAPIKey: readAgentSetupBoolean(label, "requiresAPIKey"),
    deterministicMode: readAgentSetupBoolean(label, "deterministicMode"),
    cachePolicy: currentAgentSetupDraftValue(label, "cachePolicy").trim() || "useCache",
    temperatureText: currentAgentSetupDraftValue(label, "temperatureText").trim(),
    maxTokensText: currentAgentSetupDraftValue(label, "maxTokensText").trim(),
  };
}

async function syncAgentSetupRoute(label) {
  syncAgentSetupDraftsFromDOM(label);
  await runAction(`${label}.applyDraftProfile`, buildAgentSetupRoutePayload(label));
}

async function syncAgentSetupPrompts(label) {
  syncAgentSetupDraftsFromDOM(label);
  await runAction(`${label}.setDraftSystemPrompt`, currentAgentSetupDraftValue(label, "systemPrompt"));
  await runAction(`${label}.setDraftPrompt`, currentAgentSetupDraftValue(label, "prompt"));
}

async function syncAgentSetupSessionKey(label, options = {}) {
  syncAgentSetupDraftsFromDOM(label);
  const apiKey = currentAgentSetupDraftValue(label, "apiKey").trim();
  if (!apiKey) {
    portholeWebState.notice = "Paste an API key before loading or saving it.";
    render({ forceShell: true, preserveSkeletonDOM: true });
    return;
  }

  await runAction(`${label}.setDraftAPIKey`, apiKey);
  if (options.persist) {
    await runAction(`${label}.persistDraftAPIKey`, null);
  }
  clearAgentSetupDraft(label, "apiKey");
  render({ forceShell: true, preserveSkeletonDOM: true });
}

async function clearAgentSetupSessionKey(label) {
  clearAgentSetupDraft(label, "apiKey");
  await runAction(`${label}.clearDraftAPIKey`, null);
}

async function invokeAgentSetup(label) {
  syncAgentSetupDraftsFromDOM(label);
  await syncAgentSetupRoute(label);
  await syncAgentSetupPrompts(label);

  const apiKey = currentAgentSetupDraftValue(label, "apiKey").trim();
  if (apiKey) {
    await runAction(`${label}.setDraftAPIKey`, apiKey);
    clearAgentSetupDraft(label, "apiKey");
  }

  await runAction(`${label}.invokeDraft`, true);
  render({ forceShell: true, preserveSkeletonDOM: true });
}

function resolveComponentItem(source, index) {
  if (!Number.isInteger(index) || index < 0) {
    return null;
  }
  if (source === "panel") {
    return getComponentPaletteItems()[index] || null;
  }
  if (source === "palette") {
    return getFilteredComponentPaletteItems()[index] || null;
  }
  if (source === "library") {
    const entry = getFilteredLibraryEntries()[index] || null;
    return entry && entry.configuration ? makeLibraryComponentItem(entry.configuration, index) : null;
  }
  return null;
}

function getMenuConfiguration(menuKey, index) {
  const bootstrap = portholeWebState.bootstrap;
  if (!bootstrap || !bootstrap.menus || !Array.isArray(bootstrap.menus[menuKey])) {
    return null;
  }
  if (!Number.isInteger(index) || index < 0 || index >= bootstrap.menus[menuKey].length) {
    return null;
  }
  return bootstrap.menus[menuKey][index];
}

function getMenuEntries(menuKey) {
  const bootstrap = portholeWebState.bootstrap;
  if (!bootstrap || !bootstrap.menus || !Array.isArray(bootstrap.menus[menuKey])) {
    return [];
  }
  return rankMenuEntriesForPreferences(bootstrap.menus[menuKey]);
}

function rankMenuEntriesForPreferences(entries) {
  const normalizedEntries = entries
    .map((entry, index) => {
      if (!entry || typeof entry !== "object") {
        return null;
      }
      return { ...entry, __menuOriginalIndex: index };
    })
    .filter(Boolean);
  const criteria = normalizeMenuCriteriaText(
    normalizeMenuPreferences(portholeWebState.menuPreferences).criteriaText
  );
  if (!criteria) {
    return normalizedEntries;
  }

  const tokens = menuCriteriaTokens(criteria);
  if (tokens.length === 0) {
    return normalizedEntries;
  }

  const scored = normalizedEntries
    .map((entry) => ({ entry, score: menuCriteriaScore(entry, criteria, tokens) }))
    .filter((item) => item.score > 0)
    .sort((left, right) => {
      if (left.score !== right.score) {
        return right.score - left.score;
      }
      return (left.entry.__menuOriginalIndex || 0) - (right.entry.__menuOriginalIndex || 0);
    });

  return scored.length > 0 ? scored.map((item) => item.entry) : normalizedEntries;
}

function normalizeMenuCriteriaText(value) {
  return String(value || "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 240);
}

function menuCriteriaTokens(criteria) {
  const normalized = normalizeSearchText(criteria);
  const stopwords = new Set([
    "for", "med", "til", "som", "jeg", "vil", "ha", "vis", "mine", "min", "mitt",
    "the", "and", "with", "show", "want", "need", "menus", "meny", "menyer", "kriterier",
    "criteria", "porthole", "verktøy", "verktoy"
  ]);
  return normalized
    .split(/[^a-z0-9æøå]+/i)
    .map((token) => token.trim())
    .filter((token) => token.length >= 3 && !stopwords.has(token));
}

function normalizeSearchText(value) {
  return String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function menuCriteriaScore(entry, criteria, tokens) {
  const haystack = normalizeSearchText(menuEntrySearchText(entry));
  if (!haystack) {
    return 0;
  }
  let score = 0;
  const normalizedCriteria = normalizeSearchText(criteria);
  if (normalizedCriteria.length >= 4 && haystack.includes(normalizedCriteria)) {
    score += 8;
  }
  tokens.forEach((token) => {
    if (!haystack.includes(token)) {
      return;
    }
    score += 1;
    const name = normalizeSearchText(entry && entry.name ? entry.name : "");
    if (name.includes(token)) {
      score += 2;
    }
    const discovery = entry && entry.discovery && typeof entry.discovery === "object" ? entry.discovery : {};
    const purpose = normalizeSearchText(discovery.purpose || discovery.purposeDescription || "");
    if (purpose.includes(token)) {
      score += 2;
    }
  });
  return score;
}

function menuEntrySearchText(entry) {
  if (!entry || typeof entry !== "object") {
    return "";
  }
  const discovery = entry.discovery && typeof entry.discovery === "object" ? entry.discovery : {};
  const cellReferences = Array.isArray(entry.cellReferences) ? entry.cellReferences : [];
  const pieces = [
    entry.name,
    entry.description,
    discovery.purpose,
    discovery.purposeDescription,
    discovery.sourceCellEndpoint,
    discovery.appStoreScope,
    discovery.policyCategory,
    discovery.reviewSummary,
    discovery.universalLink,
    cellReferences.map((reference) => reference && reference.endpoint).join(" "),
  ];
  ["interests", "purposeRefs", "tags", "visibleActions"].forEach((key) => {
    const value = discovery[key];
    if (Array.isArray(value)) {
      pieces.push(value.join(" "));
    } else if (typeof value === "string") {
      pieces.push(value);
    }
  });
  return pieces.filter(Boolean).join(" ");
}

function getLibraryConfigurations() {
  const bootstrap = portholeWebState.bootstrap;
  const explicit = bootstrap && Array.isArray(bootstrap.availableConfigurations)
    ? bootstrap.availableConfigurations
    : [];

  const fallback = [];
  if (bootstrap && bootstrap.menus) {
    menuKeys.forEach((menuKey) => {
      const entries = Array.isArray(bootstrap.menus[menuKey]) ? bootstrap.menus[menuKey] : [];
      fallback.push(...entries);
    });
  }

  const combined = explicit.length > 0 ? explicit : fallback;
  const deduplicated = [];
  const seen = new Set();
  combined.forEach((entry) => {
    if (!entry || typeof entry !== "object") {
      return;
    }
    const discovery = entry.discovery && typeof entry.discovery === "object" ? entry.discovery : null;
    const endpoint = discovery && typeof discovery.sourceCellEndpoint === "string"
      ? discovery.sourceCellEndpoint
      : "";
    const name = typeof entry.name === "string" ? entry.name : "";
    const identity = `${endpoint.trim().toLowerCase()}::${name.trim().toLowerCase()}`;
    if (!identity || seen.has(identity)) {
      return;
    }
    seen.add(identity);
    deduplicated.push(entry);
  });
  return sortLibraryConfigurations(deduplicated);
}

function sortLibraryConfigurations(configurations) {
  return configurations.slice().sort((left, right) => {
    const leftHighlight = resolveConferenceFeatureMetadata(left);
    const rightHighlight = resolveConferenceFeatureMetadata(right);
    const leftRank = leftHighlight ? leftHighlight.rank : Number.MAX_SAFE_INTEGER;
    const rightRank = rightHighlight ? rightHighlight.rank : Number.MAX_SAFE_INTEGER;

    if (leftRank !== rightRank) {
      return leftRank - rightRank;
    }

    const leftName = left && typeof left.name === "string" ? left.name : "";
    const rightName = right && typeof right.name === "string" ? right.name : "";
    return leftName.localeCompare(rightName, undefined, { sensitivity: "base" });
  });
}

function resolveConferenceFeatureMetadata(configuration) {
  if (!configuration || typeof configuration !== "object") {
    return null;
  }
  const name = typeof configuration.name === "string" ? configuration.name.trim() : "";
  return name ? conferenceHighlightByName.get(name) || null : null;
}

function matchesLibraryQuery(configuration, query) {
  const haystacks = [
    configuration.name,
    productFacingConfigurationName(configuration.name),
    configuration.description,
    configuration.discovery && configuration.discovery.purpose,
    configuration.discovery && configuration.discovery.purposeDescription,
    configuration.discovery && configuration.discovery.sourceCellEndpoint,
  ]
    .filter((value) => typeof value === "string" && value.trim().length > 0)
    .map((value) => value.toLowerCase());

  return haystacks.some((value) => value.includes(query));
}

function matchesComponentQuery(component, query) {
  const haystacks = [
    component && component.title,
    component && component.subtitle,
    component && component.recipe && component.recipe.displayName,
    component && component.recipe && component.recipe.subtitle,
  ]
    .filter((value) => typeof value === "string" && value.trim().length > 0)
    .map((value) => value.toLowerCase());

  return haystacks.some((value) => value.includes(query));
}

function getFilteredLibraryEntries() {
  const query = String(portholeWebState.libraryQuery || "").trim().toLowerCase();
  const menuFilter = menuKeys.includes(portholeWebState.libraryMenuFilter)
    ? portholeWebState.libraryMenuFilter
    : "";
  const allowedIdentities = menuFilter
    ? new Set(getMenuEntries(menuFilter).map((entry) => menuConfigurationIdentity(entry)).filter(Boolean))
    : null;
  const configurations = getLibraryConfigurations();
  const matched = [];

  configurations.forEach((configuration, libraryIndex) => {
    if (allowedIdentities && !allowedIdentities.has(menuConfigurationIdentity(configuration))) {
      return;
    }
    if (query && !matchesLibraryQuery(configuration, query)) {
      return;
    }

    matched.push({
      configuration,
      libraryIndex,
    });
  });

  return matched.map((entry, filteredIndex) => ({
    ...entry,
    filteredIndex,
    feature: resolveConferenceFeatureMetadata(entry.configuration),
  }));
}

function getFilteredComponentPaletteItems() {
  const query = String(portholeWebState.libraryQuery || "").trim().toLowerCase();
  const components = getComponentPaletteItems();
  if (!query) {
    return components;
  }
  return components.filter((component) => matchesComponentQuery(component, query));
}

function canInsertConfigurationAsComponent(configuration) {
  return Boolean(configuration && typeof configuration === "object" && configuration.skeleton && typeof configuration.skeleton === "object");
}

function inferLibraryIcon(configuration) {
  const signal = [
    configuration && configuration.name,
    configuration && configuration.description,
    configuration && configuration.discovery && configuration.discovery.purpose,
    configuration && configuration.discovery && configuration.discovery.sourceCellEndpoint,
  ]
    .filter((value) => typeof value === "string" && value.trim().length > 0)
    .join(" ")
    .toLowerCase();

  if (signal.includes("chat")) {
    return "bubble.left.and.bubble.right.fill";
  }
  if (signal.includes("vault") || signal.includes("obsidian")) {
    return "books.vertical.fill";
  }
  if (signal.includes("rag") || signal.includes("assistant") || signal.includes("agent") || signal.includes("ai")) {
    return "sparkles.rectangle.stack.fill";
  }
  return "square.stack.3d.up.fill";
}

function makeLibraryComponentItem(configuration, index) {
  if (!canInsertConfigurationAsComponent(configuration)) {
    return null;
  }
  const title = typeof configuration.name === "string" && configuration.name.trim().length > 0
    ? productFacingConfigurationName(configuration.name)
    : `Komponent ${index + 1}`;
  const subtitle = typeof configuration.description === "string"
    ? configuration.description
    : "";
  const icon = inferLibraryIcon(configuration);
  const idSource = typeof configuration.uuid === "string" && configuration.uuid.trim().length > 0
    ? configuration.uuid.trim()
    : `${title}-${index}`;
  return {
    id: `library.${idSource}`,
    title,
    subtitle,
    icon,
    sourceKind: "library",
    recipe: {
      id: `library.${idSource}`,
      displayName: title,
      subtitle,
      icon,
      referenceTemplate: Array.isArray(configuration.cellReferences) ? configuration.cellReferences : [],
      skeletonTemplate: configuration.skeleton,
      supportedTargetKinds: ["root", "vstack", "hstack", "scrollview", "section", "grid", "zstack"],
      preferredDropBehavior: "appendIntoContainer",
    },
  };
}

async function requestConfigurationNavigation(payload, options = {}) {
  const targetEntry = normalizeConfigurationNavigationEntry(options.targetEntry)
    || buildConfigurationNavigationEntryFromPayload(payload);
  if (!targetEntry || !targetEntry.payload) {
    return;
  }
  if (portholeWebState.pendingLoad) {
    return;
  }

  const currentEntry = currentConfigurationNavigationEntry();

  if (options.closeMenus) {
    collapseAllMenus({ render: false });
  }
  if (options.closeLibrary) {
    portholeWebState.libraryOpen = false;
    portholeWebState.libraryQuery = "";
  }
  closeMenuSettings({ render: false });
  portholeWebState.armedComponent = null;
  portholeWebState.productChromeRevealed = false;
  portholeWebState.navigationPending = {
    mode: options.navigationMode === "pop" ? "pop" : "push",
    sourceEntry: currentEntry,
    targetEntry,
    targetIndex: Number.isInteger(options.targetIndex) ? options.targetIndex : -1,
  };
  portholeWebState.pendingLoad = {
    id: targetEntry.id || targetEntry.name.toLowerCase(),
    name: targetEntry.name,
    startedAt: Date.now(),
  };
  portholeWebState.fieldValueMemory = {};
  portholeWebState.notice = `Laster ${portholeWebState.pendingLoad.name} i Porthole…`;
  portholeWebState.error = null;
  render({ forceShell: true, preserveSkeletonDOM: true });

  const targetLookupPayload = normalizeConfigurationNavigationPayload(targetEntry.payload);
  const prefersCatalogLookup = Boolean(targetLookupPayload?.configurationLookup?.sourceCellEndpoint)
    || (options.navigationMode === "pop" && Boolean(targetLookupPayload?.configurationLookup?.uuid));
  const actionPayload = prefersCatalogLookup
    ? targetLookupPayload
    : isCellConfigurationNavigationPayload(targetEntry.payload)
      ? deepCloneValue(targetEntry.payload)
      : isCellConfigurationNavigationPayload(payload)
        ? deepCloneValue(payload)
        : normalizeConfigurationNavigationPayload(payload) || targetEntry.payload;
  await runAction("addConfiguration", actionPayload);
}

async function loadConfiguration(configuration, options = {}) {
  if (!configuration || typeof configuration !== "object") {
    return;
  }
  const targetEntry = buildConfigurationNavigationEntry(configuration);
  await requestConfigurationNavigation(configurationLookupPayload(configuration), {
    ...options,
    navigationMode: "push",
    targetEntry,
  });
}

function resolveConfigurationDisplayName(configuration) {
  if (!configuration || typeof configuration !== "object") {
    return "Konfigurasjon";
  }
  if (typeof configuration.name === "string" && configuration.name.trim().length > 0) {
    return productFacingConfigurationName(configuration.name);
  }
  const discovery = configuration.discovery && typeof configuration.discovery === "object"
    ? configuration.discovery
    : null;
  if (discovery && typeof discovery.purpose === "string" && discovery.purpose.trim().length > 0) {
    return discovery.purpose.trim();
  }
  return "Konfigurasjon";
}

function productFacingConfigurationName(value) {
  const name = typeof value === "string" ? value.trim() : "";
  return name === "Co-Pilot Chat" ? "Butler Chat" : name;
}

function configurationLookupPayload(configuration) {
  if (!configuration || typeof configuration !== "object") {
    return configuration;
  }

  const lookup = {};

  if (typeof configuration.uuid === "string" && configuration.uuid.trim().length > 0) {
    lookup.uuid = configuration.uuid.trim();
  }
  if (typeof configuration.name === "string" && configuration.name.trim().length > 0) {
    lookup.name = configuration.name.trim();
  }

  const discovery = configuration.discovery && typeof configuration.discovery === "object"
    ? configuration.discovery
    : null;
  if (discovery && typeof discovery.sourceCellEndpoint === "string" && discovery.sourceCellEndpoint.trim().length > 0) {
    lookup.sourceCellEndpoint = discovery.sourceCellEndpoint.trim();
  }

  return Object.keys(lookup).length > 0 ? { configurationLookup: lookup } : configuration;
}

function normalizeConfigurationLookup(lookup) {
  if (!lookup || typeof lookup !== "object") {
    return null;
  }

  const normalized = {};
  if (typeof lookup.uuid === "string" && lookup.uuid.trim().length > 0) {
    normalized.uuid = lookup.uuid.trim();
  }
  if (typeof lookup.name === "string" && lookup.name.trim().length > 0) {
    normalized.name = lookup.name.trim();
  }
  if (typeof lookup.sourceCellEndpoint === "string" && lookup.sourceCellEndpoint.trim().length > 0) {
    normalized.sourceCellEndpoint = lookup.sourceCellEndpoint.trim();
  }
  return Object.keys(normalized).length > 0 ? normalized : null;
}

function normalizeConfigurationNavigationPayload(payload) {
  if (!payload || typeof payload !== "object") {
    return null;
  }
  if (payload.configurationLookup && typeof payload.configurationLookup === "object") {
    const lookup = normalizeConfigurationLookup(payload.configurationLookup);
    return lookup ? { configurationLookup: lookup } : null;
  }
  const lookupPayload = configurationLookupPayload(payload);
  if (!lookupPayload || typeof lookupPayload !== "object") {
    return null;
  }
  if (lookupPayload.configurationLookup && typeof lookupPayload.configurationLookup === "object") {
    const lookup = normalizeConfigurationLookup(lookupPayload.configurationLookup);
    return lookup ? { configurationLookup: lookup } : null;
  }
  return null;
}

function isCellConfigurationNavigationPayload(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    return false;
  }
  const hasName = typeof payload.name === "string" && payload.name.trim().length > 0;
  const hasRenderableShape = Object.prototype.hasOwnProperty.call(payload, "skeleton")
    || Object.prototype.hasOwnProperty.call(payload, "cellReferences")
    || Object.prototype.hasOwnProperty.call(payload, "discovery")
    || Object.prototype.hasOwnProperty.call(payload, "description")
    || Object.prototype.hasOwnProperty.call(payload, "uuid");
  return hasName && hasRenderableShape;
}

function buildConfigurationNavigationEntryFromPayload(payload) {
  const normalizedPayload = normalizeConfigurationNavigationPayload(payload);
  if (!normalizedPayload) {
    return null;
  }
  const lookup = normalizedPayload.configurationLookup;
  const name = typeof lookup.name === "string" && lookup.name.trim().length > 0
    ? lookup.name.trim()
    : "Konfigurasjon";
  const identity = typeof lookup.uuid === "string" && lookup.uuid.trim().length > 0
    ? lookup.uuid.trim().toLowerCase()
    : `${typeof lookup.sourceCellEndpoint === "string" ? lookup.sourceCellEndpoint.trim().toLowerCase() : ""}::${name.toLowerCase()}`;
  return {
    id: identity || name.toLowerCase(),
    name,
    payload: normalizedPayload,
  };
}

function buildConfigurationNavigationEntry(configuration) {
  const entry = buildConfigurationNavigationEntryFromPayload(configuration);
  if (entry && isCellConfigurationNavigationPayload(configuration)) {
    entry.payload = deepCloneValue(configuration);
  }
  return entry;
}

function normalizeConfigurationNavigationEntry(entry) {
  if (!entry || typeof entry !== "object") {
    return null;
  }
  const rawPayload = entry.payload || entry;
  const fullConfigurationPayload = isCellConfigurationNavigationPayload(rawPayload)
    ? deepCloneValue(rawPayload)
    : null;
  const payload = normalizeConfigurationNavigationPayload(rawPayload);
  if (!payload) {
    return null;
  }
  const normalized = buildConfigurationNavigationEntryFromPayload(payload);
  if (!normalized) {
    return null;
  }
  if (typeof entry.name === "string" && entry.name.trim().length > 0) {
    normalized.name = entry.name.trim();
  }
  if (fullConfigurationPayload) {
    normalized.payload = fullConfigurationPayload;
  }
  return normalized;
}

function currentConfigurationNavigationEntry() {
  const configuration = portholeWebState.bootstrap && portholeWebState.bootstrap.configuration
    ? portholeWebState.bootstrap.configuration
    : null;
  return buildConfigurationNavigationEntry(configuration);
}

function prepareConfigurationNavigationContext(payload) {
  const explicitContext = portholeWebState.navigationPending && typeof portholeWebState.navigationPending === "object"
    ? portholeWebState.navigationPending
    : null;
  if (explicitContext && explicitContext.targetEntry) {
    return {
      mode: explicitContext.mode === "pop" ? "pop" : "push",
      sourceEntry: normalizeConfigurationNavigationEntry(explicitContext.sourceEntry),
      targetEntry: normalizeConfigurationNavigationEntry(explicitContext.targetEntry),
      targetIndex: Number.isInteger(explicitContext.targetIndex) ? explicitContext.targetIndex : -1,
    };
  }

  const targetEntry = buildConfigurationNavigationEntryFromPayload(payload);
  if (!targetEntry) {
    return null;
  }
  return {
    mode: "push",
    sourceEntry: currentConfigurationNavigationEntry(),
    targetEntry,
    targetIndex: -1,
  };
}

function commitConfigurationNavigationContext(context) {
  const normalizedContext = context && typeof context === "object"
    ? {
      mode: context.mode === "pop" ? "pop" : "push",
      sourceEntry: normalizeConfigurationNavigationEntry(context.sourceEntry),
      targetEntry: normalizeConfigurationNavigationEntry(context.targetEntry),
      targetIndex: Number.isInteger(context.targetIndex) ? context.targetIndex : -1,
    }
    : null;
  if (!normalizedContext || !normalizedContext.targetEntry) {
    portholeWebState.navigationPending = null;
    return;
  }

  const nextStack = Array.isArray(portholeWebState.navigationStack)
    ? portholeWebState.navigationStack
      .map((entry) => normalizeConfigurationNavigationEntry(entry))
      .filter(Boolean)
    : [];

  if (normalizedContext.mode === "pop") {
    const resolvedIndex = normalizedContext.targetIndex >= 0
      ? Math.min(normalizedContext.targetIndex, Math.max(nextStack.length - 1, 0))
      : nextStack.findIndex((entry) => entry.id === normalizedContext.targetEntry.id);
    if (resolvedIndex >= 0) {
      nextStack.splice(resolvedIndex);
    } else if (nextStack.length > 0) {
      nextStack.pop();
    }
  } else {
    const sourceEntry = normalizedContext.sourceEntry;
    if (sourceEntry && sourceEntry.id && sourceEntry.id !== normalizedContext.targetEntry.id) {
      const lastEntry = nextStack[nextStack.length - 1] || null;
      if (!lastEntry || lastEntry.id !== sourceEntry.id) {
        nextStack.push(sourceEntry);
      }
    }
  }

  portholeWebState.navigationStack = nextStack;
  portholeWebState.navigationPending = null;
}

async function navigateBackInHistory() {
  const targetIndex = Array.isArray(portholeWebState.navigationStack)
    ? portholeWebState.navigationStack.length - 1
    : -1;
  if (targetIndex < 0 || portholeWebState.pendingLoad) {
    return;
  }
  const targetEntry = normalizeConfigurationNavigationEntry(portholeWebState.navigationStack[targetIndex]);
  if (!targetEntry) {
    return;
  }
  await requestConfigurationNavigation(targetEntry.payload, {
    closeMenus: true,
    closeLibrary: true,
    navigationMode: "pop",
    targetEntry,
    targetIndex,
  });
}

async function navigateToHistoryIndex(index) {
  if (!Number.isInteger(index) || index < 0 || index >= portholeWebState.navigationStack.length || portholeWebState.pendingLoad) {
    return;
  }
  const targetEntry = normalizeConfigurationNavigationEntry(portholeWebState.navigationStack[index]);
  if (!targetEntry) {
    return;
  }
  await requestConfigurationNavigation(targetEntry.payload, {
    closeMenus: true,
    closeLibrary: true,
    navigationMode: "pop",
    targetEntry,
    targetIndex: index,
  });
}

function toggleMenu(menuKey) {
  if (!menuKeys.includes(menuKey)) {
    return;
  }

  closeMenuSettings({ render: false });
  const next = {};
  const willExpand = !Boolean(portholeWebState.expandedMenus[menuKey]);
  if (willExpand) {
    next[menuKey] = true;
  }
  portholeWebState.expandedMenus = next;
  render({ forceShell: true, preserveSkeletonDOM: true });
  if (willExpand) {
    focusFirstEdgeMenuItemSoon(menuKey);
  } else {
    focusEdgeMenuTriggerSoon(menuKey);
  }
}

function collapseAllMenus(options = {}) {
  if (Object.keys(portholeWebState.expandedMenus).length === 0) {
    return;
  }
  portholeWebState.expandedMenus = {};
  if (options.render !== false) {
    render({ forceShell: true, preserveSkeletonDOM: true });
  }
}

function hasExpandedMenus() {
  return Object.keys(portholeWebState.expandedMenus).some((key) => portholeWebState.expandedMenus[key]);
}

function handleMenuPrimaryAction(menuKey) {
  if (!menuKeys.includes(menuKey)) {
    return;
  }

  const entries = getMenuEntries(menuKey);
  if (entries.length === 0) {
    if (menuKey === "upperMidMenu") {
      collapseAllMenus({ render: false });
      closeMenuSettings({ render: false });
      portholeWebState.libraryOpen = true;
      render({ forceShell: true, preserveSkeletonDOM: true });
    }
    return;
  }

  if (entries.length === 1) {
    void loadConfiguration(entries[0], { closeMenus: true, closeLibrary: true });
    return;
  }

  toggleMenu(menuKey);
}

function openLibraryForMenu(menuKey) {
  if (!menuKeys.includes(menuKey)) {
    return;
  }
  collapseAllMenus({ render: false });
  closeMenuSettings({ render: false });
  portholeWebState.toolsPanelOpen = false;
  portholeWebState.toolbarOverflowOpen = false;
  portholeWebState.libraryMenuFilter = menuKey;
  portholeWebState.libraryQuery = "";
  portholeWebState.libraryOpen = true;
  render({ forceShell: true, preserveSkeletonDOM: true });
  focusLibraryQuerySoon();
}

function isEditModeActive() {
  return portholeWebState.mode === "edit";
}

function usesCompactConvenienceMenus() {
  return window.matchMedia(compactMenuViewportQuery).matches;
}

function menuConfigurationIdentity(configuration) {
  if (!configuration || typeof configuration !== "object") {
    return "";
  }
  const discovery = configuration.discovery && typeof configuration.discovery === "object"
    ? configuration.discovery
    : null;
  const endpoint = discovery && typeof discovery.sourceCellEndpoint === "string"
    ? discovery.sourceCellEndpoint.trim().toLowerCase()
    : "";
  const uuid = typeof configuration.uuid === "string" ? configuration.uuid.trim().toLowerCase() : "";
  const name = typeof configuration.name === "string" ? configuration.name.trim().toLowerCase() : "";
  return uuid || `${endpoint}::${name}`;
}

function renderConfigurationNavigation({ compact = false } = {}) {
  const stack = Array.isArray(portholeWebState.navigationStack)
    ? portholeWebState.navigationStack
      .map((entry) => normalizeConfigurationNavigationEntry(entry))
      .filter(Boolean)
    : [];
  const currentEntry = currentConfigurationNavigationEntry();
  if (!currentEntry && stack.length === 0) {
    return "";
  }
  const currentLabel = currentEntry ? productFacingConfigurationName(currentEntry.name) : "Porthole";
  const backDisabled = stack.length === 0 || Boolean(portholeWebState.pendingLoad) || Boolean(portholeWebState.pendingAction);

  if (compact) {
    return `
      <div class="toolbar-navigation compact" aria-label="Configuration stack">
        <button type="button" class="toolbar-navigation-back" data-action="navigation-back" ${backDisabled ? "disabled" : ""}>
          Tilbake
        </button>
        <div class="toolbar-navigation-stack compact">
          <span class="toolbar-navigation-current">${escapeHTML(currentLabel)}</span>
        </div>
      </div>
    `;
  }

  const visibleStart = Math.max(0, stack.length - 4);
  const visibleEntries = stack.slice(visibleStart);

  const crumbs = [];
  if (visibleStart > 0) {
    crumbs.push('<span class="toolbar-navigation-ellipsis" aria-hidden="true">…</span>');
  }
  visibleEntries.forEach((entry, offset) => {
    const absoluteIndex = visibleStart + offset;
    crumbs.push(`
      <button
        type="button"
        class="toolbar-navigation-entry"
        data-action="navigation-jump"
        data-navigation-index="${absoluteIndex}"
        title="Åpne ${escapeAttr(productFacingConfigurationName(entry.name))}"
      >
        ${escapeHTML(productFacingConfigurationName(entry.name))}
      </button>
    `);
    crumbs.push('<span class="toolbar-navigation-separator" aria-hidden="true">›</span>');
  });
  crumbs.push(`<span class="toolbar-navigation-current">${escapeHTML(currentLabel)}</span>`);

  return `
    <div class="toolbar-navigation" aria-label="Configuration stack">
      <button type="button" class="toolbar-navigation-back" data-action="navigation-back" ${backDisabled ? "disabled" : ""}>
        Tilbake
      </button>
      <div class="toolbar-navigation-stack">
        ${crumbs.join("")}
      </div>
    </div>
  `;
}

function getCompactConvenienceConfigurations() {
  const seen = new Set();
  const result = [];

  menuKeys.forEach((menuKey) => {
    getMenuEntries(menuKey).forEach((configuration) => {
      const identity = menuConfigurationIdentity(configuration);
      if (!identity || seen.has(identity)) {
        return;
      }
      seen.add(identity);
      result.push(configuration);
    });
  });

  return result.slice(0, 12);
}

function ensureFloatingPanelLayouts() {
  const defaults = defaultFloatingPanelLayouts();
  const next = { ...portholeWebState.panelLayouts };
  for (const [panelKey, layout] of Object.entries(defaults)) {
    if (!next[panelKey] || typeof next[panelKey] !== "object") {
      next[panelKey] = layout;
    }
  }
  portholeWebState.panelLayouts = next;
  clampFloatingPanelLayouts();
}

function ensureFloatingPanelPresentationState() {
  const nextVisibility = { ...portholeWebState.panelVisibility };
  const nextCollapsed = { ...portholeWebState.panelCollapsed };
  for (const panelKey of Object.keys(floatingPanelDefinitions)) {
    if (typeof nextVisibility[panelKey] !== "boolean") {
      nextVisibility[panelKey] = true;
    }
    if (typeof nextCollapsed[panelKey] !== "boolean") {
      nextCollapsed[panelKey] = false;
    }
  }
  portholeWebState.panelVisibility = nextVisibility;
  portholeWebState.panelCollapsed = nextCollapsed;
}

function resetFloatingPanelLayouts() {
  portholeWebState.panelLayouts = defaultFloatingPanelLayouts();
  ensureFloatingPanelPresentationState();
  clampFloatingPanelLayouts();
  persistFloatingPanelState();
}

function defaultFloatingPanelLayouts() {
  const top = floatingToolbarBottomOffset();
  const viewportWidth = window.innerWidth || 1440;

  return {
    components: buildDefaultFloatingPanelLayout("components", {
      x: 16,
      y: top,
    }),
    elements: buildDefaultFloatingPanelLayout("elements", {
      x: 16,
      y: top + 220,
    }),
    inspector: buildDefaultFloatingPanelLayout("inspector", {
      x: Math.max(16, viewportWidth - floatingPanelDefinitions.inspector.width - 16),
      y: top,
    }),
    agentSetup: buildDefaultFloatingPanelLayout("agentSetup", {
      x: Math.max(16, viewportWidth - floatingPanelDefinitions.agentSetup.width - 16),
      y: top + 240,
    }),
  };
}

function buildDefaultFloatingPanelLayout(panelKey, origin) {
  const definition = floatingPanelDefinitions[panelKey];
  return {
    x: origin.x,
    y: origin.y,
    width: definition.width,
    height: definition.height,
  };
}

function floatingToolbarBottomOffset() {
  const toolbar = document.querySelector(".toolbar");
  if (!(toolbar instanceof HTMLElement)) {
    return 88;
  }
  const rect = toolbar.getBoundingClientRect();
  return Math.max(88, Math.round(rect.bottom + 12));
}

function clampPanelLayout(layout, panelKey) {
  const definition = floatingPanelDefinitions[panelKey];
  const availableWidth = Math.max(140, window.innerWidth - 24);
  const availableHeight = Math.max(180, window.innerHeight - floatingToolbarBottomOffset() - 12);
  const minWidth = Math.min(definition.minWidth || definition.width, availableWidth);
  const minHeight = Math.min(definition.minHeight || definition.height, availableHeight);
  const requestedWidth = Number(layout.width) || definition.width;
  const requestedHeight = Number(layout.height) || definition.height;
  const width = Math.max(minWidth, Math.min(requestedWidth, availableWidth));
  const height = Math.max(minHeight, Math.min(requestedHeight, availableHeight));
  const minX = 8;
  const minY = floatingToolbarBottomOffset();
  const maxX = Math.max(minX, window.innerWidth - width - 8);
  const maxY = Math.max(minY, window.innerHeight - height - 8);
  return {
    x: Math.min(maxX, Math.max(minX, Math.round(Number(layout.x) || 0))),
    y: Math.min(maxY, Math.max(minY, Math.round(Number(layout.y) || 0))),
    width,
    height,
  };
}

function clampFloatingPanelLayouts() {
  const next = {};
  for (const panelKey of Object.keys(floatingPanelDefinitions)) {
    const current = portholeWebState.panelLayouts[panelKey] || buildDefaultFloatingPanelLayout(panelKey, { x: 16, y: floatingToolbarBottomOffset() });
    next[panelKey] = clampPanelLayout(current, panelKey);
  }
  portholeWebState.panelLayouts = next;
}

function setPanelVisibility(panelKey, isVisible) {
  if (!floatingPanelDefinitions[panelKey]) {
    return;
  }
  ensureFloatingPanelPresentationState();
  portholeWebState.panelVisibility[panelKey] = Boolean(isVisible);
  if (isVisible) {
    ensureFloatingPanelLayouts();
  }
  persistFloatingPanelState();
}

function togglePanelVisibility(panelKey) {
  if (!floatingPanelDefinitions[panelKey]) {
    return;
  }
  ensureFloatingPanelPresentationState();
  setPanelVisibility(panelKey, !portholeWebState.panelVisibility[panelKey]);
}

function togglePanelCollapsed(panelKey) {
  if (!floatingPanelDefinitions[panelKey]) {
    return;
  }
  ensureFloatingPanelPresentationState();
  portholeWebState.panelCollapsed[panelKey] = !portholeWebState.panelCollapsed[panelKey];
  persistFloatingPanelState();
}

function restoreFloatingPanelState() {
  const snapshot = readFloatingPanelState();
  if (!snapshot) {
    return;
  }

  if (snapshot.layouts && typeof snapshot.layouts === "object") {
    const nextLayouts = {};
    for (const panelKey of Object.keys(floatingPanelDefinitions)) {
      const rawLayout = snapshot.layouts[panelKey];
      if (!rawLayout || typeof rawLayout !== "object") {
        continue;
      }
      nextLayouts[panelKey] = {
        x: Number(rawLayout.x) || 0,
        y: Number(rawLayout.y) || 0,
        width: Number(rawLayout.width) || floatingPanelDefinitions[panelKey].width,
        height: Number(rawLayout.height) || floatingPanelDefinitions[panelKey].height,
      };
    }
    portholeWebState.panelLayouts = nextLayouts;
  }

  if (snapshot.visibility && typeof snapshot.visibility === "object") {
    const nextVisibility = {};
    for (const panelKey of Object.keys(floatingPanelDefinitions)) {
      if (typeof snapshot.visibility[panelKey] === "boolean") {
        nextVisibility[panelKey] = snapshot.visibility[panelKey];
      }
    }
    portholeWebState.panelVisibility = nextVisibility;
  }

  if (snapshot.collapsed && typeof snapshot.collapsed === "object") {
    const nextCollapsed = {};
    for (const panelKey of Object.keys(floatingPanelDefinitions)) {
      if (typeof snapshot.collapsed[panelKey] === "boolean") {
        nextCollapsed[panelKey] = snapshot.collapsed[panelKey];
      }
    }
    portholeWebState.panelCollapsed = nextCollapsed;
  }

  ensureFloatingPanelPresentationState();
  ensureFloatingPanelLayouts();
}

function readFloatingPanelState() {
  try {
    const storage = window.localStorage;
    if (!storage) {
      return null;
    }
    const raw = storage.getItem(floatingPanelPersistenceKey);
    if (!raw) {
      return null;
    }
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === "object" ? parsed : null;
  } catch (error) {
    console.warn("Failed to restore floating panel state", error);
    return null;
  }
}

function persistFloatingPanelState() {
  try {
    const storage = window.localStorage;
    if (!storage) {
      return;
    }
    const layouts = {};
    for (const panelKey of Object.keys(floatingPanelDefinitions)) {
      const layout = portholeWebState.panelLayouts[panelKey];
      if (!layout || typeof layout !== "object") {
        continue;
      }
      layouts[panelKey] = {
        x: Number(layout.x) || 0,
        y: Number(layout.y) || 0,
        width: Number(layout.width) || floatingPanelDefinitions[panelKey].width,
        height: Number(layout.height) || floatingPanelDefinitions[panelKey].height,
      };
    }
    storage.setItem(floatingPanelPersistenceKey, JSON.stringify({
      layouts,
      visibility: portholeWebState.panelVisibility,
      collapsed: portholeWebState.panelCollapsed,
    }));
  } catch (error) {
    console.warn("Failed to persist floating panel state", error);
  }
}

function normalizeMenuPreferences(value) {
  const normalized = {
    topExpansionStyle: "auto",
    bottomExpansionStyle: "auto",
    showTitles: true,
    criteriaText: "",
  };

  if (!value || typeof value !== "object") {
    return normalized;
  }

  if (menuExpansionStyleOptions.includes(value.topExpansionStyle)) {
    normalized.topExpansionStyle = value.topExpansionStyle;
  }
  if (menuExpansionStyleOptions.includes(value.bottomExpansionStyle)) {
    normalized.bottomExpansionStyle = value.bottomExpansionStyle;
  }
  if (typeof value.showTitles === "boolean") {
    normalized.showTitles = value.showTitles;
  }
  if (typeof value.criteriaText === "string") {
    normalized.criteriaText = normalizeMenuCriteriaText(value.criteriaText);
  }

  return normalized;
}

function restoreMenuPreferences() {
  try {
    const storage = window.localStorage;
    if (!storage) {
      portholeWebState.menuPreferences = normalizeMenuPreferences(portholeWebState.menuPreferences);
      return;
    }
    const raw = storage.getItem(menuPreferencesPersistenceKey);
    if (!raw) {
      portholeWebState.menuPreferences = normalizeMenuPreferences(portholeWebState.menuPreferences);
      return;
    }
    portholeWebState.menuPreferences = normalizeMenuPreferences(JSON.parse(raw));
  } catch (error) {
    console.warn("Failed to restore menu preferences", error);
    portholeWebState.menuPreferences = normalizeMenuPreferences(portholeWebState.menuPreferences);
  }
}

function persistMenuPreferences() {
  try {
    const storage = window.localStorage;
    if (!storage) {
      return;
    }
    storage.setItem(
      menuPreferencesPersistenceKey,
      JSON.stringify(normalizeMenuPreferences(portholeWebState.menuPreferences))
    );
  } catch (error) {
    console.warn("Failed to persist menu preferences", error);
  }
}

function restoreEdgeMenuVisibility() {
  try {
    const raw = window.localStorage && window.localStorage.getItem(edgeMenuVisibilityPersistenceKey);
    if (raw === "true") {
      portholeWebState.edgeMenusSuppressed = false;
    } else if (raw === "false") {
      portholeWebState.edgeMenusSuppressed = true;
    }
  } catch (error) {
    console.warn("Kunne ikke lese synlighet for kantmenyer", error);
  }
}

function setEdgeMenusVisible(visible, { persist = true } = {}) {
  portholeWebState.edgeMenusSuppressed = !visible;
  if (!visible) {
    portholeWebState.expandedMenus = {};
    removeRenderedEdgeMenus();
  }
  if (!persist) {
    return;
  }
  try {
    if (window.localStorage) {
      window.localStorage.setItem(edgeMenuVisibilityPersistenceKey, visible ? "true" : "false");
    }
  } catch (error) {
    console.warn("Kunne ikke lagre synlighet for kantmenyer", error);
  }
}

function updateMenuPreference(key, value) {
  const next = {
    ...normalizeMenuPreferences(portholeWebState.menuPreferences),
    [key]: value,
  };
  portholeWebState.menuPreferences = normalizeMenuPreferences(next);
  persistMenuPreferences();
  render({ forceShell: true, preserveSkeletonDOM: true });
}

function closeMenuSettings(options = {}) {
  if (!portholeWebState.menuSettingsOpen) {
    return;
  }
  portholeWebState.menuSettingsOpen = false;
  if (options.render !== false) {
    render({ forceShell: true, preserveSkeletonDOM: true });
  }
}

function toggleMenuSettings() {
  const willOpen = !portholeWebState.menuSettingsOpen;
  if (willOpen) {
    collapseAllMenus({ render: false });
  }
  portholeWebState.menuSettingsOpen = willOpen;
  render({ forceShell: true, preserveSkeletonDOM: true });
}

// Render regime: shell/chrome work preserves the live skeleton root by default.
// Only runAction may opt into replacing it, via the explicit replaceSkeleton flag.
function render({ forceShell = false, preserveSkeletonDOM = true, replaceSkeleton = false } = {}) {
  const root = document.getElementById("porthole-webo-app");
  if (!root) {
    return;
  }

  if (portholeWebState.loading && !portholeWebState.bootstrap) {
    root.innerHTML = `
      <section class="porthole-loading">
        <h1>Porthole</h1>
        <p>Laster porthole…</p>
      </section>
    `;
    portholeWebState.shellSignature = null;
    updateStatusLiveRegion();
    return;
  }

  const nextShellSignature = buildShellSignature();
  const needsShellRender =
    forceShell ||
    portholeWebState.shellSignature !== nextShellSignature ||
    !(root.querySelector("#porthole-skeleton-root") instanceof HTMLElement);
  const focusSnapshot = needsShellRender ? captureRenderableFocusState(root) : null;
  if (preserveSkeletonDOM === false && replaceSkeleton !== true) {
    console.warn("Ignoring unsafe preserveSkeletonDOM:false without replaceSkeleton:true.");
  }
  const preservedSkeletonRoot = needsShellRender && !replaceSkeleton
    ? root.querySelector("#porthole-skeleton-root")
    : null;

  try {
    if (needsShellRender) {
      const nextShellHTML = renderShell();
      if (preservedSkeletonRoot instanceof HTMLElement) {
        const didPreserveMountedSkeleton = replaceShellChromeAroundMountedSkeleton(
          root,
          preservedSkeletonRoot,
          nextShellHTML
        );
        if (!didPreserveMountedSkeleton) {
          throw new Error("Kunne ikke oppdatere Porthole-chrome uten aa koble fra skeleton-DOM.");
        }
        portholeWebState.rendererRoot = preservedSkeletonRoot;
      } else {
        root.innerHTML = nextShellHTML;
      }
      portholeWebState.shellSignature = nextShellSignature;
      restoreRenderableFocusState(root, focusSnapshot);
    }

    renderSkeletonCanvas();
    updateStatusLiveRegion();
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error("Porthole render failed", error);
    portholeWebState.error = message;
    portholeWebState.shellSignature = null;
    if (root.querySelector("#porthole-skeleton-root") instanceof HTMLElement) {
      renderSkeletonValidationDiagnostic(message);
      updateStatusLiveRegion();
      return;
    }
    root.innerHTML = `
      <section class="porthole-loading">
        <h1>Porthole</h1>
        <p>Klientfeil i Porthole-rendering.</p>
        <p class="error">${escapeHTML(message)}</p>
      </section>
    `;
    updateStatusLiveRegion();
  }
}

function replaceShellChromeAroundMountedSkeleton(root, skeletonRoot, nextShellHTML) {
  if (typeof document.createElement !== "function") {
    return false;
  }
  const template = document.createElement("template");
  template.innerHTML = nextShellHTML;
  const nextSkeletonRoot = template.content.querySelector("#porthole-skeleton-root");
  const currentCanvas = skeletonRoot.closest("section.canvas");
  const nextCanvas = nextSkeletonRoot && nextSkeletonRoot.closest("section.canvas");
  if (
    !(currentCanvas instanceof HTMLElement) ||
    !(nextCanvas instanceof HTMLElement) ||
    currentCanvas.parentNode !== root ||
    nextCanvas.parentNode !== template.content
  ) {
    return false;
  }

  synchronizeElementAttributes(currentCanvas, nextCanvas);
  synchronizeElementAttributes(skeletonRoot, nextSkeletonRoot);
  replaceSiblingsWhileKeepingNodeMounted(currentCanvas, skeletonRoot, nextCanvas, nextSkeletonRoot);
  replaceSiblingsWhileKeepingNodeMounted(root, currentCanvas, template.content, nextCanvas);
  return skeletonRoot.isConnected && skeletonRoot.parentNode === currentCanvas;
}

function synchronizeElementAttributes(currentElement, nextElement) {
  Array.from(currentElement.attributes).forEach((attribute) => {
    if (!nextElement.hasAttribute(attribute.name)) {
      currentElement.removeAttribute(attribute.name);
    }
  });
  Array.from(nextElement.attributes).forEach((attribute) => {
    if (currentElement.getAttribute(attribute.name) !== attribute.value) {
      currentElement.setAttribute(attribute.name, attribute.value);
    }
  });
}

function replaceSiblingsWhileKeepingNodeMounted(
  currentParent,
  mountedNode,
  nextParent,
  nextMountedNode
) {
  const before = document.createDocumentFragment();
  const after = document.createDocumentFragment();
  let foundMountedNode = false;
  Array.from(nextParent.childNodes).forEach((child) => {
    if (child === nextMountedNode) {
      foundMountedNode = true;
      return;
    }
    (foundMountedNode ? after : before).appendChild(child.cloneNode(true));
  });
  if (!foundMountedNode) {
    throw new Error("Nytt Porthole-shell mangler skeleton-plassholder.");
  }

  Array.from(currentParent.childNodes).forEach((child) => {
    if (child !== mountedNode) {
      child.remove();
    }
  });
  currentParent.insertBefore(before, mountedNode);
  currentParent.appendChild(after);
}

function captureRenderableFocusState(root) {
  const activeElement = document.activeElement;
  if (!(activeElement instanceof HTMLElement) || !root.contains(activeElement)) {
    return null;
  }

  const selector = focusRestoreSelectorForElement(activeElement);
  if (!selector) {
    return null;
  }

  const snapshot = { selector };
  if (activeElement instanceof HTMLInputElement || activeElement instanceof HTMLTextAreaElement) {
    snapshot.selectionStart = activeElement.selectionStart;
    snapshot.selectionEnd = activeElement.selectionEnd;
    snapshot.selectionDirection = activeElement.selectionDirection;
  }
  return snapshot;
}

function restoreRenderableFocusState(root, snapshot) {
  if (!snapshot || !snapshot.selector) {
    return;
  }

  const element = querySelectorSafe(root, snapshot.selector);
  if (!(element instanceof HTMLElement)) {
    return;
  }

  element.focus({ preventScroll: true });

  if ((element instanceof HTMLInputElement || element instanceof HTMLTextAreaElement) &&
      typeof snapshot.selectionStart === "number" &&
      typeof snapshot.selectionEnd === "number") {
    try {
      element.setSelectionRange(
        snapshot.selectionStart,
        snapshot.selectionEnd,
        snapshot.selectionDirection || "none",
      );
    } catch (error) {
      // Some input types do not support setSelectionRange.
    }
  }
}

function focusRestoreSelectorForElement(element) {
  if (!(element instanceof HTMLElement)) {
    return null;
  }

  const focusKey = element.getAttribute("data-focus-key");
  if (focusKey) {
    return `[data-focus-key="${cssEscape(focusKey)}"]`;
  }

  if (element.getAttribute("data-library-query") === "true") {
    return '[data-library-query="true"]';
  }

  const menuSetting = element.getAttribute("data-menu-setting");
  if (menuSetting) {
    return `[data-menu-setting="${cssEscape(menuSetting)}"]`;
  }

  const menuToggle = element.getAttribute("data-menu-setting-toggle");
  if (menuToggle) {
    return `[data-menu-setting-toggle="${cssEscape(menuToggle)}"]`;
  }
  const menuText = element.getAttribute("data-menu-setting-text");
  if (menuText) {
    return `[data-menu-setting-text="${cssEscape(menuText)}"]`;
  }

  if (element.id) {
    return `#${cssEscape(element.id)}`;
  }

  return null;
}

function focusLibraryQuerySoon() {
  window.requestAnimationFrame(() => {
    const queryInput = document.querySelector('[data-library-query="true"]');
    if (!(queryInput instanceof HTMLInputElement)) {
      return;
    }
    queryInput.focus({ preventScroll: true });
    const value = String(queryInput.value || "");
    try {
      queryInput.setSelectionRange(value.length, value.length, "none");
    } catch (error) {
      // Search inputs may reject selection handling in some engines.
    }
  });
}

function focusFirstEdgeMenuItemSoon(menuKey) {
  window.requestAnimationFrame(() => {
    const item = document.querySelector(`#${cssEscape(edgeMenuItemsId(menuKey))} [role="menuitem"]`);
    if (item instanceof HTMLElement) {
      item.focus({ preventScroll: true });
    }
  });
}

function focusEdgeMenuTriggerSoon(menuKey) {
  window.requestAnimationFrame(() => {
    const trigger = document.getElementById(edgeMenuTriggerId(menuKey));
    if (trigger instanceof HTMLElement) {
      trigger.focus({ preventScroll: true });
    }
  });
}

function updateStatusLiveRegion() {
  updateSyncStatusBadge();
  const liveRegion = document.getElementById("porthole-status-live");
  if (!(liveRegion instanceof HTMLElement)) {
    return;
  }
  let message = "";
  if (portholeWebState.error) {
    message = `Feil: ${portholeWebState.error}`;
  } else if (portholeWebState.pendingLoad) {
    message = `Laster ${portholeWebState.pendingLoad.name}.`;
  } else if (portholeWebState.pendingAction) {
    message = "Porthole arbeider med handlingen.";
  } else if (portholeWebState.notice) {
    message = portholeWebState.notice;
  } else if (portholeWebState.loading || portholeWebState.refreshInFlight) {
    message = "Porthole oppdateres.";
  }
  if (liveRegion.textContent !== message) {
    liveRegion.textContent = message;
  }
}

// R1 (godkjent av Kjetil 2026-08-28): tema-CSS per konfigurasjon.
// Naar en konfigurasjon er aktiv forsoeker Porthole aa laste
// /css/themes/<konfigurasjonsnavn>.css. Finnes ikke filen, fjernes lenken
// stille (onerror) og flaten rendres med standardstilene. Temaet skal kun
// style skeleton-innholdet via styleClasses/sk-font-*-klasser, scopet til
// #porthole-skeleton-root — aldri Porthole-chromen.
let appliedConfigurationThemeName = null;
function syncConfigurationTheme(configurationName) {
  const name = typeof configurationName === "string" ? configurationName.trim() : "";
  if (name === appliedConfigurationThemeName) {
    return;
  }
  appliedConfigurationThemeName = name;
  let link = document.getElementById("porthole-configuration-theme");
  if (!name || name === "Porthole") {
    if (link) { link.remove(); }
    return;
  }
  const href = `/css/themes/${encodeURIComponent(name)}.css`;
  if (!link) {
    link = document.createElement("link");
    link.id = "porthole-configuration-theme";
    link.rel = "stylesheet";
    link.addEventListener("error", () => { link.remove(); });
    document.head.appendChild(link);
  }
  if (link.getAttribute("href") !== href) {
    link.setAttribute("href", href);
  }
}

function renderShell() {
  const bootstrap = portholeWebState.bootstrap;
  const editorState = bootstrap && bootstrap.editorState ? bootstrap.editorState : normalizeEditorState(null, null);
  const mode = editorState.mode;
  const editModeActive = mode === "edit";
  const editorAccessNotice = resolveEditorAccessNotice(editorState);
  const references = getReferences();
  const selected = references.find((entry) => entry.label === portholeWebState.selectedLabel) || null;
  const availableConfigurations = getLibraryConfigurations();
  const coPilotChatConfiguration = findCoPilotChatConfiguration();
  const pendingLoad = portholeWebState.pendingLoad;
  const pendingAction = portholeWebState.pendingAction;
  const activeConfigurationName = bootstrap && bootstrap.configuration && bootstrap.configuration.name
    ? bootstrap.configuration.name
    : "Porthole";
  const displayedConfigurationName = pendingLoad
    ? `${pendingLoad.name} (laster…)`
    : activeConfigurationName;
  syncConfigurationTheme(activeConfigurationName);
  const armedComponent = portholeWebState.armedComponent;
  const editorRoot = editModeActive
    ? resolveEditorSkeletonRoot(editorState, bootstrap && bootstrap.configuration ? bootstrap.configuration : null)
    : null;
  const treeNodes = editModeActive ? linearizeSkeletonNodes(editorRoot) : [];
  const selectedNode = editModeActive ? resolveSkeletonNodeByPath(editorRoot, editorState.selectionPath) : null;
  const componentItems = editModeActive ? getComponentPaletteItems() : [];
  const agentPanelContext = editModeActive
    ? resolveAIGatewayPanelContext(references, selected, armedComponent)
    : null;
  const compactMenusActive = usesCompactConvenienceMenus();
  const showToolbarDetails = portholeWebState.toolbarDetailsExpanded;

  const isConferenceConfiguration = /^Conference(?:\s|$)/.test(String(activeConfigurationName || ""))
    || activeConfigurationName === "Arendalsuka Participant Program";
  const isProductSurfaceConfiguration = isProductSurfaceConfigurationName(activeConfigurationName);
  const hasConfigurationNavigationHistory = Array.isArray(portholeWebState.navigationStack)
    && portholeWebState.navigationStack.length > 0;
  const suppressProductChrome = mode === "view"
    && isProductSurfaceConfiguration
    && !portholeWebState.productChromeRevealed
    && !hasConfigurationNavigationHistory;
  const suppressEdgeMenus = compactMenusActive || suppressProductChrome || portholeWebState.edgeMenusSuppressed;
  const canvasClass = [
    "canvas",
    mode === "edit" ? "edit-mode" : "view-mode",
    isConferenceConfiguration ? "conference-view" : "",
    isProductSurfaceConfiguration ? "product-view" : "",
  ].filter(Boolean).join(" ");
  const editPanelsClass = mode === "edit" ? "edit-panels visible" : "edit-panels";

  return `
    ${suppressProductChrome ? "" : `<header class="toolbar ${showToolbarDetails ? "expanded" : "compact"}">
      <div class="toolbar-primary">
        <div class="toolbar-title-block">
          <div class="toolbar-kicker-row">
            <span class="toolbar-kicker">Porthole</span>
            ${renderSyncStatusBadge({ pendingLoad, pendingAction })}
          </div>
          ${showToolbarDetails ? "" : renderConfigurationNavigation({ compact: true })}
        </div>
        <div class="toolbar-right" aria-label="Porthole-verktøylinje">
          <button
            data-action="open-copilot-chat"
            class="toolbar-action-copilot ${activeConfigurationName === "Co-Pilot Chat" ? "active" : ""}"
            ${pendingLoad || !coPilotChatConfiguration ? "disabled" : ""}
            title="Gå til den sentrale chatflaten"
          >Butler Chat</button>
          <button
            data-action="toggle-library"
            class="toolbar-desktop-action ${portholeWebState.libraryOpen ? "active" : ""}"
            aria-expanded="${portholeWebState.libraryOpen ? "true" : "false"}"
            aria-controls="porthole-library-panel"
            ${pendingLoad ? "disabled" : ""}
          >
            Bibliotek${availableConfigurations.length ? ` (${availableConfigurations.length})` : ""}
          </button>
          <div class="toolbar-mode-group toolbar-desktop-action" role="group" aria-label="Modus">
            <button data-action="mode-view" class="${mode === "view" ? "active" : ""}" aria-pressed="${mode === "view" ? "true" : "false"}">Vis</button>
            <button
              data-action="mode-edit"
              class="${[mode === "edit" ? "active" : "", editorAccessNotice && editorAccessNotice.blocked ? "blocked" : ""].filter(Boolean).join(" ")}"
              aria-pressed="${mode === "edit" ? "true" : "false"}"
              title="${editorAccessNotice ? escapeAttr(editorAccessNotice.message) : ""}"
            >Rediger</button>
          </div>
          <button
            data-action="toggle-tools-panel"
            class="${portholeWebState.toolsPanelOpen ? "active" : ""}"
            aria-expanded="${portholeWebState.toolsPanelOpen ? "true" : "false"}"
            aria-controls="porthole-tools-panel"
          >Verktøy</button>
          ${mode === "edit" ? `<button class="toolbar-primary-apply" data-action="editor-apply" ${editorState.isDirty ? "" : "disabled"}>Bruk</button>` : ""}
          <div class="toolbar-overflow-anchor">
            <button
              data-action="toggle-toolbar-overflow"
              class="${portholeWebState.toolbarOverflowOpen ? "active" : ""}"
              aria-expanded="${portholeWebState.toolbarOverflowOpen ? "true" : "false"}"
              aria-controls="porthole-toolbar-overflow"
            >Mer</button>
            ${renderToolbarOverflow({ mode, editorState, editorAccessNotice, availableConfigurations, pendingLoad, showToolbarDetails })}
          </div>
        </div>
      </div>
      ${showToolbarDetails ? renderToolbarDetails({ bootstrap, pendingLoad, pendingAction, mode, editorState, agentPanelContext }) : ""}
      ${renderEditorAccessBanner(editorAccessNotice, { showAllowed: mode === "edit" })}
    </header>`}

    ${!suppressProductChrome ? renderToolsPanel() : ""}

    ${!suppressProductChrome && portholeWebState.notice ? `<p class="notice">${escapeHTML(portholeWebState.notice)}</p>` : ""}
    ${portholeWebState.error ? `<p class="error">${escapeHTML(portholeWebState.error)}</p>` : ""}
    ${suppressProductChrome ? "" : renderAssistantDegradationBanner()}
    ${renderPendingLoadBanner(pendingLoad)}
    ${renderPendingActionBanner(pendingAction)}
    ${renderArmedComponentBanner(armedComponent, mode)}
    <section class="${canvasClass} ${pendingLoad ? "busy" : ""}" data-active-configuration="${escapeAttr(activeConfigurationName)}">
      ${suppressEdgeMenus ? "" : renderEdgeMenusOverlay()}
      ${renderLibraryPanel()}
      ${renderConfigurationJSONPanel()}
      ${renderNotificationOverlay()}
      <div id="porthole-skeleton-root" class="skeleton-host"></div>
      ${renderCanvasLoadOverlay(pendingLoad)}
      ${renderEmptyState()}
    </section>

    ${renderFloatingPanels({
      editPanelsClass,
      componentItems,
      armedComponent,
      treeNodes,
      selectionPath: editorState.selectionPath,
      references,
      selectedNode,
      selectedReference: selected,
      agentPanelContext,
    })}
  `;
}

function renderToolbarDetails({ bootstrap, pendingLoad, pendingAction, mode, editorState, agentPanelContext }) {
  const sessionId = bootstrap && bootstrap.sessionId ? bootstrap.sessionId : "";
  return `
    <div id="porthole-toolbar-details" class="toolbar-details">
      <div class="toolbar-details-copy">
        ${sessionId ? `<span class="session">${escapeHTML(sessionId)}</span>` : ""}
        <p class="active-configuration">
          Aktiv konfigurasjon:
          <strong>${escapeHTML(pendingLoad ? `${productFacingConfigurationName(pendingLoad.name)} (laster…)` : (bootstrap && bootstrap.configuration && bootstrap.configuration.name ? productFacingConfigurationName(bootstrap.configuration.name) : "Porthole"))}</strong>
        </p>
        ${renderConfigurationNavigation()}
      </div>
      <div class="toolbar-details-meta">
        ${renderRequesterSummaryBadge()}
      </div>
      <div class="toolbar-details-actions">
        ${renderMenuSettingsControl()}
        <button data-action="refresh">Oppdater</button>
        ${mode === "edit" ? renderPanelVisibilityControls(agentPanelContext) : ""}
        ${mode === "edit" ? '<button data-action="reset-panel-layout">Tilbakestill paneler</button>' : ""}
        ${mode === "edit" ? `<button data-action="editor-undo" ${editorState.canUndo ? "" : "disabled"}>Angre</button>` : ""}
        ${mode === "edit" ? `<button data-action="editor-redo" ${editorState.canRedo ? "" : "disabled"}>Gjør om</button>` : ""}
        ${mode === "edit" ? `<button data-action="editor-discard" ${editorState.isDirty ? "" : "disabled"}>Forkast</button>` : ""}
      </div>
    </div>
  `;
}

function renderToolbarOverflow({ mode, editorState, editorAccessNotice, availableConfigurations, pendingLoad, showToolbarDetails }) {
  if (!portholeWebState.toolbarOverflowOpen) {
    return "";
  }
  return `
    <div id="porthole-toolbar-overflow" class="toolbar-popover toolbar-overflow-popover">
      <div class="toolbar-overflow-mobile" role="group" aria-label="Modus og bibliotek">
        <button data-action="toggle-library" aria-expanded="${portholeWebState.libraryOpen ? "true" : "false"}" aria-controls="porthole-library-panel" ${pendingLoad ? "disabled" : ""}>
          Bibliotek${availableConfigurations.length ? ` (${availableConfigurations.length})` : ""}
        </button>
        <button data-action="mode-view" aria-pressed="${mode === "view" ? "true" : "false"}">Vis</button>
        <button data-action="mode-edit" aria-pressed="${mode === "edit" ? "true" : "false"}" class="${editorAccessNotice && editorAccessNotice.blocked ? "blocked" : ""}">Rediger</button>
      </div>
      <button data-action="toggle-toolbar-details" aria-expanded="${showToolbarDetails ? "true" : "false"}" aria-controls="porthole-toolbar-details">
        ${showToolbarDetails ? "Skjul detaljer" : "Vis detaljer"}
      </button>
      <button data-action="refresh">Oppdater</button>
      ${mode === "edit" ? `<button data-action="editor-undo" ${editorState.canUndo ? "" : "disabled"}>Angre</button>` : ""}
      ${mode === "edit" ? `<button data-action="editor-redo" ${editorState.canRedo ? "" : "disabled"}>Gjør om</button>` : ""}
      ${mode === "edit" ? `<button data-action="editor-discard" ${editorState.isDirty ? "" : "disabled"}>Forkast endringer</button>` : ""}
    </div>
  `;
}

function renderToolsPanel() {
  if (!portholeWebState.toolsPanelOpen) {
    return "";
  }
  return `
    <aside id="porthole-tools-panel" class="tools-panel" aria-label="Verktøy og menyflater">
      <div class="tools-panel-header">
        <div>
          <h2>Verktøy</h2>
          <p>Alle de seks menyfeltene er tilgjengelige her, også på små skjermer.</p>
        </div>
        <button data-action="toggle-tools-panel">Lukk</button>
      </div>
      <div class="tools-panel-actions">
        <button data-action="toggle-edge-menu-visibility" aria-pressed="${portholeWebState.edgeMenusSuppressed ? "false" : "true"}">
          ${portholeWebState.edgeMenusSuppressed ? "Vis kantmenyer" : "Skjul kantmenyer"}
        </button>
        <button data-action="toggle-library" aria-expanded="${portholeWebState.libraryOpen ? "true" : "false"}" aria-controls="porthole-library-panel">Åpne bibliotek</button>
      </div>
      <div class="tools-menu-groups">
        ${menuKeys.map((menuKey) => renderToolsMenuGroup(menuKey)).join("")}
      </div>
      <details class="tools-advanced">
        <summary>Avanserte menyvalg</summary>
        <div class="tools-advanced-fields">${renderMenuSettingsFields()}</div>
      </details>
    </aside>
  `;
}

function renderToolsMenuGroup(menuKey) {
  const entries = getMenuEntries(menuKey);
  const visual = menuVisuals[menuKey] || { label: "Meny" };
  const preview = entries.slice(0, 5);
  return `
    <section class="tools-menu-group" aria-labelledby="tools-${escapeAttr(menuKey)}-title">
      <div class="tools-menu-group-header">
        <h3 id="tools-${escapeAttr(menuKey)}-title">${escapeHTML(visual.label)}</h3>
        <span>${entries.length}</span>
      </div>
      ${preview.length === 0 ? `<p class="tools-menu-empty">Ingen tilgjengelige flater.</p>` : `
        <div class="tools-menu-list">
          ${preview.map((entry, index) => `
            <button data-action="menu-add" data-menu-key="${escapeAttr(menuKey)}" data-menu-index="${Number.isInteger(entry.__menuOriginalIndex) ? entry.__menuOriginalIndex : index}">
              <span>${escapeHTML(productFacingConfigurationName(entry.name) || "Navnløs konfigurasjon")}</span>
            </button>
          `).join("")}
        </div>
      `}
      ${entries.length > preview.length ? `<button class="tools-show-all" data-action="menu-show-all" data-menu-key="${escapeAttr(menuKey)}">Vis alle ${entries.length}</button>` : ""}
    </section>
  `;
}

function renderEditorAccessBanner(accessNotice, options = {}) {
  if (!accessNotice) {
    return "";
  }
  if (!accessNotice.blocked && options.showAllowed !== true) {
    return "";
  }
  const tone = accessNotice.blocked ? "blocked" : "ok";
  const title = accessNotice.blocked ? "Kun lesing" : "Kildebasert redigering";
  return `
    <div class="editor-access-banner ${tone}">
      <strong>${escapeHTML(title)}</strong>
      <span>${escapeHTML(accessNotice.message)}</span>
    </div>
  `;
}

function renderSyncStatusBadge({ pendingLoad, pendingAction }) {
  const descriptor = resolveSyncStatusBadge({ pendingLoad, pendingAction });
  const title = descriptor.title ? ` title="${escapeAttr(descriptor.title)}"` : "";
  return `<span id="porthole-sync-status" class="toolbar-status ${descriptor.className}" aria-hidden="true"${title}>${escapeHTML(descriptor.label)}</span>`;
}

function resolveSyncStatusBadge({ pendingLoad, pendingAction }) {
  if (pendingLoad) {
    return { className: "toolbar-status-loading", label: "Laster forhåndsvisning", title: "" };
  }
  if (pendingAction) {
    return { className: "toolbar-status-syncing", label: "Jobber…", title: "" };
  }
  if (portholeWebState.loading || portholeWebState.refreshInFlight) {
    return { className: "toolbar-status-syncing", label: "Oppdaterer…", title: "" };
  }
  if (portholeWebState.wsConnected) {
    const pongSummary = portholeWebState.wsLastPongAt
      ? ` Siste heartbeat: ${portholeWebState.wsLastPongAt}.`
      : "";
    return {
      className: "toolbar-status-live",
      label: "Live",
      title: `Live websocket er tilkoblet.${pongSummary}`,
    };
  }
  const reconnecting = Boolean(portholeWebState.wsReconnectTimer) ||
    Boolean(portholeWebState.ws && portholeWebState.ws.readyState === WebSocket.CONNECTING);
  const closeSummary = summarizeWebSocketClose(portholeWebState.wsLastClose);
  const errorSummary = portholeWebState.wsLastError ? ` ${portholeWebState.wsLastError}` : "";
  const title = reconnecting
    ? `Live websocket kobler til på nytt.${closeSummary ? ` ${closeSummary}` : ""}${errorSummary}`
    : `Live websocket er ikke tilkoblet. Porthole bruker HTTP fallback.${closeSummary ? ` ${closeSummary}` : ""}${errorSummary}`;
  const label = reconnecting ? "Live-feed kobler til…" : "HTTP fallback";
  return { className: "toolbar-status-polling", label, title };
}

function updateSyncStatusBadge() {
  const badge = document.getElementById("porthole-sync-status");
  if (!(badge instanceof HTMLElement)) {
    return;
  }
  const descriptor = resolveSyncStatusBadge({
    pendingLoad: portholeWebState.pendingLoad,
    pendingAction: portholeWebState.pendingAction,
  });
  badge.className = `toolbar-status ${descriptor.className}`;
  badge.textContent = descriptor.label;
  if (descriptor.title) {
    badge.setAttribute("title", descriptor.title);
  } else {
    badge.removeAttribute("title");
  }
}

function resolveActiveRequesterSummary() {
  const requester = portholeWebState.bootstrap && portholeWebState.bootstrap.requester
    ? portholeWebState.bootstrap.requester
    : null;
  if (!requester || typeof requester !== "object") {
    return null;
  }
  const displayName = typeof requester.displayName === "string" && requester.displayName.trim()
    ? requester.displayName.trim()
    : "Ukjent requester";
  const personaId = typeof requester.conferencePersonaId === "string" && requester.conferencePersonaId.trim()
    ? requester.conferencePersonaId.trim()
    : "";
  const personaDisplayName = typeof requester.conferencePersonaDisplayName === "string" && requester.conferencePersonaDisplayName.trim()
    ? requester.conferencePersonaDisplayName.trim()
    : "";
  const personaRole = typeof requester.conferencePersonaRole === "string" && requester.conferencePersonaRole.trim()
    ? requester.conferencePersonaRole.trim()
    : "";
  const personaWarning = typeof requester.conferencePersonaWarning === "string" && requester.conferencePersonaWarning.trim()
    ? requester.conferencePersonaWarning.trim()
    : "";
  const uuid = typeof requester.uuid === "string" && requester.uuid.trim()
    ? requester.uuid.trim()
    : "";
  return { displayName, personaId, personaDisplayName, personaRole, personaWarning, uuid };
}

function renderRequesterSummaryBadge() {
  const requester = resolveActiveRequesterSummary();
  if (!requester) {
    return "";
  }
  const personaLabel = requester.personaDisplayName || requester.personaId || "Live requester";
  const personaRole = requester.personaRole || (requester.personaId ? "conference demo persona" : "authenticated requester");
  return `
    <div class="toolbar-requester">
      <div class="toolbar-requester-copy">
        <span class="toolbar-requester-name">${escapeHTML(requester.displayName)}</span>
        <span class="toolbar-requester-persona">${escapeHTML(personaLabel)}</span>
        <span class="toolbar-requester-role">${escapeHTML(personaRole)}</span>
      </div>
      <div class="toolbar-persona-switcher" role="group" aria-label="Conference demo requester">
        ${conferencePersonaOptions.map((option) => renderConferencePersonaButton(option, requester.personaId)).join("")}
      </div>
      ${requester.personaWarning ? `<p class="toolbar-requester-warning">${escapeHTML(requester.personaWarning)}</p>` : ""}
    </div>
  `;
}

function renderConferencePersonaButton(option, activePersonaId) {
  const optionId = typeof option.id === "string" ? option.id : "";
  const active = optionId === String(activePersonaId || "");
  const label = typeof option.label === "string" && option.label.trim().length > 0
    ? option.label.trim()
    : "Requester";
  return `
    <button
      type="button"
      class="toolbar-persona-button ${active ? "active" : ""}"
      data-action="switch-conference-persona"
      data-conference-persona-id="${escapeAttr(optionId)}"
    >
      ${escapeHTML(label)}
    </button>
  `;
}

function switchConferencePersona(personaId) {
  const url = new URL("/browserhead/webo", window.location.origin);
  if (typeof personaId === "string") {
    url.searchParams.set("conferencePersona", personaId);
  }
  const currentSearch = new URLSearchParams(window.location.search);
  if (truthyQueryParam(currentSearch.get("showProductChrome")) || portholeWebState.productChromeRevealed) {
    url.searchParams.set("showProductChrome", "1");
  }
  window.location.assign(url.toString());
}

function resolveRequesterPersonaWarning(bootstrap) {
  const requester = bootstrap && bootstrap.requester && typeof bootstrap.requester === "object"
    ? bootstrap.requester
    : null;
  if (!requester) {
    return "";
  }
  return typeof requester.conferencePersonaWarning === "string" && requester.conferencePersonaWarning.trim()
    ? requester.conferencePersonaWarning.trim()
    : "";
}

function resolveNotificationCenterState() {
  const bootstrap = portholeWebState.bootstrap;
  const bootstrapNotifications = bootstrap && bootstrap.notifications
    ? normalizeNotificationCenter(bootstrap.notifications)
    : normalizeNotificationCenter(null);
  const liveNotifications = Array.isArray(portholeWebState.liveNotifications)
    ? portholeWebState.liveNotifications.map((entry) => normalizeNotificationItem(entry)).filter(Boolean)
    : [];
  const deduped = [];
  const seen = new Set();

  liveNotifications.concat(bootstrapNotifications.items).forEach((item) => {
    if (!item || !item.id || seen.has(item.id)) {
      return;
    }
    seen.add(item.id);
    deduped.push(item);
  });

  const latest = deduped[0] || bootstrapNotifications.latest || null;
  return {
    ...bootstrapNotifications,
    latest,
    items: deduped.slice(0, 8),
  };
}

function appendLiveNotification(item) {
  const normalized = normalizeNotificationItem(item);
  if (!normalized) {
    return;
  }
  const existing = Array.isArray(portholeWebState.liveNotifications) ? portholeWebState.liveNotifications : [];
  portholeWebState.liveNotifications = [
    normalized,
    ...existing.filter((entry) => normalizeNotificationItem(entry)?.id !== normalized.id),
  ].slice(0, 8);
}

function extractNotificationItemFromFlowElement(flowElement) {
  if (!flowElement || typeof flowElement !== "object") {
    return null;
  }
  const topic = typeof flowElement.topic === "string" ? flowElement.topic.trim().toLowerCase() : "";
  const title = typeof flowElement.title === "string" ? flowElement.title.trim() : "";
  const content = unwrapValueType(flowElement.content);
  const contentObject = content && typeof content === "object" && !Array.isArray(content) ? content : null;
  const looksLikeNotification = topic === "conference-notifications" || title.toLowerCase().startsWith("notification.");
  if (!looksLikeNotification) {
    return null;
  }

  const id = contentObject && typeof contentObject.id === "string" && contentObject.id.trim()
    ? contentObject.id.trim()
    : `${topic}:${title}:${Date.now()}`;
  const status = contentObject && typeof contentObject.status === "string" ? contentObject.status : "";
  const createdAt = contentObject && Number.isFinite(contentObject.createdAt) ? Number(contentObject.createdAt) : Date.now() / 1000;
  const triggerEvent = contentObject && typeof contentObject.triggerEvent === "string" ? contentObject.triggerEvent : title;
  const payload = contentObject && contentObject.payload && typeof contentObject.payload === "object" && !Array.isArray(contentObject.payload)
    ? contentObject.payload
    : {};
  const notificationTitle = typeof payload.title === "string" && payload.title.trim()
    ? payload.title.trim()
    : (triggerEvent || "Notification");
  const notificationDetail = typeof payload.message === "string" && payload.message.trim()
    ? payload.message.trim()
    : (typeof payload.body === "string" && payload.body.trim()
      ? payload.body.trim()
      : (contentObject && typeof contentObject.requiredActionKey === "string" ? contentObject.requiredActionKey : "Conference notification"));
  return {
    id,
    title: notificationTitle,
    subtitle: status || "new",
    detail: notificationDetail,
    status,
    createdAt,
  };
}

function formatNotificationTime(timestamp) {
  if (!Number.isFinite(timestamp)) {
    return "";
  }
  try {
    return new Intl.DateTimeFormat(undefined, {
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(timestamp * 1000));
  } catch (_ignore) {
    return "";
  }
}

function renderNotificationOverlay() {
  const center = resolveNotificationCenterState();
  if (!center.latest && center.items.length === 0 && center.totalTickets === 0) {
    return "";
  }

  const latest = center.latest || center.items[0];
  const count = Math.max(center.totalTickets, center.items.length);
  const subtitle = latest && latest.subtitle ? latest.subtitle : (center.connected ? "live" : "cached");
  return `
    <aside class="notification-overlay ${portholeWebState.notificationsExpanded ? "expanded" : ""}" aria-live="polite">
      <button
        type="button"
        class="notification-pill"
        data-action="toggle-notifications"
        aria-expanded="${portholeWebState.notificationsExpanded ? "true" : "false"}"
      >
        <span class="notification-pill-label">Notifikasjoner</span>
        ${count > 0 ? `<span class="notification-pill-count">${escapeHTML(String(count))}</span>` : ""}
        ${latest ? `
          <span class="notification-pill-copy">
            <strong>${escapeHTML(latest.title)}</strong>
            <span>${escapeHTML(subtitle)}</span>
          </span>
        ` : ""}
      </button>
      ${portholeWebState.notificationsExpanded ? `
        <div class="notification-panel">
          <div class="notification-panel-header">
            <strong>Nyeste meldinger</strong>
            <span>${escapeHTML(center.connected ? "Live feed" : "Ingen aktiv feed")}</span>
          </div>
          <div class="notification-list">
            ${center.items.map((item) => `
              <article class="notification-item">
                <div class="notification-item-copy">
                  <strong>${escapeHTML(item.title)}</strong>
                  ${item.subtitle ? `<span>${escapeHTML(item.subtitle)}</span>` : ""}
                  <p>${escapeHTML(item.detail)}</p>
                </div>
                ${item.createdAt ? `<time>${escapeHTML(formatNotificationTime(item.createdAt))}</time>` : ""}
              </article>
            `).join("")}
          </div>
        </div>
      ` : ""}
    </aside>
  `;
}

function renderPendingLoadBanner(pendingLoad) {
  if (!pendingLoad) {
    return "";
  }
  return `
    <p class="notice busy-notice">
      Laster <strong>${escapeHTML(productFacingConfigurationName(pendingLoad.name))}</strong>. Menyer og Library er midlertidig låst til preview-state er oppdatert.
    </p>
  `;
}

function renderPendingActionBanner(pendingAction) {
  if (!pendingAction) {
    return "";
  }
  return `
    <p class="notice busy-notice">
      ${escapeHTML(pendingAction.label)}
    </p>
  `;
}

function renderCanvasLoadOverlay(pendingLoad) {
  if (!pendingLoad) {
    return "";
  }
  return `
    <div class="canvas-load-overlay" aria-live="polite">
      <div class="canvas-load-card">
        <strong>Laster ${escapeHTML(productFacingConfigurationName(pendingLoad.name))}</strong>
        <p>Web-Porthole venter på at konfigurasjon, referanser og preview-state skal bli lesbare.</p>
        ${renderLoadingPlaceholderLayout()}
      </div>
    </div>
  `;
}

function renderLoadingPlaceholderLayout() {
  return `
    <div class="loading-placeholder-stack" aria-hidden="true">
      <div class="loading-placeholder-row">
        <span class="loading-placeholder-bar large"></span>
        <span class="loading-placeholder-chip"></span>
      </div>
      <div class="loading-placeholder-card-grid">
        <div class="loading-placeholder-card">
          <span class="loading-placeholder-bar medium"></span>
          <span class="loading-placeholder-bar short"></span>
          <span class="loading-placeholder-bar medium"></span>
        </div>
        <div class="loading-placeholder-card">
          <span class="loading-placeholder-bar medium"></span>
          <span class="loading-placeholder-bar short"></span>
          <span class="loading-placeholder-bar medium"></span>
        </div>
        <div class="loading-placeholder-card">
          <span class="loading-placeholder-bar medium"></span>
          <span class="loading-placeholder-bar short"></span>
          <span class="loading-placeholder-bar medium"></span>
        </div>
      </div>
      <div class="loading-placeholder-list">
        <span class="loading-placeholder-bar medium"></span>
        <span class="loading-placeholder-bar medium"></span>
        <span class="loading-placeholder-bar medium"></span>
      </div>
    </div>
  `;
}

function renderMenuSettingsControl() {
  return `
    <div class="toolbar-menu-settings">
      <button
        data-action="toggle-menu-settings"
        class="${portholeWebState.menuSettingsOpen ? "active" : ""}"
        aria-expanded="${portholeWebState.menuSettingsOpen ? "true" : "false"}"
      >
        Menyvalg
      </button>
      ${portholeWebState.menuSettingsOpen ? `
        <div class="menu-settings-popover">${renderMenuSettingsFields()}</div>
      ` : ""}
    </div>
  `;
}

function renderMenuSettingsFields() {
  const preferences = normalizeMenuPreferences(portholeWebState.menuPreferences);
  return `
    <label class="menu-settings-field">
      <span>Øvre menyer</span>
      <select data-menu-setting="topExpansionStyle">
        ${renderMenuExpansionStyleOptions(preferences.topExpansionStyle)}
      </select>
    </label>
    <label class="menu-settings-field">
      <span>Nedre menyer</span>
      <select data-menu-setting="bottomExpansionStyle">
        ${renderMenuExpansionStyleOptions(preferences.bottomExpansionStyle)}
      </select>
    </label>
    <label class="menu-settings-toggle">
      <input type="checkbox" data-menu-setting-toggle="showTitles" ${preferences.showTitles ? "checked" : ""} />
      <span>Vis navn i åpne menyer</span>
    </label>
    <label class="menu-settings-field">
      <span>Menykriterier</span>
      <textarea data-menu-setting-text="criteriaText" rows="3" placeholder="for eksempel konferanse, chat eller dokumenter">${escapeHTML(preferences.criteriaText)}</textarea>
    </label>
    <p class="menu-settings-note">Kriteriene rangerer bare flater du allerede har tilgang til.</p>
  `;
}

function renderMenuExpansionStyleOptions(selectedValue) {
  const labels = {
    auto: "Automatisk",
    stack: "Stabel",
    radial: "Radiell",
  };
  return menuExpansionStyleOptions.map((value) => `
    <option value="${escapeAttr(value)}" ${selectedValue === value ? "selected" : ""}>${escapeHTML(labels[value] || value)}</option>
  `).join("");
}

function renderCompactConvenienceTray() {
  const configurations = getCompactConvenienceConfigurations();
  if (configurations.length === 0) {
    return "";
  }

  return `
    <section class="compact-convenience-tray">
      <div class="compact-convenience-header">
        <div>
          <strong>Snarveier</strong>
          <p>Raske porthole-flater fra menyene.</p>
        </div>
        <span class="compact-convenience-count">${configurations.length}</span>
      </div>
      <div class="compact-convenience-scroll">
        <div class="compact-convenience-row">
          ${configurations.map((configuration, index) => renderCompactConvenienceCard(configuration, index)).join("")}
        </div>
      </div>
    </section>
  `;
}

function renderCompactConvenienceCard(configuration, index) {
  const title = typeof configuration.name === "string" && configuration.name.trim().length > 0
    ? productFacingConfigurationName(configuration.name)
    : "Unnamed";
  const description = menuConfigurationDescription(configuration);
  const disabled = Boolean(portholeWebState.pendingLoad);
  return `
    <button class="compact-convenience-card ${disabled ? "busy" : ""}" data-action="compact-load" data-compact-index="${index}" ${disabled ? "disabled" : ""}>
      <span class="compact-convenience-icon">${escapeHTML(shortLabel(title))}</span>
      <strong>${escapeHTML(title)}</strong>
      ${description ? `<span class="compact-convenience-description">${escapeHTML(description)}</span>` : ""}
    </button>
  `;
}

function renderEdgeMenusOverlay() {
  const topOffset = floatingToolbarBottomOffset();
  return `
    <div class="edge-menus-overlay" style="--overlay-top:${topOffset}px;">
      ${menuKeys.map((key) => renderEdgeMenu(key)).join("")}
    </div>
  `;
}

function renderFloatingPanels({
  editPanelsClass,
  componentItems,
  armedComponent,
  treeNodes,
  selectionPath,
  references,
  selectedNode,
  selectedReference,
  agentPanelContext,
}) {
  if (!isEditModeActive()) {
    return `<section class="${editPanelsClass}"></section>`;
  }

  ensureFloatingPanelLayouts();
  ensureFloatingPanelPresentationState();
  return `
    <section class="${editPanelsClass}">
      ${renderFloatingPanelWindow("components", renderComponentPanel(componentItems, armedComponent))}
      ${renderFloatingPanelWindow("elements", renderElementsPanel(treeNodes, selectionPath, references))}
      ${renderFloatingPanelWindow("inspector", renderInspectorPanel(selectedNode, selectionPath, selectedReference))}
      ${agentPanelContext ? renderFloatingPanelWindow("agentSetup", renderAgentSetupPanel(agentPanelContext)) : ""}
    </section>
  `;
}

function renderFloatingPanelWindow(panelKey, bodyMarkup) {
  if (portholeWebState.panelVisibility[panelKey] === false) {
    return "";
  }
  const definition = floatingPanelDefinitions[panelKey];
  const layout = clampPanelLayout(
    portholeWebState.panelLayouts[panelKey] || buildDefaultFloatingPanelLayout(panelKey, { x: 16, y: floatingToolbarBottomOffset() }),
    panelKey
  );
  portholeWebState.panelLayouts[panelKey] = layout;
  const isCollapsed = portholeWebState.panelCollapsed[panelKey] === true;
  const style = resolveFloatingPanelStyle(layout, isCollapsed);
  const draggingClass = portholeWebState.activePanelDrag && portholeWebState.activePanelDrag.panelKey === panelKey ? "dragging" : "";
  const resizingClass = portholeWebState.activePanelResize && portholeWebState.activePanelResize.panelKey === panelKey ? "resizing" : "";

  return `
    <aside class="panel floating-panel-window ${draggingClass} ${resizingClass} ${isCollapsed ? "collapsed" : ""}" data-panel-key="${escapeAttr(panelKey)}" style="${style}">
      <header class="floating-panel-header" data-panel-drag-handle="true" data-panel-key="${escapeAttr(panelKey)}">
        <h2>${escapeHTML(definition.title)}</h2>
        <div class="floating-panel-header-actions">
          <span class="floating-panel-hint">Dra</span>
          <button data-action="toggle-panel-collapse" data-panel-key="${escapeAttr(panelKey)}">${isCollapsed ? "Utvid" : "Kollaps"}</button>
          <button data-action="toggle-panel-visibility" data-panel-key="${escapeAttr(panelKey)}">Skjul</button>
        </div>
      </header>
      <div class="floating-panel-body">
        ${bodyMarkup}
      </div>
      ${isCollapsed ? "" : `<div class="floating-panel-resize-handle" data-panel-resize-handle="true" data-panel-key="${escapeAttr(panelKey)}" aria-label="Resize ${escapeAttr(definition.title)}"></div>`}
    </aside>
  `;
}

function resolveFloatingPanelStyle(layout, isCollapsed = false) {
  return [
    `left:${Math.round(layout.x)}px`,
    `top:${Math.round(layout.y)}px`,
    `width:${Math.round(layout.width)}px`,
    `height:${Math.round(isCollapsed ? 56 : layout.height)}px`,
  ].join(";");
}

function renderPanelVisibilityControls(agentPanelContext) {
  ensureFloatingPanelPresentationState();
  return availableFloatingPanelKeys(agentPanelContext).map((panelKey) => `
    <button
      data-action="toggle-panel-visibility"
      data-panel-key="${escapeAttr(panelKey)}"
      class="${portholeWebState.panelVisibility[panelKey] === false ? "" : "active"}"
    >
      ${escapeHTML(floatingPanelDefinitions[panelKey].title)}
    </button>
  `).join("");
}

function beginFloatingPanelDrag(event, panelKey, panelElement) {
  event.preventDefault();
  const layout = portholeWebState.panelLayouts[panelKey] || clampPanelLayout(buildDefaultFloatingPanelLayout(panelKey, { x: 16, y: floatingToolbarBottomOffset() }), panelKey);
  portholeWebState.activePanelDrag = {
    panelKey,
    pointerId: event.pointerId,
    startX: event.clientX,
    startY: event.clientY,
    originX: layout.x,
    originY: layout.y,
  };
  panelElement.classList.add("dragging");
  document.body.classList.add("panel-dragging");
  window.addEventListener("pointermove", handleFloatingPanelDragMove);
  window.addEventListener("pointerup", handleFloatingPanelDragEnd);
  window.addEventListener("pointercancel", handleFloatingPanelDragEnd);
}

function handleFloatingPanelDragMove(event) {
  const drag = portholeWebState.activePanelDrag;
  if (!drag) {
    return;
  }
  const nextLayout = clampPanelLayout({
    x: drag.originX + (event.clientX - drag.startX),
    y: drag.originY + (event.clientY - drag.startY),
  }, drag.panelKey);
  portholeWebState.panelLayouts[drag.panelKey] = nextLayout;
  const panel = document.querySelector(`.floating-panel-window[data-panel-key="${cssEscape(drag.panelKey)}"]`);
  if (panel instanceof HTMLElement) {
    panel.style.left = `${nextLayout.x}px`;
    panel.style.top = `${nextLayout.y}px`;
    panel.style.width = `${nextLayout.width}px`;
    panel.style.height = `${nextLayout.height}px`;
  }
}

function handleFloatingPanelDragEnd() {
  const drag = portholeWebState.activePanelDrag;
  if (!drag) {
    return;
  }
  const panel = document.querySelector(`.floating-panel-window[data-panel-key="${cssEscape(drag.panelKey)}"]`);
  if (panel instanceof HTMLElement) {
    panel.classList.remove("dragging");
  }
  portholeWebState.activePanelDrag = null;
  document.body.classList.remove("panel-dragging");
  window.removeEventListener("pointermove", handleFloatingPanelDragMove);
  window.removeEventListener("pointerup", handleFloatingPanelDragEnd);
  window.removeEventListener("pointercancel", handleFloatingPanelDragEnd);
  persistFloatingPanelState();
}

function beginFloatingPanelResize(event, panelKey, panelElement) {
  event.preventDefault();
  const layout = portholeWebState.panelLayouts[panelKey] || clampPanelLayout(buildDefaultFloatingPanelLayout(panelKey, { x: 16, y: floatingToolbarBottomOffset() }), panelKey);
  portholeWebState.activePanelResize = {
    panelKey,
    pointerId: event.pointerId,
    startX: event.clientX,
    startY: event.clientY,
    originWidth: layout.width,
    originHeight: layout.height,
    originX: layout.x,
    originY: layout.y,
  };
  panelElement.classList.add("resizing");
  document.body.classList.add("panel-resizing");
  window.addEventListener("pointermove", handleFloatingPanelResizeMove);
  window.addEventListener("pointerup", handleFloatingPanelResizeEnd);
  window.addEventListener("pointercancel", handleFloatingPanelResizeEnd);
}

function handleFloatingPanelResizeMove(event) {
  const resize = portholeWebState.activePanelResize;
  if (!resize) {
    return;
  }
  const nextLayout = clampPanelLayout({
    x: resize.originX,
    y: resize.originY,
    width: resize.originWidth + (event.clientX - resize.startX),
    height: resize.originHeight + (event.clientY - resize.startY),
  }, resize.panelKey);
  portholeWebState.panelLayouts[resize.panelKey] = nextLayout;
  const panel = document.querySelector(`.floating-panel-window[data-panel-key="${cssEscape(resize.panelKey)}"]`);
  if (panel instanceof HTMLElement) {
    panel.style.left = `${nextLayout.x}px`;
    panel.style.top = `${nextLayout.y}px`;
    panel.style.width = `${nextLayout.width}px`;
    panel.style.height = `${nextLayout.height}px`;
  }
}

function handleFloatingPanelResizeEnd() {
  const resize = portholeWebState.activePanelResize;
  if (!resize) {
    return;
  }
  const panel = document.querySelector(`.floating-panel-window[data-panel-key="${cssEscape(resize.panelKey)}"]`);
  if (panel instanceof HTMLElement) {
    panel.classList.remove("resizing");
  }
  portholeWebState.activePanelResize = null;
  document.body.classList.remove("panel-resizing");
  window.removeEventListener("pointermove", handleFloatingPanelResizeMove);
  window.removeEventListener("pointerup", handleFloatingPanelResizeEnd);
  window.removeEventListener("pointercancel", handleFloatingPanelResizeEnd);
  persistFloatingPanelState();
}

function renderArmedComponentBanner(component, mode) {
  if (mode !== "edit" || !component) {
    return "";
  }
  const title = typeof component.title === "string" ? component.title : "Komponent";
  const subtitle = typeof component.subtitle === "string" ? component.subtitle : "";
  return `
    <section class="component-armed-banner">
      <div>
        <strong>Klar til plassering:</strong> ${escapeHTML(title)}
        ${subtitle ? `<p>${escapeHTML(subtitle)}</p>` : ""}
      </div>
      <button data-action="cancel-armed-component">Avbryt</button>
    </section>
  `;
}

function renderComponentPanel(componentItems, armedComponent) {
  if (!Array.isArray(componentItems) || componentItems.length === 0) {
    return `
      <p class="panel-empty">Ingen komponenter tilgjengelige.</p>
      <button data-action="open-library">Åpne Library</button>
    `;
  }

  return `
    <p class="panel-note">Velg en komponent her og klikk deretter et innsettingspunkt i lerretet.</p>
    <div class="panel-list component-panel-list">
      ${componentItems.map((item, index) => {
        const isArmed = armedComponent && armedComponent.id === item.id;
        return `
          <article class="component-panel-item ${isArmed ? "armed" : ""}">
            <div>
              <strong>${escapeHTML(item.title || "Komponent")}</strong>
              ${item.subtitle ? `<p>${escapeHTML(item.subtitle)}</p>` : ""}
            </div>
            <button data-action="arm-component" data-component-source="panel" data-component-index="${index}">
              ${isArmed ? "Valgt" : "Plasser"}
            </button>
          </article>
        `;
      }).join("")}
    </div>
    <div class="panel-actions">
      <button data-action="open-library">Åpne hele Library</button>
    </div>
  `;
}

function renderElementsPanel(treeNodes, selectionPath, references) {
  const treeMarkup = Array.isArray(treeNodes) && treeNodes.length > 0
    ? `
      <div class="panel-list tree-list">
        ${treeNodes.map((node) => `
          <button
            class="tree-node ${node.path === selectionPath ? "selected" : ""}"
            data-action="select-node"
            data-path="${escapeAttr(node.path)}"
            style="--node-depth:${node.depth};"
          >
            <span class="tree-node-title">${escapeHTML(node.title)}</span>
            <small class="tree-node-path">${escapeHTML(node.path)}</small>
          </button>
        `).join("")}
      </div>
    `
    : "<p class='panel-empty'>Ingen skeleton-elementer i working copy.</p>";

  const referenceMarkup = Array.isArray(references) && references.length > 0
    ? `
      <div class="panel-section">
        <h3>References</h3>
        <div class="panel-list reference-list">
          ${references.map((entry) => `
            <button
              class="row ${entry.label === portholeWebState.selectedLabel ? "selected" : ""}"
              data-action="select-reference"
              data-label="${escapeAttr(entry.label)}"
            >
              <span>${escapeHTML(entry.label)}${entry.draft ? " (kladd)" : ""}</span>
              <small>${escapeHTML(entry.endpoint)}</small>
            </button>
          `).join("")}
        </div>
      </div>
    `
    : "";

  return treeMarkup + referenceMarkup;
}

function renderInspectorPanel(selectedNode, selectionPath, selectedReference) {
  const documentContext = resolveInspectorDocumentContext();
  const documentSections = [
    renderInspectorDocumentSection(documentContext),
    selectedReference ? renderInspectorReferenceSection(selectedReference) : "",
  ].filter(Boolean).join("");

  if (!selectedNode) {
    return `
      ${documentSections}
      <div class="panel-section">
        <h3>Node</h3>
        <p class="panel-empty">Velg et element i lerretet eller i Elements-panelet for å redigere felter og modifiers.</p>
      </div>
      ${renderInspectorDebugSection(documentContext)}
    `;
  }

  const parameters = editableParameterFields(selectedNode);
  const addableParameters = addableParameterFields(selectedNode, parameters);
  const modifiers = editableModifierFields(selectedNode);
  const addableModifiers = addableModifierFields(selectedNode, modifiers);
  const canDeleteNode = (selectionPath || selectedNode.path) !== "root";

  return `
    ${documentSections}

    <div class="panel-section inspector-summary">
      <h3>Valgt node</h3>
      <div class="inspector-kv-grid">
        <p><strong>Type</strong><span>${escapeHTML(selectedNode.element.type)}</span></p>
        <p><strong>Path</strong><code>${escapeHTML(selectionPath || selectedNode.path)}</code></p>
        <p><strong>Barn</strong><span>${selectedNode.childCount}</span></p>
      </div>
      <div class="inspector-actions">
        <button data-action="delete-selected-node" ${canDeleteNode ? "" : "disabled"}>Slett valgt node</button>
        <button data-action="copy-selected-node-raw" data-path="${escapeAttr(selectedNode.path)}">Kopier raw node</button>
      </div>
    </div>

    <div class="panel-section">
      <h3>Parameters</h3>
      ${renderEditableInspectorFields(parameters, selectedNode.path, "parameter", "Ingen redigerbare parametere på valgt element.")}
      ${renderAddableInspectorFields(addableParameters, selectedNode.path, "parameter")}
    </div>

    <div class="panel-section">
      <h3>Modifiers</h3>
      ${renderEditableInspectorFields(modifiers, selectedNode.path, "modifier", "Ingen aktive modifiers på valgt element.")}
      ${renderAddableInspectorFields(addableModifiers, selectedNode.path, "modifier")}
    </div>

    <div class="panel-section">
      <h3>Raw node</h3>
      <pre>${escapeHTML(JSON.stringify(selectedNode.raw, null, 2))}</pre>
    </div>

    ${renderInspectorDebugSection(documentContext)}
  `;
}

function renderInspectorDocumentSection(context) {
  const validation = context.validation;
  const accessNotice = context.accessNotice;
  const configurationName = context.workingConfiguration && typeof context.workingConfiguration.name === "string"
    ? context.workingConfiguration.name
    : "Porthole";
  const statusPills = [
    validation.errorCount > 0 ? { title: `${validation.errorCount} feil`, severity: "error" } : null,
    validation.warningCount > 0 ? { title: `${validation.warningCount} advarsler`, severity: "warning" } : null,
    validation.errorCount === 0 && validation.warningCount === 0 ? { title: "Struktur OK", severity: "info" } : null,
  ].filter(Boolean);

  return `
    <div class="panel-section inspector-summary">
      <h3>Dokument</h3>
      <div class="inspector-kv-grid">
        <p><strong>Konfigurasjon</strong><span>${escapeHTML(configurationName)}</span></p>
        <p><strong>Mode</strong><span>${escapeHTML(context.mode)}</span></p>
        <p><strong>Revision</strong><span>${context.revision}</span></p>
        <p><strong>Refs</strong><span>${validation.referenceCount}</span></p>
        <p><strong>Bindings</strong><span>${validation.bindingValueCount}</span></p>
        <p><strong>Dirty</strong><span>${context.isDirty ? "Ja" : "Nei"}</span></p>
      </div>
      <div class="inspector-pill-row">
        ${statusPills.map((entry) => `<span class="inspector-pill ${entry.severity}">${escapeHTML(entry.title)}</span>`).join("")}
      </div>
      <div class="inspector-actions">
        <button data-action="copy-working-configuration">Kopier working CellConfiguration</button>
        <button data-action="copy-committed-configuration">Kopier committed CellConfiguration</button>
      </div>
      ${accessNotice ? `
        <article class="inspector-issue ${accessNotice.blocked ? "error" : "info"}">
          <strong>${accessNotice.blocked ? "Kun lesing" : "Kildebasert redigering"}</strong>
          <p>${escapeHTML(accessNotice.message)}</p>
        </article>
      ` : ""}
      ${renderInspectorValidation(validation)}
    </div>
  `;
}

function renderInspectorValidation(validation) {
  if (!validation || !Array.isArray(validation.issues) || validation.issues.length === 0) {
    return "";
  }

  return `
    <div class="inspector-issue-list">
      ${validation.issues.map((issue) => `
        <article class="inspector-issue ${escapeAttr(issue.severity)}">
          <strong>${escapeHTML(issue.title)}</strong>
          <p>${escapeHTML(issue.detail)}</p>
        </article>
      `).join("")}
    </div>
  `;
}

function renderInspectorReferenceSection(selectedReference) {
  const referenceState = resolveReferenceState(selectedReference.label);
  return `
    <div class="panel-section">
      <h3>Aktiv reference</h3>
      <div class="inspector-kv-grid">
        <p><strong>Label</strong><span>${escapeHTML(selectedReference.label)}</span></p>
        <p><strong>Endpoint</strong><span>${escapeHTML(selectedReference.endpoint)}</span></p>
      </div>
      ${selectedReference.draft ? "<p class='panel-meta'>Kladd: aktiv når du trykker Apply.</p>" : ""}
      <div class="inspector-actions">
        ${selectedReference.draft ? "" : "<button data-action=\"remove-reference\">Fjern fra porthole</button>"}
        <button data-action="copy-selected-reference-state" data-label="${escapeAttr(selectedReference.label)}">Kopier reference-state</button>
      </div>
      <pre>${escapeHTML(JSON.stringify(referenceState, null, 2))}</pre>
    </div>
  `;
}

function renderInspectorDebugSection(context) {
  const debug = context.debugSnapshot;
  return `
    <div class="panel-section">
      <h3>Debug</h3>
      <div class="inspector-kv-grid debug-grid">
        <p><strong>Session</strong><span>${escapeHTML(debug.sessionId || "ukjent")}</span></p>
        <p><strong>Socket</strong><span>${debug.wsConnected ? "Live" : "Polling"}</span></p>
        <p><strong>Socket pong</strong><span>${escapeHTML(debug.wsLastPongAt || "venter")}</span></p>
        <p><strong>Socket error</strong><span>${escapeHTML(debug.wsLastError || "ingen")}</span></p>
        <p><strong>Requester</strong><span>${escapeHTML(debug.requesterDisplayName || "ukjent")}</span></p>
        <p><strong>Persona</strong><span>${escapeHTML(debug.conferencePersonaId || "live-requester")}</span></p>
        <p><strong>Selection</strong><span>${escapeHTML(debug.selectionPath || "none")}</span></p>
        <p><strong>Pending load</strong><span>${escapeHTML(debug.pendingLoad || "nei")}</span></p>
        <p><strong>Pending action</strong><span>${escapeHTML(debug.pendingAction || "nei")}</span></p>
        <p><strong>Selected label</strong><span>${escapeHTML(debug.selectedLabel || "none")}</span></p>
      </div>
      <div class="inspector-actions">
        <button data-action="copy-debug-snapshot">Kopier debug snapshot</button>
      </div>
      <pre>${escapeHTML(JSON.stringify(debug, null, 2))}</pre>
    </div>
  `;
}

function renderAgentSetupPanel(context) {
  if (!context) {
    return "<p class='panel-empty'>Sett inn eller velg en AI Agent-komponent for å konfigurere modell og API-tilgang.</p>";
  }

  if (context.armedOnly) {
    const title = context.armedComponent && context.armedComponent.title
      ? context.armedComponent.title
      : "AI Agent";
    return `
      <div class="panel-section">
        <div class="agent-setup-status pending">
          <strong>${escapeHTML(title)} er klar for plassering</strong>
          <p>Plasser komponenten i skeletonet først. Når referansen finnes i dokumentet kan vi styre modell, prompt og credential-setup herfra.</p>
        </div>
      </div>
    `;
  }

  const label = context.reference.label;
  const state = context.state && typeof context.state === "object" ? context.state : {};
  const setup = state.setup && typeof state.setup === "object" ? state.setup : {};
  const lastInvocation = state.lastInvocation && typeof state.lastInvocation === "object" ? state.lastInvocation : {};
  const statusClass = setup.status === "ready" ? "ready" : "pending";
  const providerField = renderAgentSetupField(label, "Provider", "providerID", {
    value: currentAgentSetupDraftValue(label, "providerID"),
    placeholder: "openai-compatible",
  });
  const modelField = renderAgentSetupField(label, "Model", "model", {
    value: currentAgentSetupDraftValue(label, "model"),
    placeholder: "gpt-4.1-mini",
  });
  const baseURLField = renderAgentSetupField(label, "Base URL", "baseURL", {
    value: currentAgentSetupDraftValue(label, "baseURL"),
    placeholder: "https://api.openai.com",
  });
  const aliasField = renderAgentSetupField(label, "Key Alias", "apiKeyAlias", {
    value: currentAgentSetupDraftValue(label, "apiKeyAlias"),
    placeholder: "default",
  });
  const tempField = renderAgentSetupField(label, "Temperature", "temperatureText", {
    value: currentAgentSetupDraftValue(label, "temperatureText"),
    placeholder: "0",
  });
  const maxTokensField = renderAgentSetupField(label, "Max Tokens", "maxTokensText", {
    value: currentAgentSetupDraftValue(label, "maxTokensText"),
    placeholder: "Optional",
  });
  const apiKeyField = renderAgentSetupField(label, "Session API Key", "apiKey", {
    value: currentAgentSetupDraftValue(label, "apiKey"),
    placeholder: "Paste key locally in browser, then load or save",
    type: "password",
  });
  const systemPrompt = currentAgentSetupDraftValue(label, "systemPrompt");
  const prompt = currentAgentSetupDraftValue(label, "prompt");
  const promptPreview = typeof lastInvocation.outputPreview === "string" ? lastInvocation.outputPreview : "";

  return `
    <div class="panel-section">
      <div class="agent-setup-status ${statusClass}">
        <strong>${escapeHTML(setup.statusLabel || "Agent setup")}</strong>
        <p>${escapeHTML(setup.nextStep || "Choose route, prompt, and credential mode before invoking.")}</p>
        <p class="panel-meta">
          Reference: ${escapeHTML(label)}
          ${context.selectedReferenceActive ? " • selected" : ""}
          ${context.availableReferenceCount > 1 ? ` • ${context.availableReferenceCount} AI refs in document` : ""}
        </p>
      </div>
    </div>

    <div class="panel-section">
      <h3>Route</h3>
      <p class="panel-note">Denne editor-draften er lokal til panelet til du trykker Apply route eller Sync and invoke.</p>
      <div class="agent-setup-grid">
        ${providerField}
        ${modelField}
        ${baseURLField}
        ${aliasField}
        ${tempField}
        ${maxTokensField}
        <label class="agent-setup-field">
          <span>Requires API Key</span>
          <select data-agent-setup-draft="true" data-agent-label="${escapeAttr(label)}" data-agent-field="requiresAPIKey">
            <option value="true" ${readAgentSetupBoolean(label, "requiresAPIKey") ? "selected" : ""}>true</option>
            <option value="false" ${readAgentSetupBoolean(label, "requiresAPIKey") ? "" : "selected"}>false</option>
          </select>
        </label>
        <label class="agent-setup-field">
          <span>Deterministic</span>
          <select data-agent-setup-draft="true" data-agent-label="${escapeAttr(label)}" data-agent-field="deterministicMode">
            <option value="true" ${readAgentSetupBoolean(label, "deterministicMode") ? "selected" : ""}>true</option>
            <option value="false" ${readAgentSetupBoolean(label, "deterministicMode") ? "" : "selected"}>false</option>
          </select>
        </label>
        <label class="agent-setup-field">
          <span>Cache Policy</span>
          <select data-agent-setup-draft="true" data-agent-label="${escapeAttr(label)}" data-agent-field="cachePolicy">
            <option value="useCache" ${currentAgentSetupDraftValue(label, "cachePolicy") === "useCache" ? "selected" : ""}>useCache</option>
            <option value="refresh" ${currentAgentSetupDraftValue(label, "cachePolicy") === "refresh" ? "selected" : ""}>refresh</option>
            <option value="bypass" ${currentAgentSetupDraftValue(label, "cachePolicy") === "bypass" ? "selected" : ""}>bypass</option>
          </select>
        </label>
      </div>
      <div class="panel-actions">
        <button data-action="agent-setup-apply-route" data-label="${escapeAttr(label)}">Apply route</button>
        <button data-action="agent-setup-invoke" data-label="${escapeAttr(label)}">Sync and invoke</button>
      </div>
    </div>

    <div class="panel-section">
      <h3>Credentials</h3>
      <p class="panel-note">API-nøkkelen lagres først lokalt i panelet. Den sendes bare til cellen når du velger load, save eller invoke.</p>
      <div class="agent-setup-grid">
        ${apiKeyField}
      </div>
      <div class="panel-actions">
        <button data-action="agent-setup-load-session-key" data-label="${escapeAttr(label)}">Load session key</button>
        <button data-action="agent-setup-save-key" data-label="${escapeAttr(label)}">Save key</button>
        <button data-action="agent-setup-clear-key" data-label="${escapeAttr(label)}">Clear key</button>
      </div>
      <p class="panel-meta">${escapeHTML(setup.credentialStatus || "")}</p>
      <p class="panel-note">${escapeHTML(setup.storageHint || "")}</p>
    </div>

    <div class="panel-section">
      <h3>Prompt</h3>
      <div class="agent-setup-stack">
        <label class="agent-setup-field full">
          <span>System Prompt</span>
          <textarea
            data-agent-setup-draft="true"
            data-agent-label="${escapeAttr(label)}"
            data-agent-field="systemPrompt"
            rows="4"
            placeholder="Optional instructions for the assistant"
          >${escapeHTML(systemPrompt)}</textarea>
        </label>
        <label class="agent-setup-field full">
          <span>Prompt</span>
          <textarea
            data-agent-setup-draft="true"
            data-agent-label="${escapeAttr(label)}"
            data-agent-field="prompt"
            rows="7"
            placeholder="What should the assistant help with right now?"
          >${escapeHTML(prompt)}</textarea>
        </label>
      </div>
      <div class="panel-actions">
        <button data-action="agent-setup-apply-prompts" data-label="${escapeAttr(label)}">Apply prompts</button>
        <button data-action="agent-setup-invoke" data-label="${escapeAttr(label)}">Sync and invoke</button>
      </div>
    </div>

    <div class="panel-section">
      <h3>Latest Result</h3>
      <p class="panel-note">
        ${escapeHTML(lastInvocation.model || setup.model || "")}
        ${typeof lastInvocation.invokeTimeMs === "number" && lastInvocation.invokeTimeMs > 0 ? ` • ${lastInvocation.invokeTimeMs} ms` : ""}
        ${lastInvocation.cacheHit === true ? " • cache hit" : ""}
      </p>
      ${promptPreview
        ? `<pre>${escapeHTML(promptPreview)}</pre>`
        : "<p class='panel-empty'>Ingen AI-respons ennå. Sync and invoke bruker siste panel-draft direkte.</p>"}
    </div>
  `;
}

function renderAgentSetupField(label, title, fieldKey, options = {}) {
  const type = options.type || "text";
  const value = options.value == null ? "" : String(options.value);
  const placeholder = options.placeholder || title;
  const fullClass = options.full ? " full" : "";
  return `
    <label class="agent-setup-field${fullClass}">
      <span>${escapeHTML(title)}</span>
      <input
        type="${escapeAttr(type)}"
        value="${escapeAttr(value)}"
        data-agent-setup-draft="true"
        data-agent-label="${escapeAttr(label)}"
        data-agent-field="${escapeAttr(fieldKey)}"
        placeholder="${escapeAttr(placeholder)}"
        autocomplete="off"
      />
    </label>
  `;
}

function resolveInspectorDocumentContext() {
  const bootstrap = portholeWebState.bootstrap;
  const editorState = bootstrap && bootstrap.editorState ? bootstrap.editorState : normalizeEditorState(null, null);
  const workingConfiguration = buildPortableConfigurationSnapshot("working");
  const committedConfiguration = buildPortableConfigurationSnapshot("committed");
  const validation = validatePortableCellConfiguration(workingConfiguration || committedConfiguration);
  const accessNotice = resolveEditorAccessNotice(editorState);

  return {
    mode: editorState.mode,
    isDirty: Boolean(editorState.isDirty),
    revision: Number.isFinite(editorState.revision) ? editorState.revision : 0,
    workingConfiguration,
    committedConfiguration,
    validation,
    accessNotice,
    debugSnapshot: buildPortholeDebugSnapshot({
      editorState,
      workingConfiguration,
      committedConfiguration,
      validation,
    }),
  };
}

function buildPortableConfigurationSnapshot(kind) {
  const bootstrap = portholeWebState.bootstrap;
  if (!bootstrap) {
    return null;
  }

  const baseConfiguration = bootstrap.configuration && typeof bootstrap.configuration === "object"
    ? deepCloneValue(bootstrap.configuration)
    : {};
  const editorState = bootstrap.editorState && typeof bootstrap.editorState === "object"
    ? bootstrap.editorState
    : normalizeEditorState(null, null);

  const isWorking = kind === "working";
  const skeleton = isWorking
    ? (editorState.workingSkeleton || editorState.committedSkeleton || baseConfiguration.skeleton || null)
    : (editorState.committedSkeleton || baseConfiguration.skeleton || null);
  const references = isWorking
    ? (Array.isArray(editorState.workingReferences) && editorState.workingReferences.length > 0 ? editorState.workingReferences : (baseConfiguration.cellReferences || []))
    : (Array.isArray(editorState.committedReferences) && editorState.committedReferences.length > 0 ? editorState.committedReferences : (baseConfiguration.cellReferences || []));

  const configuration = baseConfiguration && typeof baseConfiguration === "object"
    ? baseConfiguration
    : {};
  configuration.name = typeof configuration.name === "string" && configuration.name.trim()
    ? configuration.name
    : "Porthole";
  configuration.skeleton = skeleton ? deepCloneValue(skeleton) : null;
  configuration.cellReferences = deepCloneValue(Array.isArray(references) ? references : []);
  return configuration;
}

function validatePortableCellConfiguration(configuration) {
  const result = {
    configurationName: configuration && typeof configuration.name === "string" ? configuration.name : "Porthole",
    referenceCount: 0,
    bindingValueCount: 0,
    referencedLabels: [],
    unusedLabels: [],
    issues: [],
    errorCount: 0,
    warningCount: 0,
  };

  if (!configuration || typeof configuration !== "object") {
    result.issues.push({
      severity: "error",
      title: "Mangler konfigurasjon",
      detail: "Ingen CellConfiguration er lastet i Porthole akkurat nå.",
    });
    result.errorCount = 1;
    return result;
  }

  const references = Array.isArray(configuration.cellReferences) ? configuration.cellReferences : [];
  const labels = references
    .map((entry) => (entry && typeof entry.label === "string" ? entry.label.trim() : ""))
    .filter((value) => typeof value === "string");
  const topLevelLabels = labels.filter((value) => value.length > 0);
  const blankLabelCount = labels.length - topLevelLabels.length;
  const duplicateLabels = Object.keys(topLevelLabels.reduce((accumulator, label) => {
    const key = label.toLowerCase();
    accumulator[key] = (accumulator[key] || 0) + 1;
    return accumulator;
  }, {})).filter((key) => topLevelLabels.filter((label) => label.toLowerCase() === key).length > 1);
  const duplicateDisplay = duplicateLabels.map((key) => topLevelLabels.find((label) => label.toLowerCase() === key) || key);
  const bindingValues = referencedValuesInRawSkeleton(configuration.skeleton, topLevelLabels);
  const explicitReferenceBindings = bindingValues.filter((value) => inferredExplicitReferenceLabel(value));
  const referencedLabels = Array.from(new Set(
    bindingValues.map((value) => inferredReferenceLabel(value, topLevelLabels)).filter(Boolean)
  )).sort();
  const unresolvedBindings = bindingValues.filter((value) => {
    const label = inferredExplicitReferenceLabel(value);
    return label && topLevelLabels.includes(label) === false;
  });
  const unusedLabels = topLevelLabels.filter((label) => referencedLabels.includes(label) === false);

  result.referenceCount = references.length;
  result.bindingValueCount = bindingValues.length;
  result.referencedLabels = referencedLabels;
  result.unusedLabels = unusedLabels;

  if (!configuration.skeleton) {
    result.issues.push({
      severity: "error",
      title: "Mangler skeleton",
      detail: "Konfigurasjonen kan ikke rendres uten et skeleton-tre.",
    });
  }

  if (references.length === 0 && explicitReferenceBindings.length > 0) {
    result.issues.push({
      severity: "error",
      title: "Mangler CellReferences",
      detail: `Skeletonet peker på ${explicitReferenceBindings.length} eksplisitte Porthole-reference(r), men konfigurasjonen har ingen top-level references.`,
    });
  }

  if (blankLabelCount > 0) {
    result.issues.push({
      severity: "error",
      title: "Tom reference-label",
      detail: `${blankLabelCount} reference(r) mangler label.`,
    });
  }

  if (duplicateDisplay.length > 0) {
    result.issues.push({
      severity: "error",
      title: "Dupliserte labels",
      detail: duplicateDisplay.join(", "),
    });
  }

  if (unresolvedBindings.length > 0) {
    result.issues.push({
      severity: "error",
      title: "Bindings uten matchende reference",
      detail: unresolvedBindings.slice(0, 4).join(", "),
    });
  }

  if (unusedLabels.length > 0) {
    result.issues.push({
      severity: "warning",
      title: "Ubrukte references",
      detail: unusedLabels.join(", "),
    });
  }

  if (result.issues.length === 0) {
    result.issues.push({
      severity: "info",
      title: "Ingen åpenbare strukturelle feil",
      detail: "Skeleton, references og labels ser konsistente ut i denne lokale valideringen.",
    });
  }

  result.errorCount = result.issues.filter((entry) => entry.severity === "error").length;
  result.warningCount = result.issues.filter((entry) => entry.severity === "warning").length;
  return result;
}

function referencedValuesInRawSkeleton(rawValue, topLevelLabels = []) {
  const results = [];
  collectReferencedValues(rawValue, results, {
    insideCollectionItem: false,
    topLevelLabels: new Set(Array.isArray(topLevelLabels) ? topLevelLabels : []),
  });
  return Array.from(new Set(results));
}

function collectReferencedValues(rawValue, results, context = {}) {
  if (rawValue == null) {
    return;
  }
  if (Array.isArray(rawValue)) {
    rawValue.forEach((entry) => collectReferencedValues(entry, results, context));
    return;
  }
  if (typeof rawValue !== "object") {
    return;
  }

  Object.entries(rawValue).forEach(([key, value]) => {
    const nextContext = isCollectionItemSkeletonKey(key)
      ? { ...context, insideCollectionItem: true }
      : context;

    if (isReferenceSensitiveKey(key) && typeof value === "string" && value.trim().length > 0) {
      const normalized = value.trim();
      if (shouldCountReferencedValue(normalized, context)) {
        results.push(normalized);
      }
    }
    collectReferencedValues(value, results, nextContext);
  });
}

function isCollectionItemSkeletonKey(key) {
  return [
    "flowElementSkeleton",
    "itemSkeleton",
  ].includes(String(key || ""));
}

function shouldCountReferencedValue(value, context = {}) {
  if (!context.insideCollectionItem) {
    return true;
  }

  const label = inferredReferenceLabel(
    value,
    context.topLevelLabels instanceof Set ? Array.from(context.topLevelLabels) : []
  );
  if (!label) {
    return true;
  }

  return context.topLevelLabels instanceof Set && context.topLevelLabels.has(label);
}

function isReferenceSensitiveKey(key) {
  return [
    "keypath",
    "sourceKeypath",
    "targetKeypath",
    "topic",
    "url",
    "selectionStateKeypath",
    "selectionActionKeypath",
    "activationActionKeypath",
    "dragPayloadKeypath",
    "dropActionKeypath",
    "dropValidationStateKeypath",
    "dropDeniedReasonKeypath",
  ].includes(String(key || ""));
}

function inferredReferenceLabel(value, topLevelLabels = []) {
  const raw = String(value || "").trim();
  if (!raw) {
    return "";
  }

  const explicitLabel = inferredExplicitReferenceLabel(raw);
  if (explicitLabel) {
    return explicitLabel;
  }

  if (raw.includes("://")) {
    return "";
  }

  const candidate = raw.split(".")[0].trim();
  if (!candidate) {
    return "";
  }
  const labels = new Set((Array.isArray(topLevelLabels) ? topLevelLabels : []).map((label) => String(label || "")));
  return labels.has(candidate) ? candidate : "";
}

function inferredExplicitReferenceLabel(value) {
  const raw = String(value || "").trim();
  if (!raw.startsWith("cell:///Porthole/")) {
    return "";
  }
  const stripped = raw.slice("cell:///Porthole/".length);
  return stripped.split(".")[0].trim();
}

function buildPortholeDebugSnapshot({ editorState, workingConfiguration, committedConfiguration, validation }) {
  const bootstrap = portholeWebState.bootstrap || {};
  const requester = bootstrap.requester && typeof bootstrap.requester === "object"
    ? bootstrap.requester
    : null;
  return {
    sessionId: bootstrap.sessionId || "",
    wsConnected: Boolean(portholeWebState.wsConnected),
    wsReconnectAttempt: portholeWebState.wsReconnectAttempt,
    wsLastConnectedAt: portholeWebState.wsLastConnectedAt || "",
    wsLastPongAt: portholeWebState.wsLastPongAt || "",
    wsLastClose: portholeWebState.wsLastClose || null,
    wsLastError: portholeWebState.wsLastError || "",
    mode: editorState.mode,
    isDirty: Boolean(editorState.isDirty),
    revision: Number.isFinite(editorState.revision) ? editorState.revision : 0,
    selectionPath: editorState.selectionPath || "",
    pendingLoad: portholeWebState.pendingLoad ? portholeWebState.pendingLoad.name || portholeWebState.pendingLoad.id || "" : "",
    pendingAction: portholeWebState.pendingAction ? portholeWebState.pendingAction.label || portholeWebState.pendingAction.keypath || "" : "",
    selectedLabel: portholeWebState.selectedLabel || "",
    libraryOpen: Boolean(portholeWebState.libraryOpen),
    notice: portholeWebState.notice || "",
    error: portholeWebState.error || "",
    requesterUUID: requester && typeof requester.uuid === "string" ? requester.uuid : "",
    requesterDisplayName: requester && typeof requester.displayName === "string" ? requester.displayName : "",
    conferencePersonaId: requester && typeof requester.conferencePersonaId === "string" ? requester.conferencePersonaId : "",
    referenceLabels: Array.isArray(workingConfiguration && workingConfiguration.cellReferences)
      ? workingConfiguration.cellReferences.map((entry) => entry && entry.label ? entry.label : "").filter(Boolean)
      : [],
    workingConfigurationName: workingConfiguration && workingConfiguration.name ? workingConfiguration.name : "",
    committedConfigurationName: committedConfiguration && committedConfiguration.name ? committedConfiguration.name : "",
    validation,
  };
}

function renderEditableInspectorFields(entries, path, scope, emptyMessage) {
  if (!Array.isArray(entries) || entries.length === 0) {
    return `<p class="panel-empty">${escapeHTML(emptyMessage)}</p>`;
  }

  return `
    <div class="inspector-entry-list inspector-edit-list">
      ${entries.map((entry) => `
        <div class="inspector-entry inspector-field">
          <div class="inspector-field-header">
            <span class="inspector-entry-key">${escapeHTML(entry.title || entry.key)}</span>
            ${entry.clearable === false ? "" : `<button data-action="clear-${scope}" data-path="${escapeAttr(path)}" data-field-key="${escapeAttr(entry.key)}">Fjern</button>`}
          </div>
          <div class="inspector-field-controls">
            ${renderInspectorFieldControl(path, scope, entry)}
            <button
              data-action="set-${scope}"
              data-path="${escapeAttr(path)}"
              data-field-key="${escapeAttr(entry.key)}"
              data-value-kind="${escapeAttr(entry.valueKind)}"
            >
              Sett
            </button>
          </div>
        </div>
      `).join("")}
    </div>
  `;
}

function renderAddableInspectorFields(entries, path, scope) {
  if (!Array.isArray(entries) || entries.length === 0) {
    return "";
  }
  return `
    <div class="inspector-quick-adds">
      <p class="panel-note">Legg til vanlige ${scope === "modifier" ? "modifiers" : "felter"}:</p>
      <div class="panel-actions">
        ${entries.map((entry) => `
          <button
            data-action="add-${scope}"
            data-path="${escapeAttr(path)}"
            data-field-key="${escapeAttr(entry.key)}"
            data-value-kind="${escapeAttr(entry.valueKind)}"
            data-default-value="${escapeAttr(formatDefaultInspectorFieldValue(entry.defaultValue, entry.valueKind))}"
          >
            ${escapeHTML(entry.title || entry.key)}
          </button>
        `).join("")}
      </div>
    </div>
  `;
}

function renderInspectorFieldControl(path, scope, entry) {
  const draftKey = composeInspectorDraftKey(path, scope, entry.key);
  const currentValue = currentInspectorDraftValue(path, scope, entry);

  if (entry.valueKind === "bool") {
    return `
      <select data-inspector-draft="true" data-draft-key="${escapeAttr(draftKey)}">
        <option value="true" ${currentValue === "true" ? "selected" : ""}>true</option>
        <option value="false" ${currentValue === "false" ? "selected" : ""}>false</option>
      </select>
    `;
  }

  return `
    <input
      type="${entry.valueKind === "double" || entry.valueKind === "int" ? "text" : "text"}"
      value="${escapeAttr(currentValue)}"
      data-inspector-draft="true"
      data-draft-key="${escapeAttr(draftKey)}"
      placeholder="${escapeAttr(entry.placeholder || entry.title || entry.key)}"
    />
  `;
}

function editableParameterFields(selectedNode) {
  if (!selectedNode || !selectedNode.element) {
    return [];
  }
  const raw = encodeEditorNodeRaw(selectedNode.element);
  return Object.entries(raw)
    .filter(([key, value]) => {
      if (["id", "modifiers", "elements", "content", "header", "flowElementSkeleton", "itemSkeleton", "columns"].includes(key)) {
        return false;
      }
      return isEditableScalarValue(value);
    })
    .map(([key, value]) => ({
      key,
      title: key,
      valueKind: inferInspectorValueKind(value),
      value,
      clearable: true,
    }));
}

function addableParameterFields(selectedNode, activeFields) {
  const activeKeys = new Set((activeFields || []).map((entry) => entry.key));
  return recommendedParameterFieldsForType(selectedNode && selectedNode.element ? selectedNode.element.type : "")
    .filter((entry) => !activeKeys.has(entry.key));
}

function editableModifierFields(selectedNode) {
  if (!selectedNode || !selectedNode.element || !selectedNode.element.value || typeof selectedNode.element.value !== "object") {
    return [];
  }
  const modifiers = selectedNode.element.value.modifiers;
  if (!modifiers || typeof modifiers !== "object" || Array.isArray(modifiers)) {
    return [];
  }
  return Object.entries(modifiers)
    .filter(([, value]) => isEditableScalarValue(value))
    .map(([key, value]) => ({
      key,
      title: key,
      valueKind: inferInspectorValueKind(value),
      value,
      clearable: true,
    }));
}

function addableModifierFields(selectedNode, activeFields) {
  const activeKeys = new Set((activeFields || []).map((entry) => entry.key));
  return recommendedModifierFieldsForType(selectedNode && selectedNode.element ? selectedNode.element.type : "")
    .filter((entry) => !activeKeys.has(entry.key));
}

function recommendedParameterFieldsForType(type) {
  switch (type) {
    case "Text":
      return [
        { key: "text", title: "text", valueKind: "string", defaultValue: "New text" },
        { key: "keypath", title: "keypath", valueKind: "string", defaultValue: "state.value" },
        { key: "url", title: "url", valueKind: "string", defaultValue: "https://" },
      ];
    case "Button":
      return [
        { key: "label", title: "label", valueKind: "string", defaultValue: "Button" },
        { key: "keypath", title: "keypath", valueKind: "string", defaultValue: "action" },
      ];
    case "TextField":
    case "TextArea":
      return [
        { key: "placeholder", title: "placeholder", valueKind: "string", defaultValue: "Input" },
        { key: "sourceKeypath", title: "sourceKeypath", valueKind: "string", defaultValue: "input.value" },
        { key: "targetKeypath", title: "targetKeypath", valueKind: "string", defaultValue: "input.value" },
        { key: "text", title: "text", valueKind: "string", defaultValue: "" },
      ];
    case "AttachmentField":
    case "FileUpload":
      return [
        { key: "title", title: "title", valueKind: "string", defaultValue: "Upload file" },
        { key: "helperText", title: "helperText", valueKind: "string", defaultValue: "Selected files are sent to the cell action keypath." },
        { key: "valueKeypath", title: "valueKeypath", valueKind: "string", defaultValue: "attachments.current" },
        { key: "stateKeypath", title: "stateKeypath", valueKind: "string", defaultValue: "attachments.state" },
        { key: "actionKeypath", title: "actionKeypath", valueKind: "string", defaultValue: "attachments.upload" },
        { key: "allowsMultiple", title: "allowsMultiple", valueKind: "bool", defaultValue: false },
        { key: "supportsDrop", title: "supportsDrop", valueKind: "bool", defaultValue: true },
      ];
    case "Image":
      return [
        { key: "name", title: "name", valueKind: "string", defaultValue: "photo" },
        { key: "type", title: "type", valueKind: "string", defaultValue: "system" },
        { key: "url", title: "url", valueKind: "string", defaultValue: "https://" },
      ];
    case "List":
      return [
        { key: "keypath", title: "keypath", valueKind: "string", defaultValue: "items" },
        { key: "topic", title: "topic", valueKind: "string", defaultValue: "" },
        { key: "selectionMode", title: "selectionMode", valueKind: "string", defaultValue: "single" },
        { key: "selectionStateKeypath", title: "selectionStateKeypath", valueKind: "string", defaultValue: "selection.value" },
        { key: "selectionActionKeypath", title: "selectionActionKeypath", valueKind: "string", defaultValue: "selection.set" },
      ];
    case "Reference":
      return [
        { key: "keypath", title: "keypath", valueKind: "string", defaultValue: "cell:///Porthole" },
        { key: "topic", title: "topic", valueKind: "string", defaultValue: "default" },
      ];
    case "Toggle":
      return [
        { key: "label", title: "label", valueKind: "string", defaultValue: "Toggle" },
        { key: "keypath", title: "keypath", valueKind: "string", defaultValue: "toggle.value" },
      ];
    case "ScrollView":
      return [
        { key: "axis", title: "axis", valueKind: "string", defaultValue: "vertical" },
      ];
    case "VStack":
    case "HStack":
    case "Grid":
      return [
        { key: "spacing", title: "spacing", valueKind: "double", defaultValue: 8 },
      ];
    case "Picker":
      return [
        { key: "label", title: "label", valueKind: "string", defaultValue: "Velg" },
        { key: "keypath", title: "keypath", valueKind: "string", defaultValue: "selection.value" },
      ];
    case "Visualization":
      return [
        { key: "kind", title: "kind", valueKind: "string", defaultValue: "table" },
        { key: "keypath", title: "keypath", valueKind: "string", defaultValue: "visualization.data" },
        { key: "stateKeypath", title: "stateKeypath", valueKind: "string", defaultValue: "visualization.selection" },
        { key: "actionKeypath", title: "actionKeypath", valueKind: "string", defaultValue: "visualization.select" },
      ];
    default:
      return [];
  }
}

function recommendedModifierFieldsForType(type) {
  const fields = [
    { key: "padding", title: "padding", valueKind: "double", defaultValue: 12 },
    { key: "width", title: "width", valueKind: "double", defaultValue: 240 },
    { key: "height", title: "height", valueKind: "double", defaultValue: 120 },
    { key: "background", title: "background", valueKind: "string", defaultValue: "#FFFFFF" },
    { key: "cornerRadius", title: "cornerRadius", valueKind: "double", defaultValue: 12 },
    { key: "borderWidth", title: "borderWidth", valueKind: "double", defaultValue: 1 },
    { key: "borderColor", title: "borderColor", valueKind: "string", defaultValue: "#CBD5E1" },
    { key: "opacity", title: "opacity", valueKind: "double", defaultValue: 1 },
    { key: "hidden", title: "hidden", valueKind: "bool", defaultValue: false },
    { key: "draggableRole", title: "draggableRole", valueKind: "string", defaultValue: "person" },
    { key: "dragPayloadKeypath", title: "dragPayloadKeypath", valueKind: "string", defaultValue: "publicSafeDragPayload" },
    { key: "dragPreviewRole", title: "dragPreviewRole", valueKind: "string", defaultValue: "person-chip" },
    { key: "accessibilityDragLabel", title: "accessibilityDragLabel", valueKind: "string", defaultValue: "Dra element" },
    { key: "dropTargetRole", title: "dropTargetRole", valueKind: "string", defaultValue: "chat-invite-slot" },
    { key: "dropTargetPayloadKeypath", title: "dropTargetPayloadKeypath", valueKind: "string", defaultValue: "id" },
    { key: "dropActionKeypath", title: "dropActionKeypath", valueKind: "string", defaultValue: "chatHub.drop.receive" },
    { key: "dropValidationStateKeypath", title: "dropValidationStateKeypath", valueKind: "string", defaultValue: "chatHub.state.drop.validationState" },
    { key: "dropDeniedReasonKeypath", title: "dropDeniedReasonKeypath", valueKind: "string", defaultValue: "chatHub.state.drop.deniedReason" },
    { key: "accessibilityDropLabel", title: "accessibilityDropLabel", valueKind: "string", defaultValue: "Slipp her" },
  ];

  if (type === "Text" || type === "TextField") {
    fields.push(
      { key: "foregroundColor", title: "foregroundColor", valueKind: "string", defaultValue: "#0F172A" },
      { key: "fontSize", title: "fontSize", valueKind: "double", defaultValue: 16 },
      { key: "fontWeight", title: "fontWeight", valueKind: "string", defaultValue: "regular" },
      { key: "lineLimit", title: "lineLimit", valueKind: "int", defaultValue: 2 }
    );
  }

  return fields;
}

function isEditableScalarValue(value) {
  return typeof value === "string" || typeof value === "number" || typeof value === "boolean";
}

function inferInspectorValueKind(value) {
  if (typeof value === "boolean") {
    return "bool";
  }
  if (typeof value === "number") {
    return Number.isInteger(value) ? "int" : "double";
  }
  return "string";
}

function composeInspectorDraftKey(path, scope, fieldKey) {
  return `${path}::${scope}::${fieldKey}`;
}

function currentInspectorDraftValue(path, scope, entry) {
  const draftKey = composeInspectorDraftKey(path, scope, entry.key);
  const existingDraft = portholeWebState.inspectorDrafts[draftKey];
  if (typeof existingDraft === "string") {
    return existingDraft;
  }
  return formatDefaultInspectorFieldValue(entry.value, entry.valueKind);
}

function formatDefaultInspectorFieldValue(value, valueKind) {
  if (valueKind === "bool") {
    return value === true ? "true" : "false";
  }
  if (value == null) {
    return "";
  }
  return String(value);
}

async function addInspectorField({ path, fieldKey, valueKind, scope, defaultValue }) {
  portholeWebState.inspectorDrafts[composeInspectorDraftKey(path, scope, fieldKey)] = String(defaultValue || "");
  await applyInspectorFieldDraft({ path, fieldKey, valueKind, scope });
}

async function clearInspectorField({ path, fieldKey, scope }) {
  const updated = updateWorkingSkeletonNode(path, (rawNode) => {
    if (scope === "modifier") {
      const { key, cloned, normalizedValue } = prepareRawElementMutation(rawNode);
      if (!key) {
        return cloned;
      }
      const nextModifiers = normalizedValue.modifiers && typeof normalizedValue.modifiers === "object" && !Array.isArray(normalizedValue.modifiers)
        ? { ...normalizedValue.modifiers }
        : {};
      delete nextModifiers[fieldKey];
      if (Object.keys(nextModifiers).length > 0) {
        normalizedValue.modifiers = nextModifiers;
      } else {
        delete normalizedValue.modifiers;
      }
      cloned[key] = normalizedValue;
      return cloned;
    }

    const { key, cloned, normalizedValue } = prepareRawElementMutation(rawNode);
    if (!key) {
      return cloned;
    }
    delete normalizedValue[fieldKey];
    cloned[key] = normalizedValue;
    return cloned;
  });
  if (!updated) {
    return;
  }
  delete portholeWebState.inspectorDrafts[composeInspectorDraftKey(path, scope, fieldKey)];
  await runAction("editor.working.setSkeleton", updated);
}

async function applyInspectorFieldDraft({ path, fieldKey, valueKind, scope }) {
  const draftKey = composeInspectorDraftKey(path, scope, fieldKey);
  const rawDraft = typeof portholeWebState.inspectorDrafts[draftKey] === "string"
    ? portholeWebState.inspectorDrafts[draftKey]
    : "";
  const parsedValue = parseInspectorDraftValue(rawDraft, valueKind);
  if (parsedValue instanceof Error) {
    portholeWebState.error = parsedValue.message;
    render({ forceShell: true, preserveSkeletonDOM: true });
    return;
  }

  const updated = updateWorkingSkeletonNode(path, (rawNode) => {
    const { key, cloned, normalizedValue } = prepareRawElementMutation(rawNode);
    if (!key) {
      return cloned;
    }
    if (scope === "modifier") {
      const nextModifiers = normalizedValue.modifiers && typeof normalizedValue.modifiers === "object" && !Array.isArray(normalizedValue.modifiers)
        ? { ...normalizedValue.modifiers }
        : {};
      nextModifiers[fieldKey] = parsedValue;
      normalizedValue.modifiers = nextModifiers;
    } else {
      normalizedValue[fieldKey] = parsedValue;
    }
    cloned[key] = normalizedValue;
    return cloned;
  });

  if (!updated) {
    return;
  }
  await runAction("editor.working.setSkeleton", updated);
}

async function deleteSelectedNodeFromWorkingSkeleton() {
  const editorState = portholeWebState.bootstrap && portholeWebState.bootstrap.editorState
    ? portholeWebState.bootstrap.editorState
    : null;
  const path = editorState && typeof editorState.selectionPath === "string" ? editorState.selectionPath : "";
  if (!path || path === "root") {
    return;
  }
  const updated = deleteWorkingSkeletonNode(path);
  if (!updated) {
    return;
  }
  const parentPath = parentSkeletonPath(path) || "root";
  await runAction("editor.working.setSkeleton", updated);
  await runAction("editor.selection.set", { path: parentPath });
}

function parseInspectorDraftValue(text, valueKind) {
  const normalized = String(text ?? "").trim();
  switch (valueKind) {
    case "bool":
      if (normalized === "true") { return true; }
      if (normalized === "false") { return false; }
      return new Error("Bool-felt må være true eller false.");
    case "double": {
      const value = parseFlexibleNumber(normalized);
      return Number.isFinite(value) ? value : new Error("Forventet tallverdi.");
    }
    case "int": {
      const value = Number.parseInt(normalized, 10);
      return Number.isInteger(value) ? value : new Error("Forventet heltall.");
    }
    default:
      return normalized;
  }
}

function parseFlexibleNumber(text) {
  if (typeof text !== "string" || text.trim().length === 0) {
    return Number.NaN;
  }
  const normalized = text.replace(",", ".");
  return Number.parseFloat(normalized);
}

function updateWorkingSkeletonNode(path, mutateNode) {
  const rawSkeleton = currentEditableSkeletonRaw();
  if (!rawSkeleton || !path) {
    return null;
  }
  return rewriteRawSkeletonAtPath(rawSkeleton, parseSkeletonPath(path), mutateNode);
}

function deleteWorkingSkeletonNode(path) {
  const rawSkeleton = currentEditableSkeletonRaw();
  if (!rawSkeleton || !path || path === "root") {
    return null;
  }
  return deleteRawSkeletonAtPath(rawSkeleton, parseSkeletonPath(path));
}

function currentEditableSkeletonRaw() {
  const editorState = portholeWebState.bootstrap && portholeWebState.bootstrap.editorState
    ? portholeWebState.bootstrap.editorState
    : null;
  if (editorState && editorState.workingSkeleton && typeof editorState.workingSkeleton === "object") {
    return deepCloneValue(editorState.workingSkeleton);
  }
  if (editorState && editorState.committedSkeleton && typeof editorState.committedSkeleton === "object") {
    return deepCloneValue(editorState.committedSkeleton);
  }
  const configuration = portholeWebState.bootstrap && portholeWebState.bootstrap.configuration
    ? portholeWebState.bootstrap.configuration
    : null;
  if (configuration && configuration.skeleton && typeof configuration.skeleton === "object") {
    return deepCloneValue(configuration.skeleton);
  }
  return null;
}

function rewriteRawSkeletonAtPath(rawElement, pathIndices, mutateNode) {
  if (!Array.isArray(pathIndices) || pathIndices.length === 0) {
    return mutateNode(deepCloneValue(rawElement));
  }
  const [segment, ...rest] = pathIndices;
  const { key } = decodeRawElementRecord(rawElement);

  if (key === "Section" && isSectionSlotSegment(segment)) {
    return rewriteRawSectionSlotAtPath(rawElement, segment, rest, mutateNode);
  }

  if (key === "Tabs" && isPathIndex(segment)) {
    return rewriteRawTabsChildAtPath(rawElement, segment, rest, mutateNode);
  }

  if (!isPathIndex(segment)) {
    return null;
  }

  const index = segment;
  const { key: childKey, cloned, childList, assignChildren } = prepareRawChildrenMutation(rawElement);
  if (!childKey || !Array.isArray(childList) || index < 0 || index >= childList.length) {
    return null;
  }
  const updatedChild = rewriteRawSkeletonAtPath(childList[index], rest, mutateNode);
  if (!updatedChild) {
    return null;
  }
  childList[index] = updatedChild;
  assignChildren(cloned, key, childList);
  return cloned;
}

function deleteRawSkeletonAtPath(rawElement, pathIndices) {
  if (!Array.isArray(pathIndices) || pathIndices.length === 0) {
    return null;
  }
  const [segment, ...rest] = pathIndices;
  const { key } = decodeRawElementRecord(rawElement);

  if (key === "Section" && isSectionSlotSegment(segment)) {
    return deleteRawSectionSlotAtPath(rawElement, segment, rest);
  }

  if (key === "Tabs" && isPathIndex(segment)) {
    return deleteRawTabsChildAtPath(rawElement, segment, rest);
  }

  if (!isPathIndex(segment)) {
    return null;
  }

  const index = segment;
  const { key: childKey, cloned, childList, assignChildren } = prepareRawChildrenMutation(rawElement);
  if (!childKey || !Array.isArray(childList) || index < 0 || index >= childList.length) {
    return null;
  }
  if (rest.length === 0) {
    childList.splice(index, 1);
    assignChildren(cloned, key, childList);
    return cloned;
  }
  const updatedChild = deleteRawSkeletonAtPath(childList[index], rest);
  if (!updatedChild) {
    return null;
  }
  childList[index] = updatedChild;
  assignChildren(cloned, key, childList);
  return cloned;
}

function rewriteRawSectionSlotAtPath(rawElement, slot, rest, mutateNode) {
  const { key, cloned } = prepareRawElementMutation(rawElement);
  if (key !== "Section") {
    return null;
  }
  const section = cloned.Section && typeof cloned.Section === "object" && !Array.isArray(cloned.Section)
    ? { ...cloned.Section }
    : {};
  const child = section[slot];
  if (!child || typeof child !== "object") {
    return null;
  }
  const updatedChild = rewriteRawSkeletonAtPath(child, rest, mutateNode);
  if (!updatedChild) {
    return null;
  }
  section[slot] = updatedChild;
  cloned.Section = section;
  return cloned;
}

function deleteRawSectionSlotAtPath(rawElement, slot, rest) {
  const { key, cloned } = prepareRawElementMutation(rawElement);
  if (key !== "Section") {
    return null;
  }
  const section = cloned.Section && typeof cloned.Section === "object" && !Array.isArray(cloned.Section)
    ? { ...cloned.Section }
    : {};
  const child = section[slot];
  if (!child || typeof child !== "object") {
    return null;
  }
  if (rest.length === 0) {
    delete section[slot];
    cloned.Section = section;
    return cloned;
  }
  const updatedChild = deleteRawSkeletonAtPath(child, rest);
  if (!updatedChild) {
    return null;
  }
  section[slot] = updatedChild;
  cloned.Section = section;
  return cloned;
}

function rewriteRawTabsChildAtPath(rawElement, flattenedIndex, rest, mutateNode) {
  const tabsMutation = prepareRawTabsMutation(rawElement, flattenedIndex);
  if (!tabsMutation) {
    return null;
  }
  const updatedChild = rewriteRawSkeletonAtPath(tabsMutation.child, rest, mutateNode);
  if (!updatedChild) {
    return null;
  }
  tabsMutation.panel.content[tabsMutation.childIndex] = updatedChild;
  tabsMutation.assign();
  return tabsMutation.cloned;
}

function deleteRawTabsChildAtPath(rawElement, flattenedIndex, rest) {
  const tabsMutation = prepareRawTabsMutation(rawElement, flattenedIndex);
  if (!tabsMutation) {
    return null;
  }
  if (rest.length === 0) {
    tabsMutation.panel.content.splice(tabsMutation.childIndex, 1);
    tabsMutation.assign();
    return tabsMutation.cloned;
  }
  const updatedChild = deleteRawSkeletonAtPath(tabsMutation.child, rest);
  if (!updatedChild) {
    return null;
  }
  tabsMutation.panel.content[tabsMutation.childIndex] = updatedChild;
  tabsMutation.assign();
  return tabsMutation.cloned;
}

function prepareRawTabsMutation(rawElement, flattenedIndex) {
  if (!isPathIndex(flattenedIndex)) {
    return null;
  }
  const { key, cloned } = prepareRawElementMutation(rawElement);
  if (key !== "Tabs") {
    return null;
  }
  const tabs = cloned.Tabs && typeof cloned.Tabs === "object" && !Array.isArray(cloned.Tabs)
    ? { ...cloned.Tabs }
    : {};
  const panels = Array.isArray(tabs.panels) ? tabs.panels.map((panel) => {
    const nextPanel = panel && typeof panel === "object" && !Array.isArray(panel) ? { ...panel } : {};
    nextPanel.content = Array.isArray(nextPanel.content) ? [...nextPanel.content] : [];
    return nextPanel;
  }) : [];

  let remaining = flattenedIndex;
  for (let panelIndex = 0; panelIndex < panels.length; panelIndex += 1) {
    const panel = panels[panelIndex];
    if (remaining < panel.content.length) {
      const child = panel.content[remaining];
      if (!child || typeof child !== "object") {
        return null;
      }
      return {
        cloned,
        panel,
        child,
        childIndex: remaining,
        assign() {
          tabs.panels = panels;
          cloned.Tabs = tabs;
        },
      };
    }
    remaining -= panel.content.length;
  }
  return null;
}

function prepareRawChildrenMutation(rawElement) {
  const { key, value } = decodeRawElementRecord(rawElement);
  const cloned = deepCloneValue(rawElement);
  if (!key) {
    return { key: null, cloned, childList: null, assignChildren() {} };
  }

  if ((key === "VStack" || key === "HStack") && Array.isArray(value)) {
    return {
      key,
      cloned,
      childList: Array.isArray(cloned[key]) ? cloned[key] : [],
      assignChildren(target, targetKey, nextChildren) {
        target[targetKey] = nextChildren;
      },
    };
  }

  const rawValue = cloned[key] && typeof cloned[key] === "object" && !Array.isArray(cloned[key])
    ? cloned[key]
    : {};
  const containerKey = key === "Section"
    ? "content"
    : "elements";
  const childList = Array.isArray(rawValue[containerKey]) ? rawValue[containerKey] : [];

  return {
    key,
    cloned,
    childList,
    assignChildren(target, targetKey, nextChildren) {
      const targetValue = target[targetKey] && typeof target[targetKey] === "object" && !Array.isArray(target[targetKey])
        ? target[targetKey]
        : {};
      targetValue[containerKey] = nextChildren;
      target[targetKey] = targetValue;
    },
  };
}

function prepareRawElementMutation(rawElement) {
  const { key, value } = decodeRawElementRecord(rawElement);
  const cloned = deepCloneValue(rawElement);
  if (!key) {
    return { key: null, cloned, normalizedValue: {} };
  }
  return {
    key,
    cloned,
    normalizedValue: normalizeRawElementValueForMutation(key, value),
  };
}

function normalizeRawElementValueForMutation(key, value) {
  if ((key === "VStack" || key === "HStack") && Array.isArray(value)) {
    return { elements: deepCloneValue(value) };
  }
  if (value && typeof value === "object" && !Array.isArray(value)) {
    return deepCloneValue(value);
  }
  if (Array.isArray(value)) {
    return { elements: deepCloneValue(value) };
  }
  return {};
}

function decodeRawElementRecord(raw) {
  if (!raw || typeof raw !== "object") {
    return { key: null, value: null };
  }
  const supported = [
    "VStack", "HStack", "Text", "AttachmentField", "FileUpload", "TextField", "TextArea", "Button", "List", "Divider",
    "Object", "Section", "ScrollView", "Spacer", "Image", "Reference", "ZStack", "Grid", "Toggle", "Picker", "Tabs",
    "Visualization",
  ];
  const elementKey = Object.keys(raw).find((key) => supported.includes(key)) || null;
  return {
    key: elementKey,
    value: elementKey ? raw[elementKey] : null,
  };
}

function parseSkeletonPath(path) {
  const normalized = String(path || "").trim();
  if (!normalized || normalized === "root") {
    return [];
  }
  return normalized
    .split(".")
    .slice(1)
    .map((segment) => {
      if (/^\d+$/.test(segment)) {
        return Number.parseInt(segment, 10);
      }
      return segment;
    });
}

function isPathIndex(value) {
  return Number.isInteger(value) && value >= 0;
}

function isSectionSlotSegment(value) {
  return value === "header" || value === "footer";
}

function parentSkeletonPath(path) {
  const normalized = String(path || "").trim();
  if (!normalized || normalized === "root") {
    return null;
  }
  const segments = normalized.split(".");
  if (segments.length <= 2) {
    return "root";
  }
  return segments.slice(0, -1).join(".");
}

function deepCloneValue(value) {
  if (value == null) {
    return value;
  }
  return JSON.parse(JSON.stringify(value));
}

function resolveEditorSkeletonRoot(editorState, configuration) {
  const editingSkeleton = editorState && editorState.workingSkeleton && typeof editorState.workingSkeleton === "object"
    ? editorState.workingSkeleton
    : null;
  if (editingSkeleton) {
    return decodeSkeletonElementForEditor(editingSkeleton);
  }
  const committedSkeleton = editorState && editorState.committedSkeleton && typeof editorState.committedSkeleton === "object"
    ? editorState.committedSkeleton
    : null;
  if (committedSkeleton) {
    return decodeSkeletonElementForEditor(committedSkeleton);
  }
  if (configuration && configuration.skeleton && typeof configuration.skeleton === "object") {
    return decodeSkeletonElementForEditor(configuration.skeleton);
  }
  return null;
}

function linearizeSkeletonNodes(rootElement) {
  if (!rootElement) {
    return [];
  }
  const output = [];
  walkSkeletonNodes(rootElement, "root", 0, output);
  return output;
}

function walkSkeletonNodes(element, path, depth, output) {
  if (!element || typeof element !== "object") {
    return;
  }
  const childEntries = childElementEntriesForEditor(element);
  const children = childEntries.map((entry) => entry.child);
  output.push({
    path,
    depth,
    title: skeletonNodeTitle(element),
    element,
    childCount: children.length,
    raw: encodeEditorNodeRaw(element),
  });

  childEntries.forEach((entry) => {
    walkSkeletonNodes(entry.child, `${path}.${entry.segment}`, depth + 1, output);
  });
}

function resolveSkeletonNodeByPath(rootElement, path) {
  if (!rootElement) {
    return null;
  }
  const targetPath = typeof path === "string" && path.trim().length > 0 ? path.trim() : "root";
  const nodes = linearizeSkeletonNodes(rootElement);
  return nodes.find((node) => node.path === targetPath) || null;
}

function skeletonNodeTitle(element) {
  if (!element || typeof element !== "object") {
    return "Element";
  }
  const raw = element.value;
  const type = element.type || "Element";

  if (type === "Text" && raw && typeof raw === "object") {
    if (typeof raw.keypath === "string" && raw.keypath.trim()) {
      return `Text · ${raw.keypath}`;
    }
    if (typeof raw.text === "string" && raw.text.trim()) {
      return `Text · ${truncate(raw.text.trim(), 36)}`;
    }
  }

  if (type === "Button" && raw && typeof raw === "object" && typeof raw.label === "string" && raw.label.trim()) {
    return `Button · ${raw.label.trim()}`;
  }

  if ((type === "List" || type === "Grid" || type === "Reference" || type === "Picker") && raw && typeof raw === "object") {
    if (typeof raw.keypath === "string" && raw.keypath.trim()) {
      return `${type} · ${raw.keypath}`;
    }
    if (typeof raw.label === "string" && raw.label.trim()) {
      return `${type} · ${raw.label.trim()}`;
    }
  }

  if (type === "Visualization" && raw && typeof raw === "object") {
    if (typeof raw.kind === "string" && raw.kind.trim()) {
      const kindTitle = raw.kind.trim();
      if (typeof raw.keypath === "string" && raw.keypath.trim()) {
        return `Visualization · ${kindTitle} · ${raw.keypath.trim()}`;
      }
      return `Visualization · ${kindTitle}`;
    }
  }

  if (type === "Section" && raw && typeof raw === "object" && raw.header && typeof raw.header === "object") {
    const headerElement = decodeSkeletonElementForEditor(raw.header);
    if (headerElement && headerElement.type === "Text" && headerElement.value && typeof headerElement.value === "object") {
      if (typeof headerElement.value.text === "string" && headerElement.value.text.trim()) {
        return `Section · ${truncate(headerElement.value.text.trim(), 32)}`;
      }
    }
  }

  return type;
}

function summarizeElementParameters(element) {
  if (!element || typeof element !== "object") {
    return [];
  }
  const raw = encodeEditorNodeRaw(element);
  return Object.entries(raw)
    .filter(([key]) => !["modifiers", "elements", "content", "header", "flowElementSkeleton", "itemSkeleton"].includes(key))
    .map(([key, value]) => ({
      key,
      value: formatInspectorValue(value),
    }));
}

function summarizeElementModifiers(element) {
  if (!element || typeof element !== "object" || !element.value || typeof element.value !== "object") {
    return [];
  }
  const modifiers = element.value.modifiers;
  if (!modifiers || typeof modifiers !== "object" || Array.isArray(modifiers)) {
    return [];
  }
  return Object.entries(modifiers).map(([key, value]) => ({
    key,
    value: formatInspectorValue(value),
  }));
}

function encodeEditorNodeRaw(element) {
  if (!element || typeof element !== "object") {
    return {};
  }
  if (element.value && typeof element.value === "object" && !Array.isArray(element.value)) {
    return element.value;
  }
  if (Array.isArray(element.value)) {
    return { elements: element.value };
  }
  return { value: element.value };
}

function formatInspectorValue(value) {
  if (typeof value === "string") {
    return truncate(value, 80);
  }
  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  if (value == null) {
    return "null";
  }
  try {
    return truncate(JSON.stringify(value), 80);
  } catch (error) {
    return String(value);
  }
}

function truncate(value, maxLength) {
  const text = String(value || "");
  if (text.length <= maxLength) {
    return text;
  }
  return `${text.slice(0, Math.max(0, maxLength - 1))}…`;
}

function renderLibraryPanel() {
  if (!portholeWebState.libraryOpen) {
    return "";
  }

  const entries = getFilteredLibraryEntries();
  const featuredEntries = entries.filter((entry) => entry.feature);
  const remainingEntries = entries.filter((entry) => !entry.feature);
  const componentItems = getFilteredComponentPaletteItems();
  const query = String(portholeWebState.libraryQuery || "");
  const menuFilter = menuKeys.includes(portholeWebState.libraryMenuFilter)
    ? portholeWebState.libraryMenuFilter
    : "";
  const menuFilterLabel = menuFilter && menuVisuals[menuFilter] ? menuVisuals[menuFilter].label : "";
  const configurationLabel = entries.length === 1 ? "1 konfigurasjon" : `${entries.length} konfigurasjoner`;
  const componentLabel = componentItems.length === 1 ? "1 komponent" : `${componentItems.length} komponenter`;
  const editorState = portholeWebState.bootstrap && portholeWebState.bootstrap.editorState
    ? portholeWebState.bootstrap.editorState
    : normalizeEditorState(null, null);
  const showComponents = editorState.mode === "edit";
  const topOffset = floatingToolbarBottomOffset();
  const maxHeight = Math.max(220, window.innerHeight - topOffset - 16);

  return `
    <aside
      id="porthole-library-panel"
      class="library-panel"
      aria-label="Konfigurasjonsbibliotek"
      style="top:${topOffset}px;max-height:${maxHeight}px;"
    >
      <div class="library-panel-header">
        <div>
          <h2>Bibliotek</h2>
          <p>Last inn en hel konfigurasjon, eller plasser en komponent i gjeldende skeleton når du redigerer.</p>
        </div>
        <button data-action="close-library">Lukk</button>
      </div>
      <label class="library-search">
        <span>Søk</span>
        <input
          type="search"
          value="${escapeAttr(query)}"
          data-library-query="true"
          placeholder="Finn konfigurasjon, purpose eller endpoint"
        />
      </label>
      ${menuFilterLabel ? `
        <div class="library-filter-chip">
          <span>Viser menyfeltet <strong>${escapeHTML(menuFilterLabel)}</strong></span>
          <button data-action="clear-library-menu-filter">Vis hele biblioteket</button>
        </div>
      ` : ""}
      <p class="library-result-meta">${escapeHTML(showComponents ? `${componentLabel} og ${configurationLabel}` : configurationLabel)}</p>
      ${showComponents ? `
        <div class="library-section">
          <div class="library-section-header">
            <h3>Komponenter</h3>
            <p>Velg Plasser og klikk deretter på et slot i canvas.</p>
          </div>
          <div class="library-list">
            ${componentItems.length === 0 ? "<p class='library-empty'>Ingen komponenter matcher søket.</p>" : componentItems.map((item, index) => renderComponentPaletteRow(item, index)).join("")}
          </div>
        </div>
      ` : ""}
      ${featuredEntries.length > 0 ? `
        <div class="library-section featured">
          <div class="library-section-header">
            <h3>Konferansedemo</h3>
            <p>De to øverste flatene er den kanoniske Porthole-flyten. Resten er fordypningsflater, støtteflater og designsystem for samme conference-opplevelse.</p>
          </div>
          <div class="library-list">
            ${featuredEntries.map((entry) => renderLibraryRow(entry)).join("")}
          </div>
        </div>
      ` : ""}
      <div class="library-section">
        <div class="library-section-header">
          <h3>${featuredEntries.length > 0 ? "Øvrige konfigurasjoner" : "Konfigurasjoner"}</h3>
          <p>${featuredEntries.length > 0 ? "Resten av Library holdes tilgjengelig, men conference-klyngen over er den produksjonsnære demo-stien." : "Last inn hele flater når du vil bytte scene i porthole."}</p>
        </div>
        <div class="library-list">
        ${entries.length === 0
          ? "<p class='library-empty'>Ingen konfigurasjoner matcher søket.</p>"
          : (remainingEntries.length === 0
            ? "<p class='library-empty'>Alle treffene ligger i conference-klyngen over.</p>"
            : remainingEntries.map((entry) => renderLibraryRow(entry)).join(""))}
        </div>
      </div>
    </aside>
  `;
}

function renderConfigurationJSONPanel() {
  if (!portholeWebState.configurationJSONOpen) {
    return "";
  }

  const bootstrap = portholeWebState.bootstrap || {};
  const configuration = bootstrap.configuration && typeof bootstrap.configuration === "object"
    ? bootstrap.configuration
    : null;
  const title = configuration && typeof configuration.name === "string" && configuration.name.trim()
    ? configuration.name.trim()
    : "innlastet CellConfiguration";
  const json = configuration
    ? JSON.stringify(configuration, null, 2)
    : "{\n  \"error\": \"Ingen CellConfiguration er lastet ennå.\"\n}";
  const topOffset = floatingToolbarBottomOffset();
  const maxHeight = Math.max(260, window.innerHeight - topOffset - 16);

  return `
    <aside
      class="configuration-json-panel"
      aria-label="Loaded CellConfiguration JSON"
      style="top:${topOffset}px;max-height:${maxHeight}px;"
    >
      <div class="configuration-json-header">
        <div>
          <h2>CellConfiguration JSON</h2>
          <p>${escapeHTML(title)}</p>
        </div>
        <button data-action="close-configuration-json">Lukk</button>
      </div>
      <textarea readonly spellcheck="false" rows="18">${escapeHTML(json)}</textarea>
    </aside>
  `;
}

function renderComponentPaletteRow(component, index) {
  const targetKinds = component && component.recipe && Array.isArray(component.recipe.supportedTargetKinds)
    ? component.recipe.supportedTargetKinds.join(", ")
    : "";
  return `
    <article class="library-item component-item">
      <div class="library-item-copy">
        <h3>${escapeHTML(component.title || "Komponent")}</h3>
        ${component.subtitle ? `<p class="library-item-description">${escapeHTML(component.subtitle)}</p>` : ""}
        ${targetKinds ? `<p class="library-item-endpoint">Støtter: ${escapeHTML(targetKinds)}</p>` : ""}
      </div>
      <div class="library-item-actions">
        <span class="library-item-badge">Komponent</span>
        <button data-action="arm-component" data-component-source="palette" data-component-index="${index}">Plasser</button>
      </div>
    </article>
  `;
}

function renderLibraryRow(entry) {
  const configuration = entry && entry.configuration ? entry.configuration : null;
  const filteredIndex = entry && Number.isInteger(entry.filteredIndex) ? entry.filteredIndex : -1;
  const feature = entry && entry.feature ? entry.feature : null;
  const discovery = configuration && configuration.discovery && typeof configuration.discovery === "object"
    ? configuration.discovery
    : {};
  const description = typeof configuration.description === "string" && configuration.description.trim().length > 0
    ? configuration.description
    : (typeof discovery.purposeDescription === "string" ? discovery.purposeDescription : "");
  const purpose = typeof discovery.purpose === "string" ? discovery.purpose : "";
  const endpoint = typeof discovery.sourceCellEndpoint === "string"
    ? discovery.sourceCellEndpoint
    : (configuration.cellReferences && configuration.cellReferences[0] && configuration.cellReferences[0].endpoint) || "";
  const isActive = portholeWebState.bootstrap &&
    portholeWebState.bootstrap.configuration &&
    portholeWebState.bootstrap.configuration.uuid === configuration.uuid;
  const canInsert = portholeWebState.mode === "edit" && canInsertConfigurationAsComponent(configuration);
  const pendingIdentity = portholeWebState.pendingLoad ? portholeWebState.pendingLoad.id : "";
  const rowIdentity = menuConfigurationIdentity(configuration);
  const isPending = pendingIdentity && rowIdentity && pendingIdentity === rowIdentity;
  const isBusy = Boolean(portholeWebState.pendingLoad);
  const featureBadge = feature
    ? `<span class="library-item-badge feature-${escapeAttr(feature.tone || "support")}">${escapeHTML(feature.badge || "Conference")}</span>`
    : "";
  const displayName = productFacingConfigurationName(configuration.name) || "Untitled configuration";

  return `
    <article
      class="library-item ${feature ? "featured" : ""} ${isActive ? "active" : ""} ${isPending ? "busy" : ""}"
      data-action="library-load"
      data-action-card="library-load"
      data-library-index="${filteredIndex}"
      role="button"
      tabindex="0"
      aria-label="Last inn ${escapeAttr(displayName)}"
    >
      <div class="library-item-copy">
        <h3>${escapeHTML(displayName)}</h3>
        ${purpose ? `<p class="library-item-purpose">${escapeHTML(purpose)}</p>` : ""}
        ${description ? `<p class="library-item-description">${escapeHTML(description)}</p>` : ""}
        ${endpoint ? `<p class="library-item-endpoint">${escapeHTML(endpoint)}</p>` : ""}
      </div>
      <div class="library-item-actions">
        ${featureBadge}
        ${isActive ? "<span class='library-item-badge'>Aktiv</span>" : ""}
        ${isPending ? "<span class='library-item-badge'>Laster</span>" : ""}
        ${canInsert ? `<button data-action="arm-component" data-component-source="library" data-component-index="${filteredIndex}" ${isBusy ? "disabled" : ""}>Plasser</button>` : ""}
        <button data-action="library-load" data-library-index="${filteredIndex}" ${isBusy ? "disabled" : ""}>${isPending ? "Laster…" : "Last inn"}</button>
      </div>
    </article>
  `;
}

function renderEdgeMenu(menuKey) {
  const entries = getMenuEntries(menuKey);
  const visual = menuVisuals[menuKey] || { anchor: "upper-left", icon: "MENY", label: "Meny", centerAngle: 45 };
  const expanded = Boolean(portholeWebState.expandedMenus[menuKey]);
  const countLabel = entries.length > 0 ? String(entries.length) : "";
  const hasOverflow = entries.length > edgeMenuPresentationLimit;
  const visibleEntries = entries.slice(0, hasOverflow ? edgeMenuPresentationLimit - 1 : edgeMenuPresentationLimit);
  const presentedItemCount = visibleEntries.length + (hasOverflow ? 1 : 0);
  const fanButtons = expanded
    ? `${visibleEntries.map((entry, index) => renderEdgeMenuEntry(menuKey, entry, index, presentedItemCount, visual.centerAngle)).join("")}${hasOverflow ? renderEdgeMenuShowAll(menuKey, entries.length, presentedItemCount - 1, presentedItemCount, visual.centerAngle) : ""}`
    : "";
  const itemsId = edgeMenuItemsId(menuKey);

  return `
    <article class="edge-menu-anchor anchor-${escapeAttr(visual.anchor)} ${expanded ? "expanded" : ""}" data-menu-key="${escapeAttr(menuKey)}">
      <button
        id="${escapeAttr(edgeMenuTriggerId(menuKey))}"
        class="edge-menu-main"
        data-action="menu-toggle"
        data-menu-key="${escapeAttr(menuKey)}"
        data-focus-key="edge-trigger-${escapeAttr(menuKey)}"
        aria-label="${escapeAttr(`${visual.label}, ${entries.length} ${entries.length === 1 ? "flate" : "flater"}`)}"
        ${entries.length > 1 ? `aria-haspopup="menu" aria-expanded="${expanded ? "true" : "false"}" aria-controls="${escapeAttr(itemsId)}"` : ""}
        title="${escapeAttr(menuButtonTitle(menuKey, entries))}"
      >
        <span class="edge-menu-icon">${escapeHTML(visual.icon)}</span>
        ${countLabel ? `<span class="edge-menu-count">${escapeHTML(countLabel)}</span>` : ""}
      </button>
      <div id="${escapeAttr(itemsId)}" class="edge-menu-items" role="menu" data-edge-menu-key="${escapeAttr(menuKey)}" aria-label="${escapeAttr(visual.label)}" ${expanded ? "" : "hidden"}>
        ${fanButtons}
      </div>
    </article>
  `;
}

function renderEdgeMenuEntry(menuKey, entry, index, count, centerAngle) {
  const metrics = menuItemMetrics(menuKey, entry);
  const raw = rawMenuOffset({
    menuKey,
    index,
    count,
    centerAngle,
    sweepDegrees: sweepForMenu(menuKey),
    radius: 96,
    expansionStyle: resolvedMenuExpansionStyle(menuKey),
    hasSubtitle: metrics.showSubtitle,
  });
  const offset = clampedMenuOffset({
    menuKey,
    raw,
    itemSize: { width: metrics.width, height: metrics.height },
    alignment: metrics.alignment,
  });
  const title = typeof entry.name === "string" && entry.name.trim().length > 0 ? entry.name.trim() : "Untitled config";
  const description = metrics.showSubtitle ? menuConfigurationDescription(entry) : "";
  const textBlock = metrics.showsTitle
    ? `
      <span class="edge-menu-copy">
        <span class="edge-menu-title">${escapeHTML(title)}</span>
        ${description ? `<span class="edge-menu-subtitle">${escapeHTML(description)}</span>` : ""}
      </span>
    `
    : "";
  const glyph = `<span class="edge-menu-glyph">${escapeHTML(shortLabel(title))}</span>`;
  const innerContent = metrics.trailingGlyph
    ? `${textBlock}${glyph}`
    : `${glyph}${textBlock}`;

  return `
    <button
      class="edge-menu-item ${metrics.itemClass}"
      role="menuitem"
      tabindex="${index === 0 ? "0" : "-1"}"
      data-action="menu-add"
      data-menu-key="${escapeAttr(menuKey)}"
      data-menu-index="${Number.isInteger(entry.__menuOriginalIndex) ? entry.__menuOriginalIndex : index}"
      style="--offset-x:${offset.x.toFixed(2)}px; --offset-y:${offset.y.toFixed(2)}px; --item-width:${metrics.width}px; --item-height:${metrics.height}px;"
      title="${escapeAttr(title)}"
      aria-label="Åpne ${escapeAttr(title)}"
      ${portholeWebState.pendingLoad ? "disabled" : ""}
    >
      ${innerContent}
    </button>
  `;
}

function renderEdgeMenuShowAll(menuKey, totalCount, index, count, centerAngle) {
  const metrics = { width: 112, height: 44, alignment: menuKey.endsWith("LeftMenu") ? "leading" : (menuKey.endsWith("RightMenu") ? "trailing" : "center") };
  const raw = rawMenuOffset({
    menuKey,
    index,
    count,
    centerAngle,
    sweepDegrees: sweepForMenu(menuKey),
    radius: 96,
    expansionStyle: resolvedMenuExpansionStyle(menuKey),
    hasSubtitle: false,
  });
  const offset = clampedMenuOffset({ menuKey, raw, itemSize: metrics, alignment: metrics.alignment });
  return `
    <button
      class="edge-menu-item edge-menu-show-all"
      role="menuitem"
      tabindex="-1"
      data-action="menu-show-all"
      data-menu-key="${escapeAttr(menuKey)}"
      style="--offset-x:${offset.x.toFixed(2)}px; --offset-y:${offset.y.toFixed(2)}px; --item-width:${metrics.width}px; --item-height:${metrics.height}px;"
      aria-label="Vis alle ${totalCount} flater i ${escapeAttr(menuVisuals[menuKey] ? menuVisuals[menuKey].label : "menyfeltet")}"
    >Vis alle ${totalCount}</button>
  `;
}

function edgeMenuTriggerId(menuKey) {
  return `edge-menu-trigger-${menuKey}`;
}

function edgeMenuItemsId(menuKey) {
  return `edge-menu-items-${menuKey}`;
}

function rawMenuOffset({ menuKey, index, count, centerAngle, sweepDegrees, radius, expansionStyle, hasSubtitle }) {
  if (expansionStyle === "radial") {
    return radialOffset({ index, count, centerAngle, sweepDegrees, radius });
  }

  return {
    x: stackHorizontalOffset(menuKey, index),
    y: stackDirection(menuKey) * stackStride(menuKey, hasSubtitle) * (index + 1),
  };
}

function clampedMenuOffset({ menuKey, raw, itemSize, alignment }) {
  const metrics = currentCanvasMetrics();
  const anchor = anchorPointForMenu(menuKey, metrics);
  const pad = 10;
  const baseX = anchorBaseX(anchor.x, itemSize.width, alignment);
  const baseY = anchor.y - itemSize.height / 2;

  let absX = baseX + raw.x;
  let absY = baseY + raw.y;
  absX = Math.max(pad, Math.min(metrics.width - itemSize.width - pad, absX));
  absY = Math.max(pad, Math.min(metrics.height - itemSize.height - pad, absY));

  return {
    x: absX - baseX,
    y: absY - baseY,
  };
}

function anchorBaseX(anchorX, width, alignment) {
  switch (alignment) {
    case "leading":
      return anchorX;
    case "trailing":
      return anchorX - width;
    default:
      return anchorX - width / 2;
  }
}

function currentCanvasMetrics() {
  const isCompact = usesCompactConvenienceMenus();
  const margin = isCompact ? 24 : 32;
  return {
    width: Math.max(320, window.innerWidth - 20),
    height: Math.max(320, window.innerHeight - floatingToolbarBottomOffset() - 12),
    margin,
  };
}

function anchorPointForMenu(menuKey, metrics) {
  const width = metrics.width;
  const height = metrics.height;
  const margin = metrics.margin;

  switch (menuKey) {
    case "upperLeftMenu":
      return { x: margin, y: margin };
    case "upperMidMenu":
      return { x: width / 2, y: margin };
    case "upperRightMenu":
      return { x: width - margin, y: margin };
    case "lowerLeftMenu":
      return { x: margin, y: height - margin };
    case "lowerMidMenu":
      return { x: width / 2, y: height - margin };
    case "lowerRightMenu":
      return { x: width - margin, y: height - margin };
    default:
      return { x: width / 2, y: height / 2 };
  }
}

function radialOffset({ index, count, centerAngle, sweepDegrees, radius }) {
  if (!Number.isFinite(count) || count <= 0) {
    return { x: 0, y: 0 };
  }
  const step = count > 1 ? sweepDegrees / (count - 1) : 0;
  const start = centerAngle - sweepDegrees / 2;
  const angleDeg = start + step * index;
  const angle = (angleDeg * Math.PI) / 180;
  return {
    x: Math.cos(angle) * radius,
    y: Math.sin(angle) * radius,
  };
}

function sweepForMenu(_menuKey) {
  return 140;
}

function shortLabel(name) {
  const normalized = String(name || "").trim();
  if (!normalized) {
    return "Cfg";
  }
  const words = normalized.split(/\s+/).filter(Boolean);
  if (words.length >= 2) {
    const first = words[0].slice(0, 1);
    const second = words[1].slice(0, 1);
    return `${first}${second}`.toUpperCase();
  }
  return normalized.slice(0, 3);
}

function menuButtonTitle(menuKey, entries) {
  const visual = menuVisuals[menuKey] || { label: "Meny" };
  if (entries.length === 1) {
    const only = entries[0];
    const name = only && typeof only.name === "string" && only.name.trim().length > 0
      ? only.name.trim()
      : "selected configuration";
    return `Åpne ${name}`;
  }
  if (entries.length === 0 && menuKey === "upperMidMenu") {
    return "Åpne biblioteket";
  }
  return `${visual.label}: ${entries.length} ${entries.length === 1 ? "flate" : "flater"}`;
}

function menuConfigurationDescription(configuration) {
  if (!configuration || typeof configuration !== "object") {
    return "";
  }
  return typeof configuration.description === "string" ? configuration.description.trim() : "";
}

function resolvedMenuExpansionStyle(menuKey) {
  const preferences = normalizeMenuPreferences(portholeWebState.menuPreferences);
  const rawStyle = menuKey.startsWith("upper")
    ? preferences.topExpansionStyle
    : preferences.bottomExpansionStyle;
  return rawStyle === "radial" ? "radial" : "stack";
}

function menuLabelMode() {
  const preferences = normalizeMenuPreferences(portholeWebState.menuPreferences);
  return preferences.showTitles ? "titleOnOpen" : "iconOnly";
}

function menuAlignment(menuKey) {
  if (menuKey === "upperMidMenu" || menuKey === "lowerMidMenu") {
    return "center";
  }
  if (menuKey === "upperRightMenu" || menuKey === "lowerRightMenu") {
    return "trailing";
  }
  return "leading";
}

function menuShowsSubtitle(menuKey) {
  return menuKey === "upperMidMenu" || menuKey === "lowerMidMenu";
}

function menuItemMetrics(menuKey, entry) {
  const alignment = menuAlignment(menuKey);
  const labelMode = menuLabelMode();
  const description = menuConfigurationDescription(entry);
  const showSubtitle = labelMode === "titleOnOpen" && menuShowsSubtitle(menuKey) && Boolean(description);
  const centerMenu = alignment === "center";

  if (labelMode === "iconOnly") {
    return {
      width: 38,
      height: 38,
      alignment,
      showSubtitle: false,
      showsTitle: false,
      trailingGlyph: false,
      itemClass: `icon-only align-${alignment}`,
    };
  }

  return {
    width: centerMenu ? 304 : 238,
    height: showSubtitle ? 58 : 46,
    alignment,
    showSubtitle,
    showsTitle: true,
    trailingGlyph: alignment === "trailing",
    itemClass: `show-title align-${alignment}${showSubtitle ? " has-subtitle" : ""}`,
  };
}

function stackHorizontalOffset(menuKey, index) {
  switch (menuKey) {
    case "upperMidMenu":
    case "lowerMidMenu": {
      const pattern = [0, -12, 12, -7, 7, -4, 4];
      return pattern[index % pattern.length];
    }
    case "upperRightMenu":
    case "lowerRightMenu":
      return -Math.min(index * 5, 14);
    default:
      return Math.min(index * 5, 14);
  }
}

function stackStride(menuKey, hasSubtitle) {
  const labelMode = menuLabelMode();
  const centerMenu = menuKey === "upperMidMenu" || menuKey === "lowerMidMenu";
  if (labelMode === "iconOnly") {
    return centerMenu ? 50 : 54;
  }
  if (hasSubtitle) {
    return centerMenu ? 64 : 68;
  }
  return centerMenu ? 54 : 58;
}

function stackDirection(menuKey) {
  return menuKey.startsWith("lower") ? -1 : 1;
}

function renderEmptyState() {
  const bootstrap = portholeWebState.bootstrap;
  const configuration = bootstrap && bootstrap.configuration;
  const references = getReferences();
  const editorState = bootstrap && bootstrap.editorState ? bootstrap.editorState : null;
  const hasEditingSkeleton = Boolean(editorState && editorState.mode === "edit" && editorState.workingSkeleton);
  if ((configuration && configuration.skeleton) || hasEditingSkeleton || references.length > 0) {
    return "";
  }
  return `
    <div class="empty-state">
      <h2>Porthole er tom</h2>
      <p>${portholeWebState.armedComponent ? `Klikk på slotten for å starte med ${escapeHTML(portholeWebState.armedComponent.title || "komponenten")}.` : "Åpne Library eller be Co-Pilot vise Porthole-verktøyene for å laste inn innhold."}</p>
    </div>
  `;
}

function skeletonRenderSignature(value) {
  // JSON object field order is not layout. A bootstrap may encode the same
  // Skeleton in a different order; remounting would discard editor state and
  // pending asynchronous input such as a document's FileReader image load.
  return JSON.stringify(value, (_key, nested) => {
    if (nested && typeof nested === "object" && !Array.isArray(nested)) {
      return Object.fromEntries(Object.keys(nested).sort().map((key) => [key, nested[key]]));
    }
    return nested;
  });
}

function portholeLocalizationContext(bootstrap) {
  const supplied = bootstrap?.localizationContext;
  if (supplied?.ui_locale) return supplied;
  const resolved = window.HavenLocalization?.resolveLocale({ languages: navigator.languages || [], supportedLocales: bootstrap?.configuration?.localization?.supportedLocales || ["nb-NO", "en-US"] });
  return { ...(resolved || { ui_locale: "nb-NO" }), timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC" };
}

function renderSkeletonCanvas() {
  const root = document.getElementById("porthole-skeleton-root");
  if (!(root instanceof HTMLElement)) {
    return;
  }

  const bootstrap = portholeWebState.bootstrap;
  const configuration = bootstrap && bootstrap.configuration;
  const editorState = bootstrap && bootstrap.editorState ? bootstrap.editorState : null;
  const state = bootstrap && bootstrap.state ? bootstrap.state : {};
  const mode = editorState ? editorState.mode : "view";
  const editingSkeleton = editorState && editorState.workingSkeleton && typeof editorState.workingSkeleton === "object"
    ? editorState.workingSkeleton
    : null;
  const committedSkeleton = editorState && editorState.committedSkeleton && typeof editorState.committedSkeleton === "object"
    ? editorState.committedSkeleton
    : null;
  const fallbackSkeleton = committedSkeleton || (configuration && configuration.skeleton);
  const renderedSkeleton = mode === "edit" ? (editingSkeleton || fallbackSkeleton) : fallbackSkeleton;
  const references = getReferences();

  if (!renderedSkeleton) {
    if (portholeWebState.renderer && typeof portholeWebState.renderer.destroy === "function") {
      portholeWebState.renderer.destroy();
    }
    root.innerHTML = references.length > 0 ? renderReferenceWorkspace(references) : "";
    portholeWebState.renderer = null;
    portholeWebState.skeletonLayoutObserver?.disconnect();
    portholeWebState.rendererRoot = null;
    portholeWebState.skeletonSignature = null;
    renderSelectionOutline();
    renderInsertionSlots(null);
    return;
  }

  const skeletonRuntime = window.HavenSkeletonRuntime || window.SkeletonRuntime;
  if (!skeletonRuntime || typeof skeletonRuntime.createRenderer !== "function") {
    renderSkeletonValidationDiagnostic("Skeleton runtime er ikke tilgjengelig.");
    renderSelectionOutline();
    renderInsertionSlots(null);
    return;
  }

  const currentConfigurationName = configuration && typeof configuration.name === "string"
    ? configuration.name
    : null;
  const signature = skeletonRenderSignature({ currentConfigurationName, renderedSkeleton });
  const hostChanged = hasSkeletonHostChanged(root);
  if (!portholeWebState.renderer || signature !== portholeWebState.skeletonSignature || hostChanged) {
    const previousRenderer = portholeWebState.renderer;
    let candidateRenderer;
    try {
      candidateRenderer = skeletonRuntime.createRenderer({
        rootElement: root,
        skeleton: renderedSkeleton,
        layoutContext: declaredSkeletonLayoutContext(root),
        currentConfigurationName,
        localization: configuration?.localization || null,
        localizationContext: portholeLocalizationContext(bootstrap),
        deferMount: true,
        onAction: async (keypath, payload, meta) => {
          const routedAction = resolveRendererActionRoute(keypath, payload, meta);
          if (routedAction.mount) {
            return runComponentSourceAction(routedAction);
          }
          if (meta && meta.trigger === "document") {
            const result = await requestActionPayload(routedAction.keypath, routedAction.payload, 30000);
            return normalizeActionResultValue(actionResultPayload(result));
          }

          if (meta && meta.trigger === "button") {
            await flushPendingFieldActions();
          } else if (routedAction.keypath === "chatHub.prompt.submit") {
            cancelPendingFieldAction("chatHub.setComposer");
          }
          await runAction(routedAction.keypath, routedAction.payload);
        },
        onFieldInput: handleRendererFieldInput,
        resolveButtonPayload: resolveRendererActionPayload,
        formatText: formatSkeletonText,
      });
      candidateRenderer.update(state);
      if (typeof candidateRenderer.mount === "function") {
        candidateRenderer.mount(root);
      }
    } catch (error) {
      if (candidateRenderer && typeof candidateRenderer.destroy === "function") {
        candidateRenderer.destroy();
      }
      const message = error instanceof Error ? error.message : String(error);
      portholeWebState.error = message;
      renderSkeletonValidationDiagnostic(message);
      return;
    }
    if (previousRenderer && typeof previousRenderer.destroy === "function") {
      previousRenderer.destroy({ preserveDOM: true });
    }
    portholeWebState.renderer = candidateRenderer;
    portholeWebState.rendererRoot = root;
    observeSkeletonLayoutHost(root);
    portholeWebState.skeletonSignature = signature;
    portholeWebState.localizationSignature = JSON.stringify(configuration?.localization || null);
    clearSkeletonValidationDiagnostic();
  }

  try {
    const localizationSignature = JSON.stringify(configuration?.localization || null);
    const localizationChanged = localizationSignature !== portholeWebState.localizationSignature;
    portholeWebState.renderer.setLocalization?.(portholeLocalizationContext(bootstrap),
      localizationChanged ? configuration?.localization || null : undefined);
    portholeWebState.localizationSignature = localizationSignature;
    refreshSkeletonLayoutContext();
    portholeWebState.renderer.update(state);
    clearSkeletonValidationDiagnostic();
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    portholeWebState.error = message;
    renderSkeletonValidationDiagnostic(message);
    return;
  }
  reapplyPersistentFieldValues();
  enhanceRenderedQRCodes(root);
  renderSelectionOutline();
  renderInsertionSlots(renderedSkeleton);
  scheduleChatViewportLayout();
}

// V3-A: one measured host boundary; descendants only use declared layout.
function declaredSkeletonLayoutContext(root) {
  const capabilities = ["keyboard", "drag"];
  if (window.matchMedia("(pointer: fine)").matches) capabilities.push("pointer");
  if (window.matchMedia("(hover: hover)").matches) capabilities.push("hover");
  if (navigator.maxTouchPoints > 0) capabilities.push("touch");
  return { availableWidth: root.clientWidth, availableHeight: root.parentElement?.clientHeight, capabilities };
}

function refreshSkeletonLayoutContext() {
  const root = portholeWebState.rendererRoot;
  if (root) portholeWebState.renderer?.setLayoutContext?.(declaredSkeletonLayoutContext(root));
}

function observeSkeletonLayoutHost(root) {
  portholeWebState.skeletonLayoutObserver?.disconnect();
  if (typeof ResizeObserver !== "function") return;
  const observer = new ResizeObserver(refreshSkeletonLayoutContext);
  observer.observe(root);
  if (root.parentElement) observer.observe(root.parentElement);
  portholeWebState.skeletonLayoutObserver = observer;
}

let chatViewportLayoutFrame = null;
function scheduleChatViewportLayout() {
  if (chatViewportLayoutFrame !== null) return;
  chatViewportLayoutFrame = requestAnimationFrame(() => {
    chatViewportLayoutFrame = null;
    const viewport = window.visualViewport;
    const bottom = viewport ? viewport.offsetTop + viewport.height : window.innerHeight;
    for (const conversation of document.querySelectorAll(".canvas.product-view .style-role-chat-conversation")) {
      const bounds = conversation.getBoundingClientRect();
      if (!bounds.width || !bounds.height) continue;
      // Account for the actual toolbar, status banner and tabs above the chat.
      // Do not scroll the page or reset the reader's position in the log.
      const height = Math.max(0, Math.min(820, bottom - bounds.top - 12));
      conversation.style.setProperty("--chat-viewport-height", `${height}px`);
    }
  });
}
window.visualViewport?.addEventListener("resize", scheduleChatViewportLayout);

function hasSkeletonHostChanged(root) {
  return portholeWebState.rendererRoot !== root;
}

function renderedSkeletonForBootstrap(bootstrap) {
  const configuration = bootstrap && bootstrap.configuration;
  const editorState = bootstrap && bootstrap.editorState ? bootstrap.editorState : null;
  const mode = editorState ? editorState.mode : "view";
  const editingSkeleton = editorState && editorState.workingSkeleton && typeof editorState.workingSkeleton === "object"
    ? editorState.workingSkeleton
    : null;
  const committedSkeleton = editorState && editorState.committedSkeleton && typeof editorState.committedSkeleton === "object"
    ? editorState.committedSkeleton
    : null;
  const fallbackSkeleton = committedSkeleton || (configuration && configuration.skeleton);
  return mode === "edit" ? (editingSkeleton || fallbackSkeleton) : fallbackSkeleton;
}

function assertValidBootstrapSkeleton(bootstrap) {
  const runtime = window.HavenSkeletonRuntime || window.SkeletonRuntime;
  if (!runtime || typeof runtime.validateSkeleton !== "function") {
    return;
  }

  const configuration = bootstrap && bootstrap.configuration;
  const editorState = bootstrap && bootstrap.editorState ? bootstrap.editorState : null;
  const candidates = [
    ["configuration.skeleton", configuration && configuration.skeleton],
    ["editorState.committedSkeleton", editorState && editorState.committedSkeleton],
    ["editorState.workingSkeleton", editorState && editorState.workingSkeleton],
  ];
  for (const [field, skeleton] of candidates) {
    if (!skeleton) {
      continue;
    }
    const validation = runtime.validateSkeleton(skeleton);
    if (validation && validation.valid === true) {
      continue;
    }
    const error = new Error(validation && validation.error
      ? `${field}: ${validation.error}`
      : `${field}: Invalid skeleton update rejected.`);
    error.name = "SkeletonValidationError";
    error.preserveRenderedSkeleton = true;
    throw error;
  }
}

function renderSkeletonValidationDiagnostic(message) {
  const root = document.getElementById("porthole-skeleton-root");
  if (!(root instanceof HTMLElement)) {
    return;
  }
  let diagnostic = document.getElementById("porthole-skeleton-validation-error");
  if (!(diagnostic instanceof HTMLElement)) {
    diagnostic = document.createElement("p");
    diagnostic.id = "porthole-skeleton-validation-error";
    diagnostic.className = "error skeleton-validation-error";
    diagnostic.setAttribute("role", "alert");
    root.insertAdjacentElement("afterend", diagnostic);
  }
  diagnostic.textContent = String(message || "Invalid skeleton update rejected.");
}

function clearSkeletonValidationDiagnostic() {
  const diagnostic = document.getElementById("porthole-skeleton-validation-error");
  if (diagnostic) {
    diagnostic.remove();
  }
}

function renderSelectionOutline() {
  document.querySelectorAll(".skeleton-selected-node").forEach((node) => {
    node.classList.remove("skeleton-selected-node");
  });

  const bootstrap = portholeWebState.bootstrap;
  const editorState = bootstrap && bootstrap.editorState ? bootstrap.editorState : null;
  if (!editorState || editorState.mode !== "edit" || typeof editorState.selectionPath !== "string") {
    return;
  }

  const selectionNode = document.querySelector(`[data-skeleton-path="${cssEscape(editorState.selectionPath)}"]`);
  if (selectionNode instanceof HTMLElement) {
    selectionNode.classList.add("skeleton-selected-node");
  }
}

function renderInsertionSlots(renderedSkeleton) {
  const canvas = document.querySelector(".canvas");
  if (!(canvas instanceof HTMLElement)) {
    return;
  }

  let overlay = canvas.querySelector(".component-slot-layer");
  if (!(overlay instanceof HTMLElement)) {
    overlay = document.createElement("div");
    overlay.className = "component-slot-layer";
    canvas.appendChild(overlay);
  }
  overlay.innerHTML = "";

  const bootstrap = portholeWebState.bootstrap;
  const editorState = bootstrap && bootstrap.editorState ? bootstrap.editorState : null;
  const armedComponent = portholeWebState.armedComponent;
  if (!editorState || editorState.mode !== "edit" || !armedComponent) {
    return;
  }

  const targets = computeInsertionTargets(renderedSkeleton)
    .filter((target) => componentSupportsTarget(armedComponent, target.kinds));

  targets.forEach((target) => {
    const slot = document.createElement("button");
    slot.type = "button";
    slot.className = "component-slot";
    slot.dataset.action = "insert-component-slot";
    slot.dataset.targetPath = target.path;
    slot.textContent = target.path === "root" ? "Legg til i rotnivå" : "Legg til her";

    const rect = resolveInsertionTargetRect(target.path, canvas);
    if (rect) {
      slot.style.left = `${Math.max(12, rect.left)}px`;
      slot.style.top = `${Math.max(12, rect.top)}px`;
    } else if (target.path === "root") {
      slot.classList.add("floating");
    } else {
      return;
    }

    overlay.appendChild(slot);
  });
}

function resolveInsertionTargetRect(path, canvas) {
  if (!(canvas instanceof HTMLElement)) {
    return null;
  }
  const canvasRect = canvas.getBoundingClientRect();
  if (path === "root") {
    const rootNode = canvas.querySelector("#porthole-skeleton-root > [data-skeleton-path='root']");
    if (rootNode instanceof HTMLElement) {
      const rect = rootNode.getBoundingClientRect();
      return {
        left: rect.right - canvasRect.left - 124,
        top: rect.top - canvasRect.top + 8,
      };
    }
    return {
      left: Math.max(16, canvasRect.width / 2 - 72),
      top: Math.max(16, canvasRect.height / 2 - 18),
    };
  }

  const targetNode = canvas.querySelector(`[data-skeleton-path="${cssEscape(path)}"]`);
  if (!(targetNode instanceof HTMLElement)) {
    return null;
  }
  const rect = targetNode.getBoundingClientRect();
  return {
    left: rect.right - canvasRect.left - 124,
    top: rect.top - canvasRect.top + 8,
  };
}

function computeInsertionTargets(rawSkeleton) {
  if (!rawSkeleton || typeof rawSkeleton !== "object") {
    return [{ path: "root", kinds: ["root"] }];
  }

  const root = decodeSkeletonElementForEditor(rawSkeleton);
  const rootKind = root ? root.type.toLowerCase() : null;
  const targets = [{
    path: "root",
    kinds: ["root"].concat(rootKind ? [rootKind] : []),
  }];

  if (!root) {
    return targets;
  }

  walkInsertionTargets(root, "root", targets, true);
  return targets;
}

function walkInsertionTargets(element, path, output, skipCurrent) {
  if (!element || typeof element !== "object") {
    return;
  }

  const kind = typeof element.type === "string" ? element.type.toLowerCase() : "";
  if (!skipCurrent && canContainInsertedChildren(kind)) {
    output.push({ path, kinds: [kind] });
  }

  const children = childElementsForEditor(element);
  children.forEach((child, index) => {
    walkInsertionTargets(child, `${path}.${index}`, output, false);
  });
}

function childElementsForEditor(element) {
  return childElementEntriesForEditor(element).map((entry) => entry.child);
}

function childElementEntriesForEditor(element) {
  if (!element || typeof element !== "object") {
    return [];
  }

  switch (element.type) {
    case "VStack":
    case "HStack": {
      if (Array.isArray(element.value)) {
        return decodeChildEntries(element.value);
      }
      const raw = element.value && typeof element.value === "object" ? element.value : {};
      return decodeChildEntries(Array.isArray(raw.elements) ? raw.elements : []);
    }
    case "ScrollView":
    case "ZStack":
    case "Grid": {
      const raw = element.value && typeof element.value === "object" ? element.value : {};
      return decodeChildEntries(Array.isArray(raw.elements) ? raw.elements : []);
    }
    case "Section": {
      const raw = element.value && typeof element.value === "object" ? element.value : {};
      const entries = [];
      if (raw.header) {
        const header = decodeSkeletonElementForEditor(raw.header);
        if (header) {
          entries.push({ segment: "header", child: header });
        }
      }
      entries.push(...decodeChildEntries(Array.isArray(raw.content) ? raw.content : []));
      if (raw.footer) {
        const footer = decodeSkeletonElementForEditor(raw.footer);
        if (footer) {
          entries.push({ segment: "footer", child: footer });
        }
      }
      return entries;
    }
    case "Tabs": {
      const raw = element.value && typeof element.value === "object" ? element.value : {};
      const panels = Array.isArray(raw.panels) ? raw.panels : [];
      let offset = 0;
      const entries = [];
      panels.forEach((panel) => {
        const content = panel && Array.isArray(panel.content) ? panel.content : [];
        decodeChildEntries(content, offset).forEach((entry) => entries.push(entry));
        offset += content.length;
      });
      return entries;
    }
    default:
      return [];
  }
}

function decodeChildList(rawChildren) {
  return decodeChildEntries(rawChildren).map((entry) => entry.child);
}

function decodeChildEntries(rawChildren, offset = 0) {
  if (!Array.isArray(rawChildren)) {
    return [];
  }
  return rawChildren.map((child, index) => {
    const decoded = decodeSkeletonElementForEditor(child);
    return decoded ? { segment: String(offset + index), child: decoded } : null;
  }).filter(Boolean);
}

function decodeSkeletonElementForEditor(raw) {
  if (!raw || typeof raw !== "object") {
    return null;
  }
  const keys = Object.keys(raw);
  const supported = [
    "VStack", "HStack", "Text", "AttachmentField", "FileUpload", "TextField", "TextArea", "Button", "List", "Divider",
    "Object", "Section", "ScrollView", "Spacer", "Image", "Reference", "ZStack", "Grid", "Toggle", "Picker", "Tabs",
    "Visualization",
  ];
  const elementKey = keys.find((key) => supported.includes(key));
  if (elementKey) {
    return { type: elementKey, value: raw[elementKey] };
  }
  if (Array.isArray(raw)) {
    return { type: "VStack", value: raw };
  }
  return { type: "Object", value: raw };
}

function canContainInsertedChildren(kind) {
  return ["vstack", "hstack", "scrollview", "section", "grid", "zstack"].includes(kind);
}

function componentSupportsTarget(component, targetKinds) {
  if (!component || !component.recipe || !Array.isArray(component.recipe.supportedTargetKinds)) {
    return false;
  }
  const supportedKinds = new Set(component.recipe.supportedTargetKinds.map((value) => String(value || "").toLowerCase().trim()));
  return targetKinds.some((kind) => supportedKinds.has(String(kind || "").toLowerCase().trim()));
}

function handleCanvasSelectionClick(rawTarget) {
  const bootstrap = portholeWebState.bootstrap;
  const editorState = bootstrap && bootstrap.editorState ? bootstrap.editorState : null;
  if (!editorState || editorState.mode !== "edit") {
    return false;
  }
  if (rawTarget.closest("input, textarea, select, button, a, label")) {
    return false;
  }
  const selectionNode = rawTarget.closest("[data-skeleton-path]");
  if (!(selectionNode instanceof HTMLElement)) {
    return false;
  }
  const path = selectionNode.getAttribute("data-skeleton-path");
  if (!path) {
    return false;
  }
  void runAction("editor.selection.set", { path });
  return true;
}

function cssEscape(value) {
  if (window.CSS && typeof window.CSS.escape === "function") {
    try {
      return window.CSS.escape(String(value));
    } catch (_ignore) {
      // Fall through to the conservative escape below.
    }
  }
  return String(value)
    .replace(/^([0-9])/, "\\3$1 ")
    .replace(/[^a-zA-Z0-9_-]/g, "\\$&");
}

function querySelectorSafe(root, selector) {
  if (!root || typeof root.querySelector !== "function" || !selector) {
    return null;
  }
  try {
    return root.querySelector(selector);
  } catch (error) {
    console.warn("Ignoring invalid selector during Porthole render", selector, error);
    return null;
  }
}

function renderReferenceWorkspace(references) {
  const rows = references.map((entry) => {
    const referenceState = resolveReferenceState(entry.label);
    const connected = referenceState && referenceState.connected === true;
    const hasState = referenceState && Object.prototype.hasOwnProperty.call(referenceState, "state");
    const statePreview = hasState ? JSON.stringify(referenceState.state, null, 2) : null;

    return `
      <article class="reference-card">
        <div class="reference-card-header">
          <div>
            <h3>${escapeHTML(entry.label)}</h3>
            <p>${escapeHTML(entry.endpoint)}</p>
          </div>
          <span class="reference-status ${connected ? "connected" : "disconnected"}">
            ${connected ? "Tilkoblet" : "Ikke tilkoblet"}
          </span>
        </div>
        <div class="reference-card-actions">
          <button
            type="button"
            class="reference-card-button"
            data-action="select-reference"
            data-label="${escapeAttr(entry.label)}"
          >
            Vis i inspector
          </button>
        </div>
        ${statePreview ? `<pre class="reference-state-preview">${escapeHTML(statePreview)}</pre>` : "<p class='reference-state-empty'>Ingen state eksponert ennå.</p>"}
      </article>
    `;
  }).join("");

  return `
    <section class="reference-workspace">
      <header class="reference-workspace-header">
        <h2>Konfigurasjonen bruker referanser</h2>
        <p>Denne CellConfiguration har ingen egen skeleton. Web-klienten viser derfor de tilkoblede referansene direkte, slik at du fortsatt kan browse, inspisere og fortsette å bygge videre.</p>
      </header>
      <div class="reference-grid">
        ${rows}
      </div>
    </section>
  `;
}

function resolveReferenceState(label) {
  const bootstrap = portholeWebState.bootstrap;
  if (!bootstrap || !bootstrap.state || typeof bootstrap.state !== "object") {
    return {};
  }
  const value = bootstrap.state[label];
  return value && typeof value === "object" ? value : {};
}

function handleRendererFieldInput(binding, value) {
  rememberPersistentFieldValue(binding, value);

  const descriptor = resolveEditorDraftDescriptor(binding);
  if (descriptor) {
    scheduleSilentFieldAction(descriptor.setDraftKeypath, { text: String(value ?? "") }, 240);
    return;
  }

  const targetKeypath = binding && typeof binding.targetKeypath === "string"
    ? binding.targetKeypath.trim()
    : "";
  if (!targetKeypath) {
    return;
  }

  if (isMermaidRenderKeypath(targetKeypath)) {
    return;
  }

  scheduleSilentFieldAction(targetKeypath, String(value ?? ""), 240);
}

function rememberPersistentFieldValue(binding, value) {
  const targetKeypath = binding && typeof binding.targetKeypath === "string"
    ? binding.targetKeypath.trim()
    : "";
  if (!targetKeypath) {
    return;
  }

  portholeWebState.fieldValueMemory[targetKeypath] = {
    value: String(value ?? ""),
    sourceKeypath: binding && typeof binding.sourceKeypath === "string" ? binding.sourceKeypath.trim() : "",
    updatedAt: Date.now(),
  };
}

function forgetPersistentFieldValue(targetKeypath) {
  const normalizedTarget = typeof targetKeypath === "string" ? targetKeypath.trim() : "";
  if (!normalizedTarget || !portholeWebState.fieldValueMemory) {
    return;
  }

  delete portholeWebState.fieldValueMemory[normalizedTarget];
}

function reapplyPersistentFieldValues() {
  const renderer = portholeWebState.renderer;
  if (!renderer || typeof renderer.setFieldValueByTarget !== "function") {
    return;
  }

  const remembered = portholeWebState.fieldValueMemory && typeof portholeWebState.fieldValueMemory === "object"
    ? portholeWebState.fieldValueMemory
    : {};
  Object.entries(remembered).forEach(([targetKeypath, entry]) => {
    if (!targetKeypath || !entry || typeof entry !== "object") {
      return;
    }
    renderer.setFieldValueByTarget(targetKeypath, String(entry.value ?? ""), true);
  });
}

function resolveRendererActionRoute(keypath, payload, meta) {
  if (meta && (meta.sourceCellEndpoint !== undefined || meta.mount !== undefined)) {
    const mount = meta.mount;
    if (typeof meta.sourceCellEndpoint !== "string" || !meta.sourceCellEndpoint.trim()
      || !mount || !["instanceID", "componentID", "revision"].every((key) => typeof mount[key] === "string" && mount[key].trim())) {
      const message = "Komponentens kildehandling mangler endepunkt eller monteringsmetadata.";
      portholeWebState.error = message;
      renderSkeletonValidationDiagnostic(message);
      throw new Error(message);
    }
    return { keypath, payload, sourceCellEndpoint: meta.sourceCellEndpoint,
      mount: { instanceID: mount.instanceID, componentID: mount.componentID, revision: mount.revision } };
  }
  const trigger = meta && typeof meta.trigger === "string" ? meta.trigger : "";
  const binding = meta && meta.binding && meta.binding.element ? meta.binding : null;
  const sourceKeypath = binding && typeof binding.sourceKeypath === "string" ? binding.sourceKeypath.trim() : "";
  const targetKeypath = binding && typeof binding.targetKeypath === "string" ? binding.targetKeypath.trim() : "";
  if (
    trigger === "textarea-submit" &&
    targetKeypath === "chatHub.setComposer" &&
    sourceKeypath === "chatHub.state.composer.body"
  ) {
    const draft = typeof payload === "string" ? payload : String(payload ?? "");
    return {
      keypath: "chatHub.prompt.submit",
      payload: {
        draft,
        body: draft,
        text: draft,
      },
    };
  }
  return { keypath, payload };
}

async function runComponentSourceAction(action) {
  portholeWebState.error = null;
  portholeWebState.notice = null;
  try {
    const response = await requestActionPayload(action.keypath, action.payload, 30000, action);
    const feedback = resolveActionFeedback(action.keypath, action.payload, response, { sourceAction: true });
    if (feedback.error) throw new Error(feedback.error);
    // A source keypath may have the same name as a host navigation/editor action.
    // Do not apply its result or optimistic state to the host's keypath namespace.
    portholeWebState.notice = feedback.notice;
    render({ forceShell: true, preserveSkeletonDOM: true });
    return normalizeActionResultValue(actionResultPayload(response));
  } catch (error) {
    portholeWebState.error = error instanceof Error ? error.message : String(error);
    render({ forceShell: true, preserveSkeletonDOM: true });
    renderSkeletonValidationDiagnostic(portholeWebState.error);
    throw error;
  }
}

function resolveRendererActionPayload({ keypath, payload, meta, state }) {
  const activeBinding = meta && meta.binding && meta.binding.element ? meta.binding : null;
  const trigger = meta && typeof meta.trigger === "string" ? meta.trigger : "";
  if ((trigger === "textfield-submit" || trigger === "textarea-submit") && activeBinding) {
    return readRendererBindingValue(activeBinding);
  }

  if (trigger === "button") {
    const mermaidPayload = resolveMermaidRendererButtonPayload(keypath, payload, state);
    if (mermaidPayload !== undefined) {
      return mermaidPayload;
    }

    const conferencePayload = resolveConferenceParticipantButtonPayload(keypath, payload, state);
    if (conferencePayload !== undefined) {
      return conferencePayload;
    }

    const enrichedPayload = resolveChatWorkbenchButtonPayload(keypath, payload, state);
    if (enrichedPayload !== undefined) {
      return enrichedPayload;
    }
  }

  if (payload == null || payload === "" || isEmptyPlainObject(payload)) {
    const matchingBinding = activeBinding && activeBinding.targetKeypath === keypath
      ? activeBinding
      : findFieldBindingByTarget(state, keypath);
    if (matchingBinding && matchingBinding.element) {
      return readRendererBindingValue(matchingBinding);
    }
  }

  return payload;
}

function resolveMermaidRendererButtonPayload(keypath, payload, rendererState) {
  const normalized = String(keypath || "").trim();
  if (!isMermaidRenderKeypath(normalized)) {
    return undefined;
  }

  const source = readRendererFieldValue(rendererState, normalized);
  if (!source) {
    return payload;
  }

  if (payload != null && typeof payload === "object" && !Array.isArray(payload)) {
    return { ...payload, source };
  }

  return source;
}

function isMermaidRenderKeypath(keypath) {
  const normalized = String(keypath || "").trim();
  return normalized.endsWith(".render.mermaid") || normalized.endsWith(".renderMermaid");
}

function resolveConferenceParticipantButtonPayload(keypath, payload, rendererState) {
  const normalized = String(keypath || "").trim();
  if (
    normalized !== "conferenceParticipantShell.matchmaking.searchPeople" &&
    normalized !== "conferenceParticipantPreviewShell.matchmaking.searchPeople"
  ) {
    return undefined;
  }

  if (!isEmptyActionPayload(payload)) {
    return payload;
  }

  const field = readRendererFieldValue(rendererState, normalized) || readPersistentFieldValue(normalized);
  return field ? field : payload;
}

function resolveChatWorkbenchButtonPayload(keypath, payload, rendererState) {
  const normalized = String(keypath || "").trim();
  if (!normalized.startsWith("chatHub.")) {
    return undefined;
  }
  const field = (targetKeypath) => {
    const rendererValue = readRendererFieldValue(rendererState, targetKeypath);
    if (rendererValue) {
      return rendererValue;
    }
    return readPersistentFieldValue(targetKeypath);
  };
  const objectWithValues = (entries) => {
    const result = {};
    entries.forEach(([key, value]) => {
      if (value != null && String(value).length > 0) {
        result[key] = String(value);
      }
    });
    return Object.keys(result).length > 0 ? result : payload;
  };

  switch (normalized) {
    case "chatHub.prompt.submit": {
      const draft = field("chatHub.setComposer") || readChatHubStoredPromptDraft();
      const basePayload = payload && typeof payload === "object" && !Array.isArray(payload)
        ? payload
        : {};
      return draft ? { ...basePayload, text: draft, draft, body: draft } : payload;
    }
    case "chatHub.assistant.analyzeDraft": {
      const draft = field("chatHub.setComposer") || readChatHubStoredPromptDraft();
      return draft ? { text: draft, draft, body: draft } : payload;
    }
    case "chatHub.ui.openMatchedResourceLibrary":
      if (hasExplicitChatResourcePayload(payload)) {
        return payload;
      }
      return currentChatHubMatchedResourcePayload(payload);
    case "chatHub.docsRAG.search":
    case "chatHub.docsRAG.openTopDocument":
    case "chatHub.docsRAG.askRAG": {
      const query = field("chatHub.docsRAG.setQuery") || readChatHubDocsRAGQuery();
      return query
        ? {
            ...(payload && typeof payload === "object" && !Array.isArray(payload) ? payload : {}),
            query,
            question: query,
            text: query,
          }
        : payload;
    }
  }

  if (!isEmptyActionPayload(payload)) {
    return payload;
  }

  switch (normalized) {
    case "chatHub.sendComposedMessage": {
      const body = field("chatHub.setComposer");
      return body ? { body, text: body } : payload;
    }
    case "chatHub.poll.create":
      return objectWithValues([
        ["question", field("chatHub.poll.setQuestion")],
        ["optionsText", field("chatHub.poll.setOptions")],
      ]);
    case "chatHub.idea.capture":
      return objectWithValues([
        ["title", field("chatHub.idea.title")],
        ["content", field("chatHub.idea.content")],
      ]);
    case "chatHub.todo.create":
      return objectWithValues([
        ["title", field("chatHub.todo.title")],
        ["note", field("chatHub.todo.note")],
        ["dueAtText", field("chatHub.todo.dueAtText")],
        ["assigneeUUID", field("chatHub.todo.assigneeUUID")],
      ]);
    case "chatHub.project.create":
      return objectWithValues([
        ["title", field("chatHub.project.title")],
        ["description", field("chatHub.project.description")],
        ["membersText", field("chatHub.project.membersText")],
      ]);
    case "chatHub.reminder.create":
      return objectWithValues([
        ["title", field("chatHub.reminder.title")],
        ["scheduledAtText", field("chatHub.reminder.scheduledAtText")],
        ["scope", field("chatHub.reminder.scope")],
      ]);
    case "chatHub.meeting.schedule":
      return objectWithValues([
        ["title", field("chatHub.meeting.title")],
        ["targetProfileID", field("chatHub.meeting.targetProfileID")],
        ["proposedTimesText", field("chatHub.meeting.proposedTimesText")],
      ]);
    case "chatHub.agent.review.create":
      return objectWithValues([
        ["actionID", field("chatHub.agent.review.actionID")],
        ["reason", field("chatHub.agent.review.reason")],
        ["argumentsText", field("chatHub.agent.review.argumentsText")],
        ["signatureBase64", field("chatHub.agent.review.signatureBase64")],
      ]);
    case "chatHub.invite":
      return objectWithValues([
        ["profileID", field("chatHub.inviteDraft.profileID")],
        ["userUUID", field("chatHub.inviteDraft.userUUID")],
        ["title", field("chatHub.inviteDraft.title")],
      ]);
    case "chatHub.assistant.setCandidateQuery": {
      const query = field("chatHub.assistant.setCandidateQuery");
      return query ? { query, text: query } : payload;
    }
    default:
      return undefined;
  }
}

function hasExplicitChatResourcePayload(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    return false;
  }
  const stringKeys = [
    "resourceID",
    "id",
    "configurationName",
    "sourceCellEndpoint",
    "documentationID",
    "documentationPath",
    "caseID",
    "truthSourceID",
    "agentActionID",
  ];
  return stringKeys.some((key) => typeof payload[key] === "string" && payload[key].trim().length > 0);
}

function currentChatHubMatchedResourcePayload(fallbackPayload) {
  const chatHubState = readChatHubState();
  const assistant = chatHubState && chatHubState.assistant && typeof chatHubState.assistant === "object"
    ? chatHubState.assistant
    : {};
  const suggestion = assistant.latestSuggestion && typeof assistant.latestSuggestion === "object"
    ? assistant.latestSuggestion
    : {};
  const matches = Array.isArray(assistant.resourceMatches) ? assistant.resourceMatches : [];
  const targetPhrase = typeof suggestion.targetPhrase === "string" ? suggestion.targetPhrase.trim() : "";
  const purposeRef = typeof suggestion.purposeRef === "string" ? suggestion.purposeRef.trim() : "";
  const sourceText = typeof suggestion.sourceText === "string" ? suggestion.sourceText.trim() : "";
  const selected = matches.find((match) => match && typeof match === "object" && targetPhrase && (
    match.title === targetPhrase || match.configurationName === targetPhrase
  )) || matches.find((match) => match && typeof match === "object" && purposeRef && Array.isArray(match.purposeRefs) && match.purposeRefs.includes(purposeRef));

  if (!selected) {
    return sourceText ? { text: sourceText, query: sourceText } : fallbackPayload;
  }

  const payload = {
    ...(fallbackPayload && typeof fallbackPayload === "object" && !Array.isArray(fallbackPayload) ? fallbackPayload : {}),
    resourceID: selected.id || "",
    configurationName: selected.configurationName || selected.title || targetPhrase,
    sourceCellEndpoint: selected.sourceCellEndpoint || "",
  };
  if (selected.documentationID) {
    payload.documentationID = selected.documentationID;
  }
  if (selected.documentationURL) {
    payload.documentationURL = selected.documentationURL;
  }
  if (sourceText) {
    payload.text = sourceText;
    payload.query = sourceText;
  }
  return payload;
}

function readChatHubState() {
  const bootstrap = portholeWebState.bootstrap;
  return bootstrap &&
    bootstrap.state &&
    bootstrap.state.chatHub &&
    typeof bootstrap.state.chatHub === "object" &&
    bootstrap.state.chatHub.state &&
    typeof bootstrap.state.chatHub.state === "object"
    ? bootstrap.state.chatHub.state
    : null;
}

function readChatHubDocsRAGQuery() {
  const chatHubState = readChatHubState();
  const docsRAG = chatHubState && chatHubState.docsRAG && typeof chatHubState.docsRAG === "object"
    ? chatHubState.docsRAG
    : {};
  const ui = chatHubState && chatHubState.ui && typeof chatHubState.ui === "object"
    ? chatHubState.ui
    : {};
  return typeof docsRAG.query === "string" && docsRAG.query.trim()
    ? docsRAG.query.trim()
    : typeof ui.docsRAGQuery === "string" && ui.docsRAGQuery.trim()
      ? ui.docsRAGQuery.trim()
      : "";
}

function isEmptyActionPayload(payload) {
  return payload == null || payload === "" || isEmptyPlainObject(payload);
}

function isEmptyPlainObject(value) {
  return Boolean(
    value &&
    typeof value === "object" &&
    !Array.isArray(value) &&
    Object.keys(value).length === 0
  );
}

function readRendererFieldValue(rendererState, targetKeypath) {
  const binding = findFieldBindingByTarget(rendererState, targetKeypath);
  return binding ? readRendererBindingValue(binding) : "";
}

function readPersistentFieldValue(targetKeypath) {
  const normalizedTarget = typeof targetKeypath === "string" ? targetKeypath.trim() : "";
  if (!normalizedTarget || !portholeWebState.fieldValueMemory) {
    return "";
  }
  const entry = portholeWebState.fieldValueMemory[normalizedTarget];
  if (!entry || typeof entry !== "object") {
    return "";
  }
  return String(entry.value ?? "");
}

function readChatHubStoredPromptDraft() {
  const bootstrap = portholeWebState.bootstrap;
  const chatHubState = bootstrap &&
    bootstrap.state &&
    bootstrap.state.chatHub &&
    typeof bootstrap.state.chatHub === "object" &&
    bootstrap.state.chatHub.state &&
    typeof bootstrap.state.chatHub.state === "object"
    ? bootstrap.state.chatHub.state
    : null;
  if (!chatHubState) {
    return "";
  }

  const composerBody = chatHubState.composer &&
    typeof chatHubState.composer === "object" &&
    typeof chatHubState.composer.body === "string"
    ? chatHubState.composer.body.trim()
    : "";
  if (composerBody) {
    return composerBody;
  }

  return chatHubState.ui &&
    typeof chatHubState.ui === "object" &&
    typeof chatHubState.ui.promptDraft === "string"
    ? chatHubState.ui.promptDraft.trim()
    : "";
}

function readRendererBindingValue(binding) {
  if (!binding) {
    return "";
  }
  if (typeof binding.readValue === "function") {
    return String(binding.readValue() ?? "");
  }
  if (binding.element && "value" in binding.element) {
    return String(binding.element.value ?? "");
  }
  if (binding.element && binding.element.isContentEditable) {
    return String(binding.element.textContent ?? "");
  }
  return "";
}

function findFieldBindingByTarget(rendererState, keypath) {
  if (!rendererState || !Array.isArray(rendererState.fieldBindings)) {
    return null;
  }
  return rendererState.fieldBindings.find((binding) => binding && binding.targetKeypath === keypath) || null;
}

function resolveEditorDraftDescriptor(binding) {
  if (!binding || typeof binding.sourceKeypath !== "string") {
    return null;
  }

  const sourceKeypath = binding.sourceKeypath.trim();
  if (!sourceKeypath.endsWith(".editorDraft")) {
    return null;
  }

  const label = sourceKeypath.split(".")[0];
  if (!label) {
    return null;
  }

  const bootstrap = portholeWebState.bootstrap;
  const cellState = bootstrap && bootstrap.state && typeof bootstrap.state === "object"
    ? bootstrap.state[label]
    : null;
  const editor = cellState && typeof cellState === "object" && cellState.editor && typeof cellState.editor === "object"
    ? cellState.editor
    : null;
  const setDraftKeypath = editor && typeof editor.setDraftKeypath === "string"
    ? editor.setDraftKeypath.trim()
    : "";

  if (!setDraftKeypath) {
    return null;
  }

  return {
    label,
    setDraftKeypath,
  };
}

function scheduleSilentFieldAction(keypath, payload, delayMs) {
  const timerKey = keypath;
  const existing = portholeWebState.fieldActionTimers[timerKey];
  if (existing) {
    window.clearTimeout(typeof existing === "object" ? existing.timerId : existing);
  }

  const delay = Math.max(120, Number(delayMs) || 240);
  portholeWebState.socketRefreshSuppressUntil = Math.max(
    portholeWebState.socketRefreshSuppressUntil || 0,
    Date.now() + delay + 1500
  );

  const entry = {
    timerId: null,
    keypath,
    payload,
    actionSeq: nextPortholeOrderingSequence("action"),
    promise: null,
  };
  entry.timerId = window.setTimeout(() => {
    entry.timerId = null;
    void startSilentFieldAction(entry);
  }, delay);

  portholeWebState.fieldActionTimers[timerKey] = entry;
}

function startSilentFieldAction(entry) {
  if (!entry || typeof entry !== "object") {
    return Promise.resolve();
  }
  if (entry.promise && typeof entry.promise.then === "function") {
    return entry.promise;
  }

  const timerKey = entry.keypath;
  entry.promise = (async () => {
    try {
      const actionResult = await postJSON(actionURL, { keypath: entry.keypath, payload: entry.payload });
      applyActionResultState(entry.keypath, actionResult, entry.payload, entry.actionSeq);
    } catch (_ignore) {
      // Keep draft syncing silent to avoid banner churn while typing.
    } finally {
      if (portholeWebState.fieldActionTimers[timerKey] === entry) {
        delete portholeWebState.fieldActionTimers[timerKey];
      }
    }
  })();
  return entry.promise;
}

function cancelPendingFieldAction(keypath) {
  const timerKey = String(keypath || "").trim();
  if (!timerKey) {
    return;
  }
  const existing = portholeWebState.fieldActionTimers[timerKey];
  if (!existing) {
    return;
  }
  if (existing && typeof existing === "object" && existing.promise) {
    return;
  }
  window.clearTimeout(typeof existing === "object" ? existing.timerId : existing);
  delete portholeWebState.fieldActionTimers[timerKey];
}

async function flushPendingFieldActions() {
  const pendingEntries = Object.values(portholeWebState.fieldActionTimers)
    .filter((entry) => entry && typeof entry === "object" && typeof entry.keypath === "string");

  if (pendingEntries.length === 0) {
    return;
  }

  for (const entry of pendingEntries) {
    if (entry.timerId != null) {
      window.clearTimeout(entry.timerId);
      entry.timerId = null;
    }
  }

  await Promise.all(pendingEntries.map((entry) => startSilentFieldAction(entry)));
}

function formatSkeletonText({ keypath, context, value }) {
  const normalizedKeypath = typeof keypath === "string" ? keypath.trim() : "";
  if (
    normalizedKeypath.endsWith(".state.last_render.rendered_html") ||
    normalizedKeypath.endsWith(".state.lastRender.renderedHTML")
  ) {
    return {
      html: String(value || ""),
    };
  }

  if (
    normalizedKeypath.endsWith(".state.last_render.rendered_fallback_text") ||
    normalizedKeypath.endsWith(".state.lastRender.renderedFallbackText")
  ) {
    const renderedHTML = resolveRenderedHTMLForFallbackKeypath(normalizedKeypath);
    return {
      html: renderedHTML || escapeHTML(value || ""),
    };
  }

  if (normalizedKeypath.endsWith(".state.identityLinking.currentChallengeRenderedHTML")) {
    return {
      html: String(value || ""),
    };
  }

  if (keypath !== "text") {
    return null;
  }

  if (!context || typeof context !== "object") {
    return null;
  }

  const contentType = typeof context.contentType === "string" ? context.contentType : "text/plain";
  if (contentType !== "text/markdown") {
    return null;
  }

  return {
    html: renderMarkdownLite(value || ""),
  };
}

function resolveRenderedHTMLForFallbackKeypath(keypath) {
  const variants = [
    {
      fallbackSuffix: ".state.last_render.rendered_fallback_text",
      path: ["state", "last_render", "rendered_html"],
    },
    {
      fallbackSuffix: ".state.lastRender.renderedFallbackText",
      path: ["state", "lastRender", "renderedHTML"],
    },
  ];

  for (const variant of variants) {
    if (!keypath.endsWith(variant.fallbackSuffix)) {
      continue;
    }
    const label = keypath.substring(0, keypath.length - variant.fallbackSuffix.length);
    if (!label) {
      return "";
    }
    let current = resolveReferenceState(label);
    for (const segment of variant.path) {
      if (!current || typeof current !== "object") {
        return "";
      }
      current = current[segment];
    }
    return typeof current === "string" ? current : "";
  }

  return "";
}

function enhanceRenderedQRCodes(root) {
  if (!(root instanceof HTMLElement)) {
    return;
  }

  root.querySelectorAll("[data-qr-payload]").forEach((node) => {
    if (!(node instanceof HTMLElement)) {
      return;
    }

    const payload = typeof node.dataset.qrPayload === "string" ? node.dataset.qrPayload.trim() : "";
    if (!payload) {
      return;
    }

    const renderTarget = node.querySelector("[data-qr-render-target]");
    if (!(renderTarget instanceof HTMLElement)) {
      return;
    }

    if (renderTarget.dataset.qrRenderedPayload === payload) {
      return;
    }

    if (!window.QRCode || typeof window.QRCode.toDataURL !== "function") {
      renderTarget.innerHTML = "<p class=\"identity-link-qr-error\">QR-renderer er ikke tilgjengelig i nettleseren akkurat nå.</p>";
      return;
    }

    renderTarget.innerHTML = "<p class=\"identity-link-qr-placeholder\">Genererer QR…</p>";
    const label = typeof node.dataset.qrLabel === "string" && node.dataset.qrLabel.trim()
      ? node.dataset.qrLabel.trim()
      : "Identity link challenge";

    window.QRCode.toDataURL(payload, {
      errorCorrectionLevel: "M",
      margin: 1,
      width: 224,
      color: {
        dark: "#0B1620",
        light: "#F5FBFF",
      },
    }, (error, dataURL) => {
      if (!(renderTarget instanceof HTMLElement) || !renderTarget.isConnected) {
        return;
      }

      if (error || typeof dataURL !== "string" || !dataURL) {
        renderTarget.innerHTML = "<p class=\"identity-link-qr-error\">QR kunne ikke genereres. Bruk deep-linken under som fallback.</p>";
        return;
      }

      renderTarget.innerHTML = "";
      const image = document.createElement("img");
      image.className = "identity-link-qr-image";
      image.src = dataURL;
      image.alt = label;
      image.width = 224;
      image.height = 224;
      renderTarget.appendChild(image);
      renderTarget.dataset.qrRenderedPayload = payload;
    });
  });
}

function buildShellSignature() {
  const bootstrap = portholeWebState.bootstrap;
  const editorState = bootstrap && bootstrap.editorState ? bootstrap.editorState : normalizeEditorState(null, null);
  const editModeActive = editorState.mode === "edit";
  const references = getReferences().map((entry) => `${entry.label}:${entry.endpoint}`).join("|");
  const menuPreferences = normalizeMenuPreferences(portholeWebState.menuPreferences);
  const expandedMenus = Object.keys(portholeWebState.expandedMenus)
    .filter((key) => portholeWebState.expandedMenus[key])
    .sort()
    .join(",");
  const menus = menuKeys
    .map((key) => {
      const entries = bootstrap && bootstrap.menus && Array.isArray(bootstrap.menus[key]) ? bootstrap.menus[key] : [];
      return entries.map((entry) => entry.uuid || entry.name || "").join(",");
    })
    .join("||");
  const library = getLibraryConfigurations().map((entry) => entry.uuid || entry.name || "").join(",");
  const componentPalette = editModeActive
    ? getComponentPaletteItems().map((entry) => entry.id || entry.title || "").join(",")
    : "";
  const navigationStack = (Array.isArray(portholeWebState.navigationStack) ? portholeWebState.navigationStack : [])
    .map((entry) => normalizeConfigurationNavigationEntry(entry))
    .filter(Boolean)
    .map((entry) => `${entry.id}:${entry.name}`)
    .join("|");
  const navigationPending = portholeWebState.navigationPending && portholeWebState.navigationPending.targetEntry
    ? normalizeConfigurationNavigationEntry(portholeWebState.navigationPending.targetEntry)
    : null;

  return [
    bootstrap && bootstrap.sessionId ? bootstrap.sessionId : "",
    editorState.mode,
    editorState.isDirty ? "1" : "0",
    editorState.canUndo ? "1" : "0",
    editorState.canRedo ? "1" : "0",
    String(editorState.revision),
    editorState.selectionPath || "",
    editorState.sourceBacked ? "1" : "0",
    editorState.canEdit ? "1" : "0",
    editorState.sourceCellEndpoint || "",
    editorState.accessSummary || "",
    editorState.accessInstruction || "",
    references,
    menus,
    library,
    componentPalette,
    expandedMenus,
    menuPreferences.topExpansionStyle,
    menuPreferences.bottomExpansionStyle,
    menuPreferences.showTitles ? "1" : "0",
    menuPreferences.criteriaText,
    portholeWebState.menuSettingsOpen ? "1" : "0",
    portholeWebState.toolsPanelOpen ? "1" : "0",
    portholeWebState.toolbarOverflowOpen ? "1" : "0",
    portholeWebState.toolbarDetailsExpanded ? "1" : "0",
    portholeWebState.edgeMenusSuppressed ? "1" : "0",
    usesCompactConvenienceMenus() ? "1" : "0",
    portholeWebState.libraryOpen ? "1" : "0",
    portholeWebState.libraryQuery || "",
    portholeWebState.libraryMenuFilter || "",
    portholeWebState.selectedLabel || "",
    portholeWebState.armedComponent ? portholeWebState.armedComponent.id || "" : "",
    portholeWebState.pendingLoad ? portholeWebState.pendingLoad.id || "" : "",
    portholeWebState.pendingAction ? portholeWebState.pendingAction.keypath || "" : "",
    navigationStack,
    navigationPending ? navigationPending.id : "",
    portholeWebState.notice || "",
    portholeWebState.error || "",
  ].join("::");
}

function ensureWebSocket() {
  const bootstrap = portholeWebState.bootstrap;
  const sessionId = bootstrap && typeof bootstrap.sessionId === "string" ? bootstrap.sessionId.trim() : "";
  if (!sessionId) {
    return;
  }

  if (
    portholeWebState.ws &&
    portholeWebState.wsSessionId === sessionId &&
    (portholeWebState.ws.readyState === WebSocket.OPEN || portholeWebState.ws.readyState === WebSocket.CONNECTING)
  ) {
    return;
  }

  closeWebSocket({ keepTimer: true });
  if (portholeWebState.wsReconnectTimer) {
    window.clearTimeout(portholeWebState.wsReconnectTimer);
    portholeWebState.wsReconnectTimer = null;
  }

  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const url = buildWebSocketURL(protocol, sessionId, bootstrap);
  const ws = new WebSocket(url);
  ws.binaryType = "arraybuffer";

  portholeWebState.ws = ws;
  portholeWebState.wsSessionId = sessionId;

  ws.onopen = () => {
    portholeWebState.wsConnected = true;
    portholeWebState.wsReconnectDelayMs = 1000;
    portholeWebState.wsReconnectAttempt = 0;
    portholeWebState.wsLastConnectedAt = new Date().toISOString();
    portholeWebState.wsLastClose = null;
    portholeWebState.wsLastError = null;
    startWebSocketHeartbeat();
    updateStatusLiveRegion();
  };

  ws.onmessage = (event) => {
    void handleSocketMessage(event.data);
  };

  ws.onerror = () => {
    portholeWebState.wsConnected = false;
    portholeWebState.wsLastError = `WebSocket error ${new Date().toISOString()}`;
    updateStatusLiveRegion();
  };

  ws.onclose = (event) => {
    rejectAllSocketRequests(new Error("WebSocket connection closed."));
    portholeWebState.wsConnected = false;
    portholeWebState.wsLastClose = describeWebSocketClose(event);
    stopWebSocketHeartbeat();
    if (portholeWebState.ws === ws) {
      portholeWebState.ws = null;
    }
    scheduleWebSocketReconnect();
    updateStatusLiveRegion();
  };
}

function buildWebSocketURL(protocol, sessionId, bootstrap) {
  const url = new URL(
    `${protocol}://${window.location.host}/browserhead/wsce/${encodeURIComponent(sessionId)}`
  );
  const bridgePresence = resolveBridgePresenceDescriptor(bootstrap);
  if (bridgePresence) {
    url.searchParams.set("participantId", bridgePresence.participantId);
    url.searchParams.set("deviceId", bridgePresence.deviceId);
    bridgePresence.topics.forEach((topic) => {
      url.searchParams.append("bridgeTopic", topic);
    });
  }
  return url.toString();
}

function resolveBridgePresenceDescriptor(bootstrap) {
  const candidate =
    bootstrap && bootstrap.bridgePresence && typeof bootstrap.bridgePresence === "object"
      ? bootstrap.bridgePresence
      : bootstrap && bootstrap.portholeState && bootstrap.portholeState.bridgePresence && typeof bootstrap.portholeState.bridgePresence === "object"
        ? bootstrap.portholeState.bridgePresence
        : null;
  if (!candidate || candidate.enabled === false) {
    return null;
  }

  const participantId =
    typeof candidate.participantId === "string" ? candidate.participantId.trim() : "";
  if (!participantId) {
    return null;
  }

  const storageKey =
    typeof candidate.deviceIdStorageKey === "string" && candidate.deviceIdStorageKey.trim()
      ? candidate.deviceIdStorageKey.trim()
      : "porthole.bridge.deviceId.default";
  const devicePrefix =
    typeof candidate.deviceIdPrefix === "string" && candidate.deviceIdPrefix.trim()
      ? candidate.deviceIdPrefix.trim()
      : "porthole-web";
  const deviceId = readOrCreateBridgeDeviceId(storageKey, devicePrefix);
  if (!deviceId) {
    return null;
  }

  const topics = Array.isArray(candidate.topics)
    ? candidate.topics
      .map((value) => (typeof value === "string" ? value.trim() : ""))
      .filter(Boolean)
    : [];

  return { participantId, deviceId, topics };
}

function readOrCreateBridgeDeviceId(storageKey, devicePrefix) {
  const fallback = `${devicePrefix}-${Math.random().toString(36).slice(2)}${Date.now().toString(36)}`;
  try {
    const storage = window.localStorage;
    const existing = storage.getItem(storageKey);
    if (existing && existing.trim()) {
      return existing.trim();
    }
    storage.setItem(storageKey, fallback);
    return fallback;
  } catch (_error) {
    return fallback;
  }
}

function closeWebSocket(options = {}) {
  const keepTimer = options.keepTimer === true;
  stopWebSocketHeartbeat();
  if (!keepTimer && portholeWebState.wsReconnectTimer) {
    window.clearTimeout(portholeWebState.wsReconnectTimer);
    portholeWebState.wsReconnectTimer = null;
  }
  if (!keepTimer && portholeWebState.socketRefreshTimer) {
    window.clearTimeout(portholeWebState.socketRefreshTimer);
    portholeWebState.socketRefreshTimer = null;
  }
  if (!keepTimer) {
    Object.values(portholeWebState.fieldActionTimers).forEach((timer) => {
      window.clearTimeout(typeof timer === "object" ? timer.timerId : timer);
    });
    portholeWebState.fieldActionTimers = {};
  }

  if (portholeWebState.ws) {
    rejectAllSocketRequests(new Error("WebSocket connection closed."));
    portholeWebState.ws.onopen = null;
    portholeWebState.ws.onmessage = null;
    portholeWebState.ws.onerror = null;
    portholeWebState.ws.onclose = null;
    try {
      portholeWebState.ws.close();
    } catch (_ignore) {
      // Best effort.
    }
    portholeWebState.ws = null;
  }

  portholeWebState.wsConnected = false;
}

function scheduleWebSocketReconnect() {
  if (portholeWebState.wsReconnectTimer) {
    return;
  }

  portholeWebState.wsReconnectAttempt += 1;
  portholeWebState.wsReconnectTimer = window.setTimeout(() => {
    portholeWebState.wsReconnectTimer = null;
    portholeWebState.wsReconnectDelayMs = Math.min(portholeWebState.wsReconnectDelayMs * 2, 15000);
    ensureWebSocket();
  }, portholeWebState.wsReconnectDelayMs);
}

function startWebSocketHeartbeat() {
  stopWebSocketHeartbeat();
  if (!canUseSocketTransport()) {
    return;
  }
  portholeWebState.wsHeartbeatTimer = window.setTimeout(() => {
    void runWebSocketHeartbeat(portholeWebState.ws);
  }, websocketHeartbeatIntervalMs);
}

function stopWebSocketHeartbeat() {
  if (portholeWebState.wsHeartbeatTimer) {
    window.clearTimeout(portholeWebState.wsHeartbeatTimer);
    portholeWebState.wsHeartbeatTimer = null;
  }
  portholeWebState.wsHeartbeatInFlight = false;
}

async function runWebSocketHeartbeat(expectedSocket) {
  if (
    portholeWebState.wsHeartbeatInFlight ||
    !expectedSocket ||
    expectedSocket !== portholeWebState.ws ||
    !canUseSocketTransport()
  ) {
    return;
  }

  portholeWebState.wsHeartbeatInFlight = true;
  try {
    await sendSocketCommand(
      "porthole.ping",
      { clientTime: new Date().toISOString() },
      { timeoutMs: websocketHeartbeatTimeoutMs }
    );
    if (expectedSocket !== portholeWebState.ws) {
      return;
    }
    portholeWebState.wsLastPongAt = new Date().toISOString();
    portholeWebState.wsLastError = null;
    startWebSocketHeartbeat();
  } catch (error) {
    if (expectedSocket !== portholeWebState.ws) {
      return;
    }
    portholeWebState.wsLastError = error instanceof Error ? error.message : String(error);
    closeWebSocket({ keepTimer: true });
    scheduleWebSocketReconnect();
    updateStatusLiveRegion();
  } finally {
    if (expectedSocket === portholeWebState.ws) {
      portholeWebState.wsHeartbeatInFlight = false;
    }
  }
}

function handlePortholeVisibilityChange() {
  if (document.visibilityState === "visible") {
    recoverWebSocketAfterPageWake();
  }
}

function handlePortholePageShow() {
  recoverWebSocketAfterPageWake();
}

function recoverWebSocketAfterPageWake() {
  if (!portholeWebState.bootstrap) {
    return;
  }
  if (!canUseSocketTransport()) {
    portholeWebState.wsReconnectDelayMs = 1000;
    if (!portholeWebState.wsReconnectTimer) {
      ensureWebSocket();
    }
    return;
  }
  if (!portholeWebState.wsHeartbeatTimer && !portholeWebState.wsHeartbeatInFlight) {
    startWebSocketHeartbeat();
  }
}

function describeWebSocketClose(event) {
  if (!event) {
    return {
      code: 0,
      reason: "",
      wasClean: false,
      at: new Date().toISOString(),
    };
  }
  return {
    code: Number.isFinite(event.code) ? event.code : 0,
    reason: typeof event.reason === "string" ? event.reason : "",
    wasClean: event.wasClean === true,
    at: new Date().toISOString(),
  };
}

function summarizeWebSocketClose(closeInfo) {
  if (!closeInfo || typeof closeInfo !== "object") {
    return "";
  }
  const code = Number.isFinite(closeInfo.code) && closeInfo.code > 0 ? `code ${closeInfo.code}` : "unknown code";
  const cleanliness = closeInfo.wasClean ? "clean close" : "unclean close";
  const reason = typeof closeInfo.reason === "string" && closeInfo.reason.trim()
    ? `reason: ${closeInfo.reason.trim()}`
    : "";
  return `Last close: ${code}, ${cleanliness}${reason ? `, ${reason}` : ""}.`;
}

async function handleSocketMessage(rawData) {
  const message = await decodeSocketPayload(rawData);
  if (!message || typeof message !== "object") {
    return;
  }

  if (message.kind === "response" || message.kind === "error") {
    resolveSocketRequestMessage(message);
    return;
  }

  const flowElement = message.kind === "flow" && message.flowElement && typeof message.flowElement === "object"
    ? message.flowElement
    : message;

  const notificationItem = extractNotificationItemFromFlowElement(flowElement);
  if (notificationItem) {
    appendLiveNotification(notificationItem);
    render({ forceShell: true, preserveSkeletonDOM: true });
  }

  if (!shouldRefreshFromFlowEvent(flowElement)) {
    return;
  }

  scheduleSocketRefresh();
}

async function requestBootstrapPayload({ shellOnly = false } = {}) {
  const isConfigurationLoad = Boolean(portholeWebState.pendingLoad);
  const timeoutMs = isConfigurationLoad ? 75000 : 30000;
  // Keep the full bootstrap snapshot on HTTP. It is large, often races with
  // page/configuration reloads, and the websocket is already used for live
  // refresh signals plus heartbeat.
  const requestURL = shellOnly ? `${bootstrapURL}?phase=shell` : bootstrapURL;
  return fetchJSON(requestURL, { timeoutMs });
}

async function requestActionPayload(keypath, payload, timeoutMs, sourceAction = null) {
  const decoratedPayload = sourceAction ? payload : decorateActionPayloadForTransport(keypath, payload);
  const request = { keypath, payload: decoratedPayload ?? null };
  if (sourceAction) {
    request.sourceCellEndpoint = sourceAction.sourceCellEndpoint;
    request.mount = sourceAction.mount;
  }
  // Web Porthole keeps websocket for live refresh signals, but actions go over HTTP so
  // button feedback does not depend on a websocket response frame arriving in time.
  const timeoutMessage = isModelBackedActionKeypath(keypath)
    ? `Butler svarte ikke innen ${Math.round((timeoutMs || chatModelBackedActionTimeoutMs) / 1000)} sekunder. Proev igjen, eller sjekk at modellen er tilgjengelig.`
    : null;
  return postJSON(
    actionURL,
    request,
    { timeoutMs, timeoutMessage }
  );
}

function decorateActionPayloadForTransport(keypath, payload) {
  const normalizedKeypath = String(keypath || "").trim();
  if (isArendalsukaParticipantAgendaMutation(normalizedKeypath)) {
    if (payload && typeof payload === "object" && !Array.isArray(payload)) {
      return { ...payload, responseMode: "ack" };
    }
    return { id: payload, responseMode: "ack" };
  }
  if (!normalizedKeypath.endsWith(".dispatchAction") || !payload || typeof payload !== "object" || Array.isArray(payload)) {
    return payload;
  }

  return {
    ...payload,
    responseMode: "ack",
  };
}

function canUseSocketTransport() {
  return Boolean(
    portholeWebState.ws &&
    portholeWebState.wsConnected &&
    portholeWebState.ws.readyState === WebSocket.OPEN
  );
}

function sendSocketCommand(command, payload, options = {}) {
  const { timeoutMs = 8000 } = options;
  if (!canUseSocketTransport()) {
    return Promise.reject(new Error("WebSocket is not connected."));
  }

  portholeWebState.socketRequestSequence += 1;
  const requestId = `ws-${Date.now()}-${portholeWebState.socketRequestSequence}`;
  const frame = {
    client: portholeWebState.wsSessionId || "",
    webCommand: {
      command,
      payload: payload ?? null,
      requestId,
    },
  };

  return new Promise((resolve, reject) => {
    const timeoutHandle = window.setTimeout(() => {
      delete portholeWebState.socketPendingRequests[requestId];
      reject(new Error(`WebSocket request timed out after ${timeoutMs}ms.`));
    }, timeoutMs);

    portholeWebState.socketPendingRequests[requestId] = {
      resolve,
      reject,
      timeoutHandle,
    };

    try {
      portholeWebState.ws.send(JSON.stringify(frame));
    } catch (error) {
      window.clearTimeout(timeoutHandle);
      delete portholeWebState.socketPendingRequests[requestId];
      reject(error instanceof Error ? error : new Error(String(error)));
    }
  });
}

function resolveSocketRequestMessage(message) {
  const requestId = typeof message.requestId === "string" ? message.requestId : "";
  if (!requestId) {
    return;
  }
  const pending = portholeWebState.socketPendingRequests[requestId];
  if (!pending) {
    return;
  }

  window.clearTimeout(pending.timeoutHandle);
  delete portholeWebState.socketPendingRequests[requestId];

  if (message.kind === "error") {
    pending.reject(new Error(typeof message.message === "string" ? message.message : "WebSocket action failed."));
    return;
  }

  pending.resolve(message.payload);
}

function rejectAllSocketRequests(error) {
  const entries = Object.entries(portholeWebState.socketPendingRequests);
  portholeWebState.socketPendingRequests = {};
  entries.forEach(([, pending]) => {
    if (!pending) {
      return;
    }
    window.clearTimeout(pending.timeoutHandle);
    pending.reject(error);
  });
}

function shouldRefreshFromFlowEvent(flowElement) {
  const topic = typeof flowElement.topic === "string"
    ? flowElement.topic.trim().toLowerCase()
    : "";
  const title = typeof flowElement.title === "string" ? flowElement.title.toLowerCase() : "";
  const content = unwrapValueType(flowElement.content);

  if (topic === "porthole" || topic === "document.change") {
    return true;
  }

  if (topic === "ai.assistant.thread" || title.startsWith("ai.thread.")) {
    return true;
  }

  if (topic === "conference.session.thread" || title.startsWith("conference.session.thread.")) {
    return true;
  }

  if (topic === "assistant.correspondence.admin") {
    return true;
  }

  if (topic === "haven.purpose.coverage") {
    return true;
  }

  if (typeof content === "string" && content.toLowerCase() === "refresh") {
    return true;
  }

  return title.includes("orchestrator update");
}

function scheduleSocketRefresh() {
  const now = Date.now();
  const remainingSuppressMs = Math.max(0, portholeWebState.socketRefreshSuppressUntil - now);
  const delayMs = Math.max(120, remainingSuppressMs);

  if (portholeWebState.socketRefreshTimer) {
    window.clearTimeout(portholeWebState.socketRefreshTimer);
  }

  portholeWebState.socketRefreshTimer = window.setTimeout(() => {
    portholeWebState.socketRefreshTimer = null;
    void refreshBootstrap({ silent: true });
  }, delayMs);
}

async function copyCurrentCellConfiguration(kind) {
  const configuration = buildPortableConfigurationSnapshot(kind);
  if (!configuration) {
    portholeWebState.error = "Fant ingen CellConfiguration å kopiere.";
    render({ forceShell: true, preserveSkeletonDOM: true });
    return;
  }
  await copyJSONPayload(configuration, kind === "working"
    ? "Working CellConfiguration kopiert."
    : "Committed CellConfiguration kopiert.");
}

async function copyCurrentDebugSnapshot() {
  const context = resolveInspectorDocumentContext();
  await copyJSONPayload(context.debugSnapshot, "Debug snapshot kopiert.");
}

async function copySelectedNodeRaw(path) {
  const editorState = portholeWebState.bootstrap && portholeWebState.bootstrap.editorState
    ? portholeWebState.bootstrap.editorState
    : null;
  const root = resolveEditorSkeletonRoot(
    editorState,
    portholeWebState.bootstrap && portholeWebState.bootstrap.configuration
      ? portholeWebState.bootstrap.configuration
      : null
  );
  const selectedNode = resolveSkeletonNodeByPath(root, path);
  if (!selectedNode) {
    portholeWebState.error = "Fant ikke valgt node å kopiere.";
    render({ forceShell: true, preserveSkeletonDOM: true });
    return;
  }
  await copyJSONPayload(selectedNode.raw, "Raw node kopiert.");
}

async function copySelectedReferenceState(label) {
  await copyJSONPayload(resolveReferenceState(label), `Reference-state for ${label} kopiert.`);
}

async function copyJSONPayload(payload, successMessage) {
  const text = JSON.stringify(payload, null, 2);
  try {
    await writeClipboardText(text);
    portholeWebState.notice = successMessage;
    portholeWebState.error = null;
  } catch (error) {
    portholeWebState.error = error instanceof Error ? error.message : "Klarte ikke å kopiere til utklippstavlen.";
  }
  render({ forceShell: true, preserveSkeletonDOM: true });
}

async function writeClipboardText(text) {
  if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
    await navigator.clipboard.writeText(text);
    return;
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "true");
  textarea.style.position = "fixed";
  textarea.style.left = "-9999px";
  textarea.style.top = "0";
  document.body.appendChild(textarea);
  textarea.select();

  const succeeded = document.execCommand("copy");
  document.body.removeChild(textarea);
  if (!succeeded) {
    throw new Error("Browseren støtter ikke kopi til utklippstavle her.");
  }
}

async function decodeSocketPayload(rawData) {
  if (typeof rawData === "string") {
    return parseJSON(rawData);
  }

  if (rawData instanceof Blob) {
    return parseJSON(await rawData.text());
  }

  if (rawData instanceof ArrayBuffer) {
    return parseJSON(new TextDecoder().decode(rawData));
  }

  if (rawData && typeof rawData === "object") {
    return rawData;
  }

  return null;
}

function parseJSON(text) {
  try {
    return JSON.parse(text);
  } catch (_ignore) {
    return null;
  }
}

function unwrapValueType(value) {
  if (value == null || typeof value !== "object") {
    return value;
  }

  const candidates = ["string", "&string", "value", "&value"];
  for (let index = 0; index < candidates.length; index += 1) {
    const key = candidates[index];
    if (Object.prototype.hasOwnProperty.call(value, key)) {
      return value[key];
    }
  }

  return value;
}

async function fetchJSON(url, options = {}) {
  const { timeoutMs = 10000, timeoutMessage = null, ...fetchOptions } = options;
  const controller = typeof AbortController !== "undefined" ? new AbortController() : null;
  const timeoutHandle = controller && timeoutMs > 0
    ? window.setTimeout(() => controller.abort(), timeoutMs)
    : null;

  try {
    const response = await fetch(url, {
      credentials: "same-origin",
      ...fetchOptions,
      headers: {
        Accept: "application/json",
        ...(fetchOptions.headers || {}),
      },
      signal: controller ? controller.signal : fetchOptions.signal,
    });

    if (response.status === 401 || response.redirected) {
      const returnPath = `${window.location.pathname}${window.location.search}`;
      window.location.assign(`/login?next=${encodeURIComponent(returnPath)}`);
      throw new Error("Porthole-sesjonen er utloept. Du sendes til innlogging.");
    }

    if (!response.ok) {
      let message = `HTTP ${response.status}: ${response.statusText}`;
      try {
        const payload = await response.json();
        if (payload && typeof payload.reason === "string") {
          message = payload.reason;
        }
      } catch (_ignore) {
        // Keep fallback.
      }
      throw new Error(message);
    }

    const contentType = String(response.headers.get("content-type") || "").toLowerCase();
    if (!contentType.includes("application/json")) {
      throw new Error("Porthole mottok et ugyldig svar fra serveren. Last siden paa nytt.");
    }

    return response.json();
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error(timeoutMessage || `Request timed out after ${timeoutMs}ms.`);
    }
    throw error;
  } finally {
    if (timeoutHandle) {
      window.clearTimeout(timeoutHandle);
    }
  }
}

function postJSON(url, payload, options = {}) {
  return fetchJSON(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    ...options,
  });
}

function escapeHTML(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll("\"", "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeAttr(value) {
  return escapeHTML(value);
}

function normalizeLineBreaks(input) {
  return String(input).replaceAll("\r\n", "\n").replaceAll("\r", "\n");
}

function renderMarkdownLite(input) {
  const text = normalizeLineBreaks(input);
  const lines = text.split("\n");
  const blocks = [];
  let bulletBuffer = [];

  const flushBullets = () => {
    if (!bulletBuffer.length) {
      return;
    }
    const items = bulletBuffer
      .map((item) => `<li>${renderInlineMarkdown(item)}</li>`)
      .join("");
    blocks.push(`<ul>${items}</ul>`);
    bulletBuffer = [];
  };

  lines.forEach((line) => {
    const trimmed = line.trim();

    if (trimmed.startsWith("- ")) {
      bulletBuffer.push(trimmed.slice(2));
      return;
    }

    flushBullets();

    if (!trimmed) {
      return;
    }

    if (trimmed.startsWith("> ")) {
      blocks.push(`<blockquote>${renderInlineMarkdown(trimmed.slice(2))}</blockquote>`);
      return;
    }

    blocks.push(`<p>${renderInlineMarkdown(trimmed)}</p>`);
  });

  flushBullets();

  if (!blocks.length) {
    return `<pre>${escapeHTML(text)}</pre>`;
  }

  return blocks.join("");
}

function renderInlineMarkdown(input) {
  let html = escapeHTML(input);
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  return html;
}
