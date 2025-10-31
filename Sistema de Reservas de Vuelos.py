from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter import ttk
import random
import re

# ---------------------------
# Configuración y estado
# ---------------------------
vuelos = []          # lista global con todos los vuelos
contador_vuelos = 1

# UI / estilo global
DEFAULT_FONT = ("Segoe UI", 10)
SEAT_FREE_COLOR = "#d4fddf"
SEAT_OCCUPIED_COLOR = "#ffd6d6"
SEAT_OUTLINE = "#333333"
CANVAS_BG = "#ffffff"
SEAT_SIZE_BASE = 28

# ---------------------------
# Utilidades
# ---------------------------
def obtener_letra_fila(n):
    # n es índice 0-based -> devuelve "A", "B", ..., "Z", "AA", ...
    letras = ""
    while True:
        n, r = divmod(n, 26)
        letras = chr(65 + r) + letras
        if n == 0:
            break
        n -= 1
    return letras

def centrar_ventana(ventana, ww, wh):
    ventana.update_idletasks()
    sw = ventana.winfo_screenwidth()
    sh = ventana.winfo_screenheight()
    x = (sw - ww) // 2
    y = (sh - wh) // 2
    ventana.geometry(f"{ww}x{wh}+{x}+{y}")

# ---------------------------
# Selección modal de vuelo
# ---------------------------
def seleccionar_vuelo():
    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return None

    ventana = Toplevel()
    ventana.title("Seleccionar Vuelo")
    ventana.grab_set()
    ventana.transient(root)

    Label(ventana, text="Seleccione el número interno del vuelo:").pack(padx=12, pady=(10,4))

    opciones = [f"{i+1} — {vuelos[i][0] or 'sin código'}" for i in range(len(vuelos))]
    combo = ttk.Combobox(ventana, values=opciones, state="readonly", width=30)
    combo.set("Seleccione un vuelo")
    combo.pack(padx=12, pady=(0,12))

    seleccion = {"num": None}

    def confirmar():
        val = combo.get()
        if not val or val.startswith("Seleccione"):
            messagebox.showerror("Error", "Seleccione un vuelo.")
            return
        m = re.match(r'\d+', val.strip())
        if not m:
            messagebox.showerror("Error", "Selección inválida.")
            return
        seleccion["num"] = int(m.group())
        ventana.destroy()

    Button(ventana, text="Confirmar", command=confirmar).pack(pady=(0,10))
    ventana.wait_window()
    return seleccion["num"]

# ---------------------------
# Crear vuelo
# ---------------------------
def Crear_nuevo_vuelo():
    global contador_vuelos
    while True:
        filas = simpledialog.askinteger("Crear vuelo", "Cantidad de filas (1-50):")
        if filas is None:
            return
        if 1 <= filas <= 50:
            break
        messagebox.showerror("Error", "Número de filas inválido (1-50).")

    while True:
        columnas = simpledialog.askinteger("Crear vuelo", "Cantidad de columnas (1-20):")
        if columnas is None:
            return
        if 1 <= columnas <= 20:
            break
        messagebox.showerror("Error", "Número de columnas inválido (1-20).")

    matriz = [[False for _ in range(columnas)] for _ in range(filas)]
    vuelo = [
        f"V{contador_vuelos}",  # código (por defecto)
        "",  # origen
        "",  # destino
        0,   # precio
        matriz,
        0,   # reservas
        filas,
        columnas
    ]
    vuelos.append(vuelo)
    contador_vuelos += 1
    messagebox.showinfo("Vuelo creado", "Vuelo creado exitosamente.")

