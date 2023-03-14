# @Author: shengtudai
# @Date: 2023-03-14 09:30:00
# @Description: 将给定转录因子的调控基因序列和转录因子与PWM模型对应关系生成cbust所需的序列和motif文件
# @filename: cbust_seq_motif_generator.py

import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Generate sequence and motif files for cbust')
    parser.add_argument('--promoter_file', type=str, required=True, help='The path of input promoter file')
    parser.add_argument('--tf2motif_file', type=str, required=True, help='The path of input TF-to-motif file')
    return parser.parse_args()


def read_promoter_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    promoters = content.split('>')[1:]
    prmt_dict = {}
    for seq in promoters:
        t = seq.split('\n')
        t_tf = t[0].split(' ')[0]
        t_seq = ''.join(t[1:])
        prmt_dict[t_tf] = t_seq
    return prmt_dict


def read_tf2motif_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    lines = content.split('\n')
    tf2motif = [line.split('\t') for line in lines if line.strip()]
    return tf2motif


def generate_seq(tf, prmt_dict):
    if not os.path.exists("cbust_seqs"):
        os.mkdir("cbust_seqs")

    # 判断regulons/{tf}.tsv是否存在
    file_path = f"regulons/{tf}.txt"
    if not os.path.exists(file_path):
        print(f"{file_path} not exists")
        return False

    with open(file_path, "r") as f:
        gene_set = [x.replace("OS", "Os").replace("G", "g") for x in f.read().split('\n') if x != '']

    seqs = []
    for gene in gene_set:
        if gene in prmt_dict:
            seq = f">{gene}\n{prmt_dict[gene]}\n"
            seqs.append(seq)

    if seqs:
        with open(f"cbust_seqs/{tf}.fa", "w") as f:
            f.writelines(seqs)
        return True
    else:
        return False


def generate_motif(motifs):
    # 拼接多个motif文件
    if not os.path.exists("cbust_motifs"):
        os.mkdir("cbust_motifs")
    motif_files = [f"cbpwms/{motif}.txt" for motif in motifs]
    motif_content = []
    for motif_file in motif_files:
        with open(motif_file, "r") as f:
            content = f.read()
        motif_content += content.split('\n')
    motif_content = [line + '\n' for line in motif_content if line.strip()]
    return motif_content


def main(args):
    prmt_dict = read_promoter_file(args.promoter_file)
    tf2motif = read_tf2motif_file(args.tf2motif_file)

    for tf, motifs in tf2motif:
        flag = generate_seq(tf, prmt_dict)
        if flag:
            motif_content = generate_motif(motifs.split(','))
            with open(f"cbust_motifs/{tf}.cb", "w") as f:
                f.writelines(motif_content)
        else:
            print(f"No sequences generated for {tf}")


if __name__ == '__main__':
    args = parse_args()
    main(args)
