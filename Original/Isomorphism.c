/* Title: Isomorphism.c
 * Date: June 17, 2011
 * Author: Daniel Steeves
 * ID: 090565910
 * Email: stee5910@mylaurier.ca
 * Input: 2 graphs in setword format
 * Output: A bijection describing isomorphism between the 2 graphs
 *         if they're isomorphic, or NULL if they're not
 * Method: Use nauty to determine the canonical form of each
 *         of the graphs, then determine if the canonical forms
 *         are equal. Use the canonical order of each graph
 *         to determine the bijection between the vertices
 */

#include "nauty.h"
#include "Utilities.h"

int GraphsEqual(graph *g0,
		graph *g1,
		int m,
		int n)
     /* Determines whether 2 graphs are equal or not
      * Params: g0 - the first graph
      *         g1 - the second graph
      *         m - the number of setwords per set
      *         n - the number of sets/vertices in the graph
      * Pre:    g0, g1 - graphs
      *         m, n - positive integers
      * Post:   1 is returned if the graphs are equal,
      *           0 otherwise
      */
{
  int i;
  for(i = 0;i < m * n;i++)
    if(g0[i] != g1[i])
      /* Compare each setword */
      return FALSE;
  return TRUE; /* Made it without any inequalities */
}

Bijection GetIsomorphism(graph *g0,
		    graph *g1,
		    int m,
		    int n)
     /* Determines whether two graphs are isomorphic to
      * one another or not, and returns the isomorphism
      * if they are
      * Params: g0 - the first graph
      *         g1 - the second graph
      *         m - the number of setwords per set
      *         n - the number of sets/vertices
      * Pre:    The graphs must have the same m and n values
      *         g0, g1 - graphs
      *         m, n - positive integers
      * Post:   The isomorphism bijection is returned if it exists in the
      *         form of an array such that Isorphism[a] = b means
      *         vertex 'b' in g1 is the image of vertex 'a'
      *         in g0 under the isomorphism bijection. If no
      *         isomorphism exists, NULL is returned
      */
{
  int i;
  Bijection Isomorphism; /* The isomorphism bijection */
  int *lab0, *lab1; /* The resulting canonical order of the
		     * vertices of each of the graphs
		     */
  int *ptn0, *ptn1;
  int *orbits0, *orbits1;
  DEFAULTOPTIONS_GRAPH(TheOptions);
  statsblk stats0, stats1;
  setword *TheWorkspace;
  setword TheWorksize;
  graph *canong0, *canong1; /* After the calls to 'nauty', these are the
			     * graphs in their canonically labelled forms
			     */

  lab0 = (int *)malloc(n * sizeof(int));
  lab1 = (int *)malloc(n * sizeof(int));
  ptn0 = (int *)malloc(n * sizeof(int));
  ptn1 = (int *)malloc(n * sizeof(int));
  orbits0 = (int *)malloc(n * sizeof(int));
  orbits1 = (int *)malloc(n * sizeof(int)); 
  /* Allocate memory for these arrays */

  TheOptions.getcanon = TRUE; /* Specify to get the canonical forms */
  TheOptions.defaultptn = TRUE; /* Don't care about colouring */
  TheWorksize = 50;
  TheWorkspace = (setword *)malloc(TheWorksize * m * sizeof(setword));
  canong0 = (setword *)malloc(n * sizeof(setword));
  canong1 = (setword *)malloc(n * sizeof(setword));
  /* Allocate memory for the canonical forms of the graphs */

  nauty(g0,
	lab0,
	ptn0,
	NULL,
	orbits0,
	&TheOptions,
	&stats0,
	TheWorkspace,
	TheWorksize,
	m, n,
	canong0);
  /* Determine the canonical graph and order of g0 */

  nauty(g1,
	lab1,
	ptn1,
	NULL,
	orbits1,
	&TheOptions,
	&stats1,
	TheWorkspace,
	TheWorksize,
	m, n,
	canong1);
  /* Determine the canonical graph and order of g1 */

  if(!GraphsEqual(canong0, canong1, m, n))
    /* graph0 and graph1 are isomorphic iff
     * their canonical forms are equal
     */
    return NULL;
  
  Isomorphism = (Bijection)malloc(n * sizeof(int));
  for(i = 0;i < n;i++)
    /* Populate the bijection map */

    Isomorphism[lab0[i]] = lab1[i];
    /* Insert the ith vertices of the canonization
     * from each of the graphs into the bijection map
     */

  return Isomorphism;
}
