# class Solution :
#     def twoSum(self, nums: list[int], target: int)->list[int]:
#         num_to_index = {}
#         for index, num in enumerate (nums):
#             complement = target - num
#             if complement in num_to_index:
#                  return [num_to_index[complement], index]
#             num_to_index[num] = index
#         return[]

# class Solution:
#     #两数和 
#     def twoSum(self, nums: list[int], target: int) -> list[int]:
    
#         num_to_index = {}
#         for index, num in enumerate(nums):
#             complement = target - num
#             if complement in num_to_index:
#                 return [num_to_index[complement], index]
#             num_to_index[num] = index
#         return[]
# class Solution :
#     def twoSum(self, nums: list[int], target:int) -> list[int]:
#         n = len(nums)
#         for i in range(n):
#             for j in range(i + 1,n):
#                 if nums[i] + nums[j] == target:
#                     return[i , j]
#         return[]