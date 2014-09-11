/* Title: GraphLinkedListTonauty.c
 * Date: July 8, 2011
 * Author: Daniel Steeves
 * ID: 090565910
 * Email: stee5910@mylaurier.ca
 * Input: A graph represented by adjacency lists in linked list format
 * Output: A graph in nauty's 'graph' format
 * Method: A new nauty graph is created with the correct number
 *           of sets (vertices) and setwords for each set.
 *         The nauty graph starts with no adjacencies (edges)
 *         Adjacencies are specified from a vertex to a vertex
 *           when a pair of vertices is traversed in the linked
 *           list graph
 */

#include "nauty.h"
#include "GraphLinkedList.h"
#include "Utilities.h"

graph *GraphLinkedListTonauty(GraphLinkedList *GraphLinked)
     /* Reads in a linked list graph and outputs a graph
      * in nauty's 'graph' format
      * Params: GraphLinked - The input graph
      * Pre:    GraphLinked - A linked list graph
      *                       The 'n' field, the number of vertices
      *                       in the graph, must be specified
      * Post:   The nauty 'graph' derived from the linked list
      *         input graph is returned
      */
{
  int i, j; /* Counters */
  int m; /* Number of setwords per set */
  int n; /* Number of vertices (sets) */
  graph *Graphnauty; /* The resultant nauty graph */
  AdjListNode *CurAdjListNode;
  /* For traversing the source graph's adjacencies */

  n = GraphLinked->n;
  m = n / WORDSIZE;
  if(n % WORDSIZE > 0)
    /* If the division wasn't even */
    m++; /* Round up */

  Graphnauty = (graph *)malloc(m * n * sizeof(graph));
  /* Make the nauty graph */

  for(i = 0;i < m * n;i++)
    /* Fill the graph's incidence matrix with 0s
     * (no edges)
     */
    Graphnauty[i] = 0;

  for(i = 0;i < n;i++)
    /* Actually translate the adjacencies from
     * the source graph into the destination graph
     * Traverse each vertex of the source graph
     */
  {
    CurAdjListNode = GraphLinked->Vertices[i]->FirstAdj;
    while(CurAdjListNode != NULL)
      /* Traverse each adjacency of the current vertex in the
       * source graph
       */
    {
      j = CurAdjListNode->Vertex;

      Graphnauty[i * m + j / WORDSIZE] |=
	1 << WORDSIZE - 1 - j % WORDSIZE;
      /* Specify the adjacency if it exists */
      CurAdjListNode = CurAdjListNode->NextAdj;
      /* Move to the next adjacency for the current vertex */
    }
  }
  return Graphnauty;
}
