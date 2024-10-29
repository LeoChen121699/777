import os
import pandas as pd
import re

info_list = ['Manufacturer / model', 'Android ID', 'Email', 'AndroidID (SHA-1)','Serial', 
             'Android ID (MD5)', 'Serial (MD5)', 'Name', 'IMEI', 'Fine-grained location', 'Coarse location', 'GPS', 'IP']
value_list = ['Google Pixel 5a', '24214e9433dc8f0d', 'ritresearch23@gmail.com',
              'b483ee136544726dadbfeac449aa8f146074379d', '17061JECB05867', 
              '997ec837e4a9865d941d587b82513e1c', '92b7fc65e009702c81501096802f8730', 
              'rit research', '357641622194041', 'Rochester', 'New York', '43.0838693,-77.6799839', '68.180.86.24']

privacy_info = dict(zip(info_list, value_list))

log_folder = "/Users/chenzhiyuan/Desktop/PhD/papers/privacy-detect/logfile"
output_folder = "output" 


if not os.path.exists(output_folder):
    os.makedirs(output_folder)

summary_data = {key: 0 for key in privacy_info.keys()}
detected_files = {key: [] for key in privacy_info.keys()} 


all_files = os.listdir(log_folder)
files = [f for f in all_files if os.path.isfile(os.path.join(log_folder, f))]
files = sorted(files, key=str.lower)


df_summary = pd.DataFrame({
    'Privacy Info': info_list,
    'Info Value': value_list,
    'Count': [0] * len(info_list),
    'Detected Files': [[] for _ in info_list]
})


def count_lines_in_files(files, output_file='log_file_line.csv'):
    file_line_counts = []
    total_lines = 0  # Initialize a variable to keep track of the total number of lines

    for log_file in files:
        file_path = os.path.join(log_folder, log_file)
        with open(file_path, 'r', errors='ignore') as file:
            line_count = sum(1 for _ in file) 
            file_line_counts.append((log_file, line_count))
            total_lines += line_count  # Add the line count to the total

    # Convert the result to a DataFrame and save it as a CSV
    df_line_counts = pd.DataFrame(file_line_counts, columns=['File Name', 'Line Count'])

    output_file_path = os.path.join(output_folder, output_file)
    df_line_counts.to_csv(output_file_path, index=False)
    print(f"Line counts have been saved to {output_file_path}")
    
    return total_lines

# Call the function and get the total number of lines
total_lines = count_lines_in_files(files)
print(f"Total lines across all files: {total_lines}")



count_lines_in_files(files)


def create_regex_list(items):
    return [re.compile(rf'\b{re.escape(item)}\b') for item in items]

def find_info(files, value_list, df_summary):
    value_regex = create_regex_list(value_list)

    for log_file in files:
        file_path = os.path.join(log_folder, log_file)
        
        with open(file_path, 'r', errors='ignore') as file:
            log_content = file.read()

            # Track which privacy info has been found in this file to count only once
            found_in_file = set()

            # Search for each privacy info item in the log content
            for key, value in privacy_info.items():
                if value in log_content and key not in found_in_file:
                    # Increment count only once per file for each privacy info
                    summary_data[key] += 1
                    found_in_file.add(key)  # Mark found 

                    detected_files[key].append(log_file)
    

    df_summary['Count'] = [summary_data[key] for key in privacy_info.keys()]
    df_summary['Detected Files'] = [detected_files[key] for key in privacy_info.keys()]


    output_file_path = os.path.join(output_folder, 'df_summary.csv')
    df_summary.to_csv(output_file_path, index=False)
    print(f"Summary has been saved to {output_file_path}")

find_info(files, value_list, df_summary)
