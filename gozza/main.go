package main

import (
	"math/rand"
	"os"
)

func main() {
	inputFile := os.Args[1]
	outputFile := os.Args[2]
	ingredients, clients := ParseInput(inputFile)
	c := rand.Intn(len(ingredients))
	temp := RandomPizza(ingredients, c)
	sol := Recuit(ingredients, clients, temp)
	SaveSolution(outputFile, sol)
}
