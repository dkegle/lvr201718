# Repository for LVR homework

### SAT solver

DPLL_no_opt.py  --  basic dpll

DPLL_opt1.py  --  unit propagation in chunks

DPLL_opt2.py  --  unit propagation in chunks, loop instead of recursion

DPLL_opt3.py  -- unit propagation in chunks, no deepcopy, heuristic for choosing literal, restart after some time

### Tests

graph_coloring.py  --  generates random graphs and CNF for k-coloring

test_data/  --  contains test data in DIMACS format from various sources

### Usage

Final solver is DPLL_opt3.py, run it from command line:
```
python DPLL_opt3.py [input] [output]
```

Final test file is graph-1000-2000-3.txt.
