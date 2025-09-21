import requests
import re
import os

# 定义域名规则文件和输出文件名
domain_rule_files = [
    ("https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/direct.txt", "direct.list"),
    ("https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/proxy.txt", "proxy.list"),
    ("https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/reject.txt", "reject.list"),
    ("https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/private.txt", "private.list"),
    ("https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/apple.txt", "apple.list"),
    ("https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/icloud.txt", "icloud.list"),
    ("https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/gfw.txt", "gfw.list"),
    ("https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/tld-not-cn.txt", "tld-not-cn.list")
]

# 定义 IP 规则文件和输出文件名
ip_rule_files = [
    ("https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/telegramcidr.txt", "telegramcidr.list"),
    ("https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/lancidr.txt", "lancidr.list"),
    ("https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/cncidr.txt", "cncidr.list")
]

# 创建输出目录
output_dir = "converted_rules"
os.makedirs(output_dir, exist_ok=True)

# 转换域名规则
def convert_domain_rules(url, output_file):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"下载失败：{url}")
        return
    
    lines = response.text.splitlines()
    converted_lines = []
    
    for line in lines:
        # 跳过空行、注释或 payload: 行
        if not line.strip() or line.startswith('#') or line.strip() == 'payload:':
            continue
        # 匹配 - ' 开头的行，移除 - ' 和末尾 '
        match = re.match(r'^- \'(.+?)\'$', line.strip())
        if match:
            domain = match.group(1)
            # 判断是否为 + 开头（DOMAIN-SUFFIX），否则为 DOMAIN
            if domain.startswith('+'):
                cleaned_domain = domain[1:]  # 移除 + 
                converted_line = f"DOMAIN-SUFFIX,{cleaned_domain}"
            else:
                converted_line = f"DOMAIN,{domain}"
            converted_lines.append(converted_line)
    
    # 保存到文件
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(converted_lines))
    print(f"域名规则已保存至：{output_path}")

# 转换 IP 规则
def convert_ip_rules(url, output_file):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"下载失败：{url}")
        return
    
    lines = response.text.splitlines()
    converted_lines = []
    
    for line in lines:
        # 跳过空行、注释或 payload: 行
        if not line.strip() or line.startswith('#') or line.strip() == 'payload:':
            continue
        # 移除可能的 - ' 和 ' 字符，清理 IP
        cleaned_line = re.sub(r'^- \'|\'$', '', line.strip())
        # 跳过空行或无效内容
        if not cleaned_line:
            continue
        # 添加 IP-CIDR 前缀和 ,no-resolve 后缀
        converted_line = f"IP-CIDR,{cleaned_line},no-resolve"
        converted_lines.append(converted_line)
    
    # 保存到文件
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(converted_lines))
    print(f"IP 规则已保存至：{output_path}")

# 处理所有域名规则文件
for url, output_file in domain_rule_files:
    convert_domain_rules(url, output_file)

# 处理所有 IP 规则文件
for url, output_file in ip_rule_files:
    convert_ip_rules(url, output_file)

print("所有转换已完成。")
