import json


def txt_to_json_basic(txt_file, json_file):
    """
    基础版本：将TXT文件的每一行转换为JSON数组中的一个元素
    """
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 去除每行的换行符，过滤空行
        data = [line.strip() for line in lines if line.strip()]

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"转换成功！共处理 {len(data)} 行数据")
        return True

    except Exception as e:
        print(f"转换失败: {e}")
        return False


# 使用示例
txt_to_json_basic('C:/Users/Tangzicheng/Desktop/chinese-GPT2-start-from-zero/data/train.txt',
                  'C:/Users/Tangzicheng/Desktop/chinese-GPT2-start-from-zero/data/input.json')