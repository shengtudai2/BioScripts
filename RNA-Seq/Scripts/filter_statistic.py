# 导入pandas库
import pandas as pd
import os

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
        output_path = os.path.join(output_dir, f"{name}.txt")
        with open(output_path, "w") as f:
            f.write("\n".join(group["Gene"]) + "\n")
    # 返回三个列表
    return count_list1, count_list2, count_list3


if __name__ == "__main__":
    # 调用函数
    count_list1, count_list2, count_list3 = process_data("rice_net.tsv", 0.03, 0.03)
    # 打印结果
    print(count_list1)
    print(count_list2)
    print(count_list3)
