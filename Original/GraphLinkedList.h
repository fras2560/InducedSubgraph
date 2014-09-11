/*
 * GraphLinkedList.h
 */

typedef struct AdjListNode
{
  int Vertex; /* Label of adjacent vertex */
  struct AdjListNode *NextAdj; /* Pointer to next adjacent vertex */
}AdjListNode; /* Describes an adjacency */

typedef struct
{
  AdjListNode *FirstAdj; /* The "first" adjacency
			  * Order in the linked list
			  * doesn't matter
			  */
}AdjList; /* Describes adjacencies */

typedef struct
{
  AdjList **Vertices; /* Array of adjacency lists */
  int n; /* Number of vertices */
}GraphLinkedList; /* The actual graph structure */

extern GraphLinkedList *GraphLinkedListCreate();
extern void GraphLinkedListInsertVertex(GraphLinkedList *g);
extern void GraphLinkedListInsertAdj(GraphLinkedList *g,
				     int VertexA,
				     int VertexB);
extern int AreAdjacent(GraphLinkedList *g, int VertexA, int VertexB);
