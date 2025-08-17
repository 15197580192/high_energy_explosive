import tkinter as tk
import micro.gui as gui
from PIL import Image, ImageTk
import jwl.jwl_gui as jwl_gui
import jwl.jwl_yt_final_gui as jwl_yt_final_gui
import water.bubble_gui as bubble_gui
import water.energy_gui as energy_gui
import yt.plot_vx_gui as plot_vx_gui
import material_pile.calc_box as box
import material_pile.calc_circular as mix
import material_pile.calc_concentricball as concentricball
import material_pile.calc_inner_circular as innerball
import material_pile.calc_mixed_circular as distribute
import material_pile.calc_net_ball as net

def show_page(page):
    # 隐藏所有页面
    for p in pages:
        p.pack_forget()
    # 显示目标页面
    page.pack(fill="both", expand=True)

def create_page(title, color):
    page = tk.Frame(main_frame, bg=color)
    label = tk.Label(page, text=title, font=("Helvetica", 18), bg=color)
    label.pack(pady=20)
    back_button = tk.Button(page, text="返回主界面", command=lambda: show_page(main_page),
                           bg="#4a7abc", fg="white", relief="flat", padx=10, pady=5)
    back_button.pack(pady=10)
    return page

# 创建风格统一的按钮
def create_button(parent, text, command, bg_color):
    return tk.Button(parent, text=text, command=command,
                    bg=bg_color, fg="white", relief="raised",
                    padx=5, pady=3, font=("微软雅黑", 9))

root = tk.Tk()
root.title("高能炸药能量输出仿真预估模型")
root.geometry("1000x600")
root.configure(bg="#f0f0f0")

# 创建主框架
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# 创建主页面
main_page = tk.Frame(main_frame, bg="#f0f0f0")

# 顶部标题栏 - 添加Logo
header = tk.Frame(main_page, bg="#1e3c72", height=80)
header.pack(fill="x", pady=(0, 20))

# 创建一个容器框架来居中放置Logo和标题
center_container = tk.Frame(header, bg="#1e3c72")
center_container.pack(expand=True)

