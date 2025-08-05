import json
import uuid
from datetime import datetime

# 初始化用品列表
def load_items(filename="personal_items.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# 保存用品数据
def save_items(items, filename="personal_items.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

# 1. 添加物品
def add_item(items):
    print("\n--- 添加新物品 ---")
    
    # 生成唯一ID
    item_id = f"item-{str(uuid.uuid4())[:8]}"
    
    # 获取基本信息
    name = input("物品名称: ").strip()
    
    # 类别选择
    print("\n类别选项: 行李 | 书本 | 电影")
    category = input("选择类别: ").strip()
    
    # 位置选择
    print("\n位置选项: 卧室 | 客厅 | 书房 | 厨房 | 储藏室")
    location = input("存放位置: ").strip()
    
    # 状态选择
    print("\n状态选项: 使用中 | 闲置 | 待维修 | 已丢弃")
    status = input("当前状态: ").strip()
    
    # 其他信息
    purchase_date = input("购买日期(YYYY-MM-DD，可选): ").strip() or None
    price = float(input("购买价格(0表示未知): ").strip() or 0)
    description = input("物品描述(可选): ").strip() or ""
    
    # 标签管理
    tags = input("标签(用逗号分隔，如'工作,贵重'): ").strip()
    tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
    
    # 创建物品字典
    new_item = {
        "id": item_id,
        "name": name,
        "category": category,
        "location": location,
        "status": status,
        "purchase_date": purchase_date,
        "price": price,
        "description": description,
        "tags": tag_list,
        "last_used": datetime.now().strftime("%Y-%m-%d") if status == "使用中" else None
    }
    
    items.append(new_item)
    save_items(items)
    print(f"\n✅ 物品 '{name}' 添加成功! (ID: {item_id})")
    return True

# 2. 移除物品
def remove_item(items):
    print("\n--- 移除物品 ---")
    if not items:
        print("物品列表为空!")
        return False
    
    # 显示所有物品简略信息
    print("\n当前物品列表:")
    for item in items:
        print(f"ID: {item['id']} | 名称: {item['name']} | 类别: {item['category']} | 位置: {item['location']}")
    
    item_id = input("\n输入要移除的物品ID: ").strip()
    
    for i, item in enumerate(items):
        if item['id'] == item_id:
            confirm = input(f"确认移除 '{item['name']}'? (y/n): ").lower()
            if confirm == 'y':
                removed_item = items.pop(i)
                save_items(items)
                print(f"\n🗑️ 已移除物品: {removed_item['name']}")
                return True
            else:
                print("取消移除操作")
                return False
    
    print("错误：未找到该物品")
    return False

# 3. 更新物品状态
def update_item_status(items):
    print("\n--- 更新物品状态 ---")
    if not items:
        print("物品列表为空!")
        return False
    
    # 显示所有物品简略信息
    print("\n当前物品列表:")
    for item in items:
        print(f"ID: {item['id']} | 名称: {item['name']} | 当前状态: {item['status']}")
    
    item_id = input("\n输入要更新的物品ID: ").strip()
    
    for item in items:
        if item['id'] == item_id:
            print(f"\n物品名称: {item['name']}")
            print(f"当前状态: {item['status']}")
            print("位置: {item['location']}")
            
            # 状态选择
            print("\n新状态选项: 使用中 | 闲置 | 待维修 | 已丢弃")
            new_status = input("请输入新状态: ").strip()
            
            if new_status not in ["使用中", "闲置", "待维修", "已丢弃"]:
                print("错误：无效状态")
                return False
            
            # 更新状态
            item['status'] = new_status
            
            # 如果状态为"使用中"，更新最后使用日期
            if new_status == "使用中":
                item['last_used'] = datetime.now().strftime("%Y-%m-%d")
            
            # 可选：更新位置
            update_location = input("是否更新位置? (y/n): ").lower()
            if update_location == 'y':
                print("\n位置选项: 卧室 | 客厅 | 书房 | 厨房 | 储藏室")
                new_location = input("新位置: ").strip()
                item['location'] = new_location
            
            save_items(items)
            print(f"\n🔄 '{item['name']}' 状态已更新为: {new_status}")
            return True
    
    print("错误：未找到该物品")
    return False

# 多维度查看功能
def view_items(items):
    print("\n--- 多维度查看 ---")
    print("1. 按类别查看")
    print("2. 按位置查看")
    print("3. 按状态查看")
    print("4. 查看所有物品")
    
    choice = input("请选择查看方式: ").strip()
    
    filtered_items = []
    
    if choice == '1':  # 类别维度
        print("\n类别选项: 行李 | 书本 | 电影")
        category = input("选择类别: ").strip()
        filtered_items = [item for item in items if item['category'] == category]
        title = f"{category}类物品"
        
    elif choice == '2':  # 位置维度
        print("\n位置选项: 卧室 | 客厅 | 书房 | 厨房 | 储藏室")
        location = input("选择位置: ").strip()
        filtered_items = [item for item in items if item['location'] == location]
        title = f"{location}中的物品"
        
    elif choice == '3':  # 状态维度
        print("\n状态选项: 使用中 | 闲置 | 待维修 | 已丢弃")
        status = input("选择状态: ").strip()
        filtered_items = [item for item in items if item['status'] == status]
        title = f"状态为'{status}'的物品"
        
    elif choice == '4':  # 全部物品
        filtered_items = items
        title = "所有物品"
        
    else:
        print("无效选择")
        return
    
    # 显示结果
    print(f"\n==== {title} ==== (共 {len(filtered_items)} 件)")
    for item in filtered_items:
        print("\n" + "="*50)
        print(f"ID: {item['id']}")
        print(f"名称: {item['name']}")
        print(f"类别: {item['category']}")
        print(f"位置: {item['location']}")
        print(f"状态: {item['status']}")
        if item.get('last_used'):
            print(f"最后使用日期: {item['last_used']}")
        if item['purchase_date']:
            print(f"购买日期: {item['purchase_date']}")
        if item['price'] > 0:
            print(f"购买价格: ¥{item['price']:.2f}")
        if item['description']:
            print(f"描述: {item['description']}")
        if item['tags']:
            print(f"标签: {', '.join(item['tags'])}")
    
    print("\n" + "="*50)
def main():
    items = load_items()
    
    while True:
        print("\n==== 用品管理系统 ====")
        print("1. 添加物品")
        print("2. 移除物品")
        print("3. 更新物品状态")
        print("4. 查看物品")
        print("5. 退出系统")
        
        choice = input("请选择操作: ").strip()
        
        if choice == '1':
            add_item(items)
        elif choice == '2':
            remove_item(items)
        elif choice == '3':
            update_item_status(items)
        elif choice == '4':
            view_items(items)
        elif choice == '5':
            save_items(items)
            print("系统已退出，数据已保存")
            break
        else:
            print("无效选项，请重新选择")

if __name__ == "__main__":
    main()