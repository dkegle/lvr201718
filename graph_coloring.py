from random import randint


def generate_random_graph(n, m):
	""" connected 'random' graph on n vertices and m edges """

	# check parameters
	max_conn = int(n*(n-1)/2 + 0.5)
	if n < 1 or m + 1 < n or m > max_conn:
		return [], []

	V = [i for i in range(1, n+1)]	# count vertices from 1
	E = set()
	# make a tree
	for i in range(2, n+1):
		v2 = randint(1, i-1)
		E.add((v2, i))

	# add remaining connections
	for i in range(n, m+1):
		v1, v2 = randint(1, n), randint(1, n)
		if v1 > v2:
			v1, v2 = v2, v1

		while v1 == v2 or (v1, v2) in E:
			v2 = randint(1, n)
			if v1 > v2:
				v1, v2 = v2, v1

		E.add((v1, v2))

	E = [(v1, v2) for (v1, v2) in E] # return as list

	return V, E


def graph_coloring_cnf(V, E, k):
	""" generate CNF for k-coloring of graph (V, E) 
	vertices and colors start from 1 """

	cnf = []
	for v in V:
		# each vertex has at least one color
		cnf.append([(v-1)*k + i for i in range(1, k+1)]) 

		# each vertex has at most one color
		for i in range(1, k+1):
			cnf.extend([[-((v-1)*k + i), -((v-1)*k + j)] for j in range(i+1, k+1)])

	# endpoints of edges have different colors
	for (v1, v2) in E:
		cnf.extend([[-((v1-1)*k + i), -((v2-1)*k + i)] for i in range(1, k+1)])

	return cnf

def export_to_dimacs(cnf, file, V, E, k):
	with open(file, 'w') as f:
		f.write("c CNF for a " + str(k) + "-coloring of a graph G \nc vertices ")
#		for v in V:
#			f.write(str(v) + " ")
#		f.write("\nc edges ")
#		for (v1, v2) in E:
#			f.write("(" + str(v1) + "," + str(v2) + ") ")
		f.write("\n")
		for disj in cnf:
			f.write(" ".join([str(l) for l in disj]) + " 0\n")


n, m, k = 500, 1000, 3 # vertices, edges, number of colors

V, E = generate_random_graph(n, m)
cnf = graph_coloring_cnf(V, E, k)

g_name = "-".join(["graph",str(n), str(m), str(k)])
export_to_dimacs(cnf, "test_data/" + g_name + ".txt", V, E, k)

