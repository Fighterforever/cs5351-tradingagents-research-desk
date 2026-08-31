# Fix only the actual remaining lint findings

All application behavior and approved tests are now fixed. Root is still working in `src/research_desk/eval/live.py`: DO NOT edit that file or any of its tests. Root will fix its F541 separately. The active root opencode.json must remain unchanged.

You may edit ONLY these four files:

1. `src/research_desk/budget.py`: Ruff SIM102 at the nested if around line 54. Combine the equivalent guards while preserving evaluation order and behavior.
2. `test/offline/test_at05_version_recheck.py`: Ruff F841 for `approved` around line 53. Remove only the unused assignment target, preserving the function call and all its side effects and assertions.
3. `test/offline/test_at06_budget_context.py`: Ruff F841 for `first` around line 77. Remove only the unused assignment target; preserve the actual call, behavior and assertions.
4. `test/offline/test_live_fixes.py`: Ruff I001 import ordering at several function scopes plus unused `HumanMessage` and `os` imports. Sort those imports and remove only unused imports.

These findings are from a real current repository lint invocation. Do not add ignores, change Ruff settings, weaken assertions, rewrite tests, modify source behavior, or refactor unrelated code. Do not run --unsafe-fixes. You may use safe Ruff fixes only on these four named files, then make the few explicit semantics-preserving changes above.

Run Ruff once on those four files after editing and stop. Do not run any full test suite, API experiment, or other audit. The coordinator will run the full six gates against the final committed source.
