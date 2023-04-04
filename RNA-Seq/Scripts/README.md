### grnboost2_spearman.py
```angular2html
usage: grnboost2_spearman.py [-h] in_file tf_file out_file

Compute gene regulatory network using GRNBoost2 algorithm.

positional arguments:
  in_file     Input expression data file path (CSV format)
  tf_file     Transcription factor list file path
  out_file    Output gene regulatory network file path (TSV format)

options:
  -h, --help  show this help message and exit
```
基于GRNBoost2计算调控网络，并同时计算spearman相关系数。  
输入基因表达矩阵(行为基因，列为样本)，转录因子列表(一行一个)。
输出调控网络，四列分别为TF、Target、GRNBoost2权重、spearman相关系数。
