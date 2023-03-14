#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author: shengtudai
@Date: 2023-03-14 14:00:00
@Description: 从输入文件中删除不存在的PWM文件，同时将PWM文件名后缀去掉
@filename: clean_motif.py
"""

import os
import argparse


def clean_motif_file(infile, out_file, pwm_dir):
    """
    从输入文件中删除不存在的PWM文件，同时将PWM文件名后缀去掉

    :param infile: 包含TF和PWM名称的输入文件
    :type infile: str
    :param out_file: 输出文件路径
    :type out_file: str
    :param pwm_dir: 包含PWM文件的目录路径
    :type pwm_dir: str
    """
    # 获取所有PWM文件的名称
    motifs = [x.replace(".txt", "") for x in os.listdir(pwm_dir)]

    # 读取输入文件内容
    with open(infile, "r") as f:
        content = []
        for line in f:
            # 跳过空行
            if not line.strip():
                continue
            tf, motif_names = line.strip().split('\t')
            motif_names = motif_names.split(',')
            new_motif_names = []
            for motif in motif_names:
                # 如果PWM文件存在，则将PWM文件名后缀去掉，并加入新的PWM名称列表中
                if motif in motifs:
                    new_motif_names.append(motif)
            # 如果新的PWM名称列表为空，则跳过该行
            if not new_motif_names:
                continue
            # 将TF和新的PWM名称列表写入输出文件中
            content.append(f"{tf}\t{','.join(new_motif_names)}\n")

    # 将处理后的内容写入输出文件中
    with open(out_file, "w") as f:
        f.writelines(content)


if __name__ == '__main__':
    # 创建参数解析器对象
    parser = argparse.ArgumentParser(description='Clean motif file by removing non-existent PWM files and suffixes.')

    # 添加命令行参数
    parser.add_argument('infile', help='Input file containing TF names and motif names.')
    parser.add_argument('pwm_dir', help='Directory containing PWM files.')
    parser.add_argument('--outfile', '-o', help='Output file to store the cleaned TF-motif pairs.',
                        default='TF2motif_clean.txt')

    # 解析命令行参数
    args = parser.parse_args()

    # 输出程序开始运行信息
    print("=" * 40)
    print("Starting program...")
    print(f"Input file: {args.infile}")
    print(f"PWM directory: {args.pwm_dir}")
    print(f"Output file: {args.outfile}")
    print("=" * 40)

    # 执行函数
    clean_motif_file(args.infile, args.outfile, args.pwm_dir)

    # 输出程序结束信息
    print("=" * 40)
    print("Program finished.")
    print("=" * 40)
