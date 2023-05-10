package main

import (
	"fmt"
	"math/rand"
	"sort"
	"strings"
	"sync"
	"time"

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
	MaxRepeat     int
	LastScore     int
}

func (s State) createPizzas(ingredients Ingredients, clients []Client) []PizzaWithScore {
	var pizzas []PizzaWithScore
	for i := 0; i < s.PopSize; i++ {
		pizza := Pizza{}
		for k := range ingredients {
			if rand.Float64() > 0.5 {
				pizza.Add(k)
			}
		}
		pizzas = append(
			pizzas,
			PizzaWithScore{Pizza: pizza, Score: SatisfiedClients(pizza, clients)},
		)
	}
	return pizzas
}

func (s *State) isGenGood() bool {
	s.Repeat++
	return s.Repeat > s.MaxRepeat
}

func (s State) fillPizzaSelection(
	pizzaList *[]PizzaWithScore,
	ingredients Ingredients,
	clients []Client,
) {
	wg := sync.WaitGroup{}
	l := len(*pizzaList)
	appendList := make([]PizzaWithScore, l)
	for i := 0; i < (s.PopSize - l); i++ {
		wg.Add(1)
		go func(ind int) {
			r := rand.New(rand.NewSource(time.Now().UnixNano()))
			defer wg.Done()
			pizza := Pizza{}
			for k := range ingredients {
				if r.Float64() > 0.5 {
					pizza.Add(k)
				}
			}
			score := SatisfiedClients(pizza, clients)
			appendList[ind] = PizzaWithScore{Pizza: pizza, Score: score}
		}(i)
	}
	wg.Wait()
	for _, v := range appendList {
		*pizzaList = append(*pizzaList, v)
	}
}

func crossing(pizzaList *[]PizzaWithScore, ingredients Ingredients, clients []Client) {
	wg := sync.WaitGroup{}
	rand.Shuffle(
		len(*pizzaList),
		func(i, j int) { (*pizzaList)[i], (*pizzaList)[j] = (*pizzaList)[j], (*pizzaList)[i] },
	)
	appendList := make([]PizzaWithScore, len(*pizzaList)/2)
	for i := 0; i < len(*pizzaList)/2; i++ {
		wg.Add(1)
		go func(ind int) {
			defer wg.Done()
			r := rand.New(rand.NewSource(time.Now().UnixNano()))
			firstPizza := (*pizzaList)[2*ind].Pizza
			secondPizza := (*pizzaList)[2*ind+1].Pizza
			pizza := Pizza{}
			for k := range ingredients {
				if firstPizza.Includes(k) && secondPizza.Includes(k) {
					pizza.Add(k)
				} else if firstPizza.Includes(k) || secondPizza.Includes(k) {
					if r.Float64() > 0.5 {
						pizza.Add(k)
					}
				}
			}
			score := SatisfiedClients(pizza, clients)
			appendList[ind] = PizzaWithScore{Pizza: pizza, Score: score}
		}(i)
	}
	wg.Wait()
	for _, p := range appendList {
		*pizzaList = append(*pizzaList, p)
	}
}

func mutate(pizzaList *[]PizzaWithScore, ingredients Ingredients, clients []Client) {
	wg := sync.WaitGroup{}
	for i, pizza := range *pizzaList {
		wg.Add(1)
		go func(ind int, p PizzaWithScore) {
			defer wg.Done()
			r := rand.New(rand.NewSource(time.Now().UnixNano()))
			newPizza := Pizza{}
			if rand.Float64() > 0.5 {
				for ingredient := range ingredients {
					if r.Float64() > 0.5 {
						if newPizza.Includes(ingredient) {
							newPizza.Remove(ingredient)
						} else {
							newPizza.Add(ingredient)
						}
					}
				}
				score := SatisfiedClients(newPizza, clients)
				(*pizzaList)[ind] = PizzaWithScore{Pizza: newPizza, Score: score}
			}
		}(i, pizza)
	}
	wg.Wait()
}

func RunAlgo(filename string) Pizza {
	ingredients, clients := ParseInput(filename)
	state := State{PopSize: 500, SelectionSize: 200, Repeat: 0, MaxRepeat: 5000, LastScore: 0}
	pizzaList := state.createPizzas(ingredients, clients)
	return state.runGeneration(pizzaList, ingredients, clients)
}

func (s State) runGeneration(
	pizzaList []PizzaWithScore,
	ingredients Ingredients,
	clients []Client,
) Pizza {
	sort.SliceStable(
		pizzaList,
		func(i, j int) bool { return pizzaList[i].Score > pizzaList[j].Score },
	)
	pizzaList = pizzaList[:s.SelectionSize]
	best := pizzaList[0]
	fmt.Println("gen #", s.Repeat, "score:", best.Score)
	if s.isGenGood() {
		return best.Pizza
	}
	crossing(&pizzaList, ingredients, clients)
	mutate(&pizzaList, ingredients, clients)
	pizzaList = append([]PizzaWithScore{best}, pizzaList...)
	if len(pizzaList) < s.PopSize {
		s.fillPizzaSelection(&pizzaList, ingredients, clients)
	}
	return s.runGeneration(pizzaList, ingredients, clients)
}

func printPizzas(pizzas []Pizza) {
	for _, pizza := range pizzas {
		fmt.Printf("%d %s\n", len(pizza), strings.Join(maps.Keys(pizza), " "))
	}
}
