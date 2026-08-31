# Annotated OpenCode session 4: six CI gates and meaningful rejection examples

Session: ses_fa82cafc9ffeeAkOozPwPQ41De. Full native record: project-ci.full.json. Raw event stream and exact prompts are retained alongside it. Scope was scripts/, the Research Desk workflow and requirement schema; the session did not own application source.

Intervention1 rejected a proposed gate that treated a git-diff failure as an empty changed-file set. A failed comparison cannot establish that no review is needed. The corrected check preserves a concrete failure.

Intervention2 required approval to correspond to changed tests and explicit safety paths. An old ADR mentioning a module cannot authorize arbitrary future edits. The implemented gate checks the actual changed documents and approval chronology rather than accepting a generic APPROVED marker.

Intervention3 bound the semantic check to the actual case_registry and compact_transform interfaces. The six fixed cases and captured packages supply its inputs. It recomputes deterministic contracts and does not fabricate fresh LLM judge scores in offline CI.

Intervention4 requested isolated negative examples for all six gates. The harness alters temporary copies and captures expected refusal, avoiding contamination of the real tests or research data. The final local and remote check status is documented separately in docs/ci-gates.md; the transcript proves implementation and review, not an unrun server result.

