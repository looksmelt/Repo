# 用户数据结构
users = [
    {
    "username": "",      # 唯一标识（Key）
    "password": "",       # 密码 
    "email": "",          # 格式验证 
    "phone": "",          # 纯数字（11位）
    "nickname": "",       # 昵称 
    "age": 0,             # 整数 
    "gender": "unknown",  # 性别
    "signature": "",      # 个性签名 
    },
    # 更多用户...
]
import json
import re

# 初始化用户列表
def load_users(filename="2-mocked-users.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# 保存用户数据
def save_users(users, filename="2-mocked-users.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# 1. 用户注册
def register_user(users):
    print("\n--- 用户注册 ---")
    username = input("用户名: ").strip()
    
    # 检查用户名唯一性
    if any(u['username'] == username for u in users):
        print("错误：用户名已存在")
        return False
    
    password = input("密码: ").strip()
    email = input("邮箱: ").strip()
    phone = input("手机号: ").strip()
    
    # 手机号验证（11位数字）
    if not re.match(r'^\d{11}$', phone):
        print("错误：手机号格式不正确")
        return False
    
    # 其他信息录入
    nickname = input("昵称(可选): ").strip() or username
    age = int(input("年龄: ").strip())
    gender = input("性别(男/女): ").strip().lower()
    signature = input("个性签名(可选): ").strip() or "......"
    
    new_user = {
        "username": username,
        "password": password,
        "email": email,
        "phone": phone,
        "nickname": nickname,
        "age": age,
        "gender": gender,
        "signature": signature
    }
    
    users.append(new_user)
    save_users(users)
    print("注册成功！")
    return True

# 2. 用户登录
def login_user(users):
    print("\n--- 用户登录 ---")
    username = input("用户名: ").strip()
    password = input("密码: ").strip()
    
    for user in users:
        if user['username'] == username and user['password'] == password:
            print(f"登录成功！欢迎 {user['nickname']}")
            return user
    print("错误：用户名或密码不正确")
    return None

# 3. 修改密码
def change_password(users, current_user):
    print("\n--- 修改密码 ---")
    old_password = input("当前密码: ").strip()
    
    if old_password != current_user['password']:
        print("错误：密码验证失败")
        return False
    
    new_password = input("新密码: ").strip()
    confirm_password = input("确认新密码: ").strip()
    
    if new_password != confirm_password:
        print("错误：两次输入密码不一致")
        return False
    
    # 更新密码
    for i, user in enumerate(users):
        if user['username'] == current_user['username']:
            users[i]['password'] = new_password
            save_users(users)
            print("密码修改成功！")
            return True
    return False

# 4. 数据分析函数
def is_adult(user):
    """检查用户是否成年"""
    return user['age'] > 18

def age_analysis(users):
    """年龄分布统计"""
    adults = [u for u in users if is_adult(u)]
    minors = [u for u in users if not is_adult(u)]
    
    print(f"\n成年用户数量: {len(adults)}")
    print(f"未成年用户数量: {len(minors)}")
    
    # 性别分布
    def gender_dist(group):
        dist = {'male': 0, 'female': 0}
        for u in group:
            dist[u['gender']] += 1
        return{
        '男': dist['male'],
        '女': dist['female']
    }
    print("\n成年用户性别分布:")
    print(json.dumps(gender_dist(adults), indent=2))
    
    print("\n未成年用户性别分布:")
    print(json.dumps(gender_dist(minors), indent=2))

def chinese_username_count(users):
    """统计含中文字符的用户名"""
    count = 0
    for user in users:
        if re.search(r'[\u4e00-\u9fff]', user['username']):
            count += 1
    print(f"\n含中文字符的用户名用户数: {count}")

def email_domain_analysis(users):
    """邮箱类型分析"""
    domain_map = {}
    for user in users:
        domain = user['email'].split('@')[-1]
        if domain not in domain_map:
            domain_map[domain] = []
        domain_map[domain].append(user['username'])
    
    print("\n邮箱类型分布:")
    for domain, usernames in domain_map.items():
        print(f"- {domain}: {len(usernames)} 用户")
        print(f"  用户名: {', '.join(usernames[:3])}{'...' if len(usernames)>3 else ''}")
def main():
    users = load_users()
    current_user = None

    while True:
        print("\n==== 用户管理系统 ====")
        print("1. 注册")
        print("2. 登录")
        print("3. 修改密码")
        print("4. 数据分析")
        print("5. 退出")
        
        choice = input("请选择操作: ").strip()
        if choice == '1':
            register_user(users)
        elif choice == '2':
            current_user = login_user(users)
        elif choice == '3':
            if current_user:
                change_password(users, current_user)
            else:
                print("请先登录！")
        elif choice == '4':
            print("\n--- 数据分析 ---")
            age_analysis(users)
            chinese_username_count(users)
            email_domain_analysis(users)
        elif choice == '5':
            save_users(users)
            print("系统已退出")
            break
        else:
            print("无效选项，请重新选择")

if __name__ == "__main__":
    main()

# 在统计男女分布时有一个bug不知道怎么改了，求指导    
