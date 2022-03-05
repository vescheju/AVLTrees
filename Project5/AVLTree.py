"""
PROJECT 5 - AVL Trees
Name: Justin Vesche
"""

import queue

class TreeNode:
    # DO NOT MODIFY THIS CLASS #
    __slots__ = 'value', 'parent', 'left', 'right', 'height'

    def __init__(self, value, parent=None, left=None, right=None):
        """
        Initialization of a node
        :param value: value stored at the node
        :param parent: the parent node
        :param left: the left child node
        :param right: the right child node
        """
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right
        self.height = 0

    def __eq__(self, other):
        """
        Determine if the two nodes are equal
        :param other: the node being compared to
        :return: true if the nodes are equal, false otherwise
        """
        if type(self) is not type(other):
            return False
        return self.value == other.value

    def __str__(self):
        """String representation of a node by its value"""
        return str(self.value)

    def __repr__(self):
        """String representation of a node by its value"""
        return str(self.value)


class AVLTree:

    def __init__(self):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Initializes an empty Binary Search Tree
        """
        self.root = None
        self.size = 0

    def __eq__(self, other):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Describe equality comparison for BSTs ('==')
        :param other: BST being compared to
        :return: True if equal, False if not equal
        """
        if self.root is None and other.root is None:
            return True

        if self.size != other.size or self.root != other.root:
            return False  # size & root comp

        return self._is_equal(self.root.left, other.root.left) and self._is_equal(self.root.right, other.root.right)

    def _is_equal(self, root1, root2):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Checks if rootts are both not None then calls _compare, otherwise checks their equality.
        :param root1: root node of first tree
        :param root2: root node of second tree
        :return: True if equal, False if not
        """
        return self._compare(root1, root2) if root1 and root2 else root1 == root2

    def _compare(self, t1, t2):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Recursively compares two trees, used in __eq__.
        :param t1: root node of first tree
        :param t2: root node of second tree
        :return: True if equal, False if not
        """
        if t1 is None or t2 is None:
            return t1 == t2
        if t1 != t2:
            return False
        return self._compare(t1.left, t2.left) and self._compare(t1.right, t2.right)

    def __str__(self):
        """
        Collects a visual representation of AVL tree
        :return: string of AVL tree
        """
        if not self.root:
            return "Empty AVL Tree..."

        root = self.root
        ans = ""
        bfs_queue = []
        track = {}
        bfs_queue.append((root, 0, root.parent))
        h = AVLTree.height(self.root)

        for i in range(h + 1):
            track[i] = []

        while bfs_queue:
            node = bfs_queue.pop(0)
            if node[1] > h:
                break
            track[node[1]].append(node)

            if node[0] is None:
                bfs_queue.append((None, node[1] + 1, None))
                bfs_queue.append((None, node[1] + 1, None))
                continue

            if node[0].left:
                bfs_queue.append((node[0].left, node[1] + 1, node[0]))
            else:
                bfs_queue.append((None, node[1] + 1, None))

            if node[0].right:
                bfs_queue.append((node[0].right, node[1] + 1, node[0]))
            else:
                bfs_queue.append((None, node[1] + 1, None))

        spaces = pow(2, h) * 12
        ans += "\n"
        ans += "\t\tVisual Level Order Traversal of AVL Tree - Node (Parent Height)".center(spaces)
        ans += "\n\n"
        for i in range(h + 1):
            ans += f"Level {i}: "
            for node in track[i]:
                level = pow(2, i)
                space = int(round(spaces / level))
                if node[0] is None:
                    ans += " " * space
                    continue
                ans += "{} ({} {})".format(node[0], node[2], node[0].height).center(space, " ")
            ans += "\n"
        return ans

    # ------- Implement/Modify the functions below ------- #

    def insert(self, node, value):
        """
        Inserts a new node into the AVL tree, using a given value. Rebalance
        tree if needed.
        :return: Nothing
        """
        new_node = TreeNode(value)
        if self.root is None and node is None:
            self.root = new_node
            new_node.parent = None
            self.size += 1
            return
        elif node is not None:
            if node.value == value:
                return
            elif node.value > value:
                if node.left is None:
                    node.left = new_node
                    new_node.parent = node
                    self.size += 1
                else:
                    self.insert(node.left, value)
            else:
                if node.right is None:
                    node.right = new_node
                    new_node.parent = node
                    self.size += 1
                else:
                    self.insert(node.right, value)
            self.rebalance(node)


    def remove(self, node, value):
        """
        Use the given value to remove a value from the AVL tree, check
        for rebalanced after removing.
        :return: The new sub root after removal.
        """
        if self.root is None and node is None:
            return None
        if node is not None:
            if node.value == value:
                if node.right is not None and node.left is not None:
                    suc_node = self.max(node.left)
                    temp_value = suc_node.value
                    self.remove(node, temp_value)
                    node.value = temp_value

                elif node.right is not None and node.left is None:
                    if node.parent is None:
                        self.root = node.right
                        node.right.parent = None
                        self.size -= 1
                    elif node.parent.left == node:
                        node.parent.left = node.right
                        self.size -= 1
                        node.right.parent = node.parent
                        node = node.right
                    else:
                        node.parent.right = node.right
                        self.size -= 1
                        node.right.parent = node.parent
                        node = node.right

                elif node.left is not None and node.right is None:
                    if node.parent is None:
                        self.root = node.left
                        node.left.parent = None
                        self.size -= 1
                    elif node.parent.left == node:
                        node.parent.left = node.left
                        self.size -= 1
                        node.left.parent = node.parent
                        node = node.left
                    else:
                        node.parent.right = node.left
                        self.size -= 1
                        node.left.parent = node.parent
                        node = node.left
                else:
                    if node.parent is None:
                        self.size = 0
                        self.root = None
                        return None
                    elif node.parent.left == node:
                        node.parent.left = None
                    else:
                        node.parent.right = None
                    self.size -= 1
                    node = node.parent
            else:
                if node.value > value:
                    self.remove(node.left, value)
                    if node.parent is not None:
                        node = node.parent
                else:
                    self.remove(node.right, value)
                    if node.parent is not None:
                        node = node.parent
            return self.rebalance(node)

    @staticmethod
    def height(node):
        """
        Get height of given Node
        :return: height of the node
        """
        if node is not None:
            return node.height
        else:
            return -1

    @staticmethod
    def update_height(node):
        """
        Updates the height of the given node by looking at children
        of node
        :return: nothing
        """
        if node is None:
            return
        elif node.right is None and node.left is None:
            node.height = 0
        else:
            left_node = node.left
            right_node = node.right
            if left_node is None:
                node.height = node.right.height + 1
            elif right_node is None:
                node.height = node.left.height + 1
            else:
                if node.right.height > node.left.height:
                    node.height = node.right.height + 1
                else:
                    node.height = node.left.height + 1

    def depth(self, value):
        """
        search tree until found given node
        :return: string of AVL tree
        """
        if self.root is None:
            return -1
        counter = 0
        walker = self.root
        while walker is not None:
            if walker.value == value:
                return counter
            elif walker.value > value:
                walker = walker.left
                if walker is None:
                    return -1
                else:
                    counter += 1
            else:
                walker = walker.right
                if walker is None:
                    return -1
                else:
                    counter += 1
        return counter

    def search(self, node, value):
        """
        search the tree for the given value
        :return: return the node of the found value, or return its parent
        """
        if self.root is None or node is None:
            return None
        elif node is not None:
            if node.value == value:
                return node
            else:
                if node.value > value:
                    if node.left is None:
                        return node
                    else:
                        return self.search(node.left, value)
                else:
                    if node.right is None:
                        return node
                    else:
                        return self.search(node.right, value)

    def inorder(self, node):
        """
        Generate the in order of the tree
        :return: yield the in order
        """
        if node is None:
            return
        if node.left is not None:
            yield from self.inorder(node.left)
        yield node
        if node.right is not None:
            yield from self.inorder(node.right)


    def preorder(self, node):
        """
        Generate the pre order traversal of the tree
        :return: yield the pre order
        """
        if node is None:
            return
        yield node
        if node.left is not None:
            yield from self.preorder(node.left)

        if node.right is not None:
            yield from self.preorder(node.right)


    def postorder(self, node):
        """
        Generate the post order traversal of the tree
        :return: yield the post order
        """
        if node is None:
            return
        if node.left is not None:
            yield from self.postorder(node.left)

        if node.right is not None:
            yield from self.postorder(node.right)
        yield node

    def bfs(self):
        """
        Generate the Breadth First traversal of the tree
        :return: yield the breadth first
        """
        if self.root is None:
            return
        the_queue = queue.Queue()
        the_queue.put(self.root)
        while not the_queue.empty():
            last = the_queue.get()
            yield last
            if last.left is not None:
                the_queue.put(last.left)
            if last.right is not None:
                the_queue.put(last.right)

    def min(self, node):
        """
        Get the min of the tree by going through the left
        of the tree.
        :return: min
        """
        if self.root is None or node is None:
            return None
        elif node is not None:
            if node.left is not None:
                return self.min(node.left)
            elif node.left is None:
                return node

    def max(self, node):
        """
        Get the max of the tree by going through the right
        of the tree.
        :return: max
        """
        if self.root is None or node is None:
            return None
        elif node is not None:
            if node.right is not None:
                return self.max(node.right)
            elif node.right is None:
                return node

    def get_size(self):
        """
        Get the size of the tree
        :return: size of tree
        """
        return self.size

    @staticmethod
    def get_balance(node):
        """
        Check for the balance of the given node. Use left and right children
        to set the balance of the child
        :return: balance
        """
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 0
        elif node.left is None:
            return -1 - node.right.height
        elif node.right is None:
            return node.left.height + 1
        else:
            return node.left.height - node.right.height

    @staticmethod
    def set_child(parent, child, is_left):
        """
        Set the child of the parent with the given child, check if we set
        left or right child. Update height in process
        :return: Nothing
        """
        if is_left:
            parent.left = child
            if child is not None:
                child.parent = parent
        else:
            parent.right = child
            if child is not None:
                child.parent = parent
        AVLTree.update_height(parent)

    @staticmethod
    def replace_child(parent, current_child, new_child):
        """
        replace the child of the given parent with the new_child
        :return: nothing
        """
        if parent.left == current_child:
            AVLTree.set_child(parent, new_child, True)
        elif parent.right == current_child:
            AVLTree.set_child(parent, new_child, False)

    def left_rotate(self, node):
        """
        Rotate the given node to the right, changing the nodes parent child
        and the nodes children
        :return: new root of the subtree
        """
        return_node = node.right
        right_left_child = node.right.left
        if node.parent is not None:
            self.replace_child(node.parent, node, node.right)
        else:
            self.root = node.right
            self.root.parent = None
        self.set_child(node.right, node, True)
        self.set_child(node, right_left_child, False)
        self.update_height(node)
        self.update_height(return_node)
        return return_node

    def right_rotate(self, node):
        """
        Rotate the given node to the right, changing the nodes parent child
        and the nodes children
        :return: new root of the subtree
        """
        return_node = node.left
        left_right_child = node.left.right
        if node.parent is not None:
            self.replace_child(node.parent, node, node.left)
        else:
            self.root = node.left
            self.root.parent = None
        self.set_child(node.left, node, False)
        self.set_child(node, left_right_child, True)
        self.update_height(node)
        self.update_height(return_node)
        return return_node

    def rebalance(self, node):
        """
        check to see if rotations are needed to rebalance the given node
        :return: the new root node of the subtree
        """
        if node is None:
            return
        self.update_height(node)
        if self.get_balance(node) == -2:  # left rotate
            if self.get_balance(node.right) == 1:
                self.right_rotate(node.right)
            return self.left_rotate(node)

        elif self.get_balance(node) == 2:
            if self.get_balance(node.left) == -1:
                self.left_rotate(node.left)
            return self.right_rotate(node)
        return node

# ------- Application Problem ------- #
def is_avl_tree(node):
    """
    Check conditionals of each node to see if the value is an AVL tree.
    If condition is met then not an AVL Tree. Conditions include left-left,
    left-right, right-left, right-right
    :return: true if an avl_tree else false
    """
    if node is None:
        return True
    if node.right is None and node.left is None:
        return True
    elif node.left is not None:
        if node.right is None:
            if node.left.left is not None:
                return False
            if node.left.right is not None:
                return False
    elif node.right is not None:
        if node.left is None:
            if node.right.right is not None:
                return False
            if node.right.left is not None:
                return False
    is_left = is_avl_tree(node.left)
    if is_left is False:
        return False
    is_right = is_avl_tree(node.right)
    if is_right is False:
        return False
    return True



