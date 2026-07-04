#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";

const [, , inputPath = "Book/haven_purpose_knowledge_base_v0.json", outputPath = "Book/haven_purpose_knowledge_base_index_v0.json"] = process.argv;

const sourceText = fs.readFileSync(inputPath, "utf8");
const knowledgeBase = JSON.parse(sourceText);
const nodes = knowledgeBase.nodes ?? [];

if (!knowledgeBase.rootPurposeRef) {
  throw new Error("Knowledge base is missing rootPurposeRef");
}

const refToNode = new Map();
for (const node of nodes) {
  if (!node.purposeRef) {
    throw new Error("Node is missing purposeRef");
  }
  if (refToNode.has(node.purposeRef)) {
    throw new Error(`Duplicate purposeRef: ${node.purposeRef}`);
  }
  refToNode.set(node.purposeRef, node);
}

for (const node of nodes) {
  if (node.parentRef && !refToNode.has(node.parentRef)) {
    throw new Error(`Missing parent for ${node.purposeRef}: ${node.parentRef}`);
  }
}

const ordinalByRef = new Map(nodes.map((node, index) => [node.purposeRef, index]));
const childrenByRef = new Map();
for (const node of nodes) {
  if (node.parentRef) {
    const children = childrenByRef.get(node.parentRef) ?? [];
    children.push(node.purposeRef);
    childrenByRef.set(node.parentRef, children);
  }
}

for (const children of childrenByRef.values()) {
  children.sort((left, right) => ordinalByRef.get(left) - ordinalByRef.get(right));
}

const depthByRef = new Map();
const entryByRef = new Map();
const exitByRef = new Map();
const ancestorBitsByRef = new Map();
let cursor = 0;

function walk(ref, depth, inheritedBits) {
  const ordinal = ordinalByRef.get(ref);
  const ownBit = 1n << BigInt(ordinal);
  const bits = inheritedBits | ownBit;
  depthByRef.set(ref, depth);
  ancestorBitsByRef.set(ref, bits);
  entryByRef.set(ref, cursor++);
  for (const child of childrenByRef.get(ref) ?? []) {
    walk(child, depth + 1, bits);
  }
  exitByRef.set(ref, cursor);
}

walk(knowledgeBase.rootPurposeRef, 0, 0n);

if (entryByRef.size !== nodes.length) {
  const unreachable = nodes.map((node) => node.purposeRef).filter((ref) => !entryByRef.has(ref));
  throw new Error(`Unreachable nodes from root: ${unreachable.join(", ")}`);
}

function normalize(value) {
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

function tokenParts(value) {
  return normalize(value)
    .split(/[\s:/._-]+/)
    .filter((token) => token.length >= 2);
}

function addPosting(map, key, ref) {
  const normalized = normalize(key);
  if (!normalized) return;
  const list = map.get(normalized) ?? new Set();
  list.add(ref);
  map.set(normalized, list);
}

function addTokenPostings(map, value, ref) {
  for (const token of tokenParts(value)) {
    addPosting(map, token, ref);
  }
}

const aliasMap = new Map();
const tokenPostings = new Map();
const capabilityPostings = new Map();
const goalPostings = new Map();

for (const node of nodes) {
  const ref = node.purposeRef;
  addPosting(aliasMap, ref, ref);
  addPosting(aliasMap, node.title, ref);
  addTokenPostings(tokenPostings, ref, ref);
  addTokenPostings(tokenPostings, node.title, ref);
  addTokenPostings(tokenPostings, node.summary, ref);

  for (const alias of node.aliases ?? []) {
    addPosting(aliasMap, alias, ref);
    addTokenPostings(tokenPostings, alias, ref);
  }
  for (const alias of node.matchingHints?.aliases ?? []) {
    addPosting(aliasMap, alias, ref);
    addTokenPostings(tokenPostings, alias, ref);
  }
  for (const token of node.matchingHints?.tokens ?? []) {
    addTokenPostings(tokenPostings, token, ref);
  }
  for (const interest of node.interests ?? []) {
    addTokenPostings(tokenPostings, interest, ref);
  }
  for (const capability of node.capabilityHints ?? []) {
    addPosting(capabilityPostings, capability, ref);
    addTokenPostings(tokenPostings, capability, ref);
  }
  if (node.goal?.goalRef) {
    addPosting(goalPostings, node.goal.goalRef, ref);
    addTokenPostings(tokenPostings, node.goal.goalRef, ref);
  }
  addTokenPostings(tokenPostings, node.goal?.outcome, ref);
  for (const signal of node.goal?.successSignals ?? []) {
    addTokenPostings(tokenPostings, signal, ref);
  }
}

function postingsObject(map) {
  return Object.fromEntries(
    [...map.entries()]
      .sort(([left], [right]) => left.localeCompare(right))
      .map(([key, refs]) => [
        key,
        [...refs].sort((left, right) => ordinalByRef.get(left) - ordinalByRef.get(right))
      ])
  );
}

function bitsToHex(bits) {
  const minWidth = Math.max(1, Math.ceil(nodes.length / 4));
  return `0x${bits.toString(16).padStart(minWidth, "0")}`;
}

const index = {
  schema: "haven.purpose-knowledge-base-index.v0",
  sourceSchema: knowledgeBase.schema,
  sourcePath: inputPath,
  sourceSHA256: crypto.createHash("sha256").update(sourceText).digest("hex"),
  rootPurposeRef: knowledgeBase.rootPurposeRef,
  nodeCount: nodes.length,
  indexModel: {
    tree: "single-parent",
    facets: "cross-cutting-postings",
    ancestorCheck: "dfs-entry-exit",
    sharedHeritage: "ancestor-bitset",
    candidateGeneration: "alias-map + token/capability/goal postings before sparse cosine fallback"
  },
  nodes: nodes.map((node) => ({
    purposeRef: node.purposeRef,
    ordinal: ordinalByRef.get(node.purposeRef),
    parentRef: node.parentRef ?? null,
    parentOrdinal: node.parentRef ? ordinalByRef.get(node.parentRef) : null,
    depth: depthByRef.get(node.purposeRef),
    entry: entryByRef.get(node.purposeRef),
    exit: exitByRef.get(node.purposeRef),
    ancestorBitsetHex: bitsToHex(ancestorBitsByRef.get(node.purposeRef)),
    status: node.status ?? "unknown",
    goalRef: node.goal?.goalRef ?? null,
    facetRefs: node.facetRefs ?? []
  })),
  aliasMap: postingsObject(aliasMap),
  tokenPostings: postingsObject(tokenPostings),
  capabilityPostings: postingsObject(capabilityPostings),
  goalPostings: postingsObject(goalPostings),
  matchingOrder: [
    "canonical purposeRef / alias hash map",
    "capability postings",
    "goal postings",
    "token inverted index",
    "specificity by depth",
    "facet attachment",
    "optional sparse cosine or embedding rerank over top-K"
  ]
};

fs.writeFileSync(outputPath, `${JSON.stringify(index, null, 2)}\n`);
console.log(`wrote ${outputPath}`);
