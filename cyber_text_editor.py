import tkinter as tk
from tkinter import filedialog
import random
import math

# ================= Main Window =================
root = tk.Tk()
root.title("Cyber Editor :: GPU Hacker Mode")
root.geometry("900x520")
root.configure(bg="#050807")

WIDTH, HEIGHT = 900, 520

# ================= Background Canvas =================
canvas = tk.Canvas(root, bg="#050807", highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

# ================= GPU Grid =================
def draw_grid():
    canvas.delete("grid")
    spacing = 40
    for x in range(0, WIDTH, spacing):
        canvas.create_line(x, 0, x, HEIGHT, fill="#0f2a1f", tags="grid")
    for y in range(0, HEIGHT, spacing):
        canvas.create_line(0, y, WIDTH, y, fill="#0f2a1f", tags="grid")

draw_grid()

# ================= Cyber Nodes =================
nodes = []
node_items = []

for _ in range(30):
    x = random.randint(80, WIDTH - 80)
    y = random.randint(80, HEIGHT - 80)
    r = random.randint(2, 4)
    node = canvas.create_oval(
        x-r, y-r, x+r, y+r,
        fill="#00ff9c",
        outline=""
    )
    nodes.append([x, y, r])
    node_items.append(node)

# ================= Node Pulse Animation =================
pulse_dir = 1
def pulse_nodes():
    global pulse_dir
    for i, node in enumerate(node_items):
        x, y, r = nodes[i]
        r += pulse_dir * 0.2
        if r > 5 or r < 2:
            pulse_dir *= -1
        nodes[i][2] = r
        canvas.coords(node, x-r, y-r, x+r, y+r)
    root.after(120, pulse_nodes)

pulse_nodes()

# ================= Threat Lines =================
def animate_threats():
    canvas.delete("attack")
    for _ in range(6):
        x1, y1, _ = random.choice(nodes)
        x2, y2, _ = random.choice(nodes)
        canvas.create_line(
            x1, y1, x2, y2,
            fill="#ff0033",
            dash=(4, 3),
            width=1,
            tags="attack"
        )
    root.after(700, animate_threats)

animate_threats()

# ================= Data Packets (NMAP vibe) =================
packets = []

for _ in range(15):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    dx = random.choice([-2, -1, 1, 2])
    dy = random.choice([-2, -1, 1, 2])
    dot = canvas.create_oval(x, y, x+3, y+3, fill="#00ffaa", outline="")
    packets.append([dot, dx, dy])

def move_packets():
    for p in packets:
        dot, dx, dy = p
        canvas.move(dot, dx, dy)
        x1, y1, x2, y2 = canvas.coords(dot)
        if x2 < 0 or x1 > WIDTH:
            p[1] *= -1
        if y2 < 0 or y1 > HEIGHT:
            p[2] *= -1
    root.after(50, move_packets)

move_packets()

# ================= GPU Scanline =================
scan_y = 0
def animate_scanline():
    global scan_y
    canvas.delete("scan")
    canvas.create_rectangle(
        0, scan_y, WIDTH, scan_y + 3,
        fill="#00ff9c",
        outline="",
        stipple="gray25",
        tags="scan"
    )
    scan_y += 5
    if scan_y > HEIGHT:
        scan_y = 0
    root.after(55, animate_scanline)

animate_scanline()

# ================= Editor Frame =================
editor_frame = tk.Frame(root, bg="#0b0f0c")
editor_frame.place(relx=0.05, rely=0.08, relwidth=0.9, relheight=0.78)
editor_frame.tkraise()

text = tk.Text(
    editor_frame,
    bg="#0b0f0c",
    fg="#00ff9c",
    insertbackground="#00ff9c",
    font=("Consolas", 12),
    wrap="word",
    undo=True,
    borderwidth=0
)
text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# ================= Status Bar =================
status_bar = tk.Label(
    root,
    text="[ GPU MODE ENABLED | SOC LIVE MAP ACTIVE ]",
    bg="#020403",
    fg="#00ff9c",
    font=("Consolas", 10),
    anchor="w",
    padx=10
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# ================= File Functions =================
def new_file():
    text.delete(1.0, tk.END)
    status_bar.config(text="[ NEW SESSION INITIALIZED ]")

def open_file():
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if path:
        with open(path, "r", encoding="utf-8") as f:
            text.delete(1.0, tk.END)
            text.insert(tk.END, f.read())
        status_bar.config(text="[ FILE LOADED INTO SOC ]")

def save_file():
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.get(1.0, tk.END))
        status_bar.config(text="[ DATA LOG SAVED ]")

# ================= Menu =================
menu_bar = tk.Menu(root, bg="#020403", fg="#00ff9c")
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0, bg="#020403", fg="#00ff9c")
file_menu.add_command(label="New Session", command=new_file)
file_menu.add_command(label="Open Log", command=open_file)
file_menu.add_command(label="Save Log", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit SOC", command=root.quit)

menu_bar.add_cascade(label="File", menu=file_menu)

# ================= Run =================
root.mainloop()