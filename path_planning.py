import numpy as np

# Moves for the algorithm. Left panel for X and right panel for Y.
# Left Panel: -1 = Left, 0 = None, 1 = Right
# Right Panel : -1 = Down, 0 = None, 1 = Up
# Ex. [-1,0] = Left, [1,-1] = U
moves = np.array([[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]])


# Heuristic function based on distance between current position and goal
def heuristic_fnc(x, y, x_goal, y_goal):
    return np.sqrt(((x - x_goal) ** 2 + (y - y_goal) ** 2))


def create_path(init, goal, action):
    # We start looking at the end
    path = [[goal[0], goal[1]]]

    # From the finish point until we reach the start
    # We look the movement the algorithm took to reach the current point and "undo" the movement moving the inverse way
    x, y = goal
    while x != init[0] or y != init[1]:
        x_new = x - action[x][y][0]
        y_new = y - action[x][y][1]
        x = x_new
        y = y_new
        path.append([x_new, y_new])

    # As we begin looking at the end we have to pass the path from the beginning, so we reverse
    path.reverse()
    return np.array(path)


def findDijkstra(grid, init, goal, cost=1):
    # Discovered is an array of zeros(nothing is discovered yet)
    discovered = np.zeros_like(grid)
    discovered[init[0]][init[1]] = 1

    # Describe FROM WHERE the movement comes, so we can make the path from the finish(goal) to start once we reach goal
    action = np.ones_like(grid, dtype=np.ndarray) * np.nan

    # Set initial values, initial cost(0)
    x, y = init
    g = 0
    # The list contains cost to the point (x,y)
    queue = [[g, x, y]]
    c = 0
    while queue:
        c += 1
        # Sort the queue by g and pop the first.
        queue.sort()
        g, x, y = queue.pop(0)

        if x == goal[0] and y == goal[1]:
            break
        else:
            # Iterate through all the possible moves
            for movement in moves:
                # Set the new point after a movement
                x_new = x + movement[0]
                y_new = y + movement[1]

                # If new point is inside the boundaries, not discovered yet, and it is not and obstacle then...
                if x_new in range(0, grid.shape[0]) and y_new in range(0, grid.shape[1]) \
                        and discovered[x_new, y_new] == 0 and grid[x_new, y_new] >= 128:

                    # Calculate the cost, set the point as discovered and set the action as the movement made
                    g_new = g + cost
                    queue.append([g_new, x_new, y_new])
                    discovered[x_new, y_new] = 1
                    action[x_new, y_new] = movement
    else:
        print('No way found')
    return create_path(init, goal, action)


def findA(grid, init, goal, cost=1):

    # Discovered is an array of zeros(nothing is discovered yet)
    discovered = np.zeros_like(grid)
    discovered[init[0]][init[1]] = 1

    # Describe FROM WHERE the movement comes, so we can make the path from the finish(goal) to start once we reach goal
    action = np.ones_like(grid, dtype=np.ndarray) * np.nan

    # Set initial values, initial cost and heuristic
    x, y = init
    g = 0
    h = heuristic_fnc(x, y, goal[0], goal[1])
    f = g + h
    # The list contains the heuristic and the cost to the point (x,y)
    queue = [[f, g, x, y]]

    step = 0
    while queue:
        step += 1

        # Sort the queue by f and pop the first.
        queue.sort()
        f, g, x, y = queue.pop(0)

        if x == goal[0] and y == goal[1]:
            break
        else:
            # Iterate through all the possible moves
            for movement in moves:
                # Set the new point after a movement
                x_new = x + movement[0]
                y_new = y + movement[1]

                # If new point is inside the boundaries, not discovered yet, and it is not and obstacle then...
                if x_new in range(0, grid.shape[0]) and y_new in range(0, grid.shape[1]) \
                        and discovered[x_new, y_new] == 0 and grid[x_new, y_new] >= 128:

                    # Calculate heuristic and cost, set the point as discovered and set the action as the movement made
                    g_new = g + cost
                    h_new = heuristic_fnc(x, y, goal[0], goal[1])
                    f_new = (g_new + h_new) - 0.0001 * step
                    queue.append([f_new, g_new, x_new, y_new])
                    discovered[x_new, y_new] = 1
                    action[x_new, y_new] = movement

    else:
        print('No way found')
    return create_path(init, goal, action)
