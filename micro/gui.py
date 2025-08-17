import tkinter as tk
from tkinter import messagebox, scrolledtext
import math

class Page1:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.default_params = {
            "时间": 490/1000,
            "重量百分数(c)": 45, "重量百分数(ap)": 35, "重量百分数(al)": 100 - 45 - 35,
            "半径(c)": 120, "半径(ap)": 120, "半径(al)": 13,
            "密度(c)": 2.04, "密度(ap)": 1.954, "密度(al)": 2.102,
            "接触比例(cap)": 0.1, "接触比例(cal)": 0.6, "接触比例(cc)": 1.0 - 0.1 - 0.6,
            "接触比例(apap)": 0.7, "接触比例(apal)": 1.0 - 0.7 - 0.1,
            "速率常数(cc)": 13, "速率常数(cap)": 12, "速率常数(cal)": 35,
            "速率常数(apap)": 18.0, "速率常数(apal)": 15, "速率常数(alal)": 8
        }

        self.entries = {}

        self.create_widgets_1()

    def create_widgets(self):
        # 创建输入框和标签
        labels = list(self.default_params.keys())

        self.result_text_box = scrolledtext.ScrolledText(self.frame, height=12, width=100)
        self.result_text_box.grid(row=0, column=0, pady=10, columnspan=2)
        self.result_text_box.config(state=tk.DISABLED)  # 设置为不可编辑

        # 初始没有默认值
        # for i, label_text in enumerate(labels):
        #     label = tk.Label(self.frame, text=label_text)
        #     label.grid(row=i + 1, column=0)
        #     entry = tk.Entry(self.frame)
        #     entry.grid(row=i + 1, column=1)
        #     self.entries[label_text] = entry

        # 初始有默认值
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
        default_params_button.grid(row=len(labels) + 1, column=0, padx=(0, 5), pady=20)

        # 创建按钮
        calculate_button = tk.Button(self.frame, text="计算", command=self.calculate_and_display)
        calculate_button.grid(row=len(labels) + 1, column=1, padx=(5, 0), pady=20)

    def create_widgets_1(self):
        # 创建结果显示区域
        self.result_text_box = scrolledtext.ScrolledText(self.frame, height=12, width=80)
        self.result_text_box.grid(row=0, column=0, pady=10, columnspan=4, padx=10)  # 横跨4列，增加左右边距
        self.result_text_box.config(state=tk.DISABLED)  # 设置为不可编辑

        # 获取参数列表并分成两列
        params = list(self.default_params.items())
        total_params = len(params)
        mid_index = (total_params + 1) // 2 - 1  # 确保两列数量更均衡
        column1_params = params[:mid_index]  # 第一列参数
        column2_params = params[mid_index:]  # 第二列参数

        # 第一列参数 - 标签右对齐，输入框左对齐
        for i, (key, value) in enumerate(column1_params):
            label = tk.Label(self.frame, text=key)
            label.grid(row=i + 1, column=0, padx=(5, 5), pady=5, sticky="e")  # 右对齐，增加左边距
            entry = tk.Entry(self.frame, width=20)
            entry.insert(0, value)
            entry.grid(row=i + 1, column=1, padx=(5, 5), pady=5, sticky="w")  # 左对齐
            self.entries[key] = entry

        # 第二列参数 - 标签右对齐，输入框左对齐
        for i, (key, value) in enumerate(column2_params):
            label = tk.Label(self.frame, text=key)
            label.grid(row=i + 1, column=2, padx=(5, 5), pady=5, sticky="e")  # 右对齐，增加左边距
            entry = tk.Entry(self.frame, width=20)
            entry.insert(0, value)
            entry.grid(row=i + 1, column=3, padx=(5, 5), pady=5, sticky="w")  # 左对齐
            self.entries[key] = entry

        # 确定按钮所在行（取两列中较长的一列的长度）
        button_row = max(len(column1_params), len(column2_params)) + 1

        # 设置默认参数按钮
        default_params_button = tk.Button(self.frame, text="设置默认参数", command=self.set_default_params)
        default_params_button.grid(row=button_row, column=0, columnspan=2, pady=20)

        # 计算按钮
        calculate_button = tk.Button(self.frame, text="计算", command=self.calculate_and_display)
        calculate_button.grid(row=button_row, column=2, columnspan=2, pady=20)


    def set_default_params(self):
        for key, value in self.default_params.items():
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, str(value))

    def calculate_and_display(self):
        try:
            for key in self.default_params:
                self.default_params[key] = float(self.entries[key].get())

            radius_c = self.default_params["半径(c)"]
            radius_ap = self.default_params["半径(ap)"]
            radius_al = self.default_params["半径(al)"]

            rho_c = self.default_params["密度(c)"]
            rho_ap = self.default_params["密度(ap)"]
            rho_al = self.default_params["密度(al)"]

            frac_cap = self.default_params["接触比例(cap)"]
            frac_cal = self.default_params["接触比例(cal)"]
            frac_cc = 1.0 - frac_cap - frac_cal

            frac_apap = self.default_params["接触比例(apap)"]
            frac_apal = 1.0 - frac_apap - frac_cap

            kcc = self.default_params["速率常数(cc)"]
            kcap = self.default_params["速率常数(cap)"]
            kcal = self.default_params["速率常数(cal)"]

            kapap = self.default_params["速率常数(apap)"]
            kapal = self.default_params["速率常数(apal)"]
            kalal = self.default_params["速率常数(alal)"]

            sem_c = 3.0 / (rho_c * radius_c)
            sem_ap = 3.0 / (rho_ap * radius_ap)
            sem_al = 3.0 / (rho_al * radius_al)
            print("sem", sem_c, sem_ap, sem_al)

            sum_c = sem_c / (sem_c + sem_ap + sem_al)
            sum_ap = sem_ap / (sem_c + sem_ap + sem_al)
            sum_al = sem_al / (sem_c + sem_ap + sem_al)
            print("sum", sum_c, sum_ap, sum_al)

            sem_cap = sum_c * frac_cap
            sem_cal = sum_c * frac_cal
            sem_cc = frac_cc * sum_c

            sem_apap = sum_ap * frac_apap
            sem_apal = sum_ap * abs(1.0 - frac_apap - frac_apal)
            sem_alal = sum_al * abs(1.0 - frac_cal - frac_apal)

            lambda_c = 1.0 - math.exp(- (kcc * sem_cc + kcal * sem_cal + kcap * sem_cap) * self.default_params["时间"])
            lambda_ap = 1.0 - math.exp(- (kapap * sem_apap + kapal * sem_apal + kcap * sem_cap) * self.default_params["时间"])
            lambda_al = 1.0 - math.exp(- (kcal * sem_cal + kapal * sem_apal + kalal * sem_alal) * self.default_params["时间"])

            result_text = f"sem: {sem_c}, {sem_ap}, {sem_al}\n"
            result_text += f"sum: {sum_c}, {sem_ap}, {sum_al}\n"

            result_text += f"lambda_c: {lambda_c}\nlambda_ap: {lambda_ap}\nlambda_al: {lambda_al}"
            result_text += f"\n\nsem_c: {sem_cc}, {sem_cap}, {sem_cal}\n"
            result_text += f"sem_ap: {sem_cap}, {sem_apap}, {sem_apal}\n"
            result_text += f"sem_al: {sem_cal}, {sem_alal}, {sem_apal}\n"
            result_text += f"frac_cap: {1.0 - frac_apap - frac_apal}\n"
            result_text += f"frac_alal: {1.0 - frac_cal - frac_apal}\n"

            self.result_text_box.config(state=tk.NORMAL)  # 设置为可编辑
            self.result_text_box.delete(1.0, tk.END)  # 清空文本框
            self.result_text_box.insert(tk.END, result_text)  # 插入新的结果
            self.result_text_box.config(state=tk.DISABLED)  # 设置为不可编辑

        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")

    def hide(self):
        self.frame.pack_forget()

    def show(self):
        self.frame.pack()

def main():
    root = tk.Tk()
    root.title("lamda")
    root.geometry("650x650")

    page1 = Page1(root)

    # 隐藏 page1
    page1.show()

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()
