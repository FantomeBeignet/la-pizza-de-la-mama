package main

import (
	"os"
)

func main() {
	inputFile := os.Args[1]
	outputFile := os.Args[2]
	SaveSolution(outputFile, RunAlgo(inputFile))
}
