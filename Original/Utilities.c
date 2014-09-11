/*
 * Utilities.c
 */

#include <stdio.h>
#include "Utilities.h"

int CountSetBits(unsigned int n)
     /* Counts the number of set bits in a number
      * Params: n - number to count in
      * Pre:    n - an integer
      * Post:   The number of set bits is returned
      */
{
  int c; /* The count of the set bits */
  c = 0;
  for(;n > 0;c++)
    n &= n - 1; /* Clear the least significant bit set */

  return c;
}

char *StrAppend(char *s1, char *s2)
     /* Creates a new string consisting of a copy of
      * the second string appended to a copy of the first.
      * Parameters: s1 is the first string
      *             s2 is the second string
      * Preconditions: s1 and s2 are strings
      * Postconditions: A pointer to the new string is returned
      */
{
  return strcat(strcpy((char *)malloc((strlen(s1) + strlen(s2) + 1)
				      * sizeof(char)), s1), s2);
  //Allocate memory for new string
  //Copy first string in
  //Concatenate first and second
}

BijectionLL *BijectionLLCreate()
     /* Creates a new, empty bijection linked list
      * Params: None
      * Pre:    None
      * Post:   The empty bijection linked list is returned
      */
{
  BijectionLL *BLL;
  BLL = (BijectionLL *)malloc(sizeof(BijectionLL));
  /* Create the linked list of bijections */

  BLL->FirstBLLNode = NULL;
  BLL->NBijections = 0;
  /* No bijections to start */
  return BLL;
}

void BijectionLLInsertBijection(BijectionLL *BLL,
				Bijection B)
     /* Copies a bijection (the pointer to the start of
      * an array of integers) into the list. The integers themselves
      * are not copied, only the pointer is copied.
      * Params: BLL - The list to insert into
      *         B - The bijection to insert
      * Pre:    BLL - An existing bijection linked list
      *         B - A bijection
      * Post:   A bijection linked list node is created and
      *         assigned the passed bijection, and then the node
      *         is inserted into the end of the list.
      *         This way, the order of insertion is preserved.
      */
{
  BijectionLLNode *BLLNodeNew;
  /* The node to insert */
  BijectionLLNode *BLLNodePrevious;
  /* The previous node in the list traversal */
  BijectionLLNode *BLLNodeCurrent;
  /* The current node in the list traversal */

  BLLNodeNew = (BijectionLLNode *)malloc(1 * sizeof(BijectionLLNode));
  /* Make the new bijection linked list node */

  BLLNodeNew->B = B; /* Copy the array pointer into the list */
  BLLNodeNew->NextBLLNode = NULL; /* Last node in the list */

  BLLNodePrevious = NULL;
  BLLNodeCurrent = BLL->FirstBLLNode;
  while(BLLNodeCurrent != NULL)
    /* Insert new bijection nodes at the end of the list */
  {
    BLLNodePrevious = BLLNodeCurrent;
    BLLNodeCurrent = BLLNodeCurrent->NextBLLNode;
    /* Move to the next node */
  }
  if(BLLNodePrevious == NULL)
    /* The list is empty, point the lists 'front'
     * pointer to the new node
     */
    BLL->FirstBLLNode = BLLNodeNew;
  else
    /* The list is not empty, point the last node's
     * 'next' pointer to the new node
     */
    BLLNodePrevious->NextBLLNode = BLLNodeNew;

  BLL->NBijections++; /* Show that there's another bijection */

  return;
}
