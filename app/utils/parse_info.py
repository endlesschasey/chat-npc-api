import re

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def parse_basic_info(content):
    basic_info_match = re.search(r'## 基本信息\n\n(.*?)\n\n', content, re.DOTALL)
    if basic_info_match:
        basic_info = basic_info_match.group(1)
        info_dict = {}
        for item in basic_info.strip().split('\n'):
            if ':' in item:
                key, value = item.split(':', 1)
                key = key.strip('- ').strip()  # 去掉短横和空格
                value = value.strip()
                info_dict[key] = value
        return info_dict
    return {}

def parse_personal_intro(content):
    intro_match = re.search(r'## 个人介绍\n\n(.*?)\n\n', content, re.DOTALL)
    return intro_match.group(1) if intro_match else ""

def parse_personality_traits(content):
    traits_match = re.search(r'## 性格特征\n\n(.*?)\n\n(?=##)', content, re.DOTALL)
    if traits_match:
        traits = traits_match.group(1)
        trait_dict = {}
        for trait, description in re.findall(r'### (.*?)\n\n(.*?)(?=\n\n###|\Z)', traits, re.DOTALL):
            trait_dict[trait.strip()] = description.strip()
        return trait_dict
    return {}

def parse_goal_and_background(content):
    goal_match = re.search(r'## 角色目标\n\n(.*?)\n\n', content, re.DOTALL)
    background_match = re.search(r'## 角色背景\n\n(.*?)\n\n', content, re.DOTALL)
    goal = goal_match.group(1) if goal_match else ""
    background = background_match.group(1) if background_match else ""
    return f"{goal}\n\n{background}"

def parse_dialogues(content):
    dialogues_match = re.search(r'## 台词举例\n\n(.*?)(?=\n\n##|\Z)', content, re.DOTALL)
    if dialogues_match:
        dialogues_text = dialogues_match.group(1)
        # 使用正则表达式去掉每行开头的序号和空格
        dialogues = re.findall(r'^\d+\.\s*(.*?)$', dialogues_text, re.MULTILINE)
        dialogues = [dialogue.strip() for dialogue in dialogues if dialogue.strip()]
        if not dialogues:
            print("警告：找到了台词举例部分，但没有解析出任何台词。")
        return dialogues
    else:
        print("警告：未找到台词举例部分。")
        return []

def parse_npc_file(file_path):
    content = read_markdown_file(file_path)
    
    basic_info = parse_basic_info(content)
    personal_intro = parse_personal_intro(content)
    personality_traits = parse_personality_traits(content)
    goal_and_background = parse_goal_and_background(content)
    dialogues = parse_dialogues(content)

    print("基本信息:", basic_info)
    print("\n个人介绍:", personal_intro)
    print("\n性格特征:", personality_traits)
    print("\n角色目标和背景:", goal_and_background)
    print("\n台词举例:", dialogues)

    if not dialogues:
        print("警告：未解析到任何台词。请检查文件格式是否正确。")

    return {
        "lines": dialogues,
        "goal_and_background": goal_and_background,
        "personal_intro": personal_intro,
        "personality_traits": personality_traits,
        "basic_info": basic_info
    }

if __name__ == "__main__":
    file_path = "npcs/天狐恋.md"  # 替换为你的 Markdown 文件路径
    npc_data = parse_npc_file(file_path)
    
    # 添加更详细的输出
    print("\n解析结果:")
    for key, value in npc_data.items():
        print(f"{key}: {value}")