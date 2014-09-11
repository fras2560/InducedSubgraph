/* Title: IndexCombinations.c
 * Date: June 10, 2011
 * Author: Daniel Steeves
 * ID: 090565910
 * Email: stee5910@mylaurier.ca
 * Input: Size of the entire set (n), and the size of the
 *        combinations to generate (k)
 * Output: All index combinations of size k of a set of size n
 * Method: The first/lowest index combination is generated,
 *         then an order of increasing weight in the
 *         combination is followed all the way up to the maximum weight.
 *         The combinations are always in increasing value from lowest
 *         to highest element
 */

#include <stdio.h>

int PrintAllCombs(int n, int k)
     /* Prints all k-combinations of an index
      * set of size n
      * Params: n - the size of the index set
      *         k - the size of the combinations to choose
      * Pre:    n - an integer
      *         k - an integer
      * Post:   0 is returned if there are no problems
      *         1 is returned if n is negative
      *         2 is returned if k is negative
      *         3 is returned if there isn't enough memory to make
      *           the combination structure
      */
{
  int *comb;

  if(n < 0)
    return 1;
  if(k < 0)
    return 2;

  if(makeComb(&comb, k) == 2)
    return 3;

  if(k > n)
    /* For k > n, the cardinality of the combination is
     * defined to be 0.
     */
  {
    printComb(comb, 0);
    printf("\n");
    return 0;
  }
  firstIndexComb(comb, k);
  printComb(comb, k);
  printf("\n"); /* Print the first combination */

  while(nextIndexComb(comb, n, k) == 1)
    /* Print the remaining combinations */
  {
    printComb(comb, k);
    printf("\n");
  }

  return 0;
}

int makeComb(int **comb, int k)
     /* Creates an array of integers to hold a combination
      * Params: k: Size of the combination
      * Pre:    k: An integer
      * Post:   comb points to the new combination if no problems
      *         comb remains unchanged if there is a problem
      *         0 is returned if there are no problems
      *         1 is returned if k is negative
      *         2 is returned if there isn't enough memory for the
      *           new combination
      */
{
  int *newComb;
  if(k < 0)
    return 1;
  newComb = (int *)malloc(k * sizeof(int));
  if(newComb == NULL)
    /* No memory */
    return 2;
  *comb = newComb;

  return 0;
}

int firstIndexComb(int *comb, int k)
     /* Sets the index combination to be the first/lowest one
      * of size k
      * Params: comb: The combination
      *         k: size of the combination
      * Pre:    comb: An array of integers
      *         k: a nonnegative integer
      * Post:   If no problems, the combination is filled
      *           with the starting subset of elements
      *         0 is returned if there are no problems
      *         1 is returned if k is negative
      */
{
  int i;

  if(k < 0)
    return 1;
  for(i = 0;i < k;i++)
    comb[i] = i; /* Fill with indices */

  return 0;
}

int nextIndexComb(int *curComb, int n, int k)
     /* Converts curComb into the combination that follows it
      * The first combination is {1, 2, ..., k}
      * Params: n: The size of the set
      *         k: The size of the combinations to generate
      * Pre:    n: A nonnegative integer
      *         k: A nonnegative integer

      * Post:   0 is returned if the highest combination reached
      *         1 is returned if the highest combination not reached yet
      *         2 is returned if n is negative
      *         3 is returned if k is negative
      *         4 is returned if k > n
      */
{
  int i;
  if(n < 0)
    return 2;
  if(k < 0)
    return 3;
  if(k > n)
    return 4;
  i = k - 1; /* Start at last/right element of the combination */
  curComb[i]++; /* Increment the last element */

  while((i > 0) && (curComb[i] > n - k + i))
    /* Stop after handling first element, or when element i
     * is below the maximum value that it can be
     */
  {
    i--;
    curComb[i]++; /* Move left in the combination
		   * checking for the maximum values of each element
		   * Also, increment each element that's checked
		   */
  }

  if(curComb[0] > n - k + 0)
    /* Highest combination {n-k, n-k+1, ..., n} reached */
    return 0; /* Return with value indicating
	       * highest combination reached
	       */

  for(i = i + 1; i < k;i++)
    /* Comb looks like {..., x, n - k + 1 + i, ..., n - k + 1 + i}
     * Change it to {..., x, x + 1, x + 2, ...}
     * This minimizes the portion of the combination that was
     * maximal
     */
    curComb[i] = curComb[i - 1] + 1;

  return 1; /* Return with value indicating a subset
	     * was generated
	     */
}

int printComb(int *comb, int k)
     /* Prints a combination
      * Params: comb: combination to print
      *         k: size of the combination
      * Pre:    comb: array of integers
      *         k: a positive integer
      * Post:   If there are no problems, the combination is printed
      *         0 is returned if there are no problems
      *         1 is returned if k is negative
      */
{
  int i;
  if(k < 0)
    return 1;
  printf("{");
  for(i = 0;i < k - 1;i++)
    printf("%d, ", comb[i]); /* Print current element
			      * (with more to follow)
			      */
  if(i < k)
    printf("%d", comb[i]); /* Print last element */
  printf("}");

  return 0;
}
