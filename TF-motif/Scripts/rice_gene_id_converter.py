#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Description: Convert between rice reference genome RAP gene IDs and MSU gene IDs.
@Author: shengtudai
@Date: 2023-03-12 13:30:00
@filename : rice_gene_id_converter.py
"""

import argparse


def get_args():
    """获取命令行参数"""
    parser = argparse.ArgumentParser(description='Convert between rice reference genome RAP gene IDs and MSU gene IDs.')
    parser.add_argument("type", choices=["rap2msu", "msu2rap"], help='The type of ID to convert (RAP to MSU or MSU to RAP)')
    parser.add_argument("--map_file", default='RAP-MSU.txt', type=str, help='The file containing the ID mapping information')
    parser.add_argument("--input_file", required=True, type=str, help='The file containing the input gene IDs')
    return parser.parse_args()


def map_dict(map_file):
    """将对应关系储存到字典中"""
    relation_rap2msu = {}
    relation_msu2rap = {}
    with open(map_file) as f:
        for line in f:
            rap, msu = line.strip().split("\t")
            msu_gene_list = []
            if "," in msu:
                for transcript in msu.split(","):
                    gene_id = transcript.split(".")[0]
                    if gene_id not in msu_gene_list:
                        msu_gene_list.append(gene_id)
            if ("," not in msu) and (msu != "None"):
                msu_gene_list.append(msu.split(".")[0])
            if msu == "None":
                msu_gene_list.append(msu)

            # rap2msu字典
            relation_rap2msu[rap] = msu_gene_list

            # msu2rap字典
            for msu_gene in msu_gene_list:
                if msu_gene not in relation_msu2rap.keys():
                    relation_msu2rap[msu_gene] = []
                    relation_msu2rap[msu_gene].append(rap)
                if msu_gene in relation_msu2rap.keys():
                    if rap not in relation_msu2rap[msu_gene]:
                        relation_msu2rap[msu_gene].append(rap)
    return relation_rap2msu, relation_msu2rap


def convertor(gene_id, relation_dict):
    """根据提供的字典关系将基因ID转换为对应类型"""
    if gene_id in relation_dict:
        gene_id_list = relation_dict[gene_id]
        return ','.join(gene_id_list)
    else:
        return "None"


def main():
    args = get_args()
    content = []
    relation_rap2msu, relation_msu2rap = map_dict(args.map_file)
    relation_dict = relation_rap2msu if args.type == "rap2msu" else relation_msu2rap
    with open(args.input_file) as f:
        for gene_id in f:
            gene_id = gene_id.strip()
            gene_id_list = convertor(gene_id, relation_dict)
            content.append(gene_id + "\t" + gene_id_list + "\n")

    with open(f"gid_{args.type}.txt", "w") as res:
        res.writelines(content)


if __name__ == "__main__":
    main()