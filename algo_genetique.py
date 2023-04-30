import random as rd
from utils import parse_input


def create_pizzas(ingredients: set[str], n: int) -> list[set[str]]:
    pizza_list = []
    for i in range(n):
        pizza = set()
        for ing in ingredients:
            if rd.random() > 0.5:
                pizza.add(ing)
        pizza_list.append(pizza)
    return pizza_list


print(create_pizzas(parse_input("subject/a_exemple.txt")[0], 3))
