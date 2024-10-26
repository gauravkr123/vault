class Solution:
    def canJump(self, nums: List[int]) -> bool:
        maxRange = 0
        if len(nums) <= 1:
            return True
        for i in range(len(nums)):
            if i > maxRange:
                return False
            currJump = nums[i]+i
            maxRange = max(maxRange,currJump)
            if(maxRange >= len(nums)-1):
                return True
        
        return True
            
        