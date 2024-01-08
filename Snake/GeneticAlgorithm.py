# -------------------------------------------------------------------------------------------------
# import required packages/libraries
# -------------------------------------------------------------------------------------------------

import random
import copy
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------------------------------
# A class for a Genetic Algorithm
# -------------------------------------------------------------------------------------------------


class GeneticAlgorithm:
    
    # number of atributes of an individual
    numberOfAtributes = 2000
    # possible directions
    directions = ["UP", "DOWN", "LEFT", "RIGHT"]
    # number of Generations to execute
    numberOfGenerations = 500
    # population size
    populationSize = 1000
    # number of couples
    numberOfCouples = int(populationSize / 2)
    # mutation rate
    mutationRate = 0.05
    # criteria for panic if the generations do not improve the best fitness
    panicCriteria = 0
    # mutation rate is elevated for generations in the panic
    panicMutationRate = 0.20
    # best fitness value(s) obtained by the best individuals
    bestFitness = 0
    # max of individuals to be added in the foodElite, the elite of individuals who got a fruit
    max_foodElite = 1
    # max of individuals to be added in the fitElite, the elite of individuals who got the bests fitness
    max_fitElite = 300

    # individuals of the population
    population = None
    # members of the foodElite
    foodElite = None
    # members of the fitElite
    fitElite = None
    # population fitness
    actualGenerationFitness = None
    # best fitness of each generation
    bestGenerationalFitness = None
    # mean of fitness of each generation
    generationalMeanFitness = None
    # best individual(s) returned after the GA is executed
    bestIndividual = None

    # generate the initial population
    def generateInitialPopulation(self):
        """
        Generate the initial population with random individuals.

        Populates the Genetic Algorithm's initial population with randomly generated individuals,
        where each individual is represented by a list of directions.

        Returns:
        None: The population is directly updated within the class attribute.
        """
        # Iterate over the population size
        for individual in range(0, self.populationSize):
            # Generate a new individual with random directions
            newIndividual = random.choices(self.directions, k=self.numberOfAtributes)

            # Append the new individual to the population
            self.population.append(newIndividual)

    # Fitness function to evaluate an individual
    def fitnessFunction(self, individual, snake_position, snake_body, fruit_position,initialDirection):
        """
        Evaluates the fitness of an individual in the Snake game.

        Parameters:
        - individual (list): The individual representing the Snake's movements.
        - snake_position (list): Current position of the snake.
        - snake_body (list): List representing the snake's body.
        - fruit_position (list): Current position of the fruit.
        - initialDirection (str): Initial direction of the snake.

        Returns:
        tuple: A tuple containing fitness-related metrics -
        (alive, survivalTime, gotFruit, distLog).
        """
        # Fitness Attributes
        window_x = 720  # Width of the game window
        window_y = 480  # Height of the game window
        direction = None  # Current direction of the snake
        alive = True  # Flag indicating whether the snake is alive
        survivalTime = 0  # Number of iterations the snake has survived
        gotFruit = False # Indicate if the individual got a fruit
        distLog = 0 # Numeric log of the distance traveled by the snake in comparison with the fruit position

        # Initializing
        direction = initialDirection  # Initial snake direction
        # Initial distance of the snake in comparison with the fruit position
        actualDist = (abs(snake_position[0] - fruit_position[0])**2+abs(snake_position[1] - fruit_position[1])**2)**(1/2)

        # Game loop (individual represents a sequence of moves)
        for change in individual:
            # Increment alive time
            if alive:
                survivalTime += 1

            # Change the direction of the snake
            if change == "UP" and direction != "DOWN":
                direction = "UP"
            if change == "DOWN" and direction != "UP":
                direction = "DOWN"
            if change == "LEFT" and direction != "RIGHT":
                direction = "LEFT"
            if change == "RIGHT" and direction != "LEFT":
                direction = "RIGHT"

            # Move the snake
            if direction == "UP":
                snake_position[1] -= 10
            if direction == "DOWN":
                snake_position[1] += 10
            if direction == "LEFT":
                snake_position[0] -= 10
            if direction == "RIGHT":
                snake_position[0] += 10
            
            lastDist = actualDist # Keep log of the last distance for comparison
            # Recalculate the distance to the fruit
            actualDist = (abs(snake_position[0] - fruit_position[0])**2+abs(snake_position[1] - fruit_position[1])**2)**(1/2)
            # Analise if the distance grow or reduced
            if actualDist > lastDist:
                distLog -= 1 # Decrement log if got far from de fruit
            else:
                distLog += 1 # Increment log if got closer to the fruit

            # Snake body growing mechanism
            snake_body.insert(0, list(snake_position))
            if (
                snake_position[0] == fruit_position[0]
                and snake_position[1] == fruit_position[1]
            ):
                gotFruit = True # Indicate that got the fruit
                break # Ignore the rest of the individual to save computational resources
            else:
                snake_body.pop()

            # Game Over conditions
            if snake_position[0] < 0 or snake_position[0] > window_x - 10:
                alive = False # Indicates that the snake died
                break # Ignore the rest of the individual to save computational resources
            if snake_position[1] < 0 or snake_position[1] > window_y - 10:
                alive = False # Indicates that the snake died
                break # Ignore the rest of the individual to save computational resources

            # Check for collisions with the snake's own body
            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    alive = False # Indicates that the snake died
                    break # Ignore the rest of the individual to save computational resources
        
        # Correct the log distance if got the fruit but gone to far earlier
        if gotFruit and distLog < 0:
            distLog = 0
        
        # Return fitness metrics as a tuple
        return alive, survivalTime, gotFruit, distLog

    # receive an individual and evaluate its fitness
    def evaluateIndividual(
        self, individual, snake_position, snake_body, fruit_position, initialDirection
    ):
        """
        Parameters:
            individual (object): The individual to be evaluated.
            snake_position (list): The current position of the snake head.
            snake_body (list): The current positions of the snake body.
            fruit_position (list): The position of the fruit.
            initialDirection (int): The initial direction of the snake.

        Returns:
            fitness (float): The calculated fitness score for the individual.
        """
        # Get fitness metrics
        (alive, survivalTime, gotFruit, distLog) = self.fitnessFunction(
            individual=individual,
            snake_position=copy.deepcopy(snake_position),
            snake_body=copy.deepcopy(snake_body),
            fruit_position=copy.deepcopy(fruit_position),
            initialDirection=initialDirection
        )

        # Calculate a fitness base score
        baseFitness = 1000 + survivalTime
        # Calulate a bonus score if the snake is still alive
        survivalBonus = 100 if alive else -800
        # Calulate a bonus score if the snake got a fruit
        fruitBonus = 1000 if gotFruit else -300

        # Calculate the overall fitness score
        fitness = baseFitness + survivalBonus + fruitBonus + distLog
        # Correct the fitness if it became negative
        if fitness <= 0:
            fitness = 1

        # Update fitness elite list
        if len(self.fitElite) < self.max_fitElite: # If do not have enough members
            self.fitElite.append({"Individual": individual.copy(), "Fitness": fitness})
        else:
            if self.fitElite[0]["Fitness"] < fitness and not any(
                member["Fitness"] == fitness for member in self.fitElite
            ): # If already is member or if it fitness is worse of the others
                self.fitElite.pop(0)
                self.fitElite.append({"Individual": individual.copy(), "Fitness": fitness})
        self.fitElite = sorted(self.fitElite, key=lambda x: x["Fitness"]) # Sort the elite based in the fitness

        # Update food elite list if snake got the fruit
        if gotFruit:
            verification = False if fitness > 2100 else True # If do not have fitness (somehow got errors without)
            for member in self.foodElite: 
                if member["Fitness"] == fitness: # If already is member do nothing
                    verification = True
            if not verification: # If can enter the elite
                if len(self.foodElite) < self.max_foodElite: # If do not have enough members, just enter
                    self.foodElite.append({"Individual": individual.copy(), "Fitness": fitness})
                else:
                    # If it fitness is lesser, is more fast, enter and expel some loser
                    if self.foodElite[self.max_foodElite - 1]["Fitness"] > fitness: 
                        self.foodElite.pop(self.max_foodElite - 1)
                        self.foodElite.append({"Individual": individual.copy(), "Fitness": fitness})
                self.foodElite = sorted(self.foodElite, key=lambda x: x["Fitness"]) # Sort the elite based in the fitness

        # Return the fitness as the sum of the base fitness and the bonus score
        return fitness

    def rouletteSelection(self):
        """
        Performs selection using roulette wheel selection in a genetic algorithm.

        Returns:
            pai1 (object): The first parent selected through roulette wheel selection.
            pai2 (object): The second parent selected through roulette wheel selection.
        """
        totalFitness = sum(self.actualGenerationFitness)

        # Generate two random numbers in the range from 1 to totalFitness
        roll1 = random.sample(range(1, totalFitness), k=1)[0]
        roll2 = random.sample(range(1, totalFitness), k=1)[0]

        # Initialize the roulette wheel
        rouletteWheel = []
        # Initialize parent indices for control
        indParent1 = -1
        indParent2 = -1

        # Build the roulette wheel weighted by fitness values
        for ind, fitness in enumerate(self.actualGenerationFitness):
            if ind == 0:
                rouletteWheel.append(fitness)
            else:
                rouletteWheel.append(fitness + rouletteWheel[ind - 1])

            # Check if roll1 reached the position on the roulette wheel
            if roll1 <= rouletteWheel[ind]:
                indParent1 = ind

            # Check if roll2 reached the position on the roulette wheel
            if roll2 <= rouletteWheel[ind]:
                indParent2 = ind

            # Check if both parents have been found to exit the loop early
            if indParent1 == -1 and indParent2 == -1:
                break

        # Get the vectors representing the parents in the population
        parent1 = self.population[indParent1]
        parent2 = self.population[indParent2]

        return parent1, parent2

    # given a population, selects two parents for crossover
    def selectParents(self):
        """
        Selects two parents from the population using tournament selection.

        Returns:
        tuple: A tuple containing two parents selected through tournament selection.
        """
        # Select three random competitors for the tournament
        competitors = random.sample(range(self.populationSize), k=3)

        # Initialize the best competitor with the first one
        bestCompetitor = competitors[0]

        # Find the competitor with the highest fitness
        for competitor in competitors:
            if (
                self.actualGenerationFitness[competitor]
                >= self.actualGenerationFitness[bestCompetitor]
            ):
                bestCompetitor = competitor

        # Select the first parent based on the best competitor
        parent1 = self.population[bestCompetitor]

        # Repeat the process for the second parent
        competitors = random.sample(range(self.populationSize), k=3)
        bestCompetitor = competitors[0]
        for competitor in competitors:
            if (
                self.actualGenerationFitness[competitor]
                >= self.actualGenerationFitness[bestCompetitor]
            ):
                bestCompetitor = competitor

        # Select the second parent based on the best competitor
        parent2 = self.population[bestCompetitor]

        # Return the two parents selected through tournament selection
        return parent1, parent2

    # given two parents, generate two children recombining them
    def generateChildren(self, parent1, parent2):
        """
        Generates two children individuals through crossover of two parent individuals.

        Parameters:
        - parent1 (list): The first parent individual.
        - parent2 (list): The second parent individual.

        Returns:
        tuple: A tuple containing two child individuals resulting from the crossover.
        """

        # Default crossover type
        crossoverType = 2

        if crossoverType == 1:
            # Single point crossover
            cutPoint = random.choice(range(0, self.numberOfAtributes - 1))
            child1 = parent1[0:cutPoint] + parent2[cutPoint:]
            child2 = parent2[0:cutPoint] + parent1[cutPoint:]
        elif crossoverType == 2:
            # Double point crossover
            cutPoints = sorted(random.sample(range(0, self.numberOfAtributes - 1), k=2))
            child1 = (
                parent1[0 : cutPoints[0]]
                + parent2[cutPoints[0] : cutPoints[1]]
                + parent1[cutPoints[1] :]
            )
            child2 = (
                parent2[0 : cutPoints[0]]
                + parent1[cutPoints[0] : cutPoints[1]]
                + parent2[cutPoints[1] :]
            )
        else:
            # Uniform crossover
            child1 = ["None" for atribute in range(0, self.numberOfAtributes)]
            child2 = ["None" for atribute in range(0, self.numberOfAtributes)]
            for atribute in range(0, self.numberOfAtributes):
                child1[atribute], child2[atribute] = random.sample(
                    [parent1[atribute], parent2[atribute]], k=2
                )

        return child1, child2

    # selects an individual and apply a mutation
    def mutationOperator(self, mutatedIndividual):
        """
        Applies mutation to an individual based on the mutation rate.

        Parameters:
        - mutatedIndividual (list): The individual to be mutated.

        Returns:
        None: The mutation is applied directly to the input individual.
        """

        # Verify if the population is in panic to determine the mutation rate
        mutationCriteria = self.mutationRate if self.panicCriteria < 7 else self.panicMutationRate

        # Check if mutation should be applied based on mutation rate
        if random.random() < mutationCriteria:
            # Choose a random mutation type (1: Inversion, 2: Shift, 3: Uniform)
            mutationType = random.choice([1, 2, 3])

            if mutationType == 1:
                # Inversion: Reverses a random segment of the individual
                mutationPositions = sorted(
                    random.sample(range(0, self.numberOfAtributes), k=2)
                )
                mutatedIndividual = (
                    mutatedIndividual[0 : mutationPositions[0]]
                    + mutatedIndividual[mutationPositions[0] : mutationPositions[1]][
                        ::-1
                    ]
                    + mutatedIndividual[mutationPositions[1] :]
                )
            elif mutationType == 2:
                # Shift: Shifts a random segment of the individual to a new position
                mutationPositions = sorted(
                    random.sample(range(0, self.numberOfAtributes - 1), k=2)
                )
                mutatedIndividual = (
                    mutatedIndividual[: mutationPositions[0]]
                    + mutatedIndividual[mutationPositions[1] :]
                    + mutatedIndividual[mutationPositions[0] : mutationPositions[1]]
                )
            else:
                # Uniform: Randomly changes individual attributes based on mutation rate
                for indAtribute in range(0, self.numberOfAtributes):
                    if random.random() < mutationCriteria:
                        mutatedIndividual[indAtribute] = random.choice(self.directions)

        return mutatedIndividual

    def plotGenerationalEvolution(self):
        """
        Plots the evolution of the best fitness and mean fitness across generations.

        This method creates a plot with two lines: one for the best fitness and
        another for the mean fitness, both tracked across generations.

        Returns:
            None
        """
        # Plot for the best fitness and mean fitness
        plt.figure(figsize=(12, 8))

        # Plotting the Best Fitness
        plt.plot(
            self.bestGenerationalFitness,
            label="Best Fitness",
            color="green",
            marker="o",
            linestyle="-",
            linewidth=2,
        )

        # Plotting the Mean Fitness
        plt.plot(
            self.generationalMeanFitness,
            label="Fitness Mean",
            color="blue",
            marker="o",
            linestyle="-",
            linewidth=2,
        )

        # Adding labels and title to the plot
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Evolution of Best Fitness and Fitness Means Through Generations")

        # Adding a legend to the plot
        plt.legend()

        # Adding a grid to the plot
        plt.grid(True)

        # Displaying the plot
        plt.show()

    # run GA
    def execute(self, snake_position, snake_body, fruit_position, initialDirection):
        """
        Executes the Genetic Algorithm (GA) for evolving a population to play the Snake game.

        Parameters:
            snake_position (list): The current position of the snake head.
            snake_body (list): The current positions of the snake body.
            fruit_position (list): The position of the fruit.
            initialDirection (int): The initial direction of the snake.

        Returns:
            bestIndividual (object): The best individual (snake strategy) evolved by the GA.
        """
        
        self.population = [] # Stores individuals of the population
        self.generateInitialPopulation() # Generate the initial population

        self.bestGenerationalFitness = []  # Tracks the best fitness in each generation
        self.generationalMeanFitness = []  # Tracks the mean fitness in each generation
        self.foodElite = []  # Stores elite individuals based on fruit consumption
        self.fitElite = []  # Stores elite individuals based on overall fitness

        bestFit = 0 # Keep track of the best fitness, initialized with 0

        # Apply the GA for each generation 
        for generation in range(1, self.numberOfGenerations):
            
            self.actualGenerationFitness = []  # Reset the store of the fitness of individuals in the current generation

            # Evaluate fitness for each individual in the population
            for individual in self.population:
                self.actualGenerationFitness.append(
                    self.evaluateIndividual(
                        individual=individual,
                        snake_position=snake_position,
                        snake_body=snake_body,
                        fruit_position=fruit_position,
                        initialDirection=initialDirection
                    )
                )

            
            lastBestFit = bestFit # Save the last best fitness
            bestFit = max(self.actualGenerationFitness) # Get the new best fitness
            
            # Check for stagnation in best fitness
            if lastBestFit == bestFit:
                self.panicCriteria += 1 # If keep stagnated, increment the panic criteria to increase the mutation rate
            else:
                self.panicCriteria = 0 # Reset the panic level

            # Track best and mean fitness across generations
            self.bestGenerationalFitness.append(bestFit)
            self.generationalMeanFitness.append(
                sum(self.actualGenerationFitness) / self.populationSize
            )

            # Break conditions for the GA
            # Got enough foodElite members or stagnet for to much
            if len(self.foodElite) == self.max_foodElite or self.panicCriteria > 30:
                break

            # Display generation information
            generationType = "Generation" if self.panicCriteria < 7 else "PanicGeneration"
            print(f"{generationType} {generation} - BestFitness of {bestFit}")

            newPopulation = [] # Reset the data of the new population

            # Generate a new population using crossover and mutation
            for couple in range(0, self.numberOfCouples):
                pai1, pai2 = self.selectParents()
                filho1, filho2 = self.generateChildren(pai1, pai2)
                filho1 = self.mutationOperator(mutatedIndividual=filho1)
                filho2 = self.mutationOperator(mutatedIndividual=filho2)
                newPopulation.append(filho1)
                newPopulation.append(filho2)

            # Combine the new population with the elite individuals
            foodElite = [membro["Individual"] for membro in self.foodElite]
            fitElite = [membro["Individual"] for membro in self.fitElite]
            limPopulation = self.populationSize - len(self.foodElite) - len(self.fitElite)
            self.population = newPopulation.copy()[0:limPopulation] + foodElite + fitElite

        # Display the end of GA execution information
        # self.plotGenerationalEvolution()  # Uncomment if plotting is needed

        # Identify if got a fruit
        if len(self.foodElite) < 1:
            # If got a fruit get individual with the shortest path to the fruit and its fitness
            self.bestFitness = self.fitElite[0]["Fitness"]
            self.bestIndividual = self.fitElite[0]["Individual"]
        else:
            # If didnt get a fruit, get the best individual of the generations
            self.bestFitness = self.foodElite[0]["Fitness"]
            self.bestIndividual = self.foodElite[0]["Individual"]

        print("End of GA execution")
        print(f"BestFitness {self.bestFitness}")

        # Return the best individual
        return self.bestIndividual



# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
