import sys
import os
import glob
import json
import re

def parse_input(input_str):
    """Parse the input string to extract configuration parts."""
    configs = input_str.split(';')
    return configs

def list_files(config_str):
    """List files based on the directory and wildcards provided."""
    
    # 检查 config_str 是否为空
    if not config_str or config_str.strip() == '':
        #print(f"Empty config_str: {config_str}. Loading default configuration.")
        return {
            "files": [],  # 返回空文件列表或设置默认行为
            "type": 'row',
            "ranges": [],
            "label_mode": 0,
            "skip_head": 1
        }
    
    parts = config_str.split(',')
    
    # 检查分割后的列表长度是否足够
    if len(parts) < 3:
        raise ValueError(f"Invalid config_str: '{config_str}'. Expected at least 3 comma-separated values.")
    
    files = sorted(glob.glob(parts[0].strip()))  # 文件排序
    ranges = parse_range(parts[2].strip())

    return {
        "files": files,
        "type": parse_range_type(parts[1].strip()),
        "ranges": ranges,
        "label_mode": int(parts[3].strip()) if len(parts) > 3 else 0,  # 如果不足4个值，默认label_mode为0
        "skip_head": int(parts[4].strip()) if len(parts) > 4 else 1  # 默认跳过1行
    }


def parse_range(range_str):
    """Parse range string like [1:20], [1.2.3], [:3], [0:], or [] into a list of integers."""
    range_list = []

    if range_str == '[]' or not range_str:
        return range_list  # 返回空列表，避免解析错误

    parts = range_str.strip("[]").split('.')

    for part in parts:
        if ':' in part:
            start, end = part.split(':')
            start = int(start) if start else 0
            end = int(end) if end else None
            range_list.extend(list(range(start, end + 1 if end is not None else None)))
        elif part:
            range_list.append(int(part))

    return range_list


def parse_range_type(type_str):
    """Parse type string to handle row and column correctly."""
    if type_str in ['c', 'col', 'column']:
        return 'column'
    elif type_str in ['r', 'row']:
        return 'row'
    else:
        return type_str

