# Scientific quality execution

The admission policy remains high relevance AND a manuscript-grounded scientific quality pass. Numeric scores, prestige and publication status cannot grant admission. The six evidence dimensions and rubric are unchanged.

Quality requests use strict JSON Schema and local validation, with a maximum of two same-model assessment requests per paper (the separate bounded support check is described below): initial plus one shared retry for a transient failure, a schema-valid non-substantive response, or an explicitly truncated completion. HTTP 408/429/5xx, DNS/network/timeout/incomplete-body/connection failures and provider-terminal errors inside HTTP 200 can retry. Other HTTP errors and malformed or schema-invalid model answers do not. Retry-After is respected; a delay over 60 seconds ends this attempt instead of retrying early. When a failed OpenRouter response identifies its provider, the single retry excludes that provider while preserving the exact model. There is no automatic repair or model substitution.

The original proposed status, rationale and uncertainty are retained when grounding rejects a decision; they remain explicitly unvalidated proposals, not admissions.

The persisted `execution` ledger separates transport, protocol, evidence-validation, manuscript-access and scientific outcomes. Calls retain safe numeric usage, finish reasons, content hashes/lengths and response IDs; no credentials or hidden reasoning are saved. Missing billing fields are unknown, including for failed requests. A failed model execution does not count as full-text scientific assessment. Repeating a stored failed assessment in the same version uses the existing cache; explicit new assessment versions allow bounded recovery while preserving history.

Selected excerpts prioritize conventional methods/results/limitations and descriptive body headings before conclusion continuations. Per-heading character budgets span pages. Section records contain only the text actually shown to the model; truncation yields partial scope.

Legacy quotation anchors require normalized contiguous text visible in a non-Abstract manuscript section. Literal line-wrap and dehyphenated views are both checked consistently across quote, prompt and source, so a faithful `de- pends` quotation can match a PDF `de-` plus physical newline plus `pends`. Inline word/hyphen changes remain rejected. Normalization handles Unicode canonical composition, Latin ligatures and quotes, whitespace, line-break hyphens and spacing just inside brackets. It does not collapse word boundaries, remove arbitrary punctuation, alter numbers, use edit distance or join omitted passages. A mismatched page can be corrected only to a unique eligible section; the persisted anchor records that actual section/page.

Full text ordinarily comes from PDFs. An explicitly supplied public Europe PMC `fullTextXML` URL also supports JATS article-body sections. Its Page labels are logical XML section numbers, never asserted PDF pagination. Source URL, content hash and the location warning survive the standard cache and assessment provenance. Downloads and extraction retain the existing size, section/page and character bounds; declarations/entities and non-article bodies are rejected.

For a bounded recovery, use `reassess-quality --paper-id ID --limit 1 --assessment-version VERSION --full-text --mode llm --model MODEL` for each saved ID, reusing cached manuscripts. Keep an external manifest/cost bound and audit scientific decisions before publishing. `paper-scout.yml` can publish committed reviewed sites with `deploy_only=true`; its default daily discovery behavior is unchanged.

## Coverage and substantive responses

Extraction now records source page/section counts, attempted and unreadable pages, character limits and explicit gaps. Character/page bounds sample across beginning, middle and end instead of silently dropping the tail. All three tracks allow up to 400,000 extracted characters and 180,000 input characters. If all eligible body and appendix text fits, no per-heading clipping applies. Otherwise scientific groups receive deterministic round-robin excerpts, with disjoint passages separately labelled. References and labelled non-scientific back matter are excluded. A full scope requires complete extraction and all eligible content; the old 65% rule is gone.

Persisted `coverage` records the exact input hash/length, selected page/section inventory, omitted eligible characters, exclusions and warnings. The prompt and evidence validator use the same canonical Unicode/ligature/quote representation, retaining physical line boundaries. A third strict matching view removes only the newline after a physical hyphen, preserving compounds such as `long-term`. No source-only or abstract-only quotation can ground admission.

`full_text_assessed` means a substantive manuscript-based assessment, qualified by `assessment_scope` and `coverage`; it does not certify every PDF image or table layout. The UI labels this “Manuscript evidence assessed” and exposes selected/eligible/omitted characters. Legacy decisions keep their original provenance. New insufficient proposals with incomplete extraction, omitted body text or uncertain section boundaries remain text-coverage uncertainty.

The deterministic seed assessment is no longer supplied to the model. Schema-valid seed echoes, refusals, empty rationales and evidence-empty responses are explicit non-substantive protocol failures. At most one retry restates the schema and manuscript-evidence requirement without requesting hidden reasoning. It shares the existing two-request total with transport retries; malformed JSON still receives no repair call. Failed and successful requests retain separate usage and provenance. The model can explicitly distinguish scientific uncertainty from missing supplied text using `uncertainty_reason`; the rubric and six grounding dimensions remain unchanged.

## Historical context-bound evidence protocol (`block-evidence-v1`)

PR #28 introduced `block-evidence-v1`; these stored assessments retain the semantics in this section. New live assessments use v2, described below. The bounded manuscript selection from the coverage layer is unchanged. A deterministic addressing layer splits its exact canonical sections into roughly 900-character blocks, with source offsets, sections and pages. Only complete, adjacent pages under the same heading may share a block. Selected excerpts, extraction gaps and different sections are never joined. Page-final lexical hyphens are retained when a lowercase continuation follows; original spans remain stored. Repeated headers are not guessed away.

Each ID contains a hash prefix bound to the manuscript identity, source bytes, selected-text hash, addressing version, block contents, offsets and eligibility. Responses must also echo the full context ID. The validator reconstructs the actual supplied context and checks it against the manuscript seed. Under v1, invented, foreign, stale, unseen, Abstract and gap IDs fail closed; there is no quotation fallback in ID-based model calls. Formatting labels add bounded context overhead, reported separately as `evidence_context_characters`; no selected source content is tail-truncated.

