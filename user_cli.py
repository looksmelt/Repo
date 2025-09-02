# -*- coding: utf-8 -*-
import argparse
from user_management_full import (
    register_user, login, change_password,
    count_adults, count_minors, get_gender_distribution,
    count_users_with_chinese_chars, get_usernames_with_chinese,
    count_users_per_domain
)

def main():
    parser = argparse.ArgumentParser(description='用户管理系统命令行接口')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 注册命令
    register_parser = subparsers.add_parser('register', help='注册新用户')
    register_parser.add_argument('-u', '--username', required=True, help='用户名(4-20位字母数字下划线)')
    register_parser.add_argument('-p', '--password', required=True, help='密码(8位以上，包含大小写字母和数字)')
    register_parser.add_argument('-e', '--email', required=True, help='邮箱地址')
    register_parser.add_argument('-ph', '--phone', required=True, help='手机号(11位数字)')
    register_parser.add_argument('-n', '--nickname', help='昵称')
    register_parser.add_argument('-a', '--age', type=int, help='年龄')
    register_parser.add_argument('-g', '--gender', choices=['male', 'female'], help='性别')

    # 登录命令
    login_parser = subparsers.add_parser('login', help='用户登录')
    login_parser.add_argument('-u', '--username', required=True, help='用户名')
    login_parser.add_argument('-p', '--password', required=True, help='密码')

    # 修改密码命令
    change_pwd_parser = subparsers.add_parser('change-password', help='修改密码')
    change_pwd_parser.add_argument('-u', '--username', required=True, help='用户名')
    change_pwd_parser.add_argument('-o', '--old-password', required=True, help='旧密码')
    change_pwd_parser.add_argument('-n', '--new-password', required=True, help='新密码')

    # 统计命令组
    stats_parser = subparsers.add_parser('stats',
        help='统计功能\n可用子命令:\n  age  年龄统计\n  gender   性别统计\n  ch  中文用户名统计\n  domain   邮箱域名统计')
    stats_subparsers = stats_parser.add_subparsers(
        dest='stats_command',
        metavar='子命令',
        help='统计子命令:\n age -t [adults|minors|all] 年龄统计\n gender 性别分布\n  ch -t [count|names] 中文用户名\n  domain -t [count|list] 邮箱域名')

    # 年龄统计
    age_parser = stats_subparsers.add_parser('age', help='年龄统计')
    age_parser.add_argument('-t', '--type', choices=['adults', 'minors', 'all'], 
                          default='all', help='统计类型(成年/未成年/全部)')

    # 性别统计
    stats_subparsers.add_parser('gender', help='性别分布统计')

    # 中文用户名统计
    ch_parser = stats_subparsers.add_parser('ch', help='中文用户名统计')
    ch_parser.add_argument('-t', '--type', choices=['count', 'names'], 
                         required=True, help='统计类型(数量/列表)')

    # 域名统计
    domain_parser = stats_subparsers.add_parser('domain', help='邮箱域名统计')
    domain_parser.add_argument('-t', '--type', choices=['count', 'list'], 
                             default='count', help='统计类型(数量/列表)')

    args = parser.parse_args()

    if args.command == 'register':
        result = register_user(
            username=args.username,
            password=args.password,
            email=args.email,
            phone=args.phone,
            nickname=args.nickname,
            age=args.age,
            gender=args.gender
        )
        print(result)

    elif args.command == 'login':
        result = login(username=args.username, password=args.password)
        print(result)

    elif args.command == 'change-password':
        result = change_password(
            username=args.username,
            old_password=args.old_password,
            new_password=args.new_password
        )
        print(result)

    elif args.command == 'stats':
        if args.stats_command == 'age':
            if args.type == 'adults':
                print(f"成年用户数量: {count_adults()}")
            elif args.type == 'minors':
                print(f"未成年用户数量: {count_minors()}")
            else:
                print(f"成年用户: {count_adults()}, 未成年用户: {count_minors()}")

        elif args.stats_command == 'gender':
            dist = get_gender_distribution()
            print("性别分布:")
            print(f"成年男性: {dist['adults']['male']}")
            print(f"成年女性: {dist['adults']['female']}")
            print(f"未成年男性: {dist['minors']['male']}")
            print(f"未成年女性: {dist['minors']['female']}")

        elif args.stats_command == 'ch':
            if args.type == 'count':
                print(f"包含中文的用户名数量: {count_users_with_chinese_chars()}")
            else:
                names = get_usernames_with_chinese()
                print("包含中文的用户名列表:")
                for name in names:
                    print(f"- {name}")

        elif args.stats_command == 'domain':
            if args.type == 'count':
                domains = count_users_per_domain()
                print("各域名用户数量:")
                for domain, count in domains.items():
                    print(f"{domain}: {count}")
            else:
                from user_management_full import list_unique_domains
                domains = list_unique_domains()
                print("唯一域名列表:")
                for domain in domains:
                    print(f"- {domain}")

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
#指令示例：
# 查询年龄分布：python user_cli.py stats age -t all