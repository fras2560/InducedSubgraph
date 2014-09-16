"""
-------------------------------------------------------
bijectionlist
data structure for bijections
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-16
-------------------------------------------------------
"""
class BijectionList():
    def __init__(self):
        self.number = 0
        self.node = None

    def insert(self, node):
        previous = None
        pointer = self.node
        while pointer is not None:
            previous = pointer
            pointer = pointer.node
        if previous is None:
            self.node = node
        else:
            previous.node = node
        self.number += 1