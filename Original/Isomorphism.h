/*
 * Isomorphism.h
 */

extern int GraphsEqual(graph *g0,
                graph *g1,
                int m,
                int n);
extern int *GetIsomorphism(graph *g0,
                    graph *g1,
                    int m,
                    int n);
