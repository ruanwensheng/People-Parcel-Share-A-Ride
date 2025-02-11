#PYTHON 
random_seed = 11042004
from copy import deepcopy
import random
from typing import List

# Process represent a Pick up or Delivery state of Package
class Process:
    def __init__(self, pID, ID, capacity, is_Pick):
        self.pID = pID
        self.ID = ID
        self.capacity = capacity
        self.is_Pick = is_Pick

    # print for debug
    def __str__(self):
        if self.is_Pick:
            return f'Pickup {self.pID} at {self.ID}, capacity = {self.capacity}'
        else:
            return f'Dropoff {self.pID} at {self.ID}, capacity = {self.capacity}'

# Package represent both Human and Request, if capacity == None => Human, else Request, each package contain 2 Process Pickup and Dropof
class Package:
    def __init__(self, ID, pID, dID, capacity):
        self.ID = ID
        self.pID = pID
        self.dID = dID
        self.capacity = capacity

        self.Pickup = Process(ID, pID, capacity, True)
        self.Dropoff = Process(ID, dID, capacity, False)

# Truck represent a Truck, have ID and capacity
class Truck:
    def __init__(self, ID, capacity, distance_matrix):
        self.ID = ID
        self.capacity = capacity
        self.distance_matrix = distance_matrix

        # list of packages that this truck delivery
        self.packages: List[Package] = []

        # Route of the Truck, list of Processes
        self.solRoute: List[Process] = [Process(0, 0, 0, True), Process(0, 0, 0, False)]
        
        # Time Done of the last Process is runtime off the Truck
        self.solRoute[-1].timeDone = 0

    # check capacity constraint and calc time
    def check_constraint(self, Route: List[Process]):
        current_capacity = 0
        current_time = 0

        for i in range(1, len(Route)):
            current_time += self.distance_matrix[Route[i-1].ID][Route[i].ID]

            # if this Process is human, do nothing
            if Route[i].capacity is None:
                continue
            # if this Process is Pickup, add Process capacity to current capacity
            if Route[i].is_Pick:
                current_capacity += Route[i].capacity
            else:
                current_capacity -= Route[i].capacity
            
            if current_capacity > self.capacity:
                return False
        Route[-1].timeDone = current_time
        return True

    def Insert(self, package: Package):
        temp_Route = self.solRoute.copy()
        best_Route = self.solRoute.copy()
        best_time = float('inf')

        for i in range(1, len(temp_Route)):
            # if 2 consecutive Process is human, pass, do nothing
            if temp_Route[i-1].capacity is None and temp_Route[i].capacity is None and temp_Route[i-1].pID == temp_Route[i].pID:
                continue

            temp_Route.insert(i, package.Pickup)

            # check constraint after insert
            if self.check_constraint(temp_Route):

                # if package is human
                if package.capacity is None:
                    # insert package's Dropoff right in next index
                    temp_Route.insert(i+1, package.Dropoff)

                    if self.check_constraint(temp_Route):
                        temp_time = temp_Route[-1].timeDone
                        # if new time better than best_time, update best Route, best time
                        if temp_time < best_time:
                            best_time = temp_time
                            best_Route = temp_Route.copy()

                else:
                    for j in range(i+1, len(temp_Route)):
                        # if 2 consecutive Process is human, pass, do nothing
                        if temp_Route[j-1].capacity is None and temp_Route[j].capacity is None and temp_Route[j-1].pID == temp_Route[j].pID:
                            continue
                        
                        # insert package's Dropoff to index j
                        temp_Route.insert(j, package.Dropoff)

                        if self.check_constraint(temp_Route):
                            temp_time = temp_Route[-1].timeDone

                            # if new time better than best_time, update best Route, best time
                            if temp_time < best_time:
                                best_time = temp_time
                                best_Route = temp_Route.copy()
                            
                            # reset temp Route
                            temp_Route = self.solRoute.copy()
                            temp_Route.insert(i, package.Pickup)
            
            # reset temp Route
            temp_Route = self.solRoute.copy()
        
        # assume that Insert will always success, update solRoute to bestRoute
        if best_time < float('inf'):
            self.solRoute = best_Route.copy()
            self.solRoute[-1].timeDone = best_time
            return True
        
        # if not, print for debug
        else:
            print("here")
            exit()

def import_data():
    distance_matrix = []
    trucks = []
    packages = []
    N, M, K = map(int, input().split())
    q = list(map(int, input().split()))
    Q = list(map(int, input().split()))

    for i in range(2*N+2*M+1):
        distance_matrix.append(list(map(int, input().split())))

    for i in range(K):
        trucks.append(Truck(i+1, Q[i], distance_matrix))
        
    for i in range(1, N + 1):
        if i <= N:
            packages.append(Package(i, i, i+N+M, None))
    for i in range(1, M + 1):
        packages.append(Package(i+N, i+N, i+2*N+M, q[i-1]))
        
    return trucks, packages    

