from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import math
import sys

# 绘制小块
def draw_box(ax, origin, size, color):
    # 提取起始坐标和尺寸
    x0, y0, z0 = origin
    length, width, height = size

    # 定义方块的顶点
    vertices = [
        [x0, y0, z0],                        # V0
        [x0 + length, y0, z0],               # V1
        [x0 + length, y0 + width, z0],      # V2
        [x0, y0 + width, z0],                # V3
        [x0, y0, z0 + height],               # V4
        [x0 + length, y0, z0 + height],     # V5
        [x0 + length, y0 + width, z0 + height], # V6
        [x0, y0 + width, z0 + height]       # V7
    ]

    # 定义方块的 6 个面
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # 底面
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # 顶面
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # 前面
        [vertices[3], vertices[2], vertices[6], vertices[7]],  # 后面
        [vertices[0], vertices[3], vertices[7], vertices[4]],  # 左面
        [vertices[1], vertices[2], vertices[6], vertices[5]]   # 右面
    ]

    # 创建多边形集合并添加到图形中
    box = Poly3DCollection(faces, color=color, edgecolor='black', alpha=1)  # alpha 设置透明度
    ax.add_collection3d(box)


#GUI页面
class Page1:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.default_params = {
            "容器长": "30",
            "容器宽": "30",
            "容器高": "30",
            "层长度":"3",
            "层宽度":"2",
            "A密度": "1.0",
            "B密度": "0.5",
            "C密度": "1.5",
            "A高": "2.00",
            "B高": "1.20",
            "C高": "0.80",
            "A质量比": "0.50",
            "B质量比": "0.30",
            "C质量比": "0.20",
            "A-B接触面积": "0.10",
            "A-C接触面积": "0.10",
            "B-C接触面积": "0.10"

        }

        self.entries = {}

        self.create_widgets()

    def create_widgets(self):
        self.result_text_box = scrolledtext.ScrolledText(self.frame, height=12, width=50)
        self.result_text_box.grid(row=0, column=0, pady=10, columnspan=2)
        self.result_text_box.config(state=tk.DISABLED)

        row_counter = 1
        for key, value in self.default_params.items():
            label = tk.Label(self.frame, text=key)
            label.grid(row=row_counter, column=0)
            entry = tk.Entry(self.frame)
            entry.insert(0, value)
            entry.grid(row=row_counter, column=1)
            self.entries[key] = entry
            row_counter += 1

        default_params_button = tk.Button(self.frame, text="设置默认参数", command=self.set_default_params)
        default_params_button.grid(row=row_counter, column=0, columnspan=2, pady=10)

        calculate_button = tk.Button(self.frame, text="计算", command=self.calculate_and_display)
        calculate_button.grid(row=row_counter + 1, column=0, columnspan=1, pady=10)

        save_button = tk.Button(self.frame, text="保存当前输出文本", command=self.save_result_to_file)
        save_button.grid(row=row_counter + 1, column=1, columnspan=1, pady=10)


    def set_default_params(self):
        for key, value in self.default_params.items():
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)

    def calculate_and_display(self):
        result_text = ""
        box_size_length = float(self.entries["容器长"].get())
        box_size_weight = float(self.entries["容器宽"].get())
        box_size_high = float(self.entries["容器高"].get())

        length = float(self.entries["层长度"].get())
        weight = float(self.entries["层宽度"].get())

        d1 = float(self.entries["A密度"].get())
        d2 = float(self.entries["B密度"].get())
        d3 = float(self.entries["C密度"].get())

        # 质量比例
        A_ratio = float(self.entries["A质量比"].get())
        B_ratio = float(self.entries["B质量比"].get())
        C_ratio = float(self.entries["C质量比"].get())

        try:
            # 判断小球各个比例的多少是否超出限制
            if A_ratio > 1 or B_ratio > 1 or C_ratio > 1:
                raise ValueError("The ratio of small boxs exceeds 1, please re-enter")
            if A_ratio < 0 or B_ratio < 0 or C_ratio < 0:
                raise ValueError("The ratio of ball box less than 0, please re-enter")
            if A_ratio + B_ratio + C_ratio > 1:
                raise ValueError("The total proportion of small box is greater than 1, please re-enter")
        except ValueError as e:
            # messagebox.showerror("Error", "Small ball ratio error, please re-enter")
            error_message = str(e)
            messagebox.showerror("Error", error_message)
            return
            # sys.exit()

        h1 = float(self.entries["A高"].get())
        h2 = h1*B_ratio/A_ratio
        h3 = h1*C_ratio/A_ratio

        high = h1 + h2 + h3
        result_text += f"容器长: {box_size_length}\n"
        result_text += f"容器宽: {box_size_weight}\n"
        result_text += f"容器高: {box_size_high}\n"
        result_text += f"层长度: {length}\n"
        result_text += f"层宽度: {weight}\n"
        result_text += f"a密度: {d1}\n"
        result_text += f"b密度: {d2}\n"
        result_text += f"c密度: {d3}\n"
        result_text += f"a高度: {h1}\n"
        result_text += f"b高度: {h2}\n"
        result_text += f"c高度: {h3}\n"
        try:
        # 判断小块是否大于盒子大小
            if length > box_size_length or weight > box_size_weight or high > box_size_high:
                raise ValueError("Abnormal length, weight or high: The diameter is larger than the size of the box")

        except ValueError:
            # 如果发生值错误，显示错误消息框
            messagebox.showerror("Error", "Abnormal length, weight or high: The diameter is larger than the size of the box, please re-enter")
            return

        # 计算每个小块的体积
        v1 = length * weight * h1
        v2 = length * weight * h2
        v3 = length * weight * h3

        # 计算每个小块的质量
        m1 = v1 * d1
        m2 = v2 * d2
        m3 = v3 * d3

        # 计算可以放置小块的个数
        x_max_num = int(box_size_length / length)
        y_max_num = int(box_size_weight / weight)
        z_max_num = int(box_size_high / high)

        cnt = 1 if int(box_size_high % high / (h1)) > 0 else 0
        z_max_num_a = int(box_size_high / high) + cnt
        cnt1 = 1 if int(box_size_high % high / (h1 + h2)) > 0 else 0
        z_max_num_b = int(box_size_high / high) + cnt1
        z_max_num_c = int(box_size_high / high)

        print(f"x_max_num: {x_max_num}")
        print(f"y_max_num: {y_max_num}")
        print(f"z_max_num_a: {z_max_num_a}")
        print(f"z_max_num_b: {z_max_num_b}")
        print(f"z_max_num_c: {z_max_num_c}")

        max_num_a = x_max_num * y_max_num * z_max_num_a
        max_num_b = x_max_num * y_max_num * z_max_num_b
        max_num_c = x_max_num * y_max_num * z_max_num_c

        total_v1 = v1 * max_num_a
        total_v2 = v2 * max_num_b
        total_v3 = v3 * max_num_c
        total_v = total_v1 + total_v2 + total_v3

        total_m1 = m1 * max_num_a
        total_m2 = m2 * max_num_b
        total_m3 = m3 * max_num_c
        total_m = total_m1 + total_m2 + total_m3

        result_text += f"a最大数目: {max_num_a}\n"
        result_text += f"b最大数目: {max_num_b}\n"
        result_text += f"c最大数目: {max_num_c}\n"
        result_text += f"a体积: {total_v1}\n"
        result_text += f"b体积: {total_v2}\n"
        result_text += f"c体积: {total_v3}\n"
        result_text += f"总体积: {total_v}\n"
        result_text += f"a质量: {total_m1}\n"
        result_text += f"b质量: {total_m2}\n"
        result_text += f"c质量: {total_m3}\n"
        result_text += f"总质量: {total_m}\n"

        # 计算每种材料的接触面积
        # s_aa = d1 * z_max_num_a * (x_max_num*length*(y_max_num+1)+y_max_num*weight*(x_max_num+1))
        # s_bb = d2 * z_max_num_b * (x_max_num*length*(y_max_num+1)+y_max_num*weight*(x_max_num+1))
        # s_cc = d3 * z_max_num_c * (x_max_num*length*(y_max_num+1)+y_max_num*weight*(x_max_num+1))

        s_ab = max_num_a * length * weight
        s_bc = max_num_b * length * weight
        s_ac = max_num_c * length * weight + x_max_num * length * y_max_num * weight

        # result_text += f"s_aa: {s_aa}\n"
        # result_text += f"s_bb: {s_bb}\n"
        # result_text += f"s_cc: {s_cc}\n"
        result_text += f"ab接触面积: {s_ab}\n"
        result_text += f"bc接触面积: {s_bc}\n"
        result_text += f"ac接触面积: {s_ac}\n"

        self.entries["B高"].delete(0, tk.END)
        self.entries["B高"].insert(0, h2)
        self.entries["C高"].delete(0, tk.END)
        self.entries["C高"].insert(0, h3)

        # self.entries["A-A Area"].delete(0, tk.END)
        # self.entries["A-A Area"].insert(0, s_aa)
        self.entries["A-B接触面积"].delete(0, tk.END)
        self.entries["A-B接触面积"].insert(0, s_ab)
        self.entries["A-C接触面积"].delete(0, tk.END)
        self.entries["A-C接触面积"].insert(0, s_ac)
        # self.entries["B-B Area"].delete(0, tk.END)
        # self.entries["B-B Area"].insert(0, s_bb)
        self.entries["B-C接触面积"].delete(0, tk.END)
        self.entries["B-C接触面积"].insert(0, s_bc)
        # self.entries["C-C Area"].delete(0, tk.END)
        # self.entries["C-C Area"].insert(0, s_cc)

        self.result_text_box.config(state=tk.NORMAL)  # 设置为可编辑
        self.result_text_box.delete(1.0, tk.END)  # 清空文本框
        self.result_text_box.insert(tk.END, result_text)  # 插入新的结果
        self.result_text_box.config(state=tk.DISABLED)  # 设置为不可编辑

        # 绘制三维图
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 计算每个小块左下角坐标，绘制所有小块
        for x in range(x_max_num):
            for y in range(y_max_num):
                for z in range(z_max_num_a):
                    draw_box(ax, origin=(x * length, y * weight, z * high), size=(length, weight, h1), color='red')
                for z in range(z_max_num_b):
                    draw_box(ax, origin=(x * length, y * weight, z * high + h1), size=(length, weight, h2), color='green')
                for z in range(z_max_num_c):
                    draw_box(ax, origin=(x * length, y * weight, z * high + h1 + h2), size=(length, weight, h3), color='blue')


        # 设置轴的范围
        ax.set_xlim([0, box_size_length])
        ax.set_ylim([0, box_size_weight])
        ax.set_zlim([0, box_size_high])

        # 设置标签
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.show()
    def save_result_to_file(self):
        # 确保文本框中的内容在尝试保存之前是最新的
        result_text = self.result_text_box.get(1.0, tk.END)

        # 弹出文件保存对话框让用户选择保存位置
        filepath = tk.filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])

        # 如果用户选择了文件路径
        if filepath:
             # 打开文件以写入
            with open(filepath, 'w') as file:
                file.write(result_text)
            print(f"结果已保存到 {filepath}")


    def show(self):
        self.frame.pack()

def main():
    root = tk.Tk()
    root.title("box_calc")
    root.geometry("400x720")

    page1 = Page1(root)

    # 隐藏 page1
    page1.show()

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()



