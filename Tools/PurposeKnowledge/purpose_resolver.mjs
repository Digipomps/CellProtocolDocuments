import fs from "node:fs";

const DEFAULT_TEMPLATES = new Set([
  "purpose://project-work.overview-and-sharing",
  "purpose://questionnaire.campaign.complete"
]);

const PROTECTED_PARENT_MATCHES = new Set([
  ...DEFAULT_TEMPLATES,
  "purpose://contact.communication"
]);

const DEFAULT_CROSS_CUTTING_ROOTS = new Set([
  "purpose://quality",
  "purpose://governance",
  "purpose://validation",
  "purpose://knowledge",
  "purpose://grounding"
]);

export function loadPurposeKnowledge({
  knowledgePath = "Book/haven_purpose_knowledge_base_v0.json",
  indexPath = "Book/haven_purpose_knowledge_base_index_v0.json"
} = {}) {
  const knowledgeBase = JSON.parse(fs.readFileSync(knowledgePath, "utf8"));
  const index = JSON.parse(fs.readFileSync(indexPath, "utf8"));
  return new PurposeKnowledgeResolver(knowledgeBase, index);
}

export class PurposeKnowledgeResolver {
  constructor(knowledgeBase, index) {
    this.knowledgeBase = knowledgeBase;
    this.index = index;
    this.nodes = knowledgeBase.nodes ?? [];
    this.nodeByRef = new Map(this.nodes.map((node) => [node.purposeRef, node]));
    this.indexNodeByRef = new Map((index.nodes ?? []).map((node) => [node.purposeRef, node]));
    this.childrenByRef = new Map();
    for (const node of this.nodes) {
      if (!node.parentRef) continue;
      const children = this.childrenByRef.get(node.parentRef) ?? [];
      children.push(node.purposeRef);
      this.childrenByRef.set(node.parentRef, children);
    }
    for (const children of this.childrenByRef.values()) {
      children.sort((left, right) => this.ordinal(left) - this.ordinal(right));
    }
    this.aliasEntries = Object.entries(index.aliasMap ?? {}).sort((left, right) => right[0].length - left[0].length);
    this.crossCuttingRoots = DEFAULT_CROSS_CUTTING_ROOTS;
  }

  resolvePrompt(prompt, options = {}) {
    const normalizedPrompt = normalize(prompt);
    const rawTokens = tokenParts(prompt);
    const tokens = this.filteredTokens(rawTokens, normalizedPrompt);
    const scores = new Map();
    const reasons = new Map();

    for (const [alias, refs] of this.aliasEntries) {
      if (alias.length < 4) continue;
      const aliasTokens = tokenParts(alias);
      const aliasMatches = aliasTokens.length === 1
        ? tokens.includes(alias)
        : normalizedPrompt === alias || normalizedPrompt.includes(alias);
      if (aliasMatches) {
        const weight = alias.includes("://") ? 20 : Math.min(24, 8 + tokenParts(alias).length * 3);
        for (const ref of refs) {
          this.addScore(scores, reasons, ref, weight, `alias:${alias}`);
        }
      }
    }

    for (const token of tokens) {
      const refs = this.index.tokenPostings?.[token] ?? [];
      const tokenWeight = refs.length === 0 ? 0 : Math.max(0.75, 4 / Math.sqrt(refs.length));
      for (const ref of refs) {
        this.addScore(scores, reasons, ref, tokenWeight, `token:${token}`);
      }
    }

    for (const capability of options.visibleCapabilities ?? []) {
      for (const key of capabilityKeys(capability)) {
        const normalized = normalize(key);
        for (const [capabilityKey, refs] of Object.entries(this.index.capabilityPostings ?? {})) {
          if (normalized.includes(capabilityKey) || capabilityKey.includes(normalized)) {
            for (const ref of refs) {
              this.addScore(scores, reasons, ref, 8, `capability:${capabilityKey}`);
            }
          }
        }
      }
    }

    this.applyNegationGuards(normalizedPrompt, scores, reasons);

    const ranked = [...scores.entries()]
      .map(([purposeRef, score]) => {
        const indexNode = this.indexNodeByRef.get(purposeRef);
        return {
          purposeRef,
          score: round(score + (indexNode?.depth ?? 0) * 0.15),
          depth: indexNode?.depth ?? 0,
          goalRef: this.nodeByRef.get(purposeRef)?.goal?.goalRef ?? null,
          status: this.nodeByRef.get(purposeRef)?.status ?? "unknown",
          reasons: [...(reasons.get(purposeRef) ?? [])].slice(0, 8)
        };
      })
      .filter((item) => item.score >= (options.minRawScore ?? 2.8))
      .sort((left, right) => right.score - left.score || right.depth - left.depth || left.purposeRef.localeCompare(right.purposeRef));

    const topScore = ranked[0]?.score ?? 0;
    const relativeCutoff = options.relativeCutoff ?? 0.25;
    const selectedRanked = this.pruneGenericAncestors(
      ranked.filter((item) => item.score >= Math.max(options.minRawScore ?? 2.8, topScore * relativeCutoff))
    );
    const topPurposeRefs = selectedRanked.slice(0, options.limit ?? 12).map((item) => item.purposeRef);
    const expandedPurposeRefs = this.expandCoverage(topPurposeRefs);
    const goalRefs = expandedPurposeRefs.map((ref) => this.nodeByRef.get(ref)?.goal?.goalRef).filter(Boolean);
    const nearestSharedPurposeRef = this.lowestCommonAncestor(this.primaryRefs(topPurposeRefs));

    if (topPurposeRefs.length === 0) {
      const unknownRef = "purpose://prompt.unknown";
      return {
        schema: "haven.purpose-knowledge-resolution.v0",
        input: { text: prompt },
        status: "unknown",
        topPurposeRefs: [unknownRef],
        expandedPurposeRefs: [unknownRef],
        goalRefs: [this.nodeByRef.get(unknownRef)?.goal?.goalRef].filter(Boolean),
        nearestSharedPurposeRef: unknownRef,
        ranked,
        sideEffectFree: true,
        mutatesPerspective: false,
        mutatesEntity: false
      };
    }

    return {
      schema: "haven.purpose-knowledge-resolution.v0",
      input: { text: prompt },
      status: "resolved",
      topPurposeRefs,
      expandedPurposeRefs,
      goalRefs: stableUnique(goalRefs),
      nearestSharedPurposeRef,
      ranked,
      sideEffectFree: true,
      mutatesPerspective: false,
      mutatesEntity: false
    };
  }

