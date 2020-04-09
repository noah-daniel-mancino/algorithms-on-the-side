'''
Author: Noah Mancino
Date: 03/6/2020
Description: An implementation of a Red-Black tree.
'''
from mealticket import *

class RBNode(object):
    '''
    Description: This is the node class for the Red-Black Tree.
    '''

    def __init__(self, ticket, color='red'):
        '''
        Constructor for the RBNode class
        '''
        self.key = ticket.ticketID
        self.value = ticket
        self.color = color

        # Build sentinal nodes and set the initial parent
        self.parent = None
        self.leftChild = Sentinal()
        self.rightChild = Sentinal()

    def __str__(self):
        ''' 
        Returns a string rep of the node
        '''
        returnValue = 'Node: {} - Color: {}\n'.format(self.key, self.color)
        returnValue += 'Parent: {}\n'.format(self.parent.key)
        returnValue += 'Left Child: {}\n'.format(self.leftChild.key)
        returnValue += 'Right Child: {}\n'.format(self.rightChild.key)
        return returnValue

    def isSentinal(self):
        '''
        makes it easy to check if a node is a sentinal
        '''
        return False

    def hasLeftChild(self):
        ''' 
        This method returns true if the current node has a left child 
        '''
        returnValue = False
        if(self.leftChild.parent == self and self.leftChild != self):
            if(not self.leftChild.isSentinal()):
                returnValue = True
        return returnValue

    def hasRightChild(self):
        ''' 
        This method returns true|false depending on if the current
        node has a right child or not.
        '''
        returnValue = False
        if(self.rightChild.parent == self and self.rightChild != self):
            if(not self.rightChild.isSentinal()):
                returnValue = True
        return returnValue

    def hasOnlyOneChild(self):
        ''' 
        Returns True if the current node has only one child.
        '''
        LC = self.hasLeftChild()
        RC = self.hasRightChild()
        return (LC and not RC) or (not LC and RC)

    def hasBothChildren(self):
        ''' 
        Returns True if the current node has both children
        '''
        return self.hasLeftChild() and self.hasRightChild()

    def isLeaf(self):
        ''' 
        Returns true if the current node is a leaf node.
        '''
        returnValue = False
        if(self.rightChild.isSentinal() and self.leftChild.isSentinal()):
            returnValue = True
        return returnValue

    def isLeftChild(self):
        '''
        Returns true if the current node is a left child
        '''
        return self.parent.leftChild == self

    def isRightChild(self):
        '''
        Returns true if the current node is a right child
        '''
        return self.parent.rightChild == self

    def setRight(self, node):
        '''
        Sets a new right child
        '''
        self.rightChild = node
        if node and not node.isSentinal():
            node.parent = self

    def setLeft(self, node):
        '''
        Sets a new left child
        '''
        self.leftChild = node
        if node and not node.isSentinal():
            node.parent = self


class Sentinal(RBNode):
    '''
    This class builds the sentinal nodes and includes some nifty methods
    '''

    def __init__(self, color='black'):
        '''
        The constructor for the sentinal class
        '''
        self.key = None
        self.value = None
        self.leftChild = None
        self.rightChild = None
        self.parent = None
        self.color = 'black'

    def isSentinal(self):
        '''
        This method makes it easy to check if a given node is a sentinal
        '''
        return True


