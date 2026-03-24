# Embeddings

This note covers the embedding layer used by retrieval in `aim-codex`.

## Purpose
Embeddings allow the Engram DB to retrieve concepts, not just exact strings.

## Current Store
- Search database: `archive/engram.db`
- Embedding flow is used by the retrieval and indexing path

## Practical Rule
Do not mix incompatible embedding spaces in the same database unless you are intentionally rebuilding the index.

## Operational Implication
If the embedding model changes materially, rebuild the index.
