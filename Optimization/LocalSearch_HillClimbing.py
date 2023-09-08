import random

class Space():
    def __init__(self, length:int, width:int, num_hospitals:int) -> None:
        self.length = length
        self.width = width
        self.num_hospitals = num_hospitals
        self.step = [-1,0,1,0,-1]
        self.houses = set()
        self.hospitals = set()

    def add_a_house(self, x:int, y:int)->None:
        self.houses.add((x,y))

    def available_spaces(self) -> set[tuple[int,int]]:
        '''returns all cells not used by houses or hospitals now'''

        candidates = set((x,y) for x in range(self.length) for y in range(self.width))

        for house in self.houses:
            candidates.remove(house)
        for hospital in self.hospitals:
            candidates.remove(hospital)

        return candidates

    def get_cost(self, hospitals:set[tuple[int,int]]) -> int:
        '''Calculate the sum of distances from houses to the nearest hospital'''
        cost = 0
        for x, y in self.houses:
            cost += min(abs(x - i) + abs(y - j) for i, j in hospitals)
        return cost

    def get_neighbours(self, location:tuple[int,int]) -> list[tuple[int,int]]:
        x, y  = location
        neighbours = []
        for i,j in ((x + self.step[i], y + self.step[i+1]) for i in range(4)):
            if (i, j) in self.houses or (i, j) in self.hospitals:
                continue
            if 0 <= i < self.length and 0 <= j < self.width:
                neighbours.append((i, j))
        return neighbours

    def display(self) -> None:
        spaces = self.available_spaces()
        for x in range(self.length):
            for y in range(self.width):
                if (x, y) in spaces:
                    print('*',end = '')
                elif (x, y) in self.houses:
                    print('O',end = '')
                elif (x, y) in self.hospitals:
                    print('V',end = '')
            print()
        print()

    def hill_climb(self, max_count = None, log = False) -> set[tuple[int, int]]:

        self.hospitals = set()
        for i in range(self.num_hospitals):
            self.hospitals.add( random.choice(list(self.available_spaces()) ))
        
        print("initial state cost:", self.get_cost(self.hospitals))
        self.display()

        count = 0
        while max_count is None or count < max_count:
            count += 1
            best_neighbours = []
            least_cost = None

            neighbour = self.hospitals.copy()
            #Consider all hospitals to move
            for hospital in self.hospitals:
                neighbour.remove(hospital)
                for replacement in self.get_neighbours(hospital):
                    neighbour.add(replacement)
                    cost = self.get_cost(neighbour)
                    if least_cost is None or least_cost > cost:
                        least_cost = cost
                        best_neighbours = [neighbour.copy()]
                    elif least_cost == cost:
                        best_neighbours.append(neighbour.copy())
                    neighbour.remove(replacement)
                neighbour.add(hospital)

            if self.get_cost(self.hospitals) <= least_cost:
                return self.hospitals
            else:
                self.hospitals = random.choice(best_neighbours)
                if log:
                    print(count,':Found better neighbour cost', least_cost)
                    self.display()
    
    def random_restart(self, max_count, log = False) -> set[tuple[int, int]]:
        best_hospitals = None
        least_cost = None

        for i in range(max_count):
            if log:
                print(i,':')
            hospitals = self.hill_climb()
            cost = self.get_cost(hospitals)
            if least_cost is None or least_cost > cost:
                least_cost = cost
                best_hospitals = hospitals
                if log:
                    print('Found a new best state costs', least_cost)
                    self.display()
            elif log:
                print('no change, cost', cost)
                self.display()

        self.hospitals = best_hospitals
        if log:
            print('the final best state costs', self.get_cost(best_hospitals))
            self.display()
        return best_hospitals


if __name__ == "__main__":
    s = Space(7,7,2)
    for i in range(5):
        s.add_a_house(random.randrange(s.length),random.randrange(s.width))
    #s.hill_climb(max_count=7,log=True)
    s.random_restart(max_count=7,log=True)