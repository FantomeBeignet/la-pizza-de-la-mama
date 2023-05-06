from random import randint, choices, random
import numpy as np
from math import exp, log
import sys
from utils import parse_input, satisfied_clients, save_solution


def init(ingredients: set[str], clients: list[tuple[set[str], set[str]]]) -> float:
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


def neighbor(state: set[str], ingredients: set[str]) -> set[str]:
    new_state = state.copy()
    p = np.random.rand()
    
    # first case : we add a new ingredient
    if (p < 0.5 or len(state) == 1) and len(state)!=len(ingredients):
        new_ingr = np.random.choice(list(ingredients - state))
        new_state.add(new_ingr)
    # second case : we remove an ingredient
    else:
        old_ingr = np.random.choice(list(state))
        new_state.remove(old_ingr)

    return new_state

def simulated_annealing(ingredients: set[str], clients: list[tuple[set[str], set[str]]], first_choice: set[str]) -> set[str]:
    t= init(ingredients,clients) # TO first temperature
    cooling_factor =0.9
    Nmax  = len(ingredients)
    epsilon = 0.001
    u = first_choice 
    N = 0
    K = 0
    rng = np.random.default_rng()  # random number generator
    while (t > epsilon):
        v = neighbor(u, ingredients)
        fv = -satisfied_clients(v, clients)
        fu = -satisfied_clients(u, clients)
        if (fv < fu):
            N += 1
            u = v
        else:
            r = rng.random()
            if (r < exp((fu-fv)/t)):
                N += 1
                u = v
        K += 1
        if (N == Nmax) or (K == Nmax*100//12):
            t = t*cooling_factor
            N = 0
            K = 0
            print("Etape t = "+str(t)+", score= "+str(-fv))
    return u


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    ingredients, clients = parse_input(input_file)
    c = randint(0, len(ingredients))
    temp = set(choices(tuple(ingredients), k=c))
    sol = simulated_annealing(ingredients, clients, temp)
    print(sol)
    save_solution(sol, output_file)
