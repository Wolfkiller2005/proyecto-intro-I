import tkinter as tk
from tkinter import simpledialog, messagebox
# - - - FUNCIONES - - -
salas = []
contador_salas = 1

def obtener_letra_fila(n):
    letras = ""
    while True:
        n, r = divmod(n, 26)
        letras = chr(65 + r) + letras
        if n == 0:
            break
        n -= 1
    return letras

def crear_sala():
    global contador_salas
    filas = simpledialog.askinteger("Crear sala", "Cantidad de filas:")
    columnas = simpledialog.askinteger("Crear sala", "Cantidad de columnas:")
    if not filas or not columnas or filas < 1 or columnas < 1:
        messagebox.showerror("Error", "Datos inválidos.")
        return
    matriz = [[False for _ in range(columnas)] for _ in range(filas)]
    sala = [contador_salas, "", 0, matriz, 0, filas, columnas]
    salas.append(sala)
    messagebox.showinfo("Sala creada", f"¡Sala {contador_salas} creada exitosamente!")
    contador_salas += 1

def asignar_pelicula():
    if not salas:
        messagebox.showerror("Error", "No hay salas.")
        return
    num = simpledialog.askinteger("Asignar", "Número de sala:")
    sala = next((s for s in salas if s[0] == num), None)
    if not sala:
        messagebox.showerror("Error", "Sala no existe.")
        return
    nombre = simpledialog.askstring("Película", "Nombre de la película:")
    precio = simpledialog.askinteger("Precio", "Precio del boleto:")
    if not nombre or precio is None or precio < 0:
        messagebox.showerror("Error", "Datos inválidos.")
        return
    sala[1] = nombre
    sala[2] = precio
    messagebox.showinfo("Éxito", f"Película y precio asignados a sala {num}.")

