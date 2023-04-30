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


# print(create_pizzas(parse_input("subject/a_exemple.txt")[0], 3))
# print(is_gen_good([{"peppers", "cheese"}, {"cheese", "mushrooms", "tomatoes", "peppers", "pineappple"}, {
#       "peppers", "mushrooms"}], parse_input("subject/a_exemple.txt")[1]))
# propo_selection(create_pizzas(parse_input("subject/a_exemple.txt")
#                               [0]), parse_input("subject/a_exemple.txt")[1])
