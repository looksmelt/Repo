def two_sum(nums, target):
    """
    在数组中找到和为目标值的两个整数的下标。

    :param nums: List[int] - 整数数组
    :param target: int - 目标值
    :return: List[int] - 两个整数的下标
    """
    num_to_index = {}
    for index, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], index]
        num_to_index[num] = index
    return []

# 示例用法
if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9
    result = two_sum(nums, target)
    print("结果下标:", result)