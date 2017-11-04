import time
import copy
import os


def dimacs_to_list(file_name):
    with open(file_name) as file:
        return [set([int(var) for var in line.split()[:-1]]) \
            for line in file if line[0] != 'c' and line[0] != 'p']


def get_unit_clauses(clauses):
    """ return literals from unit clauses """
    unit_clauses = set()    # avoid duplications
    for clause in clauses:
        if len(clause) == 1:
            unit_clauses.add(next(iter(clause))) # first element
    return unit_clauses


def simplify(clauses, unit_clauses):
    """ skip clauses with literals from unit clauses, remove -l from remaining 
        and return deep copy """
    new_clauses = []
    neg_clauses = [-l for l in unit_clauses]
    for clause in clauses:
        if len(clause) == 1:    # skip unit clauses
            continue
        if len(clause) == 0:    # contradiction
            return [set()]
        for literal in unit_clauses:
            if literal in clause:
                break
        else:   # if no literal from unit_clauses is in clause
            new_clause = copy.deepcopy(clause)
            new_clause = new_clause.difference(neg_clauses)
            if len(new_clause) == 0: # found contradiction
                return [set()]
            new_clauses.append(new_clause)
    return new_clauses


def DPLL(clauses, val):
    
    # step 1: filter unit clauses
    unit_clauses = get_unit_clauses(clauses)
    val_new = copy.deepcopy(val)

    while len(unit_clauses) > 0:
        for uc in unit_clauses: # check for contradictions
            if -uc in unit_clauses:
                return None
        val_new.update(unit_clauses)
        clauses = simplify(clauses, unit_clauses)
        unit_clauses = get_unit_clauses(clauses)

    # step 2: filter pure literals - skip

    # step 3: have we finished?
    if not clauses:
        return val_new
    if set() in clauses:
        return None

    # step 4: make assumptions l or not l
    l = next(iter(clauses[0]))
    val_new.add(l)
    new_clauses = simplify(clauses, [l])
    val_l = DPLL(new_clauses, val_new)
    if val_l:
        return val_l
    else:
        val_new.discard(l)
        val_new.add(-l)

        new_clauses = simplify(clauses, [-l])
        return DPLL(new_clauses, val_new)


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
    solution = DPLL(CNF, set())
    print("Time needed " + str(time.time() - start_time) + " s")
    print(test(CNF, solution))


'''
CNF = dimacs_to_list('sudoku1.txt')
solution = DPLL(CNF, [])
print(solution, test(CNF, solution))

CNF2 = dimacs_to_list('sudoku2.txt')
solution2 = DPLL(CNF2, [])
print(test(CNF2, solution2))

'''
for filename in os.listdir('TESTS1_satisfiable'):
    print("\n"+filename)
    test_run('TESTS1_satisfiable\\' + filename)