# ---------------------------
# Asignar origen/destino/precio
# ---------------------------
def origen_destino_precio():
    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return
    num = seleccionar_vuelo()
    if num is None:
        return
    vuelo = vuelos[num-1]

    codigo = simpledialog.askstring("Código", "Ingrese el código del vuelo (ej. CM123):")
    if codigo is None:
        return
    if codigo.strip() == "":
        messagebox.showerror("Error", "Código no válido.")
        return

    origen = simpledialog.askstring("Origen", "Ingrese el origen:")
    if origen is None:
        return
    if not all(palabra.isalpha() for palabra in origen.split()):
        messagebox.showerror("Error", "Origen inválido.")
        return

    destino = simpledialog.askstring("Destino", "Ingrese el destino:")
    if destino is None:
        return
    if not all(palabra.isalpha() for palabra in destino.split()):
        messagebox.showerror("Error", "Destino inválido.")
        return

    precio = simpledialog.askinteger("Precio", "Ingrese el precio del boleto (entero):")
    if precio is None:
        return
    if precio < 1:
        messagebox.showerror("Error", "Precio inválido.")
        return

    vuelo[0] = codigo
    vuelo[1] = origen
    vuelo[2] = destino
    vuelo[3] = precio
    messagebox.showinfo("Datos asignados", f"Datos del vuelo {num} asignados correctamente.")

