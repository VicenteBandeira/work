import numpy as np
from queue import PriorityQueue
from collections import deque
import math

#constantes
ROWS = 4
COLS = 4

#estrutura do puzzle
class Puzzle:
    def __init__(self, initial_state, final_state): #construtor da classe
        self.initial_state = np.array(initial_state).reshape((ROWS, COLS))
        self.final_state = np.array(final_state).reshape((ROWS, COLS))
    
    def is_even(self, n): #verifica se um inteiro n e par
        return n%2==0

    def solvable(self):  # verificar se e possivel alcancar o estado final do estado inicial

        row_initial,col_initial = np.argwhere(self.initial_state == 0)[0]
        row_final,col_final = np.argwhere(self.final_state == 0)[0]

        initial = self.initial_state.flatten()
        final = self.final_state.flatten()

        sum_initial = 0
        sum_final = 0


        for i in range(len(initial) - 1):
            for j in range(i, len(initial)):
                if initial[j] < initial[i] and initial[j] != 0:
                    sum_initial += 1
                if final[j] < final[i] and final[j] != 0:
                    sum_final += 1

        #Condition initial
        if self.is_even(sum_initial) != self.is_even(row_initial):
            cond_initial = True
        else:
            cond_initial = False
        if self.is_even(sum_final) != self.is_even(row_final):
            cond_final = True
        else:
            cond_final = False
        if cond_initial == cond_final:
            print("E possivel alcancar o estado final dado este estado inicial")
            return

        print("Nao e possivel alcancar o estado final dado este estado inicial")
        exit() 

    def is_goal_state(self, state): #verifica se um dado estado e o estado objetivo
        return np.array_equal(state, self.final_state)
    
    def get_states(self, state): #dada uma configuracao do tabuleiro retorna todos os estados possiveis a partir dela
        possible_states = []
        row0, col0 = np.argwhere(state == 0)[0]

        if row0+1<=3:
            new_state = np.copy(state)
            new_state[row0][col0] = new_state[row0+1][col0]
            new_state[row0+1][col0] = 0
            possible_states.append(new_state)
        
        if row0-1>=0:
            new_state = np.copy(state)
            new_state[row0][col0] = new_state[row0-1][col0]
            new_state[row0-1][col0] = 0
            possible_states.append(new_state)
        
        if col0+1<=3:
            new_state = np.copy(state)
            new_state[row0][col0] = new_state[row0][col0+1]
            new_state[row0][col0+1] = 0
            possible_states.append(new_state)
        
        if col0-1>=0:
            new_state = np.copy(state)
            new_state[row0][col0] = new_state[row0][col0-1]
            new_state[row0][col0-1] = 0
            possible_states.append(new_state)
        
        return possible_states
    
    def dfs(self, max_depth):
        stack = [(self.initial_state, 0)]
        visited = set()

        while stack:
            state, steps = stack.pop()
            visited.add(tuple(state.flatten()))

            if self.is_goal_state(state):
                print("Solucao encontrada em", steps, "passos.")
                return state, steps

            if steps < max_depth:
                for new_state in self.get_states(state):
                    if tuple(new_state.flatten()) not in visited:
                        stack.append((new_state, steps+1))

        print("Solucao nao encontrada dentro da profundidade maxima")
        return None, None
    
    def bfs(self, max_depth):
        queue = deque([(self.initial_state, 0)])
        visited = set()

        while queue:
            state, steps = queue.popleft()
            visited.add(tuple(state.flatten()))

            if self.is_goal_state(state):
                print("Solucao encontrada em", steps, "passos")
                return state

            if steps<max_depth:
                for new_state in self.get_states(state):
                    if tuple(new_state.flatten()) not in visited:
                        queue.append((new_state, steps+1))
        
        print("Solucao nao encontrada dentro da profundidade maxima")
        return None, None

    
    def greedy_search(self, max_depth):
        initial_state = self.initial_state
        visited = set()
        queue = PriorityQueue()
        queue.put(self.heuristics(initial_state), initial_state, 0)

        while not queue.empty():
            _, current_state, depth = queue.get()
            visited.add(current_state)

            if self.is_goal_state(current_state):
                print("Solucao encontrada em", depth, "passos")

            if depth >= max_depth:
                continue

            for possible_state in self.get_states(current_state):
                if possible_state not in visited:
                    visited.add(possible_state)
                    queue.put(self.heuristics(possible_state), possible_state, depth+1)

        print("Solucao nao encontrada dentro da profundidade maxima")
        return None

    
    def out_of_place(self, state): #o numero de pecas "fora do sitio"
        count = 0
        for i in range(ROWS):
            for j in range(COLS):
                if state[i][j] != self.final_state[i][j]:
                    count += 1
        return count
    
    def manhattan_distance(self, state, final_state): #manhattan distance
        distance = 0

        for i in range(ROWS):
            for j in range(COLS):
                x, y = np.argwhere(final_state==state[i][j])[0]
                distance+=math.ceil(math.dist(state[i][j], state[x][y]))
        
        return distance

    def heuristics(self, state):
        return (self.out_of_place(state)+self.manhattan_distance)

initial_state = list(map(int, input(). strip(). split()))
initial_state = np.array(initial_state).reshape(ROWS, COLS)

final_state = list(map(int, input(). strip(). split()))
final_state = np.array(final_state).reshape(ROWS, COLS)

print(initial_state)
print(final_state)

puzzle = Puzzle(initial_state, final_state)
puzzle.solvable()

solution_dfs = puzzle.dfs(12)
solution_bfs = puzzle.bfs(12)
solution_greedy = puzzle.greedy_search(puzzle.initial_state)

