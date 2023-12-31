from Intersection import *
import pandas as pd


# 读取流量流向表，将excel文件中的数据转换为flow_dict形式
def excel_format_conversion(path):
    # 读取excel文件，将excel文件中的数据转换为字典形式
    # path: str, 流量流向的excel文件路径：列为进口道、行为出口道，行列都以东南西北命名
    # 进口道\出口道  东  南  西  北
    #          东  0   1   2   3
    #          南  4   5   6   7
    #          西  8   9   10  11
    #          北  12  13  14  15
    # 输出——flow_dict: dict, 流量流向字典
    # flow_dict = {"高新二路南进口": {"光谷一路西出口": 100,
    #                                 "光谷一路东出口": 200,
    #                                 "高新二路北出口": 300},
    #              "高新二路北进口": {"光谷一路西出口": 400,
    #                                 "光谷一路东出口": 500,
    #                                 "高新二路南出口": 600},
    #              "光谷一路西进口": {"高新二路南出口": 700,
    #                                 "高新二路北出口": 800,
    #                                 "光谷一路东出口": 900},
    #              "光谷一路东进口": {"高新二路南出口": 1000,
    #                                 "高新二路北出口": 1100,
    #                                 "光谷一路西出口": 1200}}
    df = pd.read_excel(path, index_col=0)
    # 将excel文件中的数据转换为字典形式
    flow_dict = {}
    for enter in df.index:
        flow_dict[enter + "进口"] = {}
        for exit in df.columns:
            flow_dict[enter + "进口"][exit + "出口"] = df.loc[enter, exit]
    return flow_dict


def draw(path):
    flow_dict = excel_format_conversion(path)
    intersection = intersection_factory(flow_dict)
    return intersection.draw_flow()


if __name__ == "__main__":
    path = r"display/流量流向表.xlsx"
    draw(path).show()
