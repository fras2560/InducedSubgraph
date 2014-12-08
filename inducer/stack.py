"""
-------------------------------------------------------
stack
a stack class
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-17
-------------------------------------------------------
"""
import copy
class DStack():
    '''
    DStack
        a simple stack class
    '''
    def __init__(self):
        self.data = []
        self.size = 0

    def __len__(self):
        '''
        override the len function
        '''
        return self.size

    def push(self, element):
        '''
        pushes an element onto the stack
        Parameters:
            element: the object to push on
        Returns:
            None
        '''
        self.size += 1
        self.data.append(element)

    def pop(self):
        '''
        pops an element off the stack
        Parameters:
            None:
        Returns:
            element: None if no elements
        '''
        if self.size >=1:
            element = self.data.pop()
            self.size -= 1
        else:
            element = None
        return element

    def copy(self):
        '''
        copies the stack
        Parameters:
            None
        Returns:
            s: a copied stack (DStack)
        '''
        s = DStack()
        for element in self.data:
            s.push(copy.deepcopy(element))
        return s

    def push_set(self, object_set):
        '''
        pushes the whole list of objects
        Parameters:
            object_set: the list of objects
        Returns:
            None
        '''
        for element in object_set:
            self.push(element)
        return

    def peak(self):
        '''
        peaks at the top object on the stack
        Parameters:
            None
        Returns:
            : the top object on the stack
        '''
        return self.data[self.size - 1]

import unittest
class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = DStack()

    def tearDown(self):
        pass

    def testPush(self):
        self.stack.push(1)
        self.assertEqual(len(self.stack.data), 1)
        self.assertEqual(self.stack.size, 1)
        self.assertEqual(self.stack.data[0], 1)

    def testPop(self):
        elements = [1, 2]
        for element in elements:
            self.stack.push(element)
        size = len(elements)
        current = self.stack.pop()
        while current is not None:
            size -= 1
            self.assertEqual(len(self.stack), size)
            self.assertEqual(current, elements[size])
            current = self.stack.pop()

    def testPushSet(self):
        elements = [1, 2]
        self.stack.push_set(elements)
        elements.pop()
        self.assertNotEqual(self.stack.data, elements)
        self.assertEqual(self.stack.data, [1, 2])

    def testCopy(self):
        elements = [1, 2]
        for element in elements:
            self.stack.push(element)
        s2 = self.stack.copy()
        s2.pop()
        self.assertNotEqual(self.stack.data, s2.data)
        self.assertEqual(self.stack.data, elements)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()