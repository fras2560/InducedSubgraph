/* Title: GContainsHCMD.c
 * Date: July 26, 2011
 * Author: Daniel Steeves
 * ID: 090565910
 * Email: stee5910@mylaurier.ca
 * Input: Path to graph G (on command line)
 *        Path to graph H (on command line)
 * Output: Text telling the user whether or not G contains H.
 *         Error messages are also displayed based on the return
 *         value from the call to GContainsH.
 * Method: Read in the paths to graph files representing
 *         graphs G and H, and then pass them along with
 *         pointers to the number of vertices of H and the
 *         linked list of isomorphisms between H and induced 
 *         subgraphs of G. Display error messages if any, then
 *         if there are no errors, display whether or not G
 *         contains H. Finally, if G contains H, show how many
 *         induced subgraphs of G are isomorphic to H and show a
 *         vertex map of each isomorphism between H and a
 *         subgraph of G.
 */

#include <stdio.h>
#include "Utilities.h"

#define USAGE "-GContainsHCMD: usage: GContainsHCMD GGraphText HGraphText"

int main(int argc, char *argv[])
     /* Main method
      */
{  
  char *GGraphText; /* Path of G file */
  char *HGraphText; /* Path of H file */

  int GContainsHVal; /* Return value from call to GContainsH */

  BijectionLL *HToXIsomorphisms;
  int NHToXIsomorphisms; /* Number of bijections */
  BijectionLLNode *IsomorphismNode;
  Bijection HToXIsomorphism;
  /* Contains isomorphisms between H and induced subgraphs
   * of G (whose vertex sets are labeled the way they
   * are in G
   */

  int i; /* Counter */
  int p; /* Number of vertices in H */

  if(argc != 3)
    /* Need to have the program name and the 2 paths */
  {
    printf(USAGE);
    printf("\n");

    return 1; /* Incorrect number of arguments */
  }

  /* There are strings given for the paths to the graphs */
  GGraphText = argv[1];
  HGraphText = argv[2];

  printf("\n");
  printf("Computing...");

  GContainsHVal = GContainsH(GGraphText,
			     HGraphText,
			     &p,
			     &HToXIsomorphisms);
  
  printf("done.\n");
  printf("\n");

  switch(GContainsHVal)
  {
  case 0:
    /* No error in GContainsH */

    NHToXIsomorphisms = HToXIsomorphisms->NBijections;
    if(NHToXIsomorphisms > 0)
    {
      printf("=== G contains H. ===\n");
      printf("Number of isomorphisms between H and induced\n");
      printf("subgraphs of G: %d\n", NHToXIsomorphisms);
      printf("They are mapped out below:\n");
      
      printf("\n");
      printf("------------------------------\n");
      
      IsomorphismNode = HToXIsomorphisms->FirstBLLNode;
      while(IsomorphismNode != NULL)
	/* Show all the isomorphisms */
      {
	HToXIsomorphism = IsomorphismNode->B;
	for(i = 0;i < p;i++)
	  printf("V(H)[%d] <-> V(G)[%d]\n", i, HToXIsomorphism[i]);

	printf("------------------------------\n");
	
	IsomorphismNode = IsomorphismNode->NextBLLNode;
      }
    }else
    {
      printf("=== G does not contain H. ===\n");
      printf("This means that there are no induced subgraphs\n");
      printf("of G that are isomorphic to H.\n");
    }

    break;
  case 1:
    printf("The G (containing graph) file doesn't exist.\n");
    break;
  case 2:
    printf("The H (contained graph) file doesn't exist.\n");
    break;
  case 3:
    printf("H (the contained graph) has more vertices than G\n");
    printf("(the containing graph).\n");
    break;
  default:
    printf("Unspecified return value from function 'GContainsH'.\n");
    break;
  }

  printf("\n");
  printf("Done.\n");
  printf("\n");
  
  return 0;
}
