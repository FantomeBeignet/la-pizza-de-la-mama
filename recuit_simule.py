from random import choice, randint, choices, random
from math import exp, log
import sys
import time
from utils import disatisfied_clients, parse_input, satisfied_clients, save_solution


def init(ingredients: set[str], clients: list[tuple[set[str], set[str]]]):
    # 100 random solutions
    random_list = []
    for i in range(2):
        c = randint(0, len(ingredients))
        temp = choices(tuple(ingredients), k=c)
        rating = satisfied_clients(set(temp), clients)
        random_list.append(rating)
    # evaluation of the absolute variation
    var = []
    for i in range(2):
        for j in range(i):
            var.append(random_list[i]-random_list[j])
    deltaE = abs(sum(var)/len(var))
    # Acceptation rate
    t0 = 0.5
    # T0
    T0 = (-deltaE)/log(t0)
    if T0 > 0:
        return T0
    else:
        return 10


def neighboor(state: set[str], ingredients: set[str]) -> set[str]:
    new_state = state.copy()
    new_ingr = choice(tuple(ingredients))
    old_ingr = choice(tuple(state))
    while (new_ingr in state):
        new_ingr = choice(tuple(ingredients))
    p = randint(0, 100)
    if (p < 50):
        new_state.add(new_ingr)
    else:
        new_state.remove(old_ingr)

    return new_state


def neighboorhood(state: set[str], ingredients: set[str]) -> list[set[str]]:
    list_neighboors = []
    if (len(state) != 1):
        for old_ingr in state:
            new_state_remove = state.copy()
            new_state_remove.remove(old_ingr)
            list_neighboors.append(new_state_remove)
    for new_ingr in ingredients:
        if (new_ingr not in state):
            new_state_add = state.copy()
            new_state_add.add(new_ingr)
            list_neighboors.append(new_state_add)

    return list_neighboors


def silukated_annealing1(ingredients: set[str], clients: list[tuple[set[str], set[str]]], first_choice: set[str]) -> set[str]:
    t = init(ingredients, clients)
    cooling_factor = 0.9
    u = first_choice
    N = 0
    K = 0
    while (t > 0.0001):
        # ns = neighboorhood(u, ingredients)
        v = neighboor(u, ingredients)
        fv = -satisfied_clients(v, clients)
        fu = -satisfied_clients(u, clients)
        if (fv < fu):
            N += 1
            u = v
        else:
            r = random()
            if (r < exp((fu-fv)/t)):
                N += 1
                u = v
        K += 1
        if (N == 50) or (K == 150):
            print("Etape "+str(K) + " (acceptée " + str(N) + " ) : "+str(t))
            t = t*cooling_factor
            N = 0
            K = 0
    return u


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    ingredients, clients = parse_input(input_file)

    c = randint(0, len(ingredients))
    temp = set(choices(tuple(ingredients), k=c))
    sol = silukated_annealing1(ingredients, clients, temp)
    print(sol)
    save_solution(sol, output_file)
