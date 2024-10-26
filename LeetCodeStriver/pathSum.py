# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root == None:
            return False
        #check if target < 0
        currentValue = targetSum-root.val
        if root.left == None and root.right == None:
            if currentValue == 0:
                return True
            else:
                return False

        if (root.left and self.hasPathSum(root.left, currentValue)) or (root.right and self.hasPathSum(root.right, currentValue)):
            return True

        return False
        