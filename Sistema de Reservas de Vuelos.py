from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter import ttk

vuelos = []          # lista global con todos los vuelos
contador_vuelos = 1  

#funcion para obtener las letras de los asientos
def obtener_letra_fila(n):
    letras = ""
    while True:
        n, r = divmod(n, 26)
        letras = chr(65 + r) + letras
        if n == 0:
            break
        n -= 1
    return letras

# Funcion para seleccionar el vuelo sin tener que escribirlo
def seleccionar_vuelo():
    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return None
    
    # Crear una ventana para seleccionar
    ventana_seleccion = Toplevel()
    ventana_seleccion.title("Seleccionar Vuelo")
    ventana_seleccion.grab_set()
    ventana_seleccion.transient(ventana_seleccion.master)
    
    Label(ventana_seleccion, text="Seleccione el número del vuelo:").pack(padx=10, pady=(10,0))
    
    # Crear lista de vuelos disponibles mostrando número
    opciones = [f"{i+1} — {vuelos[i][0]}" for i in range(len(vuelos))]
    
    combo = ttk.Combobox(ventana_seleccion, values=opciones, state="readonly", width=25)
    combo.set("Seleccione un vuelo")
    combo.pack(padx=20, pady=10)
    
    # Variable para almacenar la selección
    seleccion = None
    
    def confirmar():
        nonlocal seleccion
        if combo.get() != "Seleccione un vuelo":
            seleccion = int(combo.get().split('—')[0].strip())
            ventana_seleccion.destroy()
    
    # Botón de confirmar
    Button(ventana_seleccion, text="Confirmar", command=confirmar).pack(pady=(0,10))
    
    # Esperar hasta que se cierre la ventana
    ventana_seleccion.wait_window()
    
    return seleccion

def Crear_nuevo_vuelo():

    global contador_vuelos, vuelos

    while True:
        filas = simpledialog.askinteger("Crear vuelo", "Cantidad de filas:")

        # Validaciones -- -- -- -- -- -- -- -- -- --
        if filas is None:
            return

        if filas >  50:
            messagebox.showerror("Error","Numero de filas invalidas, no puden pasar de 50")
            
        else:
            break
        # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    while True:

        columnas = simpledialog.askinteger("Crear vuelo", "Cantidad de columnas:")

        # Validaciones -- -- -- -- -- -- -- -- -- --
        if columnas is None:
            return

        elif columnas >  20:
            messagebox.showerror("Error","Numero de columnas invalidas, no puden pasar de 20")

        elif filas >= 1 and columnas >= 1 and filas <= 50 and columnas <= 20:
            break
            
        else:
            messagebox.showerror("Error", "Datos inválidos.")
        # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    # matriz de asientos (False = libre, True = reservado)
    matriz = [[False for _ in range(columnas)] for _ in range(filas)]

    # vuelo individual
    vuelo = [
        "V1",      # ID del vuelo
        "",        # Origen 
        "",        # Destino
        0,         # Precio
        matriz,    # Matriz de asientos
        0,         # Reservas
        filas,     # Número de filas
        columnas   # Número de columnas
        ]

    vuelos.append(vuelo)

    messagebox.showinfo("Vuelo creado", f"¡Vuelo {contador_vuelos} creado exitosamente!")
    contador_vuelos += 1



def origen_destino_precio():

    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return
    
    # Usar la ventana de selección para obtener el número interno
    num_vuelo = seleccionar_vuelo()
    if num_vuelo is None:
        return

    vuelo = vuelos[num_vuelo - 1]  # La lista empieza en el indice 0

    while True:

        codigo = simpledialog.askstring("Código", "Ingrese el código del vuelo (ej. CM123):")

        # Validaciones -- -- -- -- -- -- -- -- -- --
        if codigo is None:
            return
        
        if codigo.strip() != "":
            break

        else:
            messagebox.showerror("Error", "El código no puede estar vacío.")
        # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    while True:

        origen = simpledialog.askstring("Origen", "Ingrese el origen:")

        # Validaciones -- -- -- -- -- -- -- -- -- --
        if origen is None:
            return

        # Validar que solo tenga letras y espacios
        if not all(palabra.isalpha() for palabra in origen.split()):
            messagebox.showerror("Error", "El origen solo debe contener letras y espacios.")
            
        else:
            break
        # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    while True:

        destino = simpledialog.askstring("Destino", "Ingrese el destino:")

        # Validaciones -- -- -- -- -- -- -- -- -- --
        if destino is None:
            return

        if not all(palabra.isalpha() for palabra in destino.split()):
            messagebox.showerror("Error", "El destino solo debe contener letras y espacios.")
        
        else:
             break
        # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    while True:

        precio = simpledialog.askinteger("Precio", "Ingrese el precio del boleto:")

        # Validaciones -- -- -- -- -- -- -- -- -- --
        if precio is None:
            return
        
        if precio < 1:
            messagebox.showerror("Error","El precio no puede ser 0 o menor a 0")

        else:
            break
        # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    vuelo[0] = codigo       
    vuelo[1] = origen
    vuelo[2] = destino
    vuelo[3] = precio

    messagebox.showinfo("Vuelo creado", f"Datos del vuelo {num_vuelo} asignados correctamente")


