import argparse
import pandas as pd
from distributed import Client, LocalCluster
from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2
from scipy.stats import spearmanr
from multiprocessing import Pool
parser = argparse.ArgumentParser(description='Compute gene regulatory network using GRNBoost2 algorithm.')
parser.add_argument('i:qn_file', type=str, help='Input expression data file path (CSV format)')
parser.add_argument('tf_file', type=str, help='Transcription factor list file path')
parser.add_argument('out_file', type=str, help='Output gene regulatory network file path (TSV format)')
args = parser.parse_args()

def calculate_spearman_correlation(args):
    geneA, geneB, expression_df = args
    x = expression_df.loc[geneA]
    y = expression_df.loc[geneB]
    corr, pvalue = spearmanr(x, y)
    return geneA, geneB, corr

if __name__ == '__main__':
    ex_matrix = pd.read_csv(args.in_file, index_col=0).T
    print(f"Loaded expression matrix: {ex_matrix.shape[1]} genes x {ex_matrix.shape[0]} samples.")
    tf_names = load_tf_names(args.tf_file)
    print(f"Loaded {len(tf_names)} transcription factors.")
    cluster = LocalCluster(n_workers=4, threads_per_worker=4, dashboard_address=':12345')
    client = Client(cluster)
    try:
        print("Computing gene regulatory network...")
        network = grnboost2(expression_data=ex_matrix, tf_names=tf_names, client_or_address=client)
    except Exception as e:
        print(f"Error during computation: {e}.")
        raise Exception("GRNBoost2 Computation Failed!")
    finally:
        client.close()
        cluster.close()
    print("GRNBoost2 compute done")
    expression_df = ex_matrix.T
    network_df = network
    network_df.columns = ['TF', 'TG', 'IM']
    print("input file load success")
    all_genes = set(network_df['TF']).union(set(network_df['TG']))
    print("all_genes load success")
    network_array = network_df.to_numpy()
    gene_pairs = network_array[:, [0, 1]]
    print("gene_paires load success")
    pool = Pool(processes=16)
    print("allocate threads")
    results = pool.map(calculate_spearman_correlation, [(TF, TG, expression_df) for TF, TG in gene_pairs])
    pool.close()
    pool.join()
    print("calculate done, saving to disk")
    results_df = pd.DataFrame(results, columns=['TF', 'TG', 'Coor'])
    df_merged = pd.merge(network, results_df, on=['TF', 'TG'])
    df_merged.to_csv(args.out_file, sep='\t', index=False)