def determine_range_for_file(file_path, file_type):
    """Determine the range for a file if not specified."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if file_type == 'column':
            max_cols = max(len(line.split()) for line in lines)
            return list(range(max_cols))
        elif file_type == 'row':
            return list(range(len(lines)))
    return []

def read_file(config, title_counter):
    """Read the specified file(s) based on configuration."""
    all_titles = []
    all_contents = []
    file_ranges = []

    # 加载 JSON 文件
    with open("infile.json", "r") as file:
        data = json.load(file)

    for file_path in config["files"]:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # 如果文件内容为空，跳过该文件
            if not lines:
                continue

            # 如果 ranges 为空，则自动确定
            if not config["ranges"]:
                file_ranges = determine_range_for_file(file_path, config["type"])
            else:
                file_ranges = config["ranges"]

            for idx in file_ranges:
                # 处理标题部分
                if config["label_mode"] == 0:
                    if config["type"] == 'column':
                        if len(lines) > 0 and len(lines[0].split()) > idx:
                            title = lines[0].split()[idx]
                        else:
                            title = "unknown"
                    elif config["type"] == 'row':
                        if len(lines) > idx:
                            title = lines[idx].split()[0]
                        else:
                            title = "unknown"
                elif config["label_mode"] == 1:
                    title = os.path.basename(file_path)
                elif config["label_mode"] == 2:
                    title_key = f"title_{title_counter}"
                    print(f"Trying to extract title with key {title_key} from {file_path}")

                    # 从 JSON 中提取标题
                    if title_key in data.get("titles", {}):
                        title = data["titles"][title_key]
                        print(f"Extracted title '{title}' for key {title_key} from JSON")
                    else:
                        title = "unknown"
                        print(f"Title '{title_key}' not found in json_titles")

                all_titles.append(title)
                title_counter += 1  # 更新计数器

                # 处理内容部分
                if config["type"] == 'column':
                    if len(lines[0].split()) > idx:
                        column_data = [line.split()[idx] for line in lines[config["skip_head"]:] if len(line.split()) > idx]
                        all_contents.append(column_data)
                    else:
                        all_contents.append([])

                elif config["type"] == 'row':
                    if len(lines) > idx:
                        row_data = lines[idx].split()
                        all_contents.append(row_data[config["skip_head"]:])
                    else:
                        all_contents.append([])

    return all_titles, all_contents, title_counter


def write_to_json(config_data, titles, filename='infile.json'):
    """Write configuration data to a JSON file, including write_text settings."""
    output_data = config_data.copy()
    # 将 titles 作为一级项目写入，并为每个 title 赋予唯一的索引，从 0 开始计数
    title_index = {f"title_{i}": title for i, title in enumerate(titles)}
    output_data["titles"] = title_index
    with open(filename, 'w') as f:
        json.dump(output_data, f, indent=4)


def write_to_text(titles, contents, config):
    """Write titles and contents to a text file based on config settings."""
    filename = config.get('name', 'infile.dat')
    write_type = config.get('type', 'row')

    # 计算列宽，选择16和最长标题的较大值
    max_title_length = max(len(title) for title in titles)
    col_width = max(16, max_title_length)

    with open(filename, 'w') as f:
        if write_type == 'row':
            for title, content in zip(titles, contents):
                f.write(f"{title:<{col_width}} " + " ".join(content) + "\n")
        elif write_type == 'column':
            max_len = max(len(contents[i]) for i in range(len(contents)))
            f.write(' '.join([f"{title:<{col_width}}" for title in titles]) + '\n')
            for i in range(max_len):
                row = []
                for j, content in enumerate(contents):
                    if i < len(content):
                        row.append(f"{content[i]:<{col_width}}")
                    else:
                        row.append(" " * col_width)
                f.write(' '.join(row) + '\n')

def parse_additional_options(config_str):
    """Parse additional options like txt, name, and type."""
    options = {
        "txt": "off",
        "name": "infile.dat",
        "type": "row"
    }
    for config in config_str:
        if '=' in config:
            key, value = config.split('=')
            options[key.strip()] = value.strip()

    # 将简写自动转换为全称
    if options['type'] in ['r', 'row']:
        options['type'] = 'row'
    elif options['type'] in ['c', 'col', 'column']:
        options['type'] = 'column'

    return options

def load_from_json(json_file='infile.json'):
    """Load configuration data from a JSON file."""
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)
    else:
        print(f"Error: {json_file} not found and no command-line arguments provided.")
        sys.exit(1)

def main(config_str=None):
    """Main function to process the configuration string and read files."""
    title_counter = 0  # 初始化计数器
    all_titles = []  # 初始化空列表
    all_contents = []  # 初始化空列表
    
    # 检查 config_str 是否为空或只包含引号
    if not config_str or config_str.strip() == "''":
        #print(f"config_str is empty or invalid ('{config_str}'), loading default from config file or infile.json.")
        config_data = load_from_json()  # 从 infile.json 加载

        # 读取文件并写入内容
        for config in config_data.values():
            if isinstance(config, dict) and "files" in config:
                titles, contents, title_counter = read_file(config, title_counter)
                all_titles.extend(titles)
                all_contents.extend(contents)
    else:
        config_data = {}
        additional_options = parse_additional_options(config_str.split(';'))
        configs = [config for config in config_str.split(';') if '=' not in config]

        for i, config in enumerate(configs):
            config_key = f"configuration[{i+1}]"
            file_data = list_files(config.strip())
            config_data[config_key] = file_data

            # 读取文件，获取标题和内容，并更新计数器
            titles, contents, title_counter = read_file(file_data, title_counter)
            all_titles.extend(titles)
            all_contents.extend(contents)

        # 将写入文本的配置加入 JSON 文件
        config_data["write_text"] = additional_options

        # Write the configuration data and titles to a JSON file
        write_to_json(config_data, all_titles)

    # Write to infile.dat if txt is on
    if config_data.get("write_text", {}).get('txt') == 'on':
        write_to_text(all_titles, all_contents, config_data.get("write_text", {}))

    return all_titles, all_contents


if __name__ == "__main__":
    config_str = sys.argv[1] if len(sys.argv) > 1 else None
    titles, contents = main(config_str)
    print("Titles:", titles)
    #print("Contents:", contents)

