import time
import random as rd
import sys
import math as m
from utils import parse_input, satisfied_clients, save_solution

pop_size = 50
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


def is_gen_good(pizza_list: list[set[str]], clients: list[tuple[set[str], set[str]]]) -> bool:
    global repeat
    global last_score
    if get_max_score(pizza_list, clients) == last_score:
        repeat += 1
        if repeat > 10:
            # print(repeat, last_score)
            return True
        else:
            # print(repeat, last_score)
            return False
    else:
        last_score = get_max_score(pizza_list, clients)
        repeat = 0
        # print(repeat, last_score)
        return False


def proportion_selection(pizza_list: list[set[str]], clients: list[tuple[set[str], set[str]]]) -> list[set[str]]:
    global start_time
    sel_list = []
    for i in range(sel_size):
        sel_list.append(pizza_list.pop(get_max_id(pizza_list, clients)))
        print("append", i, time.time()-start_time)
    return sel_list


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
    print("created", time.time()-start_time)
    return run_gen_algo(pizza_list, ingredients, clients)


def mutate(pizza_list: list[set[str]], ingredients: set[str]):
    for pizza in pizza_list:
        if rd.random() < 0.3:
            for ing in ingredients:
                if rd.random() > 0.5:
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
    new_pizza_list = proportion_selection(pizza_list, clients)
    global start_time
    print("selected", time.time()-start_time)
    if is_gen_good(new_pizza_list, clients):
        return new_pizza_list[get_max_id(new_pizza_list, clients)]
    else:
        best = new_pizza_list.pop(get_max_id(new_pizza_list, clients))
        print(satisfied_clients(best, clients))
        crossing(new_pizza_list, ingredients)
        print("crossing", time.time()-start_time)
        mutate(new_pizza_list, ingredients)
        print("mutated", time.time()-start_time)
        new_pizza_list.append(best)
        # print_pizzas(new_pizza_list, clients)
        if len(new_pizza_list) < pop_size:
            fill_pizza_selection(new_pizza_list, ingredients)
        print("filled", time.time()-start_time)
        return run_gen_algo(new_pizza_list, ingredients, clients)


def print_pizzas(pizza_list: list[set[str]], clients: list[tuple[set[str], set[str]]]):
    for pizza in pizza_list:
        print(pizza, satisfied_clients(pizza, clients))
    print(get_max_id(pizza_list, clients), "\n")


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    save_solution(algo_start(input_file), output_file)


# print(algo_start())
