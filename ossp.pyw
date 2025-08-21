import tkinter as tk
import random

# ---------------- OS ROOT (frameless) ----------------
root = tk.Tk()
root.overrideredirect(True)
root.configure(bg="#2c2c2c")

# Default geometry & fullscreen toggle
default_geometry = "1024x640+100+100"
root.geometry(default_geometry)
fullscreen_on = False
def toggle_fullscreen():
    global fullscreen_on
    if not fullscreen_on:
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        root.geometry(f"{w}x{h}+0+0")
    else:
        root.geometry(default_geometry)
    fullscreen_on = not fullscreen_on

# ---- Drag whole OS window
drag_data = {"x": 0, "y": 0}
def start_os_drag(e):
    drag_data["x"], drag_data["y"] = e.x, e.y
def do_os_drag(e):
    dx, dy = e.x - drag_data["x"], e.y - drag_data["y"]
    root.geometry(f"+{root.winfo_x() + dx}+{root.winfo_y() + dy}")

# ---------------- Goodbye Screen ----------------
def exit_os():
    for widget in root.winfo_children():
        widget.destroy()
    bye_frame = tk.Frame(root, bg="#2c2c2c")
    bye_frame.pack(expand=True, fill="both")
    tk.Label(
        bye_frame, text="Hasta pronto 👋",
        font=("Segoe UI", 32, "bold"), fg="white", bg="#2c2c2c"
    ).pack(expand=True)
    root.after(2000, root.destroy)

# ---------------- Taskbar ----------------
taskbar = tk.Frame(root, bg="#1e1e1e", height=40)
taskbar.pack(side="bottom", fill="x")
taskbar.bind("<Button-1>", start_os_drag)
taskbar.bind("<B1-Motion>", do_os_drag)

tk.Button(taskbar, text="⛶", bg="#1e1e1e", fg="white",
          relief="flat", font=("Segoe UI", 12),
          command=toggle_fullscreen).pack(side="right", padx=5)
tk.Button(taskbar, text="❌", bg="#1e1e1e", fg="white",
          relief="flat", font=("Segoe UI", 12),
          command=exit_os).pack(side="right", padx=5)

tk.Label(taskbar, text=" LBOS py1.0.1 ", fg="white", bg="#1e1e1e",
         font=("Segoe UI", 12)).pack(side="left", padx=10)

# ---------------- Desktop ----------------
desktop = tk.Frame(root, bg="#2c2c2c")
desktop.pack(expand=True, fill="both")

# ---------------- App Window Factory ----------------
def make_app_window(title, content_func, width, height, x=100, y=100):
    win = tk.Frame(root, bg="#d0d0d0", bd=2, relief="raised")
    win.place(x=x, y=y, width=width, height=height)

    titlebar = tk.Frame(win, bg="#404040", height=25)
    titlebar.pack(fill="x")
    tk.Label(titlebar, text=title, bg="#404040", fg="white").pack(side="left", padx=5)
    tk.Button(titlebar, text="X", bg="firebrick", fg="white", bd=0,
              command=win.destroy).pack(side="right")

    drag = {"x": 0, "y": 0}
    def start_drag(e):
        drag["x"], drag["y"] = e.x, e.y
    def do_drag(e):
        dx, dy = e.x - drag["x"], e.y - drag["y"]
        win.place(x=win.winfo_x() + dx, y=win.winfo_y() + dy)
    titlebar.bind("<Button-1>", start_drag)
    titlebar.bind("<B1-Motion>", do_drag)

    content = tk.Frame(win, bg="#000000")
    content.pack(expand=True, fill="both")
    content_func(content)

# ---------------- Pong Game App ----------------
def pong_app(container):
    canvas = tk.Canvas(container, width=380, height=250, bg="black", highlightthickness=0)
    canvas.pack(expand=True)
    paddle = canvas.create_rectangle(160, 240, 220, 245, fill="white")
    ball = canvas.create_oval(185, 230, 195, 240, fill="red")
    ball_dx, ball_dy = 3, -3
    score = 0
    score_text = canvas.create_text(190, 15, text="Puntos: 0", fill="white", font=("Courier", 12))

    def move_paddle(event):
        x1, _, x2, _ = canvas.coords(paddle)
        if event.keysym == "Left" and x1 > 0:
            canvas.move(paddle, -20, 0)
        elif event.keysym == "Right" and x2 < 380:
            canvas.move(paddle, 20, 0)

    def game_loop():
        nonlocal ball_dx, ball_dy, score
        canvas.move(ball, ball_dx, ball_dy)
        bx1, by1, bx2, by2 = canvas.coords(ball)
        if bx1 <= 0 or bx2 >= 380:
            ball_dx = -ball_dx
        if by1 <= 0:
            ball_dy = -ball_dy
        px1, py1, px2, _ = canvas.coords(paddle)
        if by2 >= py1 and px1 < (bx1+bx2)/2 < px2 and ball_dy > 0:
            ball_dy = -ball_dy
            score += 1
            canvas.itemconfig(score_text, text=f"Score: {score}")
            ball_dx *= 1.05
            ball_dy *= 1.05
        if by2 >= 250:
            canvas.create_text(190, 125, text="PARTE TERMINADA", fill="white", font=("Courier", 14))
            return
        container.after(16, game_loop)

    root.bind("<Left>", move_paddle)
    root.bind("<Right>", move_paddle)
    game_loop()