  expandCoverage(refs) {
    const result = [];
    const add = (ref) => {
      if (!ref || result.includes(ref)) return;
      result.push(ref);
    };
    for (const ref of refs) {
      add(ref);
      const node = this.nodeByRef.get(ref);
      for (const facetRef of node?.facetRefs ?? []) add(facetRef);
      if (DEFAULT_TEMPLATES.has(ref)) {
        for (const child of this.descendants(ref)) add(child);
      }
    }
    const nearest = this.lowestCommonAncestor(this.primaryRefs(refs));
    if (nearest) add(nearest);
    if (refs.some((ref) => ref.startsWith("purpose://project-work."))) {
      add("purpose://project-work.overview-and-sharing");
      add("purpose://gui.quality.functional-accessible");
      add("purpose://access.audit.privacy");
      add("purpose://test.acceptance.project-work");
    }
    if (refs.some((ref) => ref.startsWith("purpose://questionnaire."))) {
      add("purpose://questionnaire.campaign.complete");
      add("purpose://gui.quality.functional-accessible");
      add("purpose://questionnaire.access.audit");
      add("purpose://access.audit.privacy");
      add("purpose://test.acceptance.questionnaire");
      add("purpose://preference.owner-controlled");
      add("purpose://source.methodology.current");
    }
    if (refs.some((ref) => ref.startsWith("purpose://event.") || ref.startsWith("purpose://contact."))) {
      add("purpose://access.audit.privacy");
    }
    if (refs.some((ref) => ref.startsWith("purpose://personal-context."))) {
      add("purpose://access.audit.privacy");
    }
    return stableUnique(result);
  }

  descendants(ref) {
    const result = [];
    const visit = (current) => {
      for (const child of this.childrenByRef.get(current) ?? []) {
        result.push(child);
        visit(child);
      }
    };
    visit(ref);
    return result;
  }

  primaryRefs(refs) {
    const primary = refs.filter((ref) => !this.isCrossCutting(ref));
    return primary.length ? primary : refs;
  }

  isCrossCutting(ref) {
    const chain = this.chain(ref);
    return chain.some((candidate) => this.crossCuttingRoots.has(candidate));
  }

  pruneGenericAncestors(items) {
    return items.filter((item) => {
      if (PROTECTED_PARENT_MATCHES.has(item.purposeRef)) return true;
      return !items.some((other) => {
        if (other.purposeRef === item.purposeRef) return false;
        if (other.score < item.score * 0.75) return false;
        return this.isAncestor(item.purposeRef, other.purposeRef);
      });
    });
  }

  isAncestor(ancestorRef, descendantRef) {
    const ancestor = this.indexNodeByRef.get(ancestorRef);
    const descendant = this.indexNodeByRef.get(descendantRef);
    if (!ancestor || !descendant) return false;
    return ancestor.entry <= descendant.entry && descendant.exit <= ancestor.exit;
  }

