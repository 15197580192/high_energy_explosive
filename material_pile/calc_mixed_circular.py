import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import math
import sys
from matplotlib.lines import Line2D  # 用于创建自定义图例条目

#GUI页面
class Page1:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.default_params = {
            # "cicular_number":"3",
            "容器长": "30",
            "容器宽": "30",
            "容器高": "30",
            "A半径": "2.00",
            "B半径(内)": "1.59",
            "C半径": "1.00",
            "A密度": "1.0",
            "B密度": "0.2",
            "C密度": "1.5",
            "A质量": "0.75",
            "B质量": "0.15",
            "C质量": "0.10",
            "A-A切点": "0.10",
            "A-B接触面积": "0.10",
            "A-C切点": "0.10",
            "C-C切点": "0.10",

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
        default_params_button.grid(row=row_counter, column=0, columnspan=1, pady=10)

        calculate_button = tk.Button(self.frame, text="材料组成", command=self.show_concentric_spheres)
        calculate_button.grid(row=row_counter, column=1, columnspan=1, pady=10)

        calculate_button = tk.Button(self.frame, text="计算", command=self.calculate_and_display)
        calculate_button.grid(row=row_counter + 1, column=0, columnspan=1, pady=10)

        save_button = tk.Button(self.frame, text="保存当前输出文本", command=self.save_result_to_file)
        save_button.grid(row=row_counter + 1, column=1, columnspan=1, pady=10)


