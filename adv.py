from room import Room
from player import Player
from world import World
import random
from ast import literal_eval
from util import Stack, Queue

world = World()

# MAPS
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# MAP INTO DICT
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

world.print_rooms()

player = Player(world.starting_room)



traversal_path = []
# create a blank dictionary called map
map = {}
# create explore method


def explore(player, moves):
    # Make it into a bfs
    # initialize Queue
    queue = Queue()
    # add starting room to queue
    queue.enqueue([player.current_room.id])
    # to store visited nodes
    visited = set()
    # while the queue has places to go
    while queue.size() > 0:
        # create a path by dequeueing
        path = queue.dequeue()
        # grab the last visited room
        current_room = path[-1]
        # if the current room isn't in visited, add to visited
        if current_room not in visited:
            visited.add(current_room)
            # loop through the exits
            for exit in map[current_room]:
                # if the exit in the map is ?, return path
                if map[current_room][exit] == '?':
                    return path
                # else, make a new path and enqueue
                else:
                    # copy
                    # make a copy of the path
                    new_path = list(path)
                    # append vertex to the coppied path
                    new_path.append(map[current_room][exit])
                    # then enqueue the copied path
                    queue.enqueue(new_path)
    return []

# create method to check for exits that haven't been tried


# make a queue for new_moves that will be used for unexplored function
new_moves = Queue()
def unexplored(player, new_moves):
    # set exits
    exits = map[player.current_room.id]
    # create empty list for untried exits to be used later
    untried = []
    # check exits of the current room for unexplored areas
    for direction in exits:
        if exits[direction] == "?":
            # add to untried so they can be explored
            untried.append(direction)
    # if there aren't any untried exits
    if len(untried) == 0:
        # explore until you find a room with unexplored exits
        not_explored = explore(player, new_moves)
        # set new room to the player's current room
        new_room = player.current_room.id
        # loop through each unexplored room
        for room in not_explored:
            # check for unexplored exits and add them to new moves
            for direction in map[new_room]:
                if map[new_room][direction] == room:
                    new_moves.enqueue(direction)
                    new_room = room
                    break
    # otherwise, try a random untried exit
    else:
        new_moves.enqueue(untried[random.randint(0, len(untried) - 1)])

# create moves that only use untried exits


# create an unexplored room dictionary
unexplored_room = {}
# go through the exits in the current room
for direction in player.current_room.get_exits():
    # add all ? exits to unexplored_room
    unexplored_room[direction] = "?"
    # the starting room should be an unexplored room
map[world.starting_room.id] = unexplored_room

# invoke unexplored
unexplored(player, new_moves)

# set the reverse directions, just like in the adventure game
reverse_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}

# while new_moves has items in it
while new_moves.size() > 0:
    # set the starting room
    current_room = player.current_room.id
    # grab a direction from new_moves
    move = new_moves.dequeue()
    # move that direction
    player.travel(move)
    # add that to traversal_path
    traversal_path.append(move)
    # set the player's next room to a variable
    next_room = player.current_room.id
    # set the map entry for the move to next_room
    map[current_room][move] = next_room
    # if it isn't in the map
    if next_room not in map:
        map[next_room] = {}
        # for each exit found in the current room
        for exit in player.current_room.get_exits():
            # set each unexplored exit to ?
            map[next_room][exit] = "?"
    # set the reversed direction to the map and set it to current room
    map[next_room][reverse_directions[move]] = current_room
    # if there are no moves left in new_moves
    if new_moves.size() == 0:
        # run unexplored again
        unexplored(player, new_moves)
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


# UNCOMMENT TO WALK AROUND
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