# ---------------- Settings App ----------------
def settings_app(container):
    # Create scrollable frame
    canvas = tk.Canvas(container, bg="#e0e0e0", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#e0e0e0")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Title
    tk.Label(scroll_frame, text="Ajustes", font=("Segoe UI", 14, "bold"),
             bg="#e0e0e0").pack(pady=10)

    # Wallpaper Color Section
    tk.Label(scroll_frame, text="Color de fondo:", bg="#e0e0e0",
             font=("Segoe UI", 10, "bold")).pack(pady=(10, 0))
    color_frame = tk.Frame(scroll_frame, bg="#e0e0e0")
    color_frame.pack(pady=5)

    colors = {
        "#004080": "Blue",
        "#2c2c2c": "Charcoal",
        "black": "Black",
        "navy": "Navy",
        "darkgreen": "Dark Green",
        "maroon": "Maroon",
        "purple": "Purple",
        "darkorange": "Dark Orange",
        "#008080": "Teal",
        "#800080": "Indigo",
        "#ffcc00": "Gold",
        "#f0f0f0": "Light Gray",
        "#ffffff": "White",
        "#add8e6": "Sky Blue",
        "#90ee90": "Light Green",
        "#ff69b4": "Hot Pink",
        "#ffa07a": "Salmon",
        "#d2b48c": "Tan"
    }

    def set_wallpaper(col):
        root.configure(bg=col)
        desktop.configure(bg=col)

    for c in colors:
        tk.Button(color_frame, bg=c, width=3,
                  command=lambda col=c: set_wallpaper(col)).pack(side="left", padx=2)

    # Taskbar Color Section
    tk.Label(scroll_frame, text="Color de la barra de tareas:", bg="#e0e0e0",
             font=("Segoe UI", 10, "bold")).pack(pady=(15, 0))
    taskbar_frame = tk.Frame(scroll_frame, bg="#e0e0e0")
    taskbar_frame.pack(pady=5)

    taskbar_colors = {
        "#004080": "Blue",
        "#1e1e1e": "Default",
        "#333333": "Graphite",
        "#004466": "Ocean Blue",
        "#660000": "Crimson",
        "#444444": "Slate",
        "#222222": "Midnight",
        "#008000": "Green",
        "#800000": "Burgundy",
        "#808080": "Gray",
        "#000080": "Deep Navy",
        "#ff8c00": "Amber",
        "#2f4f4f": "Dark Slate",
        "#4682b4": "Steel Blue",
        "#5f9ea0": "Cadet Blue"
    }

    def set_taskbar(col):
        taskbar.configure(bg=col)

    for c in taskbar_colors:
        tk.Button(taskbar_frame, bg=c, width=3,
                  command=lambda col=c: set_taskbar(col)).pack(side="left", padx=2)

    # Reset Button
    def reset_defaults():
        set_wallpaper("#004080")
        set_taskbar("#004080")

    tk.Button(scroll_frame, text="Restablecer a valores predeterminados", bg="#d0d0d0",
              command=reset_defaults).pack(pady=10)

# ---------------- App Store App ----------------
def app_store_app(container):
    container.configure(bg="#f0f0f0")
    tk.Label(container, text="Tienda LBOS", font=("Segoe UI", 14, "bold"),
             bg="#f0f0f0").pack(pady=10)

    app_frame = tk.Frame(container, bg="#ffffff", bd=1, relief="solid")
    app_frame.pack(pady=5, padx=10, fill="x")
    tk.Label(app_frame, text="🎮 El juego de Pong", font=("Segoe UI", 12, "bold"),
             bg="#ffffff").pack(anchor="w", padx=5, pady=2)
    tk.Label(app_frame, text="El juego original de LB65memes. ¡Gratis!", bg="#ffffff").pack(anchor="w", padx=5)

    status_label = tk.Label(app_frame, text="", bg="#ffffff", fg="green")
    status_label.pack()

    def add_pong_icon():
        status_label.config(text="Instalado!")
        tk.Button(
            desktop,
            text="🎮 Pong",
            font=("Segoe UI", 14),
            command=lambda: make_app_window("Pong", pong_app, 420, 300, 350, 50)
        ).place(x=450, y=50)  # shifted right to avoid overlap

    def install_pong():
        wait_time = random.randint(6, 14) * 1000  # ms
        status_label.config(text="Instalación...")
        container.after(wait_time, add_pong_icon)

    tk.Button(app_frame, text="Instalar", command=install_pong).pack(pady=5)

# ---------------- Desktop Icons ----------------
tk.Button(
    desktop,
    text="🏬 Tienda",
    font=("Segoe UI", 14),
    command=lambda: make_app_window("Tienda", app_store_app, 350, 300, 120, 120)
).place(x=50, y=50)

tk.Button(
    desktop,
    text="⚙️ Ajustes",
    font=("Segoe UI", 14),
    command=lambda: make_app_window("Ajustes", settings_app, 653, 300, 150, 150)
).place(x=250, y=50)

root.mainloop()