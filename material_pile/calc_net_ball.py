import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from matplotlib.lines import Line2D  # 用于创建自定义图例条目
import math
import sys

#GUI页面
class Page1:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.default_params = {
            "容器长": "10",
            "容器宽": "10",
            "容器高": "10",
            "A半径(外)": "2.00",
            "B半径(中)": "0.83",
            "C半径(内)": "0.79",
            "A密度": "1.0",
            "B密度": "0.2",
            "C密度": "1.5",
            "A质量比": "0.89",
            "B质量比": "0.01",
            "C质量比": "0.09",
            "A-A切点": "10",
            "A-B接触面积": "0.10",
            "A-C接触面积": "0.10"
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
        calculate_button.grid(row=row_counter+1, column=0, columnspan=1, pady=10)

        save_button = tk.Button(self.frame, text="保存当前输出文本", command=self.save_result_to_file)
        save_button.grid(row=row_counter+1, column=1, columnspan=1, pady=10)


    def set_default_params(self):
        for key, value in self.default_params.items():
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)

    def show_concentric_spheres(self):
        # 质量比例
        A_ratio = float(self.entries["A质量比"].get())
        B_ratio = float(self.entries["B质量比"].get())
        C_ratio = float(self.entries["C质量比"].get())

        # 密度比例
        A_density = float(self.entries["A密度"].get())
        B_density = float(self.entries["B密度"].get())
        C_density = float(self.entries["C密度"].get())

        # 求出半径
        r1 = float(self.entries["A半径(外)"].get())
        r2 = float(self.entries["B半径(中)"].get())
        r3 = float(self.entries["C半径(内)"].get())

        # 定义球体的半径和颜色
        radii = [r1,r2,r3]  # 内部球体的半径
        colors = ['red', 'blue', 'green']  # 三种材料的颜色
        alphas = [0.4, 1, 1]  # 三种材料的颜色

        # 创建一个3D图形
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 大球的球心在原点
        center1 = np.array([0, 0, 0])

        # 为了保证两个小球不相交且在大球内，选择合适的球心位置
        # 这里简单地将两个小球分别放在 x 轴正半轴和负半轴上
        center2 = np.array([(r1 - r2), 0, 0])
        center3 = np.array([-(r1 - r3), 0, 0])

        centers = [center1, center2, center3]

        # 绘制同心球体
        for r, color, alpha, center in zip(radii, colors, alphas, centers):
            # 创建球面
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            x = r * np.outer(np.cos(u), np.sin(v)) + center[0]
            y = r * np.outer(np.sin(u), np.sin(v)) + center[1]
            z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]

            # 绘制球面
            ax.plot_surface(x, y, z, color=color, alpha=alpha)

        # 更新半径
        self.entries["B半径(中)"].delete(0, tk.END)
        self.entries["B半径(中)"].insert(0, r2)

        self.entries["C半径(内)"].delete(0, tk.END)
        self.entries["C半径(内)"].insert(0, r3)

        # 设置图形属性
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # 设置坐标轴范围
        ax.set_xlim([-2.5, 2.5])
        ax.set_ylim([-2.5, 2.5])
        ax.set_zlim([-2.5, 2.5])

        # 创建自定义图例条目
        legend_labels = [f'radius {r:.2f}' for r in radii]
        legend_handles = [Line2D([0], [0], color=color, lw=4, alpha=alpha) for color, alpha in zip(colors, alphas)]

        # 添加图例
        ax.legend(legend_handles, legend_labels, loc='upper right')

        # 显示图形
        plt.show()

    def calculate_and_display(self):

        # 空间大小
        box_size_length = float(self.entries["容器长"].get())

        # 质量比例
        A_ratio = float(self.entries["A质量比"].get())
        B_ratio = float(self.entries["B质量比"].get())
        C_ratio = float(self.entries["C质量比"].get())

        # 密度比例
        A_density = float(self.entries["A密度"].get())
        B_density = float(self.entries["B密度"].get())
        C_density = float(self.entries["C密度"].get())

        # 求出半径
        r1 = float(self.entries["A半径(外)"].get())
        r2 = float(self.entries["B半径(中)"].get())
        r3 = float(self.entries["C半径(内)"].get())

        diameter1 = 2 * r1
        diameter2 = 2 * r2
        diameter3 = 2 * r3

        try:
            # 判断小球半径的2倍是否大于盒子大小
            if diameter1 > box_size_length:
                raise ValueError(
                    "Abnormal small ball radius: The diameter of the big ball is larger than the size of the box")

            if diameter2 > diameter1:
                raise ValueError(
                    "Abnormal small ball radius: The diameter of the ball B is larger than the size of the big ball")

            if diameter3 > diameter2:
                raise ValueError(
                    "Abnormal small ball radius: The diameter of the ball C is larger than the size of the big ball")

            if diameter1 < diameter2 + diameter3:
                raise ValueError(
                    "Abnormal small ball radius: The diameter of the ball A&B is larger than the size of the big ball")

        except ValueError:
            # 如果发生值错误，显示错误消息框
            messagebox.showerror("Error",
                                 "Abnormal small ball radius: The diameter of the small ball is larger than the size of the box, please re-enter")
            return

        # 计算体积
        total_volume = box_size_length*box_size_length*box_size_length
        volume_per_ball_A = (4 / 3) * np.pi * r1 ** 3


        # 每类球体的体积按比例计算总数量
        total_balls = int(total_volume / volume_per_ball_A)

        # 最多可以放入,因为球体间有空隙达不到
        max_balls_A = int(total_balls)
        result_text = f"box_size：{total_volume}\n"

        # 输出每类球体的半径
        result_text += f"radius of A：{r1}\n"
        result_text += f"radius of B：{r2}\n"
        result_text += f"radius of C：{r3}\n"

        # 质心对齐堆积（SCA）填充密度约为52%
        def calculate_centroid_aligned_positions(L, r):
            positions = []
            diameter = 2 * r  # Diameter of the sphere

            # Determine the number of spheres that can fit along each axis
            num_spheres_per_axis = int(L // diameter)

            # Create a grid of positions for the centers of the spheres
            for i in range(num_spheres_per_axis):
                for j in range(num_spheres_per_axis):
                    for k in range(num_spheres_per_axis):
                        x = i * diameter + r
                        y = j * diameter + r
                        z = k * diameter + r

                        # Ensure the spheres are within the box
                        if x + r <= L and y + r <= L and z + r <= L:
                            positions.append((x, y, z))

            return positions

        def plot_plane(ax, A, B, C, D, x_range, y_range):
            if C != 0:
                # 生成x和y的网格
                x = np.linspace(x_range[0], x_range[1], 100)
                y = np.linspace(y_range[0], y_range[1], 100)
                x, y = np.meshgrid(x, y)

                # 根据平面方程 Ax + By + Cz = D 计算z值
                z = (D - A * x - B * y) / C
            elif A != 0:
                # 生成x和y的网格
                z = np.linspace(x_range[0], x_range[1], 100)
                y = np.linspace(y_range[0], y_range[1], 100)
                z, y = np.meshgrid(z, y)

                # 根据平面方程 Ax + By + Cz = D 计算z值
                x = (D - C * z - B * y) / A
            elif B != 0:
                # 生成x和y的网格
                x = np.linspace(x_range[0], x_range[1], 100)
                z = np.linspace(y_range[0], y_range[1], 100)
                x, z = np.meshgrid(x, z)

                # 根据平面方程 Ax + By + Cz = D 计算z值
                y = (D - C * z - A * x) / B

            # 绘制平面
            ax.plot_surface(x, y, z, color='blue', alpha=0.15)

        positions = calculate_centroid_aligned_positions(box_size_length, r1)    # 默认是立方体
        positions_num = len(positions)
        # 每个球与6个网面接触
        contact_counts = int(positions_num*6)

        # 放置各类球体 实际放入多少球
        num_A = positions_num

        # 输出每类球体的数量
        result_text += f"Actual Number of A balls：{num_A}\n"
        result_text += f"Actual Number of B balls：{num_A}\n"
        result_text += f"Actual Number of C balls：{num_A}\n"

        # 计算每类材料体积
        volume_A = num_A * (4 / 3) * np.pi * (r1 ** 3 - r2 ** 3 - r3 ** 3)
        volume_B = num_A * (4 / 3) * np.pi * r2 ** 3
        volume_C = num_A * (4 / 3) * np.pi * r3 ** 3
        total_volume = num_A * (4 / 3) * np.pi * r1 ** 3
        # 输出每类球体的体积
        result_text += f"Volume of A：{volume_A}\n"
        result_text += f"Volume of B：{volume_B}\n"
        result_text += f"Volume of C：{volume_C}\n"
        result_text += f"Total volume：{total_volume}\n"
        # 计算每类材料的质量
        mass_A = num_A * (4 / 3) * np.pi * (r1 ** 3) * A_density
        mass_B = num_A * (4 / 3) * np.pi * r2 ** 3 * B_density
        mass_C = num_A * (4 / 3) * np.pi * r3 ** 3 * C_density
        A_ratio = float(mass_A / (mass_A + mass_B + mass_C))
        B_ratio = float(mass_B / (mass_A + mass_B + mass_C))
        C_ratio = float(mass_C / (mass_A + mass_B + mass_C))
        # 输出每类球体的质量
        result_text += f"The mass of A：{mass_A}\n"
        result_text += f"The mass of B：{mass_B}\n"
        result_text += f"The mass of C：{mass_C}\n"

        # 计算总质量
        total_mass = mass_A + mass_B + mass_C

        # 输出总质量
        result_text += f"Total mass：{total_mass}\n"

        # 每类球体的体积按比例计算总数量
        A_A_area = contact_counts
        A_B_area = 4 * np.pi * (r2 ** 2) * num_A
        A_C_area = 4 * np.pi * (r3 ** 2) * num_A

        result_text += f"Number of tangent points: {A_A_area}\n"
        result_text += f"ALL of area A-B pairs: {A_B_area}\n"
        print(f"ALL of area A-B pairs: {A_B_area}")
        result_text += f"ALL of area A-C pairs: {A_C_area}\n"
        print(f"ALL of area A-C pairs: {A_C_area}")

        self.result_text_box.config(state=tk.NORMAL)  # 设置为可编辑
        self.result_text_box.delete(1.0, tk.END)  # 清空文本框
        self.result_text_box.insert(tk.END, result_text)  # 插入新的结果
        self.result_text_box.config(state=tk.DISABLED)  # 设置为不可编辑

        self.entries["容器宽"].delete(0, tk.END)
        self.entries["容器宽"].insert(0, box_size_length)
        self.entries["容器高"].delete(0, tk.END)
        self.entries["容器高"].insert(0, box_size_length)
        self.entries["容器长"].delete(0, tk.END)
        self.entries["容器长"].insert(0, box_size_length)

        # 更新质量密度
        self.entries["A质量比"].delete(0, tk.END)
        self.entries["A质量比"].insert(0, A_ratio)
        self.entries["B质量比"].delete(0, tk.END)
        self.entries["B质量比"].insert(0, B_ratio)
        self.entries["C质量比"].delete(0, tk.END)
        self.entries["C质量比"].insert(0, C_ratio)

        # 更新半径
        self.entries["B半径(中)"].delete(0, tk.END)
        self.entries["B半径(中)"].insert(0, r2)

        self.entries["C半径(内)"].delete(0, tk.END)
        self.entries["C半径(内)"].insert(0, r3)

        self.entries["A-A切点"].delete(0, tk.END)
        self.entries["A-A切点"].insert(0, A_A_area)
        self.entries["A-B接触面积"].delete(0, tk.END)
        self.entries["A-B接触面积"].insert(0, A_B_area)
        self.entries["A-C接触面积"].delete(0, tk.END)
        self.entries["A-C接触面积"].insert(0, A_C_area)

        # 绘制三维图
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 定义颜色
        colors = {'A': 'red'}


        for pos in positions:
            x, y, z = pos
            # print(f"Sphere center at: x={x}, y={y}, z={z}")
            u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
            xs = x + r1 * np.cos(u) * np.sin(v)
            ys = y + r1 * np.sin(u) * np.sin(v)
            zs = z + r1 * np.cos(v)
            ax.plot_surface(xs, ys, zs, color=colors['A'], alpha=0.75)

        i=0
        while (i < box_size_length):
            plot_plane(ax, 1, 0, 0, i, [0, box_size_length], [0, box_size_length])
            plot_plane(ax, 0, 1, 0, i, [0, box_size_length], [0, box_size_length])
            plot_plane(ax, 0, 0, 1, i, [0, box_size_length], [0, box_size_length])
            i+=2*r1

        # 设置轴的范围
        ax.set_xlim([0, box_size_length])
        ax.set_ylim([0, box_size_length])
        ax.set_zlim([0, box_size_length])

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
    root.title("circular_net_ball")
    root.geometry("400x720")

    page1 = Page1(root)

    # 隐藏 page1
    page1.show()

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()