# ---------------------------
# Estado del vuelo (canvas)
# ---------------------------
def estado_vuelo():
    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return
    num = seleccionar_vuelo()
    if num is None:
        return
    vuelo = vuelos[num-1]
    matriz = vuelo[4]
    filas, columnas = vuelo[6], vuelo[7]

    tamaño = max(12, min(SEAT_SIZE_BASE, 800 // max(1, columnas)))
    margen = 28
    margen_superior = 48
    total_w = columnas * tamaño + margen * 2
    total_h = filas * tamaño + margen * 2 + margen_superior

    ventana = Toplevel()
    ventana.title(f"Estado del vuelo {num} — {vuelo[0]}")
    ventana.grab_set()
    ventana.transient(root)

    frame = Frame(ventana)
    frame.pack(fill=BOTH, expand=True)

    canvas = Canvas(frame, width=min(total_w, 900), height=min(total_h, 600), bg=CANVAS_BG, highlightthickness=0)
    h_scroll = Scrollbar(frame, orient=HORIZONTAL, command=canvas.xview)
    v_scroll = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
    v_scroll.pack(side=RIGHT, fill=Y)
    h_scroll.pack(side=BOTTOM, fill=X)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    start_x = margen
    start_y = margen_superior

    canvas.create_text(start_x + (columnas * tamaño)//2, 16, text=f"VUELO {vuelo[0]}", font=(DEFAULT_FONT[0], 11, "bold"))

    for j in range(columnas):
        x = start_x + j * tamaño + tamaño // 2
        canvas.create_text(x, start_y - 14, text=str(j+1), fill="black", font=(DEFAULT_FONT[0], 9))

    for i in range(filas):
        y = start_y + i * tamaño + tamaño // 2
        letra = obtener_letra_fila(i)
        canvas.create_text(start_x - 12, y, text=letra, fill="black", font=(DEFAULT_FONT[0], 9))

    for i in range(filas):
        for j in range(columnas):
            x = start_x + j * tamaño
            y = start_y + i * tamaño
            color = SEAT_FREE_COLOR if not matriz[i][j] else SEAT_OCCUPIED_COLOR
            canvas.create_rectangle(x+1, y+1, x + tamaño - 2, y + tamaño - 2, fill=color, outline=SEAT_OUTLINE)
            if matriz[i][j]:
                canvas.create_text(x + tamaño//2, y + tamaño//2, text="X", fill="#200", font=(DEFAULT_FONT[0], max(8, tamaño//3), "bold"))

    total = filas * columnas
    ocupados = sum(1 for row in matriz for seat in row if seat)
    porcentaje = (ocupados / total) * 100 if total else 0
    info_text = f"Asientos: {total}    Ocupados: {ocupados}    % Ocupación: {porcentaje:.1f}%"
    canvas.create_text(start_x + (columnas * tamaño)//2, start_y + filas * tamaño + 18, text=info_text, font=(DEFAULT_FONT[0], 10))

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# ---------------------------
# Reservar asiento individual
# ---------------------------
def reservar_asiento():
    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return
    num = seleccionar_vuelo()
    if num is None:
        return
    vuelo = vuelos[num-1]
    matriz = vuelo[4]
    filas, columnas = vuelo[6], vuelo[7]

    asientos_libres = []
    for i in range(filas):
        for j in range(columnas):
            if not matriz[i][j]:
                etiqueta = f"{obtener_letra_fila(i)}{j+1}"
                asientos_libres.append((i, j, etiqueta))

    if not asientos_libres:
        messagebox.showinfo("Sin asientos", "No hay asientos disponibles en este vuelo.")
        return

    ventana = Toplevel()
    ventana.title(f"Seleccionar asiento - Vuelo {num}")
    ventana.grab_set()
    ventana.transient(root)
    Label(ventana, text="Seleccione un asiento disponible:").pack(padx=10, pady=(10,0))

    valores = [a[2] for a in asientos_libres]
    combo = ttk.Combobox(ventana, values=valores, state="readonly", width=12)
    combo.set("Seleccione")
    combo.pack(padx=10, pady=10)

    def confirmar():
        sel = combo.get()
        if sel == "" or sel == "Seleccione":
            messagebox.showerror("Error", "Seleccione un asiento.")
            return
        for fila_idx, col_idx, etiqueta in asientos_libres:
            if etiqueta == sel:
                matriz[fila_idx][col_idx] = True
                vuelo[5] += 1
                messagebox.showinfo("Reservado", f"Asiento {sel} reservado correctamente.")
                ventana.destroy()
                return

    Button(ventana, text="Confirmar", command=confirmar).pack(pady=(0,10))

# ---------------------------
# Cancelar reserva
# ---------------------------
def cancelar_reserva():
    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return
    num = seleccionar_vuelo()
    if num is None:
        return
    vuelo = vuelos[num-1]
    matriz = vuelo[4]
    filas, columnas = vuelo[6], vuelo[7]
    if vuelo[5] == 0:
        messagebox.showerror("ERROR","El vuelo no tiene asientos reservados")
        return

    ocupados = []
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j]:
                etiqueta = f"{obtener_letra_fila(i)}{j+1}"
                ocupados.append((i, j, etiqueta))

    ventana = Toplevel()
    ventana.title(f"Asientos Ocupados - vuelo {num}")
    ventana.grab_set()
    ventana.transient(root)

    valores = [a[2] for a in ocupados]
    combo = ttk.Combobox(ventana, values=valores, state="readonly", width=12)
    combo.set("Seleccione asiento")
    combo.pack(padx=12, pady=12)

    def confirmar():
        sel = combo.get()
        if sel == "" or sel == "Seleccione asiento":
            messagebox.showerror("Error", "Seleccione un asiento.")
            return
        for fila_idx, col_idx, etiqueta in ocupados:
            if etiqueta == sel:
                matriz[fila_idx][col_idx] = False
                vuelo[5] -= 1
                messagebox.showinfo("Cancelado", f"Reserva del asiento {sel} cancelada.")
                ventana.destroy()
                return

    Button(ventana, text="Confirmar", command=confirmar).pack(pady=(0,10))

# ---------------------------
# Estadísticas
# ---------------------------
def estadistica_ocupacion():
    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return
    num = seleccionar_vuelo()
    if num is None:
        return
    vuelo = vuelos[num-1]
    filas, columnas = vuelo[6], vuelo[7]
    total = filas*columnas
    ocupados = vuelo[5]
    porcentaje = (ocupados / total) * 100 if total else 0
    messagebox.showinfo("Estadísticas de ocupación", f"Número interno: {vuelo[0]}\nOrigen/Destino: {vuelo[1]} → {vuelo[2]}\nAsientos: {total}\nOcupados: {ocupados}\n% Ocupación: {porcentaje:.1f}%")

def estadistica_recaudacion():
    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return
    num = seleccionar_vuelo()
    if num is None:
        return
    vuelo = vuelos[num-1]
    total = vuelo[3] * vuelo[5]
    messagebox.showinfo("Estadísticas de recaudación", f"Número interno: {vuelo[0]}\nOrigen/Destino: {vuelo[1]} → {vuelo[2]}\nEntradas vendidas: {vuelo[5]}\nPrecio: {vuelo[3]}\nTotal recaudado: {total}")

# ---------------------------
# Buscar por destino y mostrar disponibles
# ---------------------------
def obtener_vuelos_por_destino(destino):
    if destino is None:
        return []
    destino = destino.strip().lower()
    resultados = []
    for i, vuelo in enumerate(vuelos, 1):
        if isinstance(vuelo[2], str) and vuelo[2].strip().lower() == destino:
            resultados.append((i, vuelo))
    return resultados

def mostrar_resultados(destino, resultados):
    ventana = Toplevel()
    ventana.title(f"Vuelos a {destino}")
    ventana.grab_set()
    ventana.transient(root)
    listbox = Listbox(ventana, width=80)
    for num, vuelo in resultados:
        disponibles = sum(1 for fila in vuelo[4] for asiento in fila if not asiento)
        listbox.insert(END, f"{num} — {vuelo[0]} | {vuelo[1]} → {vuelo[2]} | ₡{vuelo[3]} | Asientos disponibles: {disponibles}")
    listbox.pack(padx=10, pady=10)
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=(0,10))

def buscar_vuelos_por_destino_ui():
    ventana = Toplevel()
    ventana.title("Búsqueda por destino")
    ventana.grab_set()
    ventana.transient(root)

    frame_left = Frame(ventana)
    frame_left.pack(side=LEFT, padx=8, pady=8)
    Label(frame_left, text="Destinos disponibles:", font=(DEFAULT_FONT[0], 10, "bold")).pack()
    destinos = sorted({vuelo[2] for vuelo in vuelos if vuelo[2]})
    listbox = Listbox(frame_left, height=10, width=24)
    for d in destinos:
        listbox.insert(END, d)
    listbox.pack(padx=6, pady=6)

    frame_right = Frame(ventana)
    frame_right.pack(side=LEFT, padx=8, pady=8)
    Label(frame_right, text="Ingrese el destino:").pack(pady=(6,0))
    entrada = Entry(frame_right)
    entrada.pack(pady=6)

    def buscar():
        dest = entrada.get().strip()
        if not dest:
            messagebox.showerror("Error", "Ingrese un destino.")
            return
        resultados = obtener_vuelos_por_destino(dest)
        if not resultados:
            messagebox.showinfo("Resultados", f"No hay vuelos con destino: {dest}")
            return
        mostrar_resultados(dest, resultados)

    Button(frame_right, text="Buscar", command=buscar).pack(pady=6)
    Button(frame_right, text="Cerrar", command=ventana.destroy).pack(pady=6)

# ---------------------------
# Tabla de vuelos disponibles
# ---------------------------
def vuelos_disponibles():
    if not vuelos:
        messagebox.showinfo("Vuelos Disponibles", "No hay vuelos registrados.")
        return
    ventana = Toplevel()
    ventana.title("Vuelos Disponibles")
    ventana.grab_set()
    ventana.transient(root)
    tabla = ttk.Treeview(ventana, columns=("Número","Código","Origen","Destino","Precio"), show="headings", height=10)
    for col, txt, w in [("Número","Número",60),("Código","Código",100),("Origen","Origen",120),("Destino","Destino",120),("Precio","Precio",80)]:
        tabla.heading(col, text=txt)
        tabla.column(col, width=w)
    for i, vuelo in enumerate(vuelos, 1):
        tabla.insert("", END, values=(i, vuelo[0], vuelo[1], vuelo[2], f"₡{vuelo[3]}"))
    tabla.pack(padx=10, pady=10)
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=(0,8))

# ---------------------------
# Reservar varios asientos consecutivos
# ---------------------------
def Reservar_varios_asientos_consecutivos():
    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return
    num = seleccionar_vuelo()
    if num is None:
        return
    vuelo = vuelos[num-1]
    matriz = vuelo[4]
    filas, columnas = vuelo[6], vuelo[7]

    filas_opciones = [obtener_letra_fila(i) for i in range(filas)]
    columnas_opciones = [str(i+1) for i in range(columnas)]

    ventana = Toplevel()
    ventana.title(f"Reservar asientos consecutivos - Vuelo {num}")
    ventana.grab_set()
    ventana.transient(root)

    Label(ventana, text="Fila:").grid(row=0, column=0, padx=8, pady=8)
    combo_filas = ttk.Combobox(ventana, values=filas_opciones, state="readonly", width=8)
    combo_filas.current(0)
    combo_filas.grid(row=0, column=1, padx=8, pady=8)

    Label(ventana, text="Asiento inicial:").grid(row=1, column=0, padx=8, pady=8)
    combo_cols = ttk.Combobox(ventana, values=columnas_opciones, state="readonly", width=8)
    combo_cols.current(0)
    combo_cols.grid(row=1, column=1, padx=8, pady=8)

    Label(ventana, text="Cantidad:").grid(row=2, column=0, padx=8, pady=8)
    spin = Spinbox(ventana, from_=1, to=columnas, width=6)
    spin.grid(row=2, column=1, padx=8, pady=8)

    def confirmar():
        fila_label = combo_filas.get()
        col_label = combo_cols.get()
        try:
            cantidad = int(spin.get())
        except Exception:
            messagebox.showerror("Error", "Cantidad inválida.")
            return
        if not fila_label or not col_label:
            messagebox.showerror("Error", "Seleccione fila y asiento inicial.")
            return
        fila_idx = filas_opciones.index(fila_label)
        start_col = int(col_label) - 1
        if cantidad < 1 or start_col + cantidad > columnas:
            messagebox.showerror("Error", "Bloque fuera de límites.")
            return
        ocupados = [f"{obtener_letra_fila(fila_idx)}{j+1}" for j in range(start_col, start_col+cantidad) if matriz[fila_idx][j]]
        if ocupados:
            messagebox.showerror("Error", f"No se puede reservar. Ocupados: {' '.join(ocupados)}")
            return
        reservados = []
        for j in range(start_col, start_col+cantidad):
            matriz[fila_idx][j] = True
            reservados.append(f"{obtener_letra_fila(fila_idx)}{j+1}")
        vuelo[5] += cantidad
        messagebox.showinfo("Reservado", f"Reservados: {' '.join(reservados)}")
        ventana.destroy()

    Button(ventana, text="Confirmar", command=confirmar).grid(row=3, column=0, padx=8, pady=10)
    Button(ventana, text="Cancelar", command=ventana.destroy).grid(row=3, column=1, padx=8, pady=10)

# ---------------------------
# Simular venta masiva
# ---------------------------
def Simular_venta_masiva():
    if not vuelos:
        messagebox.showinfo("Simular venta masiva", "No hay vuelos registrados.")
        return
    porcentaje = simpledialog.askinteger("Simular venta masiva", "Ingrese porcentaje (1-100):")
    if porcentaje is None:
        return
    if porcentaje < 1 or porcentaje > 100:
        messagebox.showerror("Error", "Porcentaje inválido.")
        return
    resultados = []
    for idx, vuelo in enumerate(vuelos, 1):
        matriz = vuelo[4]
        filas, columnas = vuelo[6], vuelo[7]
        total = filas * columnas
        objetivo = int(round(total * (porcentaje / 100.0)))
        actuales = vuelo[5]
        if actuales >= objetivo:
            resultados.append(f"{idx} — {vuelo[0]}: ya tiene {actuales} (>= objetivo {objetivo})")
            continue
        necesidad = objetivo - actuales
        libres = [(r,c) for r in range(filas) for c in range(columnas) if not matriz[r][c]]
        if not libres:
            resultados.append(f"{idx} — {vuelo[0]}: no hay asientos libres.")
            continue
        cuanto = min(necesidad, len(libres))
        seleccion = random.sample(libres, cuanto)
        etiquetas = []
        for r,c in seleccion:
            matriz[r][c] = True
            etiquetas.append(f"{obtener_letra_fila(r)}{c+1}")
        vuelo[5] += len(seleccion)
        resultados.append(f"{idx} — {vuelo[0]}: reservados {len(seleccion)} -> {' '.join(etiquetas)}")
    ventana = Toplevel()
    ventana.title("Resultado simulación")
    ventana.grab_set()
    ventana.transient(root)
    listbox = Listbox(ventana, width=90)
    for linea in resultados:
        listbox.insert(END, linea)
    listbox.pack(padx=10, pady=10)
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=(0,10))

# ---------------------------
# Reiniciar vuelo
# ---------------------------
def Reiniciar_vuelo():
    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return
    num = seleccionar_vuelo()
    if num is None:
        return
    vuelo = vuelos[num-1]
    if not messagebox.askyesno("Confirmar reinicio", f"¿Desea reiniciar el vuelo {num} ({vuelo[0]})?"):
        return
    matriz = vuelo[4]
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz[i][j] = False
    vuelo[5] = 0
    messagebox.showinfo("Reinicio", f"Reinicio del vuelo {num} realizado.")

# ---------------------------
# Interfaz principal
# ---------------------------
root = Tk()
root.title("Sistema de Reserva de Vuelos")
ww, wh = 980, 680
centrar_ventana(root, ww, wh)
root.resizable(False, False)

style = ttk.Style()
try:
    style.theme_use('clam')
except Exception:
    pass
style.configure("TButton", font=DEFAULT_FONT, padding=6)
style.configure("TLabel", font=DEFAULT_FONT)

main = Frame(root, bg="#ffffff")
main.pack(fill=BOTH, expand=True)

sidebar = Frame(main, width=280, bg="#ffffff", bd=1, relief=RIDGE)
sidebar.pack(side=LEFT, fill=Y, padx=12, pady=12)

content = Frame(main, bg="#ffffff")
content.pack(side=LEFT, fill=BOTH, expand=True, padx=12, pady=12)

# Botones (mantener textos similares)
buttons = [
    ("1. Crear nuevo vuelo", Crear_nuevo_vuelo),
    ("2. Origen/destino y precio al vuelo", origen_destino_precio),
    ("3. Ver estado del vuelo", estado_vuelo),
    ("4. Reservar asientos", reservar_asiento),
    ("5. Cancelar reserva", cancelar_reserva),
    ("6. Ver estadística de ocupación", estadistica_ocupacion),
    ("7. Ver estadística de recaudación", estadistica_recaudacion),
    ("8. Buscar vuelo por destino", buscar_vuelos_por_destino_ui),
    ("9. Vuelos disponibles", vuelos_disponibles),
    ("10. Reservar varios asientos", Reservar_varios_asientos_consecutivos),
    ("11. Simular venta masiva", Simular_venta_masiva),
    ("12. Reiniciar vuelo", Reiniciar_vuelo),
    ("13. Salir", root.quit)
]

# colocar botones en 3 columnas
cols = 3
for c in range(cols):
    sidebar.columnconfigure(c, weight=1, uniform="col")

for idx, (text, cmd) in enumerate(buttons):
    r = idx // cols
    
    if idx == len(buttons) - 1:
        c = cols // 2
    else:
        c = idx % cols
    btn = ttk.Button(sidebar, text=text, command=cmd, width=28)
    btn.grid(row=r, column=c, padx=6, pady=6, sticky="ew")

root.mainloop()