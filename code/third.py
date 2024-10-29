# import os
# import pandas as pd
# import re
# import json

# # Privacy information list and corresponding values
# info_list = ['Manufacturer / model', 'Android ID', 'Email', 'AndroidID (SHA-1)', 'Serial', 
#              'Android ID (MD5)', 'Serial (MD5)', 'Name', 'IMEI', 'Fine-grained location', 
#              'Coarse location', 'GPS', 'Ip address']
# value_list = ['Google Pixel 5a', '24214e9433dc8f0d', 'ritresearch23@gmail.com',
#               'b483ee136544726dadbfeac449aa8f146074379d', '17061JECB05867', 
#               '997ec837e4a9865d941d587b82513e1c', '92b7fc65e009702c81501096802f8730', 
#               'rit research', '357641622194041', 'Rochester', 'New York', 
#               '43.0838693,-77.6799839', '68.180.86.24'] 

# privacy_info = dict(zip(info_list, value_list))

# log_folder = "/Users/chenzhiyuan/Desktop/PhD/papers/privacy-detect/logfile"
# output_folder = "output"

# # Create output folder if it does not exist
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # Initialize result data structure
# summary_data = {key: 0 for key in privacy_info.keys()}
# detected_files = {key: [] for key in privacy_info.keys()} 

# all_files = os.listdir(log_folder)
# files = [f for f in all_files if os.path.isfile(os.path.join(log_folder, f))]
# files = sorted(files, key=str.lower)

# # DataFrame to save logs with privacy information
# df_privacy_logs = pd.DataFrame(columns=['File Name', 'App Name', 'Log Line', 'Privacy Info', 'Privacy Value', 'Third Party', 'Log Level'])

# # Function to create regex patterns for each value in privacy_info
# def create_regex_list(items):
#     return [re.compile(rf'\b{item}\b' if not item.startswith(r'\b') else item) for item in items]

# # Function to extract app name, removing the ".txt" suffix
# def extract_app_name(file_name):
#     return file_name.split(".txt")[0] if ".txt" in file_name else file_name

# # Function to extract third-party information and log level
# def extract_thirdparty_and_loglevel(log_line):
#     parts = log_line.split(':')
#     if len(parts) >= 3:
#         words_before_third_colon = parts[2].split()
#         if len(words_before_third_colon) > 1:
#             return words_before_third_colon[-1], words_before_third_colon[-2]
#     return '', ''

# # Function to find and log privacy-related information
# def find_info_in_lines(files, value_list, df_privacy_logs):
#     value_regex = create_regex_list(value_list)

#     for log_file in files:
#         file_path = os.path.join(log_folder, log_file)
        
#         with open(file_path, 'r', errors='ignore') as file:
#             for line_num, line in enumerate(file, 1):  # Read file line by line
#                 found_in_line = False

#                 for key, regex in zip(privacy_info.keys(), value_regex):
#                     if re.search(regex, line):  # Apply regex search
#                         # Update the count and record the file containing the privacy info
#                         summary_data[key] += 1
#                         detected_files[key].append(log_file)
#                         found_in_line = True
                        
#                         # Extract app name
#                         app_name = extract_app_name(log_file)
                        
#                         # Extract third party and log level
#                         thirdparty, log_level = extract_thirdparty_and_loglevel(line)
                        
#                         # Append the log line to DataFrame
#                         new_row = pd.DataFrame({
#                             'File Name': [log_file],
#                             'App Name': [app_name],
#                             'Log Line': [line.strip()],
#                             'Privacy Info': [key],
#                             'Privacy Value': [privacy_info[key]],
#                             'Third Party': [thirdparty],
#                             'Log Level': [log_level]
#                         })
#                         df_privacy_logs = pd.concat([df_privacy_logs, new_row], ignore_index=True)
#                         break  # Exit after first match to avoid duplicate entries in the same line

#     # Save the logs containing privacy information to a CSV file
#     output_file_path = os.path.join(output_folder, 'privacy_contain_location.csv')
#     df_privacy_logs.to_csv(output_file_path, index=False)
#     print(f"Logs containing privacy information have been saved to {output_file_path}")
    
#     return df_privacy_logs

# # Run the function to find and save logs containing privacy information
# df_privacy_logs = find_info_in_lines(files, value_list, df_privacy_logs)

