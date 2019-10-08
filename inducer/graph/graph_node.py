'''
@author: Dallas Fraser
@id: 20652186
@class: CS686
@date: 2016-04-02
@note: contains a function to create the networkx graphs
'''
import logging


class GraphNode():
    index = 0
    count = 0

    def __init__(self, color=None, index=None, logger=None):
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.color = color
        if index is None:
            index = GraphNode.index
            GraphNode.index += 1
        GraphNode.count += 1
        self.index = index

    def __eq__(self, node):
        equal = False
        try:
            if self.index == node.index:
                equal = True
        except Exception:
            pass
        return equal

    def __copy__(self):
        return GraphNode(color=self.color,
                         index=self.index,
                         logger=self.logger)

    def __le__(self, node):
        equal = False
        try:
            if self.index <= node.index:
                equal = True
        except Exception:
            pass
        return equal

    def __lt__(self, node):
        equal = False
        try:
            if self.index < node.index:
                equal = True
        except Exception:
            pass
        return equal

    def __hash__(self):
        return hash(self.index)
