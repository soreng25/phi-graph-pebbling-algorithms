"""
Let a graph G have n verticies labeled from 0 to n-1
connections is a list (of lists) of length n where connections[i] is a list of all verticies that vertex #i is connected to by an edge

If main(connections) == True then G has diameter <= 2. If the function returns False then G has diameter >= 3.

Time Complexity = O(n^3)
Space Complexity = O(n^2)

Example for K{4,3} graph (diameter = 2):
connections = [ [4,5,6], [4,5,6], [4,5,6], [4,5,6], [0,1,2,3], [0,1,2,3], [0,1,2,3] ]
returns True
"""

def diameter_2_checker(connections, i, j):
    if i in connections[j]:
        return True

    for k in connections[i]:
        if k in connections[j]:
            return True
    return False

def main(connections):
    counter = 0
    
    for i in range(len(connections)):
        for j in range(i + 1, len(connections)):
            if diameter_2_checker(connections, i, j):
                counter += 1
            else:
                return i, j
                
    if counter == len(connections) * (len(connections) - 1) / 2:
        return True
    return False

#Example of a complex diameter-2 graph
print (
main([ [10,4,7,9],
       [11,4,5,8],
       [12,5,6,7],
       [13,6,8,9],
       [0,1,10,11,5,6,7,8,9],
       [1,2,11,12,4,6,7,8,9],
       [2,3,12,13,4,5,7,8,9],
       [0,2,10,12,4,5,6,8,9],
       [1,3,11,13,4,5,6,7,9],
       [0,3,10,13,4,5,6,7,8],
       [11,12,13,0,4,7,9],
       [10,12,13,1,4,5,8],
       [10,11,13,2,5,6,7],
       [10,11,12,3,6,8,9],
       [10,11,12,13]   ]

    )
)
