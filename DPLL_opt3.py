import time
import copy
import os
import random
from collections import Counter


class Clause:
    def __init__(self, id, literals):
        self.id = id
        self.literals = literals

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return str(self.literals)


def DPLL_setup(cnf):
    clauses = []
    for i in range(len(cnf)):
        clauses.append(Clause(i, cnf[i]))
    return DPLL_inc(clauses, set(), set(), dict())


def get_unit_clauses(clauses):
    """ return literals from unit clauses """
    unit_clauses = set()  # avoid duplications
    for clause in clauses:
        if len(clause.literals) == 1:
            unit_clauses.add(next(iter(clause.literals)))  # first element
    return unit_clauses


def simplify(clauses, unit_clauses, S_removed, S_modified):
    """ skip clauses with literals from unit clauses, remove -l from remaining
        and return deep copy """

    neg_clauses = [-l for l in unit_clauses]

    for i in range(len(clauses) - 1, -1, -1):
        clause = clauses[i]
        if len(clause.literals) == 1:  # skip unit clauses
            S_removed.add(clause)
            clauses.pop(i)
            continue
        if len(clause.literals) == 0:  # contradiction
            return False
        for literal in unit_clauses:
            if literal in clause.literals:
                S_removed.add(clause)
                clauses.pop(i)
                break
        else:  # if no literal from unit_clauses is in clause
            lit_intersection = clause.literals.intersection(neg_clauses)
            if lit_intersection:
                if clause in S_modified:
                    # S_modified[clause] = S_modified[clause].union(lit_intersection)
                    S_modified[clause].update(lit_intersection)
                else:
                    S_modified.update([(clause, lit_intersection)])
                clause.literals = clause.literals.difference(lit_intersection)
                if len(clause.literals) == 0:  # found contradiction
                    return False
    return True


def undo_clauses(clauses, S_removed, S_modified):
    clauses.extend(S_removed)
    for clause in S_modified:
        clause.literals.update(S_modified[clause])
        # S_removed.clear()
        # S_modified.clear()


def DPLL_inc(clauses, val, S_removed, S_modified):  # TODO: use only one stack set and one dictionay stack

    # step 1: filter unit clauses
    unit_clauses = get_unit_clauses(clauses)
    val_new = copy.deepcopy(val)

    while len(unit_clauses) > 0:
        for uc in unit_clauses:  # check for contradictions
            if -uc in unit_clauses:
                return None
        val_new.update(unit_clauses)
        if not simplify(clauses, unit_clauses, S_removed, S_modified):
            return None
        unit_clauses = get_unit_clauses(clauses)

    # step 2: filter pure literals - skip

    # step 3: have we finished?
    if not clauses:
        return val_new
    # if set() in clauses:
    #     return None

    # step 4: make assumptions l or not l
    S_removed_1 = set()
    S_modified_1 = dict()

    # heuristics for choosing a literal
    # l = next(iter(clauses[0].literals))
    # l = next(iter(clauses[random.randint(0,len(clauses)-1)].literals))
    # l = random.sample(clauses[random.randint(0,len(clauses)-1)].literals,1)[0]

    all_literals = []
    for c in clauses:
        all_literals.extend(c.literals)

    cnt = Counter(all_literals)

    # randomness / greediness (4)
    most_common_literals = cnt.most_common(4) # TODO: incremental count
    l = most_common_literals[random.randint(0, len(most_common_literals) - 1)][0]

    val_new.add(l)
    if simplify(clauses, [l], S_removed_1, S_modified_1):
        val_l = DPLL_inc(clauses, val_new, S_removed_1, S_modified_1)
        if val_l:
            return val_l

    undo_clauses(clauses, S_removed_1, S_modified_1)
    val_new.discard(l)

    S_removed_2 = set()
    S_modified_2 = dict()
    val_new.add(-l)

    if simplify(clauses, [-l], S_removed_2, S_modified_2):
        val_l = DPLL_inc(clauses, val_new, S_removed_2, S_modified_2)
        if val_l:
            return val_l

    undo_clauses(clauses, S_removed_2, S_modified_2)
    val_new.discard(-l)


def dimacs_to_list(file_name):
    with open(file_name) as file:
        return [set([int(var) for var in line.split()[:-1]]) \
                for line in file if line[0] != 'c' and line[0] != 'p']


def test(clauses, solution):
    """ validity of solution """
    if not solution:
        return False
    for l in solution:  # check for contradictions
        if -l in solution:
            return False
    for clause in clauses:  # check that clauses are true
        for literal in clause:
            if literal in solution:
                break
        else:
            return False
    return True


# tests

def test_run(file):
    CNF = dimacs_to_list(file)
    start_time = time.time()
    solution = DPLL_setup(CNF)
    print(solution)
    print("Time needed " + str(time.time() - start_time) + " s")
    print(test(CNF, solution))


# for filename in os.listdir('test_data\\TESTS1_satisfiable'):
#     print("\n" + filename)
#     test_run('test_data\\TESTS1_satisfiable\\' + filename)
