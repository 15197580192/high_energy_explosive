import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import numpy as np
import math
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def find_roots(x, y):
    s = np.abs(np.diff(np.sign(y))).astype(bool)
    return x[:-1][s] + np.diff(x)[s] / (np.abs(y[1:][s] / y[:-1][s]) + 1)

class Page5:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.default_params = {
            "r0": "1.0",
            "密度(w)": "1025.0",
            "c(w)": "1647.0",
            "m(w)": "0.026",
            "数据文件": "water/w-p-t-1-1.0m.txt"
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

        upload_button = tk.Button(self.frame, text="上传文件", command=self.upload_file)
        upload_button.grid(row=row_counter+1, column=0, columnspan=2, pady=10)

        calculate_button = tk.Button(self.frame, text="计算", command=self.calculate_and_display)
        calculate_button.grid(row=row_counter + 2, column=0, columnspan=2, pady=10)

    def upload_file(self):
        self.entries["数据文件"].delete(0, tk.END)
        filename = filedialog.askopenfilename(title="上传数据文件", filetypes=[("Text files", "*.txt")])
        self.entries["数据文件"].insert(0, filename)

    def set_default_params(self):
        for key, value in self.default_params.items():
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)

    def calculate_and_display(self):
        try:
            r0 = float(self.entries["r0"].get())
            rho_w = float(self.entries["密度(w)"].get())
            c_w = float(self.entries["c(w)"].get())
            m_w = float(self.entries["m(w)"].get())
            filename = self.entries["数据文件"].get()

            with open(filename, 'r') as infile:
                datain = infile.readlines()[8:]

            datain.pop()
            x = [float(line.split()[0]) for line in datain]
            y = [float(line.split()[1]) for line in datain]

            y = np.asarray(y)

            y0 = np.max(y) / np.e
            z = find_roots(np.asarray(x), np.asarray(y) - y0)

            max_idx = np.argmax(y)
            max_time = x[max_idx]
            max_pressure = np.max(y) * 10 ** 5

            time_pe = z[1]
            theta = time_pe - max_time

            tau = z[0]
            idx_up = np.abs(x - (6.7 * theta + tau)).argmin()

            impulse = np.trapz(y[:idx_up + 1], x[:idx_up + 1]) * 10 ** 2

            idx_tau = np.abs(x - tau).argmin()
            impulse_tau = np.trapz(y[idx_tau:idx_up + 1], x[idx_tau:idx_up + 1]) * 10 ** 2

            coef = 4.0 * math.pi * r0 ** 2
            coef = coef / m_w / rho_w / c_w
            energy_tau = np.trapz(np.square(y[idx_tau:idx_up + 1]).tolist(), x[idx_tau:idx_up + 1])
            energy_tau = energy_tau * coef * 10 ** 10

            result_text = f"peak idx: {max_idx}\n"
            result_text += f"time of maximum pressure: {max_time} mus\n"
            result_text += f"maximum pressure: {max_pressure} MPa\n"
            result_text += f"time of P_max/e: {time_pe} mus\n"
            result_text += f"theta: {theta} mus\n"
            result_text += f"tau: {tau} mus\n"
            result_text += f"impulse: {impulse} kPa.s\n"
            result_text += f"impulse start from tau: {impulse_tau} kPa.s\n"
            result_text += f"Energy start from tau: {energy_tau} MJ/kg\n"

            self.result_text_box.config(state=tk.NORMAL)
            self.result_text_box.delete(1.0, tk.END)
            self.result_text_box.insert(tk.END, result_text)
            self.result_text_box.config(state=tk.DISABLED)

            (fig, ax) = plt.subplots()
            ax.plot(x, y)
            ax.plot(z, y0 * np.ones(len(z)), marker="o", ls="", ms=4)
            ax.axhline(y=y0, xmin=0, xmax=2000, ls='dashdot')
            ax.axvline(x=x[idx_tau], ymin=0.01, ymax=2, ls='dashdot')
            ax.axvline(x=x[idx_up], ymin=0.01, ymax=2, ls='--')
            plt.show()

        except Exception as e:
            messagebox.showerror("错误", f"错误: {e}")

    def hide(self):
        self.frame.pack_forget()

    def show(self):
        self.frame.pack()

def main():
    root = tk.Tk()
    root.title("pt_energy_temp")
    root.geometry("400x550")

    page5 = Page5(root)
    root.mainloop()

if __name__ == "__main__":
    main()
