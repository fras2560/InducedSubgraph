/* Title: GContainsH.c
 * Date: July 13, 2011
 * Author: Daniel Steeves
 * ID: 090565910
 * Email: stee5910@mylaurier.ca
 * Input: Path to Graph G (as argument)
 *        Path to Graph H (as argument)
 * Output: An error code is returned.
 *         The number of vertices in H is relayed
 *         through the pointer pPtr.
 *         The isomorphisms between H and induced subgraphs of G
 *         are inserted into a bijection linked list pointed to
 *         by HToXIsomorphisms.
 * Method: Convert the text based adjacency list graphs to
 *         linked list graphs.
 *         Convert the linked list graphs to nauty graphs.
 *         Generate all induced subgraphs of G with the same
 *         number of vertices as H. Attempt to get an isomorphism
 *         between H and each of the induced subgraphs of G.
 *         If such an isomorphism exists, the vertices in the
 *         induced subgraph of G are relabeled back to what
 *         they were labeled in G and the isomorphism is inserted
 *         into the list of isomorphisms.
 */

#include "Utilities.h"
#include "nauty.h"
#include "GraphLinkedList.h"
#include "GraphTextToLinkedList.h"
#include "GraphLinkedListTonauty.h"
#include "IndexCombinations.h"
#include "InduceSubgraph.h"
#include "Isomorphism.h"
#include "GContainsH.h"

int GContainsH(char *GGraphText,
	       char *HGraphText,
	       int *pPtr,
	       BijectionLL **HToXIsomorphisms)
     /* Determines how many induced subgraphs of G are isomorphic to
      * H, and maps out all of these isomorphisms.
      * Params: GGraphText - Path to the G graph adjacency list file
      *         HGraphText - Path to the H graph adjacency list file
      *         pPtr - Points to a location to store the number
      *           of vertices in the H graph
      *         HToXIsomorphisms - Points to a list of Isomorphisms
      *           between H and induced subgraphs (X graphs) of G
      * Pre:    GGraphText - A string
      *         HGraphText - A string
      *         pPtr - A pointer to an integer
      *         HToXIsomorphisms - A double indirect pointer to a
      *           bijection linked list structure
      * Post:   Return value:
      *           0 - No errors
      *           1 - The G text graph doesn't exist
      *           2 - The H text graph doesn't exist
      *           3 - H has a greater number of vertices than G
      *           The integer pointed to by pPtr is set to the number
      *             of vertices in H if there are no errors
      *           The bijection linked list pointed to by
      *             HToXIsomorphisms is populated if there are
      *             no errors
      */
{
  GraphLinkedList *GGraphLinked; /* G (linked list) */
  GraphLinkedList *HGraphLinked; /* H (linked list) */

  graph *GGraphnauty; /* G (nauty graph) */
  graph *HGraphnauty; /* H (nauty graph) */
  graph *XGraphnauty; /* The subgraph induced by the
		       * vertex subsets of G
		       */
  int m; /* The G nauty graph has m setwords per set/vertex */
  int n; /* G has n vertices */
  int o;
  /* The H nauty graph has o setwords per set/vertex */
  /* The X nauty graph has o setwords per set/vertex */

  int *x;
  /* Subset x (array of vertices) of the vertices of G */

  int p;
  /* H has p vertices */
  /* x has p vertices */
  /* X has p vertices */

  Bijection HToXIsomorphism;
  /* Isomorphism between an induced subgraph of G and H
   * The labels of the vertices of G get changed from
   * their default values in the X subgraph back to
   * what they are in G
   */

  int i; /* Counter */

  *HToXIsomorphisms = BijectionLLCreate();
  /* Lists all the bijections of isomorphisms between
   * subgraphs of G and H
   */

  GGraphLinked = GraphTextToLinkedList(GGraphText);
  HGraphLinked = GraphTextToLinkedList(HGraphText);
  /* Convert from text to linked list */

  if(GGraphLinked == NULL)
    /* G text graph doesn't exist */
    return 1;
  if(HGraphLinked == NULL)
    /* H text graph doesn't exist */
    return 2;

  n = GGraphLinked->n;
  *pPtr = p = HGraphLinked->n; /* Get the cardinality of the vertex sets */

  if(p > n)
    /* If H has more vertices than G */
    return 3;

  GGraphnauty = GraphLinkedListTonauty(GGraphLinked);
  HGraphnauty = GraphLinkedListTonauty(HGraphLinked);
  /* Convert from linked list to nauty 'graph' */

  m = n / WORDSIZE;
  if(n % WORDSIZE > 0)
    /* If the division wasn't even */
    m++; /* Round up */
  o = p / WORDSIZE;
  if(p % WORDSIZE > 0)
    /* If the division wasn't even */
    o++; /* Round up */

  makeComb(&x, p); /* Prepare the combination (vertex subset) */
  firstIndexComb(x, p); /* Populate the combination with the
			 * lowest vertex labels
			 */

  do
  {
    XGraphnauty = InduceSubgraph(GGraphnauty,
				 x,
				 m,
				 n,
				 p);
    /* Induce the X subgraph based on the vertex subset x */

    HToXIsomorphism = GetIsomorphism(HGraphnauty, XGraphnauty, o, p);
    /* Attempt to get an isomorphism bijection between X and H */

    if(HToXIsomorphism != NULL)
      /* If H and X are isomorphic */
    {
      for(i = 0;i < p;i++)
	HToXIsomorphism[i] = x[HToXIsomorphism[i]];
	/* Translate the newly labeled vertex in the
	 * subgraph back into what it is labeled as in G
	 */
      BijectionLLInsertBijection(*HToXIsomorphisms,
				 HToXIsomorphism);
    }

  }while(nextIndexComb(x, n, p) != 0);
  /* Keep checking all possible subgraphs induced by subsets
   * of size p of vertices of G for isomorphism to H until
   * all subgraphs have been tested
   */

  return 0;
}
