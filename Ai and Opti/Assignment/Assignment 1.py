import random

# number of cities
N = 500

# initialize the table with -1
Table = [[-1 for j in range(N)] for i in range(N)]

# fill symmetric random distances
for i in range(N):
    for j in range(N):
        if Table[i][j] == -1 and i != j:
            distance = random.randint(1, 10)  # between 1 and 10 inclusive
            Table[i][j] = distance
            Table[j][i] = distance


#Hjelper Funksjon for å finne total lengde
def city_length (city,Table):
    total = 0
    for i in range(len(city) -1):
        total += Table[city[i]][city[i+1]]
    #returner til start
    total += Table[city[-1]][city[0]]
    return total

#Random Initial Solution
cities = list(range(N))
random_city = cities[:]
random.shuffle(random_city)
random_distance = city_length(random_city,Table)

print("Random City Order", random_city)
print("Random Distance", random_distance)

#Greedy initial Solution
def greedy_city(Table, start = 0):
    N = len(Table)
    unvisisted = list(range(N))
    path = [start]
    unvisisted.remove(start)

    current = start
    while unvisisted:
        nearest = unvisisted[0]
        for city in unvisisted:
            if Table[current][city] < Table[current][nearest]:
                nearest = city
        path.append(nearest)
        unvisisted.remove(nearest)
        current = nearest
    return path

greedy_city_order = greedy_city(Table, start= 0)
greedy_distance = city_length(greedy_city_order,Table)

print("Greedy City Order", greedy_city_order)
print("Greedy Distance", greedy_distance)


#Greedy improvement Algorithm
def greedy_improvement(path,Table):
    improved = True
    best_path = path[:]
    best_length = city_length(best_path,Table)

    while improved:
        improved = False
        for i in range(1,len(path)-1):
            for j in range(i+1,len(path)):
                new_path = best_path[:]
                new_path[i:j] = reversed(best_path[i:j])
                new_length = city_length(new_path,Table)

                if new_length < best_length:
                    best_path = new_path[:]
                    best_length = new_length
                    improved = True
                    break
            if improved:
                break
    return best_path, best_length

improved_random_city, improved_random_distance = greedy_improvement(random_city,Table)
improved_greedy_city, improved_greedy_distance = greedy_improvement(greedy_city_order,Table)

print("Improved Random City Order", improved_random_city)
print("Improved Random Distance", improved_random_distance)
print("Improved Greedy City Order", improved_greedy_city)
print("Improved Greedy Distance", improved_greedy_distance)