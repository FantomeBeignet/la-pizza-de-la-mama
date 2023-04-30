import random as rd
from utils import parse_input, satisfied_clients

pop_size = 10
sel_size = 5


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
    ref_score = satisfied_clients(pizza_list[0], clients)
    for pizza in pizza_list:
        if satisfied_clients(pizza, clients) != ref_score:
            return False
    return True


def proportion_selection(pizza_list: list[set[str]], clients: list[tuple[set[str], set[str]]]) -> list[set[str]]:
    sel_list = pizza_list[:sel_size]
    for pizza in pizza_list[sel_size:]:
        for i in range(len(sel_list)):
            if satisfied_clients(pizza, clients) > satisfied_clients(sel_list[i], clients):
                sel_list[i] = pizza
                break
    return sel_list


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


# pizza_list = create_pizzas(parse_input("subject/a_exemple.txt")[0])
# pizza_list = proportion_selection(
#     pizza_list, parse_input("subject/a_exemple.txt")[1])
# print(pizza_list, len(pizza_list))
# crossing(pizza_list, parse_input("subject/a_exemple.txt")[0])
# fill_pizza_selection(pizza_list, parse_input("subject/a_exemple.txt")[0])
# print(pizza_list, len(pizza_list))
