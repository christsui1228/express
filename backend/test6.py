import pandas as pd
import random

def generate_random_data(n=50):
    sizes = ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL']
    data = {
        'Size': [random.choice(sizes) for _ in range(n)],
        'ID': [f'ID{str(i+1).zfill(3)}' for i in range(n)]
    }
    return pd.DataFrame(data)

def sort_sizes(df):
    size_order = ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL']
    df_sorted = df.sort_values('Size', key=lambda x: pd.Categorical(x, categories=size_order, ordered=True))
    return df_sorted

# 生成随机数据
df = generate_random_data(50)

print("原始数据:")
print(df)
print("\n" + "="*50 + "\n")

# 排序
df_sorted = sort_sizes(df)

print("排序后的数据:")
print(df_sorted)