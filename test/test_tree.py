from structure import BinaryTreeNode, BinaryTree


def test_inorder():
    """
        1         1      N      1        1
      2   3     2   N         N   9    2   3
     N 5 N N   9 N N N       N N 8 N
    """
    fs = [BinaryTree.inorder, BinaryTree._inorder]

    for f in fs:
        # 1
        root = BinaryTreeNode.from_list([1, 2, 3, None, 5, None, None])
        assert list(n.val for n in f(root)) == [2, 5, 1, 3]

        # 2
        root = BinaryTreeNode.from_list([1, 2, None, 9, None, None, None])
        assert list(n.val for n in f(root)) == [9, 2, 1]

        # 3
        root = BinaryTreeNode.from_list([None])
        assert list(n.val for n in f(root)) == []

        # 4
        root = BinaryTreeNode.from_list([1, None, 9, None, None, 8, None])
        assert list(n.val for n in f(root)) == [1, 8, 9]

        # 5
        root = BinaryTreeNode.from_list([1, 2, 3])
        assert list(n.val for n in f(root)) == [2, 1, 3]
