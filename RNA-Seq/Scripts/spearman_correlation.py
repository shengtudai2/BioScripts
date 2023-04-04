"""
@Author : shengtudai
@Date : 2023-03-06 12:00:00
@Description: Calculate Spearman correlation between gene pairs.
@filename : spearman_correlation.py
"""

import argparse
import pandas as pd
from scipy.stats import spearmanr
from multiprocessing import Pool

"""
python3 spearman_correlation.py -t [线程数] [msu_fpkm_expression.csv] [net_grn_output.tsv] [输出文件名]
"""


def parse_args():
    parser = argparse.ArgumentParser(description='Calculate Spearman correlation between gene pairs.')
    parser.add_argument('-t', '--threads', type=int, default=1, help='number of threads to use (default: 1)')
    parser.add_argument('expression_file', type=str, help='input gene expression matrix file')
    parser.add_argument('network_file', type=str, help='input gene network file')
    parser.add_argument('output_file', type=str, help='output file')
    args = parser.parse_args()
    return args


def read_expression_file(expression_file):
    df = pd.read_csv(expression_file, index_col=0)
    return df


def read_network_file(network_file):
    df = pd.read_csv(network_file, delimiter='\t', header=None, names=['GeneA', 'GeneB', 'Corr'])
    # Filter out low correlation gene pairs
    df = df[df['Corr'] >= 0.005]
    return df


def calculate_spearman_correlation(args):
    geneA, geneB, expression_df = args
    x = expression_df.loc[geneA]
    y = expression_df.loc[geneB]
    corr, pvalue = spearmanr(x, y)
    return geneA, geneB, corr


def main():
    args = parse_args()

    # Read input files
    expression_df = read_expression_file(args.expression_file)
    network_df = read_network_file(args.network_file)
    print("input file load success")
    # Get unique genes from the network dataframe
    all_genes = set(network_df['GeneA']).union(set(network_df['GeneB']))
    print("all_genes load success")

    # Create tuples of gene pairs for calculating Spearman correlation
    network_array = network_df.to_numpy()
    gene_pairs = network_array[:, [0, 1]]
    print("gene_paires load success")

    # Use multiprocessing to calculate Spearman correlation in parallel
    pool = Pool(processes=args.threads)
    print("allocate threads")
    results = pool.map(calculate_spearman_correlation, [(geneA, geneB, expression_df) for geneA, geneB in gene_pairs])
    pool.close()
    pool.join()

    print("calculate done, saving to disk")
    # Convert results to a dataframe and save to output file
    results_df = pd.DataFrame(results, columns=['GeneA', 'GeneB', 'Spearman_Correlation'])
    results_df.to_csv(args.output_file, sep='\t', index=False)


if __name__ == '__main__':
    main()
