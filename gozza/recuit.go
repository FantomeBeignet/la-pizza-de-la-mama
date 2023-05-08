package main

import (
	"math"
	"math/rand"

	"golang.org/x/exp/maps"
)

func sliceSum(slice []float64) float64 {
	f := 0.0
	for _, v := range slice {
		f += v
	}
	return f
}

func RandomPizza(ingredients Ingredients, k int) Pizza {
	res := Pizza{}
	perm := rand.Perm(len(ingredients))
	for i := 0; i < k; i++ {
		res.Add(maps.Keys(ingredients)[perm[i]])
	}
	return res
}

func randomIngredient(ingredients Ingredients) string {
	r := rand.Intn(len(ingredients))
	for k := range ingredients {
		if r == 0 {
			return k
		}
		r--
	}
	panic("unreachable")
}

func randomPizzaIngredient(pizza Pizza) string {
	r := rand.Intn(len(pizza))
	for k := range pizza {
		if r == 0 {
			return k
		}
		r--
	}
	panic("unreachable")
}

func initRecuit(ingredients Ingredients, clients []Client) float64 {
	var randomList []int
	for i := 0; i < 100; i++ {
		c := rand.Intn(len(ingredients))
		temp := RandomPizza(ingredients, c)
		rating := SatisfiedClients(temp, clients)
		randomList = append(randomList, rating)
	}
	var deltas []float64
	for i := 0; i < 100; i++ {
		for j := 0; j < i; j++ {
			deltas = append(deltas, float64(randomList[i]-randomList[j]))
		}
	}
	deltaE := math.Abs(sliceSum(deltas) / float64(len(deltas)))
	t0 := 0.5
	T0 := (-deltaE) / math.Log(t0)
	if T0 > 0 {
		return T0
	} else {
		return 10.0
	}
}

func neighbour(pizza Pizza, ingredients Ingredients) Pizza {
	newPizza := Pizza{}
	for k := range pizza {
		newPizza.Add(k)
	}
	p := rand.Float64()
	unionDifference := Ingredients{}
	for ingr := range ingredients {
		if !pizza.Includes(ingr) {
			unionDifference.Add(ingr)
		}
	}
	if (p < 0.5 || len(pizza) == 1) && (len(pizza) != len(ingredients)) {
		newIngr := randomIngredient(unionDifference)
		newPizza.Add(newIngr)
	} else {
		oldIngr := randomPizzaIngredient(pizza)
		newPizza.Remove(oldIngr)
	}
	return newPizza
}

func Recuit(ingredients Ingredients, clients []Client, firstChoice Pizza) Pizza {
	t := initRecuit(ingredients, clients)
	coolingFactor := 0.9
	nMax := len(ingredients)
	epsilon := 0.001
	u := firstChoice
	N := 0
	K := 0
	for t > epsilon {
		v := neighbour(u, ingredients)
		fv := -SatisfiedClients(v, clients)
		fu := -SatisfiedClients(u, clients)
		if fv < fu {
			N += 1
			u = v
		} else {
			r := rand.Float64()
			if r < math.Exp(float64(fu-fv)/t) {
				N += 1
				u = v
			}
		}
		K += 1
		if (N == nMax) || (K == nMax*100/12) {
			t *= coolingFactor
			N = 0
			K = 0
		}
	}
	return u
}
