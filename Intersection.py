import matplotlib.pyplot as plt
import yaml


# 路口类
class Intersection:
    def __init__(self, enter_ls, exit_ls):
        # enter_ls: 入口道列表
        # exit_ls: 出口道列表
        self.enter_ls = enter_ls
        self.exit_ls = exit_ls
        self.da = 100
        self.min_width = 1  # 最小线宽
        self.max_width = 5  # 最大线宽
        self.min_head_width = 6  # 最小箭头宽度
        self.max_head_width = 10  # 最大箭头宽度
        self.flow_font_size = 12  # 流量标注字体大小
        self.color_dict = None  # 流量线段颜色字典
        self.init()

    # 从config.yaml中读取配置信息
    def init(self):
        # 打开并读取YAML文件
        with open('config.yaml', 'r', encoding="utf-8") as file:
            config = yaml.safe_load(file)
        # 读取配置信息
        self.min_width = config['lane_width']['min']  # 最小线宽
        self.max_width = config['lane_width']['max']  # 最大线宽
        self.min_head_width = config['lane_width']['min_head']  # 最小箭头宽度
        self.max_head_width = config['lane_width']['max_head']  # 最大箭头宽度
        self.flow_font_size = config['font_size']['flow']  # 流量标注字体大小
        self.color_dict = config['color']['lane']  # 流量线段颜色字典

    def draw_flow(self):
        # 设置各入口道和出口道的坐标
        self.set_point()
        # ---------------------------画流向流量图
        # 画出各流向流量
        plt.figure(figsize=(10, 10))
        for enter in self.enter_ls:
            for (exit, flow) in enter.flow_dict.items():
                # 画出流向流量：流量越大，线条越粗，相同进口道流出流量颜色相同
                if flow <= 0:
                    continue
                # 计算线宽
                width = self.__get_width(flow)
                # 判断是否使用曲线
                if enter.x != exit.x and enter.y != exit.y:
                    # 曲线
                    # rad=0.4表示曲线的弯曲程度
                    # 正值向右弯，负值向左弯
                    rad = -0.4
                    if (("北" in enter.name and "西" in exit.name) or
                            ("西" in enter.name and "南" in exit.name) or
                            ("南" in enter.name and "东" in exit.name) or
                            ("东" in enter.name and "北" in exit.name)):
                        rad *= -1
                    plt.annotate("",
                                 xy=(enter.x, enter.y),
                                 xytext=(exit.x, exit.y),
                                 size=20,
                                 arrowprops=dict(color=enter.color,
                                                 arrowstyle="-",
                                                 connectionstyle=f"arc3,rad={rad}",
                                                 linewidth=width
                                                 )
                                 )
                else:
                    # 直线
                    plt.plot([enter.x, exit.x], [enter.y, exit.y],
                             color=enter.color, linewidth=width)
        # 画入口道总流量
        for enter in self.enter_ls:
            if enter.flow == 0:
                continue
            # 计算线宽
            width = self.__get_width(enter.flow)
            plt.plot([enter.x, enter.x + enter.off[0] * 0.9],
                     [enter.y, enter.y + enter.off[1] * 0.9],
                     color=enter.color, linewidth=width)
        # 画出口道总流量
        # 计算线宽
        width = self.__get_width(self.get_flow())
        for exit in self.exit_ls:
            if exit.flow == 0:
                continue
            if width * 2 < self.min_head_width:
                head_width = self.min_head_width
            elif width * 2 > self.max_head_width:
                head_width = self.max_head_width
            else:
                head_width = width * 2
            plt.annotate('', xy=(exit.x + exit.off[0], exit.y + exit.off[1]),
                         xytext=(exit.x, exit.y),
                         arrowprops=dict(color=exit.color,
                                         width=width,
                                         headwidth=head_width))
        # ---------------------------标记文本信息
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        # 标出流向流量
        for enter in self.enter_ls:
            for (exit, flow) in enter.flow_dict.items():
                if flow > 0:
                    # 计算标注位置
                    # 1. 调头流量
                    if enter.name[0] == exit.name[0]:
                        x = 2 * enter.off[0]
                        y = 2 * enter.off[1]
                    else:
                        # 2. 非掉头流量
                        if enter.off[0] == 0:
                            y = 1 * enter.off[1]
                            if '西' in exit.name:
                                x = 0.2 * enter.off[1] * -1
                            elif '东' in exit.name:
                                x = 0.9 * enter.off[1] * -1
                            else:
                                x = 0.5 * enter.off[1] * -1
                        else:
                            x = 1 * enter.off[0]
                            if '南' in exit.name:
                                if '东' in enter.name:
                                    y = 0.2 * enter.off[0]
                                else:
                                    y = 0.9 * enter.off[0]
                            elif '北' in exit.name:
                                if '东' in enter.name:
                                    y = 0.9 * enter.off[0]
                                else:
                                    y = 0.2 * enter.off[0]
                            else:
                                y = 0.5 * enter.off[0]
                    plt.text(x, y, str(flow),
                             fontsize=self.flow_font_size)
        # 标出入口道总流量
        for enter in self.enter_ls:
            if enter.off[0] == 0:
                x = 0.5 * enter.off[1] * -1
                y = 2.5 * enter.off[1]
            else:
                x = 2.5 * enter.off[0]
                y = 0.5 * enter.off[0]
            plt.text(x, y,
                     str(enter.flow), fontsize=self.flow_font_size)
        # 标出出口道总流量
        for exit in self.exit_ls:
            if exit.off[0] == 0:
                x = 0.5 * exit.off[1]
                y = 2.5 * exit.off[1]
            else:
                x = 2.5 * exit.off[0]
                y = 0.5 * exit.off[0] * -1
            plt.text(x, y,
                     str(exit.flow), fontsize=self.flow_font_size)
        # 标出总流量
        plt.text(2.5, -2.5, f"{self.get_flow()}pcu/h", color="red", fontsize=15)
        # 隐藏坐标轴
        plt.axis('off')
        # 返回图像
        return plt

    # 计算路口总流量
    def get_flow(self):
        return sum([enter.flow for enter in self.enter_ls])

    # 计算线宽
    def __get_width(self, flow):
        width = flow / self.da
        if width < self.min_width:
            width = self.min_width
        elif width > self.max_width:
            width = self.max_width
        return width

    # 设置各入口道和出口道的坐标
    def set_point(self):
        for enter in self.enter_ls:
            if "南" in enter.name:
                enter.x = 0.5
                enter.y = -2
                enter.off = [0, -1]
                enter.color = self.color_dict["南"]
            elif "北" in enter.name:
                enter.x = -0.5
                enter.y = 2
                enter.off = [0, 1]
                enter.color = self.color_dict["北"]
            elif "西" in enter.name:
                enter.x = -2
                enter.y = -0.5
                enter.off = [-1, 0]
                enter.color = self.color_dict["西"]
            elif "东" in enter.name:
                enter.x = 2
                enter.y = 0.5
                enter.off = [1, 0]
                enter.color = self.color_dict["东"]
            else:
                throw(f"入口道名称请包含方向信息，当前入口道名称：{enter.name}")
        for exit in self.exit_ls:
            if "南" in exit.name:
                exit.x = -0.5
                exit.y = -2
                exit.off = [0, -1]
                exit.color = self.color_dict["南"]
            elif "北" in exit.name:
                exit.x = 0.5
                exit.y = 2
                exit.off = [0, 1]
                exit.color = self.color_dict["北"]
            elif "西" in exit.name:
                exit.x = -2
                exit.y = 0.5
                exit.off = [-1, 0]
                exit.color = self.color_dict["西"]
            elif "东" in exit.name:
                exit.x = 2
                exit.y = -0.5
                exit.off = [1, 0]
                exit.color = self.color_dict["东"]
            else:
                throw(f"出口道名称请包含方向信息，当前出口道名称：{exit.name}")


