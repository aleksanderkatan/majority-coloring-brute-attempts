# Attempts at disproving the Unfriendly Partition Conjecture

https://en.wikipedia.org/wiki/Unfriendly_partition

In this repo, I stored all my attempts at finding gadgets that could lead to a counterexample of the UPC.

There is also code for brute-finding a digraph that is not majority 3-colorable.

All graph files are sourced from [here](http://users.cecs.anu.edu.au/~bdm/data/digraphs.html).

## Concrete results:

### Oriented digraphs (no loops or cycles of length 2)

- Every digraph of up to 7 vertices is majority 3-colorable.

- For every digraph G of up to 6 vertices and every two of its vertices u and v, there exists a majority 3-coloring of G s.t. u and v are colored differently.

- Number of majority 3-colorings of a graph is not a function of the tuple of its out-degrees and/or in-degrees, even when limited to strongly connected graphs.

- For n in range {3, 4, 5}, across all graphs on n vertices every has at least 3*2^(n-2) colorings, the minimum being achieved for C3 + vertices of out-degree 1. For n=6, C3+C3 has 36 colorings instead of expected 48.

- Minimum colorings by vertices for strongly connected: {3: 6, 4: 18, 5: 24, 6: 48}

- Greedy algorithm that chooses an unsatisfied vertex and increases its color by one fails for some graphs of 6 vertices.


### Digraphs with allowed 2-cycles:

- Every digraph of up to 5 vertices is majority 3-colorable

- Minimum colorings by vertices: {3: 6, 4: 12, 5: 24} (same as without 2-cycles)

- Minimum colorings by vertices for strongly connected: {3: 6, 4: 18, 5: 24} (same as without 2-cycles)


