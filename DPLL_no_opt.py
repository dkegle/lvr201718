import time

def dimacs_to_list(file_name):
    with open(file_name) as file:
        return [set([int(var) for var in line.split()[:-1]]) \
            for line in file if line[0] != 'c' and line[0] != 'p']


def unit_clause(clauses):
    """ return literal from some unit clause, if it exists """
    for clause in clauses:
        if len(clause) == 1:
            return next(iter(clause))
    return None


def simplify(clauses, l):
    """ remove clauses with literal l, and remove -l from remaining literals """
    new_clauses = []
    for clause in clauses:
        if l not in clause:
            clause.discard(-l)
            new_clauses.append(clause)
    return new_clauses


def DPLL(clauses, val):

    # step 1: filter unit clauses
    l = unit_clause(clauses)

    while l:
        val.append(l)
        clauses = simplify(clauses, l)
        l = unit_clause(clauses)

    # step 2: filter pure literals - skip

    # step 3: have we finished?
    if not clauses:
        return val
    if set() in clauses:
        return None

    # step 4: make assumptions l or not l
    l = next(iter(clauses[0]))
    val_l = DPLL(simplify(clauses, l), val.append(l))
    if val_l:
        return val_l
    else:
        return DPLL(simplify(clauses, -l), val.append(-l))


def test(clauses, solution):
    for clause in clauses:
        sat = False
        for literal in clause:
            if literal in solution:
                sat=True
                break
        if not sat:
            return False
    return True


# tests

def test_run(file):
    CNF = dimacs_to_list(file)
    start_time = time.time()
    solution = DPLL(CNF, [])
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

# test_run('sudoku2.txt')
