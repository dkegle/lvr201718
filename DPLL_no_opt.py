def dimacs_to_list(file_name):
    with open(file_name) as file:
        return [[int(var) for var in line.split()[:-1]]
                for line in file if line[0] != 'c' and line[0] != 'p']


def unit_clouse(clouses):
    for l in clouses:
        if len(l) == 1:
            return l[0]
    return None


def simplify(clouses, l):
    return [[lit for lit in cl if lit != -l] for cl in clouses if l not in cl]


def DPLL(clouses, val):

    # step 1: filter unit clouses
    l = unit_clouse(clouses)

    while l:
        val.append(l)
        clouses = simplify(clouses, l)
        l = unit_clouse(clouses)

    # step 2: filter pure literals - skip

    # step 3: have we finished?
    if not clouses:
        return val
    if [] in clouses:
        return None

    # step 4: make assumptions l or not l
    l = clouses[0][0]
    val_l = DPLL(simplify(clouses, l), val.append(l))
    if val_l:
        return val_l
    else:
        return DPLL(simplify(clouses, -l), val.append(-l))


def test(clouses, solution):
    for clouse in clouses:
        sat = False
        for literal in clouse:
            if literal in solution:
                sat=True
                break
        if not sat:
            return False
    return True


# tests
'''
CNF = dimacs_to_list('sudoku1.txt')
solution = DPLL(CNF, [])
print(solution, test(CNF, solution))

CNF2 = dimacs_to_list('sudoku2.txt')
solution2 = DPLL(CNF2, [])
print(test(CNF2, solution2))
'''


