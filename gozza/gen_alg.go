package main

import (
	"fmt"
	"math/rand"
	"sort"
	"strings"

	"golang.org/x/exp/maps"
)

type PizzaWithScore struct {
	Score int
	Pizza Pizza
}

type State struct {
	PopSize       int
	SelectionSize int
	Repeat        int
	LastScore     int
}

func (s State) createPizzas(ingredients Ingredients) []Pizza {
	var pizzas []Pizza
	for i := 0; i < s.PopSize; i++ {
		pizza := Pizza{}
		for k := range ingredients {
			if rand.Float64() > 0.5 {
				pizza.Add(k)
			}
		}
		pizzas = append(pizzas, pizza)
	}
	return pizzas
}

func (s *State) isGenGood(pizzaList []Pizza, clients []Client) bool {
	maxScore := getMaxScore(pizzaList, clients)
	if maxScore == s.LastScore {
		s.Repeat += 1
		if s.Repeat > 10 {
			return true
		}
		return false
	}
	s.LastScore = maxScore
	s.Repeat = 0
	return false
}

func (s State) proportionSelection(scoredList []PizzaWithScore, clients []Client) []Pizza {
	sort.SliceStable(scoredList, func(i, j int) bool { return scoredList[i].Score < scoredList[j].Score })
	var res []Pizza
	for i := 0; i < s.SelectionSize; i++ {
		res = append(res, scoredList[i].Pizza)
	}
	return res
}

func (s State) fillPizzaSelection(pizzaList *[]Pizza, ingredients Ingredients) {
	for i := 0; i < (s.PopSize - len(*pizzaList)); i++ {
		pizza := Pizza{}
		for k := range ingredients {
			if rand.Float64() > 0.5 {
				pizza.Add(k)
			}
		}
		*pizzaList = append(*pizzaList, pizza)
	}
}

func getMaxScore(pizzaList []Pizza, clients []Client) int {
	bestScore := 0
	for _, pizza := range pizzaList {
		if SatisfiedClients(pizza, clients) > bestScore {
			bestScore = SatisfiedClients(pizza, clients)
		}
	}
	return bestScore
}

func getMaxId(pizzaList []Pizza, clients []Client) int {
	id := 0
	maxScore := SatisfiedClients(pizzaList[0], clients)
	for i := 1; i < len(pizzaList); i++ {
		if SatisfiedClients(pizzaList[i], clients) > maxScore {
			id = i
		}
	}
	return id
}

func crossing(pizzaList *[]Pizza, ingredients Ingredients) {
	for i := 0; i < len(*pizzaList)/2; i++ {
		pizza := Pizza{}
		for k := range ingredients {
			if (*pizzaList)[2*1].Includes(k) && (*pizzaList)[2*i+1].Includes(k) {
				pizza.Add(k)
			} else if (*pizzaList)[2*1].Includes(k) || (*pizzaList)[2*i+1].Includes(k) {
				if rand.Float64() > 0.5 {
					pizza.Add(k)
				}
			}
		}
		*pizzaList = append(*pizzaList, pizza)
	}
}

func mutate(pizzaList *[]Pizza, ingredients Ingredients) {
	for _, pizza := range *pizzaList {
		if rand.Float64() < 0.3 {
			for ingredient := range ingredients {
				if rand.Float64() > 0.5 {
					if pizza.Includes(ingredient) {
						pizza.Remove(ingredient)
					} else {
						pizza.Add(ingredient)
					}
				}
			}
		}
	}
}

func RunAlgo(filename string) Pizza {
	ingredients, clients := ParseInput(filename)
	state := State{PopSize: 50, SelectionSize: 30, Repeat: 0, LastScore: 0}
	pizzaList := state.createPizzas(ingredients)
	return state.runGeneration(pizzaList, ingredients, clients)
}

func (s State) runGeneration(pizzaList []Pizza, ingredients Ingredients, clients []Client) Pizza {
	var scoredList []PizzaWithScore
	var newPizzaList []Pizza
	for _, pizza := range pizzaList {
		scoredList = append(scoredList, PizzaWithScore{Score: SatisfiedClients(pizza, clients), Pizza: pizza})
		sort.SliceStable(scoredList, func(i, j int) bool { return scoredList[i].Score > scoredList[j].Score })
	}
	for i := 0; i < s.SelectionSize; i++ {
		newPizzaList = append(newPizzaList, scoredList[i].Pizza)
	}
	maxId := getMaxId(newPizzaList, clients)
	if s.isGenGood(newPizzaList, clients) {
		return newPizzaList[maxId]
	}
	best := newPizzaList[maxId]
	newPizzaList = append(newPizzaList[:maxId], newPizzaList[maxId+1:]...)
	crossing(&newPizzaList, ingredients)
	mutate(&newPizzaList, ingredients)
	newPizzaList = append(newPizzaList, best)
	if len(newPizzaList) < s.PopSize {
		s.fillPizzaSelection(&newPizzaList, ingredients)
	}
	return s.runGeneration(newPizzaList, ingredients, clients)
}

func printPizzas(pizzas []Pizza) {
	for _, pizza := range pizzas {
		fmt.Printf("%d %s\n", len(pizza), strings.Join(maps.Keys(pizza), " "))
	}
}
