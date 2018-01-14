# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 16:41:25 2018

@author: SUBHANNITA
"""
import random
import functools

def diagonal_exclusion(pos,individual):
    #returns list of positions for queen(pos) that would get queen(pos) checked via diagonal
    #individual, in this func, is either individual in progess or individual[0:pos]
    dia=[]
    for queen in individual:
        if queen+pos in range(8):
            dia.append(queen+pos)
        if queen-pos in range(8) and queen+pos != queen-pos:
            dia.append(queen-pos)
        pos=pos-1
    return dia


def generate_population(population_size):
    
    population=[]
    for i in range(population_size):
        individual=[]
        for j in range(8):
            dia=diagonal_exclusion(j,individual)
            #random choice from list of available (non threatened) queen positions
            r=[e for e in range(8) if e not in individual and e not in dia]
            if len(r) != 0:
                individual.append(random.choice(r))
            else:
                #if no queen positions available take any one that is not horizontally threatened
                individual.append(random.choice([e for e in range(8) if e not in individual]))

        population.append(individual)
#    print(population)
    return population


def evaluate_fitness(population):
    #evaluate fitness in range of 0 to 1 for each individual in population
    worst_fitness=28
    individual_fitness=[]
    for individual in population:
        fitness=0       
        for pos in range(8):
            #dia is list of check positions for queen(pos) by queens left of pos
            dia=diagonal_exclusion(pos,individual[:pos])
            #count the number of queens who would check queen(pos),i.e., number of occurences of queen(pos) in dia
            fitness += dia.count(individual[pos])
        #convert to maximisation problem    
        individual_fitness.append(worst_fitness-fitness)
    #convert to format for roulette wheel selection of parents
    total=sum(individual_fitness)
    individual_fitness = [float(e/total) for e in individual_fitness]
    return individual_fitness
            

def parent_selection(population,individual_fitness):
    #roulette wheel selection; from each generation 2 parents are selected
    parents=[]
    for j in range(2):
        distribution=0
        r=random.uniform(0.0,1.0)
        for i in range(len(population)):
            distribution += individual_fitness[i]
            if r < distribution:
                parents.append(population[i])
                break
#    print(parents)
    return parents
        
  
def crossover(parents):
    #take care that permutation is not disturbed
    children=[]
    crossover_probability=float(100/100)
    r=random.uniform(0.0,1.0)
    if r < crossover_probability:
        #crossover happens
        crossover_point=random.randint(1,7)
        child=parents[0][:crossover_point]
        child += [e for e in parents[1][crossover_point:] if e not in child]
        child += [e for e in parents[1][:crossover_point] if e not in child]
        children.append(child)
        child=parents[1][:crossover_point]
        child += [e for e in parents[0][crossover_point:] if e not in child]
        child += [e for e in parents[0][:crossover_point] if e not in child]
        children.append(child)
#        print("Crossover at ",crossover_point)
        
    else:
        #crossover does not happen->same parents passed through
#        print("Crossover passed through")
        children = parents

    return children


def mutation(parent):
    #Q:if q0 gets swapped with q7, then can q1 swap again with q0(now in index 7)
    mutation_probability=float(80/100)

    for queen in range(8):
        r=random.uniform(0.0,1.0)

        if r < mutation_probability:
            #this queen qill be swapped
            while True:
                #make sure its a different queen to swap with
                r = random.randint(0,7)
                if parent[queen] != parent[r]:
                    break
            temp=parent[r]
            parent[r]=parent[queen]
            parent[queen]=temp

        
    return parent
            

def survivor_selection(population,children):
    
    population += children
    individual_fitness = evaluate_fitness(population)
    sorted_individuals = [e for _, e in sorted(zip(individual_fitness,population), reverse=True)]
#    print (sorted_individuals)
    survivors = sorted_individuals[:population_size-1]
    return survivors
              
    
 
    


population_size = 1000
max_iterations = 10000
max_fitness=[]
mean_fitness=[]
population = generate_population(population_size)
iteration=1
#print(population)
while True:
    
    print ("Generation: ", iteration)
    children=[]
    individual_fitness = evaluate_fitness(population)
    max_fitness.append(max(individual_fitness))
    mean_fitness.append(functools.reduce(lambda x, y: x+y, individual_fitness)/population_size)
    print("Max fitness: ", max_fitness[-1], " Mean fitness: ", mean_fitness[-1])
    #terminal condition; not included: fitness not changing appreciably over generations
    if 1.0 in individual_fitness or iteration == max_iterations:
        break
    parents = parent_selection(population,individual_fitness)
#    print("Selected parents: ",parents)
    crossover_children = crossover(parents)
    for parent in crossover_children:
        children.append(mutation(parent))
#    print ("Children: ",children)
    population = survivor_selection(population,children)
    iteration += 1

    
    
    
    
    
    