import heapq
import random
import math
from collections import deque


# Vraca Euklidsko rastojanje izmedju 2 tacke
def distance(curr_position, target_position):
    return math.sqrt((target_position[0] - curr_position[0])*(target_position[0] - curr_position[0])
         + (target_position[1] - curr_position[1])*(target_position[1] - curr_position[1]))

# Heuristika za algoritam a*, vraca euklidsko rastojanje
def h_cost(curr_position, target_position):
    return distance(curr_position, target_position)


def f_cost(curr_position, target_position, g_cost):
    return h_cost(curr_position, target_position) + g_cost[curr_position]

# Position_matrix predstavlja lavirint, 0 - slobodno polje, 1 - prepreka
# Funkcija vraca najkracu putanju od pozicije 1 do pozicije 2, koriscenjem algoritma a*
def minimal_distance(position1, position2, position_matrix):
    g_cost = {}
    parent = {}
    open_heap = [] 
    open_set = set([])
    closed = set([])
    
    g_cost[position1] = 0
    heapq.heappush(open_heap, (f_cost(position1, position2, g_cost), position1))
    open_set.add(position1)

    while open_heap:
        current = heapq.heappop(open_heap)[1]
        if current in closed:
            continue
        closed.add(current)

        #!!!
        if current == position2:
            path = []
            while current != position1:
                path.append(current)
                current = parent[current]
            return path

        for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if current[0] + dx < 0 or current[1] + dy < 0 or current[0] + dx >= len(position_matrix[0]) or current[1] + dy >= len(position_matrix):
                continue
            neigh = (current[0] + dx, current[1] + dy)
            (neighX, neighY) = neigh
            if position_matrix[neighX][neighY] == 1 or neigh in closed:
                continue
            else: 
                if neigh not in open_set or g_cost[current] + 1 < g_cost[neigh]:
                    g_cost[neigh] = g_cost[current] + 1
                    parent[neigh] = current
                    if neigh not in open_set:
                        heapq.heappush(open_heap, (f_cost(neigh, position2, g_cost), neigh))
                        open_set.add(neigh)


def center(x, y):
    return (x + 0.5, y + 0.5)
def ceil(x):
    if x == math.ceil(x):
        return x + 1
    return math.ceil(x)
def floor(x):
    if x == math.floor(x):
        return x - 1
    return math.floor(x)
