import os
import json
from collections import Counter

def save_json(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def normalize_text(text):
    """
    规范化文本
    """
    full_width = "０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ！＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～＂"
    half_width = r"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&'" + r'()*+,-./:;<=>?@[\]^_`{|}~".'
    mapping = str.maketrans(full_width, half_width)
    return text.translate(mapping)



def create_char_vocab(data_files,
                      output_file,
                      min_freq=1):
    # 1. 统计规范化后的字符频率
    char_counts = Counter()
    for file_path in data_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
            for data in all_data:
                text = normalize_text(data['text'])
                char_counts.update(list(text))

    # 2. 过滤低频词
    frequent_chars = [char for char, count in char_counts.items() if count >= min_freq]
    
    # 3. 排序
    frequent_chars.sort()

    # 4. 添加特殊标记
    special_tokens = ["<PAD>", "<UNK>"]
    final_vocab_list = special_tokens + frequent_chars
    
    print(f"词汇表大小 (min_freq={min_freq}): {len(final_vocab_list)}")

    # 5. 保存词汇表
    save_json(final_vocab_list, output_file)
    print(f"词汇表已保存至: {output_file}")


if __name__ == '__main__':
    train_file = './data/CMeEE-V2_train.json'
    dev_file = './data/CMeEE-V2_dev.json'
    output_path = './data/vocabulary.json'
    create_char_vocab(data_files=[train_file, dev_file], output_file=output_path, min_freq=1)

