import time
from Data import Data
from AStar_iterative import AStar_itearative
from AStar import AStar

from UCS_iterative import UCS_iterative
from UCS import UCS

from DFS import DFS
from GreedyDFS import GreedyDFS
from RandomSolver import RandomSolver


if __name__ == "__main__":
    # TODO: Edit this variable
    FILE_PATH = "C:\cs451\Tuğçe_Özgirgin_S024268_hw1\hw1\small.pkl"  # Such as "small.pkl", "medium.pkl", "large.pkl"

    # Load data-
    data = Data(FILE_PATH)
        
    # A*
    print("A* Iterative")
    a_star_it = AStar_itearative(data)
    start_time = time.time()
    solution_a_star = a_star_it.solve()
    end_time = time.time()
    print("Feasibility:", data.is_feasible(solution_a_star))
    print("Objective Value:", data.calculate_objective(solution_a_star))
    print("Elapsed Time (sec):", end_time - start_time)
    print("the route: ", end=" ")
    for node in solution_a_star:
      print(node.id, end=",")
    print("\n")

    # A*
    print("A* Recursive")
    a_star_rec = AStar(data)
    start_time = time.time()
    solution_a_star = a_star_rec.solve()
    end_time = time.time()
    print("Feasibility:", data.is_feasible(solution_a_star))
    print("Objective Value:", data.calculate_objective(solution_a_star))
    print("Elapsed Time (sec):", end_time - start_time)
    print("the route: ", end=" ")
    for node in solution_a_star:
      print(node.id, end=",")
    print("\n")
    
    #GreedyDFS -suboptimal
    print("Greedy DFS")
    dfs = GreedyDFS(data)
    start_time = time.time()
    solution_dfs = dfs.solve()
    end_time = time.time()
    print("Feasibility:", data.is_feasible(solution_dfs))
    print("Objective Value:", data.calculate_objective(solution_dfs))
    print("Elapsed Time (sec):", end_time - start_time)
    print("the route: ", end=" ")
    for node in solution_dfs:
      print(node.id, end=",")
    print("\n")

    #DFS
    print("DFS")
    dfs = DFS(data)
    start_time = time.time()
    solution_dfs = dfs.solve()
    end_time = time.time()
    print("Feasibility:", data.is_feasible(solution_dfs))
    print("Objective Value:", data.calculate_objective(solution_dfs))
    print("Elapsed Time (sec):", end_time - start_time)
    print("the route: ", end=" ")
    for node in solution_dfs:
      print(node.id, end=",")
    print("\n")

    #UCS Recursive
    print("UCS Recursive")
    ucs_recursive = UCS(data)
    start_time = time.time()
    solution_ucs = ucs_recursive.solve()
    end_time = time.time()
    print("Feasibility:", data.is_feasible(solution_ucs))
    print("Objective Value:", data.calculate_objective(solution_ucs))
    print("Elapsed Time (sec):", end_time - start_time)
    print("the route: ", end=" ")
    for node in solution_ucs:
      print(node.id, end=",")
    print("\n")

    # UCS Iterative
    print("UCS Iterative")
    ucs = UCS_iterative(data)
    start_time = time.time()
    solution_ucs = ucs.solve()
    end_time = time.time()
    print("Feasibility:", data.is_feasible(solution_ucs))
    print("Objective Value:", data.calculate_objective(solution_ucs))
    print("Elapsed Time (sec):", end_time - start_time)
    print("the route: ", end=" ")
    for node in solution_ucs:
      print(node.id, end=",")
    print("\n")


