import json
import re
from typing import List, Dict, Optional, Union

# 用户数据结构
User = Dict[str, Union[str, int]]
users: List[User] = []


def load_mocked_users() -> None:
    """
    从2-mocked-users.json加载测试用户数据到全局users列表

    Raises:
        FileNotFoundError: 当测试数据文件不存在时
        json.JSONDecodeError: 当测试数据文件格式错误时
    """
    global users
    try:
        with open('2-mocked-users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
    except FileNotFoundError:
        print("警告: 测试数据文件未找到，将使用空用户列表")
    except json.JSONDecodeError:
        print("警告: 测试数据文件格式错误，将使用空用户列表")


def is_valid_username(username: str) -> bool:
    """
    验证用户名格式(4-20位字母数字下划线)

    Args:
        username: 要验证的用户名字符串

    Returns:
        bool: 如果格式有效返回True，否则返回False
    """
    pattern = r'^\w{4,20}$'
    return re.match(pattern, username) is not None
# def is_valid_username(username: str) -> bool:
#     '''
#     yanzheng yonghuming geshi(4-20wei zimu shuzi xiahuaxian)
#     args:
#         username:要验证的用户名字符串
        
#     returns:
#         boll：如果用户名的格式有效返回True,否则返回False
#     '''
#     pattern = r'^\w{4,20}$'
#     return re.match(pattern, username) is not None

def is_valid_email(email: str) -> bool:
    """
    验证邮箱格式

    Args:
        email: 要验证的邮箱字符串

    Returns:
        bool: 如果格式有效返回True，否则返回False
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
# def is_valid_email(email: str) -> bool:
#     '''
#     验证邮箱的格式
#     args:
#         email:要验证的邮箱字符串
        
#     returns:
#         boll：如果邮箱的格式有效返回True,否则返回False
#     '''
#     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#     return re.match(pattern, email) is not None

def is_valid_phone(phone: str) -> bool:
    """
    验证手机号格式(11位数字)

    Args:
        phone: 要验证的手机号字符串

    Returns:
        bool: 如果格式有效返回True，否则返回False
    """
    return phone.isdigit() and len(phone) == 11
# def is_valid_phone(phone: str) -> bool:
#     '''
#     验证手机号码格式u（11位数字）
#     args：
#         phone：要验证手机好嘛的字符串
#     returns:
#         bool：如果手机号码字符串的格式有效返回True,否则返回False'''
#     return phone.isdigit() and len(phone) == 11


def is_strong_password(password: str) -> bool:
    """
    验证密码强度(8位以上，包含大小写字母和数字)

    Args:
        password: 要验证的密码字符串

    Returns:
        bool: 如果密码强度足够返回True，否则返回False
    """
    if len(password) < 8:
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True
# def is_strong_password(password: str) -> bool:
#     '''
#     验证密码强度 （8位以上，含大小写字母和数字）
#     args：
#         password： 要验证的密码的字符串
#     returns:
#         bool:如果密码的强度足够返回Trie，否则返回False
#     '''
#     if len(password) < 8:
#         return False
#     if not re.search(r'[a-z]', password ):
#         return False
#     if not re.search(r'[A-Z]', password):
#         return Fakse
#     if not re.search(r'[0-9]', password):
#         return False
#     return True

def is_username_taken(username: str) -> bool:
    """
    检查用户名是否已被使用

    Args:
        username: 要检查的用户名

    Returns:
        bool: 如果用户名已存在返回True，否则返回False
    """
    return any(user['username'] == username for user in users)
# def is_username_taken(username: str) -> bool:
#     '''
#     检查用户名是否已被使用
#     args：
#         username:要检查的用户名
#     return：
#         bool：如果用户名已经存在返回True，否则返回False
#     '''
#     return any(user['username'] == username for user in users)


def register_user(
    username: str,
    password: str,
    email: str,
    phone: str,
    nickname: Optional[str] = None,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    **kwargs
) -> Dict[str, Union[bool, str]]:
    """
    注册新用户

    Args:
        username: 用户名(4-20位字母数字下划线)
        password: 密码(8位以上，包含大小写字母和数字)
        email: 邮箱(有效格式)
        phone: 手机号(11位数字)
        nickname: 可选昵称
        age: 可选年龄
        gender: 可选性别
        **kwargs: 其他可选用户属性

    Returns:
        Dict: 包含操作状态、消息和用户信息的字典，结构为:
        {
            'success': bool,  # 操作是否成功
            'message': str,    # 结果消息
            'user': Dict       # 注册成功的用户信息(仅success为True时存在)
        }

    Raises:
        ValueError: 当输入验证失败时

    Examples:
        >>> register_user("testuser", "Pass1234", "test@example.com", "13812345678")
        {'success': True, 'message': '用户注册成功', 'user': {...}}
    """
    # 输入验证
    if not username or not password or not email or not phone:
        return {'success': False, 'message': '所有必填字段不能为空'}

    if not is_valid_username(username):
        return {'success': False, 'message': '用户名格式无效(4-20位字母数字下划线)'}

    if is_username_taken(username):
        return {'success': False, 'message': '用户名已被使用'}

    if not is_valid_email(email):
        return {'success': False, 'message': '邮箱格式无效'}

    if not is_valid_phone(phone):
        return {'success': False, 'message': '手机号格式无效(需要11位数字)'}

    if not is_strong_password(password):
        return {'success': False, 'message': '密码强度不足(需8位以上，包含大小写字母和数字)'}
    # #输入验证
    # if not username or not password or not email or not phone:
    #     return {'success':False, 'message':'所有必填字段不能为空'}
    # if not is_valid_username(username):
    #     return {'success': False, 'message':'用户名格式无效（4-20位字母数字下划线）'}
    # if not is_username_taken(username):
    #     return {'success': False,'message':'用户名已注册'}
    # if not is_valid_email(email):
    #     return {'success': False, 'message':'邮箱格式无效'}
    # if not is_valid_phone(phone):
    #     return {'success': False, 'message':'手机号格式无效（需要11位数字）'}
    # if not is_strong_password(password):
    #     return {'success': False, 'message':'密码强度不足（需8位以上，包含大小写字母和数字）'}
    
    # 创建新用户
    # new_user = {
    #     'id': len(users) + 1,
    #     'username': username,
    #     'password': password,
    #     'email': email,
    #     'mobile': phone,
    #     'age': age,
    #     'gender': gender,
    #     'nickname': nickname,
    #     **kwargs
    # }

    # users.append(new_user)
    # return {'success': True, 'message': '用户注册成功', 'user': new_user}
    #创建新用户
    new_user = {
        'id': len(users) + 1,
        'username': username,       
        'password': password,
        'email': email,
        'mobile': phone,
        'age': age,
        'gender': gender,
        'nickname': nickname,
        **kwargs
    }
    users.append(new_user)
    return {'success': True ,'message': '用户注册成功', 'user': new_user}


def login(username: str, password: str) -> Dict[str, Union[bool, str, Dict]]:
# def login(username: str, password: str) -> Dict[str, Union[bool, str, Dict]]:

    """
    用户登录验证

    Args:
        username: 用户名
        password: 密码

    Returns:
        Dict: 包含登录状态、消息和用户信息的字典，结构为:
        {
            'success': bool,  # 登录是否成功
            'message': str,   # 结果消息
            'user': Dict      # 用户信息(仅success为True时存在)
        }

    Examples:
        >>> login("testuser", "Pass1234")
        {'success': True, 'message': '登录成功', 'user': {...}}
    """
    # if not username or not password:
    #     return {'success': False, 'massage': '用户名和密码不能为空'}
    if not username or not password:
        return {'success': False, 'message': '用户名和密码不能为空'}

    user = next((u for u in users if u['username'] == username), None)  #匹配用户名
    # user = next((u for u in users if u['username'] == username), None)

    if not user:
        return {'success': False, 'message': '用户名不存在'}
    # if not user:
    #     return {'success': False, 'message': '用户名不存在'}
    
    if user['password'] != password:
        return {'success': False, 'message': '密码不正确'}
    # if user['password'] != password:
    #     return {'success': False, 'message': '密码不正确'}

    # 返回用户信息时移除密码字段
    user_data = user.copy()
    user_data.pop('password')
    return {'success': True, 'message': '登录成功', 'user': user_data}
    # # 返回用户信息时移除密码字段
    # user_data = user.copy()
    # user_data.pop('password')
    # return {'success': True, 'message': '登录成功', 'user': user_data}


def change_password(username: str, old_password: str, new_password: str) -> Dict[str, Union[bool, str]]:
    """
    修改用户密码

    Args:
        username: 用户名
        old_password: 旧密码
        new_password: 新密码

    Returns:
        Dict: 包含操作状态和消息的字典，结构为:
        {
            'success': bool,  # 操作是否成功
            'message': str   # 结果消息
        }

    Examples:
        >>> change_password("testuser", "oldPass", "newPass123")
        {'success': True, 'message': '密码修改成功'}
    """
    if not username or not old_password or not new_password:
        return {'success': False, 'message': '所有字段不能为空'}

    if old_password == new_password:
        return {'success': False, 'message': '新密码不能与旧密码相同'}

    if not is_strong_password(new_password):
        return {'success': False, 'message': '新密码强度不足(需8位以上，包含大小写字母和数字)'}

    user = next((u for u in users if u['username'] == username), None)

    if not user:
        return {'success': False, 'message': '用户名不存在'}

    if user['password'] != old_password:
        return {'success': False, 'message': '旧密码不正确'}

    user['password'] = new_password
    return {'success': True, 'message': '密码修改成功'}

# def change_password(username: str, old_password: str, new_password: str) -> Dict[str, Union[bool, str]]:
#     """
#     修改用户密码

#     Args:
#         username: 用户名
#         old_password: 旧密码
#         new_password: 新密码

#     Returns:
#         Dict: 包含操作状态和消息的字典，结构为:
#         {
#             'success': bool,  # 操作是否成功
#             'message': str   # 结果消息
#         }

#     Examples:
#         >>> change_password("testuser", "oldPass", "newPass123")
#         {'success': True, 'message': '密码修改成功'}
#     """
#     if not username or not old_password or not new_password:
#         return {'success': False, 'message': '所有字段不能为空'}

#     if old_password == new_password:
#         return {'success': False, 'message': '新密码不能与旧密码相同'}

#     if not is_strong_password(new_password):
#         return {'success': False, 'message': '新密码强度不足(需8位以上，包含大小写字母和数字)'}

#     user = next((u for u in users if u['username'] == username), None)

#     if not user:
#         return {'success': False, 'message': '用户名不存在'}

#     if user['password'] != old_password:
#         return {'success': False, 'message': '旧密码不正确'}

#     user['password'] = new_password
#     return {'success': True, 'message': '密码修改成功'}

def is_adult(user: Dict) -> bool:
    """
    判断用户是否成年(≥18岁)

    Args:
        user: 用户字典

    Returns:
        bool: 如果用户成年返回True，否则返回False
    """
    return user.get('age', 0) >= 18 if user.get('age') is not None else False

# def is_adult(user: Dict) -> bool:
#     """
#     判断用户是否成年(≥18岁)

#     Args:
#         user: 用户字典

#     Returns:
#         bool: 如果用户成年返回True，否则返回False
#     """
#     return user.get('age', 0) >= 18 if user.get('age') is not None else False

def count_adults() -> int:
    """
    统计成年用户数量

    Returns:
        int: 成年用户数量
    """
    return sum(1 for user in users if is_adult(user))
# def count_adults() -> int:
#     """
#     统计成年用户数量

#     Returns:
#         int: 成年用户数量
#     """
#     return sum(1 for user in users if is_adult(user))


def count_minors() -> int:
    """
    统计未成年用户数量

    Returns:
        int: 未成年用户数量
    """
    return sum(1 for user in users if not is_adult(user))

# def count_minors() -> int:
#     """
#     统计未成年用户数量

#     Returns:
#         int: 未成年用户数量
#     """
#     return sum(1 for user in users if not is_adult(user))


def get_gender_distribution() -> Dict[str, Dict[str, int]]:
    """
    获取性别分布统计(按成年/未成年分组)

    Returns:
        Dict: 包含性别统计结果的字典，结构为:
        {
            'adults': {'male': x, 'female': y},
            'minors': {'male': a, 'female': b}
        }
    """
    result = {
        'adults': {'male': 0, 'female': 0},
        'minors': {'male': 0, 'female': 0}
    }

    for user in users:
        gender = user.get('gender', '').lower()
        if gender not in ['male', 'female']:
            continue

        if is_adult(user):
            result['adults'][gender] += 1
        else:
            result['minors'][gender] += 1

    return result
# def get_gender_distribution() -> Dict[str, Dict[str, int]]:
#     """
#     获取性别分布统计(按成年/未成年分组)

#     Returns:
#         Dict: 包含性别统计结果的字典，结构为:
#         {
#             'adults': {'male': x, 'female': y},
#             'minors': {'male': a, 'female': b}
#         }
#     """
#     result = {
#         'adults': {'male': 0, 'female': 0},
#         'minors': {'male': 0, 'female': 0}
#     }

#     for user in users:
#         gender = user.get('gender', '').lower()
#         if gender not in ['male', 'female']:
#             continue

#         if is_adult(user):
#             result['adults'][gender] += 1
#         else:
#             result['minors'][gender] += 1

#     return result


def contains_chinese(text: str) -> bool:
    """
    检查字符串是否包含中文字符

    Args:
        text: 要检查的字符串

    Returns:
        bool: 如果包含中文字符返回True，否则返回False
    """
    return any('\u4e00' <= char <= '\u9fff' for char in text)
# def contains_chinese(text: str) -> bool:
#     """
#     检查字符串是否包含中文字符

#     Args:
#         text: 要检查的字符串

#     Returns:
#         bool: 如果包含中文字符返回True，否则返回False
#     """
#     return any('\u4e00' <= char <= '\u9fff' for char in text)



def count_users_with_chinese_chars() -> int:
    """
    统计用户名包含中文字符的用户数量

    Returns:
        int: 包含中文字符的用户名数量
    """
    return sum(1 for user in users if contains_chinese(user.get('username', '')))
# def count_users_with_chinese_chars() -> int:
#     """
#     统计用户名包含中文字符的用户数量

#     Returns:
#         int: 包含中文字符的用户名数量
#     """
#     return sum(1 for user in users if contains_chinese(user.get('username', '')))


def get_usernames_with_chinese() -> List[str]:
    """
    获取所有包含中文字符的用户名

    Returns:
        List[str]: 包含中文字符的用户名列表
    """
    return [user['username'] for user in users if contains_chinese(user.get('username', ''))]
# def get_usernames_with_chinese() -> List[str]:
#     """
#     获取所有包含中文字符的用户名

#     Returns:
#         List[str]: 包含中文字符的用户名列表
#     """
#     return [user['username'] for user in users if contains_chinese(user.get('username', ''))]


def extract_domain(email: str) -> str:
    """
    从邮箱地址中提取域名部分

    Args:
        email: 邮箱地址

    Returns:
        str: 域名部分(小写)，如果邮箱无效则返回空字符串
    """
    return email.split('@')[-1].lower() if '@' in email else ''
# def extract_domain(email: str) -> str:
#     """
#     从邮箱地址中提取域名部分

#     Args:
#         email: 邮箱地址

#     Returns:
#         str: 域名部分(小写)，如果邮箱无效则返回空字符串
#     """
#     return email.split('@')[-1].lower() if '@' in email else ''


def list_unique_domains() -> List[str]:
    """
    获取所有唯一的邮箱域名

    Returns:
        List[str]: 按字母排序的唯一域名列表
    """
    domains = set()
    for user in users:
        domain = extract_domain(user.get('email', ''))
        if domain:
            domains.add(domain)
    return sorted(domains)
# def list_unique_domains() -> List[str]:
#     """
#     获取所有唯一的邮箱域名

#     Returns:
#         List[str]: 按字母排序的唯一域名列表
#     """
#     domains = set()
#     for user in users:
#         domain = extract_domain(user.get('email', ''))
#         if domain:
#             domains.add(domain)
#     return sorted(domains)

def count_users_per_domain() -> Dict[str, int]:
    """
    统计每个域名的用户数量

    Returns:
        Dict[str, int]: 域名到用户数量的映射字典
    """
    domain_counts = {}
    for user in users:
        domain = extract_domain(user.get('email', ''))
        if domain:
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
    return domain_counts
# def count_users_per_domain() -> Dict[str, int]:
#     """
#     统计每个域名的用户数量

#     Returns:
#         Dict[str, int]: 域名到用户数量的映射字典
#     """
#     domain_counts = {}
#     for user in users:
#         domain = extract_domain(user.get('email', ''))
#         if domain:
#             domain_counts[domain] = domain_counts.get(domain, 0) + 1
#     return domain_counts


def get_usernames_by_domain(domain: str) -> List[str]:
    """
    获取指定域名的所有用户名

    Args:
        domain: 要查询的域名

    Returns:
        List[str]: 属于该域名的用户名列表
    """
    return [user['username'] for user in users
            if extract_domain(user.get('email', '')) == domain.lower()]
# def get_usernames_by_domain(domain: str) -> List[str]:
#     """
#     获取指定域名的所有用户名

#     Args:
#         domain: 要查询的域名

#     Returns:
#         List[str]: 属于该域名的用户名列表
#     """
#     return [user['username'] for user in users
#             if extract_domain(user.get('email', '')) == domain.lower()]


# 初始化时加载测试数据
load_mocked_users()
# #初始化时加载测试数据
# load_macked_users()