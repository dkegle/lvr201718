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

class LocalEnvironment:
    def __init__(self, clauses):
        # parameters
        self.clauses = clauses
        self.val = set()
        # local vars
        self.clauses_new = []
        self.unit_clauses = set()
        self.val_new = set()
        self.l = 0
        self.next_step = 0


def DPLL(cnf):

    env = LocalEnvironment(cnf)
    stack = [env]

    while True:
        
        if env.next_step == 0:
            # step 1: filter unit clauses
            env.unit_clauses = get_unit_clauses(env.clauses)
            env.val_new = copy.deepcopy(env.val)

            contradiction = False
            while len(env.unit_clauses) > 0:
                for l in env.unit_clauses: # check for contradictions
                    if -l in env.unit_clauses:
                        if not stack: # if nothing on stack, return immediately
                            return None
                        else:   # backtrack
                            contradiction = True
                            env = stack.pop()
                            break
                if contradiction:
                    break
                env.val_new.update(env.unit_clauses)
                env.clauses = simplify(env.clauses, env.unit_clauses)
                env.unit_clauses = get_unit_clauses(env.clauses)

            if contradiction:
                continue

            # step 2: filter pure literals - skip

            # step 3: have we finished?
            if not env.clauses:
                return env.val_new
            if set() in env.clauses:
                if not stack:
                    return None
                else:
                    env = stack.pop()
                    continue

            # step 4: make assumptions l or not l
            env.l = next(iter(env.clauses[0]))
            env.val_new.add(env.l)
            env.clauses_new = simplify(env.clauses, [env.l])

            env.next_step = 1

            cp_env = copy.deepcopy(env)
            stack.append(cp_env)
            env.clauses = env.clauses_new
            env.val = env.val_new
            env.next_step = 0   # recurse
            
        elif env.next_step == 1:
            env.val_new.discard(env.l)
            env.val_new.add(-env.l)
            env.clauses_new = simplify(env.clauses, [-env.l])

            env.next_step = 0
            env.clauses = env.clauses_new
            env.val = env.val_new

    return None


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
    solution = DPLL(CNF)
    print("Time needed " + str(time.time() - start_time) + " s")
    print(test(CNF, solution))


#for filename in os.listdir('test_data\\TESTS1_satisfiable'):
#    print("\n"+filename)
#    test_run('test_data\\TESTS1_satisfiable\\' + filename)
    
#test_run("xdata\\sudoku_hard.txt")

