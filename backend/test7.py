import pandas as pd
import re
from pypinyin import lazy_pinyin, Style

# 定义尺码排序顺序
size_order = ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL']

def is_chinese(char):
    return '\u4e00' <= char <= '\u9fff'

def contains_chinese(text):
    return any(is_chinese(char) for char in text)

def process_name(name):
    # 如果名字不包含中文，则直接返回
    if not contains_chinese(name):
        return name

    # 移除点并替换为空格
    name = name.replace('.', ' ')
    
    # 使用lazy_pinyin处理整个名字
    pinyins = lazy_pinyin(name, style=Style.NORMAL)
    
    # 将每个部分的首字母大写
    processed_name = ' '.join([p.capitalize() for p in pinyins])
    
    return processed_name

def clean_size(size):
    if not isinstance(size, str):
        return size
    # 转换为大写
    size = size.upper()
    # 将XXL, XXXL等转换为2XL, 3XL等
    match = re.match(r'X{2,}L', size)
    if match:
        x_count = len(match.group()) - 1  # 减去'L'
        return f'{x_count}XL'
    return size

# 读取Excel文件
file_path = '/home/chris/size/test1.xls'
df = pd.read_excel(file_path)

# 确保列名正确
df.columns = ['姓名', '尺码']

# 处理姓名
df['处理后的姓名'] = df['姓名'].apply(process_name)

# 处理尺码
df['尺码'] = df['尺码'].apply(clean_size)

# 根据定义的顺序排序
size_order_dict = {size: index for index, size in enumerate(size_order)}
df['尺码顺序'] = df['尺码'].map(size_order_dict)
df = df.sort_values('尺码顺序')

# 删除辅助排序列
df = df.drop('尺码顺序', axis=1)

# 显示结果
print(df)

# 保存结果（如果需要）
# df.to_excel('/home/chris/size/processed_and_sorted_test1.xlsx', index=False)