# RAG Prompt Transformer

Deterministic reference tool for the `RAGPromptTransformerCell` contract in
`Book/28_RAG_Prompt_Transformer_Cell.md`.

The tool takes a RAG source package plus a target model profile and emits a
prompt package. It does not search, call a model, fetch credentials, or mutate
state.

## Usage

```bash
python3 Tools/RAGPromptTransformer/rag_prompt_transformer.py \
  --input Tools/RAGPromptTransformer/fixtures/skeleton_rag_source_package.json \
  --out /tmp/skeleton_prompt_package.json
```

Run tests:

```bash
python3 -m unittest discover Tools/RAGPromptTransformer/tests
```

