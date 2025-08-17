import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import numpy as np
import math
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

class Page4:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.default_params = {
            "密度(水)": "1025",
            "重量(mw)": "0.02640",
            "静压(pw)": "148500",
            "数据文件": "water/w-bubble.txt"
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
            rhow = float(self.entries["密度(水)"].get())
            mw = float(self.entries["重量(mw)"].get())
            pw = float(self.entries["静压(pw)"].get())
            filename = self.entries["数据文件"].get()

            with open(filename, 'r') as infile:
                datain = infile.readlines()[8:]

            datain.pop()
            x = [float(line.split()[0]) for line in datain]
            y = [float(line.split()[1]) for line in datain]

            maximum_bubble = np.max(y)
            self.result_text_box.config(state=tk.NORMAL)
            self.result_text_box.delete(1.0, tk.END)
            self.result_text_box.insert(tk.END, f"maximum of bubble is like {maximum_bubble} cm\n")

            minima_ind = argrelextrema(np.asarray(y), np.less)
            pulse1 = x[minima_ind[0][0]]
            pulse2 = x[minima_ind[0][1]]
            pulse_Tb = (pulse2 - pulse1) / 1000
            self.result_text_box.insert(tk.END, f"pulse Tb is like {pulse_Tb}, {pulse1}, {pulse2/1000}ms\n")

            (fig, ax) = plt.subplots()
            ax.plot(x, y)
            self.result_text_box.insert(tk.END, f"index first of tuple minima:  {minima_ind[0][0]}\n")
            x_minima = minima_ind[0]
            y_minima = np.asarray(y)[minima_ind[0]]
            ax.plot(x_minima, y_minima, marker='*', linestyle='dashed', color='green', label="Minima")

            self.result_text_box.insert(tk.END, f"index of  maxima:   {np.argmax(y) / 1000}ms\n")

            tb_index = np.argmax(y)
            tb = (2.0 * tb_index + pulse2) / 2000
            enetb = tb**3 * pw**2.5 * 0.6839 / mw / rhow**1.5 * 10**(-15)
            self.result_text_box.insert(tk.END, f"cycle of tb {tb} ms\n")
            self.result_text_box.insert(tk.END, f"cycle of tb energy {enetb} MJ/kg\n")

            self.result_text_box.config(state=tk.DISABLED)

            ax.plot(np.asarray(x)[np.argmax(y)], np.max(y), marker='*', linestyle='dashed', color='orange',
                    label="peaks")
            plt.show()

        except Exception as e:
            messagebox.showerror("错误", f"错误: {e}")

    def hide(self):
        self.frame.pack_forget()

    def show(self):
        self.frame.pack()

def main():
    root = tk.Tk()
    root.title("bubble")
    root.geometry("400x550")

    page4 = Page4(root)
    root.mainloop()

if __name__ == "__main__":
    main()
