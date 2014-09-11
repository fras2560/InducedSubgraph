/*
 * Utilities.h
 */

typedef int *Bijection;
/* A bijection is defined here as a unique index relating to
 * a (supposedly) unique value that may or may not be an index
 */

typedef struct BijectionLLNode
{
  Bijection B;
  struct BijectionLLNode *NextBLLNode;
}BijectionLLNode;

typedef struct
{
  BijectionLLNode *FirstBLLNode;
  int NBijections;
}BijectionLL;

extern int CountSetBits(unsigned int n);
extern char *StrAppend(char *s1, char *s2);
extern BijectionLL *BijectionLLCreate();
extern void BijectionLLInsertBijection(BijectionLL *BLL,
				       Bijection B);
