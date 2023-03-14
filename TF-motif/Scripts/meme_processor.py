"""
@Author : shengtudai
@Date   : 2023-03-06 15:00
@Description: 用于处理MEME文件，提取其中的Motif和pandas矩阵，并输出到指定目录下，同时生成regulons.txt文件
@filename : meme_processor.py
"""
import argparse
import os
import pandas as pd
from typing import List


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='Process MEME files.')
    parser.add_argument('input_dir', type=str, help='the directory containing .meme files')
    parser.add_argument('--output_dir', '-o', type=str, default='./', help='the directory to save output files')

    args = parser.parse_args()

    return args


def get_tf_names(input_dir: str) -> List[str]:
    """获取输入目录中所有.meme文件的文件名（不含后缀）"""
    tf_names = [os.path.splitext(file)[0] for file in os.listdir(input_dir) if file.endswith('.meme')]
    return tf_names


def process_meme_file(meme_file_path: str, output_dir: str) -> str:
    """处理单个meme文件，并返回输出文件的内容"""
    # 读取文件内容
    with open(meme_file_path, 'r') as f:
        content = f.readlines()

    # 提取motif和pandas矩阵
    motif = None
    matrix_rows = []
    for line in content:
        if line.startswith('MOTIF'):
            motif = line.split()[2]
        elif len(line.split()) == 4:
            matrix_rows.append(list(map(lambda x: float(x) * 100, line.split())))

    # 将矩阵转换为pandas数据帧
    df = pd.DataFrame(matrix_rows)

    # 构造输出文件内容
    output_content = '>' + motif + '\n' + df.to_csv(sep='\t', header=False, index=False)

    # 写入输出文件
    with open(os.path.join(output_dir, motif + '.txt'), 'w') as f:
        f.write(output_content)

    return motif


def main() -> None:
    """主函数"""
    # 解析命令行参数
    args = parse_args()

    # 获取输入目录中所有.meme文件的文件名（不含后缀）
    tf_names = get_tf_names(args.input_dir)

    regulons_content = ''
    # 处理每个.meme文件，并保存结果
    for tf_name in tf_names:
        motif = process_meme_file(os.path.join(args.input_dir, tf_name + '.meme'), args.output_dir)
        regulons_content += tf_name + '\t' + motif + '\n'

    with open('regulons.txt', 'w') as f:
        f.write(regulons_content)


if __name__ == '__main__':
    main()