# 加载并显示Logo图片
try:
    # 替换为实际的logo图片路径
    logo_img = Image.open("lOGO\logo.png")
    logo_img = logo_img.resize((60, 60), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(center_container, image=logo_photo, bg="#1e3c72")
    logo_label.image = logo_photo
    logo_label.pack(side="left", padx=(0, 10), pady=10)

except Exception as e:
    print(f"无法加载Logo图片: {e}")
    logo_label = tk.Label(center_container, text="[LOGO]", font=("Microsoft YaHei", 14),
                          bg="#1e3c72", fg="white")
    logo_label.pack(side="left", padx=(0, 10), pady=10)

# 标题文字
title_label = tk.Label(center_container, text="高能炸药能量输出仿真预估模型",
                       font=("Microsoft YaHei", 20, "bold"), bg="#1e3c72", fg="white")
title_label.pack(side="left", pady=15)

# 主内容区 - 使用框架确保内容居中
content_frame = tk.Frame(main_page, bg="#f0f0f0")
content_frame.pack(expand=True)

# 定义颜色方案
colors = {
    "reaction": "#5c6bc0",     # 反应完全度
    "jwl": "#26a69a",          # JWL方程
    "structure": "#7e57c2",    # 结构计算
    "water": "#29b6f6",        # 水下能量
    "cylinder": "#66bb6a"      # 圆筒能量
}

# 第一行功能块
row1_frame = tk.Frame(content_frame, bg="#f0f0f0")
row1_frame.pack(pady=5)

# 反应完全度
section1 = tk.LabelFrame(row1_frame, text="   反应完全度 ", font=("微软雅黑", 10),
                        bg="white", padx=10, pady=10)
section1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
create_button(section1, "lamda计算", lambda: gui.main(), colors["reaction"]).pack(pady=5)

# JWL方程
section2 = tk.LabelFrame(row1_frame, text=" JWL气体状态方程 ", font=("微软雅黑", 10),
                        bg="white", padx=10, pady=10)
section2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
create_button(section2, "系数拟合", lambda: jwl_gui.main(), colors["jwl"]).pack(pady=5)
create_button(section2, "圆筒数据拟合", lambda: jwl_yt_final_gui.main(), colors["jwl"]).pack(pady=5)

# 结构计算 - 第一组
sectionA = tk.LabelFrame(row1_frame, text=" 层状结构 ", font=("微软雅黑", 10),
                        bg="white", padx=10, pady=10)
sectionA.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
create_button(sectionA, "box", lambda: box.main(), colors["structure"]).pack(pady=5)

sectionB = tk.LabelFrame(row1_frame, text=" 机械混合结构 ", font=("微软雅黑", 10),
                        bg="white", padx=10, pady=10)
sectionB.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
create_button(sectionB, "mix", lambda: mix.main(), colors["structure"]).pack(pady=5)

sectionF = tk.LabelFrame(row1_frame, text="  分布式结构 ", font=("微软雅黑", 10),
                        bg="white", padx=10, pady=10)
sectionF.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")
create_button(sectionF, "distribute", lambda: distribute.main(), colors["structure"]).pack(pady=5)

# 第二行功能块
row2_frame = tk.Frame(content_frame, bg="#f0f0f0")
row2_frame.pack(pady=5)

# 水下能量
section3 = tk.LabelFrame(row2_frame, text="  水下能量输出 ", font=("微软雅黑", 10),
                        bg="white", padx=10, pady=10)
section3.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
create_button(section3, "气泡能计算", lambda: bubble_gui.main(), colors["water"]).pack(pady=5)
create_button(section3, "冲击波能计算", lambda: energy_gui.main(), colors["water"]).pack(pady=5)

# 圆筒能量
section4 = tk.LabelFrame(row2_frame, text=" 圆筒能量输出 ", font=("微软雅黑", 10),
                        bg="white", padx=10, pady=10)
section4.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
create_button(section4, "数据处理", lambda: plot_vx_gui.main(), colors["cylinder"]).pack(pady=5)

# 结构计算 - 第二组
sectionD = tk.LabelFrame(row2_frame, text="    核壳结构  ", font=("微软雅黑", 10),
                        bg="white", padx=10, pady=10)
sectionD.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
create_button(sectionD, "concentric", lambda: concentricball.main(), colors["structure"]).pack(pady=5)

sectionE = tk.LabelFrame(row2_frame, text="   共颗粒结构 ", font=("微软雅黑", 10),
                        bg="white", padx=10, pady=10)
sectionE.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
create_button(sectionE, "inner-pellet", lambda: innerball.main(), colors["structure"]).pack(pady=5)

sectionC = tk.LabelFrame(row2_frame, text=" 网状结构 ", font=("微软雅黑", 10),
                        bg="white", padx=10, pady=10)
sectionC.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")
create_button(sectionC, "net", lambda: net.main(), colors["structure"]).pack(pady=5)

# 底部版权信息
footer = tk.Frame(main_page, bg="#f0f0f0", height=30)
footer.pack(fill="x", pady=(20, 0))
tk.Label(footer, text="© 高能炸药能量仿真系统 | 版本 1.0",
        font=("微软雅黑", 9), bg="#f0f0f0", fg="#666666").pack(side="bottom")

main_page.pack(fill="both", expand=True)

# 创建其他页面
page1 = create_page("反应完全度计算界面", "#e3f2fd")
page2 = create_page("JWL方程系数拟合界面", "#e0f2f1")
page3 = create_page("结构计算界面", "#f3e5f5")
page4 = create_page("水下能量计算界面", "#e3f2fd")
page5 = create_page("圆筒能量计算界面", "#e8f5e9")
page6 = create_page("分布式结构计算界面", "#fff3e0")

# 将页面添加到列表中
pages = [main_page, page1, page2, page3, page4, page5, page6]

root.mainloop()