/* Title: GraphLinkedList.c
 * Date: July 11, 2011
 * Author: Daniel Steeves
 * ID: 090565910
 * Email: stee5910@mylaurier.ca
 * Input: Parameters to construct graphs
 * Output: The constructed graph, and information about the graph
 * Method: Implements and manipulates graphs in an adjacency list
 *         graph representation using linked lists
 */

#include "nauty.h"
#include "GraphLinkedList.h"

GraphLinkedList *GraphLinkedListCreate()
     /* Creates a graph using the linked list implementation
      * Params: None
      * Pre:    None
      * Post:   A pointer to the newly created graph is returned
      */
{
  GraphLinkedList *g;
  g = (GraphLinkedList *)malloc(sizeof(GraphLinkedList));
  /* Create the graph */
  g->n = 0;
  /* No vertices to start */
  return g;
}

void GraphLinkedListInsertVertex(GraphLinkedList *g)
     /* Inserts a new vertex into a linked list graph
      * Params: g - The graph to insert into
      * Pre:    g - A linked list graph
      * Post:   A new vertex is inserted
      */
{
  AdjList **Vertices; /* Points to the old set of vertices */
  AdjList **NewVertices; /* Points to the new set of vertices */
  int i; /* Counter */
  int n; /* Number of vertices to start */
  Vertices = g->Vertices;
  n = g->n;
  NewVertices = (AdjList **)malloc((n + 1) * sizeof(AdjList *));
  /* Make room for the new set of vertices */
  for(i = 0;i < n;i++)
    /* Copy over the adjacency list pointers */
    NewVertices[i] = Vertices[i];
  free((void *)Vertices);
  /* Done copying, free up space taken up by old pointers */
  NewVertices[n] = (AdjList *)malloc(1 * sizeof(AdjList));
  /* Create the new vertex */
  NewVertices[n++]->FirstAdj = NULL;
  g->Vertices = NewVertices;
  g->n = n;
  /* Point the graph to the new set of vertices */
  
  return;
}

void GraphLinkedListInsertAdj(GraphLinkedList *g,
				    int VertexA,
				    int VertexB)
     /* Inserts an edge into the graph
      * Params: g - The graph to insert into
      *         VertexA - The initial vertex
      *         VertexB - The terminal vertex
      * Pre:    g - A linked list graph
      *         VertexA - a label of a vertex in the graph
      *         VertexB - a label of a vertex in the graph
      * Post:   The adjacency is inserted into the graph
      */
{
  AdjListNode *NewAdj; /* The new adjacency */

  NewAdj = (AdjListNode *)malloc(1 * sizeof(AdjListNode));
  /* Make the adjacency list node */

  NewAdj->Vertex = VertexB;
  NewAdj->NextAdj = g->Vertices[VertexA]->FirstAdj;
  g->Vertices[VertexA]->FirstAdj = NewAdj;
  /* Insert the adjacency into the graph */

  return;
}

int AreAdjacent(GraphLinkedList *g, int VertexA, int VertexB)
     /* Tests whether 2 vertices are adjacent in a graph
      * Params: g - The graph to test
      *         VertexA - The initial vertex
      *         VertexB - The terminal vertex
      * Pre:    g - A linked list graph
      *         VertexA - a label of a vertex in the graph
      *         VertexB - a label of a vertex in the graph
      * Post:   1 is returned if there is an edge from VertexA
      *         to VertexB
      *         0 is returned otherwise
      */
{
  AdjListNode *Current; /* To traverse VertexA's adjacency list */
  Current = g->Vertices[VertexA]->FirstAdj;
  while(Current != NULL && Current->Vertex != VertexB)
    Current = Current->NextAdj;
  if(Current == NULL)
    return 0; /* The 2 vertices are not adjacent */
  else
    return 1; /* The 2 vertices are adjacent */

  return NULL;
}
