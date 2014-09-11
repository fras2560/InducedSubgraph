all: GContainsHUI GContainsHCMD

clean:
	rm GContainsHUI GContainsHCMD

GContainsHUI: nauty.h nauty.c nautil.c naugraph.c Utilities.h Utilities.c GraphLinkedList.h GraphLinkedList.c GraphTextToLinkedList.h GraphTextToLinkedList.c GraphLinkedListTonauty.h GraphLinkedListTonauty.c IndexCombinations.h IndexCombinations.c InduceSubgraph.h InduceSubgraph.c Isomorphism.h Isomorphism.c GContainsH.h GContainsH.c GContainsHUI.c
	gcc -g nauty.c nautil.c naugraph.c Utilities.c GraphLinkedList.c GraphTextToLinkedList.c GraphLinkedListTonauty.c IndexCombinations.c InduceSubgraph.c Isomorphism.c GContainsH.c GContainsHUI.c -o GContainsHUI

GContainsHCMD: nauty.h nauty.c nautil.c naugraph.c Utilities.h Utilities.c GraphLinkedList.h GraphLinkedList.c GraphTextToLinkedList.h GraphTextToLinkedList.c GraphLinkedListTonauty.h GraphLinkedListTonauty.c IndexCombinations.h IndexCombinations.c InduceSubgraph.h InduceSubgraph.c Isomorphism.h Isomorphism.c GContainsH.h GContainsH.c GContainsHCMD.c
	gcc -g nauty.c nautil.c naugraph.c Utilities.c GraphLinkedList.c GraphTextToLinkedList.c GraphLinkedListTonauty.c IndexCombinations.c InduceSubgraph.c Isomorphism.c GContainsH.c GContainsHCMD.c -o GContainsHCMD