# # Display the found logs
# print(df_privacy_logs)

# ====================

import os
import pandas as pd
import re

# Privacy information list and values
info_list = ['Manufacturer / model', 'Android ID', 'Email', 'AndroidID (SHA-1)', 'Serial', 
             'Android ID (MD5)', 'Serial (MD5)', 'Name', 'IMEI', 'Fine-grained location', 
             'Coarse location', 'GPS', 'IP']
value_list = ['Google Pixel 5a', '24214e9433dc8f0d', 'ritresearch23@gmail.com',
              'b483ee136544726dadbfeac449aa8f146074379d', '17061JECB05867', 
              '997ec837e4a9865d941d587b82513e1c', '92b7fc65e009702c81501096802f8730', 
              'rit research', '357641622194041', 'Rochester', 'New York', '43.0838693,-77.6799839', '68.180.86.24']

privacy_info = dict(zip(info_list, value_list))

log_folder = "/Users/chenzhiyuan/Desktop/PhD/papers/privacy-detect/logfile"
output_folder = "output"

# Create output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# DataFrame to save all logs containing privacy information
df_privacy_logs = pd.DataFrame(columns=['File Name', 'App Name', 'Log Line', 'Privacy Info', 'Privacy Value', 'Third Party', 'Log Level'])

# Function to extract app name, removing the ".txt" suffix
def extract_app_name(file_name):
    return file_name.split(".txt")[0] if ".txt" in file_name else file_name

# Function to extract third-party and log level information
def extract_thirdparty_and_loglevel(log_line):
    parts = log_line.split(':')
    if len(parts) >= 3:
        words = parts[2].split()
        return words[-1] if words else '', words[-2] if len(words) > 1 else ''
    return '', ''

# Function to find and log all lines containing privacy information
def find_info_in_lines(files, privacy_info, df_privacy_logs):
    for log_file in files:
        file_path = os.path.join(log_folder, log_file)
        
        with open(file_path, 'r', encoding='utf-8-sig',errors='ignore') as file:
            for line in file:
                # Search for each privacy info item in each line
                for key, value in privacy_info.items():
                    if value in line:
                        # Extract app name and third party/log level info for each matching line
                        app_name = extract_app_name(log_file)
                        thirdparty, log_level = extract_thirdparty_and_loglevel(line)
                        
                        new_row = pd.DataFrame({
                            'File Name': [log_file],
                            'App Name': [app_name],
                            'Log Line': [line.strip()],
                            'Privacy Info': [key],
                            'Privacy Value': [value],
                            'Third Party': [thirdparty],
                            'Log Level': [log_level]
                        })
                        df_privacy_logs = pd.concat([df_privacy_logs, new_row], ignore_index=True)

    # Save results to CSV
    output_file_path = os.path.join(output_folder, 'privacy_all_logs2.csv')
    df_privacy_logs.to_csv(output_file_path, index=False)
    print(f"All logs containing privacy information have been saved to {output_file_path}")
    
    return df_privacy_logs

# Execute the function to find and log all lines containing privacy values
all_files = os.listdir(log_folder)
files = [f for f in all_files if os.path.isfile(os.path.join(log_folder, f))]
df_privacy_logs = find_info_in_lines(files, privacy_info, df_privacy_logs)

# Display the found logs
print(df_privacy_logs)







# ====================




# import os
# import pandas as pd
# import re

# # 隐私信息列表和对应的值
# info_list = ['Manufacturer / model', 'Android ID', 'Email', 'AndroidID (SHA-1)','Serial', 
#              'Android ID (MD5)', 'Serial (MD5)', 'Name', 'IMEI', 'Fine-grained location', 'Coarse location', 'GPS', 'Ip address']
# value_list = ['Google Pixel 5a', '24214e9433dc8f0d', 'ritresearch23@gmail.com',
#               'b483ee136544726dadbfeac449aa8f146074379d', '17061JECB05867', 
#               '997ec837e4a9865d941d587b82513e1c', '92b7fc65e009702c81501096802f8730', 
#               'rit research', '357641622194041', 'Rochester', 'New York', '43.0838693,-77.6799839', '68.180.86.24']

# privacy_info = dict(zip(info_list, value_list))

# log_folder = "/Users/chenzhiyuan/Desktop/PhD/papers/privacy-detect/logfile"
# output_folder = "output"

