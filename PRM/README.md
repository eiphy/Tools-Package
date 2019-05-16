These scripts are used to find the shortest path in a randomly generated map.

If the program doesn't find a path to the goal point, it will densen the map and try again. If still no solution, it asks for your instruction.
The pval is the percentage of its current val, i.e new_val = current_val * pval.
Pree Enter to abandon this query.

As for the performance, test has made w.r.t node density = 10 & r = 1. For the newly generated environment, the program usually used several seconds to
generate the roadmap and finish path planning. Once the roadmap is established, usually less than 0.2 seconds are needed to plan a new path. The node density
will largely affect the computation time.

These scripts can run on win(python3.7) and ubuntu18(python3.6)