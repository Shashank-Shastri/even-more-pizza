import pulp as pl
from itertools import permutations, chain

def get_unique_ingredients(pizzas):

    if isinstance(pizzas[0], list):
        pizzas = [ingredients for pizza in pizzas for ingredients in pizza]
    ingredients = list(set(pizzas))
    return ingredients

def get_score(pizzas, deliveries):

    if isinstance(deliveries[0], list):
        score = sum([get_score(pizzas, delivery) for delivery in deliveries])
    else:
        deliveries = [pizzas[delivery] for delivery in deliveries]
        unique_ingredients = get_unique_ingredients(deliveries)
        score = len(unique_ingredients) ** 2
    return score

def get_pizza(pizzas, pizzaIndices, team_count):

    maxScore = 0
    delivery = []
    delivery_permutations = permutations(pizzaIndices, team_count)
    for order in delivery_permutations:
        score = get_score(pizzas, order)
        if score > maxScore:
            maxScore = score
            delivery = list(order)
    return delivery, maxScore

def optimize_order(orders, totalPizzas):

    # Create a LP Maximization problem 
    Lp_prob = pl.LpProblem('Problem', pl.LpMaximize)  
    
    # Create problem Variables  
    x = pl.LpVariable("x", 0, orders[0], cat='Integer')   # Create a variable 0 <= x <= orders[0]
    y = pl.LpVariable("y", 0, orders[1], cat='Integer')   # Create a variable 0 <= y <= orders[1]
    z = pl.LpVariable("z", 0, orders[2], cat='Integer')   # Create a variable 0 <= z <= orders[2]
    
    # Objective Function 
    Lp_prob += 2 * x + 3 * y + 4 * z
    
    # Constraints: 
    Lp_prob += 2 * x + 3 * y + 4 * z <= totalPizzas
    
    Lp_prob.solve(pl.PULP_CBC_CMD(msg=0))   # Solver
    
    optimized_order = [int(v.varValue) for v in Lp_prob.variables()]
    
    delivered_pizzas = pl.value(Lp_prob.objective)
    
    return optimized_order, int(delivered_pizzas)

def solve(pizzas, orders, totalPizzas):

    orginal_orders = orders
    orders, totalPizzasDelivered = optimize_order(orders, totalPizzas)
    print(orders, totalPizzasDelivered)
    deliveries = []
    all_deliveries = []
    maxScore = 0
    team_count = 2
    for order in orders:
        if(order):
            pizzaIndices = [i for i in range(len(pizzas)) if i not in all_deliveries]
            for i in range(order):
                delivery, score = get_pizza(pizzas, pizzaIndices, team_count)
                all_deliveries = [*all_deliveries, *delivery]
                maxScore += score
                delivery = [str(x) for x in delivery]
                deliveries.append([str(team_count), *delivery])
            team_count += 1
    return deliveries, sum(orders), maxScore

def process(fileName):

    # Print data to console
    print("")
    print("-----------------------")
    print(fileName)
    print("-----------------------")

    #  Read the open file by name
    inputFile = open(inputFilesDirectory + fileName + ".in", "rt")

    #  Read file
    firstLine = inputFile.readline()
    pizzaList = inputFile.read()
    inputFile.close()


    #  Print input data
    print("INPUT")
    #print(firstLine)

    #  Assign parameters
    orders = list(map(int, firstLine.split()))
    totalPizzas = orders[0]
    orders = orders[1:]

    #  Create the pizza list by reading the file
    pizzaList = list(map(str, pizzaList.split('\n')))
    pizzas = [p.split()[1:] for p in pizzaList if p]

    #print(solve(pizzas, orders, totalPizzas))
    outputList, delivered_teams, score = solve(pizzas, orders, totalPizzas)  # Solve the problem and get output

    #  Print output data and create output file
       
    print("")
    print("OUTPUT")
    print(len(outputList))

    outputString = ""
    print(outputList)
    for l in outputList:
        outputString = outputString + " ".join(l) + "\n"

    outputFile = open(outputFilesDirectory + fileName + ".out", "w")
    outputFile.write(str(delivered_teams) + "\n")
    outputFile.write(outputString)
    outputFile.close()


inputFilesDirectory = "Input/"  # Location of input files
outputFilesDirectory = "Output/"  # Location of output files

fileNames = ["a_example", "b_little_bit_of_everything", "c_many_ingredients",
             "d_many_pizzas", "e_many_teams"]  # File names

for fileName in fileNames:  # Take each and every file and solve
    process(fileName)
