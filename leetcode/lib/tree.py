class BT:  # Binary Tree
    @classmethod
    def isleaf(cls, node):
        return node and not any((node.left, node.right))

    @classmethod
    def preorder(cls, root):
        unused = root and [root]
        while unused:
            node = unused.pop()
            yield node
            unused.extend(filter(None, (node.right, node.left)))

    @classmethod
    def levelorder(cls, root, skip_none_child=True):
        level = root and [root]
        if skip_none_child:
            while level:
                yield level
                level = [child for node in level for child in (node.left, node.right) if child]
        else:
            while any(level):
                yield level
                level = [child for node in level for child in (node and node.left, node and node.right)]

    @classmethod
    def inorder(cls, root, direction='left'):
        def side_traversal(n):
            while n:
                yield n
                n = getattr(n, direction)

        unused = list(side_traversal(root))
        opposite = 'left' if direction == 'left' else 'right'
        while unused:
            node = unused.pop()
            yield node
            unused.extend(side_traversal(getattr(node, opposite)))

    @classmethod
    def postorder(cls, root):
        def left_traversal(n):
            while n:
                if n.right:
                    yield n.right
                yield n
                n = n.left

        unused = list(left_traversal(root))
        while unused:
            node = unused.pop()
            if unused and node.right is unused[-1]:
                unused[-1] = node
                unused.extend(left_traversal(node.right))
            else:
                yield node