class RedBlackTree:
    ''' 
    Skeleton code for the red-black tree
    '''

    def __init__(self):
        '''
        The constructor for the red-black tree
        '''
        self._root = None
        self.size = 0
        self.output = ''

        # All leaf nodes point to self.sentinel, rather than 'None'
        # Parent of root should also be self.sentinel
        self.sentinel = Sentinal()
        self.sentinel.parent = self.sentinel
        self.sentinel.leftChild = self.sentinel
        self.sentinel.rightChild = self.sentinel

    def traverse(self, mode):
        '''
        The traverse method returns a string rep of the tree according to
        the specified mode
        '''
        self.output = ''
        if(isinstance(mode, str)) and self.size:
            if(mode == 'in-order'):
                self.inorder(self._root)
            elif(mode == 'pre-order'):
                self.preorder(self._root)
            elif(mode == 'post-order'):
                self.postorder(self._root)
        else:
            self.output = '  '
        return self.output[:-2]

    def inorder(self, node):
        '''
        Computes the preorder traversal 
        '''
        if(node.key is not None):
            self.inorder(node.leftChild)
            self.output += str(node.key) + ', '
            self.inorder(node.rightChild)

    def preorder(self, node):
        '''
        Computes the pre-order traversal
        '''
        if(node.key is not None):
            self.output += str(node.key) + ', '
            self.inorder(node.leftChild)
            self.inorder(node.rightChild)

    def postorder(self, node):
        '''
        Compute postorder traversal
        '''
        if(node.key is not None):
            self.inorder(node.leftChild)
            self.inorder(node.rightChild)
            self.output += str(node.key) + ', '

    def findSuccessor(self, node):
        '''
        This method returns the sucessor of a given node.
        '''
        successor = None
        # if node has a right child
        if node.hasRightChild():
            # then successor is the min of the right subtree
            currentNode = node.rightChild
            while currentNode.hasLeftChild():
                currentNode = currentNode.leftChild
            successor = currentNode
        elif node.parent:  # node has no right child, but has a parent
            if node.isLeftChild():  # node is a left child
                successor = node.parent  # then succ is the parent
            else:  # node is right child, and has not right child
                # remove parent's rightChild reference
                node.parent.rightChild = None
                # recursively find call findSuccessor on parent
                successor = self.findSuccessor(node.parent)
                # replace parent's rightChild reference
                node.parent.rightChild = node
        return successor

    def find(self, ticketID):
        '''
        Returns a mealticket with the specified ticketID if it exists, 
        otherwise returns false.
        '''
        meal = self.findNode(ticketID) if isinstance(ticketID, int) else False
        return meal.value if meal is not False else meal

    def delete(self, ticketID):
        ''' 
        If a node holding a ticket with the specified ticketID exists in the
        tree, it is deleted while the tree's property's are maintained.
        Returns True upon success and False upon failure.
        '''
        ticket = self.findNode(ticketID) if isinstance(
            ticketID, int) else False
        if ticket:
            self.size -= 1
            originalColor = ticket.color
            if ticket.isLeaf():
                x = self.sentinel 
                # Case: ticket is a leaf less than its parent
                if ticket.isLeftChild():
                    ticket.parent.leftChild = self.sentinel
                    self.sentinel.parent = ticket.parent
                # Case: ticket is a leaf greater than or equal to its parent
                elif ticket.isRightChild():
                    ticket.parent.rightChild = self.sentinel
                    self.sentinel.parent = ticket.parent
                # Case: ticket is the root
                else:
                    self._root = None

            elif ticket.hasOnlyOneChild():
                # Case: the node to be deleted only has a right child
                if ticket.leftChild.isSentinal():
                    ticket.value = ticket.rightChild.value
                    ticket.key = ticket.rightChild.key
                    ticket.color = ticket.rightChild.color
                    ticket.setLeft(ticket.rightChild.leftChild)
                    ticket.setRight(ticket.rightChild.leftChild)
                # Case: the node to be deleted only has a left child
                else:
                    ticket.value = ticket.leftChild.value
                    ticket.key = ticket.leftChild.key
                    ticket.color = ticket.leftChild.color
                    ticket.setRight(ticket.leftChild.rightChild)
                    ticket.setLeft(ticket.leftChild.leftChild)
                x = ticket
            else:
                replacement = self.findSuccessor(ticket)
                x = replacement.rightChild
                originalColor = replacement.color
                # Case: the node has two children, one is its successor
                if replacement.parent.key == ticket.key:
                    ticket.value = replacement.value
                    ticket.key = replacement.key
                    ticket.rightChild = x
                    replacement.parent = None
                    x.parent = ticket
                # Case: the node has two children, neither are its successor
                else:
                    ticket.value = replacement.value
                    ticket.key = replacement.key
                    replacement.parent.leftChild = x
                    x.parent = replacement.parent
                    replacement.parent = None
            
            if originalColor == 'black' and self._root is not None:
                self.deleteFixup(x)

        return ticket is not False

    def insert(self, ticket):
        '''
        Inserts a new node holding the given mealticket into the tree. Returns
        True upon success and False upon failure.
        '''
        currentNode = self._root
        inserted = RBNode(ticket)
        ticket.leftChild = self.sentinel
        ticket.rightChild = self.sentinel
        if not isinstance(ticket, MealTicket):
            print("This tree is only meant to handle mealTickets")
            return False
        # We travel down the tree according to the search property until
        # we reach a leaf, at which point we create a new node and add it
        # to whichever side the search property dictates.
        self.size += 1
        while currentNode is not None and not currentNode.isSentinal():
            # travel down the tree
            if currentNode.key > ticket.ticketID:
                newNode = currentNode.leftChild
                traveled = 'left'
            else:
                newNode = currentNode.rightChild
                traveled = 'right'
            # If the next node is the sentinal, we finished traversing and
            # it is time to append.
            if newNode.isSentinal():
                if traveled == 'right':
                    currentNode.setRight(inserted)
                elif traveled == 'left':
                    currentNode.setLeft(inserted)
            currentNode = newNode
        # If current node is none we just have to add a root, which is easy
        if currentNode is None:
            self._root = inserted
            inserted.parent = self.sentinel
        # This leaves us with a valid BST, but not always with valid RB-tree.
        # If the newly inserted node has a red parent, we have violated the
        # rule that red nodes must have red children.
        self.insertFixup(inserted)
        return True

    def _leftRotate(self, currentNode):
        ''' 
        Perform a left rotation from a given node
        '''
        # Assuming the currentnode's right child is not nill, we want to move
        # it 'above' currentnode in the tree while maintaining the search
        # property. 
        # I wish I could have thought of some better variable names,
        # but it was surprisingly difficult so I just went with the convention
        # they use in the CLR&S textbook. 
        y = currentNode.rightChild
        if y.isSentinal():
            return
        currentNode.rightChild = y.leftChild
        # If y has a left branch we need to move it to the right of currentNode
        if not y.leftChild.isSentinal():
            y.leftChild.parent = currentNode
        # The next line until the end of the else statement builds the
        # parent child association between y and current node's parent
        y.parent = currentNode.parent
        if currentNode.parent.isSentinal():
            self._root = y
            y.parent = self.sentinel
        elif currentNode.isLeftChild():
            currentNode.parent.leftChild = y
        else:
            currentNode.parent.rightChild = y
        # Now, we plant currentNode to the left of y.
        y.leftChild = currentNode
        currentNode.parent = y

    def _rightRotate(self, currentNode):
        ''' 
        Perform a right rotation from a given node
        '''
        # Assuming the currentnode's left child is not nill, we want to move
        # it 'above' currentnode in the tree while maintaining the search
        # property.
        y = currentNode.leftChild
        if y.isSentinal():
            return
        currentNode.leftChild = y.rightChild
        # If y has a right branch we need to move it to the left of currentNode.
        if not y.rightChild.isSentinal():
            y.rightChild.parent = currentNode
        # The next line until the end of the else statement builds the
        # parent child association between y and current node's parent.
        y.parent = currentNode.parent
        if currentNode.parent.isSentinal():
            self._root = y
        elif currentNode.isLeftChild():
            currentNode.parent.leftChild = y
        else:
            currentNode.parent.rightChild = y
        # Now, we plant currentNode to the right of y.
        y.rightChild = currentNode
        currentNode.parent = y

    def findNode(self, ticketID):
        '''
        Returns node specified by ticketID if it exists, and False otherwise.
        '''
        found = False
        currentNode = self._root
        # Go where the search property tells you to until you find a maching
        # node or a leaf.
        while currentNode is not None and not currentNode.isSentinal():
            if currentNode.key == ticketID:
                found = currentNode
                break
            if currentNode.key > ticketID:
                currentNode = currentNode.leftChild
            else:
                currentNode = currentNode.rightChild
        return found

    def insertFixup(self, currentNode):
        '''
        An internal method to maintain red-black properties after insertions
        are preformed
        '''
        while currentNode.parent is not None and currentNode.parent.color == 'red':
            if currentNode.parent.isLeftChild():
                # Case: currentNode has a red uncle.
                y = currentNode.parent.parent.rightChild
                if y.color == 'red':
                    currentNode.parent.color = 'black'
                    y.color = 'black'
                    currentNode.parent.parent.color = 'red'
                    currentNode = currentNode.parent.parent
                else:
                    if currentNode.isRightChild():
                # Case: currentNode has a black uncle and currentNode is a 
                # right child.
                        currentNode = currentNode.parent
                        self._leftRotate(currentNode)
                # Case: currentNode has a black uncle and currentNode is a
                # left child.
                    currentNode.parent.color = 'black'
                    currentNode.parent.parent.color = 'red'
                    self._rightRotate(currentNode.parent.parent)
            else:
                # All of the cases where currentNode's parent is a right child
                # are mirror images of cases where currentNode's parent is a
                # left child. 
                y = currentNode.parent.parent.leftChild
                if y.color == 'red':
                    currentNode.parent.color = 'black'
                    y.color = 'black'
                    currentNode.parent.parent.color = 'red'
                    currentNode = currentNode.parent.parent
                else:
                    if currentNode.isLeftChild():
                        currentNode = currentNode.parent
                        self._rightRotate(currentNode)
                    currentNode.parent.color = 'black'
                    currentNode.parent.parent.color = 'red'
                    self._leftRotate(currentNode.parent.parent)
        self._root.color = 'black'

    def deleteFixup(self, currentNode):
        '''
        This method restores red black tree properties that may be violated
        during node deletions.
        '''
        while currentNode != self._root and currentNode.color == 'black':
            if currentNode.isLeftChild():
                # Case: currentNode has a red sibling
                w = currentNode.parent.rightChild
                if w.color == 'red':
                    w.color = 'black'
                    currentNode.parent.color = 'red'
                    self._leftRotate(currentNode.parent)
                    w = currentNode.parent.rightChild
                if (w.leftChild and w.leftChild.color == 'black' and 
                        w.rightChild and w.rightChild.color == 'black'):
                    # Case: currentNode has a black sibling with black children
                    w.color = 'red'
                    currentNode = currentNode.parent
                else:
                    if w.rightChild and w.rightChild.color == 'black':
                    # Case: currentNode has a black sibling with different
                    # colored children.
                        w.leftChild.color = 'black'
                        w.color = 'red'
                        self._rightRotate(w)
                        w = currentNode.parent.rightChild
                    # Case: currentNode has a black sibling with red children
                    w.color = currentNode.parent.color
                    currentNode.parent.color = 'black'
                    if w.rightChild:
                        w.rightChild.color = 'black'
                    self._leftRotate(currentNode.parent)
                    currentNode = self._root
            else:
                    # When currentNode is a black child, all cases are mirror
                    # images of when currentNode is a left child
                w = currentNode.parent.leftChild
                if w.color == 'red':
                    w.color = 'black'
                    currentNode.parent.color = 'red'
                    self._rightRotate(currentNode.parent)
                    w = currentNode.parent.leftChild
                if (w.leftChild and w.rightChild.color == 'black' and 
                        w.leftChild and w.leftChild.color == 'black'):
                    w.color = 'red'
                    currentNode = currentNode.parent
                else:
                    if w.leftChild and w.leftChild.color == 'black':
                        w.rightChild.color = 'black'
                        w.color = 'red'
                        self._leftRotate(w)
                        w = currentNode.parent.leftChild
                    w.color = currentNode.parent.color
                    currentNode.parent.color = 'black'
                    if w.leftChild:
                        w.leftChild.color = 'black'
                    self._rightRotate(currentNode.parent)
                    currentNode = self._root
        currentNode.color = 'black'
        return 
