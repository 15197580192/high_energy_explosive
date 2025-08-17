import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def find_roots(x, y):
    s = np.abs(np.diff(np.sign(y))).astype(bool)
    return x[:-1][s] + np.diff(x)[s] / (np.abs(y[1:][s] / y[:-1][s]) + 1)

class Page6:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.default_params = {
            "mass_of_the_container":"77.409",
            "mass_of_the_explosive":"40.841",
            "filename_expansion": "yt/yt-rx-t.txt",
            "filename_velocity": "yt/yt-rx-t.txt",
            "y0": "1.9"
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

        upload_expansion_button = tk.Button(self.frame, text="upload expansion", command=self.upload_expansion_file)
        upload_expansion_button.grid(row=row_counter + 1, column=0, columnspan=1, pady=10)

        upload_velocity_button = tk.Button(self.frame, text="upload velocity", command=self.upload_velocity_file)
        upload_velocity_button.grid(row=row_counter + 1, column=1, columnspan=1, pady=10)

        calculate_button = tk.Button(self.frame, text="计算", command=self.calculate_and_display)
        calculate_button.grid(row=row_counter + 2, column=0, columnspan=2, pady=10)

    def upload_expansion_file(self):
        self.entries["filename_expansion"].delete(0, tk.END)
        filename = filedialog.askopenfilename(title="上传扩张数据文件", filetypes=[("Text files", "*.txt")])
        self.entries["filename_expansion"].insert(0, filename)

    def upload_velocity_file(self):
        self.entries["filename_velocity"].delete(0, tk.END)
        filename = filedialog.askopenfilename(title="上传速度数据文件", filetypes=[("Text files", "*.txt")])
        self.entries["filename_velocity"].insert(0, filename)

    def set_default_params(self):
        for key, value in self.default_params.items():
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)

    def calculate_and_display(self):
        try:
            filename_expansion = self.entries["filename_expansion"].get()
            filename_velocity = self.entries["filename_velocity"].get()
            y0 = float(self.entries["y0"].get())

            with open(filename_expansion, 'r') as infile:
                datain = infile.readlines()[8:]
                datain.pop()
                x_expansion = [float(line.split()[0]) for line in datain]
                y_expansion = [float(line.split()[1]) for line in datain]

            with open(filename_velocity, 'r') as infile:
                datavin = infile.readlines()[8:]
                datavin.pop()
                x_velocity = [float(line.split()[0]) for line in datavin]
                y_velocity = [float(line.split()[1]) for line in datavin]

            y0_expansion = float(y0)
            z_expansion = find_roots(np.asarray(x_expansion), np.asarray(y_expansion) - y0_expansion)
            time_expansion = z_expansion[0]

            interp_func = interp1d(x_velocity, y_velocity)
            velocity = interp_func(time_expansion)

            m1 = float(self.entries["mass_of_the_container"].get())  # mass of the container
            m2 = float(self.entries["mass_of_the_explosive"].get())  # mass of the explosive
            e_gurney = (1 / 2 + m1 / m2) * (velocity ** 2) / 2
            gurney_p = (2 * e_gurney) ** 0.5

            result_text = f"time of this expansion: {time_expansion}\n"
            result_text += f"velocity of expansion: {velocity}\n"
            result_text += f"energy of gurney: {e_gurney}\n"
            result_text += f"gurney para is: {gurney_p}\n"

            self.result_text_box.config(state=tk.NORMAL)
            self.result_text_box.delete(1.0, tk.END)
            self.result_text_box.insert(tk.END, result_text)
            self.result_text_box.config(state=tk.DISABLED)

            fig, axs = plt.subplots(2, 1, figsize=(8, 6))
            axs[0].plot(x_expansion, y_expansion)
            axs[0].plot(z_expansion, y0_expansion * np.ones(len(z_expansion)), marker="o", ls="", ms=4)
            axs[0].axhline(y=y0_expansion, xmin=0, xmax=50, ls='dashdot')
            axs[0].set_title('rx by time')

            axs[1].plot(x_velocity, y_velocity)
            axs[1].axvline(x=time_expansion, ymin=0.01, ymax=2, ls='dashdot')
            axs[1].plot(time_expansion, velocity, marker="o", ls="", ms=4)
            axs[1].set_title('vx by time')

            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("错误", f"错误: {e}")

def main():
    root = tk.Tk()
    root.title("plot-vx-1")
    root.geometry("400x580")

    page6 = Page6(root)
    root.mainloop()

if __name__ == "__main__":
    main()
