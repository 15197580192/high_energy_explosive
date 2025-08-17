import tkinter as tk
from tkinter import scrolledtext, filedialog
import numpy as np
import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

class PlotWindow:
    def __init__(self, image_path):
        self.root = tk.Toplevel()
        self.root.title("拟合曲线图")
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self.root, image=self.photo)
        self.label.pack()
        self.root.mainloop()

class Page3:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.default_params = {
            "r1": "4.08",
            "r2": "1.09",
            "omega": "0.21",
            "rho_0": "1920.0",
            "pcj": "22.0",
            "dcj": "6817.0",
            "e0": "8.69",
            "rho_m": "1920.0",
            "radius_0": "12.7",
            "x0": "2.6",
            "filename":"jwl/data.txt"
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
        calculate_button.grid(row=row_counter+2, column=0, columnspan=2, pady=10)

    def set_default_params(self):
        for key, value in self.default_params.items():
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)

    def upload_file(self):
        self.entries["filename"].delete(0, tk.END)
        filename = filedialog.askopenfilename(title="上传数据文件", filetypes=[("Text files", "*.txt")])
        self.entries["filename"].insert(0, filename)

    def calculate_and_display(self):
        try:
            filename = self.entries["filename"].get()

            with open(filename, 'r') as file:
                lines = file.readlines()

            data = [list(map(float, line.split())) for line in lines[1:]]
            f = np.array(data)

            f = np.array(f)
            rad = f[:, 0]
            ed = f[:, 1]

            r1 = float(self.entries["r1"].get())
            r2 = float(self.entries["r2"].get())
            omega = float(self.entries["omega"].get())

            rho_0 = float(self.entries["rho_0"].get())
            pcj = float(self.entries["pcj"].get())
            dcj = float(self.entries["dcj"].get())
            e0 = float(self.entries["e0"].get())
            rho_m = float(self.entries["rho_m"].get())
            radius_0 = float(self.entries["radius_0"].get())
            x0 = float(self.entries["x0"].get())

            Q0 = 7003.0*10**3
            gamma = (rho_0*dcj**2)*10**(-9)/pcj - 1.0
            vcj = gamma/(gamma+1)

            vrad = 1.0146 + 0.19174 * rad + 0.006178 * rad**2

            rx = vrad
            ry = e0-ed*rho_m*10**(-3)

            def func(RX, r1, r2, omega):
                a11 = math.exp (-r1*vcj)/r1; a12 = math.exp(-r2*vcj)/r2
                a13 = vcj**(-omega)/omega

                a21 = math.exp(-r1*vcj); a22 = math.exp (-r2*vcj); a23 = vcj**(-omega-1)

                a31 = r1*math.exp(-r1*vcj); a32 = r2*math.exp(-r2*vcj)
                a33 = (omega+1)*vcj**(-omega-2)

                y1 = e0 + 0.5*pcj*(1-vcj); y2 = pcj; y3 = rho_0 * (dcj**2)*(10**(-9))

                M = np.array([[a11,a12,a13],[a21,a22,a23],[a31,a32,a33]])
                Y= np.array([y1,y2,y3])
                X = np.linalg.solve(M,Y)
                return X[0]*np.exp (-r1*RX)/r1+ X[1]*np.exp(-r2*RX)/r2+X[2]*RX**(-omega)/omega

            # initial_guess = [4.08, 1.09, 0.21]
            initial_guess = [r1, r2, omega]
            popt,_ = curve_fit(func, rx, ry, p0=initial_guess)

            result_text = f"vcj,gamma: {vcj},{gamma}\n"
            result_text += f"RX,RY: {rx},{ry}\n"
            result_text += f"error for 19mm: {rx[0]-ry[0]}\n"
            result_text += f"parameter:  {popt}\n"
            self.result_text_box.config(state=tk.NORMAL)
            self.result_text_box.delete(1.0, tk.END)
            self.result_text_box.insert(tk.END, result_text)
            self.result_text_box.config(state=tk.DISABLED)

            # 绘制拟合曲线
            plt.figure(figsize=(5, 4))
            plt.plot(rx, ry, 'o', color ='red', label ="data")
            estimated = func(rx, popt[0], popt[1], popt[2])
            plt.plot(rx, estimated, '--', color ='blue', label ="optimized data")
            plt.legend()
            plt.savefig('fit_curve.png')  # 保存图形
            plt.close()

            # 显示图形
            plot_window = PlotWindow('fit_curve.png')

        except Exception as e:
            self.result_text_box.config(state=tk.NORMAL)
            self.result_text_box.delete(1.0, tk.END)
            self.result_text_box.insert(tk.END, f"错误: {e}")
            self.result_text_box.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    root.title("jwl-yt-final")
    root.geometry("400x580")

    page3 = Page3(root)
    root.mainloop()

if __name__ == "__main__":
    main()
