from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from utils import Stack, Queue


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

visited_graph = {}


def adjacent_rooms_check(current_room, check_room):
    if current_room == check_room:
        return 'same room'
    elif current_room.n_to == check_room:
        return 'n'
    elif current_room.s_to == check_room:
        return 's'
    elif current_room.e_to == check_room:
        return 'e'
    elif current_room.w_to == check_room:
        return 'w'

# if not adjacent, BFS to find shortest path to new node
def bfs(current_room, target_room):
  
    q = Queue()
    q.enqueue([current_room])
    # create a set of traversed vertices
    visited = set()
    # while queue is not empty:
    while q.size() > 0:
        # dequeue/pop first vertex
        path = q.dequeue()
        current = path[-1]
        # if not visited
        if current not in visited:
            
            if current == target_room:
                return path
            # mark as visited
            visited.add(current)
            # enqueue all neighbors
            for option in current.get_exits():
                new_path = list(path)
                new_path.append(current.get_room_in_direction(option))
                q.enqueue(new_path)

# DFS
s = Stack()
s.push([player.current_room])
visited = set()
while s.size() > 0:
    path = s.pop()
    current = path[-1]
    player_position = adjacent_rooms_check(player.current_room, current)
    
    if current.id not in visited: # change to visited
        if player_position != None and player_position != 'same room':
            player.travel(player_position)
            traversal_path.append(player_position)
        # creating the room entry in our graph
        visited_graph[current.id] = {}
        visited.add(current.id) # added
        for option in current.get_exits():
            visited_graph[player.current_room.id].update({option: None})
        # Each time a node is removed, check adjacency to current position
        # player_position = adjacent_rooms_check(player.current_room, current)
        if player_position == 'same room':
            for next_room in player.current_room.get_exits():
                new_path = path + [player.current_room.get_room_in_direction(next_room)]
                s.push(new_path)
        else:
            # if not adjacent, BFS to find shortest path to our new room
            shortest = bfs(player.current_room, path[-1])
            # now that we have the shortest path to our new room, we need to figure out direction to get there
            # empty list to track directions
            position = []
            # checking the adjacency of each room in our shortest path
            for room in shortest:
                direction = adjacent_rooms_check(player.current_room, room)
                # adding the correct direction to the list
                if direction != 'same room':
                    position.append(direction)
                    # moving in the direction
                    player.travel(direction)
            # adding those movements to the list
            traversal_path += position
            for next_room in player.current_room.get_exits():
                new_path = path + [player.current_room.get_room_in_direction(next_room)]
                s.push(new_path)
            


# print('visited graph')
# print(visited_graph)
# print('path')
# print(traversal_path)



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
