# Background
The phi-pebbling number of a graph, denoted by Φ(G) is defined similarly to the pebbling number of a graph, denoted by π(G), except every pebble is allowed 1 "free" move to an adjacent vertex before standard 2-for-1 pebbling occurs. It is known that Φ(G) ≤ ⌊π(G)/2⌋ but we improve this bound for a large variety of graph families, and provide examples where the bound is sharp.

Note that verifying phi-pebbling numbers is an NP-Complete problem and verifying the diameter of a graph is a P problem.

# Methodology
For each graph family, in order to formulate the phi-pebbling numbers, we first attempted some smaller cases by hand and made a conjecture. Second, we tested whether this conjecture held for some larger cases using the phi-pebbling.py code. Lastly, if everything held, then all results were rigorously proven using combinatorial techniques.

In some cases, such as Diameter-2 Graphs, we had to run additional testing to verify that each graph does indeed have a diameter of 2 (which in itself is an interesting problem), using programs such as the one found in diameter-2.py.

# Results 
Radius-1 Graphs (Stars, Wheels, Friendship, etc.) : Φ(R) ≤ 2
Diameter-2 Graphs: Φ(D) ≤ ⌊√(4n+5)⌋ - 2
Complete Graphs: Φ(K_n) = 1
Complete k-Partite Graphs: Φ(K_m,n) ≤ 2
Path Graphs: Φ(P_n) = 2^(n-2)
Hypercubes: Φ(Q_n) = ⌈3^n/2⌉
Trees: Φ(T) = Σ(2^(l-1) - 1) + 1
Thorn Graphs: Φ(G*) = π_2(G)
Cycle Graphs: Φ(C_n) = π(C_n)/2 if n ≡ 0 or 2 (mod 4), ⌈π(C_n)/2⌉ if n ≡ 1 (mod 4), ⌊π(C_n)/2⌋ if n ≡ 3 (mod 4)
Fan Graphs: Φ(F_m,n) ≤ 2 Petersen Graph: Φ(P) = 3
Cartesian Products: Φ(G x H) ≤ min{Φ(G)(π(H)+|H|), Φ(H)(π(G)+|G|)}
Grids: Φ(G_m,n) = 2^(m+n-3)
Crowns: Φ(C_n) ≤ 4
Platonic Graphs (In order of |V|): 2, 2, 3, FINISH LAST TWO GRAPHS

# To Do List
Platonic Graph (FINISH)
Braids, Cactus
Snarks

