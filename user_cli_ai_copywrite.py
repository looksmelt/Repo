# 用户管理系统的数据结构
users = [
    { 
        "username": "",     # 用户名
        "password": "",     # 密码
        "phone": "",        # 手机号
        "email": "",        # 邮箱
        "age": 0,           # 年龄
        "gender": "",       # 性别 
        "nickname": "",     # 昵称     
        "signature": "",    # 个性签名        
},
# 更多用户
]

import json 
import re   

#初始化用户列表
def load_users(filename="2-mocked-users.json"):
    try:
        with open("2-mocked-users.json", "r" , encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("警告：用户数据文件格式错误，将使用空列表")
        return []
# 保存用户数据
def save_users(users ,filename="2-mocked-users.json"):
    with open('2-mocked-users.json', 'w', encoding='utf-8') as f:
        json.dump(users , f, ensure_ascii=False,indent=2)
    with open("2-mocked-users.json","w", encoding ="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9,._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
# 1. 用户注册
def register_user(users):
    print("\n--- 用户注册 ---")
    
    # 获取并验证用户名
    while True:
        username = input("用户名: ").strip()
        if not username:
            print("错误：用户名不能为空")
            continue
            
        if any(u['username'] == username for u in users):
            print("错误：用户名已存在")
            continue
            
        break
    
    # 获取密码
    password = input("密码: ").strip()
    if not password:
        print("错误：密码不能为空")
        return False
    
    # 获取并验证邮箱
    while True:
        email = input("邮箱: ").strip()
        if not is_valid_email(email):
            print("错误：邮箱格式不正确")
            continue
        break
    
    # 获取并验证手机号
    while True:
        phone = input("手机号: ").strip()
        if not re.match(r'^\d{11}$', phone):
            print("错误：手机号必须是11位数字")
            continue
        break
    
    # 其他信息录入
    nickname = input("昵称(可选): ").strip() or username
    
    while True:
        try:
            age = int(input("年龄: ").strip())
            if age < 0 or age > 120:
                print("错误：年龄必须在0-120之间")
                continue
            break
        except ValueError:
            print("错误：请输入有效的整数年龄")
    
    gender = ""
    while gender not in ["男", "女"]:
        gender = input("性别(男/女): ").strip().lower()
        if gender in ["男", "m"]:
            gender = "男"
        elif gender in ["女", "f"]:
            gender = "女"
        else:
            print("错误：请输入'男'或'女'")
    
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
    print(f"注册成功！欢迎 {nickname}")
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
    
    # 确保 current_user 是有效的用户字典
    if not current_user or not isinstance(current_user, dict):
        print("错误：用户未登录或登录信息无效")
        return False
    
    # 验证当前密码
    attempts = 0
    while attempts < 3:
        old_password = input("当前密码: ").strip()
        if old_password == current_user['password']:
            break
        attempts += 1
        print(f"错误：密码不正确，还剩{3-attempts}次尝试")
    
    if attempts >= 3:
        print("错误：密码验证失败次数过多")
        return False
    
    # 设置新密码
    while True:
        new_password = input("新密码: ").strip()
        if not new_password:
            print("错误：密码不能为空")
            continue
            
        confirm_password = input("确认新密码: ").strip()
        if new_password != confirm_password:
            print("错误：两次输入密码不一致")
            continue
            
        break
    
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
    return user['age'] >= 18

def gender_normalize(gender):
    """统一性别表示格式"""
    gender = str(gender).lower().strip()
    if gender in ['男', 'male', 'm']:
        return '男'
    if gender in ['女', 'female', 'f']:
        return '女'
    return '未知'

def age_analysis(users):
    """年龄分布统计"""
    if not users:
        print("暂无用户数据")
        return
    
    adults = [u for u in users if is_adult(u)]
    minors = [u for u in users if not is_adult(u)]
    
    print(f"\n用户总数: {len(users)}")
    print(f"成年用户数量: {len(adults)} (占比{len(adults)/len(users):.1%})")
    print(f"未成年用户数量: {len(minors)} (占比{len(minors)/len(users):.1%})")
    
    # 性别分布统计
    def gender_distribution(group):
        dist = {'男': 0, '女': 0, '未知': 0}
        for u in group:
            dist[gender_normalize(u['gender'])] += 1
        return dist
    
    # 成年用户性别分布
    adult_gender = gender_distribution(adults)
    print("\n[成年用户性别分布]")
    print(f"男: {adult_gender['男']} (占比{adult_gender['男']/len(adults):.1%})")
    print(f"女: {adult_gender['女']} (占比{adult_gender['女']/len(adults):.1%})")
    print(f"未知: {adult_gender['未知']}")
    
    # 未成年用户性别分布
    minor_gender = gender_distribution(minors)
    print("\n[未成年用户性别分布]")
    print(f"男: {minor_gender['男']} (占比{minor_gender['男']/len(minors):.1%})")
    print(f"女: {minor_gender['女']} (占比{minor_gender['女']/len(minors):.1%})")
    print(f"未知: {minor_gender['未知']}")

def chinese_username_count(users):
    """统计含中文字符的用户名"""
    if not users:
        print("暂无用户数据")
        return
    
    count = 0
    for user in users:
        if re.search(r'[\u4e00-\u9fff]', user['username']):
            count += 1
    
    print(f"\n含中文字符的用户名用户数: {count} (占比{count/len(users):.1%})")

def email_domain_analysis(users):
    """邮箱类型分析"""
    if not users:
        print("暂无用户数据")
        return
    
    domain_map = {}
    for user in users:
        try:
            domain = user['email'].split('@')[-1].lower()
            domain_map[domain] = domain_map.get(domain, 0) + 1
        except IndexError:
            pass
    
    if not domain_map:
        print("未找到有效的邮箱数据")
        return
    
    # 按用户数排序
    sorted_domains = sorted(domain_map.items(), key=lambda x: x[1], reverse=True)
    
    print("\n[邮箱类型分布]")
    for domain, count in sorted_domains[:5]:  # 只显示前5种类型
        print(f"- {domain}: {count} 用户 (占比{count/len(users):.1%})")
    
    if len(sorted_domains) > 5:
        print(f"...及其他 {len(sorted_domains)-5} 种邮箱类型")

def main():
    users = load_users()
    current_user = None

    while True:
        print("\n==== 用户管理系统 ====")
        if current_user and isinstance(current_user, dict):
            print(f"当前用户: {current_user['nickname']} ({current_user['username']})")
        else:
            print("当前用户: 未登录")
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