# 抽象点类
class Point:
    def __init__(self, name, type):
        # x, y: 坐标
        # name: 名称
        self.x = 0
        self.y = 0
        self.name = name
        self.flow = 0  # 总流量
        self.flow_dict = {}  # 与之相连的节点及对应流量
        self.type = type  # 类型
        self.color = None  # 颜色
        self.off = []  # 画该节点总流量时由节点坐标推出总流量坐标的偏移量
        self.flow = 0  # 路口总流量

    def __hash__(self):
        return hash((self.name, self.x, self.y))


# 获取路口对象的工厂方法
def intersection_factory(flow_dict, name="路口"):
    # flow_dict: 流量字典 {入口道名称: {出口道名称: 流量, ...}, ...
    # 由流量流向表创建入口道对象和出口道对象列表，并建立各入口道和出口道之间流向关系
    enter_ls = []
    exit_ls = []
    exit_name_dict = {}
    for enter_name, exit_dict in flow_dict.items():
        enter = Point(enter_name, "enter")
        enter_ls.append(enter)
        for exit_name, flow in exit_dict.items():
            if exit_name in exit_name_dict:
                exit = exit_name_dict[exit_name]
            else:
                exit = Point(exit_name, "exit")
                exit_ls.append(exit)
                exit_name_dict[exit_name] = exit
            enter.flow_dict[exit] = exit.flow_dict[enter] = flow
    # 统计各入口道和出口道的总流量
    for enter in enter_ls:
        enter.flow = sum(enter.flow_dict.values())
    for exit in exit_ls:
        exit.flow = sum(exit.flow_dict.values())
    # 创建路口对象
    intersection = Intersection(enter_ls, exit_ls)
    return intersection
