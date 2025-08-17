import tkinter as tk
from tkinter import messagebox, scrolledtext
import math

def calculate_and_display():
    try:
        time = float(entries["time"].get())
        mw_c = float(entries["mw_c"].get())
        mw_ap = float(entries["mw_ap"].get())
        mw_al = 100 - mw_c - mw_ap

        radius_c = float(entries["radius_c"].get())
        radius_ap = float(entries["radius_ap"].get())
        radius_al = float(entries["radius_al"].get())

        rho_c = float(entries["rho_c"].get())
        rho_ap = float(entries["rho_ap"].get())
        rho_al = float(entries["rho_al"].get())

        frac_cap = float(entries["frac_cap"].get())
        frac_cal = float(entries["frac_cal"].get())
        frac_cc = 1.0 - frac_cap - frac_cal

        frac_apap = float(entries["frac_apap"].get())
        frac_apal = 1.0 - frac_apap - frac_cap

        kcc = float(entries["kcc"].get())
        kcap = float(entries["kcap"].get())
        kcal = float(entries["kcal"].get())

        kapap = float(entries["kapap"].get())
        kapal = float(entries["kapal"].get())
        kalal = float(entries["kalal"].get())

        sem_c = 0.0
        sem_ap = 0.0
        sem_al = 0.0

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

        print("sem_c", sem_cc, sem_cap, sem_cal)
        print("sem_ap", sem_cap, sem_apap, sem_apal)
        print("sem_al", sem_cal, sem_alal, sem_apal)
        print("frac_cap", 1.0 - frac_apap - frac_apal)
        print("frac_alal", 1.0 - frac_cal - frac_apal)

        lambda_c = 1.0 - math.exp(- (kcc * sem_cc + kcal * sem_cal + kcap * sem_cap) * time)
        lambda_ap = 1.0 - math.exp(- (kapap * sem_apap + kapal * sem_apal + kcap * sem_cap) * time)
        lambda_al = 1.0 - math.exp(- (kcal * sem_cal + kapal * sem_apal + kalal * sem_alal) * time)

        result_text = f"lambda_c: {lambda_c}\nlambda_ap: {lambda_ap}\nlambda_al: {lambda_al}"
        result_text_box.config(state=tk.NORMAL)  # 设置为可编辑
        result_text_box.delete(1.0, tk.END)  # 清空文本框
        result_text_box.insert(tk.END, result_text)  # 插入新的结果
        result_text_box.config(state=tk.DISABLED)  # 设置为不可编辑

    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

# 创建主窗口
root = tk.Tk()
root.title("Tkinter 模拟化学过程")

# 创建滚动条
scrollbar = tk.Scrollbar(root, orient="vertical")

# 创建Canvas
canvas = tk.Canvas(root, yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)

# 创建Frame
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# 连接滚动条与Canvas
scrollbar.config(command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# 创建输入框和标签
labels = ["time", "mw_c", "mw_ap", "radius_c", "radius_ap", "radius_al",
          "rho_c", "rho_ap", "rho_al", "frac_cap", "frac_cal", "frac_apap",
          "frac_apal", "kcc", "kcap", "kcal", "kapap", "kapal", "kalal"]

entries = {}

# 创建滚动文本框
result_text_box = scrolledtext.ScrolledText(frame, height=10, width=50)
result_text_box.grid(row=0, column=0, pady=10, columnspan=2)
result_text_box.config(state=tk.DISABLED)  # 设置为不可编辑

for i, label_text in enumerate(labels):
    label = tk.Label(frame, text=label_text)
    label.grid(row=i + 1, column=0)
    entry = tk.Entry(frame)
    entry.grid(row=i + 1, column=1)
    entries[label_text] = entry

# 创建按钮
calculate_button = tk.Button(frame, text="计算", command=calculate_and_display)
calculate_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

# 配置Canvas的滚动区域
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# 运行主循环
root.mainloop()
