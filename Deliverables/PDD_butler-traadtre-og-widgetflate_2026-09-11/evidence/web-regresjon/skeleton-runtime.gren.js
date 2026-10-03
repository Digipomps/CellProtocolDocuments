// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

(function (global) {
  "use strict";

  const SUPPORTED_TYPES = new Set([
    "VStack",
    "HStack",
    "Text",
    "AttachmentField",
    "FileUpload",
    "TextField",
    "TextArea",
    "Button",
    "List",
    "Tree",
    "ComponentSurface",
    "Divider",
    "Object",
    "Section",
    "ScrollView",
    "Spacer",
    "Image",
    "Reference",
    "ZStack",
    "Grid",
    "Toggle",
    "Picker",
    "Tabs",
    "NavigationBar",
    "Visualization",
    "Unsupported",
  ]);

  // --- Skeleton icon rendering (Lucide) ---------------------------------
  //
  // SkeletonButton.icon and SkeletonImage.name (when type === "system") carry
  // SF Symbol names — the convention CellApple's native SwiftUI renderer has
  // used for SkeletonImage since before this file existed (Image(systemName:)).
  // Rather than teach the portable CellProtocol schema a second, web-specific
  // icon vocabulary, the web renderer keeps consuming SF Symbol names and
  // translates a curated subset of them into a small bundled Lucide icon set
  // (MIT licensed, https://lucide.dev) below. Lucide ships one icon family
  // with rounded stroke caps/joins by default — that IS the "Lucide Rounded"
  // style referenced in the HAVEN design system docs, not a separate variant.
  //
  // This is intentionally NOT exhaustive: it covers the icons already in use
  // across HAVEN surfaces plus a handful of common UI glyphs, sized to stay
  // maintainable. An SF Symbol name with no mapping renders a visible
  // "unmapped icon" fallback glyph (circle-question-mark) and logs a console
  // warning once — degrading explicitly instead of silently rendering
  // nothing, so gaps are visible to whoever builds the next surface.
  //
  // To add an icon: fetch the raw SVG from
  // https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/<name>.svg,
  // copy its inner <path>/<circle>/... markup into LUCIDE_ICON_PATHS, then add
  // an entry to SF_SYMBOL_TO_LUCIDE.

  const LUCIDE_ICON_PATHS = {
    "arrow-left": "<path d=\"m12 19-7-7 7-7\" /><path d=\"M19 12H5\" />",
    "arrow-right": "<path d=\"M5 12h14\" /><path d=\"m12 5 7 7-7 7\" />",
    "bell": "<path d=\"M10.268 21a2 2 0 0 0 3.464 0\" /><path d=\"M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326\" />",
    "calendar": "<path d=\"M8 2v3\" /><path d=\"M16 2v3\" /><rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\" /><path d=\"M3 9h18\" />",
    "check": "<path d=\"M20 6 9 17l-5-5\" />",
    "chevron-down": "<path d=\"m6 9 6 6 6-6\" />",
    "chevron-left": "<path d=\"m15 18-6-6 6-6\" />",
    "chevron-right": "<path d=\"m9 18 6-6-6-6\" />",
    "chevron-up": "<path d=\"m18 15-6-6-6 6\" />",
    "circle-question-mark": "<circle cx=\"12\" cy=\"12\" r=\"10\" /><path d=\"M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3\" /><path d=\"M12 17h.01\" />",
    "circle-user": "<circle cx=\"12\" cy=\"12\" r=\"10\" /><circle cx=\"12\" cy=\"10\" r=\"3\" /><path d=\"M7 20.662V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.662\" />",
    "clock": "<circle cx=\"12\" cy=\"12\" r=\"10\" /><path d=\"M12 6v6l4 2\" />",
    "download": "<path d=\"M12 15V3\" /><path d=\"M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4\" /><path d=\"m7 10 5 5 5-5\" />",
    "heart": "<path d=\"M2 9.5a5.5 5.5 0 0 1 9.591-3.676.56.56 0 0 0 .818 0A5.49 5.49 0 0 1 22 9.5c0 2.29-1.5 4-3 5.5l-5.492 5.313a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5\" />",
    "house": "<path d=\"M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8\" /><path d=\"M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z\" />",
    "image": "<rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\" ry=\"2\" /><circle cx=\"9\" cy=\"9\" r=\"2\" /><path d=\"m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21\" />",
    "info": "<circle cx=\"12\" cy=\"12\" r=\"10\" /><path d=\"M12 16v-4\" /><path d=\"M12 8h.01\" />",
    "mail": "<path d=\"m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7\" /><rect x=\"2\" y=\"4\" width=\"20\" height=\"16\" rx=\"2\" />",
    "map-pin": "<path d=\"M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0\" /><circle cx=\"12\" cy=\"10\" r=\"3\" />",
    "menu": "<path d=\"M4 5h16\" /><path d=\"M4 12h16\" /><path d=\"M4 19h16\" />",
    "message-circle": "<path d=\"M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719\" />",
    "pencil": "<path d=\"M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z\" /><path d=\"m15 5 4 4\" />",
    "phone": "<path d=\"M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384\" />",
    "plus": "<path d=\"M5 12h14\" /><path d=\"M12 5v14\" />",
    "search": "<path d=\"m21 21-4.34-4.34\" /><circle cx=\"11\" cy=\"11\" r=\"8\" />",
    "settings": "<path d=\"M9.671 4.136a2.34 2.34 0 0 1 4.659 0 2.34 2.34 0 0 0 3.319 1.915 2.34 2.34 0 0 1 2.33 4.033 2.34 2.34 0 0 0 0 3.831 2.34 2.34 0 0 1-2.33 4.033 2.34 2.34 0 0 0-3.319 1.915 2.34 2.34 0 0 1-4.659 0 2.34 2.34 0 0 0-3.32-1.915 2.34 2.34 0 0 1-2.33-4.033 2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915\" /><circle cx=\"12\" cy=\"12\" r=\"3\" />",
    "star": "<path d=\"M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z\" />",
    "trash-2": "<path d=\"M10 11v6\" /><path d=\"M14 11v6\" /><path d=\"M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6\" /><path d=\"M3 6h18\" /><path d=\"M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2\" />",
    "triangle-alert": "<path d=\"m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3\" /><path d=\"M12 9v4\" /><path d=\"M12 17h.01\" />",
    "upload": "<path d=\"M12 3v12\" /><path d=\"m17 8-5-5-5 5\" /><path d=\"M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4\" />",
    "user": "<path d=\"M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2\" /><circle cx=\"12\" cy=\"7\" r=\"4\" />",
    "x": "<path d=\"M18 6 6 18\" /><path d=\"m6 6 12 12\" />",
  };

  // SF Symbol name -> bundled Lucide icon name. Several SF Symbols (".fill",
  // ".circle" variants) intentionally collapse onto the same Lucide glyph —
  // Lucide's single-weight outline style doesn't distinguish filled/outline
  // the way SF Symbols does, so this is a deliberate many-to-one mapping,
  // not a gap.
  const SF_SYMBOL_TO_LUCIDE = {
    "person": "user",
    "person.fill": "user",
    "person.circle": "circle-user",
    "person.circle.fill": "circle-user",
    "calendar": "calendar",
    "message": "message-circle",
    "message.fill": "message-circle",
    "bubble.left": "message-circle",
    "bubble.left.fill": "message-circle",
    "house": "house",
    "house.fill": "house",
    "chevron.left": "chevron-left",
    "chevron.right": "chevron-right",
    "chevron.down": "chevron-down",
    "chevron.up": "chevron-up",
    "xmark": "x",
    "xmark.circle": "x",
    "xmark.circle.fill": "x",
    "checkmark": "check",
    "checkmark.circle": "check",
    "checkmark.circle.fill": "check",
    "magnifyingglass": "search",
    "gearshape": "settings",
    "gearshape.fill": "settings",
    "gear": "settings",
    "star": "star",
    "star.fill": "star",
    "heart": "heart",
    "heart.fill": "heart",
    "plus": "plus",
    "plus.circle": "plus",
    "plus.circle.fill": "plus",
    "arrow.left": "arrow-left",
    "arrow.right": "arrow-right",
    "line.horizontal.3": "menu",
    "bell": "bell",
    "bell.fill": "bell",
    "envelope": "mail",
    "envelope.fill": "mail",
    "phone": "phone",
    "phone.fill": "phone",
    "mappin": "map-pin",
    "mappin.circle": "map-pin",
    "mappin.circle.fill": "map-pin",
    "clock": "clock",
    "clock.fill": "clock",
    "square.and.arrow.up": "upload",
    "square.and.arrow.down": "download",
    "trash": "trash-2",
    "trash.fill": "trash-2",
    "pencil": "pencil",
    "info.circle": "info",
    "info.circle.fill": "info",
    "exclamationmark.triangle": "triangle-alert",
    "exclamationmark.triangle.fill": "triangle-alert",
    "photo": "image",
  };

  const UNMAPPED_ICON_FALLBACK = "circle-question-mark";

  // Backstop for the optimistic tab highlight. It is not a guess about how long
  // the round trip takes — `selectTab` releases the highlight the moment the
  // action settles — only a ceiling so an action that never settles cannot pin
  // the strip on a tab the server never accepted. Matched to the cell-action
  // budget in porthole-webo.js rather than picked independently.
  const TAB_SELECTION_HOLD_CEILING_MS = 45000;
  const warnedUnmappedIcons = new Set();

  function resolveLucideIconName(sfSymbolName) {
    if (typeof sfSymbolName !== "string" || !sfSymbolName.trim()) {
      return null;
    }
    const trimmed = sfSymbolName.trim();
    const mapped = SF_SYMBOL_TO_LUCIDE[trimmed];
    if (mapped && LUCIDE_ICON_PATHS[mapped]) {
      return mapped;
    }
    if (!warnedUnmappedIcons.has(trimmed)) {
      warnedUnmappedIcons.add(trimmed);
      console.warn(
        `Skeleton icon "${trimmed}" has no web (Lucide) mapping yet; rendering fallback glyph. ` +
        "Add it to SF_SYMBOL_TO_LUCIDE in skeleton-runtime.js."
      );
    }
    return UNMAPPED_ICON_FALLBACK;
  }

  function createSkeletonIconElement(sfSymbolName, options) {
    const iconName = resolveLucideIconName(sfSymbolName);
    if (!iconName) {
      return null;
    }
    const markup = LUCIDE_ICON_PATHS[iconName];
    if (!markup) {
      return null;
    }
    const opts = options || {};
    const size = Number.isFinite(opts.size) ? opts.size : 18;
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("width", String(size));
    svg.setAttribute("height", String(size));
    svg.setAttribute("fill", "none");
    svg.setAttribute("stroke", "currentColor");
    svg.setAttribute("stroke-width", "2");
    svg.setAttribute("stroke-linecap", "round");
    svg.setAttribute("stroke-linejoin", "round");
    svg.setAttribute("aria-hidden", "true");
    svg.dataset.skeletonIcon = sfSymbolName;
    svg.dataset.skeletonIconResolved = iconName;
    if (opts.className) {
      svg.setAttribute("class", opts.className);
    }
    // Trusted, bundled markup only (keyed off our own LUCIDE_ICON_PATHS
    // table) — never derived from skeleton JSON content, so this is not an
    // injection vector.
    svg.innerHTML = markup;
    return svg;
  }

  const LEAFLET_SCRIPT_PATH = "/vendor/leaflet/leaflet.js";
  const LEAFLET_STYLESHEET_PATH = "/vendor/leaflet/leaflet.css";
  let leafletRuntimePromise = null;
  const tabSelectionMemory = new Map();
  let skeletonPresentationScrollLockCount = 0;

  function createRenderer(options) {
    if (!options || !(options.rootElement instanceof HTMLElement)) {
      throw new Error("SkeletonRuntime requires rootElement.");
    }

    const validation = validateSkeleton(options.skeleton);
    if (!validation.valid) {
      if (!options.rootElement.hasChildNodes()) {
        const diagnostic = document.createElement("p");
        diagnostic.className = "skeleton-runtime-error";
        diagnostic.setAttribute("role", "alert");
        diagnostic.textContent = validation.error;
        options.rootElement.replaceChildren(diagnostic);
      }
      const error = new Error(validation.error);
      error.name = "SkeletonValidationError";
      throw error;
    }

    const targetRootElement = options.rootElement;
    const deferMount = options.deferMount === true;
    const renderRootElement = deferMount ? document.createElement("div") : targetRootElement;
    if (deferMount && targetRootElement.id) {
      renderRootElement.id = targetRootElement.id;
    }

    const state = {
      fontFallback: getComputedStyle(targetRootElement).fontFamily || "system-ui, sans-serif",
      rootElement: renderRootElement,
      onAction: typeof options.onAction === "function" ? options.onAction : async () => {},
      onNavigate: typeof options.onNavigate === "function" ? options.onNavigate : null,
      navigationBaseURL:
        typeof options.navigationBaseURL === "string" && options.navigationBaseURL.trim()
          ? options.navigationBaseURL.trim()
          : global.location?.href,
      currentConfigurationName:
        typeof options.currentConfigurationName === "string" && options.currentConfigurationName.trim()
          ? options.currentConfigurationName.trim()
          : null,
      onFieldInput: typeof options.onFieldInput === "function" ? options.onFieldInput : null,
      resolveButtonPayload:
        typeof options.resolveButtonPayload === "function" ? options.resolveButtonPayload : null,
      formatText: typeof options.formatText === "function" ? options.formatText : null,
      rootData: {},
      rendererOptions: options,
      layoutContext: options.layoutContext || {},
      treeBindings: [],
      componentBindings: new Map(),
      dragContext: options.dragContext || { transfer: null, source: null, listeners: new Set() },
      localization: global.HavenLocalization?.createRuntime({
        configuration: options.localization || null,
        catalogs: options.localizationCatalogs || [],
        context: options.localizationContext || { ui_locale: "nb-NO" },
      }) || null,
      localizationBindings: [],
      localizationContextSignature: JSON.stringify(options.localizationContext || { ui_locale: "nb-NO" }),
      textBindings: [],
      listBindings: [],
      gridBindings: [],
      referenceBindings: [],
      fieldBindings: [],
      localFieldValues: new Map(),
      attachmentBindings: [],
      toggleBindings: [],
      pickerBindings: [],
      tabBindings: [],
      navigationBarBindings: [],
      buttonBindings: [],
      visualizationBindings: [],
      visibilityBindings: [],
      presentationBindings: [],
      presentationSequence: 0,
      presentationKeydownHandler: null,
      presentationKeydownHandlerInstalled: false,
      activePresentationBindings: [],
      presentationScrollLocked: false,
      isMounted: !deferMount,
    };

    const rootSkeleton = extractRootSkeleton(options.skeleton);
    const rootNode = renderElement(rootSkeleton, state, options.itemContext || null, "root", "root");

    state.rootElement.replaceChildren(rootNode);
    state.refreshDragStyles = () => refreshDragStyles(state);
    state.dragContext.listeners.add(state.refreshDragStyles);
    state.beginExternalDrag = (event) => {
      if (!state.rootElement.contains(event.target)) return;
      setHostDrag(state, parseDragTransfer(event) || { dragRole: "", dragPayload: null }, event.target);
    };
    state.cancelDrag = (event) => {
      if (event.type !== "keydown" || event.key === "Escape") setHostDrag(state, null, null);
    };
    // One transient drag context per host, shared by mounted definitions.
    if (!options.dragContext) {
      document.addEventListener("dragstart", state.beginExternalDrag);
      document.addEventListener("dragend", state.cancelDrag);
      document.addEventListener("drop", state.cancelDrag);
      document.addEventListener("keydown", state.cancelDrag);
    }
    updateLayoutContext(state);
    state.presentationKeydownHandler = (event) => handlePresentationKeydown(state, event);
    if (state.isMounted) {
      document.addEventListener("keydown", state.presentationKeydownHandler, true);
      state.presentationKeydownHandlerInstalled = true;
      updatePresentationBindings(state);
    }

    return {
      update(nextData) {
        state.rootData = nextData && typeof nextData === "object" ? nextData : {};
        state.localization?.setRootData(state.rootData);
        flushDynamicBindings(state);
        updateLocalizationBindings(state);
      },
      setLayoutContext(context) {
        state.layoutContext = context || {};
        updateLayoutContext(state);
      },
      captureState() {
        return captureRendererState(state);
      },
      restoreState(snapshot) {
        restoreRendererState(state, snapshot);
      },
      setLocalization(context, configuration, catalogs = []) {
        if (!state.localization) return false;
        const signature = JSON.stringify(context);
        if (configuration === undefined && signature === state.localizationContextSignature) return true;
        if (configuration !== undefined) {
          const candidate = global.HavenLocalization.createRuntime({ configuration, catalogs, context });
          candidate.setRootData(state.rootData);
          state.localization.clear();
          state.localization = candidate;
        } else {
          state.localization.setContext(context);
        }
        state.localizationContextSignature = signature;
        updateTextBindings(state);
        updateLocalizationBindings(state);
        return true;
      },
      localizationDiagnostics() { return state.localization?.getDiagnostics() || []; },
      localizationMetrics() { return state.localization?.getMetrics() || {}; },
      mount(nextRootElement = targetRootElement) {
        if (!(nextRootElement instanceof HTMLElement)) {
          throw new Error("SkeletonRuntime mount requires an HTMLElement.");
        }
        if (state.rootElement !== nextRootElement) {
          nextRootElement.replaceChildren(...Array.from(state.rootElement.childNodes));
          state.rootElement = nextRootElement;
        }
        state.isMounted = true;
        if (state.presentationKeydownHandler && !state.presentationKeydownHandlerInstalled) {
          document.addEventListener("keydown", state.presentationKeydownHandler, true);
          state.presentationKeydownHandlerInstalled = true;
        }
        updateVisibilityBindings(state);
        updatePresentationBindings(state);
      },
      destroy({ preserveDOM = false } = {}) {
        state.componentBindings.forEach((binding) => binding.renderer?.destroy());
        state.componentBindings.clear();
        state.dragContext.listeners.delete(state.refreshDragStyles);
        if (!options.dragContext) {
          setHostDrag(state, null, null);
          document.removeEventListener("dragstart", state.beginExternalDrag);
          document.removeEventListener("dragend", state.cancelDrag);
          document.removeEventListener("drop", state.cancelDrag);
          document.removeEventListener("keydown", state.cancelDrag);
        }
        state.localization?.clear();
        state.localizationBindings = [];
        if (state.presentationKeydownHandler && state.presentationKeydownHandlerInstalled) {
          document.removeEventListener("keydown", state.presentationKeydownHandler, true);
          state.presentationKeydownHandlerInstalled = false;
        }
        state.presentationKeydownHandler = null;
        cleanupPresentationBindings(state);
        cleanupVisualizationBindings(state.visualizationBindings);
        state.visualizationBindings = [];
        if (!preserveDOM) {
          state.rootElement.replaceChildren();
        }
      },
      getFieldValueByTarget(targetKeypath) {
        const binding = state.fieldBindings.find((entry) => entry.targetKeypath === targetKeypath);
        return binding ? readFieldBindingValue(binding) : "";
      },
      getFieldValueBySource(sourceKeypath) {
        const binding = state.fieldBindings.find((entry) => entry.sourceKeypath === sourceKeypath);
        return binding ? readFieldBindingValue(binding) : "";
      },
      setFieldValueByTarget(targetKeypath, value, preserveCaret) {
        const binding = state.fieldBindings.find((entry) => entry.targetKeypath === targetKeypath);
        if (!binding) {
          return;
        }
        const nextValue = String(value ?? "");
        rememberLocalFieldValue(state, binding, nextValue);
        writeFieldBindingValue(binding, nextValue, Boolean(preserveCaret));
      },
      insertTokenByTarget(targetKeypath, token, fallbackText) {
        const binding = state.fieldBindings.find((entry) => entry.targetKeypath === targetKeypath);
        if (!binding) {
          return;
        }
        insertTokenIntoBinding(binding, String(token ?? ""), String(fallbackText ?? ""));
      },
      focusFieldByTarget(targetKeypath) {
        const binding = state.fieldBindings.find((entry) => entry.targetKeypath === targetKeypath);
        if (binding) {
          focusFieldBinding(binding);
        }
      },
    };
  }

  function cleanupVisualizationBindings(bindings) {
    (bindings || []).forEach((binding) => {
      disposeVisualizationBinding(binding);
    });
  }

  function disposeVisualizationBinding(binding) {
    if (binding) {
      binding.mapRenderToken = (binding.mapRenderToken || 0) + 1;
    }
    if (binding && binding.documentController) {
      binding.documentController.destroy();
      binding.documentController = null;
    }
    if (!binding || !binding.mapController) {
      return;
    }
    try {
      binding.mapController.destroy();
    } catch (_) {
      // Best effort cleanup.
    }
    binding.mapController = null;
  }

  function extractRootSkeleton(raw) {
    return decodeElement(extractSkeletonCandidate(raw));
  }

  function decodeElement(raw) {
    const keys = Object.keys(raw);
    const elementKey = keys[0];
    return { type: elementKey, value: raw[elementKey] };
  }

  function validateSkeleton(raw) {
    const candidate = extractSkeletonCandidate(raw);
    const error = validateElement(candidate, 0, "root") || global.HavenLocalization?.validateSkeleton(candidate)[0];
    return error ? { valid: false, error } : { valid: true, error: null };
  }

  function extractSkeletonCandidate(raw) {
    if (isPlainObject(raw) && isPlainObject(raw.skeleton)) {
      return raw.skeleton;
    }
    return raw;
  }

  function validateElement(raw, depth, path) {
    if (depth >= 256) {
      return `Invalid skeleton at ${path}: maximum nesting depth exceeded.`;
    }
    if (!isPlainObject(raw)) {
      return `Invalid skeleton at ${path}: expected a single-key element object.`;
    }

    const keys = Object.keys(raw);
    if (keys.length !== 1 || !SUPPORTED_TYPES.has(keys[0])) {
      return `Invalid skeleton at ${path}: expected exactly one supported element key.`;
    }

    const type = keys[0];
    const payload = raw[type];
    return validateElementPayload(type, payload, depth + 1, `${path}.${type}`);
  }

  function validateElementPayload(type, payload, depth, path) {
    if (payload?.modifiers?.localization != null && global.HavenLocalization) {
      const error = global.HavenLocalization.validateSlots(type, payload.modifiers.localization);
      if (error) return `Invalid skeleton at ${path}.modifiers.localization: ${error}`;
    }
    if (depth >= 256) {
      return `Invalid skeleton at ${path}: maximum nesting depth exceeded.`;
    }

    if (type === "VStack" || type === "HStack") {
      if (Array.isArray(payload)) {
        return validateElementArray(payload, depth + 1, path);
      }
      if (!isPlainObject(payload)) {
        return `Invalid skeleton at ${path}: expected an array or stack object.`;
      }
      if (Object.prototype.hasOwnProperty.call(payload, "elements") && !Array.isArray(payload.elements)) {
        return `Invalid skeleton at ${path}.elements: expected an array.`;
      }
      return validateElementArray(payload.elements || [], depth + 1, `${path}.elements`);
    }

    if (type === "ZStack") {
      if (!isPlainObject(payload)) {
        return `Invalid skeleton at ${path}: expected a stack object.`;
      }
      if (!Array.isArray(payload.elements)) {
        return `Invalid skeleton at ${path}.elements: expected an array.`;
      }
      return validateElementArray(payload.elements, depth + 1, `${path}.elements`);
    }

    if (!isPlainObject(payload)) {
      return `Invalid skeleton at ${path}: expected an object payload.`;
    }

    if (type === "Tree") {
      const error = validateRequiredStrings(payload, ["keypath", "idKeypath", "parentIDKeypath",
        "levelKeypath", "leadingInsetKeypath", "hasChildrenKeypath", "expandedKeypath",
        "selectedIDStateKeypath", "selectionActionKeypath", "expansionActionKeypath"], path);
      if (error) return error;
      if (!isPlainObject(payload.rowSkeleton) || !payload.rowSkeleton.VStack) {
        return `Invalid skeleton at ${path}.rowSkeleton: expected a wrapped VStack.`;
      }
      return validateElement(payload.rowSkeleton, depth + 1, `${path}.rowSkeleton`);
    }
    if (type === "ComponentSurface") {
      // WP-F format: nøyaktig én av instanceID og instanceIDKeypath.
      const hasID = typeof payload.instanceID === "string" && payload.instanceID.trim() !== "";
      const hasKeypath = typeof payload.instanceIDKeypath === "string" && payload.instanceIDKeypath.trim() !== "";
      if (hasID === hasKeypath) {
        return `Invalid skeleton at ${path}: expected exactly one of instanceID and instanceIDKeypath.`;
      }
      return validateRequiredStrings(payload, ["sourceKeypath"], path)
        || (!["inline", "pinned"].includes(payload.variant)
          ? `Invalid skeleton at ${path}.variant: expected inline or pinned.` : null);
    }

    if (type === "ScrollView") {
      if (!Array.isArray(payload.elements)) {
        return `Invalid skeleton at ${path}.elements: expected an array.`;
      }
      return validateElementArray(payload.elements, depth + 1, `${path}.elements`);
    }

    if (type === "Section") {
      if (!Array.isArray(payload.content)) {
        return `Invalid skeleton at ${path}.content: expected an array.`;
      }
      const contentError = validateElementArray(payload.content, depth + 1, `${path}.content`);
      if (contentError) return contentError;
      for (const key of ["header", "footer"]) {
        if (payload[key] != null) {
          const error = validateElement(payload[key], depth + 1, `${path}.${key}`);
          if (error) return error;
        }
      }
      return null;
    }

    if (type === "Tabs") {
      if (!Array.isArray(payload.panels)) {
        return `Invalid skeleton at ${path}.panels: expected an array.`;
      }
      for (let index = 0; index < payload.panels.length; index += 1) {
        const panel = payload.panels[index];
        if (!isPlainObject(panel) || typeof panel.id !== "string" || !Array.isArray(panel.content)) {
          return `Invalid skeleton at ${path}.panels[${index}]: expected an id and content array.`;
        }
        const error = validateElementArray(panel.content, depth + 1, `${path}.panels[${index}].content`);
        if (error) return error;
      }
      return validateRequiredString(payload, "activeTabStateKeypath", path);
    }

    if (type === "NavigationBar") {
      const stateError = validateOptionalStrings(payload, ["activeStateKeypath"], path);
      if (stateError) return stateError;
      if (!Array.isArray(payload.items)) {
        return `Invalid skeleton at ${path}.items: expected an array.`;
      }
      for (let index = 0; index < payload.items.length; index += 1) {
        const item = payload.items[index];
        if (!isPlainObject(item)) {
          return `Invalid skeleton at ${path}.items[${index}]: expected an object.`;
        }
        const requiredError = validateRequiredStrings(item, ["keypath", "label"], `${path}.items[${index}]`);
        if (requiredError) return requiredError;
        const optionalError = validateOptionalStrings(
          item,
          ["url", "keypathKeypath", "labelKeypath", "payloadKeypath", "activeValue", "activeConfigurationName"],
          `${path}.items[${index}]`
        );
        if (optionalError) return optionalError;
      }
      return null;
    }

    if (type === "Grid") {
      if (!Array.isArray(payload.columns)) {
        return `Invalid skeleton at ${path}.columns: expected an array.`;
      }
      for (let index = 0; index < payload.columns.length; index += 1) {
        const column = payload.columns[index];
        if (!isPlainObject(column) || !["fixed", "flexible", "adaptive"].includes(column.type)) {
          return `Invalid skeleton at ${path}.columns[${index}]: expected a supported column type.`;
        }
        for (const key of ["value", "min", "max"]) {
          if (column[key] != null && !Number.isFinite(column[key])) {
            return `Invalid skeleton at ${path}.columns[${index}].${key}: expected a number.`;
          }
        }
      }
      if (payload.elements != null && !Array.isArray(payload.elements)) {
        return `Invalid skeleton at ${path}.elements: expected an array.`;
      }
      const elementsError = validateElementArray(payload.elements || [], depth + 1, `${path}.elements`);
      if (elementsError) return elementsError;
      return payload.itemSkeleton == null
        ? null
        : validateElement(payload.itemSkeleton, depth + 1, `${path}.itemSkeleton`);
    }

    if (type === "Object") {
      if (!isPlainObject(payload.elements)) {
        return `Invalid skeleton at ${path}.elements: expected an object.`;
      }
      for (const [key, element] of Object.entries(payload.elements)) {
        const error = validateElement(element, depth + 1, `${path}.elements.${key}`);
        if (error) return error;
      }
      return null;
    }

    if (type === "List" || type === "Reference") {
      if (payload.flowElementSkeleton != null) {
        if (!isPlainObject(payload.flowElementSkeleton) || Object.keys(payload.flowElementSkeleton)[0] !== "VStack") {
          return `Invalid skeleton at ${path}.flowElementSkeleton: expected a VStack element.`;
        }
        const error = validateElement(payload.flowElementSkeleton, depth + 1, `${path}.flowElementSkeleton`);
        if (error) return error;
      }
      if (type === "Reference") {
        return validateRequiredStrings(payload, ["keypath", "topic"], path);
      }
      return null;
    }

    if (type === "Text") {
      return validateOptionalStrings(payload, ["text", "keypath", "url"], path);
    }
    if (type === "Button") {
      return validateRequiredStrings(payload, ["label", "keypath"], path)
        || validateOptionalStrings(payload, ["url", "keypathKeypath", "labelKeypath", "payloadKeypath"], path);
    }
    if (type === "TextField") {
      return validateOptionalStrings(payload, ["text", "sourceKeypath", "targetKeypath", "placeholder"], path);
    }
    if (type === "TextArea") {
      const stringError = validateOptionalStrings(
        payload,
        ["text", "sourceKeypath", "targetKeypath", "placeholder", "submitActionKeypath", "editorMode"],
        path
      );
      if (stringError) return stringError;
      for (const key of ["minLines", "maxLines"]) {
        if (payload[key] != null && !Number.isInteger(payload[key])) {
          return `Invalid skeleton at ${path}.${key}: expected an integer.`;
        }
      }
      if (payload.submitOnEnter != null && typeof payload.submitOnEnter !== "boolean") {
        return `Invalid skeleton at ${path}.submitOnEnter: expected a boolean.`;
      }
      return null;
    }
    if (type === "Toggle") {
      const stringError = validateRequiredStrings(payload, ["label", "keypath"], path);
      if (stringError) return stringError;
      return typeof payload.isOn === "boolean"
        ? null
        : `Invalid skeleton at ${path}.isOn: expected a boolean.`;
    }
    if (type === "Picker") {
      const stringError = validateOptionalStrings(
        payload,
        ["label", "placeholder", "keypath", "optionLabelKeypath", "selectionValueKeypath", "selectionStateKeypath", "selectionActionKeypath", "selectionPayloadMode"],
        path
      );
      if (stringError) return stringError;
      if (payload.elements != null && !Array.isArray(payload.elements)) {
        return `Invalid skeleton at ${path}.elements: expected an array.`;
      }
      if (payload.allowsEmptySelection != null && typeof payload.allowsEmptySelection !== "boolean") {
        return `Invalid skeleton at ${path}.allowsEmptySelection: expected a boolean.`;
      }
      return null;
    }
    if (type === "Visualization") {
      return validateRequiredString(payload, "kind", path)
        || validateOptionalStrings(payload, ["keypath", "stateKeypath", "actionKeypath"], path);
    }
    return null;
  }

  function validateElementArray(elements, depth, path) {
    for (let index = 0; index < elements.length; index += 1) {
      const error = validateElement(elements[index], depth + 1, `${path}[${index}]`);
      if (error) return error;
    }
    return null;
  }

  function validateRequiredString(payload, key, path) {
    return typeof payload[key] === "string"
      ? null
      : `Invalid skeleton at ${path}.${key}: expected a string.`;
  }

  function validateRequiredStrings(payload, keys, path) {
    for (const key of keys) {
      const error = validateRequiredString(payload, key, path);
      if (error) return error;
    }
    return null;
  }

  function validateOptionalStrings(payload, keys, path) {
    for (const key of keys) {
      if (payload[key] != null && typeof payload[key] !== "string") {
        return `Invalid skeleton at ${path}.${key}: expected a string.`;
      }
    }
    return null;
  }

  function isPlainObject(value) {
    return Boolean(value && typeof value === "object" && !Array.isArray(value));
  }

  function decodeChildren(raw) {
    if (!Array.isArray(raw)) {
      return [];
    }
    return raw.map((entry) => decodeElement(entry));
  }

  function decodeStackSpec(raw) {
    if (Array.isArray(raw)) {
      return {
        children: raw,
        spacing: null,
        modifiers: null,
      };
    }

    if (raw && typeof raw === "object") {
      return {
        children: Array.isArray(raw.elements) ? raw.elements : [],
        spacing: Number.isFinite(raw.spacing) ? raw.spacing : null,
        modifiers: raw.modifiers && typeof raw.modifiers === "object" ? raw.modifiers : null,
      };
    }

    return {
      children: [],
      spacing: null,
      modifiers: null,
    };
  }

  function renderElement(element, state, context, key, path) {
    const node = renderElementNode(element, state, context, key, path);
    const spec = Array.isArray(element.value) ? {} : (element.value || {});
    node.skeletonLayout = { type: element.type, spec, state, context, base: null };
    return node;
  }

  function renderElementNode(element, state, context, key, path) {
    switch (element.type) {
      case "VStack":
        return renderStack(element.value, state, context, key, path, "vstack");
      case "HStack":
        return renderStack(element.value, state, context, key, path, "hstack");
      case "Text":
        return renderText(element.value, state, context, key, path);
      case "AttachmentField":
        return renderFileUpload(element.value, state, context, key, path, element.type);
      case "FileUpload":
        return renderFileUpload(element.value, state, context, key, path, element.type);
      case "TextField":
        return renderTextField(element.value, state, context, key, path);
      case "TextArea":
        return renderTextArea(element.value, state, context, key, path);
      case "Button":
        return renderButton(element.value, state, context, key, path);
      case "Tree":
        return renderTree(element.value, state, context, key, path);
      case "ComponentSurface":
        return renderComponentSurface(element.value, state, context, key, path);
      case "List":
        return renderList(element.value, state, context, key, path);
      case "Divider":
        return renderDivider(element.value, state, context, path);
      case "Section":
        return renderSection(element.value, state, context, key, path);
      case "ScrollView":
        return renderScrollView(element.value, state, context, key, path);
      case "Spacer":
        return renderSpacer(element.value, state, context, path);
      case "Image":
        return renderImage(element.value, state, context, key, path);
      case "Reference":
        return renderReference(element.value, state, context, key, path);
      case "ZStack":
        return renderZStack(element.value, state, context, key, path);
      case "Grid":
        return renderGrid(element.value, state, context, key, path);
      case "Toggle":
        return renderToggle(element.value, state, context, key, path);
      case "Picker":
        return renderPicker(element.value, state, context, key, path);
      case "Tabs":
        return renderTabs(element.value, state, context, key, path);
      case "NavigationBar":
        return renderNavigationBar(element.value, state, context, key, path);
      case "Visualization":
        return renderVisualization(element.value, state, context, key, path);
      case "Object":
        return renderObject(element.value, state, context, key, path);
      case "Unsupported":
        return renderUnsupported(element.value, state, context, key, path);
      default:
        return renderUnsupported(
          { elementType: element.type, reason: "No CellScaffold renderer is registered." },
          state,
          context,
          key,
          path
        );
    }
  }

  function applySkeletonIdentity(node, key, path) {
    node.dataset.skeletonKey = key;
    if (typeof path === "string" && path.length > 0) {
      node.dataset.skeletonPath = path;
    }
  }

  // WP-R2: Tree consumes the cell's ordered visible list; it never traverses or
  // filters data. Navigation changes focus only, selection/expansion await data.
  function replaceItemContext(context, item) {
    Object.keys(context).forEach((key) => delete context[key]);
    if (item && typeof item === "object") {
      Object.entries(item).forEach(([key, value]) => Object.defineProperty(context, key, { value, configurable: true, enumerable: true, writable: true }));
    }
  }

  function renderTree(spec, state, context, key, path) {
    const container = document.createElement("div");
    container.className = "skeleton-tree";
    container.setAttribute("role", "tree");
    applySkeletonIdentity(container, key, path);
    applyElementModifiers(container, spec.modifiers, state, path, context);
    const binding = { container, spec, context, key, path, rows: new Map(), items: [], focusedID: null };
    state.treeBindings.push(binding);
    return container;
  }

  function treeFocus(binding, id, moveDOMFocus = true) {
    if (!binding.rows.has(id)) return;
    binding.focusedID = id;
    binding.rows.forEach((entry, rowID) => { entry.row.tabIndex = rowID === id ? 0 : -1; });
    if (moveDOMFocus) {
      const row = binding.rows.get(id).row;
      row.focus({ preventScroll: true });
      row.scrollIntoView({ block: "nearest", inline: "nearest" });
    }
  }

  function treeAction(binding, state, id, expanded) {
    const payload = expanded === undefined ? { nodeID: id } : { nodeID: id, expanded };
    const keypath = expanded === undefined ? binding.spec.selectionActionKeypath : binding.spec.expansionActionKeypath;
    return dispatchAction(state, keypath, payload, { trigger: expanded === undefined ? "tree-selection" : "tree-expansion" })
      .catch((error) => { console.warn("Skeleton tree action failed", error); });
  }

  function makeTreeRow(binding, state, id) {
    const { spec } = binding;
    const row = document.createElement("div");
    row.className = "skeleton-tree-row";
    row.dataset.nodeId = id;
    row.setAttribute("role", "treeitem");
    row.tabIndex = -1;
    const context = {};
    const item = binding.items.find((value) => getByPath(value, spec.idKeypath) === id);
    replaceItemContext(context, item);
    applyElementModifiers(row, spec.rowModifiers, state, null, context);
    const disclosure = document.createElement("button");
    disclosure.type = "button";
    disclosure.className = "skeleton-tree-disclosure";
    disclosure.tabIndex = -1;
    // The row owns the accessible label/expanded state and the single tab stop.
    disclosure.setAttribute("aria-hidden", "true");
    applyElementModifiers(disclosure, spec.disclosureModifiers, state, null, context);
    disclosure.addEventListener("mousedown", (event) => event.preventDefault());
    disclosure.addEventListener("click", (event) => {
      event.stopPropagation();
      treeFocus(binding, id);
      void treeAction(binding, state, id, getByPath(context, spec.expandedKeypath) !== true);
    });
    row.appendChild(disclosure);
    const content = renderElement(decodeElement(spec.rowSkeleton), state, context, `${binding.key}.node.${id}`, null);
    row.appendChild(content);
    content.querySelectorAll("button, a, input, textarea, select, [tabindex]").forEach((node) => { node.tabIndex = -1; });
    row.addEventListener("focus", () => treeFocus(binding, id, false));
    row.addEventListener("click", (event) => {
      if (isInteractiveTarget(event.target)) return;
      treeFocus(binding, id);
      void treeAction(binding, state, id);
    });
    row.addEventListener("keydown", (event) => {
      if (event.target !== row || event.altKey || event.metaKey || event.ctrlKey) return;
      const ids = binding.items.map((item) => getByPath(item, spec.idKeypath));
      const index = ids.indexOf(id);
      let nextID;
      switch (event.key) {
        case "ArrowDown": nextID = ids[Math.min(index + 1, ids.length - 1)]; break;
        case "ArrowUp": nextID = ids[Math.max(index - 1, 0)]; break;
        case "Home": nextID = ids[0]; break;
        case "End": nextID = ids[ids.length - 1]; break;
        case "ArrowRight":
          if (getByPath(context, spec.hasChildrenKeypath) === true) {
            if (getByPath(context, spec.expandedKeypath) !== true) void treeAction(binding, state, id, true);
            else nextID = ids.find((childID) => getByPath(binding.rows.get(childID)?.context, spec.parentIDKeypath) === id);
          }
          break;
        case "ArrowLeft":
          if (getByPath(context, spec.hasChildrenKeypath) === true && getByPath(context, spec.expandedKeypath) === true) {
            void treeAction(binding, state, id, false);
          } else nextID = getByPath(context, spec.parentIDKeypath);
          break;
        case "Enter": case " ": void treeAction(binding, state, id); break;
        default: return; // In particular, Tab enters once and leaves normally.
      }
      event.preventDefault();
      if (nextID != null) treeFocus(binding, nextID);
    });
    return { row, disclosure, context };
  }

  function updateTreeBindings(state) {
    state.treeBindings.forEach((binding) => {
      const { spec, container } = binding;
      const resolved = resolveKeypath(spec.keypath, state.rootData, binding.context);
      const items = Array.isArray(resolved) ? resolved : [];
      const ids = items.map((item) => getByPath(item, spec.idKeypath));
      if (ids.some((id) => typeof id !== "string" || !id) || new Set(ids).size !== ids.length) {
        container.dataset.skeletonError = "Tree requires unique string node IDs";
        return;
      }
      delete container.dataset.skeletonError;
      const hadFocus = container.contains(document.activeElement);
      let focusID = binding.focusedID;
      const visited = new Set();
      while (focusID && !ids.includes(focusID) && !visited.has(focusID)) {
        visited.add(focusID);
        focusID = getByPath(binding.rows.get(focusID)?.context, spec.parentIDKeypath);
      }
      const selectedID = resolveKeypath(spec.selectedIDStateKeypath, state.rootData, binding.context);
      if (!ids.includes(focusID)) focusID = ids.includes(selectedID) ? selectedID : ids[0];
      binding.items = items;
      items.forEach((item, index) => {
        const id = ids[index];
        let entry = binding.rows.get(id);
        if (!entry) {
          entry = makeTreeRow(binding, state, id);
          binding.rows.set(id, entry);
        }
        replaceItemContext(entry.context, item);
        const { row, disclosure } = entry;
        row.setAttribute("aria-level", String(getByPath(item, spec.levelKeypath)));
        row.setAttribute("aria-selected", String(id === selectedID));
        row.style.paddingInlineStart = `${getByPath(item, spec.leadingInsetKeypath) || 0}px`;
        const hasChildren = getByPath(item, spec.hasChildrenKeypath) === true;
        const expanded = getByPath(item, spec.expandedKeypath) === true;
        if (hasChildren) row.setAttribute("aria-expanded", String(expanded));
        else row.removeAttribute("aria-expanded");
        disclosure.style.visibility = hasChildren ? "visible" : "hidden";
        disclosure.disabled = !hasChildren;
        disclosure.textContent = expanded ? "▾" : "▸";
        if (container.children[index] !== row) container.insertBefore(row, container.children[index] || null);
      });
      binding.rows.forEach((entry, id) => {
        if (ids.includes(id)) return;
        pruneDescendantBindings(state, entry.row, binding);
        entry.row.remove();
        binding.rows.delete(id);
      });
      container.tabIndex = items.length ? -1 : 0;
      treeFocus(binding, focusID, hadFocus && document.activeElement !== binding.rows.get(focusID)?.row);
      if (hadFocus && !items.length) container.focus();
    });
  }

  function renderComponentSurface(spec, state, context, key, path) {
    // WP-F format: fast instanceID, eller ID lest fra radens data (instanceIDKeypath).
    const resolvedID = typeof spec.instanceID === "string" && spec.instanceID
      ? spec.instanceID
      : resolveKeypath(spec.instanceIDKeypath, state.rootData, context);
    const instanceID = typeof resolvedID === "string" || typeof resolvedID === "number" ? String(resolvedID) : "";
    if (!instanceID) {
      const failure = document.createElement("div");
      failure.className = "skeleton-component-surface-error";
      failure.textContent = "ComponentSurface: unresolved instanceID";
      applySkeletonIdentity(failure, key, path);
      return failure;
    }
    // The cache is keyed solely by instanceID, including when a List reorders.
    let binding = state.componentBindings.get(instanceID);
    if (!binding) {
      const container = document.createElement("div");
      container.className = "skeleton-component-surface";
      container.dataset.instanceId = instanceID;
      binding = { container, itemContext: {}, renderer: null, definition: null };
      state.componentBindings.set(instanceID, binding);
      applyElementModifiers(container, spec.modifiers, state, path, context);
    }
    Object.assign(binding, { spec, context, key, path });
    binding.container.dataset.componentVariant = spec.variant || "inline";
    applySkeletonIdentity(binding.container, `component.${instanceID}`, path);
    return binding.container;
  }

  function componentActionMetadata(mount, instanceID, meta) {
    return { ...meta, sourceCellEndpoint: mount.sourceCellEndpoint,
      mount: { instanceID, componentID: mount.componentID, revision: mount.revision } };
  }

  function updateComponentBindings(state) {
    state.componentBindings.forEach((binding, instanceID) => {
      if (!state.rootElement.contains(binding.container)) {
        binding.renderer?.destroy();
        state.componentBindings.delete(instanceID);
        return;
      }
      const mount = resolveKeypath(binding.spec.sourceKeypath, state.rootData, binding.context);
      const ancestors = state.rendererOptions.componentAncestors || [];
      const valid = !ancestors.includes(instanceID) && ancestors.length < 64 && mount && ["componentID", "revision", "sourceCellEndpoint"].every((key) => typeof mount[key] === "string" && mount[key].trim())
        && validateSkeleton(mount.skeleton).valid;
      if (!valid) {
        binding.renderer?.destroy();
        binding.renderer = null;
        binding.definition = null;
        binding.container.textContent = "ComponentSurface: unresolved or invalid mount";
        binding.container.dataset.skeletonError = "invalid-component-mount";
        return;
      }
      delete binding.container.dataset.skeletonError;
      binding.mount = mount;
      replaceItemContext(binding.itemContext, mount.item);
      const definition = JSON.stringify([mount.componentID, mount.revision]);
      if (definition !== binding.definition) {
        const snapshot = binding.renderer?.captureState();
        binding.renderer?.destroy();
        binding.definition = definition;
        binding.container.dataset.componentId = mount.componentID;
        binding.container.dataset.componentRevision = mount.revision;
        binding.renderer = createRenderer({
          rootElement: binding.container, skeleton: mount.skeleton, itemContext: binding.itemContext,
          dragContext: state.dragContext, layoutContext: state.layoutContext,
          componentAncestors: [...ancestors, instanceID],
          localization: state.rendererOptions.localization,
          localizationContext: state.rendererOptions.localizationContext,
          onAction: (keypath, payload, meta) => state.onAction(keypath, payload, componentActionMetadata(binding.mount, instanceID, meta)),
        });
        binding.renderer.update(state.rootData);
        if (snapshot) binding.renderer.restoreState(snapshot);
      } else {
        binding.renderer.update(state.rootData);
      }
    });
  }

  function captureRendererState(state) {
    const fields = state.fieldBindings.map((binding) => ({
      target: binding.targetKeypath, source: binding.sourceKeypath,
      value: readRememberedFieldValue(state, binding),
      focused: bindingHasFocus(binding), start: binding.element.selectionStart, end: binding.element.selectionEnd,
    }));
    const scroll = Array.from(state.rootElement.querySelectorAll("[data-skeleton-key]")).map((node) => ({
      key: node.dataset.skeletonKey, top: node.scrollTop, left: node.scrollLeft,
      focused: node === document.activeElement,
    }));
    const trees = state.treeBindings.map((binding) => ({ keypath: binding.spec.keypath, focusedID: binding.focusedID,
      focused: binding.container.contains(document.activeElement) }));
    const focusedButton = state.buttonBindings.find((binding) => binding.button === document.activeElement);
    return { fields, scroll, trees, focusedAction: focusedButton ? resolveButtonSpec(focusedButton.spec, focusedButton.context).keypath : null };
  }

  function restoreRendererState(state, snapshot) {
    snapshot.trees.forEach((saved) => {
      const binding = state.treeBindings.find((entry) => entry.spec.keypath === saved.keypath);
      if (binding) treeFocus(binding, saved.focusedID, saved.focused);
    });
    snapshot.fields.forEach((field) => {
      const binding = state.fieldBindings.find((entry) => entry.targetKeypath === field.target && entry.sourceKeypath === field.source);
      if (!binding) return;
      if (field.value !== null) {
        rememberLocalFieldValue(state, binding, field.value);
        writeFieldBindingValue(binding, field.value, false);
      }
      if (field.focused) {
        focusFieldBinding(binding);
        if (typeof field.start === "number" && binding.element.setSelectionRange) binding.element.setSelectionRange(field.start, field.end);
      }
    });
    snapshot.scroll.forEach((saved) => {
      const node = Array.from(state.rootElement.querySelectorAll("[data-skeleton-key]")).find((entry) => entry.dataset.skeletonKey === saved.key);
      if (!node) return;
      node.scrollTop = saved.top;
      node.scrollLeft = saved.left;
      if (saved.focused && !snapshot.focusedAction) node.focus({ preventScroll: true });
    });
    if (snapshot.focusedAction) {
      const button = state.buttonBindings.find((binding) => resolveButtonSpec(binding.spec, binding.context).keypath === snapshot.focusedAction);
      button?.button.focus({ preventScroll: true });
    }
  }

  function renderStack(raw, state, context, key, path, orientation) {
    const container = document.createElement("div");
    container.className = orientation === "hstack" ? "skeleton-hstack" : "skeleton-vstack";
    container.dataset.axis = orientation === "hstack" ? "row" : "column"; // WP-B4 paritet
    applySkeletonIdentity(container, key, path);
    const stackSpec = decodeStackSpec(raw);
    applyElementModifiers(container, stackSpec.modifiers, state, path, context);
    applyStackAlignmentModifiers(container, stackSpec.modifiers, orientation === "hstack" ? "row" : "column");
    if (Number.isFinite(stackSpec.spacing)) {
      container.style.gap = `${stackSpec.spacing}px`;
    }

    const children = decodeChildren(stackSpec.children);
    const anchoredNavigationIndex = orientation === "vstack"
      ? children.findIndex((child) => child.type === "NavigationBar")
      : -1;
    let anchoredNavigation = null;
    children.forEach((child, index) => {
      const rendered = renderElement(child, state, context, `${key}.${child.type}.${index}`, `${path}.${index}`);
      if (index === anchoredNavigationIndex) {
        rendered.classList.add("is-bottom-anchored");
        anchoredNavigation = rendered;
      } else {
        container.appendChild(rendered);
      }
    });
    if (anchoredNavigation) {
      container.appendChild(anchoredNavigation);
    }
    return container;
  }

  function renderText(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const node = document.createElement("div");
    node.className = "skeleton-text";
    applySkeletonIdentity(node, key, path);
    applyElementModifiers(node, spec.modifiers, state, path, context);
    if (spec.modifiers && spec.modifiers.styleRole === "admin-page-heading") {
      node.setAttribute("role", "heading");
      node.setAttribute("aria-level", "1");
    } else if (spec.modifiers && spec.modifiers.styleRole === "admin-section-heading") {
      node.setAttribute("role", "heading");
      node.setAttribute("aria-level", "2");
    }

    const binding = {
      element: node,
      keypath: typeof spec.keypath === "string" ? spec.keypath : null,
      staticText: typeof spec.text === "string" ? spec.text : null,
      localization: spec.modifiers?.localization?.text,
      context,
    };

    state.textBindings.push(binding);
    return node;
  }

  function renderFileUpload(raw, state, context, key, path, elementType) {
    const spec = normalizeFileUploadSpec(raw);
    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-fileupload";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    if (spec.title) {
      const title = document.createElement("div");
      title.className = "skeleton-fileupload-title";
      title.textContent = spec.title;
      wrapper.appendChild(title);
    }
    if (spec.subtitle) {
      const subtitle = document.createElement("div");
      subtitle.className = "skeleton-fileupload-subtitle";
      subtitle.textContent = spec.subtitle;
      wrapper.appendChild(subtitle);
    }

    const card = document.createElement("div");
    card.className = "skeleton-fileupload-card";
    card.tabIndex = 0;
    card.setAttribute("role", "group");
    card.setAttribute("aria-label", spec.title || "File upload");

    const input = document.createElement("input");
    input.type = "file";
    input.className = "skeleton-fileupload-input";
    input.hidden = true;
    input.multiple = spec.allowsMultiple === true;
    if (spec.acceptedContentTypes.length > 0) {
      input.accept = spec.acceptedContentTypes.join(",");
    }

    const empty = document.createElement("div");
    empty.className = "skeleton-fileupload-empty";

    const emptyTitle = document.createElement("div");
    emptyTitle.className = "skeleton-fileupload-empty-title";
    emptyTitle.textContent = spec.emptyTitle || "No file selected";
    empty.appendChild(emptyTitle);

    const emptyMessage = document.createElement("div");
    emptyMessage.className = "skeleton-fileupload-empty-message";
    emptyMessage.textContent = spec.emptyMessage || "Choose a file to send it to this cell.";
    empty.appendChild(emptyMessage);

    const previewList = document.createElement("div");
    previewList.className = "skeleton-fileupload-preview-list";

    const status = document.createElement("div");
    status.className = "skeleton-fileupload-status";
    status.setAttribute("aria-live", "polite");

    const actions = document.createElement("div");
    actions.className = "skeleton-fileupload-actions";

    const chooseButton = document.createElement("button");
    chooseButton.type = "button";
    chooseButton.className = "skeleton-button skeleton-fileupload-button";
    chooseButton.textContent = "Velg fil";
    chooseButton.disabled = !spec.actionKeypath;
    actions.appendChild(chooseButton);

    const submitButton = document.createElement("button");
    submitButton.type = "button";
    submitButton.className = "skeleton-button skeleton-fileupload-submit";
    submitButton.textContent = "Last opp";
    submitButton.hidden = spec.submitOnSelection !== false;
    submitButton.disabled = true;
    actions.appendChild(submitButton);

    card.appendChild(empty);
    card.appendChild(previewList);
    card.appendChild(status);
    card.appendChild(actions);
    card.appendChild(input);
    wrapper.appendChild(card);

    if (spec.helperText) {
      const helper = document.createElement("div");
      helper.className = "skeleton-fileupload-helper";
      helper.textContent = spec.helperText;
      wrapper.appendChild(helper);
    }

    let pendingFiles = [];

    const setStatus = (message, tone) => {
      status.textContent = message || "";
      status.dataset.tone = tone || "";
    };

    const submitFiles = async (files, trigger) => {
      if (!spec.actionKeypath || !files.length) {
        return;
      }

      const validationMessage = validateUploadFiles(files, spec);
      if (validationMessage) {
        setStatus(validationMessage, "error");
        return;
      }

      setStatus("Preparing file…", "busy");
      chooseButton.disabled = true;
      submitButton.disabled = true;
      try {
        const temporaryPayload = await filesToTemporaryAttachmentPayload(files, spec);
        await dispatchAction(state, spec.actionKeypath, {
          kind: trigger === "drop" ? "drop" : "pick",
          fieldID: spec.fieldID || path || key,
          temporaryPayload,
        }, {
          trigger: "fileupload",
          elementType,
          context,
        });
        setStatus("File sent to cell.", "success");
        input.value = "";
        pendingFiles = [];
      } catch (error) {
        console.warn("Skeleton file upload failed", error);
        setStatus(error instanceof Error ? error.message : "File upload failed.", "error");
      } finally {
        chooseButton.disabled = !spec.actionKeypath;
        submitButton.disabled = pendingFiles.length === 0;
      }
    };

    chooseButton.addEventListener("click", () => {
      if (!spec.actionKeypath) {
        return;
      }
      void dispatchAction(state, spec.actionKeypath, {
        kind: "pick",
        fieldID: spec.fieldID || path || key,
      }, {
        trigger: "fileupload-pick",
        elementType,
        context,
      });
      input.click();
    });

    input.addEventListener("change", () => {
      const files = normalizeFileList(input.files, spec);
      if (spec.submitOnSelection === false) {
        pendingFiles = files;
        submitButton.disabled = pendingFiles.length === 0;
        setStatus(files.length ? `${files.length} file${files.length === 1 ? "" : "s"} ready.` : "", "");
        return;
      }
      void submitFiles(files, "pick");
    });

    submitButton.addEventListener("click", () => {
      void submitFiles(pendingFiles, "pick");
    });

    if (spec.supportsDrop) {
      card.classList.add("supports-drop");
      card.addEventListener("dragover", (event) => {
        event.preventDefault();
        card.classList.add("is-drag-targeted");
      });
      card.addEventListener("dragleave", () => {
        card.classList.remove("is-drag-targeted");
      });
      card.addEventListener("drop", (event) => {
        event.preventDefault();
        card.classList.remove("is-drag-targeted");
        const files = normalizeFileList(event.dataTransfer ? event.dataTransfer.files : null, spec);
        void submitFiles(files, "drop");
      });
    }

    state.attachmentBindings.push({
      wrapper,
      card,
      empty,
      previewList,
      status,
      spec,
      context,
      lastSignature: null,
    });

    return wrapper;
  }

  function renderTextField(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};

    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-textfield-wrapper";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    const field = document.createElement("input");
    field.type = "text";
    field.className = "skeleton-textfield";
    field.placeholder = typeof spec.placeholder === "string" ? spec.placeholder : "";
    bindLocalizedText(state, field, spec.modifiers?.localization?.placeholder, context,
      () => spec.placeholder || "", (text) => {
        field.placeholder = text;
        if (spec.modifiers?.styleRole === "admin-form-field") field.setAttribute("aria-label", spec.modifiers?.accessibilityLabel || text || "Adminfelt");
      });
    applyElementModifiers(field, spec.modifiers, state, path, context);
    if (spec.modifiers && spec.modifiers.styleRole === "admin-form-field") {
      field.setAttribute("aria-label", spec.modifiers?.accessibilityLabel || field.placeholder || "Adminfelt");
    }

    const sourceKeypath = typeof spec.sourceKeypath === "string" ? spec.sourceKeypath : null;
    const targetKeypath = typeof spec.targetKeypath === "string" ? spec.targetKeypath : null;

    const binding = {
      element: field,
      sourceKeypath,
      targetKeypath,
      memoryKey: fieldBindingMemoryKey(path, targetKeypath, sourceKeypath),
      staticText: typeof spec.text === "string" ? spec.text : null,
      context,
    };

    wireFieldInput({
      field,
      state,
      binding,
      submitKeypath: targetKeypath,
      submitOnEnter: true,
      trigger: "textfield-submit",
      submitWithMetaEnterOnly: false,
    });

    wrapper.appendChild(field);
    state.fieldBindings.push(binding);
    return wrapper;
  }

  const TEXT_AREA_FIELD_MODIFIERS = ["styleRole", "styleClasses", "fontSize", "fontWeight", "fontFamilies",
    "foregroundColor", "foregroundColorKeypath", "lineHeightMultiple", "letterSpacing", "numericVariant",
    "multilineTextAlignment", "lineLimit", "textDecoration", "localization"];

  function textAreaFieldModifiers(modifiers) {
    if (!modifiers || typeof modifiers !== "object") return modifiers;
    return Object.fromEntries(TEXT_AREA_FIELD_MODIFIERS
      .filter((name) => Object.prototype.hasOwnProperty.call(modifiers, name))
      .map((name) => [name, modifiers[name]]));
  }

  function textAreaDeclaresBox(modifiers) {
    if (!modifiers || typeof modifiers !== "object") return false;
    return (Number.isFinite(modifiers.borderWidth) && modifiers.borderWidth > 0)
      || Boolean(modifiers.background) || Boolean(modifiers.backgroundKeypath)
      || Number.isFinite(modifiers.padding) || Boolean(modifiers.paddingInsets);
  }

  function renderTextArea(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const editorMode = typeof spec.editorMode === "string" ? spec.editorMode.trim() : "";

    if (editorMode === "richMarkdown") {
      return renderRichMarkdownTextArea(spec, state, context, key, path);
    }

    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-textarea-wrapper";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    const field = document.createElement("textarea");
    field.className = "skeleton-textarea";
    field.placeholder = typeof spec.placeholder === "string" ? spec.placeholder : "";
    bindLocalizedText(state, field, spec.modifiers?.localization?.placeholder, context,
      () => spec.placeholder || "", (text) => {
        field.placeholder = text;
        if (spec.modifiers?.styleRole === "admin-form-field") field.setAttribute("aria-label", spec.modifiers?.accessibilityLabel || text || "Adminfelt");
      });
    field.rows = typeof spec.minLines === "number" && spec.minLines > 0 ? spec.minLines : 4;
    if (typeof spec.maxLines === "number" && spec.maxLines > 0) {
      field.style.maxHeight = `${Math.max(spec.maxLines, field.rows) * 1.5}em`;
    }
    // WP-B4 paritet: boksen (ramme, bakgrunn, polstring, størrelse) står på omslaget én gang, som
    // i CellApple; selve feltet får bare typografi og rolle.
    applyElementModifiers(field, textAreaFieldModifiers(spec.modifiers), state, path, context);
    if (textAreaDeclaresBox(spec.modifiers)) wrapper.classList.add("skeleton-textarea-boxed");
    if (spec.modifiers && spec.modifiers.styleRole === "admin-form-field") {
      field.setAttribute("aria-label", spec.modifiers?.accessibilityLabel || field.placeholder || "Adminnotater");
    }

    const sourceKeypath = typeof spec.sourceKeypath === "string" ? spec.sourceKeypath : null;
    const targetKeypath = typeof spec.targetKeypath === "string" ? spec.targetKeypath : null;
    const submitActionKeypath = typeof spec.submitActionKeypath === "string" && spec.submitActionKeypath.trim()
      ? spec.submitActionKeypath.trim()
      : null;
    const submitOnEnter = spec.submitOnEnter === true;

    const binding = {
      element: field,
      sourceKeypath,
      targetKeypath,
      submitActionKeypath,
      memoryKey: fieldBindingMemoryKey(path, targetKeypath, sourceKeypath),
      staticText: typeof spec.text === "string" ? spec.text : null,
      context,
    };

    wireFieldInput({
      field,
      state,
      binding,
      submitKeypath: submitActionKeypath || targetKeypath,
      submitOnEnter,
      trigger: "textarea-submit",
      submitWithMetaEnterOnly: true,
    });

    wrapper.appendChild(field);
    state.fieldBindings.push(binding);
    return wrapper;
  }

  function renderRichMarkdownTextArea(spec, state, context, key, path) {
    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-textarea-wrapper skeleton-rich-textarea-wrapper";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    const toolbar = document.createElement("div");
    toolbar.className = "skeleton-rich-toolbar";

    const editor = document.createElement("div");
    editor.className = "skeleton-rich-textarea";
    editor.contentEditable = "true";
    editor.setAttribute("role", "textbox");
    editor.setAttribute("aria-multiline", "true");
    editor.dataset.placeholder = typeof spec.placeholder === "string" ? spec.placeholder : "";
    bindLocalizedText(state, editor, spec.modifiers?.localization?.placeholder, context,
      () => spec.placeholder || "", (text) => { editor.dataset.placeholder = text; });
    if (typeof spec.minLines === "number" && spec.minLines > 0) {
      editor.style.minHeight = `${Math.max(spec.minLines, 4) * 1.65}em`;
    }
    if (typeof spec.maxLines === "number" && spec.maxLines > 0) {
      editor.style.maxHeight = `${Math.max(spec.maxLines, spec.minLines || 4) * 1.75}em`;
    }
    applyElementModifiers(editor, spec.modifiers, state, path, context);

    const toolbarButtons = [
      { label: "B", command: "bold", title: "Fet tekst" },
      { label: "I", command: "italic", title: "Kursiv tekst" },
      { label: "</>", command: "code", title: "Inline kode" },
      { label: "•", command: "bullet", title: "Punktliste" },
      { label: "❝", command: "quote", title: "Sitat" },
    ];

    toolbarButtons.forEach((item) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "skeleton-rich-toolbar-button";
      button.textContent = item.label;
      button.title = item.title;
      button.addEventListener("mousedown", (event) => {
        event.preventDefault();
      });
      button.addEventListener("click", () => {
        applyRichTextCommand(editor, item.command);
        syncRichTextAreaBinding(binding, state);
      });
      toolbar.appendChild(button);
    });

    const sourceKeypath = typeof spec.sourceKeypath === "string" ? spec.sourceKeypath : null;
    const targetKeypath = typeof spec.targetKeypath === "string" ? spec.targetKeypath : null;
    const submitActionKeypath = typeof spec.submitActionKeypath === "string" && spec.submitActionKeypath.trim()
      ? spec.submitActionKeypath.trim()
      : null;
    const submitKeypath = submitActionKeypath || targetKeypath;
    const submitOnEnter = spec.submitOnEnter === true;

    const binding = {
      element: editor,
      sourceKeypath,
      targetKeypath,
      submitActionKeypath,
      memoryKey: fieldBindingMemoryKey(path, targetKeypath, sourceKeypath),
      staticText: typeof spec.text === "string" ? spec.text : null,
      context,
      editorMode: "richMarkdown",
      readValue: () => serializeRichMarkdown(editor),
      writeValue: (nextValue) => {
        setRichEditorMarkdown(editor, nextValue);
      },
      focus: () => {
        editor.focus({ preventScroll: true });
      },
      insertToken: (token, fallbackText) => {
        applyRichTextToken(editor, token, fallbackText);
      },
      isFocused: () => document.activeElement === editor,
    };

    editor.addEventListener("input", () => {
      syncRichTextAreaBinding(binding, state);
    });

    editor.addEventListener("blur", () => {
      normalizeRichEditor(editor);
      syncRichTextAreaBinding(binding, state);
    });

    editor.addEventListener("keydown", (event) => {
      if (!submitKeypath) {
        return;
      }

      const isMetaEnter = (event.metaKey || event.ctrlKey) && event.key === "Enter";
      const isPlainEnter = event.key === "Enter" && !event.shiftKey && !event.altKey && !event.metaKey && !event.ctrlKey;
      const shouldSubmit = isMetaEnter || (submitOnEnter && isPlainEnter);
      if (!shouldSubmit) {
        return;
      }

      event.preventDefault();
      syncRichTextAreaBinding(binding, state);
      void dispatchAction(state, submitKeypath, readFieldBindingValue(binding), {
        trigger: "textarea-submit",
        binding,
      });
    });

    wrapper.appendChild(toolbar);
    wrapper.appendChild(editor);
    state.fieldBindings.push(binding);
    return wrapper;
  }

  function wireFieldInput({ field, state, binding, submitKeypath, submitOnEnter, trigger, submitWithMetaEnterOnly }) {
    field.addEventListener("input", () => {
      rememberLocalFieldValue(state, binding, field.value);
      if (state.onFieldInput) {
        state.onFieldInput(binding, field.value);
      }
    });

    field.addEventListener("keydown", (event) => {
      if (!submitKeypath) {
        return;
      }

      const isMetaEnter = (event.metaKey || event.ctrlKey) && event.key === "Enter";
      const isPlainEnter = event.key === "Enter" && !event.shiftKey && !event.altKey && !event.metaKey && !event.ctrlKey;

      const shouldSubmit = submitWithMetaEnterOnly
        ? isMetaEnter || (submitOnEnter && isPlainEnter)
        : submitOnEnter && isPlainEnter;

      if (!shouldSubmit) {
        return;
      }

      event.preventDefault();
      void dispatchAction(state, submitKeypath, field.value, {
        trigger,
        binding,
      });
    });
  }

  function resolveButtonSpec(spec, context) {
    const resolved = {
      keypath: typeof spec.keypath === "string" ? spec.keypath : "",
      label: typeof spec.label === "string" ? spec.label : "Action",
      url: typeof spec.url === "string" ? spec.url : null,
      payload: Object.prototype.hasOwnProperty.call(spec, "payload") ? spec.payload : null,
    };

    if (context && typeof context === "object" && !Array.isArray(context)) {
      const keypathField = typeof spec.keypathKeypath === "string" && spec.keypathKeypath.trim()
        ? spec.keypathKeypath.trim()
        : "keypath";
      const labelField = typeof spec.labelKeypath === "string" && spec.labelKeypath.trim()
        ? spec.labelKeypath.trim()
        : "label";
      const payloadField = typeof spec.payloadKeypath === "string" && spec.payloadKeypath.trim()
        ? spec.payloadKeypath.trim()
        : "payload";

      if (typeof context[keypathField] === "string" && context[keypathField].trim()) {
        resolved.keypath = context[keypathField].trim();
      }
      if (typeof context[labelField] === "string" && context[labelField].trim()) {
        resolved.label = context[labelField];
      }
      if (Object.prototype.hasOwnProperty.call(context, payloadField)) {
        resolved.payload = context[payloadField];
      }

      const isDetailNavigationButton = resolved.keypath === "addConfiguration"
        && (
          (typeof context.detailKeypath === "string" && context.detailKeypath.trim())
          || Object.prototype.hasOwnProperty.call(context, "detailPayload")
        );
      if (isDetailNavigationButton) {
        if (typeof context.detailKeypath === "string" && context.detailKeypath.trim()) {
          resolved.keypath = context.detailKeypath.trim();
        }
        if (typeof context.detailLabel === "string" && context.detailLabel.trim()) {
          resolved.label = context.detailLabel;
        }
        if (Object.prototype.hasOwnProperty.call(context, "detailPayload")) {
          resolved.payload = context.detailPayload;
        }
      }
    }

    return resolved;
  }

  function isNavigationButtonSpec(spec) {
    return typeof spec?.keypath === "string"
      && spec.keypath.trim() === ""
      && typeof spec.url === "string"
      && spec.url.trim() !== "";
  }

  function isLoopbackHostname(hostname) {
    const normalized = String(hostname || "").toLowerCase().replace(/^\[|\]$/g, "");
    return normalized === "localhost"
      || normalized.endsWith(".localhost")
      || normalized === "::1"
      || normalized === "127.0.0.1"
      || normalized.startsWith("127.");
  }

  function resolveNavigationURL(spec, baseURL) {
    if (!isNavigationButtonSpec(spec)) {
      return null;
    }

    try {
      const rawURL = spec.url.trim();
      if (rawURL.startsWith("//")) {
        return null;
      }
      const parsed = new URL(rawURL, baseURL);
      const isRelative = !/^[A-Za-z][A-Za-z\d+.-]*:/.test(rawURL);
      if (isRelative && (!baseURL || parsed.origin !== new URL(baseURL).origin)) {
        return null;
      }
      if (parsed.username || parsed.password || !parsed.hostname) {
        return null;
      }
      if (parsed.protocol === "https:") {
        return parsed;
      }
      if (parsed.protocol === "http:" && isLoopbackHostname(parsed.hostname)) {
        return parsed;
      }
    } catch (_error) {
      return null;
    }
    return null;
  }

  function appendSkeletonButtonContent(element, label, iconElement) {
    const labelElement = document.createElement("span");
    labelElement.className = "skeleton-button-label";
    labelElement.textContent = label;
    if (iconElement) {
      element.classList.add("has-icon");
      element.style.display = "inline-flex";
      element.style.alignItems = "center";
      element.style.gap = "6px";
      iconElement.style.flex = "none";
      element.appendChild(iconElement);
    }
    element.appendChild(labelElement);
    return labelElement;
  }

  function renderButton(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const resolved = resolveButtonSpec(spec, context);
    const isNavigation = isNavigationButtonSpec(resolved);
    const navigationURL = resolveNavigationURL(resolved, state.navigationBaseURL);
    const iconElement = createSkeletonIconElement(spec.icon, { className: "skeleton-button-icon" });

    if (isNavigation && navigationURL) {
      const link = document.createElement("a");
      link.className = "skeleton-button skeleton-navigation-link";
      link.href = navigationURL.href;
      const labelElement = appendSkeletonButtonContent(link, resolved.label, iconElement);
      bindLocalizedText(state, link, spec.modifiers?.localization?.label, context,
        () => resolveButtonSpec(spec, context).label, (text) => { labelElement.textContent = text; link.setAttribute("aria-label", spec.modifiers?.accessibilityLabel || text); });
      applySkeletonIdentity(link, key, path);
      applyElementModifiers(link, spec.modifiers, state, path, context);
      if (state.onNavigate) {
        link.addEventListener("click", (event) => {
          event.preventDefault();
          void Promise.resolve(state.onNavigate(navigationURL.href, {
            trigger: "button",
            context,
          })).catch((error) => {
            console.warn("Skeleton navigation failed", error);
          });
        });
      }
      return link;
    }

    const button = document.createElement("button");
    button.type = "button";
    button.className = "skeleton-button";
    applySkeletonIdentity(button, key, path);
    const labelElement = appendSkeletonButtonContent(button, resolved.label, iconElement);
    applyElementModifiers(button, spec.modifiers, state, path, context);

    if (isNavigation) {
      button.disabled = true;
      button.setAttribute("aria-disabled", "true");
      button.title = "Navigation target unavailable";
      return button;
    }

    const binding = {
      button,
      labelElement,
      spec,
      context,
      pendingRequestCount: 0,
      acknowledgementTimeout: null,
      localizedLabel: () => localizedText(state, spec.modifiers?.localization?.label,
        resolveButtonSpec(spec, context).label, context),
    };
    state.buttonBindings.push(binding);
    bindLocalizedText(state, button, spec.modifiers?.localization?.label, context,
      () => resolveButtonSpec(spec, context).label, (text) => {
        setButtonLabelText(binding, binding.pendingRequestCount > 0 ? pendingButtonLabel(text)
          : button.classList.contains("is-acknowledged") ? acknowledgedButtonLabel(text) : text);
        button.setAttribute("aria-label", spec.modifiers?.accessibilityLabel || text);
      });

    button.addEventListener("click", () => {
      const current = resolveButtonSpec(spec, context);
      if (!current.keypath || binding.pendingRequestCount > 0) {
        return;
      }
      markButtonPending(binding, current.label);
      void dispatchAction(state, current.keypath, current.payload, {
        trigger: "button",
        binding,
        context,
      })
        .then(() => {
          acknowledgeButton(binding, current.label);
        })
        .catch((error) => {
          console.warn("Skeleton button action failed", error);
        })
        .finally(() => {
          clearButtonPending(binding);
        });
    });

    return button;
  }

  function setButtonLabelText(binding, text) {
    binding.labelElement.textContent = text;
  }

  function markButtonPending(binding, label) {
    if (!binding || !(binding.button instanceof HTMLButtonElement)) {
      return;
    }

    clearButtonAcknowledgement(binding);
    binding.pendingRequestCount += 1;
    binding.button.disabled = true;
    binding.button.setAttribute("aria-busy", "true");
    binding.button.classList.add("is-pending");
    setButtonLabelText(binding, pendingButtonLabel(resolvedButtonLabel(binding)));
  }

  function clearButtonPending(binding) {
    if (!binding || !(binding.button instanceof HTMLButtonElement)) {
      return;
    }

    binding.pendingRequestCount = Math.max(0, Number(binding.pendingRequestCount || 0) - 1);
    if (binding.pendingRequestCount > 0) {
      return;
    }

    binding.button.disabled = false;
    binding.button.removeAttribute("aria-busy");
    binding.button.classList.remove("is-pending");

    if (!binding.button.classList.contains("is-acknowledged")) {
      setButtonLabelText(binding, resolvedButtonLabel(binding));
    }
  }

  function acknowledgeButton(binding, label) {
    if (!binding || !(binding.button instanceof HTMLButtonElement)) {
      return;
    }

    clearButtonAcknowledgement(binding);
    binding.button.classList.add("is-acknowledged");
    label = resolvedButtonLabel(binding);
    const acknowledgementLabel = acknowledgedButtonLabel(label);
    if (acknowledgementLabel !== label) {
      setButtonLabelText(binding, acknowledgementLabel);
    }

    binding.acknowledgementTimeout = window.setTimeout(() => {
      binding.acknowledgementTimeout = null;
      if (!(binding.button instanceof HTMLButtonElement)) {
        return;
      }
      binding.button.classList.remove("is-acknowledged");
      if (binding.pendingRequestCount === 0) {
        setButtonLabelText(binding, resolvedButtonLabel(binding));
      }
    }, 1100);
  }

  function clearButtonAcknowledgement(binding) {
    if (!binding || !(binding.button instanceof HTMLButtonElement)) {
      return;
    }

    if (binding.acknowledgementTimeout) {
      window.clearTimeout(binding.acknowledgementTimeout);
      binding.acknowledgementTimeout = null;
    }
    binding.button.classList.remove("is-acknowledged");
  }

  function pendingButtonLabel(label) {
    const baseLabel = String(label || "").trim();
    if (!baseLabel) {
      return "Jobber...";
    }
    if (/lagre/i.test(baseLabel)) {
      return "Lagrer...";
    }
    return baseLabel.endsWith("...") ? baseLabel : `${baseLabel}...`;
  }

  function acknowledgedButtonLabel(label) {
    const baseLabel = String(label || "").trim();
    if (/lagre/i.test(baseLabel)) {
      return "Lagret";
    }
    return baseLabel;
  }

  function resolvedButtonLabel(binding) {
    if (!binding) {
      return "";
    }
    return binding.localizedLabel ? binding.localizedLabel() : resolveButtonSpec(binding.spec, binding.context).label;
  }

  function renderList(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-list";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    const keypath = typeof spec.keypath === "string" ? spec.keypath : null;
    const listBinding = {
      kind: "list",
      modifiers: spec.modifiers || {},
      container: wrapper,
      keypath,
      context,
      rowSkeleton: spec.flowElementSkeleton ? decodeElement(spec.flowElementSkeleton) : null,
      fallbackRowKeypath: inferFallbackRowKeypath(keypath),
      selectionMode: normalizeSelectionMode(spec.selectionMode),
      selectionValueKeypath: typeof spec.selectionValueKeypath === "string" ? spec.selectionValueKeypath : null,
      selectionStateKeypath: typeof spec.selectionStateKeypath === "string" ? spec.selectionStateKeypath : null,
      selectionActionKeypath: typeof spec.selectionActionKeypath === "string" ? spec.selectionActionKeypath : null,
      activationActionKeypath: typeof spec.activationActionKeypath === "string" ? spec.activationActionKeypath : null,
      selectionPayloadMode: normalizeSelectionPayloadMode(spec.selectionPayloadMode),
      allowsEmptySelection: typeof spec.allowsEmptySelection === "boolean" ? spec.allowsEmptySelection : true,
      items: [],
      // U2/U3 — tre og følg-halen (admin workbench, PDD 2026-09-04)
      childrenKeypath: typeof spec.childrenKeypath === "string" && spec.childrenKeypath ? spec.childrenKeypath : null,
      expandedStateKeypath: typeof spec.expandedStateKeypath === "string" && spec.expandedStateKeypath ? spec.expandedStateKeypath : null,
      followTail: spec.followTail === true,
      rawItems: [],
      rowMeta: [],
      expanded: null,
      expandedSeedSignature: null,
      selectedIndices: new Set(),
      pendingSelectedIndices: null,
      selectionSyncSuspended: false,
      lastSignature: null,
    };

    state.listBindings.push(listBinding);
    return wrapper;
  }

  function renderDivider(raw, state, context, path) {
    const divider = document.createElement("hr");
    divider.className = "skeleton-divider";
    if (typeof path === "string" && path.length > 0) {
      divider.dataset.skeletonPath = path;
    }
    if (raw && typeof raw === "object") {
      applyElementModifiers(divider, raw.modifiers, state, path, context);
    }
    return divider;
  }

  function renderSection(raw, state, context, key, path) {
    const section = document.createElement("section");
    section.className = "skeleton-section";
    applySkeletonIdentity(section, key, path);

    const spec = raw && typeof raw === "object" ? raw : {};
    applyElementModifiers(section, spec.modifiers, state, path, context);
    if (spec.header) {
      const header = document.createElement("div");
      header.className = "skeleton-section-header";
      header.appendChild(renderElement(decodeElement(spec.header), state, context, `${key}.section.header`, `${path}.header`));
      section.appendChild(header);
    }

    const children = Array.isArray(spec.content) ? spec.content : [];
    const content = document.createElement("div");
    content.className = "skeleton-section-content";
    section.appendChild(content);

    children.forEach((child, index) => {
      content.appendChild(renderElement(decodeElement(child), state, context, `${key}.section.${index}`, `${path}.${index}`));
    });

    if (spec.footer) {
      const footer = document.createElement("div");
      footer.className = "skeleton-section-footer";
      footer.appendChild(renderElement(decodeElement(spec.footer), state, context, `${key}.section.footer`, `${path}.footer`));
      section.appendChild(footer);
    }

    return section;
  }

  function renderScrollView(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const scroller = document.createElement("div");
    scroller.className = "skeleton-scroll-view";
    const axis = typeof spec.axis === "string" && spec.axis.trim()
      ? spec.axis.trim().toLowerCase()
      : "vertical";
    scroller.dataset.scrollAxis = axis;
    scroller.classList.add(`scroll-axis-${sanitizeClassName(axis)}`);
    applySkeletonIdentity(scroller, key, path);
    applyElementModifiers(scroller, spec.modifiers, state, path, context);

    const children = Array.isArray(spec.elements) ? spec.elements : [];
    const anchoredNavigationIndex = children.findIndex((child) => (
      isPlainObject(child) && Object.keys(child)[0] === "NavigationBar"
    ));
    let anchoredNavigation = null;
    children.forEach((child, index) => {
      const rendered = renderElement(decodeElement(child), state, context, `${key}.scroll.${index}`, `${path}.${index}`);
      if (index === anchoredNavigationIndex) {
        rendered.classList.add("is-bottom-anchored");
        anchoredNavigation = rendered;
      } else {
        scroller.appendChild(rendered);
      }
    });
    if (anchoredNavigation) {
      scroller.appendChild(anchoredNavigation);
    }

    return scroller;
  }

  function renderSpacer(raw, state, context, path) {
    const spacer = document.createElement("div");
    spacer.className = "skeleton-spacer";
    if (typeof path === "string" && path.length > 0) {
      spacer.dataset.skeletonPath = path;
    }
    if (raw && typeof raw === "object") {
      applyElementModifiers(spacer, raw.modifiers, state, path, context);
    }
    const width = raw && typeof raw === "object" && typeof raw.width === "number" ? raw.width : null;
    if (width !== null) {
      spacer.style.width = `${width}px`;
      spacer.style.minWidth = `${width}px`;
      spacer.style.flex = "0 0 auto";
    } else {
      // WP-B4 paritet: som SwiftUI Spacer tar en Spacer uten bredde ledig plass langs stakkens akse.
      spacer.style.flex = "1 1 0px";
      spacer.style.minWidth = "0px";
      spacer.style.minHeight = "0px";
    }
    return spacer;
  }

  function renderImage(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-image-wrapper";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers);

    // Mirrors CellApple's native resolvedImage(_:): a url always wins (loaded
    // as a real image), and only in its absence does type === "system" mean
    // "this name is an SF Symbol, not an asset catalog image name" — resolved
    // here into the bundled Lucide set instead of the /images/<name> path
    // resolveImageSource() falls back to below.
    const hasURL = typeof spec.url === "string" && spec.url.trim().length > 0;
    const isSystemIcon = !hasURL && spec.type === "system" && typeof spec.name === "string" && spec.name.trim();
    if (isSystemIcon) {
      const icon = createSkeletonIconElement(spec.name, { className: "skeleton-image skeleton-image-icon" });
      if (icon) {
        icon.removeAttribute("aria-hidden");
        icon.setAttribute("role", "img");
        icon.setAttribute("aria-label", spec.modifiers?.accessibilityLabel || spec.name.trim());
        if (spec.padding && Number.isFinite(spec.padding)) {
          wrapper.style.padding = `${spec.padding}px`;
        }
        wrapper.appendChild(icon);
        return wrapper;
      }
    }

    const image = document.createElement("img");
    image.className = "skeleton-image";
    image.loading = "lazy";
    image.alt = spec.modifiers?.accessibilityLabel || (typeof spec.name === "string" ? spec.name : "skeleton-image");

    const source = resolveImageSource(spec);
    if (source) {
      image.src = source;
    }
    if (spec.scaledToFit === true) {
      image.style.objectFit = "contain";
      image.style.width = "100%";
      image.style.height = "100%";
    }
    if (spec.padding && Number.isFinite(spec.padding)) {
      wrapper.style.padding = `${spec.padding}px`;
    }

    wrapper.appendChild(image);
    return wrapper;
  }

  function resolveImageSource(spec) {
    if (typeof spec.url === "string" && spec.url.trim()) {
      return spec.url.trim();
    }
    if (typeof spec.name === "string" && spec.name.trim()) {
      const name = spec.name.trim();
      if (name.startsWith("http://") || name.startsWith("https://") || name.startsWith("/")) {
        return name;
      }
      return `/images/${name}`;
    }
    return "";
  }

  function renderReference(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-reference";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    const title = document.createElement("p");
    title.className = "skeleton-reference-title";
    const topic = typeof spec.topic === "string" && spec.topic ? ` (${spec.topic})` : "";
    title.textContent = `Reference ${spec.keypath || ""}${topic}`;
    wrapper.appendChild(title);

    const rows = document.createElement("div");
    rows.className = "skeleton-list";
    wrapper.appendChild(rows);

    const binding = {
      kind: "reference",
      container: rows,
      keypath: typeof spec.keypath === "string" ? spec.keypath : null,
      context,
      rowSkeleton: spec.flowElementSkeleton ? decodeElement(spec.flowElementSkeleton) : null,
      fallbackRowKeypath: inferFallbackRowKeypath(typeof spec.keypath === "string" ? spec.keypath : null),
      lastSignature: null,
    };
    state.referenceBindings.push(binding);
    return wrapper;
  }

  function renderZStack(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-zstack";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    const children = Array.isArray(spec.elements) ? spec.elements : [];
    children.forEach((child, index) => {
      const layer = document.createElement("div");
      layer.className = "skeleton-zstack-layer";
      layer.appendChild(renderElement(decodeElement(child), state, context, `${key}.zstack.${index}`, `${path}.${index}`));
      wrapper.appendChild(layer);
    });

    return wrapper;
  }

  function renderGrid(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-grid";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    const columns = Array.isArray(spec.columns) ? spec.columns : [];
    if (columns.length) {
      wrapper.style.gridTemplateColumns = gridTemplateColumns(columns);
    }
    if (Number.isFinite(spec.spacing)) {
      wrapper.style.gap = `${spec.spacing}px`;
    }

    const keypath = typeof spec.keypath === "string" ? spec.keypath : null;
    if (keypath) {
      state.gridBindings.push({
        kind: "grid",
        container: wrapper,
        keypath,
        context,
        rowSkeleton: spec.itemSkeleton ? decodeElement(spec.itemSkeleton) : null,
        fallbackRowKeypath: inferFallbackRowKeypath(keypath),
        items: [],
        lastSignature: null,
      });
      return wrapper;
    }

    const children = Array.isArray(spec.elements) ? spec.elements : [];
    children.forEach((child, index) => {
      wrapper.appendChild(renderElement(decodeElement(child), state, context, `${key}.grid.${index}`, `${path}.${index}`));
    });

    return wrapper;
  }

  function gridTemplateColumns(columns) {
    const adaptive = columns.find((column) => column && column.type === "adaptive");
    if (adaptive) {
      const min = Number.isFinite(adaptive.min) ? adaptive.min : 120;
      if (Number.isFinite(adaptive.max) && adaptive.max > min) {
        return `repeat(auto-fit, minmax(${min}px, ${adaptive.max}px))`;
      }
      return `repeat(auto-fit, minmax(${min}px, 1fr))`;
    }

    return columns
      .map((column) => {
        if (!column || typeof column !== "object") {
          return "1fr";
        }
        if (column.type === "fixed" && Number.isFinite(column.value)) {
          return `${column.value}px`;
        }
        if (column.type === "flexible") {
          const min = Number.isFinite(column.min) ? column.min : 0;
          if (Number.isFinite(column.max) && column.max > min) {
            return `minmax(${min}px, ${column.max}px)`;
          }
          return `minmax(${min}px, 1fr)`;
        }
        return "1fr";
      })
      .join(" ");
  }

  function renderToggle(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const wrapper = document.createElement("label");
    wrapper.className = "skeleton-toggle";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    const input = document.createElement("input");
    input.type = "checkbox";
    if (spec.modifiers?.accessibilityLabel) input.setAttribute("aria-label", spec.modifiers.accessibilityLabel);

    const label = document.createElement("span");
    label.textContent = typeof spec.label === "string" ? spec.label : "Toggle";

    wrapper.appendChild(input);
    wrapper.appendChild(label);

    const keypath = typeof spec.keypath === "string" ? spec.keypath : null;
    if (typeof spec.isOn === "boolean") {
      input.checked = spec.isOn;
    }

    input.addEventListener("change", () => {
      if (!keypath) {
        return;
      }
      void dispatchAction(state, keypath, input.checked, {
        trigger: "toggle",
      });
    });

    state.toggleBindings.push({
      element: input,
      keypath,
      context,
    });

    return wrapper;
  }

  function renderPicker(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-picker";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    const pickerLabel = typeof spec.label === "string" ? spec.label.trim() : "";
    if (pickerLabel) {
      const label = document.createElement("label");
      label.className = "skeleton-picker-label";
      label.textContent = pickerLabel;
      wrapper.appendChild(label);
    }

    const select = document.createElement("select");
    select.className = "skeleton-picker-select";
    if (pickerLabel) {
      select.setAttribute("aria-label", pickerLabel);
    }
    applyElementModifiers(select, spec.modifiers, state, path, context);
    wrapper.appendChild(select);

    const binding = {
      element: select,
      keypath: typeof spec.keypath === "string" ? spec.keypath : null,
      context,
      optionLabelKeypath: typeof spec.optionLabelKeypath === "string" ? spec.optionLabelKeypath : null,
      selectionValueKeypath: typeof spec.selectionValueKeypath === "string" ? spec.selectionValueKeypath : null,
      selectionStateKeypath: typeof spec.selectionStateKeypath === "string" ? spec.selectionStateKeypath : null,
      selectionActionKeypath: typeof spec.selectionActionKeypath === "string" ? spec.selectionActionKeypath : null,
      selectionPayloadMode: normalizeSelectionPayloadMode(spec.selectionPayloadMode),
      allowsEmptySelection: typeof spec.allowsEmptySelection === "boolean" ? spec.allowsEmptySelection : true,
      placeholder: typeof spec.placeholder === "string" && spec.placeholder.trim()
        ? spec.placeholder.trim()
        : "Velg",
      staticElements: Array.isArray(spec.elements) ? spec.elements : [],
      selectionMode: "single",
      items: [],
      selectedIndices: new Set(),
      lastSignature: null,
      lastResolvedSelectionSignature: null,
    };

    select.addEventListener("change", () => {
      const previousIndex = sortedSelectionIndices(binding.selectedIndices)[0] ?? null;
      const nextIndex = select.value === "" ? null : Number.parseInt(select.value, 10);
      const trigger = nextIndex === null ? "deselect" : "select";

      binding.selectedIndices = Number.isInteger(nextIndex)
        ? new Set([nextIndex])
        : new Set();

      void submitPickerSelectionChange(binding, state, trigger, previousIndex);
    });

    state.pickerBindings.push(binding);
    return wrapper;
  }

  function renderTabs(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-tabs";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    const tablist = document.createElement("div");
    tablist.className = "skeleton-tabs-list";
    tablist.setAttribute("role", "tablist");

    const panel = document.createElement("div");
    panel.className = "skeleton-tabs-panel";

    wrapper.appendChild(tablist);
    wrapper.appendChild(panel);

    const binding = {
      kind: "tabs",
      wrapper,
      tablist,
      panel,
      context,
      path,
      tabsKeypath: typeof spec.tabsKeypath === "string" ? spec.tabsKeypath : null,
      activeTabStateKeypath: typeof spec.activeTabStateKeypath === "string" ? spec.activeTabStateKeypath : "",
      selectionActionKeypath: typeof spec.selectionActionKeypath === "string" ? spec.selectionActionKeypath : null,
      idKeypath: typeof spec.idKeypath === "string" && spec.idKeypath.length ? spec.idKeypath : "id",
      labelKeypath: typeof spec.labelKeypath === "string" && spec.labelKeypath.length ? spec.labelKeypath : "title",
      panels: Array.isArray(spec.panels) ? spec.panels : [],
      memoryKey: tabMemoryKey(state, key, path, spec),
      rows: [],
      activeTabID: "",
      localSelectedTabID: "",
      localSelectionExpiresAt: 0,
      lastRowsSignature: null,
      lastRenderedPanelID: null,
    };

    state.tabBindings.push(binding);
    renderTabsBinding(binding, state);
    return wrapper;
  }

  function renderNavigationBar(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const navigation = document.createElement("nav");
    navigation.className = "skeleton-navigation-bar";
    navigation.setAttribute("aria-label", "App navigation");
    applySkeletonIdentity(navigation, key, path);
    applyElementModifiers(navigation, spec.modifiers, state, path, context);

    const binding = {
      navigation,
      context,
      path,
      activeStateKeypath: typeof spec.activeStateKeypath === "string" ? spec.activeStateKeypath : null,
      items: Array.isArray(spec.items) ? spec.items : [],
      itemBindings: [],
      // Mirrors Tabs' localSelectedTabID/localSelectionExpiresAt: highlight
      // the tapped item immediately instead of waiting for the round trip
      // and the next reconcile tick to confirm it server-side.
      localActiveValue: null,
      localActiveValueExpiresAt: 0,
    };
    state.navigationBarBindings.push(binding);
    renderNavigationBarBinding(binding, state);
    return navigation;
  }

  function renderNavigationBarBinding(binding, state) {
    binding.navigation.replaceChildren();
    binding.itemBindings = [];

    binding.items.forEach((spec, index) => {
      const resolved = resolveButtonSpec(spec, binding.context);
      const isNavigation = isNavigationButtonSpec(resolved);
      const navigationURL = resolveNavigationURL(resolved, state.navigationBaseURL);
      let element;

      if (isNavigation && navigationURL) {
        element = document.createElement("a");
        element.href = navigationURL.href;
        if (state.onNavigate) {
          element.addEventListener("click", (event) => {
            event.preventDefault();
            void Promise.resolve(state.onNavigate(navigationURL.href, {
              trigger: "button",
              context: binding.context,
              navigationBar: true,
            })).catch((error) => {
              console.warn("Skeleton navigation bar navigation failed", error);
            });
          });
        }
      } else {
        element = document.createElement("button");
        element.type = "button";
        if (isNavigation || !resolved.keypath) {
          element.disabled = true;
          element.setAttribute("aria-disabled", "true");
          element.title = isNavigation ? "Navigation target unavailable" : "Action target unavailable";
        } else {
          let pending = false;
          element.addEventListener("click", () => {
            const current = resolveButtonSpec(spec, binding.context);
            if (pending || !current.keypath) {
              return;
            }
            pending = true;
            element.disabled = true;
            element.setAttribute("aria-busy", "true");
            if (typeof spec.activeValue === "string" && spec.activeValue) {
              binding.localActiveValue = spec.activeValue;
              // Same rule as the tab strip: held until the action settles, with
              // the ceiling only as a backstop. The five-second version let the
              // highlight snap back to the previous item on a slow round trip
              // while the surface had already moved on.
              binding.localActiveValueExpiresAt = Date.now() + TAB_SELECTION_HOLD_CEILING_MS;
              updateNavigationBarBinding(binding, state);
            }
            void dispatchAction(state, current.keypath, current.payload, {
              trigger: "button",
              context: binding.context,
              navigationBar: true,
            })
              .catch((error) => {
                console.warn("Skeleton navigation bar action failed", error);
              })
              .finally(() => {
                pending = false;
                element.disabled = false;
                element.removeAttribute("aria-busy");
                binding.localActiveValue = null;
                binding.localActiveValueExpiresAt = 0;
              });
          });
        }
      }

      element.className = "skeleton-navigation-bar-item";
      element.textContent = resolved.label;
      element.dataset.navigationBarIndex = String(index);
      applyElementModifiers(element, spec.modifiers, state, `${binding.path}.items.${index}`, binding.context);
      binding.navigation.appendChild(element);
      binding.itemBindings.push({ element, spec, isNavigation });
    });

    updateNavigationBarBinding(binding, state);
  }

  function updateNavigationBarBindings(state) {
    state.navigationBarBindings.forEach((binding) => updateNavigationBarBinding(binding, state));
  }

  function updateNavigationBarBinding(binding, state) {
    const resolvedStateValue = binding.activeStateKeypath
      ? comparableSkeletonValue(resolveKeypath(binding.activeStateKeypath, state.rootData, binding.context))
      : null;
    const activeStateValue = binding.localActiveValue && Date.now() < binding.localActiveValueExpiresAt
      ? binding.localActiveValue
      : resolvedStateValue;

    binding.itemBindings.forEach(({ element, spec, isNavigation }) => {
      const isActive = isNavigation
        ? typeof spec.activeConfigurationName === "string"
          && spec.activeConfigurationName === state.currentConfigurationName
        : typeof spec.activeValue === "string" && spec.activeValue === activeStateValue;
      element.classList.toggle("is-active", isActive);
      if (isActive) {
        element.setAttribute("aria-current", "page");
      } else {
        element.removeAttribute("aria-current");
      }
    });
  }

  function comparableSkeletonValue(value) {
    if (typeof value === "string") return value;
    if (typeof value === "number" || typeof value === "boolean") return String(value);
    return null;
  }

  function renderVisualization(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const wrapper = document.createElement("div");
    wrapper.className = "skeleton-visualization";
    wrapper.style.minWidth = "0";
    wrapper.style.maxWidth = "100%";
    applySkeletonIdentity(wrapper, key, path);
    applyElementModifiers(wrapper, spec.modifiers, state, path, context);

    const body = document.createElement("div");
    body.className = "skeleton-visualization-body";
    body.style.minWidth = "0";
    body.style.maxWidth = "100%";
    wrapper.appendChild(body);

    const inlineSpec = Object.prototype.hasOwnProperty.call(spec, "spec") ? spec.spec : null;
    state.visualizationBindings.push({
      wrapper,
      body,
      kind: stringOrNull(spec.kind) || "table",
      keypath: stringOrNull(spec.keypath),
      stateKeypath: stringOrNull(spec.stateKeypath),
      actionKeypath: stringOrNull(spec.actionKeypath),
      inlineSpec,
      accessibilityLabel: inlineSpec && typeof inlineSpec === "object" && !Array.isArray(inlineSpec)
        ? visualizationString(inlineSpec.accessibilityLabel || inlineSpec.title || inlineSpec.label)
        : "",
      context,
      lastSignature: null,
    });

    return wrapper;
  }

  function visualizationString(value) {
    if (typeof value === "string" && value.trim()) {
      return value.trim();
    }
    if (typeof value === "number" || typeof value === "boolean") {
      return String(value);
    }
    if (value && typeof value === "object" && !Array.isArray(value)) {
      return visualizationString(value.label || value.title || value.name || value.id);
    }
    return "";
  }

  function visualizationNumber(value) {
    if (typeof value === "number" && Number.isFinite(value)) {
      return value;
    }
    if (typeof value === "string" && value.trim()) {
      const parsed = Number.parseFloat(value.replace(",", "."));
      return Number.isFinite(parsed) ? parsed : null;
    }
    return null;
  }

  function visualizationDisplay(value) {
    if (value == null) {
      return "";
    }
    if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
      return String(value);
    }
    return safeJSONStringify(value);
  }

  function visualizationRows(spec) {
    if (Array.isArray(spec)) {
      return spec;
    }
    const object = spec && typeof spec === "object" && !Array.isArray(spec) ? spec : {};
    for (const key of ["rows", "items", "data", "values"]) {
      if (Array.isArray(object[key])) {
        return object[key];
      }
    }
    return [];
  }

  function visualizationColumns(spec) {
    const object = spec && typeof spec === "object" && !Array.isArray(spec) ? spec : {};
    if (Array.isArray(object.columns) && object.columns.length) {
      const columns = object.columns.map((column, index) => {
        if (typeof column === "string" && column.trim()) {
          return { id: column.trim(), key: column.trim(), label: column.trim(), align: "leading" };
        }
        if (column && typeof column === "object" && !Array.isArray(column)) {
          const key = visualizationString(column.key || column.id || column.label) || `column-${index}`;
          return {
            id: key,
            key,
            label: visualizationString(column.label || column.title) || key,
            align: visualizationString(column.alignment || column.align || "leading").toLowerCase(),
          };
        }
        return null;
      }).filter(Boolean);
      if (columns.length) {
        return columns;
      }
    }

    const rows = visualizationRows(spec);
    const first = rows[0];
    if (first && typeof first === "object" && !Array.isArray(first)) {
      return Object.keys(first).sort().map((key) => ({
        id: key,
        key,
        label: key,
        align: "leading",
      }));
    }
    return [{ id: "value", key: "__value__", label: "value", align: "leading" }];
  }

  function visualizationCellValue(row, column) {
    if (column.key === "__value__") {
      return row;
    }
    return row && typeof row === "object" && !Array.isArray(row) ? row[column.key] : null;
  }

  function visualizationChartStyle(spec) {
    const object = spec && typeof spec === "object" && !Array.isArray(spec) ? spec : {};
    return (visualizationString(object.chartType || object.style || object.variant || "bar") || "bar").toLowerCase();
  }

  function visualizationChartPoints(spec) {
    return visualizationRows(spec).map((row, index) => {
      if (typeof row === "number" && Number.isFinite(row)) {
        return { id: `point-${index}`, label: `Item ${index + 1}`, value: row, color: "", raw: row };
      }
      if (row && typeof row === "object" && !Array.isArray(row)) {
        const value = visualizationNumber(row.value ?? row.y ?? row.amount ?? row.count);
        if (!Number.isFinite(value)) {
          return null;
        }
        return {
          id: visualizationString(row.id || row.label) || `point-${index}`,
          label: visualizationString(row.label || row.title || row.name || row.id) || `Item ${index + 1}`,
          value,
          color: visualizationString(row.color),
          raw: row,
        };
      }
      return null;
    }).filter(Boolean);
  }

  function visualizationGraphNodes(spec) {
    const source = Array.isArray(spec)
      ? spec
      : (spec && typeof spec === "object" && !Array.isArray(spec) ? (Array.isArray(spec.nodes) ? spec.nodes : spec.items) : []);
    if (!Array.isArray(source)) {
      return [];
    }
    return source.map((node, index) => {
      if (!node || typeof node !== "object" || Array.isArray(node)) {
        return null;
      }
      return {
        id: visualizationString(node.id) || `node-${index}`,
        label: visualizationString(node.label || node.title || node.name || node.id) || `Node ${index + 1}`,
        subtitle: visualizationString(node.subtitle || node.kind || node.group),
        kind: visualizationString(node.kind || node.group || "node"),
        group: visualizationString(node.group || node.kind || "node"),
        x: visualizationNumber(node.x),
        y: visualizationNumber(node.y),
        color: visualizationString(node.color),
        radius: visualizationNumber(node.radius),
        raw: node,
      };
    }).filter(Boolean);
  }

  function visualizationGraphEdges(spec) {
    const object = spec && typeof spec === "object" && !Array.isArray(spec) ? spec : {};
    const source = Array.isArray(object.edges) ? object.edges : object.links;
    if (!Array.isArray(source)) {
      return [];
    }
    return source.map((edge, index) => {
      if (!edge || typeof edge !== "object" || Array.isArray(edge)) {
        return null;
      }
      const sourceID = visualizationString(edge.source || edge.from);
      const targetID = visualizationString(edge.target || edge.to);
      if (!sourceID || !targetID) {
        return null;
      }
      return {
        id: visualizationString(edge.id) || `edge-${index}`,
        source: sourceID,
        target: targetID,
        label: visualizationString(edge.label || edge.relationship || edge.kind),
        color: visualizationString(edge.color),
        raw: edge,
      };
    }).filter(Boolean);
  }

  const visualizationDayMs = 24 * 60 * 60 * 1000;

  function visualizationDateMs(value) {
    const raw = visualizationString(value);
    if (!raw) {
      return null;
    }
    const iso = raw.match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (iso) {
      const year = Number.parseInt(iso[1], 10);
      const month = Number.parseInt(iso[2], 10);
      const day = Number.parseInt(iso[3], 10);
      const ms = Date.UTC(year, month - 1, day);
      return Number.isFinite(ms) ? ms : null;
    }
    const parsed = Date.parse(raw);
    if (!Number.isFinite(parsed)) {
      return null;
    }
    const date = new Date(parsed);
    return Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
  }

  function visualizationDateLabel(ms) {
    if (!Number.isFinite(ms)) {
      return "";
    }
    return new Date(ms).toISOString().slice(0, 10);
  }

  function visualizationTimelineStatusColor(item) {
    const health = String(item.health || "").toLowerCase();
    const status = String(item.status || "").toLowerCase();
    const priority = String(item.priority || "").toLowerCase();
    if (status === "blocked" || health === "red") {
      return "#E95656";
    }
    if (health === "yellow" || priority === "p0" || priority === "p1") {
      return "#D99B2B";
    }
    if (["done", "shipped", "completed", "closed"].includes(status)) {
      return "#44A36F";
    }
    return "#2C8F88";
  }

  function visualizationTimelineItems(spec) {
    return visualizationRows(spec).map((row, index) => {
      if (!row || typeof row !== "object" || Array.isArray(row)) {
        return null;
      }
      const rawStart = row.start ?? row.startDate ?? row.from ?? row.begin;
      const rawEnd = row.end ?? row.endDate ?? row.target ?? row.targetDate ?? row.dueDate ?? row.date;
      let startMs = visualizationDateMs(rawStart);
      let endMs = visualizationDateMs(rawEnd);
      if (!Number.isFinite(startMs) && Number.isFinite(endMs)) {
        startMs = endMs;
      }
      if (Number.isFinite(startMs) && !Number.isFinite(endMs)) {
        endMs = startMs;
      }
      if (Number.isFinite(startMs) && Number.isFinite(endMs) && startMs > endMs) {
        const swapped = startMs;
        startMs = endMs;
        endMs = swapped;
      }
      const label = visualizationString(row.label || row.title || row.project || row.name || row.id) || `Item ${index + 1}`;
      const subtitle = visualizationString(row.summary || row.focus || row.nextAction || row.status || row.health);
      const id = visualizationString(row.id || row.projectID || row.milestoneID || label) || `timeline-${index}`;
      const laneID = visualizationString(row.laneID || row.releaseID || row.releaseRef || row.lane || row.release);
      const laneLabel = visualizationString(row.laneLabel || row.releaseTitle || row.release || row.lane || laneID);
      const computedStartLabel = visualizationDateLabel(startMs);
      const computedEndLabel = visualizationDateLabel(endMs);
      const startLabel = visualizationString(row.startLabel || row.startDateLabel) || computedStartLabel;
      const endLabel = visualizationString(row.endLabel || row.endDateLabel || row.targetLabel || row.targetDateLabel) || computedEndLabel;
      const dateRange = visualizationString(row.dateRange || row.rangeLabel)
        || (startLabel && endLabel ? `${startLabel} - ${endLabel}` : (startLabel || endLabel));
      return {
        index,
        id,
        label,
        subtitle,
        status: visualizationString(row.status),
        health: visualizationString(row.health),
        priority: visualizationString(row.priority),
        laneID,
        laneLabel,
        laneTarget: visualizationString(row.laneTarget || row.releaseTarget),
        startMs,
        endMs,
        startLabel,
        endLabel,
        dateRange,
        milestoneLabel: visualizationString(row.nextMilestone || row.title),
        raw: row,
      };
    }).filter(Boolean);
  }

  function visualizationTimelineGroups(items) {
    const groups = [];
    const groupsByID = new Map();
    items.forEach((item) => {
      const id = item.laneID || "__unassigned";
      let group = groupsByID.get(id);
      if (!group) {
        group = {
          id,
          label: item.laneLabel || (item.laneID ? item.laneID : "No release"),
          target: item.laneTarget || "",
          items: [],
        };
        groupsByID.set(id, group);
        groups.push(group);
      }
      if (!group.target && item.laneTarget) {
        group.target = item.laneTarget;
      }
      group.items.push(item);
    });
    return groups;
  }

  function visualizationTimelineRange(items) {
    const dated = items.filter((item) => Number.isFinite(item.startMs) && Number.isFinite(item.endMs));
    if (!dated.length) {
      return null;
    }
    let min = Math.min(...dated.map((item) => item.startMs));
    let max = Math.max(...dated.map((item) => item.endMs));
    if (min === max) {
      min -= 7 * visualizationDayMs;
      max += 7 * visualizationDayMs;
    } else {
      min -= visualizationDayMs;
      max += visualizationDayMs;
    }
    return { min, max, span: Math.max(max - min, visualizationDayMs) };
  }

  function visualizationTimelinePosition(ms, range) {
    if (!range || !Number.isFinite(ms)) {
      return 0;
    }
    return Math.max(0, Math.min(100, ((ms - range.min) / range.span) * 100));
  }

  function visualizationMapCoordinate(value) {
    if (!Array.isArray(value) || value.length < 2) {
      return null;
    }
    const first = visualizationNumber(value[0]);
    const second = visualizationNumber(value[1]);
    if (!Number.isFinite(first) || !Number.isFinite(second)) {
      return null;
    }
    return [first, second];
  }

  function visualizationMapBounds(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      return null;
    }
    const minX = visualizationNumber(value.minX);
    const minY = visualizationNumber(value.minY);
    const maxX = visualizationNumber(value.maxX);
    const maxY = visualizationNumber(value.maxY);
    if (![minX, minY, maxX, maxY].every(Number.isFinite)) {
      return null;
    }
    return { minX, minY, maxX, maxY };
  }

  function visualizationMapViewport(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      return null;
    }
    return {
      center: visualizationMapCoordinate(value.center),
      zoom: visualizationNumber(value.zoom),
      bounds: visualizationMapBounds(value.bounds),
    };
  }

  function visualizationMapBase(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      return null;
    }
    const kind = visualizationString(value.kind || (value.urlTemplate ? "tiles" : (value.url ? "image" : ""))).toLowerCase();
    if (kind === "tiles") {
      const urlTemplate = visualizationString(value.urlTemplate || value.template || value.url);
      if (!urlTemplate) {
        return null;
      }
      return {
        kind: "tiles",
        urlTemplate,
        attribution: visualizationString(value.attribution),
        minZoom: visualizationNumber(value.minZoom),
        maxZoom: visualizationNumber(value.maxZoom),
        tileSize: visualizationNumber(value.tileSize),
        subdomains: Array.isArray(value.subdomains) ? value.subdomains.map(visualizationString).filter(Boolean) : null,
      };
    }
    if (kind === "image") {
      const url = visualizationString(value.url);
      const bounds = visualizationMapBounds(value.bounds);
      if (!url || !bounds) {
        return null;
      }
      const intrinsicSize = value.intrinsicSize && typeof value.intrinsicSize === "object" && !Array.isArray(value.intrinsicSize)
        ? {
            width: visualizationNumber(value.intrinsicSize.width),
            height: visualizationNumber(value.intrinsicSize.height),
          }
        : null;
      return {
        kind: "image",
        url,
        bounds,
        intrinsicSize: intrinsicSize && Number.isFinite(intrinsicSize.width) && Number.isFinite(intrinsicSize.height)
          ? intrinsicSize
          : null,
        opacity: visualizationNumber(value.opacity),
      };
    }
    return null;
  }

  function visualizationMapStyle(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      return {};
    }
    return {
      strokeColor: visualizationString(value.strokeColor),
      strokeWidth: visualizationNumber(value.strokeWidth),
      strokeOpacity: visualizationNumber(value.strokeOpacity),
      fillColor: visualizationString(value.fillColor),
      fillOpacity: visualizationNumber(value.fillOpacity),
      tintColor: visualizationString(value.tintColor),
      radius: visualizationNumber(value.radius),
    };
  }

  function buildVisualizationMapFeaturePayload(feature, coordinateSpace) {
    const payload = feature.raw && typeof feature.raw === "object" && !Array.isArray(feature.raw)
      ? { ...feature.raw }
      : {};
    payload.id = visualizationString(payload.id) || feature.id;
    if (feature.label && !payload.label) {
      payload.label = feature.label;
    }
    payload.coordinateSpace = coordinateSpace;
    payload.feature = feature.raw;
    return payload;
  }

  function visualizationMapFeatures(spec) {
    const object = spec && typeof spec === "object" && !Array.isArray(spec) ? spec : {};
    const source = Array.isArray(object.features) ? object.features : [];
    const coordinateSpace = visualizationString(object.coordinateSpace || "geospatial").toLowerCase() === "planar"
      ? "planar"
      : "geospatial";
    return source.map((entry, index) => {
      if (!entry || typeof entry !== "object" || Array.isArray(entry)) {
        return null;
      }
      const geometry = entry.geometry && typeof entry.geometry === "object" && !Array.isArray(entry.geometry)
        ? entry.geometry
        : {};
      const type = visualizationString(geometry.type || geometry.kind).toLowerCase();
      const rawCoordinates = geometry.coordinates;
      let coordinates = null;
      if (type === "point") {
        coordinates = visualizationMapCoordinate(rawCoordinates);
      } else if (type === "polyline" || type === "polygon") {
        coordinates = Array.isArray(rawCoordinates)
          ? rawCoordinates.map(visualizationMapCoordinate).filter(Boolean)
          : null;
      }
      if (!type || !coordinates || (Array.isArray(coordinates) && coordinates.length === 0)) {
        return null;
      }
      const feature = {
        id: visualizationString(entry.id) || `feature-${index}`,
        label: visualizationString(entry.label || entry.title || entry.name || entry.id) || `Feature ${index + 1}`,
        selectable: entry.selectable !== false,
        style: visualizationMapStyle(entry.style),
        geometryType: type,
        coordinates,
        raw: entry,
      };
      feature.payload = buildVisualizationMapFeaturePayload(feature, coordinateSpace);
      return feature;
    }).filter(Boolean);
  }

  function visualizationMapSpec(spec) {
    const object = spec && typeof spec === "object" && !Array.isArray(spec) ? spec : {};
    return {
      coordinateSpace: visualizationString(object.coordinateSpace || "geospatial").toLowerCase() === "planar"
        ? "planar"
        : "geospatial",
      base: visualizationMapBase(object.base),
      viewport: visualizationMapViewport(object.viewport),
      fit: visualizationString(object.fit || "fitFeatures") || "fitFeatures",
      revision: visualizationString(object.revision),
      features: visualizationMapFeatures(object),
    };
  }

  function visualizationMapSceneSignature(spec) {
    const normalized = visualizationMapSpec(spec);
    if (normalized.revision) {
      return `revision:${normalized.revision}`;
    }
    return safeJSONStringify({
      coordinateSpace: normalized.coordinateSpace,
      base: normalized.base,
      viewport: normalized.viewport,
      fit: normalized.fit,
      features: normalized.features.map((feature) => ({
        id: feature.id,
        geometryType: feature.geometryType,
        coordinates: feature.coordinates,
        style: feature.style,
        selectable: feature.selectable,
      })),
    });
  }

  function visualizationMapSelectionSignature(selection) {
    return safeJSONStringify({
      selectedID: selection.selectedID || "",
      selectedIndex: Number.isInteger(selection.selectedIndex) ? selection.selectedIndex : null,
      selectedIDs: Array.from(selection.selectedIDs || []).sort(),
    });
  }

  function visualizationMapBindingSignature(spec, stateValue) {
    return safeJSONStringify({
      scene: visualizationMapSceneSignature(spec),
      selection: visualizationMapSelectionSignature(normalizeVisualizationSelection(stateValue)),
    });
  }

  function normalizeVisualizationSelection(stateValue) {
    const selection = {
      selectedID: "",
      selectedIndex: null,
      selectedIDs: new Set(),
    };

    if (Number.isInteger(stateValue)) {
      selection.selectedIndex = stateValue;
      return selection;
    }
    if (typeof stateValue === "string" && stateValue.trim()) {
      selection.selectedID = stateValue.trim();
      return selection;
    }
    if (Array.isArray(stateValue)) {
      stateValue.forEach((entry) => {
        const id = visualizationString(entry);
        if (id) {
          selection.selectedIDs.add(id);
        }
      });
      return selection;
    }
    if (stateValue && typeof stateValue === "object") {
      selection.selectedID = visualizationString(stateValue.selectedID || stateValue.id || stateValue.activeID);
      if (Number.isInteger(stateValue.selectedIndex)) {
        selection.selectedIndex = stateValue.selectedIndex;
      } else if (Number.isInteger(stateValue.index)) {
        selection.selectedIndex = stateValue.index;
      }
      if (Array.isArray(stateValue.selectedIDs)) {
        stateValue.selectedIDs.forEach((entry) => {
          const id = visualizationString(entry);
          if (id) {
            selection.selectedIDs.add(id);
          }
        });
      }
    }
    return selection;
  }

  function visualizationSelectionContains(selection, id, index) {
    if (Number.isInteger(selection.selectedIndex) && selection.selectedIndex === index) {
      return true;
    }
    if (id && selection.selectedID === id) {
      return true;
    }
    return Boolean(id && selection.selectedIDs.has(id));
  }

  function buildVisualizationPayload(kind, interaction, item, index, id, label) {
    const payload = {
      trigger: "visualization",
      visualizationKind: kind,
      interaction,
      index,
      item,
    };
    if (id) {
      payload.id = id;
    }
    if (label) {
      payload.label = label;
    }
    if (interaction === "row") {
      payload.row = item;
    } else if (interaction === "point") {
      payload.point = item;
    } else if (interaction === "node") {
      payload.node = item;
    } else if (interaction === "feature") {
      payload.feature = item;
    } else if (interaction === "occurrence") {
      payload.occurrence = item;
    } else if (interaction === "timeline" || interaction === "gantt") {
      payload.timelineItem = item;
    }
    if (item && typeof item === "object" && !Array.isArray(item) && Object.prototype.hasOwnProperty.call(item, "value")) {
      payload.value = item.value;
    }
    if (interaction === "feature" && item && typeof item === "object" && !Array.isArray(item) && typeof item.coordinateSpace === "string") {
      payload.coordinateSpace = item.coordinateSpace;
    }
    return payload;
  }

  function dispatchVisualizationInteraction(runtimeState, binding, interaction, item, index, id, label) {
    if (!binding.actionKeypath) {
      return;
    }
    void dispatchAction(
      runtimeState,
      binding.actionKeypath,
      buildVisualizationPayload(binding.kind, interaction, item, index, id, label),
      {
        trigger: "visualization",
        interaction,
        context: binding.context,
      }
    );
  }

  function renderVisualizationBinding(binding, runtimeState, spec, stateValue) {
    const body = binding.body;
    if (!(body instanceof HTMLElement)) {
      return;
    }

    const kind = String(binding.kind || "table").trim().toLowerCase();
    if (kind === "richdocument" || kind === "documentchat" || kind === "documenthelp") {
      const documentId = spec && spec.schema === "haven.document.v1" ? spec.documentId : null;
      if (documentId && binding.documentId && documentId !== binding.documentId && binding.documentController) {
        // A reference can change while its Skeleton stays identical. Keep the
        // old tab draft under its own document ID and start from the new current.
        binding.documentController.destroy();
        binding.documentController = null;
        body.replaceChildren();
      }
      if (documentId) binding.documentId = documentId;
      if (!binding.documentController) {
        if (!window.HavenRichDocument) {
          binding.documentSnapshot = spec;
          body.textContent = "Laster dokumentverktøy …";
          if (!window.havenDocumentRuntimePromise) {
            window.havenDocumentRuntimePromise = new Promise((resolve, reject) => {
              const script = document.createElement("script");
              script.src = "/js/haven-rich-document.js";
              script.onload = resolve; script.onerror = reject;
              document.head.appendChild(script);
            });
          }
          if (!binding.documentLoading) {
            binding.documentLoading = true;
            window.havenDocumentRuntimePromise.then(() => {
              if (body.isConnected) { body.replaceChildren(); renderVisualizationBinding(binding, runtimeState, binding.documentSnapshot, null); }
            }).catch(() => { body.textContent = "Dokumentverktøyet kunne ikke lastes. Last siden på nytt."; });
          }
          return;
        }
        binding.documentController = window.HavenRichDocument.mount(body, {
          chatOnly: kind === "documentchat",
          helpOnly: kind === "documenthelp",
          send: (payload) => dispatchAction(runtimeState, binding.actionKeypath, payload, { trigger: "document", context: binding.context }),
        });
      }
      binding.documentController.update(spec);
      return;
    }
    const selection = normalizeVisualizationSelection(stateValue);
    if (kind === "map") {
      renderVisualizationMap(binding, runtimeState, spec, selection);
      return;
    }
    disposeVisualizationBinding(binding);
    body.innerHTML = "";
    if (kind === "table") {
      renderVisualizationTable(binding, runtimeState, spec, selection);
      return;
    }
    if (kind === "chart") {
      renderVisualizationChart(binding, runtimeState, spec, selection);
      return;
    }
    if (kind === "network" || kind === "graph") {
      renderVisualizationNetwork(binding, runtimeState, spec, selection);
      return;
    }
    if (kind === "calendar") {
      renderVisualizationCalendar(binding, runtimeState, spec, selection);
      return;
    }
    if (kind === "timeline" || kind === "gantt") {
      renderVisualizationTimeline(binding, runtimeState, spec, selection, kind);
      return;
    }
    body.appendChild(renderVisualizationFallback(`Visualization kind '${binding.kind}' is not supported yet.`));
  }

  function renderVisualizationFallback(message) {
    const node = document.createElement("div");
    node.className = "skeleton-visualization-fallback";
    node.textContent = message;
    return node;
  }

  function visualizationCalendarSpec(spec) {
    const object = spec && typeof spec === "object" && !Array.isArray(spec) ? spec : {};
    const range = object.range && typeof object.range === "object" && !Array.isArray(object.range) ? object.range : {};
    const fallback = object.fallback && typeof object.fallback === "object" && !Array.isArray(object.fallback) ? object.fallback : {};
    const occurrences = Array.isArray(object.occurrences)
      ? object.occurrences
      : (Array.isArray(object.items) ? object.items : (Array.isArray(fallback.items) ? fallback.items : visualizationRows(object)));
    return {
      schema: visualizationString(object.schema || "haven.calendar.visualization.v1"),
      view: visualizationString(object.view || "agenda").toLowerCase() || "agenda",
      timezone: visualizationString(object.timezone || "UTC") || "UTC",
      range: {
        startAt: visualizationString(range.startAt || range.start || object.startAt),
        endAt: visualizationString(range.endAt || range.end || object.endAt),
      },
      display: object.display && typeof object.display === "object" && !Array.isArray(object.display) ? object.display : {},
      fallback,
      occurrences: occurrences.map(visualizationCalendarOccurrence).filter(Boolean),
    };
  }

  function visualizationCalendarOccurrence(value, index) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      return null;
    }
    const item = value.item && typeof value.item === "object" && !Array.isArray(value.item) ? value.item : {};
    const time = item.time && typeof item.time === "object" && !Array.isArray(item.time) ? item.time : {};
    const startAt = visualizationString(value.startAt || time.startAt || value.startsAt || time.startsAt);
    if (!startAt) {
      return null;
    }
    const endAt = visualizationString(value.endAt || time.endAt || value.endsAt || time.endsAt);
    const title = visualizationString(value.title || item.title || item.summary) || "Untitled";
    const id = visualizationString(value.id || value.occurrenceId || item.id || item.uid) || `occurrence-${index}`;
    return {
      id,
      itemId: visualizationString(value.itemId || item.id),
      uid: visualizationString(value.uid || item.uid),
      title,
      startAt,
      endAt,
      timezone: visualizationString(value.timezone || time.timezone),
      isAllDay: value.isAllDay === true || time.isAllDay === true,
      status: visualizationString(value.status || item.status),
      availability: visualizationString(value.availability || item.availability),
      locationSummary: visualizationString(value.locationSummary || (item.location && (item.location.name || item.location.address))),
      raw: value,
      startMs: visualizationDateMs(startAt),
      endMs: visualizationDateMs(endAt),
    };
  }

  function visualizationDateMs(value) {
    const text = visualizationString(value);
    if (!text) {
      return NaN;
    }
    const parsed = Date.parse(text);
    if (Number.isFinite(parsed)) {
      return parsed;
    }
    const dateOnly = text.match(/^(\d{4})-(\d{2})-(\d{2})$/);
    if (dateOnly) {
      return Date.UTC(Number(dateOnly[1]), Number(dateOnly[2]) - 1, Number(dateOnly[3]));
    }
    return NaN;
  }

  function visualizationCalendarDateLabel(value, timezone, options) {
    const ms = typeof value === "number" ? value : visualizationDateMs(value);
    if (!Number.isFinite(ms)) {
      return visualizationString(value);
    }
    try {
      return new Intl.DateTimeFormat(undefined, {
        timeZone: timezone || undefined,
        ...options,
      }).format(new Date(ms));
    } catch {
      return new Date(ms).toLocaleString();
    }
  }

  function renderVisualizationCalendar(binding, runtimeState, spec, selection) {
    const body = binding.body;
    const calendarSpec = visualizationCalendarSpec(spec);
    const occurrences = calendarSpec.occurrences;
    if (!occurrences.length) {
      body.appendChild(renderVisualizationFallback(calendarSpec.display.emptyMessage || "Ingen kalenderoppføringer ennå."));
      return;
    }

    const host = document.createElement("div");
    host.className = "skeleton-visualization-calendar";
    host.style.display = "grid";
    host.style.gap = "10px";
    host.style.minWidth = "0";

    const header = document.createElement("div");
    header.style.display = "flex";
    header.style.justifyContent = "space-between";
    header.style.alignItems = "baseline";
    header.style.gap = "12px";

    const title = document.createElement("div");
    title.textContent = calendarSpec.display.title || `${calendarSpec.view.charAt(0).toUpperCase()}${calendarSpec.view.slice(1)} calendar`;
    title.style.fontWeight = "700";
    title.style.fontSize = "14px";
    header.appendChild(title);

    const range = document.createElement("div");
    range.textContent = calendarSpec.range.startAt && calendarSpec.range.endAt
      ? `${visualizationCalendarDateLabel(calendarSpec.range.startAt, calendarSpec.timezone, { month: "short", day: "numeric" })} - ${visualizationCalendarDateLabel(calendarSpec.range.endAt, calendarSpec.timezone, { month: "short", day: "numeric" })}`
      : calendarSpec.timezone;
    range.style.fontSize = "12px";
    range.style.color = "#64748B";
    header.appendChild(range);
    host.appendChild(header);

    const grouped = calendarSpec.view === "month"
      ? visualizationCalendarGroupByDay(occurrences, calendarSpec.timezone)
      : [{ id: "__all", label: "", occurrences }];

    grouped.forEach((group) => {
      if (group.label) {
        const dayLabel = document.createElement("div");
        dayLabel.textContent = group.label;
        dayLabel.style.fontSize = "12px";
        dayLabel.style.fontWeight = "700";
        dayLabel.style.color = "#475569";
        dayLabel.style.marginTop = "4px";
        host.appendChild(dayLabel);
      }
      const list = document.createElement("div");
      list.style.display = "grid";
      list.style.gap = calendarSpec.view === "day" ? "8px" : "6px";
      group.occurrences.forEach((occurrence, index) => {
        const absoluteIndex = occurrences.indexOf(occurrence);
        list.appendChild(renderVisualizationCalendarOccurrenceNode(binding, runtimeState, occurrence, Number.isInteger(absoluteIndex) ? absoluteIndex : index, selection, calendarSpec));
      });
      host.appendChild(list);
    });

    body.appendChild(host);
  }

  function visualizationCalendarGroupByDay(occurrences, timezone) {
    const groups = new Map();
    occurrences.forEach((occurrence) => {
      const label = visualizationCalendarDateLabel(occurrence.startMs, timezone, { weekday: "short", month: "short", day: "numeric" });
      if (!groups.has(label)) {
        groups.set(label, []);
      }
      groups.get(label).push(occurrence);
    });
    return Array.from(groups.entries()).map(([label, items]) => ({
      id: label,
      label,
      occurrences: items,
    }));
  }

  function renderVisualizationCalendarOccurrenceNode(binding, runtimeState, occurrence, index, selection, calendarSpec) {
    const isSelected = visualizationSelectionContains(selection, occurrence.id, index);
    const node = binding.actionKeypath ? document.createElement("button") : document.createElement("div");
    if (node instanceof HTMLButtonElement) {
      node.type = "button";
      node.style.border = "0";
      node.style.cursor = "pointer";
    }
    node.className = "skeleton-visualization-calendar-occurrence";
    node.style.display = "grid";
    node.style.gridTemplateColumns = calendarSpec.view === "timeline" ? "minmax(84px, 0.28fr) minmax(0, 1fr)" : "minmax(72px, 0.22fr) minmax(0, 1fr)";
    node.style.gap = "10px";
    node.style.alignItems = "start";
    node.style.width = "100%";
    node.style.padding = "10px";
    node.style.borderRadius = "8px";
    node.style.textAlign = "left";
    node.style.background = isSelected ? "rgba(37, 99, 235, 0.12)" : "rgba(248, 250, 252, 0.92)";
    node.style.color = "#0F172A";
    node.style.border = isSelected ? "1px solid rgba(37, 99, 235, 0.35)" : "1px solid rgba(148, 163, 184, 0.28)";

    const time = document.createElement("div");
    time.textContent = occurrence.isAllDay
      ? "All day"
      : visualizationCalendarTimeRange(occurrence, calendarSpec.timezone);
    time.style.fontSize = "12px";
    time.style.fontWeight = "700";
    time.style.color = "#2563EB";
    node.appendChild(time);

    const content = document.createElement("div");
    content.style.display = "grid";
    content.style.gap = "3px";
    content.style.minWidth = "0";

    const title = document.createElement("div");
    title.textContent = occurrence.title;
    title.style.fontSize = "13px";
    title.style.fontWeight = "700";
    title.style.overflow = "hidden";
    title.style.textOverflow = "ellipsis";
    title.style.whiteSpace = "nowrap";
    content.appendChild(title);

    const metaParts = [occurrence.locationSummary, occurrence.status, occurrence.availability].filter(Boolean);
    if (metaParts.length) {
      const meta = document.createElement("div");
      meta.textContent = metaParts.join(" · ");
      meta.style.fontSize = "12px";
      meta.style.color = "#64748B";
      meta.style.overflow = "hidden";
      meta.style.textOverflow = "ellipsis";
      meta.style.whiteSpace = "nowrap";
      content.appendChild(meta);
    }
    node.appendChild(content);

    if (binding.actionKeypath) {
      node.addEventListener("click", () => {
        dispatchVisualizationInteraction(runtimeState, binding, "occurrence", occurrence.raw, index, occurrence.id, occurrence.title);
      });
    }
    return node;
  }

  function visualizationCalendarTimeRange(occurrence, timezone) {
    const start = visualizationCalendarDateLabel(occurrence.startMs, timezone, { hour: "2-digit", minute: "2-digit" });
    if (!Number.isFinite(occurrence.endMs)) {
      return start;
    }
    const end = visualizationCalendarDateLabel(occurrence.endMs, timezone, { hour: "2-digit", minute: "2-digit" });
    return `${start} - ${end}`;
  }

  function renderVisualizationTable(binding, runtimeState, spec, selection) {
    const body = binding.body;
    const rows = visualizationRows(spec);
    const columns = visualizationColumns(spec);
    if (!rows.length) {
      body.appendChild(renderVisualizationFallback("Ingen rader ennå."));
      return;
    }
    if (columns.length > 4 && typeof window !== "undefined" && window.matchMedia("(max-width: 520px)").matches) {
      renderVisualizationStackedTable(binding, runtimeState, rows, columns, selection);
      return;
    }

    const scroller = document.createElement("div");
    scroller.className = "skeleton-visualization-table-scroll";

    const gridColumns = `repeat(${columns.length}, minmax(0, 1fr))`;

    const table = document.createElement("div");
    table.className = "skeleton-visualization-table";
    const accessibleLabel = binding.accessibilityLabel || visualizationString(spec.title || spec.label);
    if (accessibleLabel) {
      table.setAttribute("role", binding.actionKeypath ? "region" : "table");
      table.setAttribute("aria-label", accessibleLabel);
    }

    const header = document.createElement("div");
    header.className = "skeleton-visualization-table-header";
    if (!binding.actionKeypath && accessibleLabel) {
      header.setAttribute("role", "row");
    }
    header.style.gridTemplateColumns = gridColumns;
    columns.forEach((column) => {
      const label = document.createElement("div");
      label.className = "skeleton-visualization-table-heading";
      if (!binding.actionKeypath && accessibleLabel) {
        label.setAttribute("role", "columnheader");
      }
      label.textContent = column.label;
      // Justeringen kommer fra spesifikasjonen; utseendet fra stilarket.
      label.dataset.align = column.align === "trailing" ? "trailing"
        : (column.align === "center" ? "center" : "leading");
      header.appendChild(label);
    });
    table.appendChild(header);

    rows.forEach((row, index) => {
      const rowID = row && typeof row === "object" && !Array.isArray(row) ? visualizationString(row.id) : `row-${index}`;
      const rowLabel = row && typeof row === "object" && !Array.isArray(row) ? visualizationString(row.label) : "";
      const isSelected = visualizationSelectionContains(selection, rowID, index);
      const rowNode = binding.actionKeypath ? document.createElement("button") : document.createElement("div");
      rowNode.className = "skeleton-visualization-table-row";
      if (rowNode instanceof HTMLButtonElement) {
        rowNode.type = "button";
        rowNode.classList.add("is-actionable");
      } else if (accessibleLabel) {
        rowNode.setAttribute("role", "row");
      }
      rowNode.classList.toggle("is-selected", Boolean(isSelected));
      rowNode.style.gridTemplateColumns = gridColumns;

      columns.forEach((column) => {
        const cell = document.createElement("div");
        cell.className = "skeleton-visualization-table-cell";
        if (!binding.actionKeypath && accessibleLabel) {
          cell.setAttribute("role", "cell");
        }
        cell.textContent = visualizationDisplay(visualizationCellValue(row, column));
        cell.dataset.align = column.align === "trailing" ? "trailing"
          : (column.align === "center" ? "center" : "leading");
        rowNode.appendChild(cell);
      });

      if (binding.actionKeypath) {
        rowNode.addEventListener("click", () => {
          dispatchVisualizationInteraction(runtimeState, binding, "row", row, index, rowID || `row-${index}`, rowLabel);
        });
      }
      table.appendChild(rowNode);
      if (index < rows.length - 1) {
        const divider = document.createElement("div");
        if (accessibleLabel) {
          divider.setAttribute("role", "presentation");
        }
        divider.style.height = "1px";
        divider.style.background = "rgba(255, 255, 255, 0.08)";
        table.appendChild(divider);
      }
    });

    scroller.appendChild(table);
    body.appendChild(scroller);
  }

  function renderVisualizationStackedTable(binding, runtimeState, rows, columns, selection) {
    const body = binding.body;
    const stack = document.createElement("div");
    stack.className = "skeleton-visualization-table-stacked";
    stack.style.display = "grid";
    stack.style.gap = "8px";

    rows.forEach((row, index) => {
      const rowObject = row && typeof row === "object" && !Array.isArray(row) ? row : null;
      const rowID = rowObject ? visualizationString(rowObject.id) : `row-${index}`;
      const rowLabel = rowObject ? visualizationString(rowObject.label || rowObject.project || rowObject.title || rowObject.name) : `Row ${index + 1}`;
      const isSelected = visualizationSelectionContains(selection, rowID, index);
      const rowNode = binding.actionKeypath ? document.createElement("button") : document.createElement("div");
      rowNode.className = "skeleton-visualization-table-card";
      if (rowNode instanceof HTMLButtonElement) {
        rowNode.type = "button";
        rowNode.style.border = "0";
        rowNode.style.cursor = "pointer";
      }
      rowNode.style.display = "grid";
      rowNode.style.gap = "6px";
      rowNode.style.width = "100%";
      rowNode.style.padding = "10px";
      rowNode.style.borderRadius = "8px";
      rowNode.style.textAlign = "left";
      rowNode.style.background = isSelected ? "rgba(44,143,136,0.18)" : "rgba(22,42,58,0.78)";
      rowNode.style.color = "#EAF7F8";

      const title = document.createElement("div");
      title.textContent = rowLabel || `Row ${index + 1}`;
      title.style.fontSize = "13px";
      title.style.fontWeight = "700";
      title.style.overflow = "hidden";
      title.style.textOverflow = "ellipsis";
      title.style.whiteSpace = "nowrap";
      rowNode.appendChild(title);

      columns.forEach((column) => {
        const value = visualizationDisplay(visualizationCellValue(row, column));
        if (!value) {
          return;
        }
        const pair = document.createElement("div");
        pair.style.display = "grid";
        pair.style.gridTemplateColumns = "88px minmax(0, 1fr)";
        pair.style.gap = "8px";
        pair.style.alignItems = "baseline";

        const key = document.createElement("div");
        key.textContent = column.label;
        key.style.fontSize = "11px";
        key.style.fontWeight = "700";
        key.style.color = "#9AC4CF";
        key.style.overflow = "hidden";
        key.style.textOverflow = "ellipsis";
        key.style.whiteSpace = "nowrap";
        pair.appendChild(key);

        const valueNode = document.createElement("div");
        valueNode.textContent = value;
        valueNode.style.fontSize = "12px";
        valueNode.style.color = "#EAF7F8";
        valueNode.style.overflowWrap = "anywhere";
        pair.appendChild(valueNode);
        rowNode.appendChild(pair);
      });

      if (binding.actionKeypath) {
        rowNode.addEventListener("click", () => {
          dispatchVisualizationInteraction(runtimeState, binding, "row", row, index, rowID || `row-${index}`, rowLabel);
        });
      }
      stack.appendChild(rowNode);
    });

    body.appendChild(stack);
  }

  function renderVisualizationChart(binding, runtimeState, spec, selection) {
    const body = binding.body;
    const points = visualizationChartPoints(spec);
    if (!points.length) {
      body.appendChild(renderVisualizationFallback("Ingen datapunkter ennå."));
      return;
    }

    const style = visualizationChartStyle(spec);
    if (style === "line" && points.length > 1) {
      renderVisualizationLineChart(binding, runtimeState, spec, points, selection);
      return;
    }

    const maxValue = Math.max(...points.map((point) => point.value), 1);
    const chart = document.createElement("div");
    const accessibleLabel = binding.accessibilityLabel || visualizationString(spec.title || spec.label);
    if (accessibleLabel && !binding.actionKeypath) {
      chart.setAttribute("role", "img");
      chart.setAttribute("aria-label", `${accessibleLabel}: ${points.map((point) => `${point.label} ${point.value}`).join(", ")}`);
    } else if (accessibleLabel) {
      chart.setAttribute("role", "group");
      chart.setAttribute("aria-label", accessibleLabel);
    }
    chart.className = "skeleton-visualization-bars";

    points.forEach((point, index) => {
      const isSelected = visualizationSelectionContains(selection, point.id, index);
      const column = document.createElement("div");
      column.className = "skeleton-visualization-bar-column";
      column.classList.toggle("is-actionable", Boolean(binding.actionKeypath));

      const bar = document.createElement("div");
      bar.className = "skeleton-visualization-bar";
      bar.classList.toggle("is-selected", Boolean(isSelected));
      // Hoyden er data; alt annet er stilark.
      bar.style.height = `${Math.max(2, (point.value / maxValue) * 100)}%`;
      if (point.color) {
        bar.style.background = point.color;
      }
      // En soyle uten tall er en form. Verdien staar paa den.
      bar.title = `${point.label}: ${point.value}`;
      column.appendChild(bar);

      const value = document.createElement("div");
      value.className = "skeleton-visualization-bar-value";
      value.textContent = formatAxisValue(point.value);
      column.appendChild(value);

      const label = document.createElement("div");
      label.className = "skeleton-visualization-bar-label";
      label.textContent = point.label;
      column.appendChild(label);

      if (binding.actionKeypath) {
        column.addEventListener("click", () => {
          dispatchVisualizationInteraction(runtimeState, binding, "point", point.raw, index, point.id, point.label);
        });
      }
      chart.appendChild(column);
    });

    body.appendChild(chart);
  }

  /// Runder en akseslutt opp til noe et menneske leser fort: 1, 2 eller 5
  /// ganger en tierpotens.
  function niceAxisBound(value) {
    if (!Number.isFinite(value) || value <= 0) {
      return 1;
    }
    const magnitude = Math.pow(10, Math.floor(Math.log10(value)));
    const normalised = value / magnitude;
    const step = normalised <= 1 ? 1 : normalised <= 2 ? 2 : normalised <= 5 ? 5 : 10;
    return step * magnitude;
  }

  function formatAxisValue(value) {
    const magnitude = Math.abs(value);
    if (magnitude >= 1000000) {
      return `${Math.round(value / 100000) / 10}M`;
    }
    if (magnitude >= 1000) {
      return `${Math.round(value / 100) / 10}k`;
    }
    return String(Math.round(value * 100) / 100);
  }

  function renderVisualizationLineChart(binding, runtimeState, spec, points, selection) {
    const body = binding.body;
    // Tegneflaten er bred fordi diagrammet ER bredt. Med viewBox 100 x 220 og
    // standard preserveAspectRatio ble innholdet skalert til å passe HOYDEN og
    // sentrert, så kurven brukte under en tiendedel av bredden mens
    // x-etikettene under lå utover hele. De to viste ikke det samme.
    const width = 1000;
    const height = 220;
    const padTop = 12;
    const padBottom = 28;
    const padLeft = 48;
    const padRight = 12;
    const plotWidth = width - padLeft - padRight;
    const plotHeight = height - padTop - padBottom;

    const values = points.map((point) => point.value);
    // Skalaen starter på null når alt er positivt: en akse som starter et
    // vilkårlig sted gjør en liten endring til et stup.
    const rawMax = Math.max(...values, 0);
    const rawMin = Math.min(...values, 0);
    const niceMax = niceAxisBound(rawMax);
    const niceMin = rawMin < 0 ? -niceAxisBound(-rawMin) : 0;
    const span = (niceMax - niceMin) || 1;

    const positions = points.map((point, index) => {
      const x = points.length === 1
        ? padLeft + plotWidth / 2
        : padLeft + (plotWidth * index / Math.max(points.length - 1, 1));
      const y = padTop + plotHeight * (1 - ((point.value - niceMin) / span));
      return { x, y };
    });

    const container = document.createElement("div");
    const accessibleLabel = binding.accessibilityLabel || visualizationString(spec.title || spec.label);
    if (accessibleLabel && !binding.actionKeypath) {
      container.setAttribute("role", "img");
      container.setAttribute("aria-label", `${accessibleLabel}: ${points.map((point) => `${point.label} ${point.value}`).join(", ")}`);
    } else if (accessibleLabel) {
      container.setAttribute("role", "group");
      container.setAttribute("aria-label", accessibleLabel);
    }
    container.style.position = "relative";
    container.style.height = `${height}px`;

    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("class", "skeleton-visualization-line");
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    svg.setAttribute("preserveAspectRatio", "none");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", String(height));

    // Rutenett og verdiakse. Uten dem svarer diagrammet på "endret det seg",
    // men ikke på "er dette utenfor det normale" - og det siste er
    // spørsmålet en operatør faktisk sitter med.
    const axisLabels = [];
    const ticks = 4;
    for (let index = 0; index <= ticks; index += 1) {
      const value = niceMin + (span * index / ticks);
      const y = padTop + plotHeight * (1 - (index / ticks));

      const line = document.createElementNS(svgNS, "line");
      line.setAttribute("class", "skeleton-visualization-gridline");
      line.setAttribute("x1", String(padLeft));
      line.setAttribute("x2", String(width - padRight));
      line.setAttribute("y1", String(y));
      line.setAttribute("y2", String(y));
      // preserveAspectRatio="none" strekker x, saa en linjebredde i
      // brukerenheter ville blitt bred. vector-effect holder den 1px.
      line.setAttribute("vector-effect", "non-scaling-stroke");
      svg.appendChild(line);

      // Etiketten tegnes som HTML, ikke som SVG-tekst: med
      // preserveAspectRatio="none" strekkes tekst sammen med x-aksen, og et
      // tall som er klemt sammen til halv bredde er ikke lenger et tall du
      // leser fort. Hoydeskalaen er 1:1 (height == viewBox-hoyde), saa
      // y i brukerenheter ER y i piksler.
      const label = document.createElement("div");
      label.className = "skeleton-visualization-axis-label";
      label.style.top = `${y}px`;
      label.style.width = `${padLeft - 8}px`;
      label.textContent = formatAxisValue(value);
      axisLabels.push(label);
    }

    // Flaten under kurven gjor det lettere aa se retningen paa avstand.
    if (positions.length > 1) {
      const area = document.createElementNS(svgNS, "polygon");
      area.setAttribute("class", "skeleton-visualization-area");
      const base = padTop + plotHeight;
      area.setAttribute("points", [
        `${positions[0].x},${base}`,
        ...positions.map((point) => `${point.x},${point.y}`),
        `${positions[positions.length - 1].x},${base}`,
      ].join(" "));
      svg.appendChild(area);
    }

    const polyline = document.createElementNS(svgNS, "polyline");
    polyline.setAttribute("class", "skeleton-visualization-line-path");
    polyline.setAttribute("fill", "none");
    polyline.setAttribute("vector-effect", "non-scaling-stroke");
    polyline.setAttribute("points", positions.map((point) => `${point.x},${point.y}`).join(" "));
    svg.appendChild(polyline);

    // Punktene tegnes som HTML, ikke som SVG-sirkler. I et strukket
    // koordinatsystem blir en sirkel en ellipse, og en ellipse ser ut som en
    // feil. Posisjonen er eksakt: x som prosent av tegneflaten, y i piksler
    // fordi hoydeskalaen er 1:1.
    const markers = points.map((point, index) => {
      const isSelected = visualizationSelectionContains(selection, point.id, index);
      const marker = document.createElement("div");
      marker.className = "skeleton-visualization-point";
      marker.classList.toggle("is-selected", Boolean(isSelected));
      marker.style.left = `${(positions[index].x / width) * 100}%`;
      marker.style.top = `${positions[index].y}px`;
      marker.title = `${point.label}: ${point.value}`;
      if (point.color) {
        marker.style.background = point.color;
      }
      if (binding.actionKeypath) {
        marker.classList.add("is-actionable");
        marker.addEventListener("click", () => {
          dispatchVisualizationInteraction(runtimeState, binding, "point", point.raw, index, point.id, point.label);
        });
      }
      return marker;
    });

    container.classList.add("skeleton-visualization-line-host");
    container.appendChild(svg);
    axisLabels.forEach((label) => container.appendChild(label));
    markers.forEach((marker) => container.appendChild(marker));

    const labels = document.createElement("div");
    labels.style.display = "flex";
    labels.style.justifyContent = "space-between";
    labels.style.marginTop = "-8px";
    labels.style.fontSize = "12px";
    points.forEach((point) => {
      const label = document.createElement("div");
      label.textContent = point.label;
      label.style.flex = "1 1 0";
      label.style.textAlign = "center";
      labels.appendChild(label);
    });

    body.appendChild(container);
    body.appendChild(labels);
  }

  function renderVisualizationNetwork(binding, runtimeState, spec, selection) {
    const body = binding.body;
    const nodes = visualizationGraphNodes(spec);
    const edges = visualizationGraphEdges(spec);
    if (!nodes.length) {
      body.appendChild(renderVisualizationFallback("Ingen noder ennå."));
      return;
    }

    const selectedID = binding.localSelectedID || selection.selectedID || visualizationString(spec && spec.selectedID);
    const selectedNode = nodes.find((node) => node.id === selectedID) || nodes[0];
    const positions = resolveVisualizationGraphPositions(nodes, edges, selectedNode ? selectedNode.id : "");
    const neighborIDs = new Set([selectedNode && selectedNode.id].filter(Boolean));
    edges.forEach((edge) => {
      if (selectedNode && (edge.source === selectedNode.id || edge.target === selectedNode.id)) {
        neighborIDs.add(edge.source);
        neighborIDs.add(edge.target);
      }
    });

    const container = document.createElement("div");
    container.className = "skeleton-visualization-graph-explorer";
    container.style.position = "relative";
    container.style.minHeight = "440px";
    container.style.overflow = "hidden";
    container.style.borderRadius = "14px";
    container.style.background = "radial-gradient(circle at 45% 45%, #24272b 0%, #17191c 54%, #111214 100%)";
    container.style.border = "1px solid rgba(255,255,255,0.1)";
    container.style.boxShadow = "inset 0 1px 0 rgba(255,255,255,0.08)";
    container.style.touchAction = "none";

    const toolbar = document.createElement("div");
    toolbar.className = "skeleton-visualization-graph-toolbar";
    toolbar.style.position = "absolute";
    toolbar.style.zIndex = "4";
    toolbar.style.top = "12px";
    toolbar.style.left = "12px";
    toolbar.style.right = "12px";
    toolbar.style.display = "flex";
    toolbar.style.alignItems = "center";
    toolbar.style.justifyContent = "space-between";
    toolbar.style.gap = "12px";
    toolbar.style.pointerEvents = "none";

    const title = document.createElement("div");
    title.style.color = "#F5F7FA";
    title.style.fontWeight = "700";
    title.style.fontSize = "13px";
    title.textContent = visualizationString(spec && (spec.title || spec.summaryText)) || `${nodes.length} nodes`;
    toolbar.appendChild(title);

    const groupStrip = document.createElement("div");
    groupStrip.style.display = "flex";
    groupStrip.style.flexWrap = "wrap";
    groupStrip.style.justifyContent = "flex-end";
    groupStrip.style.gap = "6px";
    const groups = Array.isArray(spec && spec.groups) ? spec.groups.slice(0, 5) : [];
    groups.forEach((group) => {
      const chip = document.createElement("span");
      chip.style.border = "1px solid rgba(255,255,255,0.12)";
      chip.style.borderRadius = "999px";
      chip.style.padding = "3px 8px";
      chip.style.color = "#C8D0D8";
      chip.style.background = "rgba(255,255,255,0.06)";
      chip.style.fontSize = "11px";
      chip.textContent = `${visualizationString(group.label || group.id)} ${visualizationString(group.count)}`;
      groupStrip.appendChild(chip);
    });
    toolbar.appendChild(groupStrip);
    container.appendChild(toolbar);

    const scene = document.createElement("div");
    scene.className = "skeleton-visualization-graph-scene";
    scene.style.position = "absolute";
    scene.style.inset = "0";
    scene.style.transformOrigin = "50% 50%";
    container.appendChild(scene);

    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("viewBox", "0 0 100 100");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.style.position = "absolute";
    svg.style.inset = "0";
    svg.style.overflow = "visible";

    const defs = document.createElementNS(svgNS, "defs");
    const marker = document.createElementNS(svgNS, "marker");
    marker.setAttribute("id", `graph-arrow-${Math.random().toString(36).slice(2)}`);
    marker.setAttribute("markerWidth", "6");
    marker.setAttribute("markerHeight", "6");
    marker.setAttribute("refX", "5");
    marker.setAttribute("refY", "3");
    marker.setAttribute("orient", "auto");
    const arrow = document.createElementNS(svgNS, "path");
    arrow.setAttribute("d", "M0,0 L6,3 L0,6 Z");
    arrow.setAttribute("fill", "rgba(188,196,204,0.65)");
    marker.appendChild(arrow);
    defs.appendChild(marker);
    svg.appendChild(defs);

    const selectedEdges = selectedNode ? edges.filter((edge) => edge.source === selectedNode.id || edge.target === selectedNode.id) : [];
    edges.forEach((edge) => {
      const source = positions[edge.source];
      const target = positions[edge.target];
      if (!source || !target) {
        return;
      }
      const isRelated = !selectedNode || edge.source === selectedNode.id || edge.target === selectedNode.id;
      const line = document.createElementNS(svgNS, "line");
      line.setAttribute("x1", String(source.x));
      line.setAttribute("y1", String(source.y));
      line.setAttribute("x2", String(target.x));
      line.setAttribute("y2", String(target.y));
      line.setAttribute("stroke", isRelated ? (edge.color || "rgba(210,216,222,0.62)") : "rgba(124,132,142,0.14)");
      line.setAttribute("stroke-width", isRelated ? "0.72" : "0.36");
      line.setAttribute("opacity", isRelated ? "0.72" : "0.22");
      line.setAttribute("marker-end", `url(#${marker.getAttribute("id")})`);
      svg.appendChild(line);
    });

    scene.appendChild(svg);

    const labeledKinds = new Set(["project", "workitem", "idea", "todo", "repo"]);
    let visibleRelatedLabels = 0;
    nodes.forEach((node, index) => {
      const isSelected = (selectedNode && selectedNode.id === node.id) || visualizationSelectionContains(selection, node.id, index);
      const isRelated = !selectedNode || neighborIDs.has(node.id);
      const position = positions[node.id] || { x: 50, y: 50 };
      const button = document.createElement("button");
      button.type = "button";
      button.className = "skeleton-visualization-graph-node";
      button.style.position = "absolute";
      button.style.left = `${position.x}%`;
      button.style.top = `${position.y}%`;
      button.style.transform = "translate(-50%, -50%)";
      button.style.border = "0";
      button.style.background = "transparent";
      button.style.cursor = binding.actionKeypath ? "pointer" : "default";
      button.style.display = "flex";
      button.style.flexDirection = "column";
      button.style.alignItems = "center";
      button.style.gap = "6px";
      button.style.opacity = isRelated ? "1" : "0.22";
      button.style.maxWidth = "120px";
      button.title = [node.label, node.subtitle].filter(Boolean).join(" · ");

      const dot = document.createElement("div");
      const radius = Number.isFinite(node.radius) ? node.radius : 5;
      const size = Math.max(8, Math.min(28, radius * (isSelected ? 3.1 : (isRelated ? 2.1 : 1.45))));
      dot.style.width = `${size}px`;
      dot.style.height = `${size}px`;
      dot.style.borderRadius = "999px";
      dot.style.background = node.color || (isSelected ? "#FFFFFF" : "#A8B0BA");
      dot.style.border = isSelected ? "3px solid rgba(255,255,255,0.95)" : "1.5px solid rgba(255,255,255,0.62)";
      dot.style.boxShadow = isSelected ? `0 0 0 8px ${node.color || "#FFFFFF"}33` : (isRelated ? "0 0 0 2px rgba(0,0,0,0.25)" : "none");
      button.appendChild(dot);

      const normalizedKind = String(node.kind || "").toLowerCase();
      const shouldShowLabel = isSelected
        || (isRelated && labeledKinds.has(normalizedKind) && visibleRelatedLabels < 26)
        || (!selectedNode && normalizedKind === "project" && visibleRelatedLabels < 12);
      if (shouldShowLabel) {
        visibleRelatedLabels += isSelected ? 0 : 1;
        const label = document.createElement("div");
        label.style.fontSize = isSelected ? "12px" : "10.5px";
        label.style.textAlign = "center";
        label.style.color = isSelected ? "#FFFFFF" : "#D7DEE5";
        label.style.textShadow = "0 1px 2px rgba(0,0,0,0.9)";
        label.style.lineHeight = "1.15";
        label.style.overflow = "hidden";
        label.style.display = "-webkit-box";
        label.style.webkitLineClamp = isSelected ? "2" : "1";
        label.style.webkitBoxOrient = "vertical";
        label.style.maxWidth = isSelected ? "160px" : "104px";
        label.style.padding = isSelected ? "3px 6px" : "2px 5px";
        label.style.borderRadius = "8px";
        label.style.background = isSelected ? "rgba(0,0,0,0.44)" : "rgba(0,0,0,0.32)";
        label.textContent = node.label;
        button.appendChild(label);
      }

      if (binding.actionKeypath) {
        button.addEventListener("click", () => {
          binding.localSelectedID = node.id;
          binding.lastSignature = null;
          renderVisualizationBinding(binding, runtimeState, spec, node.id);
          dispatchVisualizationInteraction(runtimeState, binding, "node", node.raw, index, node.id, node.label);
        });
      }
      scene.appendChild(button);
    });

    let graphZoom = Number.isFinite(binding.graphZoom) ? binding.graphZoom : 1;
    const graphPan = binding.graphPan && typeof binding.graphPan === "object" ? binding.graphPan : { x: 0, y: 0 };
    const applyTransform = () => {
      scene.style.transform = `translate(${graphPan.x}px, ${graphPan.y}px) scale(${graphZoom})`;
    };
    applyTransform();

    container.addEventListener("wheel", (event) => {
      event.preventDefault();
      const direction = event.deltaY > 0 ? -1 : 1;
      graphZoom = Math.max(0.55, Math.min(2.4, graphZoom + direction * 0.08));
      binding.graphZoom = graphZoom;
      binding.graphPan = graphPan;
      applyTransform();
    }, { passive: false });

    let dragStart = null;
    container.addEventListener("pointerdown", (event) => {
      if (event.target && event.target.closest && event.target.closest(".skeleton-visualization-graph-node")) {
        return;
      }
      dragStart = { x: event.clientX, y: event.clientY, panX: graphPan.x, panY: graphPan.y };
      container.setPointerCapture(event.pointerId);
      container.style.cursor = "grabbing";
    });
    container.addEventListener("pointermove", (event) => {
      if (!dragStart) {
        return;
      }
      graphPan.x = dragStart.panX + event.clientX - dragStart.x;
      graphPan.y = dragStart.panY + event.clientY - dragStart.y;
      binding.graphPan = graphPan;
      applyTransform();
    });
    container.addEventListener("pointerup", (event) => {
      dragStart = null;
      try { container.releasePointerCapture(event.pointerId); } catch (_) {}
      container.style.cursor = "";
    });

    const inspector = document.createElement("aside");
    inspector.className = "skeleton-visualization-graph-inspector";
    inspector.style.position = "absolute";
    inspector.style.right = "12px";
    inspector.style.bottom = "12px";
    inspector.style.zIndex = "4";
    inspector.style.width = "min(280px, calc(100% - 24px))";
    inspector.style.padding = "12px";
    inspector.style.borderRadius = "12px";
    inspector.style.background = "rgba(10,11,13,0.78)";
    inspector.style.border = "1px solid rgba(255,255,255,0.1)";
    inspector.style.backdropFilter = "blur(14px)";
    inspector.style.color = "#F5F7FA";
    inspector.innerHTML = "";
    const inspectorTitle = document.createElement("div");
    inspectorTitle.style.fontWeight = "700";
    inspectorTitle.style.fontSize = "14px";
    inspectorTitle.textContent = selectedNode ? selectedNode.label : "Graph";
    const inspectorMeta = document.createElement("div");
    inspectorMeta.style.marginTop = "4px";
    inspectorMeta.style.color = "#AEB7C1";
    inspectorMeta.style.fontSize = "12px";
    inspectorMeta.textContent = selectedNode ? `${selectedNode.kind || "node"} · ${selectedEdges.length} links` : `${nodes.length} nodes · ${edges.length} links`;
    inspector.appendChild(inspectorTitle);
    inspector.appendChild(inspectorMeta);
    container.appendChild(inspector);

    body.appendChild(container);
  }

  function renderVisualizationTimeline(binding, runtimeState, spec, selection, variant) {
    const body = binding.body;
    const items = visualizationTimelineItems(spec);
    const range = visualizationTimelineRange(items);
    if (!items.length || !range) {
      body.appendChild(renderVisualizationFallback(`No ${variant === "gantt" ? "Gantt" : "timeline"} items available yet.`));
      return;
    }

    const dated = items.filter((item) => Number.isFinite(item.startMs) && Number.isFinite(item.endMs));
    const undated = items.filter((item) => !Number.isFinite(item.startMs) || !Number.isFinite(item.endMs));

    const host = document.createElement("div");
    host.className = `skeleton-visualization-${variant}`;
    host.style.display = "grid";
    host.style.gap = "10px";
    host.style.minWidth = "0";

    const axis = document.createElement("div");
    axis.className = "skeleton-visualization-timeline-axis";
    axis.style.display = "grid";
    axis.style.gridTemplateColumns = "minmax(104px, 0.38fr) minmax(0, 1fr)";
    axis.style.gap = "12px";
    axis.style.alignItems = "center";

    const axisLabel = document.createElement("div");
    axisLabel.textContent = variant === "gantt" ? "Schedule" : "Timeline";
    axisLabel.style.fontSize = "12px";
    axisLabel.style.fontWeight = "700";
    axisLabel.style.color = "#9AC4CF";
    axis.appendChild(axisLabel);

    const ticks = document.createElement("div");
    ticks.style.position = "relative";
    ticks.style.height = "22px";
    ticks.style.borderBottom = "1px solid rgba(90,107,117,0.22)";
    const tickCount = 2;
    for (let index = 0; index < tickCount; index += 1) {
      const ms = range.min + (range.span * index / Math.max(tickCount - 1, 1));
      const tick = document.createElement("div");
      tick.style.position = "absolute";
      tick.style.left = `${index === tickCount - 1 ? 100 : (index * 100 / Math.max(tickCount - 1, 1))}%`;
      tick.style.transform = index === tickCount - 1 ? "translateX(-100%)" : "none";
      tick.style.fontSize = "11px";
      tick.style.color = "#9AC4CF";
      tick.textContent = visualizationDateLabel(ms);
      ticks.appendChild(tick);
    }
    axis.appendChild(ticks);
    host.appendChild(axis);

    const groups = variant === "gantt" ? visualizationTimelineGroups(dated) : [{ id: "__timeline", label: "", target: "", items: dated }];
    const showLaneHeaders = variant === "gantt" && groups.some((group) => group.id !== "__unassigned");

    const appendTimelineItem = (item, fallbackIndex) => {
      const itemIndex = Number.isInteger(item.index) ? item.index : fallbackIndex;
      const left = visualizationTimelinePosition(item.startMs, range);
      const right = visualizationTimelinePosition(item.endMs, range);
      const width = Math.max(variant === "gantt" ? 2.5 : 1.25, right - left);
      const isMilestone = Math.abs(item.endMs - item.startMs) < visualizationDayMs;
      const isSelected = visualizationSelectionContains(selection, item.id, itemIndex);
      const color = visualizationTimelineStatusColor(item);
      const row = binding.actionKeypath ? document.createElement("button") : document.createElement("div");
      row.className = "skeleton-visualization-timeline-item";
      if (row instanceof HTMLButtonElement) {
        row.type = "button";
        row.style.border = "0";
        row.style.cursor = "pointer";
      }
      row.style.display = "grid";
      row.style.gridTemplateColumns = "minmax(104px, 0.38fr) minmax(0, 1fr)";
      row.style.gap = "12px";
      row.style.alignItems = "center";
      row.style.width = "100%";
      row.style.padding = "8px 10px";
      row.style.borderRadius = "8px";
      row.style.textAlign = "left";
      row.style.background = isSelected ? "rgba(44,143,136,0.14)" : "rgba(15,23,42,0.025)";

      const label = document.createElement("div");
      label.style.minWidth = "0";
      const title = document.createElement("div");
      title.textContent = item.label;
      title.style.fontWeight = "700";
      title.style.fontSize = "13px";
      title.style.color = "#EAF7F8";
      title.style.whiteSpace = "nowrap";
      title.style.overflow = "hidden";
      title.style.textOverflow = "ellipsis";
      label.appendChild(title);
      const meta = document.createElement("div");
      meta.textContent = [item.dateRange, item.status, item.health, item.priority].filter(Boolean).join(" / ");
      meta.style.fontSize = "11px";
      meta.style.color = "#9AC4CF";
      meta.style.whiteSpace = "nowrap";
      meta.style.overflow = "hidden";
      meta.style.textOverflow = "ellipsis";
      label.appendChild(meta);
      row.appendChild(label);

      const track = document.createElement("div");
      track.className = "skeleton-visualization-timeline-track";
      track.style.position = "relative";
      track.style.height = "32px";
      track.style.borderRadius = "8px";
      track.style.background = "repeating-linear-gradient(90deg, rgba(90,107,117,0.12) 0, rgba(90,107,117,0.12) 1px, transparent 1px, transparent 25%)";

      const bar = document.createElement("div");
      bar.className = `skeleton-visualization-${variant}-bar`;
      bar.style.position = "absolute";
      bar.style.left = `${left}%`;
      bar.style.top = variant === "timeline" && isMilestone ? "10px" : "8px";
      bar.style.width = `${width}%`;
      bar.style.minWidth = variant === "timeline" && isMilestone ? "10px" : "22px";
      bar.style.height = variant === "timeline" && isMilestone ? "10px" : "16px";
      bar.style.borderRadius = variant === "timeline" && isMilestone ? "3px" : "999px";
      bar.style.transform = variant === "timeline" && isMilestone ? "translateX(-50%) rotate(45deg)" : "none";
      bar.style.background = color;
      bar.style.boxShadow = isSelected ? `0 0 0 3px ${color}33` : "none";
      track.appendChild(bar);

      if (item.milestoneLabel && variant === "gantt") {
        const milestone = document.createElement("div");
        milestone.className = "skeleton-visualization-gantt-milestone";
        milestone.title = item.milestoneLabel;
        milestone.style.position = "absolute";
        milestone.style.left = `${right}%`;
        milestone.style.top = "8px";
        milestone.style.width = "12px";
        milestone.style.height = "12px";
        milestone.style.borderRadius = "3px";
        milestone.style.transform = "translateX(-50%) rotate(45deg)";
        milestone.style.background = "#F1B64A";
        milestone.style.border = "1px solid rgba(255,255,255,0.85)";
        track.appendChild(milestone);
      }

      row.appendChild(track);
      if (binding.actionKeypath) {
        row.addEventListener("click", () => {
          dispatchVisualizationInteraction(runtimeState, binding, variant, item.raw, itemIndex, item.id, item.label);
        });
      }
      host.appendChild(row);
    };

    groups.forEach((group) => {
      if (showLaneHeaders) {
        const lane = document.createElement("div");
        lane.className = "skeleton-visualization-gantt-lane";
        lane.style.display = "grid";
        lane.style.gridTemplateColumns = "minmax(104px, 0.38fr) minmax(0, 1fr)";
        lane.style.gap = "12px";
        lane.style.alignItems = "center";
        lane.style.padding = "4px 10px 0";

        const laneLabel = document.createElement("div");
        laneLabel.textContent = group.label;
        laneLabel.style.fontSize = "12px";
        laneLabel.style.fontWeight = "800";
        laneLabel.style.color = "#EAF7F8";
        laneLabel.style.whiteSpace = "nowrap";
        laneLabel.style.overflow = "hidden";
        laneLabel.style.textOverflow = "ellipsis";
        lane.appendChild(laneLabel);

        const laneTrack = document.createElement("div");
        laneTrack.style.display = "flex";
        laneTrack.style.alignItems = "center";
        laneTrack.style.gap = "8px";
        laneTrack.style.minWidth = "0";
        const laneLine = document.createElement("div");
        laneLine.style.height = "1px";
        laneLine.style.flex = "1 1 auto";
        laneLine.style.background = "rgba(154,196,207,0.22)";
        laneTrack.appendChild(laneLine);
        if (group.target) {
          const target = document.createElement("div");
          target.textContent = group.target;
          target.style.fontSize = "11px";
          target.style.color = "#9AC4CF";
          target.style.whiteSpace = "nowrap";
          laneTrack.appendChild(target);
        }
        lane.appendChild(laneTrack);
        host.appendChild(lane);
      }
      group.items.forEach(appendTimelineItem);
    });

    if (undated.length) {
      const undatedNode = document.createElement("div");
      undatedNode.className = "skeleton-visualization-timeline-undated";
      undatedNode.style.fontSize = "12px";
      undatedNode.style.color = "#9AC4CF";
      undatedNode.textContent = `${undated.length} undated item(s) hidden from ${variant}.`;
      host.appendChild(undatedNode);
    }

    body.appendChild(host);
  }

  function renderVisualizationMap(binding, runtimeState, spec, selection) {
    const body = binding.body;
    if (!(body instanceof HTMLElement)) {
      return;
    }

    const scene = visualizationMapSpec(spec);
    if (!scene.base && !scene.features.length) {
      disposeVisualizationBinding(binding);
      body.innerHTML = "";
      body.appendChild(renderVisualizationFallback("Ingen kartobjekter ennå."));
      return;
    }

    const sceneSignature = visualizationMapSceneSignature(spec);
    const selectionSignature = visualizationMapSelectionSignature(selection);
    if (binding.mapController && binding.mapController.sceneSignature === sceneSignature) {
      if (binding.mapController.selectionSignature !== selectionSignature) {
        binding.mapController.updateSelection(selection);
        binding.mapController.selectionSignature = selectionSignature;
      }
      return;
    }

    disposeVisualizationBinding(binding);
    body.innerHTML = "";
    const host = document.createElement("div");
    host.className = "skeleton-visualization-map";
    host.style.height = "300px";
    host.style.width = "100%";
    host.style.borderRadius = "12px";
    host.style.overflow = "hidden";
    host.style.background = "rgba(15, 23, 42, 0.04)";
    body.appendChild(host);

    const token = (binding.mapRenderToken || 0) + 1;
    binding.mapRenderToken = token;

    ensureLeafletRuntime().then((L) => {
      if (binding.mapRenderToken !== token || !(host instanceof HTMLElement)) {
        return;
      }
      const controller = createVisualizationLeafletMapController(L, host, scene, selection, {
        binding,
        runtimeState,
      });
      controller.sceneSignature = sceneSignature;
      controller.selectionSignature = selectionSignature;
      binding.mapController = controller;
    }).catch((error) => {
      if (binding.mapRenderToken !== token) {
        return;
      }
      body.innerHTML = "";
      body.appendChild(renderVisualizationFallback(error && error.message ? error.message : "Could not load map runtime."));
    });
  }

  function ensureLeafletRuntime() {
    if (global.L && typeof global.L.map === "function") {
      return Promise.resolve(global.L);
    }
    if (leafletRuntimePromise) {
      return leafletRuntimePromise;
    }
    leafletRuntimePromise = Promise.all([
      ensureStylesheet(LEAFLET_STYLESHEET_PATH, "haven-leaflet-css"),
      ensureScript(LEAFLET_SCRIPT_PATH, "haven-leaflet-js"),
    ]).then(() => {
      if (!global.L || typeof global.L.map !== "function") {
        throw new Error("Leaflet did not initialize.");
      }
      return global.L;
    });
    return leafletRuntimePromise;
  }

  function ensureStylesheet(href, id) {
    if (document.getElementById(id)) {
      return Promise.resolve();
    }
    return new Promise((resolve, reject) => {
      const link = document.createElement("link");
      link.id = id;
      link.rel = "stylesheet";
      link.href = href;
      link.onload = () => resolve();
      link.onerror = () => reject(new Error(`Could not load stylesheet '${href}'.`));
      document.head.appendChild(link);
    });
  }

  function ensureScript(src, id) {
    const existing = document.getElementById(id);
    if (existing && existing.dataset.loaded === "true") {
      return Promise.resolve();
    }
    if (existing) {
      return new Promise((resolve, reject) => {
        existing.addEventListener("load", () => resolve(), { once: true });
        existing.addEventListener("error", () => reject(new Error(`Could not load script '${src}'.`)), { once: true });
      });
    }
    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.id = id;
      script.src = src;
      script.defer = true;
      script.onload = () => {
        script.dataset.loaded = "true";
        resolve();
      };
      script.onerror = () => reject(new Error(`Could not load script '${src}'.`));
      document.head.appendChild(script);
    });
  }

  function createVisualizationLeafletMapController(L, host, scene, selection, context) {
    const map = L.map(host, {
      zoomControl: true,
      attributionControl: true,
      preferCanvas: true,
      crs: scene.coordinateSpace === "planar" ? L.CRS.Simple : L.CRS.EPSG3857,
    });

    const featureLayers = [];
    let baseLayer = null;
    let imageOverlay = null;

    if (scene.coordinateSpace === "planar" && scene.base && scene.base.kind === "image") {
      const bounds = leafletBoundsForPlanar(scene.base.bounds, L);
      imageOverlay = L.imageOverlay(scene.base.url, bounds, {
        opacity: Number.isFinite(scene.base.opacity) ? scene.base.opacity : 1,
      }).addTo(map);
      baseLayer = imageOverlay;
    } else if (scene.base && scene.base.kind === "tiles") {
      const tileOptions = {
        attribution: scene.base.attribution || "",
      };
      if (Number.isFinite(scene.base.minZoom)) {
        tileOptions.minZoom = scene.base.minZoom;
      }
      if (Number.isFinite(scene.base.maxZoom)) {
        tileOptions.maxZoom = scene.base.maxZoom;
      }
      if (Number.isFinite(scene.base.tileSize)) {
        tileOptions.tileSize = scene.base.tileSize;
      }
      if (Array.isArray(scene.base.subdomains) && scene.base.subdomains.length) {
        tileOptions.subdomains = scene.base.subdomains;
      }
      baseLayer = L.tileLayer(scene.base.urlTemplate, tileOptions).addTo(map);
    }

    scene.features.forEach((feature) => {
      const layer = createLeafletFeatureLayer(L, feature, scene.coordinateSpace);
      if (!layer) {
        return;
      }
      layer.__havenFeature = feature;
      if (feature.selectable && context.binding.actionKeypath) {
        layer.on("click", () => {
          dispatchVisualizationInteraction(
            context.runtimeState,
            context.binding,
            "feature",
            feature.payload,
            feature.index,
            feature.id,
            feature.label
          );
        });
      }
      layer.addTo(map);
      featureLayers.push(layer);
    });

    applyLeafletViewport(map, L, scene, featureLayers, imageOverlay);

    const controller = {
      map,
      baseLayer,
      imageOverlay,
      featureLayers,
      scene,
      updateSelection(nextSelection) {
        featureLayers.forEach((layer) => {
          const feature = layer.__havenFeature;
          if (!feature) {
            return;
          }
          const selected = visualizationSelectionContains(nextSelection, feature.id, feature.index);
          applyLeafletFeatureSelection(layer, feature, selected);
        });
      },
      destroy() {
        map.remove();
      },
      sceneSignature: "",
      selectionSignature: "",
    };
    controller.updateSelection(selection);
    return controller;
  }

  function leafletLatLngForCoordinate(L, coordinate, coordinateSpace) {
    if (!Array.isArray(coordinate) || coordinate.length < 2) {
      return null;
    }
    return coordinateSpace === "planar"
      ? L.latLng(coordinate[1], coordinate[0])
      : L.latLng(coordinate[1], coordinate[0]);
  }

  function leafletBoundsForPlanar(bounds, L) {
    return L.latLngBounds(
      L.latLng(bounds.minY, bounds.minX),
      L.latLng(bounds.maxY, bounds.maxX)
    );
  }

  function createLeafletFeatureLayer(L, feature, coordinateSpace) {
    const style = feature.style || {};
    if (feature.geometryType === "point") {
      const latLng = leafletLatLngForCoordinate(L, feature.coordinates, coordinateSpace);
      if (!latLng) {
        return null;
      }
      return L.circleMarker(latLng, {
        radius: Number.isFinite(style.radius) ? style.radius : 8,
        color: style.strokeColor || style.tintColor || "#FFFFFF",
        weight: Number.isFinite(style.strokeWidth) ? style.strokeWidth : 2,
        opacity: Number.isFinite(style.strokeOpacity) ? style.strokeOpacity : 1,
        fillColor: style.fillColor || style.tintColor || "#2563EB",
        fillOpacity: Number.isFinite(style.fillOpacity) ? style.fillOpacity : 0.9,
      });
    }
    const latLngs = Array.isArray(feature.coordinates)
      ? feature.coordinates.map((coordinate) => leafletLatLngForCoordinate(L, coordinate, coordinateSpace)).filter(Boolean)
      : [];
    if (!latLngs.length) {
      return null;
    }
    if (feature.geometryType === "polyline") {
      return L.polyline(latLngs, {
        color: style.strokeColor || style.tintColor || "#2563EB",
        weight: Number.isFinite(style.strokeWidth) ? style.strokeWidth : 3,
        opacity: Number.isFinite(style.strokeOpacity) ? style.strokeOpacity : 0.9,
      });
    }
    if (feature.geometryType === "polygon") {
      return L.polygon(latLngs, {
        color: style.strokeColor || style.tintColor || "#2563EB",
        weight: Number.isFinite(style.strokeWidth) ? style.strokeWidth : 2,
        opacity: Number.isFinite(style.strokeOpacity) ? style.strokeOpacity : 0.9,
        fillColor: style.fillColor || style.tintColor || "#38BDF8",
        fillOpacity: Number.isFinite(style.fillOpacity) ? style.fillOpacity : 0.2,
      });
    }
    return null;
  }

  function applyLeafletFeatureSelection(layer, feature, selected) {
    const style = feature.style || {};
    if (typeof layer.setStyle === "function") {
      const nextStyle = {};
      if (feature.geometryType === "point") {
        nextStyle.color = style.strokeColor || style.tintColor || "#FFFFFF";
        nextStyle.weight = (Number.isFinite(style.strokeWidth) ? style.strokeWidth : 2) + (selected ? 1 : 0);
        nextStyle.opacity = Number.isFinite(style.strokeOpacity) ? style.strokeOpacity : 1;
        nextStyle.fillColor = style.fillColor || style.tintColor || "#2563EB";
        nextStyle.fillOpacity = selected
          ? Math.min(1, (Number.isFinite(style.fillOpacity) ? style.fillOpacity : 0.9) + 0.1)
          : (Number.isFinite(style.fillOpacity) ? style.fillOpacity : 0.9);
      } else if (feature.geometryType === "polyline") {
        nextStyle.color = style.strokeColor || style.tintColor || "#2563EB";
        nextStyle.weight = (Number.isFinite(style.strokeWidth) ? style.strokeWidth : 3) + (selected ? 1 : 0);
        nextStyle.opacity = selected
          ? Math.min(1, (Number.isFinite(style.strokeOpacity) ? style.strokeOpacity : 0.9) + 0.05)
          : (Number.isFinite(style.strokeOpacity) ? style.strokeOpacity : 0.9);
      } else if (feature.geometryType === "polygon") {
        nextStyle.color = style.strokeColor || style.tintColor || "#2563EB";
        nextStyle.weight = (Number.isFinite(style.strokeWidth) ? style.strokeWidth : 2) + (selected ? 1 : 0);
        nextStyle.opacity = Number.isFinite(style.strokeOpacity) ? style.strokeOpacity : 0.9;
        nextStyle.fillColor = style.fillColor || style.tintColor || "#38BDF8";
        nextStyle.fillOpacity = selected
          ? Math.min(1, (Number.isFinite(style.fillOpacity) ? style.fillOpacity : 0.2) + 0.08)
          : (Number.isFinite(style.fillOpacity) ? style.fillOpacity : 0.2);
      }
      layer.setStyle(nextStyle);
    }
    if (feature.geometryType === "point" && typeof layer.setRadius === "function") {
      layer.setRadius((Number.isFinite(style.radius) ? style.radius : 8) + (selected ? 2 : 0));
    }
  }

  function applyLeafletViewport(map, L, scene, featureLayers, imageOverlay) {
    if (scene.viewport && scene.viewport.bounds) {
      map.fitBounds(boundsForScene(scene.viewport.bounds, scene.coordinateSpace, L), { padding: [24, 24] });
      return;
    }
    if (scene.viewport && Array.isArray(scene.viewport.center) && Number.isFinite(scene.viewport.zoom)) {
      const center = leafletLatLngForCoordinate(L, scene.viewport.center, scene.coordinateSpace);
      if (center) {
        map.setView(center, scene.viewport.zoom);
        return;
      }
    }

    if (scene.fit === "manual") {
      if (featureLayers.length === 0) {
        map.setView(scene.coordinateSpace === "planar" ? L.latLng(0, 0) : L.latLng(59.9139, 10.7522), scene.coordinateSpace === "planar" ? 0 : 4);
      }
      return;
    }

    if (scene.coordinateSpace === "planar" && imageOverlay && scene.base && scene.base.kind === "image") {
      map.fitBounds(leafletBoundsForPlanar(scene.base.bounds, L), { padding: [24, 24] });
      return;
    }

    if (featureLayers.length) {
      const group = L.featureGroup(featureLayers);
      map.fitBounds(group.getBounds(), { padding: [24, 24] });
      return;
    }

    map.setView(scene.coordinateSpace === "planar" ? L.latLng(0, 0) : L.latLng(59.9139, 10.7522), scene.coordinateSpace === "planar" ? 0 : 4);
  }

  function boundsForScene(bounds, coordinateSpace, L) {
    if (coordinateSpace === "planar") {
      return leafletBoundsForPlanar(bounds, L);
    }
    return L.latLngBounds(
      L.latLng(bounds.minY, bounds.minX),
      L.latLng(bounds.maxY, bounds.maxX)
    );
  }

  function resolveVisualizationGraphPositions(nodes, edges = [], selectedID = "") {
    const explicit = nodes.filter((node) => Number.isFinite(node.x) && Number.isFinite(node.y));
    if (explicit.length === nodes.length && nodes.length) {
      const maxX = Math.max(...explicit.map((node) => node.x), 1);
      const maxY = Math.max(...explicit.map((node) => node.y), 1);
      return Object.fromEntries(nodes.map((node) => [
        node.id,
        {
          x: maxX > 1 ? (node.x / maxX) * 100 : node.x * 100,
          y: maxY > 1 ? (node.y / maxY) * 100 : node.y * 100,
        },
      ]));
    }

    const byID = new Map(nodes.map((node) => [node.id, node]));
    const selectedNodeID = byID.has(selectedID)
      ? selectedID
      : (nodes.find((node) => node.id === "project-haven-main") || nodes.find((node) => String(node.kind || "").toLowerCase() === "project") || nodes[0] || {}).id;
    const positions = {};
    const relatedIDs = new Set(selectedNodeID ? [selectedNodeID] : []);
    edges.forEach((edge) => {
      if (!selectedNodeID) {
        return;
      }
      if (edge.source === selectedNodeID || edge.target === selectedNodeID) {
        relatedIDs.add(edge.source);
        relatedIDs.add(edge.target);
      }
    });

    const kindWeight = (kind) => {
      switch (String(kind || "").toLowerCase()) {
      case "project": return 0;
      case "workitem": return 1;
      case "idea": return 2;
      case "todo": return 3;
      case "repo": return 4;
      case "cell": return 5;
      case "label":
      case "tag": return 6;
      default: return 7;
      }
    };
    const sortNodes = (a, b) => {
      const weightDelta = kindWeight(a.kind) - kindWeight(b.kind);
      if (weightDelta !== 0) {
        return weightDelta;
      }
      return String(a.label || a.id).localeCompare(String(b.label || b.id), undefined, { sensitivity: "base" });
    };
    const clamp = (value) => Math.max(5, Math.min(95, value));
    const placePolar = (node, angle, radius, centerX = 50, centerY = 50) => {
      positions[node.id] = {
        x: clamp(centerX + Math.cos(angle - Math.PI / 2) * radius),
        y: clamp(centerY + Math.sin(angle - Math.PI / 2) * radius),
      };
    };

    if (selectedNodeID) {
      positions[selectedNodeID] = { x: 50, y: 50 };
    }

    const relatedNodes = nodes
      .filter((node) => node.id !== selectedNodeID && relatedIDs.has(node.id))
      .sort(sortNodes);
    relatedNodes.forEach((node, index) => {
      const ring = Math.floor(index / 22);
      const ringIndex = index % 22;
      const ringSize = Math.min(22, relatedNodes.length - ring * 22);
      const radius = 16 + ring * 8;
      const angle = (ringIndex / Math.max(ringSize, 1)) * Math.PI * 2 + ring * 0.24;
      placePolar(node, angle, radius);
    });

    const unrelatedNodes = nodes
      .filter((node) => positions[node.id] === undefined)
      .sort(sortNodes);
    const groups = new Map();
    unrelatedNodes.forEach((node) => {
      const group = String(node.group || node.kind || "node").toLowerCase();
      if (!groups.has(group)) {
        groups.set(group, []);
      }
      groups.get(group).push(node);
    });
    const groupEntries = Array.from(groups.entries()).sort((lhs, rhs) => {
      const lhsWeight = kindWeight(lhs[0]);
      const rhsWeight = kindWeight(rhs[0]);
      if (lhsWeight !== rhsWeight) {
        return lhsWeight - rhsWeight;
      }
      return rhs[1].length - lhs[1].length;
    });
    groupEntries.forEach(([group, groupNodes], groupIndex) => {
      const groupAngle = (groupIndex / Math.max(groupEntries.length, 1)) * Math.PI * 2;
      const groupRadius = selectedNodeID ? 38 : 30;
      const centerX = 50 + Math.cos(groupAngle - Math.PI / 2) * groupRadius;
      const centerY = 50 + Math.sin(groupAngle - Math.PI / 2) * groupRadius;
      groupNodes.forEach((node, index) => {
        const spiral = 4 + Math.floor(index / 10) * 3.2;
        const angle = (index * 2.399963229728653) + groupIndex * 0.35;
        positions[node.id] = {
          x: clamp(centerX + Math.cos(angle) * spiral),
          y: clamp(centerY + Math.sin(angle) * spiral),
        };
      });
    });

    return positions;
  }

  function renderObject(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const node = document.createElement("div");
    node.className = "skeleton-object";
    applySkeletonIdentity(node, key, path);
    applyElementModifiers(node, spec.modifiers, state, path, context);

    Object.keys(spec.elements || {}).sort().forEach((propertyName, index) => {
      const row = document.createElement("div");
      row.className = "skeleton-object-row";

      const label = document.createElement("div");
      label.className = "skeleton-object-key";
      label.textContent = `${propertyName}:`;
      row.appendChild(label);

      const value = document.createElement("div");
      value.className = "skeleton-object-value";
      value.appendChild(
        renderElement(
          decodeElement(spec.elements[propertyName]),
          state,
          context,
          `${key}.object.${propertyName}.${index}`,
          `${path}.${propertyName}`
        )
      );
      row.appendChild(value);
      node.appendChild(row);
    });
    return node;
  }

  function renderUnsupported(raw, state, context, key, path) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const node = document.createElement("div");
    node.className = "skeleton-fallback skeleton-unsupported";
    node.setAttribute("role", "note");
    applySkeletonIdentity(node, key, path);
    applyElementModifiers(node, spec.modifiers, state, path, context);

    const elementType = typeof spec.elementType === "string"
      ? spec.elementType
      : (typeof spec.type === "string" ? spec.type : "Unknown");
    const title = document.createElement("div");
    title.className = "skeleton-unsupported-title";
    title.textContent = `Unsupported skeleton element: ${elementType}`;
    node.appendChild(title);

    if (typeof spec.reason === "string" && spec.reason.trim()) {
      const reason = document.createElement("div");
      reason.className = "skeleton-unsupported-reason";
      reason.textContent = spec.reason.trim();
      node.appendChild(reason);
    }
    return node;
  }

  // R2 (godkjent av Kjetil 2026-08-28): web-rendereren konsumerer fontStyle og
  // hAlignment/vAlignment, som til naa var Swift-only og forsvant stille paa web.
  // Rollene speiler SwiftUI-tekststilene slik fabrikkene bruker dem. Eksplisitt
  // fontSize/fontWeight i modifiers vinner alltid over fontStyle-rollen.
  const FONT_STYLE_ROLES = {
    largeTitle:  { fontSize: 34, fontWeight: "700", lineHeight: 1.15 },
    title:       { fontSize: 28, fontWeight: "600", lineHeight: 1.18 },
    title2:      { fontSize: 22, fontWeight: "600", lineHeight: 1.2 },
    title3:      { fontSize: 20, fontWeight: "600", lineHeight: 1.22 },
    headline:    { fontSize: 17, fontWeight: "600", lineHeight: 1.3 },
    subheadline: { fontSize: 15, fontWeight: "400", lineHeight: 1.35, opacity: 0.85 },
    body:        { fontSize: 17, fontWeight: "400", lineHeight: 1.45 },
    callout:     { fontSize: 16, fontWeight: "400", lineHeight: 1.4 },
    footnote:    { fontSize: 13, fontWeight: "400", lineHeight: 1.35, opacity: 0.8 },
    caption:     { fontSize: 12, fontWeight: "400", lineHeight: 1.3, opacity: 0.8 },
    caption1:    { fontSize: 12, fontWeight: "400", lineHeight: 1.3, opacity: 0.8 },
    caption2:    { fontSize: 11, fontWeight: "400", lineHeight: 1.3, opacity: 0.75 },
  };

  function applyFontStyleRole(element, modifiers) {
    const role = typeof modifiers.fontStyle === "string" ? modifiers.fontStyle.trim() : "";
    if (!role) {
      return;
    }
    element.dataset.fontStyle = role;
    element.classList.add(`sk-font-${sanitizeClassName(role)}`);
    const spec = FONT_STYLE_ROLES[role];
    if (!spec) {
      return;
    }
    if (typeof modifiers.fontSize !== "number") {
      element.style.fontSize = `${spec.fontSize}px`;
    }
    if (typeof modifiers.fontWeight !== "string" || !modifiers.fontWeight) {
      element.style.fontWeight = spec.fontWeight;
    }
    if (spec.lineHeight) {
      element.style.lineHeight = String(spec.lineHeight);
    }
    if (typeof spec.opacity === "number" && typeof modifiers.opacity !== "number") {
      element.style.opacity = String(spec.opacity);
    }
  }

  function portableFontWeight(value) {
    const weights = { ultralight: "100", thin: "200", light: "300", regular: "400", normal: "400",
      medium: "500", semibold: "600", bold: "700", heavy: "800", black: "900" };
    const name = String(value).trim().toLowerCase();
    return weights[name] || (/^[1-9]00$/.test(name) ? name : "400");
  }

  function applyInsets(element, insets, padding = 0) {
    const names = { top: "paddingTop", leading: "paddingInlineStart", bottom: "paddingBottom", trailing: "paddingInlineEnd" };
    Object.entries(names).forEach(([edge, property]) => { element.style[property] = `${insets[edge] ?? padding}px`; });
  }

  function applyPortableModifiers(element, modifiers, state) {
    if (modifiers.paddingInsets) applyInsets(element, modifiers.paddingInsets, modifiers.padding || 0);
    if (modifiers.fontFamilies?.length) {
      const fallback = state?.fontFallback || "system-ui, sans-serif";
      element.style.fontFamily = `${modifiers.fontFamilies.map((font) => JSON.stringify(font)).join(", ")}, ${fallback}`;
    }
    if (Number.isFinite(modifiers.lineHeightMultiple)) element.style.lineHeight = String(modifiers.lineHeightMultiple);
    if (Number.isFinite(modifiers.letterSpacing)) element.style.letterSpacing = `${modifiers.letterSpacing}px`;
    if (["proportional", "tabular"].includes(modifiers.numericVariant)) element.style.fontVariantNumeric = `${modifiers.numericVariant}-nums`;
    ["minHeight", "maxHeight", "minWidth"].forEach((name) => {
      if (Number.isFinite(modifiers[name])) element.style[name] = `${modifiers[name]}px`;
    });
    if (Number.isFinite(modifiers.flexGrow)) element.style.flexGrow = String(modifiers.flexGrow);
    if (Number.isFinite(modifiers.itemSpacing) && element.classList.contains("skeleton-list")) element.style.gap = `${modifiers.itemSpacing}px`;
    if (modifiers.controlStyle === "plain") element.classList.add("skeleton-control-plain");
    if (typeof modifiers.accessibilityLabel === "string") element.setAttribute("aria-label", modifiers.accessibilityLabel);
    if (modifiers.borderStyle) element.style.borderStyle = modifiers.borderStyle;
    if (Array.isArray(modifiers.borderEdges)) {
      const sides = { top: "Top", leading: "InlineStart", bottom: "Bottom", trailing: "InlineEnd" };
      Object.entries(sides).forEach(([edge, side]) => {
        element.style[`border${side}Width`] = `${modifiers.borderEdges.includes(edge) ? (modifiers.borderWidth ?? 0) : 0}px`;
      });
    }
    if (modifiers.contentClip === true) element.style.overflow = "hidden";
    if (modifiers.textDecoration) element.style.textDecoration = modifiers.textDecoration;
    if (Number.isFinite(modifiers.textRotationDegrees)) element.style.rotate = `${modifiers.textRotationDegrees}deg`;
    if (modifiers.leadingMarker) {
      const marker = modifiers.leadingMarker;
      element.classList.add("skeleton-leading-marker");
      Object.entries({ width: marker.width, top: marker.insetTop, bottom: marker.insetBottom,
        offset: marker.offset, radius: marker.cornerRadius }).forEach(([name, value]) => {
        element.style.setProperty(`--marker-${name}`, `${value}px`);
      });
      element.style.setProperty("--marker-color", marker.color);
    }
  }

  const VARIANT_STYLE_PROPERTIES = ["flexDirection", "gridTemplateColumns", "gap", "paddingTop", "paddingInlineStart",
    "paddingBottom", "paddingInlineEnd", "minHeight", "maxHeight", "flexGrow", "fontSize", "borderColor", "color", "alignItems", "justifyContent", "width"];
  const VARIANT_OVERRIDES = ["axis", "columns", "spacing", "paddingInsets", "minHeight", "maxHeight", "flexGrow", "fontSize", "borderColor", "foregroundColor", "width"];

  function layoutVariantMatches(variant, available, state, context) {
    if (variant.when && !evaluateVisibilityCondition(variant.when, state, context)) return false;
    for (const dimension of ["Width", "Height"]) {
      const value = available[`available${dimension}`];
      for (const bound of ["min", "max"]) {
        const threshold = variant[`${bound}Available${dimension}`];
        if (threshold != null && (!Number.isFinite(value) || (bound === "min" ? value < threshold : value > threshold))) return false;
      }
    }
    return (variant.requiresCapability || []).every((capability) => (available.capabilities || []).includes(capability));
  }

  function narrowDimension(inherited, declared) {
    if (!Number.isFinite(declared)) return inherited;
    return Number.isFinite(inherited) ? Math.min(inherited, declared) : declared;
  }

  function declaredGridWidths(columns, width, spacing, count) {
    if (!columns?.length) return [];
    const adaptive = columns.find((column) => column.type === "adaptive");
    if (adaptive) {
      if (!Number.isFinite(width)) return [];
      const minimum = adaptive.min ?? 120;
      const tracks = Math.max(1, Math.min(count || 1, Math.floor((width + spacing) / (minimum + spacing))));
      return Array(tracks).fill(Math.min(adaptive.max ?? Infinity, Math.max(0, (width - spacing * (tracks - 1)) / tracks)));
    }
    const sizes = columns.map((column) => column.type === "fixed" ? column.value : column.min || 0);
    if (!Number.isFinite(width)) return columns.map((column) => column.type === "fixed" ? column.value : undefined);
    let remaining = Math.max(0, width - spacing * (columns.length - 1) - sizes.reduce((sum, value) => sum + value, 0));
    let flexible = columns.map((column, index) => column.type === "flexible" ? index : -1).filter((index) => index >= 0);
    while (remaining > 0.01 && flexible.length) {
      const share = remaining / flexible.length;
      flexible.forEach((index) => {
        const addition = Math.min(share, (columns[index].max ?? Infinity) - sizes[index]);
        sizes[index] += Math.max(0, addition);
        remaining -= Math.max(0, addition);
      });
      flexible = flexible.filter((index) => sizes[index] < (columns[index].max ?? Infinity));
    }
    return sizes;
  }

  function updateLayoutContext(state) {
    const visit = (node, inherited) => {
      if (!(node instanceof HTMLElement)) return;
      const interaction = node.skeletonInteraction;
      if (interaction) Object.assign(node.style, interaction.base);
      const record = node.skeletonLayout;
      let available = { ...inherited };
      let columns = null;
      let spacing = 0;
      if (record) {
        const { spec, context } = record;
        const modifiers = spec.modifiers || {};
        available.availableWidth = narrowDimension(available.availableWidth, modifiers.width);
        available.availableHeight = narrowDimension(available.availableHeight, modifiers.height);
        const variants = modifiers.layoutVariants || [];
        const index = variants.findIndex((variant) => layoutVariantMatches(variant, available, record.state, context));
        const variant = index < 0 ? {} : variants[index];
        if (variants.length) {
          if (!record.base) record.base = Object.fromEntries(VARIANT_STYLE_PROPERTIES.map((name) => [name, node.style[name]]));
          Object.entries(record.base).forEach(([name, value]) => { node.style[name] = value; });
          node.dataset.layoutVariant = String(index);
        }
        const effective = { ...modifiers };
        VARIANT_OVERRIDES.forEach((name) => { if (variant[name] != null) effective[name] = variant[name]; });
        if (variant.axis && ["HStack", "VStack"].includes(record.type)) node.style.flexDirection = variant.axis === "horizontal" ? "row" : "column";
        if (["HStack", "VStack"].includes(record.type)) {
          const direction = variant.axis ? (variant.axis === "horizontal" ? "row" : "column") : (record.type === "HStack" ? "row" : "column");
          applyStackAlignmentModifiers(node, modifiers, direction);
          node.dataset.axis = direction; // WP-B4 paritet
        }
        if (variant.columns && record.type === "Grid") node.style.gridTemplateColumns = gridTemplateColumns(variant.columns);
        if (Number.isFinite(variant.spacing)) node.style.gap = `${variant.spacing}px`;
        if (variant.paddingInsets) applyInsets(node, variant.paddingInsets, modifiers.padding || 0);
        ["minHeight", "maxHeight", "fontSize"].forEach((name) => {
          if (Number.isFinite(variant[name])) node.style[name] = `${variant[name]}px`;
        });
        if (Number.isFinite(variant.flexGrow)) node.style.flexGrow = String(variant.flexGrow);
        if (variant.borderColor) node.style.borderColor = variant.borderColor;
        if (variant.foregroundColor) node.style.color = variant.foregroundColor;
        // WP-F format: fast bredde eller skjult mens varianten gjelder; elementet og tilstanden beholdes.
        if (Number.isFinite(variant.width)) {
          node.style.width = `${variant.width}px`;
          available.availableWidth = narrowDimension(available.availableWidth, variant.width);
        }
        // dataset, ikke toggleAttribute: samme attributter, og node-kontrakttestens DOM kjenner dataset.
        if (variant.hidden === true) node.dataset.layoutHidden = "true"; else delete node.dataset.layoutHidden;
        if (Number.isFinite(variant.width) || typeof modifiers.width === "number") node.dataset.fixedWidth = "true"; else delete node.dataset.fixedWidth;
        // Bound colors are live in a mounted item as in a List row.
        [["backgroundKeypath", "background"], ["foregroundColorKeypath", "color"]].forEach(([key, property]) => {
          if (modifiers[key] && !(property === "color" && variant.foregroundColor)) {
            node.style[property] = resolveKeypath(modifiers[key], record.state.rootData, context) || modifiers[property === "color" ? "foregroundColor" : "background"] || "";
          }
        });
        if (modifiers.hAlignmentKeypath) {
          const alignment = resolveKeypath(modifiers.hAlignmentKeypath, record.state.rootData, context) || modifiers.hAlignment;
          if (["HStack", "VStack"].includes(record.type)) {
            // WP-B4 paritet: stakkens justering gjelder innholdet (se applyElementModifiers).
            const direction = variant.axis ? (variant.axis === "horizontal" ? "row" : "column") : (record.type === "HStack" ? "row" : "column");
            applyStackAlignmentModifiers(node, { ...modifiers, hAlignment: alignment }, direction);
          } else {
            node.style.alignSelf = { leading: "flex-start", center: "center", trailing: "flex-end" }[alignment] || "";
          }
        }
        const padding = effective.padding || 0;
        const insets = effective.paddingInsets || {};
        if (Number.isFinite(available.availableWidth)) available.availableWidth = Math.max(0, available.availableWidth - (insets.leading ?? padding) - (insets.trailing ?? padding));
        if (Number.isFinite(available.availableHeight)) available.availableHeight = Math.max(0, narrowDimension(available.availableHeight, effective.maxHeight) - (insets.top ?? padding) - (insets.bottom ?? padding));
        if (record.type === "Grid") {
          columns = variant.columns || spec.columns;
          spacing = variant.spacing ?? spec.spacing ?? 10;
        }
      }
      if (interaction) {
        ["background", "color", "opacity"].forEach((property) => { interaction.base[property] = node.style[property]; });
        applyInteractionState(node, state);
      }
      const children = Array.from(node.children);
      const widths = declaredGridWidths(columns, available.availableWidth, spacing, children.length);
      children.forEach((child, index) => visit(child, widths.length
        ? { ...available, availableWidth: widths[index % widths.length] }
        : available));
    };
    // The host supplies these numbers. Never infer viewport classes or measure
    // individual elements: undeclared containers pass the same context on.
    Array.from(state.rootElement.children).forEach((child) => visit(child, state.layoutContext));
  }

  function registerInteractionStyles(element, modifiers, state) {
    if (!state || !modifiers.interactionStyles) return;
    const record = { styles: modifiers.interactionStyles, base: {}, hovered: false, focused: false };
    ["background", "color", "opacity"].forEach((property) => { record.base[property] = element.style[property]; });
    element.skeletonInteraction = record;
    const refresh = () => applyInteractionState(element, state);
    element.addEventListener("mouseenter", () => { record.hovered = true; refresh(); });
    element.addEventListener("mouseleave", () => { record.hovered = false; refresh(); });
    element.addEventListener("focusin", () => { record.focused = element.matches(":focus-visible"); refresh(); });
    element.addEventListener("focusout", () => { record.focused = false; refresh(); });
  }

  function applyInteractionState(element, state) {
    const record = element.skeletonInteraction;
    if (!record) return;
    const { styles } = record;
    const combined = { ...record.base };
    const apply = (style) => {
      if (!style) return;
      if (style.background != null) combined.background = style.background;
      if (style.foregroundColor != null) combined.color = style.foregroundColor;
      if (style.opacity != null) combined.opacity = String(style.opacity);
    };
    if (record.hovered) apply(styles.hover);
    if (record.focused) apply(styles.focusVisible);
    if (state.dragContext.transfer) apply(styles.dragActive);
    if (state.dragContext.source === element) apply(styles.dragSource);
    Object.assign(element.style, combined);
  }

  function setHostDrag(state, transfer, source) {
    const previous = state.dragContext.source;
    if (previous !== source) previous?.classList.remove("drag-active");
    Object.assign(state.dragContext, { transfer, source });
    state.dragContext.listeners.forEach((refresh) => refresh());
  }

  function refreshDragStyles(state) {
    const nodes = [state.rootElement, ...state.rootElement.querySelectorAll("*")];
    nodes.forEach((element) => {
      applyInteractionState(element, state);
      const drop = element.skeletonDrop;
      if (drop) {
        const accepting = dragRoleAccepted(state.dragContext.transfer, drop.acceptedDragRoles);
        element.classList.toggle("drop-accepting", accepting);
        if (!state.dragContext.transfer) updateDropTargetState(element, drop.modifiers, state, drop.context, "idle");
      }
    });
  }

  function isSkeletonStack(element) {
    return element instanceof HTMLElement
      && (element.classList.contains("skeleton-hstack") || element.classList.contains("skeleton-vstack"));
  }

  function applyStackAlignmentModifiers(element, modifiers, direction) {
    if (!(element instanceof HTMLElement) || !modifiers || typeof modifiers !== "object") {
      return;
    }
    const h = typeof modifiers.hAlignment === "string" ? modifiers.hAlignment.trim() : "";
    const v = typeof modifiers.vAlignment === "string" ? modifiers.vAlignment.trim() : "";
    const cross = { leading: "flex-start", center: "center", trailing: "flex-end",
                    top: "flex-start", bottom: "flex-end", firstTextBaseline: "first baseline" };
    if (direction === "column") {
      if (cross[h]) { element.style.alignItems = cross[h]; }
      if (cross[v]) { element.style.justifyContent = cross[v]; }
    } else {
      if (cross[v]) { element.style.alignItems = cross[v]; }
      if (cross[h]) { element.style.justifyContent = cross[h]; }
    }
  }

  function applyElementModifiers(element, modifiers, state = null, path = null, context = null) {
    if (!(element instanceof HTMLElement) || !modifiers || typeof modifiers !== "object") {
      return;
    }

    element.skeletonLayout = { type: null, spec: { modifiers }, state, context, base: null };
    const styleRole = typeof modifiers.styleRole === "string" ? modifiers.styleRole.trim() : "";
    if (styleRole) {
      element.dataset.styleRole = styleRole;
      element.classList.add(`style-role-${sanitizeClassName(styleRole)}`);
    }

    const motionHint = typeof modifiers.motionHint === "string" ? modifiers.motionHint.trim() : "";
    if (motionHint) {
      element.dataset.motionHint = motionHint;
      element.classList.add("motion-hint");
      element.classList.add(`motion-hint-${sanitizeClassName(motionHint)}`);
      window.requestAnimationFrame(() => {
        element.classList.add("motion-hint-mounted");
      });
    }

    const motionSourceRole = typeof modifiers.motionSourceRole === "string" ? modifiers.motionSourceRole.trim() : "";
    if (motionSourceRole) {
      element.dataset.motionSourceRole = motionSourceRole;
      element.classList.add(`motion-source-${sanitizeClassName(motionSourceRole)}`);
    }

    if (Array.isArray(modifiers.styleClasses)) {
      modifiers.styleClasses.forEach((entry) => {
        if (typeof entry === "string" && entry.trim()) {
          element.classList.add(sanitizeClassName(entry.trim()));
        }
      });
    }

    if (typeof modifiers.padding === "number") {
      element.style.padding = `${modifiers.padding}px`;
    }
    if (typeof modifiers.width === "number") {
      element.style.width = `${modifiers.width}px`;
      element.dataset.fixedWidth = "true"; // WP-F paritet: fast bredde krymper ikke i en rad (porthole-webo.css)
    }
    if (typeof modifiers.height === "number") {
      element.style.height = `${modifiers.height}px`;
    }
    if (modifiers.maxWidthInfinity === true) {
      element.style.maxWidth = "100%";
      element.dataset.fillWidth = "true"; // WP-B4 paritet: fyller bredden i en kolonne (porthole-webo.css)
    }
    if (modifiers.maxHeightInfinity === true) {
      element.style.maxHeight = "100%";
      element.dataset.fillHeight = "true"; // WP-B4 paritet: fyller høyden i en rad (porthole-webo.css)
    }
    if (modifiers.wrap === true) {
      // Containers here are already display:flex (skeleton-hstack, skeleton-list,
      // skeleton-vstack); flex-wrap alone gives real per-item-width wrapping
      // (unlike SkeletonGrid's fixed-track columns). Lists default to a
      // column axis, so flip to row for a wrap request - HStack/VStack are
      // already row/column respectively and don't need the axis override.
      element.style.flexWrap = "wrap";
      if (element.classList.contains("skeleton-list")) {
        element.style.flexDirection = "row";
        element.style.alignItems = "center";
      }
    }
    // hAlignment/vAlignment position THIS element within its flex parent
    // (align-self) rather than arranging children inside it - the flexbox
    // equivalent of SwiftUI's `.frame(alignment:)` on the element itself.
    // align-self is single-axis (it only affects the parent's cross axis),
    // so unlike SwiftUI's true 2D frame alignment, combining hAlignment and
    // vAlignment on the same element isn't meaningful here - whichever is
    // set wins, with hAlignment taking priority when both are present. This
    // is enough for the common case (e.g. a chat message row's own alignment
    // within a column-flex list), not a full 2D layout primitive.
    const rootData = state ? state.rootData : null;
    const resolvedHAlignment = (modifiers.hAlignmentKeypath
      ? valueToDisplay(resolveKeypath(modifiers.hAlignmentKeypath, rootData, context))
      : null) || modifiers.hAlignment;
    // No vAlignmentKeypath in the schema (only hAlignment/background/
    // foregroundColor got item-bound keypaths) - vAlignment stays static.
    const resolvedVAlignment = modifiers.vAlignment;
    const alignSelfFrom = (value) => {
      if (value === "leading" || value === "top") return "flex-start";
      if (value === "trailing" || value === "bottom") return "flex-end";
      if (value === "center") return "center";
      return null;
    };
    const alignSelf = alignSelfFrom(resolvedHAlignment) || alignSelfFrom(resolvedVAlignment);
    // WP-B4 paritet: en HStack/VStack har alltid full bredde (CellApple .frame(maxWidth: .infinity));
    // dens egen hAlignment/vAlignment plasserer innholdet, ikke stakken selv.
    if (isSkeletonStack(element)) {
      if (modifiers.hAlignmentKeypath && resolvedHAlignment) {
        applyStackAlignmentModifiers(element, { ...modifiers, hAlignment: resolvedHAlignment },
          element.classList.contains("skeleton-hstack") ? "row" : "column");
      }
    } else if (alignSelf) {
      element.style.alignSelf = alignSelf;
    }
    const resolvedBackground = (modifiers.backgroundKeypath
      ? valueToDisplay(resolveKeypath(modifiers.backgroundKeypath, rootData, context))
      : null) || modifiers.background;
    if (typeof resolvedBackground === "string" && resolvedBackground) {
      element.style.background = resolvedBackground;
    }
    if (typeof modifiers.cornerRadius === "number") {
      element.style.borderRadius = `${modifiers.cornerRadius}px`;
    }
    const resolvedForegroundColor = (modifiers.foregroundColorKeypath
      ? valueToDisplay(resolveKeypath(modifiers.foregroundColorKeypath, rootData, context))
      : null) || modifiers.foregroundColor;
    if (typeof resolvedForegroundColor === "string" && resolvedForegroundColor) {
      element.style.color = resolvedForegroundColor;
    }
    applyFontStyleRole(element, modifiers);
    if (typeof modifiers.fontSize === "number") {
      element.style.fontSize = `${modifiers.fontSize}px`;
    }
    if (typeof modifiers.fontWeight === "string" && modifiers.fontWeight) {
      element.style.fontWeight = portableFontWeight(modifiers.fontWeight);
    }
    if (typeof modifiers.opacity === "number") {
      element.style.opacity = String(modifiers.opacity);
    }
    registerVisibilityBinding(element, modifiers, state, context);
    updateElementVisibility(element, modifiers, state, context);
    registerPresentationBinding(element, modifiers, state, path, context);

    if (typeof modifiers.multilineTextAlignment === "string") {
      if (modifiers.multilineTextAlignment === "leading") {
        element.style.textAlign = "left";
      } else if (modifiers.multilineTextAlignment === "trailing") {
        element.style.textAlign = "right";
      } else if (modifiers.multilineTextAlignment === "center") {
        element.style.textAlign = "center";
      }
    }

    if (typeof modifiers.lineLimit === "number" && modifiers.lineLimit > 0) {
      element.style.display = "-webkit-box";
      element.style.webkitLineClamp = String(modifiers.lineLimit);
      element.style.webkitBoxOrient = "vertical";
      element.style.overflow = "hidden";
    }

    if (typeof modifiers.borderWidth === "number" && modifiers.borderWidth >= 0) {
      element.style.borderStyle = "solid";
      element.style.borderWidth = `${modifiers.borderWidth}px`;
      if (typeof modifiers.borderColor === "string" && modifiers.borderColor) {
        element.style.borderColor = modifiers.borderColor;
      }
    }

    if (Number.isFinite(modifiers.shadowRadius) || Number.isFinite(modifiers.shadowSpread)) {
      const shadowX = typeof modifiers.shadowX === "number" ? modifiers.shadowX : 0;
      const shadowY = typeof modifiers.shadowY === "number" ? modifiers.shadowY : 0;
      const shadowColor = typeof modifiers.shadowColor === "string" ? modifiers.shadowColor : "rgba(0,0,0,0.2)";
      element.style.boxShadow = `${shadowX}px ${shadowY}px ${modifiers.shadowRadius || 0}px ${modifiers.shadowSpread || 0}px ${shadowColor}`;
    }

    applyPortableModifiers(element, modifiers, state);
    registerInteractionStyles(element, modifiers, state);
    applyDragAndDropModifiers(element, modifiers, state, path, context);
  }

  function registerVisibilityBinding(element, modifiers, state, context) {
    if (!state || !modifiers.visibility || typeof modifiers.visibility !== "object") {
      return;
    }
    state.visibilityBindings.push({ element, modifiers, context });
  }

  function updateVisibilityBindings(state) {
    state.visibilityBindings = state.visibilityBindings.filter((binding) => {
      if (!binding || !(binding.element instanceof HTMLElement)) {
        return false;
      }
      const retainedInRenderer = state.rootElement instanceof HTMLElement
        && state.rootElement.contains(binding.element);
      if (!binding.element.isConnected && !retainedInRenderer) {
        return false;
      }
      updateElementVisibility(binding.element, binding.modifiers, state, binding.context);
      return true;
    });
  }

  function updateElementVisibility(element, modifiers, state, context) {
    if (!(element instanceof HTMLElement) || !modifiers || typeof modifiers !== "object") {
      return;
    }
    const isVisible = modifiers.hidden === true
      ? false
      : evaluateVisibilityRule(modifiers.visibility, state, context);

    element.hidden = !isVisible;
    if (isVisible) {
      element.removeAttribute("aria-hidden");
      delete element.dataset.visibilityState;
    } else {
      element.setAttribute("aria-hidden", "true");
      element.dataset.visibilityState = "hidden";
    }
  }

  const PRESENTATION_KINDS = new Set(["overlay", "drawer", "sheet", "popover", "modal"]);
  const PRESENTATION_PLACEMENTS = new Set(["leading", "trailing", "top", "bottom", "center", "anchor"]);
  const PRESENTATION_BACKDROPS = new Set(["none", "dim", "blur"]);
  const PRESENTATION_ESCAPE_BEHAVIORS = new Set(["disabled", "closeAction"]);

  function registerPresentationBinding(element, modifiers, state, path, context) {
    if (!state || !(element instanceof HTMLElement) || !modifiers || typeof modifiers !== "object") {
      return;
    }
    const presentation = normalizePresentation(modifiers.presentation);
    if (!presentation) {
      return;
    }

    let binding = element.__havenSkeletonPresentationBinding || null;
    if (binding) {
      binding.modifiers = modifiers;
      binding.presentation = presentation;
      binding.path = path;
      binding.context = context;
    } else {
      binding = {
        element,
        modifiers,
        presentation,
        path,
        context,
        order: state.presentationSequence += 1,
        backdrop: null,
        wasOpen: false,
        previousFocus: null,
      };
      element.__havenSkeletonPresentationBinding = binding;
      state.presentationBindings.push(binding);
    }

    applyPresentationMetadata(binding, false);
  }

  function normalizePresentation(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
      return null;
    }
    const kind = normalizePresentationToken(raw.kind, PRESENTATION_KINDS);
    if (!kind) {
      return null;
    }
    const fallbackPlacement = defaultPresentationPlacement(kind);
    const placement = normalizePresentationToken(raw.placement, PRESENTATION_PLACEMENTS) || fallbackPlacement;
    const closeActionKeypath = stringOrNull(raw.closeActionKeypath);
    const escapeKeyBehavior = normalizePresentationToken(raw.escapeKeyBehavior, PRESENTATION_ESCAPE_BEHAVIORS)
      || (closeActionKeypath ? "closeAction" : "disabled");
    const backdropStyle = normalizePresentationToken(raw.backdropStyle, PRESENTATION_BACKDROPS)
      || (kind === "modal" ? "dim" : "none");
    const mobileFallback = normalizePresentationFallback(raw.mobileFallback);

    return {
      kind,
      placement,
      closeActionKeypath,
      openStateKeypath: stringOrNull(raw.openStateKeypath),
      dismissOnBackdrop: raw.dismissOnBackdrop === true,
      backdropStyle,
      escapeKeyBehavior,
      focusTrap: typeof raw.focusTrap === "boolean" ? raw.focusTrap : kind === "modal",
      anchorRole: stringOrNull(raw.anchorRole),
      anchorKeypath: stringOrNull(raw.anchorKeypath),
      zIndex: Number.isFinite(raw.zIndex) ? raw.zIndex : null,
      mobileFallback,
      accessibilityLabel: stringOrNull(raw.accessibilityLabel),
    };
  }

  function normalizePresentationFallback(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
      return null;
    }
    const kind = normalizePresentationToken(raw.kind, PRESENTATION_KINDS);
    const placement = normalizePresentationToken(raw.placement, PRESENTATION_PLACEMENTS);
    if (!kind && !placement) {
      return null;
    }
    return { kind, placement };
  }

  function normalizePresentationToken(value, allowed) {
    if (typeof value !== "string") {
      return null;
    }
    const token = value.trim();
    return allowed.has(token) ? token : null;
  }

  function defaultPresentationPlacement(kind) {
    switch (kind) {
      case "drawer":
        return "trailing";
      case "sheet":
        return "bottom";
      case "popover":
        return "anchor";
      case "modal":
        return "center";
      default:
        return "center";
    }
  }

  function applyPresentationMetadata(binding, isOpen) {
    const { element, presentation } = binding;
    if (!(element instanceof HTMLElement) || !presentation) {
      return;
    }
    ["overlay", "drawer", "sheet", "popover", "modal"].forEach((kind) => {
      element.classList.remove(`skeleton-presentation-${kind}`);
    });
    ["leading", "trailing", "top", "bottom", "center", "anchor"].forEach((placement) => {
      element.classList.remove(`skeleton-presentation-placement-${placement}`);
    });
    element.classList.add("skeleton-presentation");
    element.classList.add(`skeleton-presentation-${presentation.kind}`);
    element.classList.add(`skeleton-presentation-placement-${presentation.placement}`);
    element.classList.toggle("skeleton-presentation-open", isOpen);
    element.dataset.presentationKind = presentation.kind;
    element.dataset.presentationPlacement = presentation.placement;
    if (presentation.mobileFallback && presentation.mobileFallback.kind) {
      element.dataset.presentationMobileKind = presentation.mobileFallback.kind;
    } else {
      delete element.dataset.presentationMobileKind;
    }
    if (presentation.mobileFallback && presentation.mobileFallback.placement) {
      element.dataset.presentationMobilePlacement = presentation.mobileFallback.placement;
    } else {
      delete element.dataset.presentationMobilePlacement;
    }
    if (presentation.accessibilityLabel) {
      element.setAttribute("aria-label", presentation.accessibilityLabel);
    }
    if (["drawer", "sheet", "popover", "modal"].includes(presentation.kind)) {
      element.setAttribute("role", "dialog");
    }
    if (presentation.kind === "modal" && presentation.focusTrap && isOpen) {
      element.setAttribute("aria-modal", "true");
    } else {
      element.removeAttribute("aria-modal");
    }
    if (!element.hasAttribute("tabindex") && (presentation.kind === "modal" || presentation.focusTrap)) {
      element.setAttribute("tabindex", "-1");
    }
  }

  function updatePresentationBindings(state) {
    if (!state) {
      return;
    }
    const openBindings = [];
    state.presentationBindings = state.presentationBindings.filter((binding) => {
      if (!binding || !(binding.element instanceof HTMLElement)) {
        cleanupPresentationBinding(binding);
        return false;
      }
      const retainedInRenderer = state.rootElement instanceof HTMLElement
        && state.rootElement.contains(binding.element);
      if (!binding.element.isConnected) {
        if (retainedInRenderer && state.isMounted === false) {
          return true;
        }
        cleanupPresentationBinding(binding);
        return false;
      }
      const presentation = normalizePresentation(binding.modifiers && binding.modifiers.presentation);
      if (!presentation) {
        cleanupPresentationBinding(binding);
        return false;
      }
      binding.presentation = presentation;
      ensurePresentationHost(binding);
      ensurePresentationBackdrop(binding, state);
      const isOpen = isPresentationBindingOpen(binding);
      applyPresentationMetadata(binding, isOpen);
      updatePresentationBackdrop(binding, isOpen);
      if (isOpen) {
        openBindings.push(binding);
        if (!binding.wasOpen) {
          handlePresentationOpened(binding);
        }
      } else if (binding.wasOpen) {
        handlePresentationClosed(binding);
      }
      binding.wasOpen = isOpen;
      return true;
    });

    openBindings.sort(comparePresentationBindings);
    openBindings.forEach((binding, index) => {
      const zIndex = Number.isFinite(binding.presentation.zIndex)
        ? binding.presentation.zIndex
        : 100 + index;
      binding.element.style.zIndex = String(1000 + zIndex);
      if (binding.backdrop) {
        binding.backdrop.style.zIndex = String(999 + zIndex);
      }
    });
    state.activePresentationBindings = openBindings;
    updatePresentationScrollLock(state, openBindings);
  }

  function ensurePresentationHost(binding) {
    const parent = binding.element.parentElement;
    if (parent) {
      parent.classList.add("skeleton-presentation-host");
    }
  }

  function presentationNeedsBackdrop(presentation) {
    return presentation.dismissOnBackdrop === true || presentation.backdropStyle !== "none" || presentation.kind === "modal";
  }

  function ensurePresentationBackdrop(binding, state) {
    const { presentation } = binding;
    if (!presentationNeedsBackdrop(presentation)) {
      removePresentationBackdrop(binding);
      return;
    }
    if (!binding.backdrop) {
      const backdrop = document.createElement("div");
      backdrop.className = "skeleton-presentation-backdrop";
      backdrop.addEventListener("click", (event) => {
        if (!binding.presentation.dismissOnBackdrop) {
          return;
        }
        const top = topOpenPresentationBinding(state);
        if (top !== binding) {
          return;
        }
        event.preventDefault();
        event.stopPropagation();
        closePresentationBinding(state, binding, "backdrop");
      });
      binding.backdrop = backdrop;
    }
    if (binding.element.parentElement && !binding.backdrop.isConnected) {
      binding.element.parentElement.insertBefore(binding.backdrop, binding.element);
    }
  }

  function updatePresentationBackdrop(binding, isOpen) {
    if (!binding.backdrop) {
      return;
    }
    const { presentation } = binding;
    binding.backdrop.hidden = !isOpen;
    binding.backdrop.classList.toggle("is-open", isOpen);
    binding.backdrop.dataset.presentationBackdrop = presentation.backdropStyle;
    binding.backdrop.dataset.presentationKind = presentation.kind;
    binding.backdrop.dataset.presentationPlacement = presentation.placement;
  }

  function removePresentationBackdrop(binding) {
    if (binding && binding.backdrop && binding.backdrop.parentElement) {
      binding.backdrop.parentElement.removeChild(binding.backdrop);
    }
    if (binding) {
      binding.backdrop = null;
    }
  }

  function cleanupPresentationBinding(binding) {
    if (!binding) {
      return;
    }
    removePresentationBackdrop(binding);
    if (binding.element instanceof HTMLElement) {
      delete binding.element.__havenSkeletonPresentationBinding;
    }
  }

  function cleanupPresentationBindings(state) {
    if (!state) {
      return;
    }
    state.presentationBindings.forEach(cleanupPresentationBinding);
    state.presentationBindings = [];
    state.activePresentationBindings = [];
    updatePresentationScrollLock(state, []);
  }

  function isPresentationBindingOpen(binding) {
    return binding && binding.element instanceof HTMLElement
      && binding.element.hidden !== true
      && binding.element.dataset.visibilityState !== "hidden";
  }

  function comparePresentationBindings(lhs, rhs) {
    const lhsZ = lhs.presentation && Number.isFinite(lhs.presentation.zIndex) ? lhs.presentation.zIndex : lhs.order;
    const rhsZ = rhs.presentation && Number.isFinite(rhs.presentation.zIndex) ? rhs.presentation.zIndex : rhs.order;
    if (lhsZ !== rhsZ) {
      return lhsZ - rhsZ;
    }
    return lhs.order - rhs.order;
  }

  function topOpenPresentationBinding(state) {
    const openBindings = (state.activePresentationBindings || []).filter(isPresentationBindingOpen);
    if (!openBindings.length) {
      return null;
    }
    return openBindings[openBindings.length - 1];
  }

  function handlePresentationKeydown(state, event) {
    const binding = topOpenPresentationBinding(state);
    if (!binding || event.defaultPrevented) {
      return;
    }
    if (event.key === "Escape") {
      if (binding.presentation.escapeKeyBehavior === "closeAction" && binding.presentation.closeActionKeypath) {
        event.preventDefault();
        event.stopPropagation();
        closePresentationBinding(state, binding, "escape");
      }
      return;
    }
    if (event.key === "Tab" && binding.presentation.focusTrap === true) {
      trapPresentationFocus(binding, event);
    }
  }

  function closePresentationBinding(state, binding, reason) {
    const keypath = binding && binding.presentation ? binding.presentation.closeActionKeypath : null;
    if (!keypath) {
      return;
    }
    void dispatchAction(state, keypath, {
      source: "skeleton.presentation",
      reason,
      path: binding.path || null,
      kind: binding.presentation.kind,
    }, {
      trigger: "skeleton-presentation",
      reason,
      path: binding.path,
      context: binding.context,
    }).catch((error) => {
      console.warn("Skeleton presentation dismiss failed", error);
    });
  }

  function handlePresentationOpened(binding) {
    if (!binding.presentation.focusTrap && binding.presentation.kind !== "modal") {
      return;
    }
    binding.previousFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    window.requestAnimationFrame(() => {
      focusPresentation(binding);
    });
  }

  function handlePresentationClosed(binding) {
    if (binding.previousFocus instanceof HTMLElement && binding.previousFocus.isConnected) {
      try {
        binding.previousFocus.focus({ preventScroll: true });
      } catch (_) {
        binding.previousFocus.focus();
      }
    }
    binding.previousFocus = null;
  }

  function focusPresentation(binding) {
    const target = firstFocusableDescendant(binding.element) || binding.element;
    if (!(target instanceof HTMLElement)) {
      return;
    }
    try {
      target.focus({ preventScroll: true });
    } catch (_) {
      target.focus();
    }
  }

  function trapPresentationFocus(binding, event) {
    const focusable = focusableDescendants(binding.element);
    if (!focusable.length) {
      event.preventDefault();
      focusPresentation(binding);
      return;
    }
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    const active = document.activeElement;
    if (event.shiftKey && active === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && active === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function firstFocusableDescendant(element) {
    return focusableDescendants(element)[0] || null;
  }

  function focusableDescendants(element) {
    if (!(element instanceof HTMLElement)) {
      return [];
    }
    const selector = [
      "a[href]",
      "button:not([disabled])",
      "input:not([disabled])",
      "textarea:not([disabled])",
      "select:not([disabled])",
      "[tabindex]:not([tabindex='-1'])",
      "[contenteditable='true']",
    ].join(",");
    return Array.from(element.querySelectorAll(selector))
      .filter((candidate) => candidate instanceof HTMLElement
        && candidate.offsetParent !== null
        && candidate.hidden !== true
        && candidate.getAttribute("aria-hidden") !== "true");
  }

  function updatePresentationScrollLock(state, openBindings) {
    const shouldLock = openBindings.some((binding) => {
      const presentation = binding.presentation;
      return presentation.kind === "modal"
        || (presentation.kind === "sheet" && (presentation.focusTrap === true || presentation.backdropStyle !== "none"));
    });
    if (state.presentationScrollLocked === shouldLock) {
      return;
    }
    state.presentationScrollLocked = shouldLock;
    skeletonPresentationScrollLockCount += shouldLock ? 1 : -1;
    skeletonPresentationScrollLockCount = Math.max(0, skeletonPresentationScrollLockCount);
    const isLocked = skeletonPresentationScrollLockCount > 0;
    document.documentElement.classList.toggle("skeleton-presentation-scroll-locked", isLocked);
    if (document.body) {
      document.body.classList.toggle("skeleton-presentation-scroll-locked", isLocked);
    }
  }

  function evaluateVisibilityRule(rule, state, context) {
    if (!rule) {
      return true;
    }
    if (typeof rule !== "object" || Array.isArray(rule)) {
      return false;
    }
    if (!("when" in rule)) {
      return true;
    }
    return evaluateVisibilityCondition(rule.when, state, context);
  }

  function evaluateVisibilityCondition(condition, state, context) {
    if (!condition || typeof condition !== "object" || Array.isArray(condition)) {
      return false;
    }

    if (Object.prototype.hasOwnProperty.call(condition, "scope")) {
      if (!["root", "item", "context"].includes(condition.scope)) {
        return false;
      }
    }

    let evaluatedAnyPredicate = false;
    if (Object.prototype.hasOwnProperty.call(condition, "allOf")) {
      if (!Array.isArray(condition.allOf)) {
        return false;
      }
      evaluatedAnyPredicate = true;
      if (!condition.allOf.every((entry) => evaluateVisibilityCondition(entry, state, context))) {
        return false;
      }
    }
    if (Object.prototype.hasOwnProperty.call(condition, "anyOf")) {
      if (!Array.isArray(condition.anyOf)) {
        return false;
      }
      evaluatedAnyPredicate = true;
      if (!condition.anyOf.some((entry) => evaluateVisibilityCondition(entry, state, context))) {
        return false;
      }
    }
    if (Object.prototype.hasOwnProperty.call(condition, "not")) {
      if (!condition.not || typeof condition.not !== "object" || Array.isArray(condition.not)) {
        return false;
      }
      evaluatedAnyPredicate = true;
      if (evaluateVisibilityCondition(condition.not, state, context)) {
        return false;
      }
    }

    if (Object.prototype.hasOwnProperty.call(condition, "keypath") && typeof condition.keypath !== "string") {
      return false;
    }
    if (Object.prototype.hasOwnProperty.call(condition, "exists") && typeof condition.exists !== "boolean") {
      return false;
    }

    const hasKeypath = typeof condition.keypath === "string" && condition.keypath.trim();
    const resolvedValue = hasKeypath
      ? resolveVisibilityKeypath(condition.keypath.trim(), condition.scope, state, context)
      : undefined;

    if (hasKeypath) {
      evaluatedAnyPredicate = true;
    }
    if (typeof condition.exists === "boolean") {
      evaluatedAnyPredicate = true;
      if ((resolvedValue !== undefined && resolvedValue !== null) !== condition.exists) {
        return false;
      }
    }
    if (Object.prototype.hasOwnProperty.call(condition, "equals")) {
      evaluatedAnyPredicate = true;
      if (resolvedValue === undefined || !visibilityValuesMatch(resolvedValue, condition.equals)) {
        return false;
      }
    }
    if (Object.prototype.hasOwnProperty.call(condition, "notEquals")) {
      evaluatedAnyPredicate = true;
      if (resolvedValue === undefined || visibilityValuesMatch(resolvedValue, condition.notEquals)) {
        return false;
      }
    }
    if (Object.prototype.hasOwnProperty.call(condition, "in")) {
      if (!Array.isArray(condition.in)) {
        return false;
      }
      evaluatedAnyPredicate = true;
      if (resolvedValue === undefined || !condition.in.some((entry) => visibilityValuesMatch(resolvedValue, entry))) {
        return false;
      }
    }
    if (Object.prototype.hasOwnProperty.call(condition, "contains")) {
      evaluatedAnyPredicate = true;
      if (resolvedValue === undefined || !visibilityValueContains(resolvedValue, condition.contains)) {
        return false;
      }
    }

    return evaluatedAnyPredicate;
  }

  function resolveVisibilityKeypath(keypath, scope, state, context) {
    if (keypath === "." || keypath === "$") {
      if (scope === "item" || scope === "context") {
        return context;
      }
      return state ? state.rootData : undefined;
    }
    if (scope === "item" || scope === "context") {
      const contextValue = getByPath(context, keypath);
      if (contextValue !== undefined) {
        return contextValue;
      }
      return scope === "context" && state ? getByPath(state.rootData, keypath) : undefined;
    }
    return state ? getByPath(state.rootData, keypath) : undefined;
  }

  function visibilityValueContains(value, candidate) {
    if (typeof value === "string" && typeof candidate === "string") {
      return value.includes(candidate);
    }
    if (Array.isArray(value)) {
      return value.some((entry) => visibilityValuesMatch(entry, candidate));
    }
    return false;
  }

  function visibilityValuesMatch(lhs, rhs) {
    if (lhs === rhs) {
      return true;
    }
    if (typeof lhs === "number" && typeof rhs === "number") {
      return Number(lhs) === Number(rhs);
    }
    return false;
  }

  function applyDragAndDropModifiers(element, modifiers, state, path, context) {
    if (!(element instanceof HTMLElement) || !state || !modifiers || typeof modifiers !== "object") {
      return;
    }

    const draggableRole = typeof modifiers.draggableRole === "string" ? modifiers.draggableRole.trim() : "";
    if (draggableRole) {
      element.setAttribute("draggable", "true");
      element.dataset.draggableRole = draggableRole;
      element.classList.add("drag-source", `drag-role-${sanitizeClassName(draggableRole)}`);
      if (typeof modifiers.accessibilityDragLabel === "string" && modifiers.accessibilityDragLabel.trim()) {
        element.setAttribute("aria-label", modifiers.accessibilityDragLabel.trim());
      }

      const payloadKeypath = typeof modifiers.dragPayloadKeypath === "string"
        ? modifiers.dragPayloadKeypath.trim()
        : "";
      const resolveDragPayload = () => payloadKeypath
        ? resolveKeypath(payloadKeypath, state.rootData, context)
        : null;
      const initialDragPayload = resolveDragPayload();
      if (initialDragPayload !== undefined && initialDragPayload !== null) {
        element.dataset.dragPayload = String(initialDragPayload);
      }

      element.addEventListener("dragstart", (event) => {
        if (!event.dataTransfer) {
          return;
        }
        const dragPayload = resolveDragPayload();
        if (dragPayload !== undefined && dragPayload !== null) {
          element.dataset.dragPayload = String(dragPayload);
        }
        const transfer = {
          dragRole: draggableRole,
          dragPayload: dragPayload === undefined ? null : dragPayload,
        };
        event.stopPropagation();
        setHostDrag(state, transfer, element);
        event.dataTransfer.setData("application/x-cellprotocol-drag", JSON.stringify(transfer));
        event.dataTransfer.setData("text/plain", dragPreviewText(element));
        event.dataTransfer.effectAllowed = "all";
        const previewRole = typeof modifiers.dragPreviewRole === "string" ? modifiers.dragPreviewRole.trim() : "";
        if (previewRole || element.classList.contains("skeleton-component-surface")) {
          const ghost = buildDragGhost(element, previewRole || "component-card");
          document.body.appendChild(ghost);
          event.dataTransfer.setDragImage(ghost, 20, 20);
          window.setTimeout(() => ghost.remove(), 0);
        }
        element.classList.add("drag-active");
      });

      element.addEventListener("dragend", () => {
        element.classList.remove("drag-active");
        setHostDrag(state, null, null);
      });
    }

    const dropTargetRole = typeof modifiers.dropTargetRole === "string" ? modifiers.dropTargetRole.trim() : "";
    if (!dropTargetRole) {
      return;
    }

    const acceptedDragRoles = Array.isArray(modifiers.acceptedDragRoles)
      ? modifiers.acceptedDragRoles.filter((entry) => typeof entry === "string" && entry.trim()).map((entry) => entry.trim())
      : [];
    element.skeletonDrop = { modifiers, context, acceptedDragRoles };
    element.dataset.dropTargetRole = dropTargetRole;
    element.classList.add("drop-target", `drop-target-${sanitizeClassName(dropTargetRole)}`);
    if (typeof modifiers.accessibilityDropLabel === "string" && modifiers.accessibilityDropLabel.trim()) {
      element.setAttribute("aria-dropeffect", "execute");
      element.setAttribute("aria-label", modifiers.accessibilityDropLabel.trim());
    }

    element.addEventListener("dragover", (event) => {
      const transfer = parseDragTransfer(event) || state.dragContext.transfer;
      if (!dragRoleAccepted(transfer, acceptedDragRoles)) {
        return;
      }
      event.preventDefault();
      if (event.dataTransfer) {
        event.dataTransfer.dropEffect = dataTransferEffectForIntent(resolveDropIntent(modifiers.dropIntents, event.altKey));
      }
      updateDropTargetState(element, modifiers, state, context, "hovering");
    });

    element.addEventListener("dragleave", (event) => {
      if (!event.relatedTarget || !element.contains(event.relatedTarget)) {
        updateDropTargetState(element, modifiers, state, context, "idle");
      }
    });

    element.addEventListener("drop", (event) => {
      const transfer = parseDragTransfer(event) || state.dragContext.transfer;
      if (!dragRoleAccepted(transfer, acceptedDragRoles)) {
        return;
      }
      event.preventDefault();
      event.stopPropagation();
      updateDropTargetState(element, modifiers, state, context, "idle");

      setHostDrag(state, null, null);
      const dropActionKeypath = typeof modifiers.dropActionKeypath === "string" ? modifiers.dropActionKeypath.trim() : "";
      if (!dropActionKeypath) {
        return;
      }
      const dropIntent = resolveDropIntent(modifiers.dropIntents, event.altKey);
      const dropTargetPayloadKeypath = typeof modifiers.dropTargetPayloadKeypath === "string"
        ? modifiers.dropTargetPayloadKeypath.trim()
        : "";
      const dropTargetPayload = dropTargetPayloadKeypath
        ? resolveKeypath(dropTargetPayloadKeypath, state.rootData, context)
        : null;
      void dispatchAction(state, dropActionKeypath, {
        dragRole: transfer.dragRole,
        dragPayload: transfer.dragPayload ?? null,
        dropTargetRole,
        dropTargetPayload: dropTargetPayload === undefined ? null : dropTargetPayload,
        dropIntent,
        modifierActive: event.altKey === true,
      }, {
        trigger: "skeleton-drop",
        path,
        dropTargetRole,
        dropTargetPayload: dropTargetPayload === undefined ? null : dropTargetPayload,
      });
    });
  }

  function parseDragTransfer(event) {
    if (!event || !event.dataTransfer) {
      return null;
    }
    try {
      const raw = event.dataTransfer.getData("application/x-cellprotocol-drag");
      if (!raw) {
        return null;
      }
      const parsed = JSON.parse(raw);
      if (!parsed || typeof parsed !== "object" || typeof parsed.dragRole !== "string") {
        return null;
      }
      return {
        dragRole: parsed.dragRole.trim(),
        dragPayload: Object.prototype.hasOwnProperty.call(parsed, "dragPayload") ? parsed.dragPayload : null,
      };
    } catch (_) {
      return null;
    }
  }

  function dragRoleAccepted(transfer, acceptedDragRoles) {
    if (!transfer || !transfer.dragRole) {
      return false;
    }
    return acceptedDragRoles.includes(transfer.dragRole);
  }

  function resolveDropIntent(dropIntents, modifierActive) {
    const intents = Array.isArray(dropIntents)
      ? dropIntents.filter((entry) => typeof entry === "string" && entry.trim()).map((entry) => entry.trim())
      : [];
    if (modifierActive && intents.includes("copy")) {
      return "copy";
    }
    if (modifierActive && intents.includes("add")) {
      return "add";
    }
    return intents[0] || "add";
  }

  function dataTransferEffectForIntent(intent) {
    if (intent === "move") {
      return "move";
    }
    if (intent === "link") {
      return "link";
    }
    return "copy";
  }

  function dragPreviewText(element) {
    const raw = element.textContent || element.getAttribute("aria-label") || "";
    return raw.replace(/\s+/g, " ").trim().slice(0, 80);
  }

  function buildDragGhost(sourceElement, previewRole) {
    const ghost = document.createElement("div");
    ghost.className = `drag-ghost drag-ghost-${sanitizeClassName(previewRole)}`;
    ghost.style.position = "fixed";
    ghost.style.top = "-9999px";
    ghost.style.left = "-9999px";
    ghost.style.pointerEvents = "none";
    const component = sourceElement.matches(".skeleton-component-surface") ? sourceElement : sourceElement.querySelector(".skeleton-component-surface");
    if (component) {
      const preview = component.cloneNode(true);
      preview.querySelectorAll("[id]").forEach((node) => node.removeAttribute("id"));
      preview.querySelectorAll("button, input, textarea, select, a").forEach((node) => { node.tabIndex = -1; });
      preview.style.opacity = "1";
      ghost.setAttribute("aria-hidden", "true");
      ghost.inert = true;
      ghost.appendChild(preview);
      ghost.style.width = `${Math.min(320, sourceElement.getBoundingClientRect().width || 240)}px`;
    } else ghost.textContent = dragPreviewText(sourceElement) || "Flytt";
    return ghost;
  }

  function updateDropTargetState(element, modifiers, state, context, hint) {
    element.classList.remove("drop-hover", "drop-valid", "drop-invalid", "drop-denied", "drop-pending");
    if (hint !== "hovering") {
      element.removeAttribute("title");
      return;
    }
    element.classList.add("drop-hover");
    const validationKeypath = typeof modifiers.dropValidationStateKeypath === "string"
      ? modifiers.dropValidationStateKeypath.trim()
      : "";
    const validationState = validationKeypath ? resolveKeypath(validationKeypath, state.rootData, context) : null;
    if (typeof validationState === "string" && validationState.trim()) {
      element.classList.add(`drop-${sanitizeClassName(validationState.trim())}`);
    }
    const reasonKeypath = typeof modifiers.dropDeniedReasonKeypath === "string"
      ? modifiers.dropDeniedReasonKeypath.trim()
      : "";
    const deniedReason = reasonKeypath ? resolveKeypath(reasonKeypath, state.rootData, context) : null;
    if (typeof deniedReason === "string" && deniedReason.trim()) {
      element.title = deniedReason.trim();
    }
  }

  function sanitizeClassName(name) {
    return String(name).replace(/[^a-zA-Z0-9_-]+/g, "-");
  }

  async function dispatchAction(state, keypath, payload, meta) {
    let effectivePayload = payload;
    if (state.resolveButtonPayload) {
      effectivePayload = state.resolveButtonPayload({ keypath, payload, meta, state });
    }
    return await state.onAction(keypath, effectivePayload, meta);
  }

  function normalizeFileUploadSpec(raw) {
    const spec = raw && typeof raw === "object" ? raw : {};
    const acceptedContentTypes = Array.isArray(spec.acceptedContentTypes)
      ? spec.acceptedContentTypes
      : Array.isArray(spec.accept)
        ? spec.accept
        : [];
    return {
      ...spec,
      title: stringOrNull(spec.title) || stringOrNull(spec.label),
      subtitle: stringOrNull(spec.subtitle),
      helperText: stringOrNull(spec.helperText),
      valueKeypath: stringOrNull(spec.valueKeypath) || stringOrNull(spec.sourceKeypath),
      stateKeypath: stringOrNull(spec.stateKeypath),
      actionKeypath: stringOrNull(spec.actionKeypath) || stringOrNull(spec.targetKeypath),
      acceptedContentTypes: acceptedContentTypes.filter((entry) => typeof entry === "string" && entry.trim()).map((entry) => entry.trim()),
      allowsMultiple: spec.allowsMultiple === true || spec.multiple === true,
      supportsDrop: spec.supportsDrop === true,
      maxSizeBytes: Number.isFinite(spec.maxSizeBytes) ? spec.maxSizeBytes : null,
      uploadMode: typeof spec.uploadMode === "string" && spec.uploadMode.trim() ? spec.uploadMode.trim() : "base64",
      submitOnSelection: spec.submitOnSelection,
      emptyTitle: stringOrNull(spec.emptyTitle),
      emptyMessage: stringOrNull(spec.emptyMessage),
      modifiers: spec.modifiers && typeof spec.modifiers === "object" ? spec.modifiers : null,
    };
  }

  function stringOrNull(value) {
    return typeof value === "string" && value.trim() ? value : null;
  }

  function normalizeFileList(fileList, spec) {
    const files = Array.from(fileList || []).filter((file) => file instanceof File);
    return spec.allowsMultiple ? files : files.slice(0, 1);
  }

  function validateUploadFiles(files, spec) {
    if (!files.length) {
      return "No file selected.";
    }
    if (Number.isFinite(spec.maxSizeBytes) && spec.maxSizeBytes > 0) {
      const tooLarge = files.find((file) => file.size > spec.maxSizeBytes);
      if (tooLarge) {
        return `${tooLarge.name} is larger than ${formatByteSize(spec.maxSizeBytes)}.`;
      }
    }
    return "";
  }

  async function filesToTemporaryAttachmentPayload(files, spec) {
    const items = [];
    for (const file of files) {
      items.push(await fileToTemporaryAttachmentItem(file, spec));
    }
    if (items.length === 1) {
      return items[0];
    }
    return {
      items,
      count: items.length,
      uploadMode: spec.uploadMode,
    };
  }

  async function fileToTemporaryAttachmentItem(file, spec) {
    const payload = {
      displayName: file.name,
      mimeType: file.type || "",
      byteSize: file.size,
      kind: preferredUploadKind(file, spec.acceptedContentTypes),
      uploadMode: spec.uploadMode,
      lastModified: Number.isFinite(file.lastModified) ? file.lastModified : null,
    };

    if (spec.uploadMode === "metadata") {
      return payload;
    }

    const dataURL = await readFileAsDataURL(file);
    const commaIndex = dataURL.indexOf(",");
    const base64 = commaIndex >= 0 ? dataURL.slice(commaIndex + 1) : dataURL;

    if (spec.uploadMode === "chunked") {
      payload.chunks = chunkString(base64, 256 * 1024);
      payload.chunkEncoding = "base64";
      payload.chunkSize = 256 * 1024;
    } else {
      payload.dataBase64 = base64;
    }

    return payload;
  }

  function readFileAsDataURL(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result || ""));
      reader.onerror = () => reject(reader.error || new Error("Could not read selected file."));
      reader.readAsDataURL(file);
    });
  }

  function chunkString(value, chunkSize) {
    const chunks = [];
    for (let index = 0; index < value.length; index += chunkSize) {
      chunks.push(value.slice(index, index + chunkSize));
    }
    return chunks;
  }

  function preferredUploadKind(file, acceptedContentTypes) {
    const mime = String(file.type || "").toLowerCase();
    const accepted = (acceptedContentTypes || []).join(" ").toLowerCase();
    if (mime.startsWith("image/") || accepted.includes("image")) {
      return "image";
    }
    if (mime.startsWith("video/") || accepted.includes("video")) {
      return "video";
    }
    if (mime.startsWith("audio/") || accepted.includes("audio")) {
      return "audio";
    }
    if (mime === "application/pdf" || accepted.includes("pdf")) {
      return "document";
    }
    return "file";
  }

  function formatByteSize(bytes) {
    if (!Number.isFinite(bytes) || bytes <= 0) {
      return "0 B";
    }
    if (typeof Intl !== "undefined" && Intl.NumberFormat) {
      try {
        return new Intl.NumberFormat(undefined, { style: "unit", unit: "byte", unitDisplay: "narrow" }).format(bytes);
      } catch (_) {
        // Fall through to compact binary formatting.
      }
    }
    const units = ["B", "KB", "MB", "GB"];
    let value = bytes;
    let unit = 0;
    while (value >= 1024 && unit < units.length - 1) {
      value /= 1024;
      unit += 1;
    }
    return `${value.toFixed(unit === 0 ? 0 : 1)} ${units[unit]}`;
  }

  function updateTextBindings(state) {
    state.textBindings.forEach((binding) => {
      let rendered = binding.staticText;
      if (binding.keypath) {
        rendered = valueToDisplay(resolveKeypath(binding.keypath, state.rootData, binding.context));
      }

      if (binding.localization) {
        rendered = localizedText(state, binding.localization, rendered, binding.context);
      }
      // Localization v1 is plain text, including untrusted argument values.
      if (state.formatText && !binding.localization) {
        const formatted = state.formatText({
          keypath: binding.keypath,
          context: binding.context,
          value: rendered,
        });
        if (formatted && typeof formatted === "object" && typeof formatted.html === "string") {
          binding.element.innerHTML = formatted.html;
          return;
        }
      }

      if (binding.element.textContent !== (rendered ?? "")) binding.element.textContent = rendered ?? "";
    });
  }

  function localizedText(state, descriptor, fallback, context) {
    return state.localization && descriptor
      ? state.localization.resolve(descriptor, fallback ?? "", { item: context, context }).text
      : fallback ?? "";
  }

  function bindLocalizedText(state, element, descriptor, context, fallback, apply) {
    if (!descriptor) return;
    const binding = { element, descriptor, context, fallback, apply };
    state.localizationBindings.push(binding);
    apply(localizedText(state, descriptor, fallback(), context));
  }

  function updateLocalizationBindings(state) {
    state.localizationBindings.forEach((binding) => {
      if (state.rootElement.contains(binding.element)) {
        binding.apply(localizedText(state, binding.descriptor, binding.fallback(), binding.context));
      }
    });
  }

  function updateFieldBindings(state) {
    state.fieldBindings.forEach((binding) => {
      const isFocused = bindingHasFocus(binding);
      let nextValue = binding.staticText;
      if (binding.sourceKeypath) {
        const sourceValue = valueToDisplay(resolveKeypath(binding.sourceKeypath, state.rootData, binding.context));
        let localValue = readRememberedFieldValue(state, binding);
        if (isFocused && localValue !== null) {
          return;
        }
        if (localValue !== null && localValue === sourceValue) {
          forgetRememberedFieldValue(state, binding);
          localValue = null;
        }
        nextValue = localValue !== null ? localValue : sourceValue;
      } else {
        const localValue = readRememberedFieldValue(state, binding);
        if (localValue !== null) {
          nextValue = localValue;
        }
      }

      if (typeof nextValue !== "string") {
        nextValue = "";
      }

      if (isFocused) {
        return;
      }

      if (readFieldBindingValue(binding) !== nextValue) {
        writeFieldBindingValue(binding, nextValue, false);
      }
    });
  }

  function updateListBindings(state) {
    updateCollectionBindings(state.listBindings, state);
    updateTextBindings(state);
  }

  function updateGridBindings(state) {
    updateCollectionBindings(state.gridBindings, state);
    updateTextBindings(state);
  }

  function updateReferenceBindings(state) {
    updateCollectionBindings(state.referenceBindings, state);
    updateTextBindings(state);
  }

  function updateAttachmentBindings(state) {
    state.attachmentBindings.forEach((binding) => {
      if (!binding || !binding.spec) {
        return;
      }

      const attachments = attachmentValuesFromState(binding.spec, state.rootData, binding.context);
      const fieldState = binding.spec.stateKeypath
        ? resolveKeypath(binding.spec.stateKeypath, state.rootData, binding.context)
        : null;
      const signature = JSON.stringify({ attachments, fieldState });
      if (signature === binding.lastSignature) {
        return;
      }

      binding.lastSignature = signature;
      renderAttachmentBinding(binding, attachments, fieldState);
    });
  }

  function updateVisualizationBindings(state) {
    state.visualizationBindings.forEach((binding) => {
      const resolvedSpec = binding.keypath
        ? resolveKeypath(binding.keypath, state.rootData, binding.context)
        : binding.inlineSpec;
      const resolvedState = binding.stateKeypath
        ? resolveKeypath(binding.stateKeypath, state.rootData, binding.context)
        : null;
      const kind = String(binding.kind || "table").trim().toLowerCase();
      const signature = kind === "map"
        ? visualizationMapBindingSignature(resolvedSpec, resolvedState)
        : safeJSONStringify({
            spec: resolvedSpec,
            state: resolvedState,
          });
      if (signature === binding.lastSignature) {
        return;
      }
      binding.lastSignature = signature;
      renderVisualizationBinding(binding, state, resolvedSpec, resolvedState);
    });
  }

  function attachmentValuesFromState(spec, rootData, context) {
    if (!spec.valueKeypath) {
      return [];
    }
    const value = resolveKeypath(spec.valueKeypath, rootData, context);
    if (Array.isArray(value)) {
      return value.filter((entry) => entry && typeof entry === "object");
    }
    if (value && typeof value === "object") {
      if (Array.isArray(value.items)) {
        return value.items.filter((entry) => entry && typeof entry === "object");
      }
      return [value];
    }
    return [];
  }

  function renderAttachmentBinding(binding, attachments, fieldState) {
    if (!(binding.previewList instanceof HTMLElement) || !(binding.empty instanceof HTMLElement)) {
      return;
    }

    binding.previewList.innerHTML = "";
    const items = Array.isArray(attachments) ? attachments : [];
    binding.empty.hidden = items.length > 0;
    items.forEach((attachment) => {
      binding.previewList.appendChild(renderAttachmentPreview(attachment));
    });

    const phase = fieldState && typeof fieldState.phase === "string" ? fieldState.phase : "";
    const progress = fieldState && Number.isFinite(fieldState.progressFraction) ? fieldState.progressFraction : null;
    const errorMessage = fieldState && typeof fieldState.errorMessage === "string" ? fieldState.errorMessage : "";
    if (errorMessage) {
      binding.status.textContent = errorMessage;
      binding.status.dataset.tone = "error";
    } else if (phase === "uploading" || phase === "picking") {
      binding.status.textContent = progress === null ? "Uploading…" : `Uploading ${Math.round(progress * 100)}%`;
      binding.status.dataset.tone = "busy";
    } else if (phase === "attached") {
      binding.status.textContent = "Attachment ready.";
      binding.status.dataset.tone = "success";
    }
  }

  function renderAttachmentPreview(attachment) {
    const row = document.createElement("div");
    row.className = "skeleton-fileupload-preview";

    const thumb = document.createElement("div");
    thumb.className = "skeleton-fileupload-thumb";
    const previewURL = typeof attachment.previewURL === "string" ? attachment.previewURL : "";
    const mimeType = typeof attachment.mimeType === "string" ? attachment.mimeType : "";
    const kind = typeof attachment.kind === "string" ? attachment.kind : "";
    if (previewURL && (mimeType.startsWith("image/") || kind.toLowerCase() === "image")) {
      const image = document.createElement("img");
      image.src = previewURL;
      image.alt = "";
      thumb.appendChild(image);
    } else {
      thumb.textContent = uploadIconForKind(kind, mimeType);
    }

    const content = document.createElement("div");
    content.className = "skeleton-fileupload-preview-content";
    const name = document.createElement("div");
    name.className = "skeleton-fileupload-preview-name";
    name.textContent = attachment.displayName || "Attached file";
    content.appendChild(name);

    const meta = document.createElement("div");
    meta.className = "skeleton-fileupload-preview-meta";
    const parts = [];
    if (mimeType) {
      parts.push(mimeType);
    } else if (kind) {
      parts.push(kind);
    }
    if (Number.isFinite(attachment.byteSize)) {
      parts.push(formatByteSize(attachment.byteSize));
    }
    meta.textContent = parts.join(" · ") || "Ready";
    content.appendChild(meta);

    row.appendChild(thumb);
    row.appendChild(content);
    return row;
  }

  function uploadIconForKind(kind, mimeType) {
    const normalized = `${kind || ""} ${mimeType || ""}`.toLowerCase();
    if (normalized.includes("image")) {
      return "IMG";
    }
    if (normalized.includes("video")) {
      return "VID";
    }
    if (normalized.includes("audio")) {
      return "AUD";
    }
    if (normalized.includes("pdf") || normalized.includes("document")) {
      return "DOC";
    }
    return "FILE";
  }

  function flushDynamicBindings(state) {
    updateTreeBindings(state);
    updateVisibilityBindings(state);
    updateTextBindings(state);
    updateFieldBindings(state);
    updateAttachmentBindings(state);
    updateVisualizationBindings(state);
    updateTabBindings(state);
    updateNavigationBarBindings(state);
    updateListBindings(state);
    updateGridBindings(state);
    updateReferenceBindings(state);
    updateToggleBindings(state);
    updatePickerBindings(state);
    updateVisibilityBindings(state);
    updatePresentationBindings(state);

    // Grid/reference renders can create fresh nested bindings during the first pass.
    // Run a second shallow pass so nested lists/grids inside newly-created containers
    // receive their initial items before the UI becomes interactive.
    updateListBindings(state);
    updateGridBindings(state);
    updateReferenceBindings(state);
    updateTextBindings(state);
    updateFieldBindings(state);
    updateAttachmentBindings(state);
    updateVisualizationBindings(state);
    updateTabBindings(state);
    updateNavigationBarBindings(state);
    updateVisibilityBindings(state);
    updatePresentationBindings(state);
    // A tab pass can create fresh descendants after active tab state settles
    // (for example nested tabs rendered inside a newly selected parent tab).
    // Flush those bindings before returning so panel content is usable without
    // waiting for another server/browser update tick.
    updateListBindings(state);
    updateGridBindings(state);
    updateReferenceBindings(state);
    updateTextBindings(state);
    updateFieldBindings(state);
    updateAttachmentBindings(state);
    updateVisualizationBindings(state);
    updateToggleBindings(state);
    updatePickerBindings(state);
    updateNavigationBarBindings(state);
    updateVisibilityBindings(state);
    updatePresentationBindings(state);
    updateTreeBindings(state);
    updateComponentBindings(state);
    state.buttonBindings.forEach((binding) => {
      if (binding.pendingRequestCount > 0 || binding.button.classList.contains("is-acknowledged")) return;
      const label = resolvedButtonLabel(binding);
      setButtonLabelText(binding, label);
      if (binding.spec.modifiers?.accessibilityLabel) binding.button.setAttribute("aria-label", binding.spec.modifiers.accessibilityLabel);
    });
    updateTextBindings(state);
    updateFieldBindings(state);
    updateToggleBindings(state);
    updatePickerBindings(state);
    updateVisibilityBindings(state);
    updateLayoutContext(state);
    refreshDragStyles(state);
  }

  function updateTabBindings(state) {
    state.tabBindings.forEach((binding) => {
      const rows = resolveTabRows(binding, state);
      const rowsSignature = safeJSONStringify(rows.map((row, index) => ({
        index,
        id: tabIDForRow(binding, row),
        label: tabLabelForRow(binding, row),
      })));
      const nextActiveTabID = resolveActiveTabID(binding, state, rows);

      if (binding.lastRowsSignature !== rowsSignature) {
        binding.rows = rows;
        binding.lastRowsSignature = rowsSignature;
        binding.lastRenderedPanelID = null;
        renderTabsBinding(binding, state);
      }

      if (nextActiveTabID && nextActiveTabID !== binding.activeTabID) {
        binding.activeTabID = nextActiveTabID;
        binding.lastRenderedPanelID = null;
        renderTabsBinding(binding, state);
      }
    });
  }

  function resolveTabRows(binding, state) {
    if (binding.tabsKeypath) {
      const resolved = resolveKeypath(binding.tabsKeypath, state.rootData, binding.context);
      if (Array.isArray(resolved)) {
        return resolved;
      }
    }

    return binding.panels.map((panel, index) => ({
      id: panel && typeof panel.id === "string" ? panel.id : `tab-${index + 1}`,
      title: defaultTabTitle(panel && panel.id),
    }));
  }

  function resolveActiveTabID(binding, state, rows) {
    const rowIDs = rows.map((row) => tabIDForRow(binding, row)).filter(Boolean);
    const panelIDs = binding.panels.map((panel) => panel && panel.id).filter(Boolean);
    const validIDs = new Set(panelIDs.length ? panelIDs : rowIDs);
    let resolved = binding.activeTabStateKeypath
      ? resolveKeypath(binding.activeTabStateKeypath, state.rootData, binding.context)
      : null;

    if (Array.isArray(resolved)) {
      resolved = resolved.length ? resolved[0] : null;
    }
    if (resolved && typeof resolved === "object") {
      resolved = resolved.selectedValue || resolved.id || resolved.selected || null;
    }

    const candidate = resolved === null || resolved === undefined ? "" : String(resolved);
    if (
      binding.localSelectedTabID &&
      validIDs.has(binding.localSelectedTabID) &&
      Date.now() < binding.localSelectionExpiresAt &&
      candidate !== binding.localSelectedTabID
    ) {
      return binding.localSelectedTabID;
    }
    if (candidate === binding.localSelectedTabID) {
      binding.localSelectedTabID = "";
      binding.localSelectionExpiresAt = 0;
    }
    if (candidate && validIDs.has(candidate)) {
      return candidate;
    }
    const remembered = binding.memoryKey ? tabSelectionMemory.get(binding.memoryKey) : "";
    if (remembered && validIDs.has(remembered)) {
      return remembered;
    }
    if (remembered && binding.memoryKey) {
      tabSelectionMemory.delete(binding.memoryKey);
    }
    if (binding.activeTabID && validIDs.has(binding.activeTabID)) {
      return binding.activeTabID;
    }
    return panelIDs[0] || rowIDs[0] || "";
  }

  function renderTabsBinding(binding, state) {
    if (!binding || !(binding.tablist instanceof HTMLElement) || !(binding.panel instanceof HTMLElement)) {
      return;
    }

    const rows = binding.rows.length ? binding.rows : resolveTabRows(binding, state);
    binding.rows = rows;
    const activeTabID = resolveActiveTabID(binding, state, rows);
    binding.activeTabID = activeTabID;

    binding.tablist.innerHTML = "";
    if (rows.length === 0) {
      pruneDescendantBindings(state, binding.panel, binding);
      binding.panel.innerHTML = "";
      binding.lastRenderedPanelID = "";
      return;
    }

    rows.forEach((row, index) => {
      const id = tabIDForRow(binding, row);
      if (!id) {
        return;
      }
      const button = document.createElement("button");
      button.type = "button";
      button.className = "skeleton-tabs-tab";
      button.setAttribute("role", "tab");
      button.setAttribute("aria-selected", id === activeTabID ? "true" : "false");
      button.textContent = tabLabelForRow(binding, row) || defaultTabTitle(id);
      if (id === activeTabID) {
        button.classList.add("is-active");
      }
      button.addEventListener("click", (event) => {
        event.preventDefault();
        void selectTab(binding, state, row, id, index);
      });
      binding.tablist.appendChild(button);
    });

    if (binding.lastRenderedPanelID === activeTabID && binding.panel.childElementCount > 0) {
      return;
    }

    pruneDescendantBindings(state, binding.panel, binding);
    binding.panel.innerHTML = "";
    binding.lastRenderedPanelID = activeTabID;

    const activePanelIndex = Math.max(0, binding.panels.findIndex((panel) => panel && panel.id === activeTabID));
    const activePanel = binding.panels[activePanelIndex] || binding.panels[0];
    const content = activePanel && Array.isArray(activePanel.content) ? activePanel.content : [];
    if (activePanel && activePanel.modifiers) {
      applyElementModifiers(binding.panel, activePanel.modifiers, state, null, binding.context);
    }
    const pathOffset = binding.panels
      .slice(0, activePanelIndex)
      .reduce((sum, panel) => sum + (panel && Array.isArray(panel.content) ? panel.content.length : 0), 0);
    content.forEach((child, index) => {
      const childPath = typeof binding.path === "string" && binding.path.length > 0
        ? `${binding.path}.${pathOffset + index}`
        : null;
      binding.panel.appendChild(
        renderElement(decodeElement(child), state, binding.context, `tabs.${activeTabID}.${index}`, childPath)
      );
    });
    // No autoscroll here on purpose. This runs only when the active tab
    // actually changed, and a freshly switched panel belongs at its top. The
    // call that used to sit here passed an element into the object-shaped
    // queueWorkbenchAutoScroll and had silently been a no-op.
  }

  async function selectTab(binding, state, row, id, index) {
    if (!binding || !id) {
      return;
    }

    binding.activeTabID = id;
    binding.localSelectedTabID = id;
    // The optimistic highlight is held until the action settles, not for a
    // fixed stretch of wall clock. Five seconds was a guess about how long the
    // round trip takes, and when the guess was wrong the strip quietly fell
    // back to the previous tab while the panel already showed the new one — so
    // the tab a screen reader announced as selected was not the tab on screen.
    // A debug build on a loaded CI runner hit that every time; a fast machine
    // never did, which is why it read as a flaky test rather than a bug.
    // The ceiling below is only there so a never-settling action cannot pin the
    // strip forever; the `finally` in the dispatch below is what normally
    // releases it.
    binding.localSelectionExpiresAt = Date.now() + TAB_SELECTION_HOLD_CEILING_MS;
    if (binding.memoryKey) {
      tabSelectionMemory.set(binding.memoryKey, id);
    }
    binding.lastRenderedPanelID = null;
    renderTabsBinding(binding, state);
    refreshCollectionRenderState(state);

    if (!binding.selectionActionKeypath) {
      return;
    }

    const payload = {
      trigger: "select",
      selectedIndex: index,
      selected: row,
      selectedValue: id,
      id,
    };
    try {
      await dispatchAction(state, binding.selectionActionKeypath, payload, {
        trigger: "tabs-selection-action",
        binding,
        selectedIndex: index,
      });
    } catch (error) {
      console.warn("Skeleton tabs selection failed", error);
      // A refusal leaves the strip showing a tab the server never accepted, and
      // nothing else will correct it: the failed action brought no state to
      // apply. Releasing the highlight without redrawing would leave the lie on
      // screen, so the redraw happens here and only here.
      binding.localSelectedTabID = "";
      binding.localSelectionExpiresAt = 0;
      binding.lastRenderedPanelID = null;
      renderTabsBinding(binding, state);
      return;
    }
    // The server answered, and applying its state already redrew the strip.
    // Releasing the hold now just stops it from overriding what the server says
    // on the next render.
    binding.localSelectedTabID = "";
    binding.localSelectionExpiresAt = 0;
  }

  function tabIDForRow(binding, row) {
    const value = row && typeof row === "object"
      ? getByPath(row, binding.idKeypath)
      : row;
    return value === null || value === undefined ? "" : String(value);
  }

  function tabLabelForRow(binding, row) {
    const value = row && typeof row === "object"
      ? getByPath(row, binding.labelKeypath)
      : row;
    return value === null || value === undefined ? "" : String(value);
  }

  function defaultTabTitle(id) {
    return String(id || "Tab")
      .replace(/[-_]/g, " ")
      .replace(/([a-z])([A-Z])/g, "$1 $2")
      .replace(/\b\w/g, (match) => match.toUpperCase());
  }

  function tabMemoryKey(state, key, path, spec) {
    const rootID = state && state.rootElement && state.rootElement.id
      ? state.rootElement.id
      : "skeleton-root";
    const panels = Array.isArray(spec && spec.panels)
      ? spec.panels.map((panel) => panel && typeof panel.id === "string" ? panel.id : "").join("|")
      : "";
    return `${rootID}:${path || key || "tabs"}:${panels}`;
  }

  function updatePickerBindings(state) {
    state.pickerBindings.forEach((binding) => {
      const resolved = binding.keypath
        ? resolveKeypath(binding.keypath, state.rootData, binding.context)
        : binding.staticElements;
      const items = Array.isArray(resolved) ? resolved : [];
      const signature = buildListSignature(items);

      if (signature !== binding.lastSignature) {
        binding.lastSignature = signature;
        binding.items = items;
        renderPickerBinding(binding);
      }

      syncPickerSelectionFromState(binding, state);
    });
  }

  function updateCollectionBindings(bindings, state) {
    bindings.forEach((binding) => {
      const resolved = binding.keypath
        ? resolveKeypath(binding.keypath, state.rootData, binding.context)
        : [];
      const items = Array.isArray(resolved) ? resolved : [];
      const signature = buildListSignature(items);

      if (signature === binding.lastSignature) {
        return;
      }

      binding.lastSignature = signature;
      binding.rawItems = items;
      binding.items = flattenListTree(binding, items, state);
      binding.selectedIndices = reconcileSelectedIndices(binding.selectedIndices, binding.items.length);
      renderCollectionBinding(binding, state);
      if (binding.kind === "list") {
        syncListSelectionFromState(binding, state);
      }
    });

    bindings.forEach((binding) => {
      if (binding.kind === "list") {
        syncListSelectionFromState(binding, state);
      }
    });
  }

  // Multiple collection bindings can re-render inside one animation frame.
  // Keep the pre-render reader intent until the latest queued frame applies it.
  const pendingWorkbenchAutoScroll = new WeakMap();

  function renderCollectionBinding(binding, state) {
    if (!binding || !(binding.container instanceof HTMLElement)) {
      return;
    }

    const autoScroll = captureWorkbenchAutoScroll(binding.container, binding);
    pruneDescendantBindings(state, binding.container, binding);
    binding.container.innerHTML = "";

    const items = Array.isArray(binding.items) ? binding.items : [];
    if (!items.length) {
      // En tom liste sier ingenting selv. «Ingen elementer» sto her før og ble
      // overstyrt av tolv CSS-regler flate for flate, fordi teksten ikke hadde
      // noe formål: den doblet «Ventende: 0», den lå i Butler-loggen før første
      // ord, den sto i biblioteket. Elementet blir igjen som DOM-markør
      // (data-empty) så en flate som har noe å si om tomheten kan si det selv
      // - i skjelettet, eller i CSS via ::before - og så tester kan skille
      // «lastet og tom» fra «ikke lastet».
      const empty = document.createElement("div");
      empty.className = binding.kind === "grid" ? "skeleton-grid-empty" : "skeleton-list-empty";
      empty.dataset.empty = "true";
      empty.setAttribute("aria-hidden", "true");
      binding.container.appendChild(empty);
      queueWorkbenchAutoScroll(autoScroll);
      return;
    }

    const fragment = document.createDocumentFragment();
    items.forEach((item, index) => {
      if (binding.kind === "grid") {
        fragment.appendChild(renderGridCollectionItem(binding, state, item, index));
      } else {
        fragment.appendChild(renderCollectionRow(binding, state, item, index));
      }
    });

    binding.container.appendChild(fragment);
    queueWorkbenchAutoScroll(autoScroll);
  }

  function captureWorkbenchAutoScroll(element, binding) {
    if (!(element instanceof HTMLElement)) {
      return null;
    }
    // U3: a List with followTail follows its own nearest scroller, whatever its role.
    const scroller = binding && binding.followTail === true
      ? findFollowTailScroller(element)
      : element.closest(".style-role-chat-prompt-scroll, .style-role-component-panel-scroll");
    if (!(scroller instanceof HTMLElement)) {
      return null;
    }
    const pending = pendingWorkbenchAutoScroll.get(scroller);
    if (pending) {
      // innerHTML has already collapsed scrollTop, so the live DOM no longer
      // describes where the reader was before this render burst began.
      return {
        scroller,
        shouldScroll: pending.shouldScroll,
        scrollTop: pending.scrollTop
      };
    }
    // Capture this before collection rendering changes scrollHeight. A reader who
    // moved away from the bottom should keep the same reading position, so the
    // exact scrollTop is captured too: re-rendering clears innerHTML, which
    // collapses scrollTop to 0, and nothing else would restore it.
    const bottomDistance = scroller.scrollHeight - scroller.scrollTop - scroller.clientHeight;
    return {
      scroller,
      shouldScroll: bottomDistance < 48,
      scrollTop: scroller.scrollTop
    };
  }

  function queueWorkbenchAutoScroll(autoScroll) {
    if (!autoScroll || !(autoScroll.scroller instanceof HTMLElement)) {
      return;
    }
    const { scroller, shouldScroll, scrollTop } = autoScroll;
    pendingWorkbenchAutoScroll.set(scroller, autoScroll);
    window.requestAnimationFrame(() => {
      if (pendingWorkbenchAutoScroll.get(scroller) !== autoScroll) {
        return;
      }
      pendingWorkbenchAutoScroll.delete(scroller);
      if (!scroller.isConnected) {
        return;
      }
      if (shouldScroll === true) {
        scroller.scrollTop = scroller.scrollHeight;
        return;
      }
      // The re-render emptied the container, so the browser has already reset
      // scrollTop to 0. Put the reader back where they were instead of throwing
      // them to the top of the log.
      const maxScrollTop = Math.max(0, scroller.scrollHeight - scroller.clientHeight);
      const restored = Math.min(Math.max(0, scrollTop), maxScrollTop);
      if (scroller.scrollTop !== restored) {
        scroller.scrollTop = restored;
      }
    });
  }

  function renderGridCollectionItem(binding, state, item, index) {
    const card = document.createElement("article");
    card.className = "skeleton-grid-item";
    card.dataset.index = String(index);

    if (binding.rowSkeleton) {
      card.appendChild(renderElement(binding.rowSkeleton, state, item, `grid.row.${index}`, null));
    } else {
      card.appendChild(renderFallbackRow(item, binding.fallbackRowKeypath));
    }

    return card;
  }

  // ---- U2: tre-liste (childrenKeypath / expandedStateKeypath) ------------------------
  // Rows are flattened to the visible rows only, so selection, payloads and rendering
  // keep working on a plain index. Expansion lives in the renderer; toggling never
  // round-trips to the cell.

  function listRowIdentity(binding, item, pathKey) {
    if (item && typeof item === "object") {
      const idKey = binding.selectionValueKeypath;
      if (idKey && item[idKey] !== undefined && item[idKey] !== null) {
        return String(item[idKey]);
      }
      if (item.id !== undefined && item.id !== null) {
        return String(item.id);
      }
      if (item.uuid !== undefined && item.uuid !== null) {
        return String(item.uuid);
      }
    }
    return `#${pathKey}`;
  }

  function listRowChildren(binding, item) {
    if (!binding.childrenKeypath || !item || typeof item !== "object") {
      return [];
    }
    const direct = item[binding.childrenKeypath];
    if (Array.isArray(direct)) {
      return direct;
    }
    const resolved = resolveKeypath(binding.childrenKeypath, item, null);
    return Array.isArray(resolved) ? resolved : [];
  }

  function seedExpandedFromState(binding, state) {
    if (!binding.expandedStateKeypath) {
      if (!(binding.expanded instanceof Set)) {
        binding.expanded = new Set(["*"]);
      }
      return;
    }
    const value = resolveKeypath(binding.expandedStateKeypath, state.rootData, binding.context);
    const signature = JSON.stringify(value === undefined ? null : value);
    if (signature === binding.expandedSeedSignature && binding.expanded instanceof Set) {
      return;
    }
    binding.expandedSeedSignature = signature;
    if (value === "*") {
      binding.expanded = new Set(["*"]);
    } else if (Array.isArray(value)) {
      binding.expanded = new Set(value.map((entry) => String(entry)));
    } else {
      binding.expanded = new Set();
    }
  }

  function flattenListTree(binding, items, state) {
    const source = Array.isArray(items) ? items : [];
    if (!binding.childrenKeypath) {
      binding.rowMeta = [];
      return source;
    }
    seedExpandedFromState(binding, state);
    const expandAll = binding.expanded.has("*");
    const rows = [];
    const meta = [];
    const walk = (list, depth, prefix) => {
      list.forEach((item, position) => {
        const pathKey = prefix ? `${prefix}.${position}` : String(position);
        const identity = listRowIdentity(binding, item, pathKey);
        const children = listRowChildren(binding, item);
        const hasChildren = children.length > 0;
        const expanded = hasChildren && (expandAll || binding.expanded.has(identity));
        rows.push(item);
        meta.push({ depth, identity, hasChildren, expanded });
        if (expanded) {
          walk(children, depth + 1, pathKey);
        }
      });
    };
    walk(source, 0, "");
    binding.rowMeta = meta;
    return rows;
  }

  function toggleListRowExpansion(binding, state, rowMeta) {
    if (!(binding.expanded instanceof Set)) {
      binding.expanded = new Set();
    }
    if (binding.expanded.has("*")) {
      // Materialise "all expanded" into explicit identities before the first collapse.
      binding.expanded.delete("*");
      (binding.rowMeta || []).forEach((entry) => {
        if (entry.hasChildren && entry.expanded) {
          binding.expanded.add(entry.identity);
        }
      });
    }
    if (binding.expanded.has(rowMeta.identity)) {
      binding.expanded.delete(rowMeta.identity);
    } else {
      binding.expanded.add(rowMeta.identity);
    }
    const selectedIdentities = new Set();
    (binding.rowMeta || []).forEach((entry, index) => {
      if (binding.selectedIndices instanceof Set && binding.selectedIndices.has(index)) {
        selectedIdentities.add(entry.identity);
      }
    });
    binding.items = flattenListTree(binding, binding.rawItems, state);
    const nextSelected = new Set();
    (binding.rowMeta || []).forEach((entry, index) => {
      if (selectedIdentities.has(entry.identity)) {
        nextSelected.add(index);
      }
    });
    binding.selectedIndices = nextSelected;
    renderCollectionBinding(binding, state);
    refreshCollectionRenderState(state);
  }

  function makeTreeToggle(binding, state, rowMeta) {
    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "skeleton-list-row-toggle";
    if (!rowMeta.hasChildren) {
      toggle.classList.add("is-leaf");
      toggle.setAttribute("aria-hidden", "true");
      toggle.tabIndex = -1;
      toggle.disabled = true;
      return toggle;
    }
    toggle.setAttribute("aria-expanded", rowMeta.expanded ? "true" : "false");
    toggle.setAttribute("aria-label", rowMeta.expanded ? "Slå sammen" : "Utvid");
    toggle.textContent = rowMeta.expanded ? "\u25BE" : "\u25B8";
    toggle.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      toggleListRowExpansion(binding, state, rowMeta);
    });
    return toggle;
  }

  // ---- U3: følg halen -----------------------------------------------------------------

  function findFollowTailScroller(element) {
    let node = element instanceof HTMLElement ? element : null;
    while (node) {
      const overflowY = window.getComputedStyle(node).overflowY;
      if ((overflowY === "auto" || overflowY === "scroll") && node.scrollHeight > node.clientHeight) {
        return node;
      }
      if (overflowY === "auto" || overflowY === "scroll") {
        // Scrollable container that has not overflowed yet (first rows arriving).
        return node;
      }
      node = node.parentElement;
    }
    return null;
  }

  function renderCollectionRow(binding, state, item, index) {
    const row = document.createElement("article");
    row.className = "skeleton-list-row";
    const rowModifiers = binding.modifiers || {};
    if (rowModifiers.rowDecoration === "none") {
      row.classList.add("skeleton-row-plain");
      Object.assign(row.style, { border: "0", borderRadius: "0", boxShadow: "none", background: "transparent" });
    }
    if (rowModifiers.rowInsets) applyInsets(row, rowModifiers.rowInsets, 0);
    row.dataset.index = String(index);
    const rowMeta = Array.isArray(binding.rowMeta) && binding.rowMeta[index] ? binding.rowMeta[index] : null;
    if (rowMeta) {
      row.dataset.depth = String(rowMeta.depth);
      row.style.setProperty("--skeleton-list-depth", String(rowMeta.depth));
      if (rowMeta.hasChildren) {
        row.classList.add("has-children");
        row.setAttribute("aria-expanded", rowMeta.expanded ? "true" : "false");
      }
    }

    const isSelected = binding.kind === "list" && binding.selectedIndices instanceof Set
      ? binding.selectedIndices.has(index) || isCollectionItemSelected(item)
      : isCollectionItemSelected(item);
    const isSelectionPending = binding.kind === "list"
      && binding.pendingSelectedIndices instanceof Set
      && binding.pendingSelectedIndices.has(index);
    const hasSelectionUI = binding.kind === "list" && binding.selectionMode !== "none";
    const hasActivation = binding.kind === "list" && Boolean(binding.activationActionKeypath);

    if (hasSelectionUI) {
      row.classList.add("is-selectable");
    }
    if (isSelected) {
      row.classList.add("is-selected");
    }
    if (isSelectionPending) {
      row.classList.add("is-selection-pending");
    }
    resolveRowStyleClasses(item).forEach((className) => {
      row.classList.add(className);
    });

    const shell = document.createElement("div");
    shell.className = "skeleton-list-row-shell";

    if (hasSelectionUI) {
      shell.appendChild(makeSelectionMarker(binding, isSelected));
    }

    if (rowMeta && binding.childrenKeypath) {
      shell.appendChild(makeTreeToggle(binding, state, rowMeta));
    }
    const main = document.createElement("div");
    main.className = "skeleton-list-row-main";
    if (binding.rowSkeleton) {
      main.appendChild(renderElement(binding.rowSkeleton, state, item, `list.row.${index}`, null));
    } else {
      main.appendChild(renderFallbackRow(item, binding.fallbackRowKeypath));
    }
    shell.appendChild(main);

    if (hasSelectionUI && binding.selectionMode === "single") {
      shell.appendChild(makeSelectionMarker(binding, isSelected));
    }

    if (hasActivation) {
      const actionButton = document.createElement("button");
      actionButton.type = "button";
      actionButton.className = "skeleton-list-row-action";
      actionButton.textContent = "Åpne";
      actionButton.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        void handleListActivation(binding, state, index);
      });
      shell.appendChild(actionButton);
    }

    row.appendChild(shell);

    if (hasSelectionUI) {
      row.addEventListener("click", (event) => {
        if (isInteractiveTarget(event.target)) {
          return;
        }
        alignListSelectionWithVisibleRow(binding, index, row);
        const previousSelection = new Set(binding.selectedIndices instanceof Set ? binding.selectedIndices : []);
        const trigger = applyListSelectionChange(binding, index);
        if (!trigger) {
          return;
        }
        binding.pendingSelectedIndices = new Set(binding.selectedIndices);
        binding.selectionSyncSuspended = true;
        renderCollectionBinding(binding, state);
        refreshCollectionRenderState(state);
        void submitListSelectionChange(binding, state, trigger, previousSelection, index);
      });
    }

    return row;
  }

  function alignListSelectionWithVisibleRow(binding, index, row) {
    if (!binding || binding.selectionMode === "none" || !(row instanceof HTMLElement)) {
      return;
    }

    if (!(binding.selectedIndices instanceof Set)) {
      binding.selectedIndices = new Set();
    }

    const selectionMarker = row.querySelector(".skeleton-list-row-check");
    const itemAppearsSelected = Array.isArray(binding.items)
      && Number.isInteger(index)
      && isCollectionItemSelected(binding.items[index]);
    const markerAppearsSelected = selectionMarker
      && /\[x\]/i.test(selectionMarker.textContent || "");
    const rowAppearsSelected = row.classList.contains("is-selected")
      || row.classList.contains("is-selection-pending")
      || markerAppearsSelected
      || itemAppearsSelected;
    if (binding.selectionMode === "multiple") {
      if (rowAppearsSelected) {
        binding.selectedIndices.add(index);
      } else {
        binding.selectedIndices.delete(index);
      }
      return;
    }

    if (rowAppearsSelected) {
      binding.selectedIndices = new Set([index]);
    } else if (binding.selectedIndices.has(index)) {
      binding.selectedIndices.delete(index);
    }
  }

  function isCollectionItemSelected(item) {
    return item && typeof item === "object" && !Array.isArray(item)
      && (item.isSelected === true || item.selected === true);
  }

  function makeSelectionMarker(binding, isSelected) {
    const marker = document.createElement("span");
    marker.className = "skeleton-list-row-check";
    if (binding.selectionMode === "multiple") {
      marker.textContent = isSelected ? "[x]" : "[ ]";
    } else {
      marker.textContent = isSelected ? "[x]" : "";
      if (!isSelected) {
        marker.classList.add("is-hidden");
      }
    }
    return marker;
  }

  function normalizeSelectionMode(mode) {
    switch (mode) {
      case "single":
      case "multiple":
        return mode;
      default:
        return "none";
    }
  }

  function normalizeSelectionPayloadMode(mode) {
    switch (mode) {
      case "item":
      case "item_id":
      case "selected_items":
      case "selected_ids":
        return mode;
      default:
        return null;
    }
  }

  function reconcileSelectedIndices(selectedIndices, itemCount) {
    const reconciled = new Set();
    if (!(selectedIndices instanceof Set) || itemCount <= 0) {
      return reconciled;
    }

    selectedIndices.forEach((index) => {
      if (Number.isInteger(index) && index >= 0 && index < itemCount) {
        reconciled.add(index);
      }
    });
    return reconciled;
  }

  function applyListSelectionChange(binding, index) {
    if (!binding || binding.selectionMode === "none") {
      return null;
    }

    if (!(binding.selectedIndices instanceof Set)) {
      binding.selectedIndices = new Set();
    }

    if (binding.selectionMode === "single") {
      if (binding.selectedIndices.has(index)) {
        if (binding.allowsEmptySelection) {
          binding.selectedIndices.clear();
          return "deselect";
        }
        return null;
      }
      binding.selectedIndices = new Set([index]);
      return "select";
    }

    if (binding.selectedIndices.has(index)) {
      if (!binding.allowsEmptySelection && binding.selectedIndices.size === 1) {
        return null;
      }
      binding.selectedIndices.delete(index);
      return "deselect";
    }

    binding.selectedIndices.add(index);
    return "select";
  }

  async function handleListActivation(binding, state, index) {
    if (!binding || !binding.activationActionKeypath) {
      return;
    }

    const previousSelection = new Set(binding.selectedIndices instanceof Set ? binding.selectedIndices : []);
    if (binding.selectionMode !== "none") {
      binding.selectedIndices = activationSelection(binding, index);
      renderCollectionBinding(binding, state);
      refreshCollectionRenderState(state);
    }

    try {
      // Aktivering gjelder alltid nøyaktig én rad — også i lister uten
      // selection-UI (selectionMode "none"), der selectedIndices aldri settes.
      // Uten dette fikk serveren `selected: null` og svarte
      // «component surface id is required» mens knappen så ut som om den
      // ikke gjorde noe.
      const payload = buildListSelectionPayload(binding, "activate", index);
      if (payload.selectionMode !== "multiple" && (payload.selected === null || payload.selected === undefined)) {
        payload.selectedIndex = index;
        payload.selected = payload.interacted;
      }
      await dispatchAction(state, binding.activationActionKeypath, payload, {
        trigger: "list-activate",
        binding,
        selectedIndices: sortedSelectionIndices(binding.selectedIndices),
      });
    } catch (error) {
      binding.selectedIndices = previousSelection;
      renderCollectionBinding(binding, state);
      refreshCollectionRenderState(state);
      console.warn("Skeleton list activation failed", error);
    }
  }

  function activationSelection(binding, index) {
    if (binding.selectionMode === "multiple") {
      const updated = new Set(binding.selectedIndices instanceof Set ? binding.selectedIndices : []);
      updated.add(index);
      return updated;
    }
    return new Set([index]);
  }

  async function submitListSelectionChange(binding, state, trigger, previousSelection, interactedIndex = null) {
    if (!binding) {
      return;
    }

    if (!binding.selectionActionKeypath) {
      binding.pendingSelectedIndices = null;
      binding.selectionSyncSuspended = false;
      return;
    }

    let failed = false;
    try {
      const payload = buildListSelectionPayload(binding, trigger, interactedIndex);
      await dispatchAction(state, binding.selectionActionKeypath, payload, {
        trigger: "list-selection-action",
        binding,
        selectedIndices: sortedSelectionIndices(binding.selectedIndices),
      });
    } catch (error) {
      failed = true;
      binding.selectedIndices = new Set(previousSelection instanceof Set ? previousSelection : []);
      console.warn("Skeleton list selection failed", error);
    } finally {
      binding.pendingSelectedIndices = null;
      binding.selectionSyncSuspended = false;
      if (!failed) {
        syncListSelectionFromState(binding, state);
      }
      renderCollectionBinding(binding, state);
      refreshCollectionRenderState(state);
    }
  }

  function syncListSelectionFromState(binding, state) {
    if (!binding || binding.kind !== "list" || !binding.selectionStateKeypath) {
      return;
    }
    if (binding.selectionSyncSuspended) {
      return;
    }

    const resolvedSelection = resolveKeypath(binding.selectionStateKeypath, state.rootData, binding.context);
    const resolvedSignature = safeJSONStringify(resolvedSelection);
    if (resolvedSignature === binding.lastResolvedSelectionSignature) {
      return;
    }

    binding.lastResolvedSelectionSignature = resolvedSignature;
    const nextIndices = resolveListSelectedIndices(binding, resolvedSelection);
    const currentSignature = safeJSONStringify(sortedSelectionIndices(binding.selectedIndices));
    const nextSignature = safeJSONStringify(sortedSelectionIndices(nextIndices));
    if (currentSignature === nextSignature) {
      return;
    }

    binding.selectedIndices = nextIndices;
    renderCollectionBinding(binding, state);
  }

  function resolveListSelectedIndices(binding, selectionState) {
    if (!binding || binding.kind !== "list") {
      return new Set();
    }

    if (selectionState === null || selectionState === undefined) {
      return new Set();
    }

    if (binding.selectionMode === "multiple") {
      if (selectionState && typeof selectionState === "object" && Array.isArray(selectionState.selectedIndices)) {
        return new Set(
          selectionState.selectedIndices.filter((index) => Number.isInteger(index) && index >= 0 && index < binding.items.length)
        );
      }

      const selectionValues = Array.isArray(selectionState)
        ? selectionState
        : selectionState && typeof selectionState === "object" && Array.isArray(selectionState.selected)
          ? selectionState.selected
          : [];

      return resolveListSelectedIndicesByValue(binding, selectionValues);
    }

    if (selectionState && typeof selectionState === "object" && Number.isInteger(selectionState.selectedIndex)) {
      return selectionState.selectedIndex >= 0 && selectionState.selectedIndex < binding.items.length
        ? new Set([selectionState.selectedIndex])
        : new Set();
    }

    const selectedValue =
      selectionState && typeof selectionState === "object" && Object.prototype.hasOwnProperty.call(selectionState, "selected")
        ? selectionState.selected
        : selectionState;

    return resolveListSelectedIndicesByValue(binding, [selectedValue]);
  }

  function resolveListSelectedIndicesByValue(binding, selectionValues) {
    const payloadMode = effectiveSelectionPayloadMode(
      binding.selectionPayloadMode,
      binding.selectionMode === "multiple" ? "multiple" : "single"
    );
    const indices = [];

    selectionValues.forEach((selectedValue) => {
      if (selectedValue === null || selectedValue === undefined) {
        return;
      }

      const matchIndex = binding.items.findIndex((item) => {
        try {
          return selectionPayloadValue(binding, item, payloadMode) === selectedValue;
        } catch (_error) {
          return false;
        }
      });

      if (matchIndex >= 0) {
        indices.push(matchIndex);
      }
    });

    return new Set(indices);
  }

  function buildListSelectionPayload(binding, trigger, interactedIndex = null) {
    const rows = Array.isArray(binding.items) ? binding.items : [];
    const selectedIndices = sortedSelectionIndices(binding.selectedIndices);
    const selectionMode = effectiveSelectionMode(binding.selectionMode, selectedIndices.length);
    const payloadMode = effectiveSelectionPayloadMode(binding.selectionPayloadMode, selectionMode);
    const payload = {
      selectionMode,
      trigger,
    };
    const hasInteractedRow = Number.isInteger(interactedIndex) && interactedIndex >= 0 && interactedIndex < rows.length;

    if (hasInteractedRow) {
      payload.interactedIndex = interactedIndex;
      payload.interacted = selectionPayloadValue(binding, rows[interactedIndex], payloadMode);
    }

    if (selectionMode === "multiple") {
      payload.selectedIndices = selectedIndices;
      payload.selected = selectedIndices.map((index) => selectionPayloadValue(binding, rows[index], payloadMode));
      return payload;
    }

    const selectedIndex = selectedIndices.length ? selectedIndices[0] : null;
    payload.selectedIndex = selectedIndex;
    payload.selected = selectedIndex === null
      ? null
      : selectionPayloadValue(binding, rows[selectedIndex], payloadMode);
    return payload;
  }

  function effectiveSelectionMode(configuredMode, selectionCount) {
    if (configuredMode === "multiple") {
      return "multiple";
    }
    if (configuredMode === "single") {
      return "single";
    }
    return selectionCount > 1 ? "multiple" : "single";
  }

  function effectiveSelectionPayloadMode(configuredMode, selectionMode) {
    if (configuredMode) {
      return configuredMode;
    }
    return selectionMode === "multiple" ? "selected_items" : "item";
  }

  function selectionPayloadValue(binding, row, payloadMode) {
    switch (payloadMode) {
      case "item":
      case "selected_items":
        return row;
      case "item_id":
      case "selected_ids": {
        const selectedValue = binding.selectionValueKeypath
          ? getByPath(row, binding.selectionValueKeypath)
          : undefined;
        if (selectedValue === undefined) {
          throw new Error(`Missing selection value at keypath '${binding.selectionValueKeypath || ""}'.`);
        }
        return selectedValue;
      }
      default:
        return row;
    }
  }

  function sortedSelectionIndices(selectedIndices) {
    if (!(selectedIndices instanceof Set)) {
      return [];
    }
    return Array.from(selectedIndices.values())
      .filter((index) => Number.isInteger(index))
      .sort((left, right) => left - right);
  }

  function resolveRowStyleClasses(item) {
    if (!item || typeof item !== "object" || Array.isArray(item)) {
      return [];
    }

    const rawClasses = item.rowStyleClasses;
    if (!Array.isArray(rawClasses)) {
      return [];
    }

    return rawClasses
      .map((entry) => typeof entry === "string" ? sanitizeClassName(entry) : "")
      .filter((entry) => entry.length > 0);
  }

  function refreshCollectionRenderState(state) {
    flushDynamicBindings(state);
  }

  function pruneDescendantBindings(state, container, protectedBinding) {
    state.treeBindings = state.treeBindings.filter((entry) => entry === protectedBinding || !isBindingContainerInsideContainer(entry.container, container));
    state.localizationBindings = state.localizationBindings.filter((entry) => !isBindingElementInsideContainer(entry.element, container));
    state.textBindings = state.textBindings.filter((entry) => !isBindingElementInsideContainer(entry.element, container));
    state.fieldBindings = state.fieldBindings.filter((entry) => !isBindingElementInsideContainer(entry.element, container));
    state.attachmentBindings = state.attachmentBindings.filter((entry) => !isBindingElementInsideContainer(entry.wrapper, container));
    state.toggleBindings = state.toggleBindings.filter((entry) => !isBindingElementInsideContainer(entry.element, container));
    state.pickerBindings = state.pickerBindings.filter((entry) => !isBindingElementInsideContainer(entry.element, container));
    state.tabBindings = state.tabBindings.filter((entry) => entry === protectedBinding || !isBindingElementInsideContainer(entry.wrapper, container));
    state.navigationBarBindings = state.navigationBarBindings.filter((entry) => !isBindingElementInsideContainer(entry.navigation, container));
    state.buttonBindings = state.buttonBindings.filter((entry) => !isBindingElementInsideContainer(entry.button, container));
    state.visibilityBindings = state.visibilityBindings.filter((entry) => !isBindingElementInsideContainer(entry.element, container));
    state.presentationBindings = state.presentationBindings.filter((entry) => {
      if (!isBindingElementInsideContainer(entry.element, container)) {
        return true;
      }
      cleanupPresentationBinding(entry);
      return false;
    });
    state.listBindings = state.listBindings.filter((entry) => entry === protectedBinding || !isBindingContainerInsideContainer(entry.container, container));
    state.gridBindings = state.gridBindings.filter((entry) => entry === protectedBinding || !isBindingContainerInsideContainer(entry.container, container));
    state.referenceBindings = state.referenceBindings.filter((entry) => entry === protectedBinding || !isBindingContainerInsideContainer(entry.container, container));
  }

  function isBindingElementInsideContainer(element, container) {
    return element instanceof HTMLElement && container.contains(element);
  }

  function isBindingContainerInsideContainer(candidateContainer, container) {
    return candidateContainer instanceof HTMLElement && candidateContainer !== container && container.contains(candidateContainer);
  }

  function isInteractiveTarget(target) {
    return target instanceof Element && Boolean(target.closest("button, a, input, textarea, select, label, [contenteditable='true']"));
  }

  function updateToggleBindings(state) {
    state.toggleBindings.forEach((binding) => {
      if (!binding || !binding.keypath) {
        return;
      }
      const value = resolveKeypath(binding.keypath, state.rootData, binding.context);
      const normalized = valueToBool(value, binding.element.checked);
      if (binding.element.checked !== normalized) {
        binding.element.checked = normalized;
      }
    });
  }

  function renderFallbackRow(item, fallbackKeypath) {
    const row = document.createElement("div");
    row.className = "skeleton-list-row-fallback";

    if (item && typeof item === "object") {
      if (fallbackKeypath === "participants") {
        row.innerHTML = [
          `<div class=\"skeleton-text\">${escapeHTML(String(item.displayName || "unknown"))}</div>`,
          `<div class=\"skeleton-text\">${escapeHTML(String(item.uuid || "-"))}</div>`,
        ].join("");
        return row;
      }

      if (fallbackKeypath === "messages") {
        const createdAt = typeof item.createdAt === "number" ? new Date(item.createdAt * 1000).toLocaleTimeString() : "-";
        const contentType = String(item.contentType || "text/plain");
        const body = contentType === "text/markdown"
          ? renderMarkdownLite(String(item.text || ""))
          : `<pre>${escapeHTML(String(item.text || ""))}</pre>`;

        row.innerHTML = [
          `<header class=\"skeleton-message-meta\">`,
          `<span><strong>${escapeHTML(String(item.authorDisplayName || "unknown"))}</strong> <em>${escapeHTML(contentType)}</em></span>`,
          `<span>${escapeHTML(createdAt)}</span>`,
          `</header>`,
          `<div class=\"skeleton-message-body\">${body}</div>`,
        ].join("");
        return row;
      }
    }

    row.textContent = valueToDisplay(item);
    return row;
  }

  function inferFallbackRowKeypath(keypath) {
    if (typeof keypath !== "string") {
      return null;
    }
    if (keypath.endsWith("participants")) {
      return "participants";
    }
    if (keypath.endsWith("messages")) {
      return "messages";
    }
    return null;
  }

  function resolveKeypath(keypath, rootData, context) {
    if (!keypath || typeof keypath !== "string") {
      return null;
    }

    const contextValue = getByPath(context, keypath);
    if (contextValue !== undefined) {
      return contextValue;
    }

    return getByPath(rootData, keypath);
  }

  function getByPath(source, path) {
    if (!source || typeof source !== "object") {
      return undefined;
    }

    const normalized = String(path)
      .replace(/\[(\d+)\]/g, ".$1")
      .split(".")
      .filter(Boolean);

    let current = source;
    for (let index = 0; index < normalized.length; index += 1) {
      const key = normalized[index];
      if (current && typeof current === "object" && key in current) {
        current = current[key];
      } else {
        return undefined;
      }
    }
    return current;
  }

  function valueToDisplay(value) {
    if (value === null || value === undefined) {
      return "";
    }
    if (typeof value === "string") {
      return value;
    }
    if (typeof value === "number" || typeof value === "boolean") {
      return String(value);
    }
    return safeJSONStringify(value);
  }

  function valueToBool(value, fallback) {
    if (typeof value === "boolean") {
      return value;
    }
    if (typeof value === "number") {
      return value !== 0;
    }
    if (typeof value === "string") {
      const lowered = value.trim().toLowerCase();
      if (lowered === "true" || lowered === "1" || lowered === "yes" || lowered === "on") {
        return true;
      }
      if (lowered === "false" || lowered === "0" || lowered === "no" || lowered === "off") {
        return false;
      }
    }
    return Boolean(fallback);
  }

  function buildListSignature(items) {
    return safeJSONStringify(
      items.map((item) => {
        if (item && typeof item === "object") {
          if (typeof item.id === "string") {
            return `${item.id}:${item.version || ""}:${item.updatedAt || item.createdAt || ""}`;
          }
          if (typeof item.uuid === "string") {
            return `${item.uuid}:${item.lastSeenAt || ""}`;
          }
        }
        return item;
      })
    );
  }

  function renderPickerBinding(binding) {
    if (!binding || !(binding.element instanceof HTMLSelectElement)) {
      return;
    }

    const select = binding.element;
    const previousValue = select.value;
    select.innerHTML = "";

    if (binding.allowsEmptySelection) {
      const placeholder = document.createElement("option");
      placeholder.value = "";
      placeholder.textContent = binding.placeholder;
      select.appendChild(placeholder);
    }

    const items = Array.isArray(binding.items) ? binding.items : [];
    items.forEach((item, index) => {
      const option = document.createElement("option");
      option.value = String(index);
      option.textContent = pickerLabelForItem(binding, item);
      select.appendChild(option);
    });

    const selectedIndex = sortedSelectionIndices(binding.selectedIndices)[0];

    if (
      Number.isInteger(selectedIndex) &&
      Array.from(select.options).some((option) => option.value === String(selectedIndex))
    ) {
      select.value = String(selectedIndex);
    } else if (previousValue && Array.from(select.options).some((option) => option.value === previousValue)) {
      select.value = previousValue;
    } else if (binding.allowsEmptySelection) {
      select.value = "";
    } else if (items.length > 0) {
      select.value = "0";
      binding.selectedIndices = new Set([0]);
    }
  }

  function pickerLabelForItem(binding, item) {
    if (binding.optionLabelKeypath) {
      const nested = getByPath(item, binding.optionLabelKeypath);
      if (nested !== undefined && nested !== null) {
        return valueToDisplay(nested);
      }
    }
    return valueToDisplay(item);
  }

  function syncPickerSelectionFromState(binding, state) {
    if (!(binding.element instanceof HTMLSelectElement)) {
      return;
    }

    const resolvedSignature = safeJSONStringify(
      binding.selectionStateKeypath
        ? resolveKeypath(binding.selectionStateKeypath, state.rootData, binding.context)
        : null
    );

    if (resolvedSignature === binding.lastResolvedSelectionSignature) {
      return;
    }

    binding.lastResolvedSelectionSignature = resolvedSignature;
    const selectedIndex = resolvePickerSelectedIndex(binding, state);
    if (selectedIndex === null) {
      binding.selectedIndices = new Set();
      if (binding.allowsEmptySelection) {
        binding.element.value = "";
      }
      return;
    }

    if (binding.items[selectedIndex] === undefined) {
      return;
    }

    binding.selectedIndices = new Set([selectedIndex]);
    binding.element.value = String(selectedIndex);
  }

  function resolvePickerSelectedIndex(binding, state) {
    if (!binding.selectionStateKeypath) {
      return sortedSelectionIndices(binding.selectedIndices)[0] ?? null;
    }

    const selectionState = resolveKeypath(binding.selectionStateKeypath, state.rootData, binding.context);
    if (selectionState === null || selectionState === undefined) {
      return null;
    }

    if (typeof selectionState === "object" && Number.isInteger(selectionState.selectedIndex)) {
      return selectionState.selectedIndex;
    }

    // En liste godtar bade {selected: verdi} og verdien selv. Plukkeren krevde
    // tidligere objektformen, saa den samme tilstanden ga valgt rad i en liste
    // og ingenting i en plukker. Na er de to enige.
    const selectedValue =
      typeof selectionState === "object"
        && Object.prototype.hasOwnProperty.call(selectionState, "selected")
        ? selectionState.selected
        : selectionState;

    if (selectedValue === null || selectedValue === undefined) {
      return null;
    }

    const payloadMode = effectiveSelectionPayloadMode(binding.selectionPayloadMode, "single");
    const matchIndex = binding.items.findIndex((item) => {
      try {
        return selectionPayloadValue(binding, item, payloadMode) === selectedValue;
      } catch (_error) {
        return false;
      }
    });

    return matchIndex >= 0 ? matchIndex : sortedSelectionIndices(binding.selectedIndices)[0] ?? null;
  }

  async function submitPickerSelectionChange(binding, state, trigger, previousIndex) {
    if (!binding || !binding.selectionActionKeypath) {
      return;
    }

    try {
      const payload = buildListSelectionPayload(binding, trigger);
      await dispatchAction(state, binding.selectionActionKeypath, payload, {
        trigger: "picker-selection-action",
        binding,
        selectedIndices: sortedSelectionIndices(binding.selectedIndices),
      });
    } catch (error) {
      console.warn("Skeleton picker selection failed", error);
      binding.selectedIndices = Number.isInteger(previousIndex) ? new Set([previousIndex]) : new Set();
      if (binding.element instanceof HTMLSelectElement) {
        binding.element.value = Number.isInteger(previousIndex) ? String(previousIndex) : "";
      }
    }
  }

  function applyFieldValue(element, nextValue, preserveCaret) {
    if (!isEditableTextControl(element)) {
      return;
    }

    if (preserveCaret && document.activeElement === element) {
      const start = element.selectionStart;
      const end = element.selectionEnd;
      element.value = nextValue;
      if (typeof start === "number" && typeof end === "number") {
        const safeStart = Math.min(start, element.value.length);
        const safeEnd = Math.min(end, element.value.length);
        element.setSelectionRange(safeStart, safeEnd);
      }
      return;
    }

    element.value = nextValue;
  }

  function insertToken(element, token, fallbackText) {
    if (!isEditableTextControl(element)) {
      return;
    }

    const start = element.selectionStart;
    const end = element.selectionEnd;
    const selection = element.value.slice(start, end);
    const replacement = token.replaceAll("text", selection || fallbackText || "text");

    element.value = `${element.value.slice(0, start)}${replacement}${element.value.slice(end)}`;
    const caret = start + replacement.length;
    element.setSelectionRange(caret, caret);
    element.focus({ preventScroll: true });
  }

  function isEditableTextControl(element) {
    if (element instanceof HTMLTextAreaElement) {
      return true;
    }
    return element instanceof HTMLInputElement && element.type === "text";
  }

  function readFieldBindingValue(binding) {
    if (!binding) {
      return "";
    }
    if (typeof binding.readValue === "function") {
      return String(binding.readValue() ?? "");
    }
    if (binding.element && "value" in binding.element) {
      return String(binding.element.value ?? "");
    }
    return "";
  }

  function writeFieldBindingValue(binding, nextValue, preserveCaret) {
    if (!binding) {
      return;
    }
    if (typeof binding.writeValue === "function") {
      binding.writeValue(String(nextValue ?? ""), Boolean(preserveCaret));
      return;
    }
    applyFieldValue(binding.element, String(nextValue ?? ""), Boolean(preserveCaret));
  }

  function insertTokenIntoBinding(binding, token, fallbackText) {
    if (!binding) {
      return;
    }
    if (typeof binding.insertToken === "function") {
      binding.insertToken(token, fallbackText);
      return;
    }
    insertToken(binding.element, token, fallbackText);
  }

  function focusFieldBinding(binding) {
    if (!binding) {
      return;
    }
    if (typeof binding.focus === "function") {
      binding.focus();
      return;
    }
    if (binding.element && typeof binding.element.focus === "function") {
      binding.element.focus({ preventScroll: true });
    }
  }

  function bindingHasFocus(binding) {
    if (!binding) {
      return false;
    }
    if (typeof binding.isFocused === "function") {
      return Boolean(binding.isFocused());
    }
    return document.activeElement === binding.element;
  }

  function syncRichTextAreaBinding(binding, state) {
    const nextValue = readFieldBindingValue(binding);
    rememberLocalFieldValue(state, binding, nextValue);
    if (state.onFieldInput) {
      state.onFieldInput(binding, nextValue);
    }
  }

  function fieldBindingMemoryKey(path, targetKeypath, sourceKeypath) {
    const normalizedPath = typeof path === "string" ? path.trim() : "";
    if (normalizedPath) {
      return normalizedPath;
    }

    const normalizedTarget = typeof targetKeypath === "string" ? targetKeypath.trim() : "";
    if (normalizedTarget) {
      return `target:${normalizedTarget}`;
    }

    const normalizedSource = typeof sourceKeypath === "string" ? sourceKeypath.trim() : "";
    if (normalizedSource) {
      return `source:${normalizedSource}`;
    }

    return "";
  }

  function rememberLocalFieldValue(state, binding, value) {
    if (!state || !state.localFieldValues || !binding || (binding.sourceKeypath && !binding.targetKeypath)) {
      return;
    }

    const memoryKey = typeof binding.memoryKey === "string" ? binding.memoryKey : "";
    if (!memoryKey) {
      return;
    }

    state.localFieldValues.set(memoryKey, String(value ?? ""));
  }

  function readRememberedFieldValue(state, binding) {
    if (!state || !state.localFieldValues || !binding || (binding.sourceKeypath && !binding.targetKeypath)) {
      return null;
    }

    const memoryKey = typeof binding.memoryKey === "string" ? binding.memoryKey : "";
    if (!memoryKey || !state.localFieldValues.has(memoryKey)) {
      return null;
    }

    return String(state.localFieldValues.get(memoryKey) ?? "");
  }

  function forgetRememberedFieldValue(state, binding) {
    if (!state || !state.localFieldValues || !binding) {
      return;
    }

    const memoryKey = typeof binding.memoryKey === "string" ? binding.memoryKey : "";
    if (!memoryKey) {
      return;
    }

    state.localFieldValues.delete(memoryKey);
  }

  function applyRichTextToken(editor, token, fallbackText) {
    const normalizedToken = String(token || "").trim();
    if (!normalizedToken) {
      return;
    }

    const selection = window.getSelection();
    const replacementText = normalizedToken.replaceAll("text", selectedPlainText(editor, selection) || fallbackText || "text");

    if (normalizedToken === "**text**") {
      applyRichTextCommand(editor, "bold", replacementText);
      return;
    }
    if (normalizedToken === "*text*") {
      applyRichTextCommand(editor, "italic", replacementText);
      return;
    }
    if (normalizedToken === "`code`" || normalizedToken === "`text`") {
      applyRichTextCommand(editor, "code", replacementText);
      return;
    }
    if (normalizedToken.startsWith("- ")) {
      applyRichTextCommand(editor, "bullet", replacementText);
      return;
    }
    if (normalizedToken.startsWith("> ")) {
      applyRichTextCommand(editor, "quote", replacementText);
      return;
    }

    insertPlainTextAtSelection(editor, replacementText);
  }

  function applyRichTextCommand(editor, command, fallbackText) {
    editor.focus({ preventScroll: true });
    switch (command) {
      case "bold":
        document.execCommand("styleWithCSS", false, false);
        document.execCommand("bold");
        break;
      case "italic":
        document.execCommand("styleWithCSS", false, false);
        document.execCommand("italic");
        break;
      case "bullet":
        if (!hasTextSelection(editor) && fallbackText) {
          insertPlainTextAtSelection(editor, fallbackText);
        }
        document.execCommand("insertUnorderedList");
        break;
      case "quote":
        if (!hasTextSelection(editor) && fallbackText) {
          insertPlainTextAtSelection(editor, fallbackText);
        }
        document.execCommand("formatBlock", false, "blockquote");
        break;
      case "code":
        wrapSelectionInInlineCode(editor, fallbackText);
        break;
      default:
        break;
    }
    normalizeRichEditor(editor);
  }

  function setRichEditorMarkdown(editor, nextValue) {
    const markdown = String(nextValue || "").replaceAll("\r\n", "\n").replaceAll("\r", "\n");
    if (!markdown.trim()) {
      editor.innerHTML = "";
      return;
    }
    editor.innerHTML = renderMarkdownLite(markdown);
    normalizeRichEditor(editor);
  }

  function normalizeRichEditor(editor) {
    if (!(editor instanceof HTMLElement)) {
      return;
    }

    const walker = document.createTreeWalker(editor, NodeFilter.SHOW_ELEMENT, null);
    const staleNodes = [];
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (!(node instanceof HTMLElement)) {
        continue;
      }
      if (node.tagName === "DIV" && node.parentElement === editor) {
        staleNodes.push(node);
      }
      if (node.tagName === "B") {
        swapElementTag(node, "strong");
      }
      if (node.tagName === "I") {
        swapElementTag(node, "em");
      }
    }

    staleNodes.forEach((node) => {
      const paragraph = document.createElement("p");
      while (node.firstChild) {
        paragraph.appendChild(node.firstChild);
      }
      node.replaceWith(paragraph);
    });

    if (editor.innerHTML === "<br>") {
      editor.innerHTML = "";
    }
  }

  function swapElementTag(node, nextTagName) {
    if (!(node instanceof HTMLElement) || !node.ownerDocument) {
      return;
    }
    const replacement = node.ownerDocument.createElement(nextTagName);
    Array.from(node.attributes).forEach((attribute) => {
      replacement.setAttribute(attribute.name, attribute.value);
    });
    while (node.firstChild) {
      replacement.appendChild(node.firstChild);
    }
    node.replaceWith(replacement);
  }

  function hasTextSelection(editor) {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0 || selection.isCollapsed) {
      return false;
    }
    const range = selection.getRangeAt(0);
    return editor.contains(range.commonAncestorContainer);
  }

  function selectedPlainText(editor, selection) {
    if (!selection || selection.rangeCount === 0) {
      return "";
    }
    const range = selection.getRangeAt(0);
    if (!editor.contains(range.commonAncestorContainer)) {
      return "";
    }
    return range.toString();
  }

  function insertPlainTextAtSelection(editor, text) {
    editor.focus({ preventScroll: true });
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) {
      editor.appendChild(document.createTextNode(text));
      return;
    }
    const range = selection.getRangeAt(0);
    if (!editor.contains(range.commonAncestorContainer)) {
      editor.appendChild(document.createTextNode(text));
      return;
    }
    range.deleteContents();
    const node = document.createTextNode(text);
    range.insertNode(node);
    range.setStartAfter(node);
    range.collapse(true);
    selection.removeAllRanges();
    selection.addRange(range);
  }

  function wrapSelectionInInlineCode(editor, fallbackText) {
    editor.focus({ preventScroll: true });
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) {
      insertPlainTextAtSelection(editor, fallbackText || "code");
      return;
    }
    const range = selection.getRangeAt(0);
    if (!editor.contains(range.commonAncestorContainer)) {
      insertPlainTextAtSelection(editor, fallbackText || "code");
      return;
    }

    const code = document.createElement("code");
    if (range.collapsed) {
      code.textContent = fallbackText || "code";
      range.insertNode(code);
      range.setStartAfter(code);
      range.collapse(true);
      selection.removeAllRanges();
      selection.addRange(range);
      return;
    }

    try {
      const fragment = range.extractContents();
      code.appendChild(fragment);
      range.insertNode(code);
      range.selectNodeContents(code);
      selection.removeAllRanges();
      selection.addRange(range);
    } catch (_error) {
      insertPlainTextAtSelection(editor, fallbackText || selection.toString() || "code");
    }
  }

  function serializeRichMarkdown(editor) {
    if (!(editor instanceof HTMLElement)) {
      return "";
    }

    normalizeRichEditor(editor);
    const blocks = [];
    Array.from(editor.childNodes).forEach((node) => {
      serializeRichBlock(node, blocks);
    });
    return normalizeRichMarkdownOutput(blocks.join("\n\n"));
  }

  function serializeRichBlock(node, blocks) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = normalizeInlineWhitespace(node.textContent || "");
      if (text) {
        blocks.push(text);
      }
      return;
    }

    if (!(node instanceof HTMLElement)) {
      return;
    }

    const tagName = node.tagName.toLowerCase();
    if (tagName === "ul") {
      const items = Array.from(node.children)
        .filter((child) => child.tagName.toLowerCase() === "li")
        .map((child) => `- ${serializeInlineMarkdown(child).trim()}`)
        .filter(Boolean);
      if (items.length) {
        blocks.push(items.join("\n"));
      }
      return;
    }

    if (tagName === "blockquote") {
      const quote = serializeInlineMarkdown(node).trim();
      if (quote) {
        blocks.push(quote.split("\n").map((line) => `> ${line}`).join("\n"));
      }
      return;
    }

    if (tagName === "p" || tagName === "div") {
      const paragraph = serializeInlineMarkdown(node).trim();
      if (paragraph) {
        blocks.push(paragraph);
      }
      return;
    }

    if (tagName === "br") {
      blocks.push("");
      return;
    }

    const fallback = serializeInlineMarkdown(node).trim();
    if (fallback) {
      blocks.push(fallback);
    }
  }

  function serializeInlineMarkdown(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      return escapeMarkdownText(node.textContent || "");
    }

    if (!(node instanceof HTMLElement)) {
      return "";
    }

    const tagName = node.tagName.toLowerCase();
    if (tagName === "br") {
      return "\n";
    }

    const content = Array.from(node.childNodes).map((child) => serializeInlineMarkdown(child)).join("");

    if (tagName === "strong" || tagName === "b") {
      return content ? `**${content}**` : "";
    }
    if (tagName === "em" || tagName === "i") {
      return content ? `*${content}*` : "";
    }
    if (tagName === "code") {
      return content ? `\`${content.replaceAll("`", "\\`")}\`` : "";
    }

    return content;
  }

  function normalizeInlineWhitespace(input) {
    return String(input || "").replace(/\u00a0/g, " ").replace(/\s+/g, " ").trim();
  }

  function escapeMarkdownText(input) {
    return String(input || "")
      .replaceAll("\\", "\\\\")
      .replaceAll("`", "\\`")
      .replaceAll("*", "\\*");
  }

  function normalizeRichMarkdownOutput(input) {
    return String(input || "")
      .replace(/\r\n/g, "\n")
      .replace(/\r/g, "\n")
      .replace(/\n{3,}/g, "\n\n")
      .trim();
  }

  function safeJSONStringify(value) {
    try {
      return JSON.stringify(value, null, 2);
    } catch (_error) {
      return String(value);
    }
  }

  function escapeHTML(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function renderMarkdownLite(input) {
    const text = String(input).replaceAll("\r\n", "\n").replaceAll("\r", "\n");
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

  global.HavenSkeletonRuntime = {
    createRenderer,
    validateSkeleton,
    resolveNavigationURL,
  };
})(window);