    def set_default_params(self):
        for key, value in self.default_params.items():
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)


    def show_concentric_spheres(self):
        # 质量比例
        A_ratio = float(self.entries["A质量"].get())
        B_ratio = float(self.entries["B质量"].get())
        C_ratio = float(self.entries["C质量"].get())
        # 密度比例
        d1 = float(self.entries["A密度"].get())
        d2 = float(self.entries["B密度"].get())
        d3 = float(self.entries["C密度"].get())
        # 球体半径
        r1 = float(self.entries["A半径"].get())
        r3 = float(self.entries["C半径"].get())
        r2 = (r1 ** 3 / (A_ratio * d2 / B_ratio * d1 + 1)) ** (1 / 3)  # 计算B球体的半径，记得更新B Radius

        # 定义球体的半径和颜色
        radii = [r1, r2, r3]  # 内部球体的半径
        colors = ['red', 'green', 'blue']  # 三种材料的颜色
        alphas = [0.48, 0.5 ,0.5]  # 三种材料的颜色

        # 创建一个3D图形
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 绘制同心球体
        for r, color, alpha in zip(radii[:2], colors[:2], alphas[:2]):
            # 创建球面
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            x = r * np.outer(np.cos(u), np.sin(v))
            y = r * np.outer(np.sin(u), np.sin(v))
            z = r * np.outer(np.ones(np.size(u)), np.cos(v))

            # 去除 x > 0 且 y > 0 的部分，并处理边界,显示效果不佳
            mask = ~((x > 0) & (y < 0))
            x = np.where(mask, x, np.nan)
            y = np.where(mask, y, np.nan)
            z = np.where(mask, z, np.nan)

            # 绘制球面
            ax.plot_surface(x, y, z, color=color, alpha=alpha)

        # 绘制外部球体
        u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        xs = 0 + r3 * np.cos(u) * np.sin(v)
        ys = 0 + r3 * np.sin(u) * np.sin(v)
        zs = (r1+r3) + r3 * np.cos(v)
        ax.plot_surface(xs, ys, zs, color = 'blue', alpha = 0.5)

        # 更新r2
        self.entries["B半径(内)"].delete(0, tk.END)  # 清空文本框
        self.entries["B半径(内)"].insert(0, r2)  # 插入新的结果

        # 设置图形属性
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # 设置坐标轴范围
        ax.set_xlim([-4, 4])
        ax.set_ylim([-4, 4])
        ax.set_zlim([-4, 4])

        # 创建自定义图例条目
        legend_labels = [f'radius {r:.2f}' for r in radii]
        legend_handles = [Line2D([0], [0], color=color, lw=4, alpha=alpha) for color, alpha in zip(colors, alphas)]

        # 添加图例
        ax.legend(legend_handles, legend_labels, loc='upper right')

        # 显示图形
        plt.show()

    def calculate_and_display(self):

        # 每类球体的密度
        d1 = float(self.entries["A密度"].get())
        d2 = float(self.entries["B密度"].get())
        d3 = float(self.entries["C密度"].get())

        # 每类球体的体积按质量比例计算总数量
        A_ratio = float(self.entries["A质量"].get())
        B_ratio = float(self.entries["B质量"].get())
        C_ratio = float(self.entries["C质量"].get())

        # 盒子大小
        box_size_length = float(self.entries["容器长"].get())
        box_size_weight = float(self.entries["容器宽"].get())
        box_size_high = float(self.entries["容器高"].get())

        # 球体半径
        r1 = float(self.entries["A半径"].get())
        r3 = float(self.entries["C半径"].get())
        r2 = (r1**3/(A_ratio*d2/B_ratio*d1+1))**(1/3)   # 计算B球体的半径，记得更新B Radius

        diameter1 = 2 * r1
        diameter2 = 2 * r2
        diameter3 = 2 * r3
        try:
        # 判断小球半径的2倍是否大于盒子大小
            if diameter1 > box_size_length or diameter1 > box_size_weight or diameter1 > box_size_high:
                raise ValueError("Abnormal small ball radius: The diameter of the small ball is larger than the size of the box")

            if diameter2 > box_size_length or diameter2 > box_size_weight or diameter2 > box_size_high:
                raise ValueError("Abnormal small ball radius: The diameter of the small ball is larger than the size of the box")

            if diameter3 > box_size_length or diameter3 > box_size_weight or diameter3 > box_size_high:
                raise ValueError("Abnormal small ball radius: The diameter of the small ball is larger than the size of the box")
            if diameter2 > diameter1:
                raise ValueError("Abnormal size:B is in A, th e diameter of B must be smaller than A, please re-enter")
        except ValueError:
            # 如果发生值错误，显示错误消息框
            messagebox.showerror("Error", "Abnormal small ball radius: The diameter of the small ball is larger than the size of the box, please re-enter")
            return

        try:
            # 判断小球各个比例的多少是否超出限制
            if A_ratio > 1 or B_ratio > 1 or C_ratio > 1:
                raise ValueError("The ratio of small balls exceeds 1, please re-enter")
            if A_ratio < 0 or B_ratio < 0 or C_ratio < 0:
                raise ValueError("Small ball ratio less than 0, please re-enter")
            if A_ratio + B_ratio + C_ratio > 1:
                raise ValueError("The total proportion of small balls is greater than 1, please re-enter")
        except ValueError as e:
            error_message = str(e)
            messagebox.showerror("Error", error_message)
            return

        # 计算每类球体的体积
        total_volume = box_size_length*box_size_weight*box_size_high
        volume_per_ball_A = (4 / 3) * np.pi * r1 ** 3
        volume_per_ball_B = (4 / 3) * np.pi * r2 ** 3
        volume_per_ball_C = (4 / 3) * np.pi * r3 ** 3

        # 每类球体的体积按比例计算总数量
        total_balls = int(total_volume / ((volume_per_ball_A * A_ratio/(A_ratio+C_ratio)) + (volume_per_ball_C * C_ratio/(A_ratio+C_ratio))))

        max_balls_A = int(total_balls * A_ratio/(A_ratio+C_ratio))
        max_balls_B = max_balls_A
        max_balls_C = int(total_balls * C_ratio/(A_ratio+C_ratio))
        # max_balls_C = total_balls - max_balls_A - max_balls_B

        # 输出每类球体的数量  最大预估能放入多少球
        result_text = f"A Radius: {r1}\n"
        result_text += f"B Radius: {r2}\n"
        result_text += f"C Radius: {r3}\n"

        result_text += f"box_size_length: {box_size_length}\n"
        result_text += f"box_size_weight: {box_size_weight}\n"
        result_text += f"box_size_high: {box_size_high}\n"

        # 初始化球体位置列表
        positions = []

        # 检查两个球体是否重叠
        def is_overlapping(new_pos, existing_positions):
            for pos in existing_positions:
                dist = np.sqrt((new_pos[0] - pos[0]) ** 2 + (new_pos[1] - pos[1]) ** 2 + (new_pos[2] - pos[2]) ** 2)
                if dist < (new_pos[3] + pos[3]):
                    return True
            return False

        # 放置球体的函数
        def place_balls(num_balls, positions, label, radius, max_attempts=100000):
            count = 0
            attempts = 0
            while count < num_balls and attempts < max_attempts:
                x = np.random.uniform(radius, box_size_length - radius)
                y = np.random.uniform(radius, box_size_weight - radius)
                z = np.random.uniform(radius, box_size_high - radius)
                if not is_overlapping((x, y, z, radius), positions):
                    positions.append((x, y, z, radius, label))
                    count += 1
                attempts += 1
            return count

        # 放置各类球体 实际放入多少球
        num_A = place_balls(max_balls_A, positions, 'A', r1)
        num_B = num_A
        num_C = place_balls(max_balls_C, positions, 'C', r3)
        # 输出每类球体的数量
        result_text += f"Actual Number of A balls：{num_A}\n"
        result_text += f"Actual Number of B balls：{num_B}\n"
        result_text += f"Actual Number of C balls：{num_C}\n"

        # 每类材料的体积
        volume_per_ball_A = (4 / 3) * np.pi * (r1 ** 3 - r2 ** 3)
        total_volume = volume_per_ball_A * num_A + volume_per_ball_B * num_B + volume_per_ball_C * num_C
        result_text += f"Volume per A：{volume_per_ball_A}\n"
        result_text += f"Volume per B：{volume_per_ball_B}\n"
        result_text += f"Volume per C：{volume_per_ball_C}\n"
        result_text += f"Total volume：{total_volume}\n"

        # 计算每类球体的质量
        mass_A = num_A * volume_per_ball_A * d1
        mass_B = num_B * volume_per_ball_B * d2
        mass_C = num_C * volume_per_ball_C * d3
        # 输出每类球体的质量
        result_text += f"The mass of A balls：{mass_A}\n"
        result_text += f"The mass of B balls：{mass_B}\n"
        result_text += f"The mass of C balls：{mass_C}\n"
        # 计算总质量
        total_mass = mass_A + mass_B + mass_C

        # 输出总质量
        result_text += f"Total mass：{total_mass}\n"

        # 计算相切的球体对数量
        def count_tangent_pairs(positions):
            tangent_pairs = {
                'A-A': 0,
                'A-C': 0,
                'C-C': 0
            }
            n = len(positions)
            for i in range(n):
                for j in range(i + 1, n):
                    dist = np.sqrt((positions[i][0] - positions[j][0]) ** 2 +
                                   (positions[i][1] - positions[j][1]) ** 2 +
                                   (positions[i][2] - positions[j][2]) ** 2)
                    if np.isclose(dist, positions[i][3] + positions[j][3], atol=0.1):  # 使用一个小容差来处理浮点数比较
                        label_pair = f"{positions[i][4]}-{positions[j][4]}"
                        if label_pair in tangent_pairs:
                            tangent_pairs[label_pair] += 1
                        else:
                            label_pair = f"{positions[j][4]}-{positions[i][4]}"
                            tangent_pairs[label_pair] += 1
            return tangent_pairs

        tangent_pairs = count_tangent_pairs(positions)
        for pair, count in tangent_pairs.items():
            print(f"Number of {pair} tangent pairs: {count}")
            # 输出每类球体的相切个数
            result_text += f"Number of {pair} tangent pairs: {count}\n"


        # 每类球体的体积按比例计算总数量
        A_A_area = tangent_pairs['A-A']
        A_B_area = max_balls_A * (4 * np.pi * r2 ** 2)
        A_C_area = tangent_pairs['A-C']
        C_C_area = tangent_pairs['C-C']
        self.entries["A-A切点"].delete(0, tk.END)  # 清空文本框
        self.entries["A-A切点"].insert(0,A_A_area)  # 插入新的结果
        self.entries["A-B接触面积"].delete(0, tk.END)  # 清空文本框
        self.entries["A-B接触面积"].insert(0,A_B_area)  # 插入新的结果
        self.entries["A-C切点"].delete(0, tk.END)  # 清空文本框
        self.entries["A-C切点"].insert(0,A_C_area)  # 插入新的结果
        self.entries["C-C切点"].delete(0, tk.END)  # 清空文本框
        self.entries["C-C切点"].insert(0,C_C_area)  # 插入新的结果

        result_text += f"A-B Area: {A_B_area}\n"

        self.result_text_box.config(state=tk.NORMAL)  # 设置为可编辑
        self.result_text_box.delete(1.0, tk.END)  # 清空文本框
        self.result_text_box.insert(tk.END, result_text)  # 插入新的结果
        self.result_text_box.config(state=tk.DISABLED)  # 设置为不可编辑
        # 更新r2
        self.entries["B半径(内)"].delete(0, tk.END)  # 清空文本框
        self.entries["B半径(内)"].insert(0,r2)  # 插入新的结果


        # 绘制三维图
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 定义颜色
        colors = {'A': 'red', 'B': 'green', 'C': 'blue'}

        # 绘制球体
        for pos in positions:
            x, y, z, radius, label = pos
            u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
            xs = x + radius * np.cos(u) * np.sin(v)
            ys = y + radius * np.sin(u) * np.sin(v)
            zs = z + radius * np.cos(v)
            ax.plot_surface(xs, ys, zs, color=colors[label], alpha=0.6)

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
    root.title("mix_circular_calc")
    root.geometry("400x720")

    page1 = Page1(root)

    # 隐藏 page1
    page1.show()

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()