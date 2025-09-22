# -*- coding: utf-8 -*-
import json
import random
from datetime import datetime
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import font as tkFont

# ===== 五行颜色映射 =====
wuxing_color = {
    "木": "#00FF00",  # 绿色
    "火": "#FF4500",  # 橙红
    "土": "#DAA520",  # 金黄色
    "金": "#00CED1",  # 青色
    "水": "#1E90FF"   # 蓝色
}

# ===== 吉凶背景色 =====
luck_bg = {
    "大吉": "#FFD700",  # 金色
    "吉": "#008000",    # 绿色
    "凶": "#8B0000"     # 深红
}

# ===== 读取 gua.json =====
script_dir = os.path.dirname(os.path.abspath(__file__))
gua_file = os.path.join(script_dir, "gua.json")
try:
    with open(gua_file, "r", encoding="utf-8") as f:
        gua_list = json.load(f)
except FileNotFoundError:
    messagebox.showerror("错误", f"找不到 {gua_file}")
    exit(1)

# ===== 五行关系 =====
wuxing_sheng = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
wuxing_ke = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
luck_order = ["凶", "吉", "大吉"]

# ===== 时辰表 =====
shichen_data = [
    ("子", "水"), ("丑", "土"), ("寅", "木"), ("卯", "木"),
    ("辰", "土"), ("巳", "火"), ("午", "火"), ("未", "土"),
    ("申", "金"), ("酉", "金"), ("戌", "土"), ("亥", "水")
]

# ===== 获取时辰五行 =====
def get_shichen_wuxing(now: datetime):
    hour = now.hour
    index = ((hour + 1) // 2) % 12
    return shichen_data[index]

# ===== 修正吉凶 =====
def adjust_luck(original_luck, shichen_wx, gua_wx):
    if shichen_wx == wuxing_sheng.get(gua_wx):
        new_index = min(luck_order.index(original_luck) + 1, len(luck_order) - 1)
        relation = "相生"
    elif shichen_wx == wuxing_ke.get(gua_wx):
        new_index = max(luck_order.index(original_luck) - 1, 0)
        relation = "相克"
    elif gua_wx == shichen_wx:
        relation = "相同"
        new_index = luck_order.index(original_luck)
    else:
        relation = "无影响"
        new_index = luck_order.index(original_luck)
    return luck_order[new_index], relation

# ===== 抽卦并显示 =====
def draw_gua():
    now = datetime.now()
    shichen, shichen_wx = get_shichen_wuxing(now)
    gua = random.choice(gua_list)
    new_luck, relation = adjust_luck(gua["luck"], shichen_wx, gua["wuxing"])

    # 默认背景
    output_box.config(bg="black", fg="white")
    if new_luck in luck_bg:
        output_box.config(bg=luck_bg[new_luck])

    output_box.delete(1.0, tk.END)

    # 时间
    output_box.insert(tk.END, f"当前时间：{now.strftime('%Y-%m-%d %H:%M')}\n", "normal")

    # 时辰 + 五行颜色
    output_box.insert(tk.END, f"农历时辰：{shichen}时（", "normal")
    output_box.insert(tk.END, shichen_wx, f"wuxing_{shichen_wx}")
    output_box.insert(tk.END, "）\n\n", "normal")

    # 卦名
    output_box.insert(tk.END, f"{gua['name']} {gua['sym']}\n", "gua_title")

    # 卦五行
    output_box.insert(tk.END, "卦五行：", "gua_big")
    output_box.insert(tk.END, gua["wuxing"], f"wuxing_{gua['wuxing']}")
    output_box.insert(tk.END, "\n", "normal")

    # 原始吉凶
    output_box.insert(tk.END, f"原始吉凶：{gua['luck']}\n", "gua_big")

    # 卦辞
    output_box.insert(tk.END, f"卦辞：{gua['desc']}\n\n", "gua_big")

    # 白话文解读
    output_box.insert(tk.END, "【白话文解读】\n", "section")
    output_box.insert(tk.END, f"财运：{gua['finance']}\n", "normal")
    output_box.insert(tk.END, f"社交：{gua['social']}\n", "normal")
    output_box.insert(tk.END, f"游戏：{gua['gaming']}\n", "normal")
    output_box.insert(tk.END, f"健康：{gua['health']}\n\n", "normal")

    # 五行对比
    output_box.insert(tk.END, "【五行对比】\n", "section2")
    output_box.insert(tk.END, "五行关系：", "normal")
    output_box.insert(tk.END, shichen_wx, f"wuxing_{shichen_wx}")
    output_box.insert(tk.END, " 与 ", "normal")
    output_box.insert(tk.END, gua["wuxing"], f"wuxing_{gua['wuxing']}")
    output_box.insert(tk.END, f" → {relation}\n", "normal")
    output_box.insert(tk.END, f"修正后吉凶：{new_luck}\n", "normal")

# ===== GUI 部分 =====
root = tk.Tk()
root.title("赛博挂算机")
root.geometry("520x650")

btn = tk.Button(root, text="抽一卦", font=("微软雅黑", 14), command=draw_gua)
btn.pack(pady=10)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD)
output_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# ===== 字体样式 =====
big_font = tkFont.Font(family="微软雅黑", size=16, weight="bold")  # 卦等大
med_font = tkFont.Font(family="微软雅黑", size=14, weight="bold")  # 五行对比
section_font = tkFont.Font(family="微软雅黑", size=12, weight="bold")
normal_font = tkFont.Font(family="微软雅黑", size=12)

# ===== 基本标签 =====
output_box.tag_config("normal", font=normal_font, foreground="white")
output_box.tag_config("gua_title", font=big_font, foreground="#FF69B4")  # 卦名粉色
output_box.tag_config("gua_big", font=big_font, foreground="white")
output_box.tag_config("section", font=section_font, foreground="#FFD700") # 金色
output_box.tag_config("section2", font=med_font, foreground="#FFD700")    # 五行对比

# ===== 五行颜色标签 =====
for wx, color in wuxing_color.items():
    tagname = f"wuxing_{wx}"
    output_box.tag_config(tagname, font=big_font, foreground=color)

root.mainloop()
