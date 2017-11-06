# Repository for LVR homework

## SAT solver

DPLL_no_opt.py  --  basic dpll

DPLL_opt1.py  --  unit propagation in chunks

DPLL_opt2.py  --  unit propagation in chunks, loop instead of recursion

DPLL_opt3.py  -- unit propagation in chunks, no deepcopy, heuristic for choosing literal

Final version is DPLL_opt3.py, run it from command line:

```
python DPLL_opt3.py [input] [output]
```

### Tests

graph_coloring.py  --  generates random graphs and CNF for k-coloring

test_data/  --  contains test data in DIMACS format from various sources

test_data/graph-1000-2000-3.txt  --  example generated with graph_coloring.py (random graph on 1000 vertices and 2000 edges, it is 3-colorable, solved in 5.6 sec)