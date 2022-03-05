import unittest
from AVLTree import AVLTree, is_avl_tree, TreeNode

class TestProject1(unittest.TestCase):
    def test_is_avl_tree(self):
        a = AVLTree()
        assert is_avl_tree(a.root) is True  # 1

        a.root = TreeNode(2)
        assert is_avl_tree(a.root) is True  # 2

        a.root.left = TreeNode(1)
        assert is_avl_tree(a.root) is True  # 3

        a.root.left.left = TreeNode(0)

        assert is_avl_tree(a.root) is False  # 4

        a.root.right = TreeNode(0)
        assert is_avl_tree(a.root) is True  # 5


if __name__ == "__main__":
    unittest.main()
