from heapq import heappush, heappop

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(deck, pos):
    x, y = pos
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < deck.width and 
            0 <= new_y < deck.height and 
            deck.tiles[new_y][new_x].is_walkable()):
            neighbors.append((new_x, new_y))
    
    return neighbors

def find_path(deck, start, goal):
    if not (deck.tiles[goal[1]][goal[0]].is_walkable()):
        return []

    frontier = []
    heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heappop(frontier)[1]

        if current == goal:
            break

        for next_pos in get_neighbors(deck, current):
            new_cost = cost_so_far[current] + 1
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + manhattan_distance(goal, next_pos)
                heappush(frontier, (priority, next_pos))
                came_from[next_pos] = current

    # Reconstruct path
    if goal not in came_from:
        return []

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    
    return path
