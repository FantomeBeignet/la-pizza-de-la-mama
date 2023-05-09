import time
import random as rd
import sys
import math as m
from utils import parse_input, satisfied_clients, save_solution

pop_size = 500
sel_size = m.floor(0.6*pop_size)
global repeat
repeat = 0
last_score = 0
start_time = time.time()


def create_pizzas(ingredients: set[str]) -> list[set[str]]:
    pizza_list = []
    for i in range(pop_size):
        pizza = set()
        for ing in ingredients:
            if rd.random() > 0.5:
                pizza.add(ing)
        pizza_list.append(pizza)
    return pizza_list


def is_gen_good(score) -> bool:
    global repeat
    repeat += 1
    return (repeat > 1000 or score > 2000)
    # global last_score
    # if get_max_score(pizza_list, clients) == last_score:
    #     repeat += 1
    #     if repeat > 10:
    #         # print(repeat, last_score)
    #         return True
    #     else:
    #         # print(repeat, last_score)
    #         return False
    # else:
    #     last_score = get_max_score(pizza_list, clients)
    #     repeat = 0
    #     # print(repeat, last_score)
    #     return False


def proportion_selection(scored_list: list[int, set[str]]) -> list[set[str]]:
    scored_list.sort()
    return [e[1] for e in sorted(scored_list)[:sel_size]]


def get_max_id(pizza_list: list[set[str]], clients: list[tuple[set[str], set[str]]]):
    id = 0
    max_score = satisfied_clients(pizza_list[0], clients)
    for i in range(len(pizza_list)):
        if satisfied_clients(pizza_list[i], clients) > max_score:
            max_score = satisfied_clients(pizza_list[i], clients)
            id = i
    return id


def crossing(pizza_list: list[set[str]], ingredients: set[str]):
    for i in range(len(pizza_list) // 2):
        pizza = set()
        for ing in ingredients:
            if (ing in pizza_list[2*i] and ing in pizza_list[2*i+1]):
                pizza.add(ing)
            elif (ing in pizza_list[2*i] or ing in pizza_list[2*i+1]):
                if rd.random() > 0.5:
                    pizza.add(ing)
        pizza_list.append(pizza)


def fill_pizza_selection(pizza_list: list[set[str]], ingredients: set[str]):
    for i in range(pop_size - len(pizza_list)):
        pizza = set()
        for ing in ingredients:
            if rd.random() > 0.5:
                pizza.add(ing)
        pizza_list.append(pizza)


def algo_start(input_file: str) -> set[str]:
    global start_time
    ingredients, clients = parse_input(input_file)
    pizza_list = create_pizzas(ingredients)
    return run_gen_algo(pizza_list, ingredients, clients)


def mutate(pizza_list: list[set[str]], ingredients: set[str]):
    for pizza in pizza_list:
        if rd.random() < 0.3:
            for ing in ingredients:
                if rd.random() > 0.8:
                    if ing in pizza:
                        pizza.remove(ing)
                    else:
                        pizza.add(ing)


def get_max_score(pizza_list: list[set[str]], clients: list[tuple[set[str], set[str]]]):
    best_score = 0
    for pizza in pizza_list:
        if satisfied_clients(pizza, clients) > best_score:
            best_score = satisfied_clients(pizza, clients)
    return best_score


def run_gen_algo(pizza_list: list[set[str]], ingredients: set[str], clients: list[tuple[set[str], set[str]]]) -> set[str]:
    scored_list = []
    for pizza in pizza_list:
        scored_list.append([satisfied_clients(pizza, clients), pizza])
    scored_list.sort(reverse=True)
    new_pizza_list = [e[1] for e in scored_list[:sel_size]]
    global start_time
    print("["+timestamping(time.time() -
          start_time)+"] generation", repeat+1, "| score :", scored_list[0][0])
    if is_gen_good(scored_list[0][0]):
        return new_pizza_list[get_max_id(new_pizza_list, clients)]
    else:
        best = new_pizza_list.pop(get_max_id(new_pizza_list, clients))
        crossing(new_pizza_list, ingredients)
        mutate(new_pizza_list, ingredients)
        new_pizza_list.append(best)
        # print_pizzas(new_pizza_list, clients)
        if len(new_pizza_list) < pop_size:
            fill_pizza_selection(new_pizza_list, ingredients)
        return run_gen_algo(new_pizza_list, ingredients, clients)


def print_pizzas(pizza_list: list[set[str]], clients: list[tuple[set[str], set[str]]]):
    for pizza in pizza_list:
        print(pizza, satisfied_clients(pizza, clients))
    print(get_max_id(pizza_list, clients), "\n")


def timestamping(time):
    min = m.floor(time/60)
    sec = m.floor(time - min*60)
    return str(min) + "\'"+str(sec)+"\""


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    save_solution(algo_start(input_file), output_file)


# print(algo_start())