def estado_vuelo():
    
    num_vuelo = seleccionar_vuelo()
    if num_vuelo is None:
        return

    vuelo = vuelos[num_vuelo - 1]  #inicia con indice 0
    matriz = vuelo[4]
    filas, columnas = vuelo[6], vuelo[7]
    tamaño = 12
    margen = 28
    margen_superior = 40

    ventana_estado = Toplevel()
    ventana_estado.title(f"Estado del vuelo {num_vuelo}")
    canvas = Canvas(ventana_estado, width=columnas*tamaño + margen, height=filas*tamaño + margen + margen_superior)
    canvas.pack()
    canvas.create_text(margen + (columnas*tamaño)//2, 10, text="VUELO", font=("Arial", 9, "bold"))
    ventana_estado.grab_set()
    ventana_estado.transient(ventana_estado.master)

    #Creación de los numeros de las columnas
    for j in range(columnas):
        canvas.create_text(margen + j*tamaño + tamaño//2, margen_superior-10, text=str(j+1), fill="black", font=("Arial", 8))

    #Creación de las letras de las filas
    for i in range(filas):

        letra = obtener_letra_fila(i)

        canvas.create_text(margen-12, margen_superior + i*tamaño + tamaño//2, text=letra, fill="black", font=("Arial", 8))

    #Dibuja la matriz de asientos
    for i in range(filas):
        for j in range(columnas):

            x = margen + j*tamaño
            y = margen_superior + i*tamaño
            color = "white" if not matriz[i][j] else "gray"
            canvas.create_rectangle(x, y, x+tamaño, y+tamaño, fill=color, outline="black")

            if matriz[i][j]:
                canvas.create_text(x+tamaño//2, y+tamaño//2, text="X", fill="black", font=("Arial", 7, "bold"))

    #Estadisticas -- -- -- -- -- -- -- --
    total = filas * columnas
    ocupados = sum(seat for row in matriz for seat in row)
    porcentaje = (ocupados / total) * 100 if total else 0
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    info = f"Asientos: {total}\nOcupados: {ocupados}\n% Ocupación: {porcentaje:.1f}%"
    label = Label(ventana_estado, text=info, font=("Arial", 9))
    label.pack(pady=10)

def reservar_asiento():

    num_vuelo = seleccionar_vuelo()
    if num_vuelo is None:
        return

    vuelo = vuelos[num_vuelo - 1]
    matriz = vuelo[4]
    filas, columnas = vuelo[6], vuelo[7]

    # construir lista de asientos libres con etiqueta "A1", "B3", ...
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
    ventana.title(f"Seleccionar asiento - Vuelo {num_vuelo}")
    ventana.grab_set()
    ventana.transient(ventana.master)
    Label(ventana, text="Seleccione un asiento disponible:").pack(padx=10, pady=(10,0))

    # combobox con solo las etiquetas
    valores = [a[2] for a in asientos_libres]
    combo = ttk.Combobox(ventana, values=valores, state="readonly", width=10)
    combo.set("Seleccione")
    combo.pack(padx=10, pady=10)

    def confirmar():
        sel = combo.get()
        if sel == "" or sel == "Seleccione":
            messagebox.showerror("Error", "Seleccione un asiento.")
            return
        # buscar indices del asiento seleccionado
        for fila_idx, col_idx, etiqueta in asientos_libres:
            if etiqueta == sel:
                matriz[fila_idx][col_idx] = True           # marcar reservado
                vuelo[5] = vuelo[5] + 1                    # incrementar contador reservas (índice 5)
                messagebox.showinfo("Reservado", f"Asiento {sel} reservado correctamente.")
                ventana.destroy()
                return

    Button(ventana, text="Confirmar", command=confirmar).pack(pady=(0,10))

def cancelar_reserva():

    num_vuelo = seleccionar_vuelo()
    if num_vuelo is None:
        return
    
    vuelo = vuelos[num_vuelo - 1]

    if vuelo[5] == 0:
        messagebox.showerror("ERROR","el vuelo no tiene asientos reservados")
        return
    
    # Lista para guardar asientos ocupados
    ocupados = []
    matriz = vuelo[4]
    filas = vuelo[6]
    columnas = vuelo[7]

    # Guardar índices y etiqueta
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == True:
                letra = chr(65 + i)
                numero = j + 1
                etiqueta = f"{letra}{numero}"
                ocupados.append((i, j, etiqueta))

    ventana_reservados = Toplevel()
    ventana_reservados.title(f"Asientos Ocupados - vuelo {num_vuelo}")
    ventana_reservados.grab_set()
    ventana_reservados.transient(ventana_reservados.master)

    # Mostrar solo las etiquetas en el combobox
    valores = [asiento[2] for asiento in ocupados]
    lista = ttk.Combobox(ventana_reservados, values=valores, state="readonly")
    lista.set("Seleccione asiento")
    lista.pack(padx=20, pady=20)

    def confirmar():
        sel = lista.get()
        if sel == "" or sel == "Seleccione asiento":
            messagebox.showerror("Error", "Seleccione un asiento.")
            return
        
        # buscar indices del asiento seleccionado
        for fila_idx, col_idx, etiqueta in ocupados:
            if etiqueta == sel:
                matriz[fila_idx][col_idx] = False  # liberar asiento
                vuelo[5] = vuelo[5] - 1  # decrementar reservas
                messagebox.showinfo("Cancelado", f"Reserva del asiento {sel} cancelada correctamente.")
                ventana_reservados.destroy()
                return
            
    Button(ventana_reservados, text="Confirmar", command=confirmar).pack(pady=(0,10))    

def estadistica_ocupacion():

    num_vuelo = seleccionar_vuelo()
    if num_vuelo is None:
        return

    vuelo = vuelos[num_vuelo - 1]
    id = vuelo[0]
    origen = vuelo[1]
    destino = vuelo[2]
    filas, columnas = vuelo[6], vuelo[7]

    total = filas * columnas
    ocupados = vuelo[5]
    porcentaje = (ocupados / total) * 100 if total else 0

    messagebox.showinfo("Estadisticas de ocupacion", f"numero interno: {id} \nsalida/destino: {origen} → {destino} \nAsientos: {total}\nOcupados: {ocupados}\n% Ocupación: {porcentaje:.1f}%")

def estadistica_recaudacion():

    num_vuelo = seleccionar_vuelo()
    if num_vuelo is None:
        return

    vuelo = vuelos[num_vuelo - 1]
    id = vuelo[0]
    origen = vuelo[1]
    destino = vuelo[2]
    precio = vuelo[3]
    reservas = vuelo[5]
 
    messagebox.showinfo("Estadisticas de ocupacion", f"numero interno: {id} \nsalida/destino: {origen} → {destino} \nEntradas vendidas: {reservas} \nprecio del boleto: {precio} \ntotal recaudado: {(precio*reservas)} ")

def obtener_vuelos_por_destino(destino):
    if destino is None:
        return []
    destino = destino.strip().lower()
    resultados = []
    for i, vuelo in enumerate(vuelos, 1):
        if isinstance(vuelo, (list, tuple)) and len(vuelo) > 2:
            if isinstance(vuelo[2], str) and vuelo[2].strip().lower() == destino:
                resultados.append((i, vuelo))
    return resultados


def buscar_vuelos_por_destino_ui():
    # Crear ventana para mostrar destinos y búsqueda
    ventana_busqueda = Toplevel()
    ventana_busqueda.title("Búsqueda por destino")
    ventana_busqueda.grab_set()
    ventana_busqueda.transient(ventana_busqueda.master)

    # Frame izquierdo para destinos disponibles
    frame_destinos = Frame(ventana_busqueda)
    frame_destinos.pack(side=LEFT, padx=10, pady=10)
    
    Label(frame_destinos, text="Destinos disponibles:", font=("Arial", 9, "bold")).pack()
    
    # Obtener destinos únicos
    destinos = set()
    for vuelo in vuelos:
        if vuelo[2]:  # Si el destino no está vacío
            destinos.add(vuelo[2])
    
    # Mostrar destinos en listbox
    listbox_destinos = Listbox(frame_destinos, width=20, height=10)
    for destino in sorted(destinos):
        listbox_destinos.insert(END, destino)
    listbox_destinos.pack(pady=5)

    # Frame derecho para búsqueda
    frame_busqueda = Frame(ventana_busqueda)
    frame_busqueda.pack(side=LEFT, padx=10, pady=10)
    
    Label(frame_busqueda, text="Ingrese el destino:").pack(pady=5)
    entrada = Entry(frame_busqueda)
    entrada.pack(pady=5)
    
    def buscar():
        destino = entrada.get().strip()
        if not destino:
            messagebox.showerror("Error", "Ingrese un destino")
            return
            
        resultados = obtener_vuelos_por_destino(destino)
        if not resultados:
            messagebox.showinfo("Resultados", f"No hay vuelos con destino: {destino}")
            return

        # Mostrar resultados en nueva ventana
        mostrar_resultados(destino, resultados)
    
    Button(frame_busqueda, text="Buscar", command=buscar).pack(pady=5)
    Button(frame_busqueda, text="Cerrar", command=ventana_busqueda.destroy).pack(pady=5)

def mostrar_resultados(destino, resultados):
    ventana = Toplevel()
    ventana.title(f"Vuelos a {destino}")
    ventana.grab_set()
    ventana.transient(ventana.master)

    listbox = Listbox(ventana, width=80)
    for num, vuelo in resultados:
        codigo = vuelo[0]
        origen = vuelo[1]
        dest = vuelo[2]
        precio = vuelo[3]
        matriz = vuelo[4]
        disponibles = sum(1 for fila in matriz for asiento in fila if not asiento)
        listbox.insert(END, f"{num} — {codigo} | {origen} → {dest} | ₡{precio} | Asientos disponibles: {disponibles}")
    listbox.pack(padx=10, pady=10)

    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=(0,10))

def vuelos_disponibles():
    if not vuelos:
        messagebox.showinfo("Vuelos Disponibles", "No hay vuelos registrados.")
        return
    
    ventana_vuelos = Toplevel()
    ventana_vuelos.title("Vuelos Disponibles")
    ventana_vuelos.grab_set()
    ventana_vuelos.transient(ventana_vuelos.master)
    
    # Crear (tabla) para mostrar los vuelos
    tabla = ttk.Treeview(ventana_vuelos, columns=("Número", "Código", "Origen", "Destino", "Precio"))
    
    # Configurar columnas
    tabla.heading("Número", text="Número")
    tabla.heading("Código", text="Código")
    tabla.heading("Origen", text="Origen")
    tabla.heading("Destino", text="Destino")
    tabla.heading("Precio", text="Precio")
    
    # Ocultar la primera columna vacía
    tabla.column("#0", width=0, stretch=NO)
    
    # Ajustar ancho de columnas
    tabla.column("Número", width=60)
    tabla.column("Código", width=100)
    tabla.column("Origen", width=100)
    tabla.column("Destino", width=100)
    tabla.column("Precio", width=100)
    
    # Insertar datos
    for i, vuelo in enumerate(vuelos, 1):
        tabla.insert("", END, values=(
            i,              # Número de vuelo
            vuelo[0],      # Código
            vuelo[1],      # Origen
            vuelo[2],      # Destino
            f"₡{vuelo[3]}" # Precio
        ))
    
    tabla.pack(padx=10, pady=10)
    
    # Botón para cerrar
    Button(ventana_vuelos, text="Cerrar", command=ventana_vuelos.destroy).pack(pady=10)


def Reiniciar_vuelo():

    num_vuelo = seleccionar_vuelo()
    if num_vuelo is None:
        return

    # Pedir confirmación
    if not messagebox.askyesno("Confirmar reinicio", f"¿Desea reiniciar el vuelo {num_vuelo} ({vuelo[0]})?"):
        return
    
    vuelo = vuelos[num_vuelo - 1]
    matriz = vuelo[4]
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz[i][j] = False
    
    vuelo[5] = 0

    messagebox.showinfo("Reinicio", f"Reinicio del vuelo {num_vuelo} ({vuelo[0]}) realizado correctamente.")

#Ventana Principal
ventana = Tk()
ventana.title("Sistema de reserva de vuelos")

# Definir tamaño
ventana.update_idletasks()
ventana.geometry("375x750+0+0")
ventana.resizable(False, False)

#botones
Button(ventana, text="1. Crear nuevo vuelo", command=Crear_nuevo_vuelo).place(x=25, y=25, width=125, height=50)
Button(ventana, text="2. Asignar origen/destino y precio al vuelo", command=origen_destino_precio).place(x=25, y=80, width=245, height=50)
Button(ventana, text="3. ver estado del vuelo", command=estado_vuelo).place(x=25, y=135, width=125, height=50)
Button(ventana, text="4. reservar asientos", command=reservar_asiento).place(x=25, y=190, width=125, height=50)
Button(ventana, text="5. cancelar reserva", command=cancelar_reserva).place(x=25, y=245, width=125, height=50)
Button(ventana, text="6. Ver estadistica de ocupacion", command=estadistica_ocupacion).place(x=25, y=300, width=245, height=50)
Button(ventana, text="7. Ver estadistica de recaudacion", command=estadistica_recaudacion).place(x=25, y=355, width=245, height=50)
Button(ventana, text="8. Buscar vuelo por destino", command=buscar_vuelos_por_destino_ui).place(x=25, y=410, width=245, height=50)
Button(ventana, text="9. Vuelos disponibles", command=vuelos_disponibles).place(x=25, y=465, width=125, height=50)


Button(ventana, text="12. Reiniciar vuelo", command=Reiniciar_vuelo).place(x=25, y=630, width=125, height=50)
Button(ventana, text="13. Salir", command=ventana.quit).place(x=25, y=685, width=245, height=50)
ventana.mainloop()