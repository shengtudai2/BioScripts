"""
@Author : shengtudai
@Date : 2023-03-06 09:00
@Description: 将网络坐标文件中第三列大于给定阈值t的数据按照第一列分组输出到指定目录下的多个文本文件中。
@filename : group_net_coor.py
"""

import argparse
import os
import pandas as pd


def parse_args():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description='将网络坐标文件中第三列大于给定阈值t的数据按照第一列分组输出到指定目录下的多个文本文件中。')
    parser.add_argument('net_coor_file', type=str, help='网络坐标文件路径')
    parser.add_argument('-t', '--threshold', type=float, default=0.03, help='阈值，默认为0.03')
    parser.add_argument('-d', '--dest_dir', type=str, default='groups', help='输出目录，默认为当前目录下的groups文件夹')
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.isfile(args.net_coor_file):
        print(f"Error: 文件 {args.net_coor_file} 不存在。")
        return

    df = pd.read_csv(args.net_coor_file, sep='\t', header=0)
    groups = df[df.iloc[:, 2] > args.threshold].groupby(df.columns[0])

    if not os.path.exists(args.dest_dir):
        os.makedirs(args.dest_dir)

    for group_name, group in groups:
        output_path = os.path.join(args.dest_dir, f"{group_name}.txt")
        with open(output_path, 'w') as f:
            f.write('\n'.join(group.iloc[:, 1]) + '\n')


if __name__ == '__main__':
    main()