The model returns a compact claim, support explanation and `supported`/`partial`/`unsupported` interpretation for each cited block. Existence establishes provenance only. A pass still requires supported positive evidence across the same six scientific dimensions and adequate confidence. An insufficient judgment requires a supported substantive concern and adequate supplied coverage. Unsupported/partial core interpretations retain scientific uncertainty even when every address exists. These support judgments are made by the scientific assessor, not a deterministic theorem prover or independent second assessor; source snippets remain visible for review.

Exact displayed source text is derived only from canonical blocks. Model claims remain separate. Multiple blocks retain individual snippets and page sets; disjoint blocks are explicitly separated. Research cards show pages and expandable canonical source snippets rather than prominent internal IDs. Sidecars retain IDs, context hashes and complete span provenance.

Legacy quote-based records and manual-review JSON remain readable and valid under `scientific-gate-v1`; old decisions are not rewritten. The v1 model wire schema has an explicit version and no model-generated quotation field. The bounded residual run uses assessment version `quality-evidence-v1` to avoid reusing an older response under the new protocol; the scientific rubric remains `scholarly-rubric-v1`.

`length`, `max_tokens` and `max_output_tokens` finish reasons are explicit output-limit failures. Partial content is never parsed or supplied back to the model. One recovery request asks for a compact complete response, preserving rationale, limitations, uncertainty and all required evidence dimensions. It shares the existing two-request maximum with transport and non-substantive retries. Both requests retain billing and finish metadata. A second failure remains protocol uncertainty. Ordinary malformed JSON still has no repair/continuation path. The wire schema caps rationale, uncertainty, claims, explanations, evidence objects and cited IDs; duplicate summaries/metadata and long quotes are no longer requested.

Research-card schema `paper-scout-card-v2` gains optional evidence provenance fields; existing cards remain valid. The nested `evidence_version` and assessment version identify new records explicitly.


## Claim-aware support (`block-evidence-v2`)

New live assessments explicitly distinguish four checks: the referenced block
exists, it belongs to the exact supplied context, its section role is eligible
for this dimension and statement kind, and its content supports the claim.
The scientific rubric and six required gate dimensions remain unchanged.

Section roles reuse the deterministic heading classifier (`abstract`,
`introduction`, `methods`, `results`, `limitations`, `discussion`, `conclusion`,
`related`, `appendix`, `body`, `excluded`). They are stored in blocks and hashed
into the context identity. Unknown body headings and appendices are candidates,
not proof of methods or results. The prompt supplies explicit body candidate IDs
per dimension, plus the limited Abstract contribution IDs.

An Abstract may support an attributed high-level contribution/scope
`source_claim` in `contribution_clarity` only. The novelty/value dimension always requires body evidence. It cannot establish scientific adequacy, novelty, verified
results, methods, evaluation, limitations, reproducibility or claim alignment.
`assessor_inference` denotes bounded synthesis or critique of cited body facts;
it need not be a literal manuscript sentence. A limitation inference may use
methods/results as premises, while an attributed limitation statement needs an
appropriate source role. Mixing an ineligible Abstract ID with a valid body ID
is still rejected; the pipeline never silently removes a bad reference.

Numerical checks require the same explicit value in the cited blocks, preserving
common numeric units (`%`, multipliers, K/M/B magnitudes). Decimal/comma/spacing
normalization cannot change the value. Other units, metric identity, denominators,
populations, comparison direction and scientific interpretation require the
claim/evidence verifier. Number occurrence alone never validates a claim.
Derived arithmetic and ambiguous extraction are conservatively unresolved;
a number elsewhere in the manuscript cannot rescue an uncited assertion.

A single separate request verifies all claims/explanations using only their
respective cited canonical blocks. Published rationale and uncertainty are also
checked against the union of those cited blocks that pass eligibility for their originating evidence item. Items are isolated explicitly
in the prompt; each response must cover every item exactly once. The local result
binds the complete claim/source input hash. The verifier receives no proposed
paper verdict, full manuscript, author or venue metadata, and may return only
`supported`, `unsupported` or `uncertain` with a brief reason. It cannot rewrite
claims or create evidence. This is bounded model screening, not proof of truth;
using the same authorized model can retain correlated errors.

This one additional call is justified because deterministic matching cannot
reliably distinguish, for example, average evidence coverage from complete
evidence recovery, or assess a nonliteral inference. It has a 250,000-byte input
ceiling and 4096-token output ceiling, no retries or repair. The two-attempt
assessment/recovery ceiling remains unchanged: at most two assessment requests
plus one verifier request per paper, three actual requests total. Every actual
call, including failed/truncated verifier responses, has its own usage ledger;
input rejection before sending is labelled `not_sent` with zero cost.

Invalid IDs/contexts/claim-role selections are technical grounding failures.
A verifier transport/schema/output-limit failure is technical protocol
uncertainty. Valid, eligible evidence that does not establish the proposed claim
is scientific uncertainty. Rejected claims remain only in the execution audit;
they cannot supply gate evidence, positive signals or an operative rationale.
The verifier never turns an infrastructure failure into scientific insufficiency.

Legacy quote and `block-evidence-v1` assessments are read without revalidation or
rewriting their reviewed decisions. The root sidecar remains `paper-scout-card-v2`
with additive optional `statement_kind`, `claim_role`, `support_verification` and
source-block `section_role` fields. The assessment manifest must account for the
new bounded verifier cost before any paid rerun.
