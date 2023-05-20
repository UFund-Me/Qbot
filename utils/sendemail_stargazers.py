'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-04-13 21:55:09
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-04-13 22:28:53
FilePath: /Qbot/utils/sendemail_stargazers.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''

import smtplib
import requests
import re
from github import Github

# Github 认证 token
token = "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"

# 设置 GitHub 认证
g = Github(token)

# 获取 repo 对象
repo_owner = "Charmve"
repo_name = "Charmve"
repo = g.get_repo(f"{repo_owner}/{repo_name}")

# pull issues 请求头
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json",
}

def close_github_issues(issue_url):
    pattern = r'issues\/(\d+)'
    match = re.search(pattern, issue_url)
    if match:
        issue_number = match.group(1)
        print(issue_number)
    else:
        print("No issue number found in the URL.")
    
    # 如果超过了一周，则构造PATCH请求来关闭该issue
    data = {'state': 'closed'}
    response = requests.patch(issue_url, headers=headers, json=data)

    # 检查响应状态码
    if response.ok:
        print(f"Issue #{issue_number} closed successfully.")
    else:
        print(f"Error closing issue #{issue_number}: {response.text}")

# 获取被 star 的用户列表，并发送邮件
for stargazer in repo.get_stargazers():
    # 获取收件人邮箱地址
    user = g.get_user(stargazer.login)
    receiver_email = user.email
    user_id = user.id
    print("receiver:", user_id)

    # 发送邮件
    if receiver_email:
        print("receiver_email:", receiver_email)
        """
        # 构造邮件内容和标题
        subject = "News! Charmve update repo"
        body = "Hello, {user_id}"

        message = f"Subject: {subject}\n\n{body}"
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message)
        """
    else:
        # 构造请求体
        data = {"title": "Issue Title", "body": "Issue Body"}

        # 发送 POST 请求
        # https://github.com/Charmve/100days
        repo_owner = "TheSpeedX"
        repo_name = "socker"
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
        response = requests.post(url, headers=headers, json=data)

        # 打印结果
        if response.status_code == 201:
            # print(response.json())
            issue_url = response.json()['html_url']
            print("Issue 已经成功创建！", issue_url)
            close_github_issues(issue_url)
            exit()
        else:
            print(f"创建 Issue 失败，错误码：{response.status_code}")