def mostrar_estado_sala():
    if not salas:
        messagebox.showerror("Error", "No hay salas.")
        return
    num = simpledialog.askinteger("Estado", "Número de sala:")
    sala = next((s for s in salas if s[0] == num), None)
    if not sala:
        messagebox.showerror("Error", "Sala no existe.")
        return
    matriz = sala[3]
    filas, columnas = sala[5], sala[6]
    tamaño = 12
    margen = 28

    ventana_estado = tk.Toplevel()
    ventana_estado.title(f"Estado de la sala {num}")
    canvas = tk.Canvas(ventana_estado, width=columnas*tamaño + margen, height=filas*tamaño + margen)
    canvas.pack()

    canvas.create_text(margen + (columnas*tamaño)//2, 10, text="PANTALLA", font=("Arial", 9, "bold"))

    for j in range(columnas):
        canvas.create_text(margen + j*tamaño + tamaño//2, margen-10, text=str(j+1), fill="black", font=("Arial", 8))

    for i in range(filas):
        letra = obtener_letra_fila(i)
        canvas.create_text(margen-12, margen + i*tamaño + tamaño//2, text=letra, fill="black", font=("Arial", 8))

    for i in range(filas):
        for j in range(columnas):
            x, y = margen + j*tamaño, margen + i*tamaño
            color = "white" if not matriz[i][j] else "gray"
            canvas.create_rectangle(x, y, x+tamaño, y+tamaño, fill=color, outline="black")
            if matriz[i][j]:
                canvas.create_text(x+tamaño//2, y+tamaño//2, text="X", fill="black", font=("Arial", 7, "bold"))

    total = filas * columnas
    ocupados = sum(seat for row in matriz for seat in row)
    porcentaje = (ocupados / total) * 100 if total else 0
    info = f"Asientos: {total}\nOcupados: {ocupados}\n% Ocupación: {porcentaje:.1f}%"
    label = tk.Label(ventana_estado, text=info, font=("Arial", 9))
    label.pack(pady=10)

def reservar_asiento():
    if not salas:
        messagebox.showerror("Error", "No hay salas.")
        return
    num = simpledialog.askinteger("Sala", "Número de sala:")
    sala = next((s for s in salas if s[0] == num), None)
    if not sala:
        messagebox.showerror("Error", "Sala no existe.")
        return
    fila_letra = simpledialog.askstring("Fila", "Letra de fila:").upper()
    columna = simpledialog.askinteger("Columna", "Número de columna:")

    def letra_a_indice(letra):
        res = 0
        for c in letra:
            res = res * 26 + (ord(c) - 65 + 1)
        return res - 1
    i = letra_a_indice(fila_letra)
    j = columna - 1
    if 0 <= i < sala[5] and 0 <= j < sala[6]:
        if not sala[3][i][j]:
            sala[3][i][j] = True
            sala[4] += 1
            messagebox.showinfo("Éxito", f"Asiento {fila_letra}{columna} reservado.")
        else:
            messagebox.showerror("Ocupado", "El asiento ya está reservado.")
    else:
        messagebox.showerror("Error", "Asiento inválido.")

def cancelar_reserva():
    if not salas:
        messagebox.showerror("Error", "No hay salas.")
        return
    num = simpledialog.askinteger("Sala", "Número de sala:")
    sala = next((s for s in salas if s[0] == num), None)
    if not sala:
        messagebox.showerror("Error", "Sala no existe.")
        return
    fila_letra = simpledialog.askstring("Fila", "Letra de fila:").upper()
    columna = simpledialog.askinteger("Columna", "Número de columna:")
    def letra_a_indice(letra):
        res = 0
        for c in letra:
            res = res * 26 + (ord(c) - 65 + 1)
        return res - 1
    i = letra_a_indice(fila_letra)
    j = columna - 1
    if 0 <= i < sala[5] and 0 <= j < sala[6]:
        if sala[3][i][j]:
            sala[3][i][j] = False
            sala[4] -= 1
            messagebox.showinfo("Éxito", f"Reserva del asiento {fila_letra}{columna} cancelada.")
        else:
            messagebox.showerror("Error", "El asiento no estaba reservado.")
    else:
        messagebox.showerror("Error", "Asiento inválido.")

def estadisticas_ocupacion():
    if not salas:
        messagebox.showerror("Error", "No hay salas.")
        return
    num = simpledialog.askinteger("Ocupación", "Número de sala:")
    sala = next((s for s in salas if s[0] == num), None)
    if not sala:
        messagebox.showerror("Error", "Sala no existe.")
        return
    total = sala[5] * sala[6]
    reservados = sala[4]
    porcentaje = (reservados / total) * 100 if total else 0
    messagebox.showinfo("Ocupación", f"Sala {num} - {sala[1]}\nAsientos totales: {total}\nReservados: {reservados}\nPorcentaje de ocupación: {porcentaje:.2f}%")

def estadisticas_recaudacion():
    if not salas:
        messagebox.showerror("Error", "No hay salas.")
        return
    num = simpledialog.askinteger("Recaudación", "Número de sala:")
    sala = next((s for s in salas if s[0] == num), None)
    if not sala:
        messagebox.showerror("Error", "Sala no existe.")
        return
    total = sala[4] * sala[2]
    messagebox.showinfo("Recaudación", f"Sala {num} - {sala[1]}\nEntradas vendidas: {sala[4]}\nPrecio por entrada: {sala[2]}\nTotal recaudado: {total}")

# - - - VENTANA - - -
ventana = tk.Tk()
ventana.title("Sistema de Reserva de Cine")

# - - - BOTONES - - -
tk.Button(ventana, text="1. Crear Sala", command=crear_sala).pack(fill="x")
tk.Button(ventana, text="2. Asignar Película y Precio", command=asignar_pelicula).pack(fill="x")
tk.Button(ventana, text="3. Ver Estado de Sala", command=mostrar_estado_sala).pack(fill="x")
tk.Button(ventana, text="4. Reservar Asiento", command=reservar_asiento).pack(fill="x")
tk.Button(ventana, text="5. Cancelar Reserva", command=cancelar_reserva).pack(fill="x")
tk.Button(ventana, text="6. Estadísticas Ocupación", command=estadisticas_ocupacion).pack(fill="x")
tk.Button(ventana, text="7. Estadísticas Recaudación", command=estadisticas_recaudacion).pack(fill="x")
tk.Button(ventana, text="13. Salir", command=ventana.quit).pack(fill="x")

ventana.mainloop()