# def two_sum(nums, target):
#     """
#     在数组中找到和为目标值的两个整数的下标。

#     :param nums: List[int] - 整数数组
#     :param target: int - 目标值
#     :return: List[int] - 两个整数的下标
#     """
#     num_to_index = {}
#     for index, num in enumerate(nums):
#         complement = target - num
#         if complement in num_to_index:
#             return [num_to_index[complement], index]
#         num_to_index[num] = index
#     return []
# if __name__ == "__main__":
#     nums = [2, 7, 11, 15]
#     target = 9
#     result = two_sum(nums, target)
#     print("结果下标:", result)
# class Solution:
#     def twoSum(self, nums: list[int], target: int) -> list[int]:
#         n = len(nums)
#         for i in range(n):
#             for j in range(i + 1, n):
#                 if nums[i] + nums[j] == target:
#                     return [i, j]
        
#         return []
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        hashtable = dict()
        for i, num in enumerate(nums):
            if target - num in hashtable:
                return [hashtable[target - num], i]
            hashtable[nums[i]] = i
        return []
