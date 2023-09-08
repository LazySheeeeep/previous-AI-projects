class Node():
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, state):
        self.frontier.append(state)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return 0 == len(self.frontier)
    
    def pop(self):
        if self.empty():
            raise Exception("EMPTY!!")
        else:
            return self.frontier.pop(len(self.frontier)-1)

class QueueFrontier(StackFrontier):
    def pop(self):
        if(self.empty()):
            raise Exception("EMPTY!!")
        else:
            return self.frontier.pop(0)

class Maze():
    def __init__(self, filename):
        with open(filename,'r') as f:
            contents = f.read()

        if contents.count('S') != 1:
            raise Exception()

        if contents.count('Z') != 1:
            raise Exception()

        contents = contents.splitlines()
        self.ylength = len(contents)
        self.xlength = max(len(length) for length in contents) 

        self.walls = []
        for i in range(self.ylength):
            current_row = []
            for j in range(self.xlength):
                try:
                    if contents[i][j] == 'S':
                        self.start = (i, j)
                        current_row.append(False)
                    elif contents[i][j] == 'Z':
                        self.goal = (i, j)
                        current_row.append(False)
                    elif contents[i][j] == '#':
                        current_row.append(False)
                    else:
                        current_row.append(True)
                except IndexError:
                    current_row.append(False)
            self.walls.append(current_row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if not col:
                    if (i, j) == self.start:
                        print('S',end = '')
                    elif (i, j) == self.goal:
                        print('Z',end = '')
                    elif solution is not None and (i, j) in solution:
                        print('*',end = '')
                    else:
                        print(' ',end = '')
                else:
                    print('@',end = '')
            print()
        print()

    def neighbours_of_state(self, state):
        x, y = state
        candidate = [
            ('up',(x,y+1)),
            ('down',(x,y-1)),
            ("left",(x-1,y)),
            ("right",(x+1,y))]
        neighbours = []

        for action, (i, j) in candidate:
            try:
                if not self.walls[i][j]:
                    neighbours.append((action, (i, j)))
            except IndexError:
                continue
        return neighbours

    def solve(self):
        self.num_explored = 0

        start = Node(self.start,None,None)

        frontier = StackFrontier()
        frontier.add(start)

        self.nodes_explored = set()

        while True:
            if frontier.empty():
                raise Exception("NO SOLUTION!!")

            node = frontier.pop()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions,cells)
                return

            self.nodes_explored.add(node.state)

            for action, state in self.neighbours_of_state(node.state):
                if state not in self.nodes_explored and not frontier.contains_state(state):
                    child = Node(state = state,parent = node,action = action)
                    frontier.add(child)

'''
maze = Maze('maze.txt')
maze.solve()
maze.print()
'''





