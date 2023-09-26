输入流量流向表，可以生成流量流向图，目前仅支持3或4个进口/出口道的路口，且只能画为十字形式，画图配置信息可以在config.yaml文件中更改
### 操作步骤
1. 创建流量流向表
列为进口道、行为出口道，行列都以东南西北命名
```
进口道\出口道  东  南  西  北
         东  0   1   2   3
         南  4   5   6   7
         西  8   9   10  11
         北  12  13  14  15
```
2. 读入流量流向表、画流量流向图
读流量流向表和画流量流向图的工具方法在flow_diagram.py中，并在注释中描述了各自的输入和输出数据格式
```python
path = r"display/流量流向表.xlsx"
draw_flow_diagram(excel_format_conversion(path))
```
画图结果如下：
[img](display/Figure_1.png)