def sgn(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

# Zamislimo da imamo dovoljno veliku tabelu. Posmatramo polja koordinata (x0, y0) i (x, y) 
# i njihove centre povezemo dijagonalom. Dijagonala prolazi kroz neka polja. 
# Funkcija path vraca listu tih polja.
def path(x0, y0, x, y): 
    path = []

    if x == x0:
        return [(x0, i)  for i in range(min(y, y0), max(y,y0) + 1)]

    if y == y0:
        return [(i, y0) for i in range(min(x, x0), max(x, x0) + 1)]

    path.append((x, y))
    (x, y) = center(x,y)
    (x0, y0) = center(x0, y0)    
    #dok (x0,y0) i (x,y) nisu u istom kvadraticu
    v = (x - x0, y - y0) 
    while (math.floor(x0), math.floor(y0)) != path[-1]:
        #print(path[-1])
        tx = min((ceil(x) - x0)/v[0], (floor(x) - x0)/v[0])
        ty = min((ceil(y) - y0)/v[1], (floor(y) - y0)/v[1])
        
        if tx == ty:
            path.append((path[-1][0] - sgn(x-x0),path[-1][1] - sgn(y-y0)))
        elif tx < ty:
            path.append((path[-1][0], path[-1][1] - sgn(y-y0)))
        else:
            path.append((path[-1][0] - sgn(x-x0), path[-1][1]))

        t = max(tx, ty)
        (x, y) = (x0 + t*v[0], y0 + t*v[1])
    return path

# Funkcija proverava da li se objekti na poljima pos1 i pos2 vide
# u lavirintu position_matrix. Objekti se vide ukoliko linija koja spaja centre polja ne sece
# unutrasnjost ni jednog zbuna 
def see_each_other(position1, position2, position_matrix):
    curr_path = path(position1[0], position1[1], position2[0], position2[1])
    for place in curr_path:
        if position_matrix[place[0]][place[1]]:
            return False
    return True
            
#vraca listu svih vidljivih polja u mapi iz tacke x0, y0
def all_visible_spaces_from(pair, map):
    (x0, y0) = pair
    #ukoliko se zbun nalazi na polju, ne interesuje se nas kolika je vidljivost tog polja
    if map[x0][y0] == 1:
        return []

    #dimenzije mape
    n = len(map)
    m = len(map[0])

    #ideja je da zamislimo nasu mapu kao graf, susedi su kvadratici koji imaju bar jednu zajednicku tacku
    #taj graf oblizamo bfsom, pa cemo koristiti red. 
    #collections je biblioteka u kojoj postoji klasa deque, preko koje se moze implementirati red 
    q = deque()
    #visited je recnik gde cuvamo sva "posecena" polja kao kljuceve. Polje je poseceno, ako ga ne treba opet dodati u red
    # vrednost moze biti 1,2,3
    # 2 ako se polje vidi, 3 ako se polje ne vidi, 1 ako tek treba da odlucimo 
    visited = {}

    
    #u red dodajemo tacku (x0,y0) 
    # i postavljamo visited na 1, posto tek treba da odlucimo da li vidimo ili ne vidimo (x0,y0) 
    q.append((x0, y0))
    visited[(x0,y0)] = 1

    #dok red nije prazan
    while not q == deque([]):
        #uzimamo kvadratic iz reda
        (x,y) = q.popleft()

        #proveravamo da li se taj kvadratic vidi, i postavljamo visited na odgovarajucu vrednost
        if is_visible_from(x, y, x0, y0, map, visited):
            visited[(x,y)] = 2
        else:
            visited[(x,y)] = 3

        #ukoliko se polje vidi, onda ima smisla u red stavljati njegove susede
        if visited[(x,y)] == 2:
            d =[0, -1, 1]
            for dx in d:
                for dy in d:
                    # ovde pazimo da koordinate koje smo dobili su ispravne i da nisu vec u recniku visited
                    if x + dx < n and x + dx >=0 and y + dy < m and y + dy >= 0 and not visited.has_key((x + dx, y+dy)):
                        q.append((x + dx, y + dy))
                        visited[(x + dx, y + dy)] = 1
    
    #pravimo listu visible koju cemo vratiti
    visible = set([])
    for key, value in visited.items():
        if value == 2:
            visible.add(key)
    return visible

    
# ova funkcija proverava da li se iz tacke (x0, y0) vidi tacka (x,y) u mapi, sa nekim dodatnim informacijama iz visited
def is_visible_from(x, y, x0, y0, map, visited):
    if x == x0 and y == y0:
        return True
    elif x == x0:
        y_prev = y - sgn(y - y0)
        return visited[(x,y_prev)] == 2 and map[x][y_prev] == 0
    elif y == y0:
        x_prev = x - sgn(x - x0)
        return visited[(x_prev,y)] == 2 and map[x_prev][y] == 0
    elif abs(x - x0) == abs(y - y0):
        x_prev = x - sgn(x - x0)
        y_prev = y - sgn(y - y0)
        return visited[(x_prev,y_prev)] == 2 and map[x_prev][y_prev] == 0
    elif abs(x-x0) > abs(y - y0):
        x_prev = x - sgn(x - x0)
        y_prev = y - sgn(y - y0)
        return  map[x_prev][y] == 0  and map[x_prev][y_prev] == 0
    elif abs(x-x0) < abs(y - y0):
        x_prev = x - sgn(x - x0)
        y_prev = y - sgn(y - y0)
        return  map[x][y_prev] == 0 and map[x_prev][y_prev] == 0
    else:
        exit()

#pomocna funkcija    
def f(x):
    x = abs(x)
    if x > 12:
        return 0
    funct = {0: 0, 1:0, 2:0, 3:0, 4:1, 5:2, 6:5, 7:9, 8:15, 9:20, 10:28, 11:30, 12:45}
    return funct[x]
