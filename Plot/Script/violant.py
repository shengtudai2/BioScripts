# 导入pandas库
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# 定义函数
def process_data(filename, im_threshold, coor_threshold, output_dir="groups"):
    # 读取文件，使用制表符分隔
    df = pd.read_csv(filename, sep="\t")
    # 按照TF列分组
    groups = df.groupby("TF")
    # 初始化三个列表，用于存储每一次统计的结果
    count_list1 = []
    count_list2 = []
    count_list3 = []
    # 遍历每一组
    for name, group in groups:
        # 统计每一组的数据个数，并添加到第一个列表中
        count1 = len(group)
        count_list1.append(count1)
        # 过滤掉IM列小于阈值的数据，并统计每一组的数据个数，并添加到第二个列表中
        group = group[group["IM"] > im_threshold]
        count2 = len(group)
        count_list2.append(count2)
        # 过滤掉Coor列小于阈值的数据，并统计每一组的数据个数，并添加到第三个列表中
        group = group[group["Coor"] > coor_threshold]
        count3 = len(group)
        count_list3.append(count3)
        # 将每一组的数据写入到指定目录下的文本文件中
        # output_path = os.path.join(output_dir, f"{name}.txt")
        # with open(output_path, "w") as f:
        #     f.write("\n".join(group["Gene"]) + "\n")
    # 返回三个列表
    return count_list1, count_list2, count_list3


# %%
if __name__ == "__main__":
    # 调用函数
    count_list1, count_list2, count_list3 = process_data("arabidopsis_net.tsv", 0.05, 0.1)
    # 打印结果
    print(count_list1)
    print(count_list2)
    print(count_list3)
    # %%
    fig = plt.figure(figsize=(8, 6))
    gs = GridSpec(2, 1, height_ratios=[4, 1], hspace=0)
    axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]
    sns.violinplot(data=[count_list1, count_list2, count_list3], ax=axes[0])
    axes[0].set_xticks([0, 1, 2])
    axes[0].set_xticklabels(["GRNBoost2", "GRNBoost2\n(IM > 0.05)", "GRNBoost2\n(IM > 0.05, Coor > 0.1)"])
    axes[0].set_ylabel("TG nums")

    table_data = [
        [f"{len(count_list1)}", f"{len(count_list2)}", f"{len(count_list3)}"],
        [f"{int(sum(count_list1) / len(count_list1))}", f"{int(sum(count_list2) / len(count_list2))}",
         f"{int(sum(count_list3) / len(count_list3))}"]
    ]

    axes[1].axis("off")

    table = axes[1].table(cellText=table_data, rowLabels=["TF nums", "AVG TGs"], loc="center", cellLoc="center",
                          edges="open", bbox=[0, -0.5, 1, 1])
    table.scale(1, 2)
    plt.show()
    fig.savefig("at_grn_IM_coor_violant.pdf", dpi=300, bbox_inches="tight")

    # --------------------------------------------------------------#
    with open("rice_regulons.tsv", "r") as f:
        lines = f.read().split("\n")
        count_list4 = [len(line.split("\t")[1].split(',')) for line in lines if line != '']
        mean = np.mean(count_list4)
        std = np.std(count_list4)
        threshold = mean + 3 * std
        count_list4 = [i for i in count_list4 if 9 < i < threshold]

    with open("rice_infer_net.tsv", "r") as f:
        lines = f.read().split("\n")
        count_list5 = [len(line.split("\t")[1].split(',')) for line in lines if line != '']
        mean = np.mean(count_list5)
        std = np.std(count_list5)
        threshold = mean + 3 * std
        count_list5 = [i for i in count_list5 if 9 < i < threshold]

    fig = plt.figure(figsize=(6, 6))
    gs = GridSpec(2, 1, height_ratios=[4, 1], hspace=0)
    axes = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]
    sns.violinplot(data=[count_list4, count_list5], ax=axes[0])
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(["TFBS Filter", "InferNet"])
    axes[0].set_ylabel("TG nums")

    table_data = [
        [f"{len(count_list4)}", f"{len(count_list5)}"],
        [f"{int(sum(count_list4) / len(count_list4))}", f"{int(sum(count_list5) / len(count_list5))}"]
    ]

    axes[1].axis("off")

    table = axes[1].table(cellText=table_data, rowLabels=["TF nums", "AVG TGs"], loc="center", cellLoc="center",
                          edges="open", bbox=[0, -0.5, 1, 1])
    table.scale(1, 2)
    plt.show()
    fig.savefig("rice_regulons_infernet_violant.pdf", dpi=300, bbox_inches="tight")

    print(count_list4)
    print(count_list5)
