# Independent tests


---
<!-- trackio-cell
{"type": "code", "id": "cell_70486db109d7", "created_at": "2026-07-27T13:18:51+00:00", "title": "Run: python (exit 0)", "command": ["python", "-m", "unittest", "discover", "-s", "repro/tests", "-v"], "exit_code": 0, "duration_s": 0.096}
-->
````bash
$ python -m unittest discover -s repro/tests -v
````

exit 0 · 0.1s


````output
test_general_cfg_oracle (test_constructions.ConstructionTests.test_general_cfg_oracle) ... ok
test_malformed_postfix_rejected (test_constructions.ConstructionTests.test_malformed_postfix_rejected) ... ok
test_postfix_oracles_agree (test_constructions.ConstructionTests.test_postfix_oracles_agree) ... ok
test_sequential_control_is_not_parallel_bound (test_constructions.ConstructionTests.test_sequential_control_is_not_parallel_bound) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.003s

OK

````
