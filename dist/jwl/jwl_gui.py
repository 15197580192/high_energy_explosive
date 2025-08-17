import tkinter as tk
from tkinter import scrolledtext
import numpy as np
import math

class Page2:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.default_params = {
            "r1": "6.88",
            "r2": "2.19",
            "omega": "0.25",
            # "gamma": "2.2",
            "rho_0": "1920",
            "pcj": "24.0",
            "dcj": "7026.0",
            "e0": "9.67"
            # "Q0": "7003.0"
        }

        self.entries = {}

        self.create_widgets()

    def create_widgets(self):
        self.result_text_box = scrolledtext.ScrolledText(self.frame, height=12, width=50)
        self.result_text_box.grid(row=0, column=0, pady=10, columnspan=2)
        self.result_text_box.config(state=tk.DISABLED)  # 设置为不可编辑

        # 创建参数输入框和标签
        row_counter = 1
        for key, value in self.default_params.items():
            label = tk.Label(self.frame, text=key)
            label.grid(row=row_counter, column=0)
            entry = tk.Entry(self.frame)
            entry.insert(0, value)
            entry.grid(row=row_counter, column=1)
            self.entries[key] = entry
            row_counter += 1

        # 设置默认参数按钮
        default_params_button = tk.Button(self.frame, text="设置默认参数", command=self.set_default_params)
        default_params_button.grid(row=row_counter, column=0, columnspan=2, pady=10)

        # 创建计算按钮
        calculate_button = tk.Button(self.frame, text="计算", command=self.calculate_and_display)
        calculate_button.grid(row=row_counter + 1, column=0, columnspan=2, pady=10)

    def set_default_params(self):
        for key, value in self.default_params.items():
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)

    def calculate_and_display(self):
        try:
            # 从输入框获取参数值
            r1 = float(self.entries["r1"].get())
            r2 = float(self.entries["r2"].get())
            omega = float(self.entries["omega"].get())
            # gamma = float(self.entries["gamma"].get())
            rho_0 = float(self.entries["rho_0"].get())
            pcj = float(self.entries["pcj"].get())
            dcj = float(self.entries["dcj"].get())
            e0 = float(self.entries["e0"].get())
            # Q0 = float(self.entries["Q0"].get())

            gamma = (rho_0 * dcj**2) * 10**(-9) / pcj - 1.0
            vcj = gamma / (gamma + 1)

            a11 = math.exp(-r1 * vcj) / r1
            a12 = math.exp(-r2 * vcj) / r2
            a13 = vcj**(-omega) / omega
            a21 = math.exp(-r1 * vcj)
            a22 = math.exp(-r2 * vcj)
            a23 = vcj**(-omega - 1)
            a31 = r1 * math.exp(-r1 * vcj)
            a32 = r2 * math.exp(-r2 * vcj)
            a33 = (omega + 1) * vcj**(-omega - 2)

            M = np.array([[a11, a12, a13], [a21, a22, a23], [a31, a32, a33]])

            y1 = e0 + 0.5 * pcj * (1 - vcj)
            y2 = pcj
            y3 = rho_0 * (dcj**2) * (10**(-9))
            Y = np.array([y1, y2, y3])

            X = np.linalg.solve(M, Y)

            result_text = f"vcj: {vcj}\nX: {X}\n"
            self.result_text_box.config(state=tk.NORMAL)
            self.result_text_box.delete(1.0, tk.END)
            self.result_text_box.insert(tk.END, result_text)
            self.result_text_box.config(state=tk.DISABLED)

        except Exception as e:
            self.result_text_box.config(state=tk.NORMAL)
            self.result_text_box.delete(1.0, tk.END)
            self.result_text_box.insert(tk.END, f"错误: {e}")
            self.result_text_box.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    root.title("jwl")
    root.geometry("400x500")

    page2 = Page2(root)
    root.mainloop()

if __name__ == "__main__":
    main()