random.seed(random_seed)

class Individual:
    def __init__(self, trucks: List[Truck], packages: List[Package], chromosome=None):
        # len of chromosome
        self.n = len(packages)
        if chromosome is None:
            self.chromosome = [random.randint(1, len(trucks)) for _ in range(self.n)]
        else:
            self.chromosome = chromosome
        
        self.trucks = deepcopy(trucks)
        self.packages = deepcopy(packages)

        self.fitness = 0
    
    def decode(self):
        for truck in self.trucks:
            truck.packages = []
            truck.solRoute = [Process(0, 0, 0, True), Process(0, 0, 0, False)]
            truck.solRoute[-1].timeDone = 0

        for i in range(len(self.chromosome)):
            self.trucks[self.chromosome[i]-1].packages.append(self.packages[i])
    
    def solve(self):
        self.decode()
        for truck in self.trucks:
            for package in truck.packages:
                truck.Insert(package)
    
    # calc fitness
    def calc_fitness(self):
        self.solve()
        fitnesses = [0 for _ in range(len(self.trucks))]

        for truck in self.trucks:
            fitnesses[truck.ID-1] = truck.solRoute[-1].timeDone
        
        return max(fitnesses), sum(fitnesses)
    
    # normal crossover
    def crossover(self, other):
        mom_chromosome, dad_chromosome = random.sample([self.chromosome, other.chromosome], 2)

        return mom_chromosome[:self.n//2] + dad_chromosome[self.n//2:]
    
    # mutation
    def mutation(self, rate):
        if random.random() < rate:
            choice = random.randint(0, self.n-1)
            self.chromosome[choice] = random.randint(1, len(self.trucks))

class GA:
    def __init__(self, trucks, packages, n, generations, mutation_rate):
        self.trucks = trucks
        self.packages = packages
        # Populations contain n Individual
        self.populations: List[Individual] = [Individual(trucks, packages) for _ in range(n)]
        self.n = n
        self.generations = generations
        self.mutation_rate = mutation_rate
    
    def solve(self):
        self.calc_fitness()
        self.best_sol = self.populations[-1]

        iteration = 0
        max_iteration = 50

        # run for ... generations
        for generation in range(self.generations):
            iteration += 1
            Probs = self.calc_fitness()

            if self.populations[-1].fitness < self.best_sol.fitness:
                self.best_sol = self.populations[-1]
                iteration = 0

            # early stopping
            if iteration > max_iteration:
                break

            new_gen = []

            # create new populations
            for i in range(self.n):
                # choose parent
                parent: List[Individual] = self.natural_selection(Probs)

                # cross over
                child_chromosome = parent[0].crossover(parent[1])

                child = Individual(self.trucks, self.packages, child_chromosome)

                # mutation
                child.mutation(self.mutation_rate)

                # add new gen
                new_gen.append(child)
        
            self.populations = new_gen
    
    def calc_fitness(self):
        for indiviudal in self.populations:
            indiviudal.fitness = indiviudal.calc_fitness()

        self.populations.sort(reverse=True, key=lambda x: x.fitness)

        sp = 1.2
        Probs = [1/self.n * (sp - (2*sp-2)*(i-1)/(self.n-1)) for i in range(1, self.n+1)]
        Probs.reverse()
        
        for i, individual in enumerate(self.populations):
            individual.prob = Probs[i]
        
        for i in range(1, len(Probs)):
            Probs[i] += Probs[i-1]
            
        return Probs

    # choose 2 parents based on rank
    def natural_selection(self, Probs):
        parent = []
        Probs = [0] + Probs

        for _ in range(2):
            choice = random.uniform(0, Probs[-1])
            for i in range(1, len(Probs)):
                if Probs[i-1] <= choice <= Probs[i]:
                    parent.append(self.populations[i-1])
                    break

        return parent

    def print_sol(self):
        print(len(self.trucks))
        for truck in self.best_sol.trucks:
            print(len(truck.solRoute))
            for node in truck.solRoute:
                print(node.ID, end=" ")
            print()
        
    def export_sol(self, file):
        with open(file, 'w') as f:
            f.write(f'{len(self.trucks)}\n')

            for truck in self.best_sol.trucks:
                f.write(f'{len(truck.solRoute)}\n')

                for node in truck.solRoute:
                    f.write(f'{node.ID} ')
                
                f.write("\n")

def main():
    trucks, packages = import_data()

    sol = GA(trucks, packages, 100, 100, 0.1)
    sol.solve()
    sol.print_sol()

main()
