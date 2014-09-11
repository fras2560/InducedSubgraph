/* Title: GraphTextToLinkedList.c
 * Date: June 28, 2011
 * Author: Daniel Steeves
 * ID: 090565910
 * Email: stee5910@mylaurier.ca
 * Input: A file containing adjacency lists of a graph.
 *        The file must have the correct format:
 *          Vertex labels are the very first thing on each line,
 *            although their value doesn't actually matter,
 *            the vertices are labelled 0-(n-1) when they are
 *            processed into the linked list adjacency structure.
 *          There must be a colon separating the (possibly empty)
 *            vertex labels and the adjacency lists. There are no
 *            spaces surrounding this colon.
 *          The adjacencies are separated by spaces.
 *          The lines in the file are separated by newline
 *            characters. There must not be a newline at
 *            the end of the file.
 * Output: A linked list graph structure is generated based on
 *         the data in the file.
 * Method: A new linked list graph is created.
 *         A vertex is inserted for each line in the file,
 *         and adjacencies are inserted for each label after
 *         the colon on each line.
 */

#include "nauty.h"
#include "GraphLinkedList.h"
#include "Utilities.h"

GraphLinkedList *GraphTextToLinkedList(char *GraphTextFilename)
     /* Reads in a file containing the adjacency lists
      * of a graph, and creates an adjacency list (linked list)
      * graph structure
      * Params: GraphTextFilename - Filename of file to read
      * Pre:    GraphTextFilename - String, the name of an existing
      *                             file containing valid adjacency
      *                             list data
      * Post:   The adjacency list (linked list) graph structure
      *         representing the data in the file is returned
      */
{

  FILE *GraphTextFile; /* File stream to read in the graph */
  GraphLinkedList *g; /* The retrieved graph */
  char C; /* Process one char at a time */
  char CString[2]; /* To contain C and a NULL-terminator */
  int Vertex; /* Label of current vertex */
  char *Adj; /* Current vertex or adjacency */
  int OnAdj; /* Specifies whether an adjacency list is currently
	      * being traversed */

  CString[1] = NULL; /* This will stay as NULL the whole time */

  GraphTextFile = fopen(GraphTextFilename, "r");
  /* Open a stream of the graph file */

  if(GraphTextFile == NULL)
    /* If the file doesn't exist */
    return NULL; /* Can't continue */

  g = GraphLinkedListCreate();
  /* The resulting linked list graph */

  Vertex = 0; /* First vertex */
  C = fgetc(GraphTextFile);
  /* Get the first char */
  if(C != EOF)
  {
    OnAdj = FALSE;
    Adj = (char *)malloc(1 * sizeof(char));
    Adj[0] = NULL;
    GraphLinkedListInsertVertex(g);
    /* Add the first vertex to the graph */
    while(TRUE)
      /* Iterate through the entire graph text file */
    {
      if(!OnAdj)
	/* Working with vertices, gotta skip past the vertex
	 * label and the colon
	 */
      {
	while(fgetc(GraphTextFile) != ':');
	OnAdj = TRUE;
      }else
	/* Working with adjacencies */
      {
	if(C == ' ')
	  /* Done with an adjacency, more to follow for this vertex
	   * A space only follows an adjacency
	   */
	{
	  GraphLinkedListInsertAdj(g, Vertex, atoi(Adj));
	  free((void *)Adj);
	  Adj = (char *)malloc(1 * sizeof(char));
	  Adj[0] = NULL;
	  /* Clear the adjacency string */
	}else if(C == '\n')
	  /* Done with an adjacency, no more to follow for this vertex */
	{
	  if(Adj[0] != NULL)
	    /* If an adjacency is specified for this vertex */
	  {
	    GraphLinkedListInsertAdj(g, Vertex, atoi(Adj));
	    free((void *)Adj);
	    Adj = (char *)malloc(1 * sizeof(char));
	    Adj[0] = NULL;
	    /* Clear the adjacency string */
	  }
	  Vertex++;
	  GraphLinkedListInsertVertex(g);
	  /* Move to the next vertex */
	  OnAdj = FALSE; /* No longer traversing adjacencies */
	}else if(C == EOF)
	  /* Insert the last adjacency if one is specified,
	   * then done with the graph text file
	   */
	{
	  if(Adj[0] != NULL)
	    /* If an adjacency is specified for this vertex */
	  {
	    GraphLinkedListInsertAdj(g, Vertex, atoi(Adj));
	    free((void *)Adj);
	    Adj = (char *)malloc(1 * sizeof(char));
	    Adj[0] = NULL;
	    /* Clear the adjacency string */
	  }
	  OnAdj = FALSE;
	  break;
	}else
	  /* Getting the label of an adjacent vertex */
	{
	  CString[0] = C;
	  Adj = StrAppend(Adj, CString);
	  /* Add a char to the label */
	}
      }
	
      C = fgetc(GraphTextFile);
      /* Get the next char */
    }
  }
  fclose(GraphTextFile);

  return g;
}
