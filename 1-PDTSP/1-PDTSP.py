import sys, math
from copy import deepcopy

def distance(A, B):
	x = A[0] - B[0]
	y = A[1] - B[1]

	return math.ceil(math.sqrt(x*x + y*y))

def read_instance(file):
	clients = []
	with open(file, "r") as instance:
		vehicle_cap, n = map(int,instance.readline().split())
		print("Cap:"+str(vehicle_cap)+", n:"+str(n))
		for line in instance:
			x, y, demand = line.split()
			clients.append([float(x),float(y),int(demand)])

	return clients, vehicle_cap, n

def greedy(clients, max_cap, n):
	depot = clients[0] # Depot
	cap = max_cap # Leaves Depot with full capacity
	unvisited = deepcopy(clients[1:])
	visited = [depot]
	min_cost = float("inf")

	curr_client = depot
	
	while unvisited:
		client = choose_client(curr_client, cap, max_cap, unvisited, n)
		visited.append(client)
		unvisited.remove(client)
		cap += client[2]
		curr_client = client

	print("Greedy tour:")
	print("Cost: "+str(tour_cost(visited)))

def choose_client(curr, cap, max_cap, unvisited, n):
	dists = sorted([(distance(curr, client),client) for client in unvisited], key = lambda t: t[0])
	
	# Check if the vehicle can go to the destination
	for client in dists:
		if client[1][2] + cap >= 0 and client[1][2] + cap <= max_cap:
			return client[1]

def insertion(clients, max_cap, n):
	depot = clients[0]
	cap = max_cap
	unvisited = deepcopy(clients[1:])
	visited = [depot]
	min_cost = float("inf")

	curr_client = depot

	# First, chooses two valid clients to visit, to create an initial
	# closed cycle
	for i in range(2):
		client = choose_client(curr_client, cap, max_cap, unvisited, n)
		visited.append(client)
		unvisited.remove(client)
		cap += client[2]
		curr_client = client

	while unvisited:
		insert, client = choose_insertion(visited, max_cap, unvisited, n)
		visited.insert(insert,client)
		unvisited.remove(client)
		
	print("Insertion tour:")
	print("Cost: "+str(tour_cost(visited)))

def choose_insertion(tour, max_cap, unvisited, n):
	# Find client x that minimizes c(u,x) + c(x,v) - c(u,v)
	best_cost = float("inf")
	best_metric = float("inf")
	best_insert = (-1,-1)

	# For each pair of clients, finds a viable unvisited client
	# with the least cost of insertion
	for i in range(-1,len(tour)-1,1):
		for client in unvisited:
			ux = distance(tour[i],client)
			xv = distance(client,tour[i+1])
			uv = distance(tour[i],tour[i+1])
			metric = ux + xv - uv 
			# Besides checking new cost, checks if the route is
			# viable based on the restrictions of the problem
			if metric < best_metric and check_viability(client, tour, i) is True:
				best_metric = metric
				best_insert = i
				best_client = client

	return best_insert, best_client

def check_viability(client, tour, i):
	aux_tour = deepcopy(tour)
	aux_tour.insert(i,client)
	tot_cap = sum(pair[2] for pair in aux_tour)

	if tot_cap >= 0:
		return True
	else:
		return False

def tour_cost(tour):
	tot_cost = sum(distance(tour[i],tour[i+1]) for i in range(-1,len(tour)-1,1))
	return tot_cost

instance = "test2"
c, v, n = read_instance(instance)
greedy(c, v, n)
insertion(c, v, n)