# # 如果输出文件夹不存在则创建
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # 初始化结果数据结构
# summary_data = {key: 0 for key in privacy_info.keys()}
# detected_files = {key: [] for key in privacy_info.keys()} 

# all_files = os.listdir(log_folder)
# files = [f for f in all_files if os.path.isfile(os.path.join(log_folder, f))]
# files = sorted(files, key=str.lower)

# # 创建保存包含隐私信息的日志行的表格
# df_privacy_logs = pd.DataFrame(columns=['File Name', 'App Name', 'Log Line', 'Privacy Info', 'Privacy Value', 'Third Party', 'Log Level'])

# # 用于创建正则表达式的函数
# def create_regex_list(items):
#     return [re.compile(rf'\b{re.escape(item)}\b') for item in items]

# # 提取 app name 的函数，提取 .txt 前的内容，如果没有 .txt，则返回整个文件名
# def extract_app_name(file_name):
#     if ".txt" in file_name:
#         return file_name.split(".txt")[0]  # 只提取 .txt 前面的内容
#     return file_name  # 如果不包含 .txt，则返回整个文件名

# # 提取 thirdparty 和 log level 的函数
# def extract_thirdparty_and_loglevel(log_line):
#     parts = log_line.split(':')
    
#     if len(parts) >= 3:
#         # thirdparty = parts[2].split()[0]  # 第三个 ':' 前面的第一个词
#         words_before_third_colon = parts[2].split()
#         if len(words_before_third_colon) > 0:
#             thirdparty = words_before_third_colon[-1]  # 第三个 ':' 前的倒数第一个词
#             log_level = words_before_third_colon[-2]  # 第三个 ':' 前的倒数第二个词
            
#         else:
#             thirdparty = ''
#             log_level = ''
        
#         # if len(words_before_third_colon) > 1:
#         #     log_level = words_before_third_colon[-2]  # 第三个 ':' 前的倒数第二个词
#         # else:
#         #     log_level = ''
#     else:
#         thirdparty = ''
#         log_level = ''
    
#     return thirdparty, log_level

# # 查找包含隐私信息的行，并记录日志行及文件名
# def find_info_in_lines(files, value_list, df_privacy_logs):
#     value_regex = create_regex_list(value_list)

#     for log_file in files:
#         file_path = os.path.join(log_folder, log_file)
        
#         with open(file_path, 'r', errors='ignore') as file:
#             for line_num, line in enumerate(file, 1):  # 按行读取文件
#                 found_in_line = False  # 标记该行是否包含隐私信息

#                 # 搜索每个隐私信息
#                 for key, value in privacy_info.items():
#                     if value in line:
#                         # 增加找到的隐私信息的计数
#                         summary_data[key] += 1
#                         detected_files[key].append(log_file)
#                         found_in_line = True  # 标记已找到
                        
#                         # 提取 app name
#                         app_name = extract_app_name(log_file)
                        
#                         # 提取 thirdparty 和 log level
#                         thirdparty, log_level = extract_thirdparty_and_loglevel(line)
                        
#                         # 将包含隐私信息的行记录到DataFrame
#                         new_row = pd.DataFrame({
#                             'File Name': [log_file],
#                             'App Name': [app_name],
#                             'Log Line': [line.strip()],
#                             'Privacy Info': [key],
#                             'Privacy Value': [value],
#                             'Third Party': [thirdparty],
#                             'Log Level': [log_level]
#                         })

#                         # 使用 pd.concat 替代 append
#                         df_privacy_logs = pd.concat([df_privacy_logs, new_row], ignore_index=True)
#                         break  # 只记录第一个找到的隐私信息即可，避免重复计数

#     # 保存包含隐私信息的日志行到CSV文件
#     # output_file_path = os.path.join(output_folder, 'privacy.csv')
#     output_file_path = os.path.join(output_folder, 'privacy_contain_location.csv')
#     df_privacy_logs.to_csv(output_file_path, index=False)
#     print(f"包含隐私信息的日志已保存到 {output_file_path}")
    
#     return df_privacy_logs

# # 调用函数，查找并保存包含隐私信息的日志行
# df_privacy_logs = find_info_in_lines(files, value_list, df_privacy_logs)

# # 显示找到的日志行
# print(df_privacy_logs)