  lowestCommonAncestor(refs) {
    const knownRefs = stableUnique(refs).filter((ref) => this.indexNodeByRef.has(ref));
    if (knownRefs.length === 0) return null;
    let shared = this.ancestorBits(knownRefs[0]);
    for (const ref of knownRefs.slice(1)) {
      shared &= this.ancestorBits(ref);
    }
    let best = null;
    for (const node of this.index.nodes ?? []) {
      const mask = 1n << BigInt(node.ordinal);
      if ((shared & mask) === 0n) continue;
      if (!best || node.depth > best.depth) best = node;
    }
    return best?.purposeRef ?? null;
  }

  chain(ref) {
    const node = this.nodeByRef.get(ref);
    if (!node) return [];
    const result = [];
    let cursor = node;
    while (cursor) {
      result.push(cursor.purposeRef);
      cursor = cursor.parentRef ? this.nodeByRef.get(cursor.parentRef) : null;
    }
    return result.reverse();
  }

  ancestorBits(ref) {
    return BigInt(this.indexNodeByRef.get(ref)?.ancestorBitsetHex ?? "0x0");
  }

  ordinal(ref) {
    return this.indexNodeByRef.get(ref)?.ordinal ?? Number.MAX_SAFE_INTEGER;
  }

  addScore(scores, reasons, ref, delta, reason) {
    if (!this.nodeByRef.has(ref)) return;
    scores.set(ref, (scores.get(ref) ?? 0) + delta);
    const reasonSet = reasons.get(ref) ?? new Set();
    reasonSet.add(reason);
    reasons.set(ref, reasonSet);
  }

  applyNegationGuards(normalizedPrompt, scores, reasons) {
    const guards = [
      {
        pattern: /\b(ikke|ikkje|not)\s+(lag|lage|opprett|opprette|create|build)\b.{0,80}\b(sporreundersokelse|questionnaire|survey)\b/,
        subtree: "purpose://questionnaire.campaign.complete",
        alsoRemove: ["purpose://digital-work.collect-structured-input"],
        reason: "negated-questionnaire"
      },
      {
        pattern: /\b(trenger ikke|treng ikkje|do not need|dont need)\b.{0,80}\b(sporreundersokelse|questionnaire|survey)\b/,
        subtree: "purpose://questionnaire.campaign.complete",
        alsoRemove: ["purpose://digital-work.collect-structured-input"],
        reason: "negated-questionnaire"
      },
      {
        pattern: /\b(ikke|ikkje|not)\s+(lag|lage|opprett|opprette|create|build)\b.{0,80}\b(prosjekt\w*|project\w*)\b/,
        subtree: "purpose://project-work.overview-and-sharing",
        alsoRemove: ["purpose://digital-work.coordinate"],
        reason: "negated-project-work"
      }
    ];
    for (const guard of guards) {
      if (!guard.pattern.test(normalizedPrompt)) continue;
      for (const ref of [guard.subtree, ...(guard.alsoRemove ?? []), ...this.descendants(guard.subtree)]) {
        scores.delete(ref);
        const reasonSet = reasons.get(ref) ?? new Set();
        reasonSet.add(guard.reason);
        reasons.set(ref, reasonSet);
      }
    }
  }

  filteredTokens(rawTokens) {
    const stop = new Set([
      "jeg", "meg", "du", "det", "den", "der", "som", "for", "med", "til", "og", "eller", "men", "kan", "skal", "vil", "må", "ma", "nå", "no", "en", "et", "the", "and", "or", "to", "with", "for", "can", "you", "please", "just"
      , "hva", "hvor", "ka", "er", "pa", "på", "ha", "fa", "få", "kunne", "bare", "dette", "denne", "eg", "han", "hun", "henne", "etterpa", "etterpå", "na", "ikke", "ikkje", "lager"
    ]);
    return stableUnique(rawTokens.filter((token) => token.length >= 2 && !stop.has(token)));
  }
}

export function normalize(value) {
  return String(value ?? "")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/æ/g, "ae")
    .replace(/ø/g, "o")
    .replace(/å/g, "a")
    .replace(/[^a-z0-9:/._-]+/g, " ")
    .trim()
    .replace(/\s+/g, " ");
}

export function tokenParts(value) {
  return normalize(value)
    .split(/[\s:/._-]+/)
    .filter(Boolean);
}

function capabilityKeys(capability) {
  if (typeof capability === "string") return [capability];
  if (!capability || typeof capability !== "object") return [];
  return [
    capability.id,
    capability.endpoint,
    capability.name,
    capability.title,
    ...(capability.keypaths ?? []),
    ...(capability.purposeRefs ?? [])
  ].filter(Boolean).map(String);
}

function stableUnique(values) {
  const seen = new Set();
  const result = [];
  for (const value of values) {
    if (value == null || seen.has(value)) continue;
    seen.add(value);
    result.push(value);
  }
  return result;
}

function round(value) {
  return Math.round(value * 1000) / 1000;
}
