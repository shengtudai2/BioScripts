# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author: shengtudai
@Date: 2023-03-14 14:00:00
@Description: 从输入文件中删除相似的PWM矩阵
@filename: remove_duplicate_pwm.py
"""

import os
import argparse
from scipy.stats import pearsonr


def pwm_similarity(pwm1, pwm2):
    """
    计算PWM1和PWM2之间的相似性得分（皮尔逊相关系数）

    :param pwm1: 第一个PWM矩阵，格式为嵌套列表
    :type pwm1: list[list[float]]
    :param pwm2: 第二个PWM矩阵，格式为嵌套列表
    :type pwm2: list[list[float]]
    :return: 两个PWM矩阵之间的相似性得分
    :rtype: float
    """
    if len(pwm1) != len(pwm2):  # 两个PWM矩阵的长度不同，返回0
        return 0
    n = len(pwm1)
    corr_sum = 0
    for i in range(n):
        corr, _ = pearsonr(pwm1[i], pwm2[i])
        corr_sum += corr
    return corr_sum / n


def remove_duplicate_pwm(pwm_list, threshold=0.9):
    """
    从给定的PWM矩阵列表中删除相似的PWM矩阵

    :param pwm_list: 待处理的PWM矩阵列表，格式为嵌套列表
    :type pwm_list: list[list[float]]
    :param threshold: PWM相似性的阈值，默认值为0.9
    :type threshold: float
    :return: 删除重复后的PWM矩阵列表
    :rtype: list[list[float]]
    """
    unique_pwms = []
    for i, pwm1 in enumerate(pwm_list):
        is_duplicate = False
        for pwm2 in unique_pwms:
            if pwm_similarity(pwm1, pwm2) > threshold:
                is_duplicate = True
                break
        if not is_duplicate:
            unique_pwms.append(pwm1)
    return unique_pwms


def load_motif(motif_file):
    """
    从文件中加载PWM矩阵

    :param motif_file: 包含PWM矩阵的文件路径
    :type motif_file: str
    :return: 加载出来的PWM矩阵
    :rtype: list[list[float]]
    """
    with open(motif_file, 'r') as f:
        content = f.readlines()
    pwm = []
    for line in content:
        if line.startswith('>'):
            continue
        pwm.append(list(map(float, line.split())))
    return pwm


def main(args):
    """
    主函数

    :param args: 命令行参数
    :type args: argparse.Namespace
    """
    with open(args.infile, "r") as f:
        content = []
        for line in f:
            tf_name, motif_name_str = line.strip().split("\t")
            motif_names = motif_name_str.split(",")
            # 删除不存在的PWM文件
            motif_names = [motif for motif in motif_names if os.path.exists(os.path.join(args.dir, motif + ".txt"))]

            # 如果motif_names为空，则跳过该行
            if not motif_names:
                continue

            # 加载PWM矩阵
            pwms = [load_motif(os.path.join(args.dir, motif_name + ".txt")) for motif_name in motif_names]

            # 删除相似的PWM矩阵
            unique_pwms = remove_duplicate_pwm(pwms, threshold=args.threshold)

            # 获取相应的唯一motif名称
            unique_motif_names = [motif_names[i] for i, pwm in enumerate(pwms) if pwm in unique_pwms]

            # 将TF和唯一motif名称写入输出文件中
            content.append(tf_name + "\t" + ",".join(unique_motif_names) + "\n")

        # 将输出内容写入输出文件中
        with open(args.outfile, "w") as f:
            f.writelines(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove duplicate PWMs from input file.")
    parser.add_argument("infile", help="Input file containing TF names and motif names.")
    parser.add_argument("dir", help="Directory containing PWM files.")
    parser.add_argument("--threshold", type=float, default=0.9, help="PWM similarity threshold.")
    parser.add_argument("--outfile", "-o", help="Output file to store the unique TF-motif pairs.",
                        default="TF2motif_unique.txt")
    args = parser.parse_args()

    # 输出程序开始运行信息
    print("=" * 40)
    print("Starting program...")
    print(f"Input file: {args.infile}")
    print(f"PWM directory: {args.dir}")
    print(f"PWM similarity threshold: {args.threshold}")
    print(f"Output file: {args.outfile}")
    print("=" * 40)

    # 执行主函数
    main(args)

    # 输出程序结束信息
    print("=" * 40)
    print("Program finished.")
    print("=" * 40)
