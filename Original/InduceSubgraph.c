/* Title: InduceSubgraph.c
 * Date: June 17, 2011
 * Author: Daniel Steeves
 * ID: 090565910
 * Email: stee5910@mylaurier.ca
 * Input: A graph in setword format, and a map
 *          (array) of the vertices to induce the
 *          subgraph
 * Output: The induced subgraph
 * Method: Traverse all the setwords in the graph
 *           and specify adjacencies in the subgraph
 *           that exist among the inducing verticies
 *           in the graph
 */

#include "nauty.h"

graph *InduceSubgraph(graph *g,
		      int *SubgraphVertices,
		      int m,
		      int n,
		      int p)
     /* Takes a graph and a subset of the vertices of that graph,
      * and creates an induced subgraph
      * Params: g - the graph
      *         SubgraphVertices - The array of vertices for the subgraph
      *                            An index on this array is a vertex in
      *                            the subgraph, and dereferences as a
      *                            vertex in the graph
      *         m - number of setwords per set in the graph
      *         n - number of vertices in the graph
      *         p - number of vertices in the subgraph
      * Pre:    g - a graph in setword format
      *         SubgraphVertices - an array of integers
      *         m, n, p - positive integers
      * Post:   The subgraph is returned
      */
{
  graph *InducedSubgraph;
  setword gSetword; /* Setword from g */
  int i, j; /* Counters */
  int o; /* Number of setwords per set in the subgraph */

  o = p / WORDSIZE;
  if(p % WORDSIZE > 0)
    /* If the division wasn't even */
    o++; /* Round up */

  InducedSubgraph = (graph *)malloc(o * p * sizeof(graph));
  /* Allocate space for the subgraph */

  for(i = 0;i < o * p;i++)
    /* Fill the subgraph's incidence matrix with 0s
     * (no edges)
     */
    InducedSubgraph[i] = 0;

  for(i = 0;i < p;i++)
    for(j = 0;j < p;j++)
      /* Consider all possible adjacencies */
    {
      gSetword = g[SubgraphVertices[i] * m + SubgraphVertices[j] / WORDSIZE];
      /* Read in the setword from g containing the i,jth entry
       * in the adjacency matrix 
       */
      gSetword &= 1 << (WORDSIZE - 1 - SubgraphVertices[j] % WORDSIZE);
      /* Mask out all bits except the one that represents the
       * i,jth entry
       */
      if(gSetword > 0)
	gSetword = 1;
      /* Moves the target bit of the graph into the least
       * significant position
       */
      gSetword <<= WORDSIZE - 1 - j % WORDSIZE;
      /* Moves the target bit of the graph into the position of the 
       * target bit in the subgraph
       */
      InducedSubgraph[i * o + j / WORDSIZE] |= gSetword;
      /* Set the target bit (specify an edge) in the subgraph
       * if it is set in the graph
       */
    }
  return InducedSubgraph;
}
