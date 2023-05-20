import requests

# Github 认证 token
token = "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"

# 请求头
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

# 请求体
data = {
    "title": "Issue Title",
    "body": "Issue Body"
}

# 发送 POST 请求
# https://github.com/Charmve/100days
repo_owner = "TheSpeedX"
repo_name = "socker"
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
response = requests.post(url, headers=headers, json=data)

# 打印结果
if response.status_code == 201:
    print("Issue 已经成功创建！")
else:
    print(f"创建 Issue 失败，错误码：{response.status_code}")
