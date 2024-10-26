# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def inorder(self, root, counter, k, ans) -> None:
        if not root or counter[0] > k:
            return

        self.inorder(root.left, counter, k, ans)
        counter[0] = counter[0]+1
        if(counter[0] == k):
            ans[0] = root.val
            return
        self.inorder(root.right, counter, k, ans)

    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        ans = [float("inf")]
        counter = [0]
        self.inorder(root, counter, k, ans)
        return ans[0]
        