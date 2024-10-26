# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def maxDepth(self, root, ans) -> int:
        if not root:
            return 0

        l = self.maxDepth(root.left, ans)
        r = self.maxDepth(root.right, ans)
        ans[0] = max(ans[0], l + r)
        return 1 + max(l, r)
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        ans = [0]
        self.maxDepth(root, ans)
        return ans[0]

        