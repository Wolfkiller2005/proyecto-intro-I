from tkinter import *
from tkinter import simpledialog, messagebox

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
    vuelo = [f"V{contador_vuelos}", "", "", 0, matriz, 0, filas, columnas]

    vuelos.append(vuelo)

    messagebox.showinfo("Vuelo creado", f"¡Vuelo {contador_vuelos} creado exitosamente!")
    contador_vuelos += 1



def origen_destino_precio():

    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return
    
    while True:
        num_vuelo = simpledialog.askinteger("Asignar datos", "Número interno del vuelo:")

        # Validaciones -- -- -- -- -- -- -- -- -- --
        if num_vuelo is None:
            return

        if num_vuelo < 1 or num_vuelo > len(vuelos):
            messagebox.showerror("Error", "Número de vuelo inválido.")
           
        else:
            break
        # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

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

    messagebox.showinfo("Vuelo creado", f"Datos del vuelo {num_vuelo} asignados correctamente")

def estado_vuelo():
    
    if not vuelos:
        messagebox.showerror("Error", "No hay vuelos disponibles.")
        return
    
    while True:
        num_vuelo = simpledialog.askinteger("Estado del vuelo", "Ingrese el número de vuelo:")

        # Validaciones -- -- -- -- -- -- -- -- -- --
        if num_vuelo is None:
            return

        if num_vuelo < 1 or num_vuelo > len(vuelos):
            messagebox.showerror("Error", "Número de vuelo inválido.")
           
        else:
            break
        # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

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

    for j in range(columnas):
        canvas.create_text(margen + j*tamaño + tamaño//2, margen_superior-10, text=str(j+1), fill="black", font=("Arial", 8))

    for i in range(filas):

        letra = obtener_letra_fila(i)

        canvas.create_text(margen-12, margen_superior + i*tamaño + tamaño//2, text=letra, fill="black", font=("Arial", 8))

    #dibuja la matriz de asientos
    for i in range(filas):
        for j in range(columnas):

            x = margen + j*tamaño
            y = margen_superior + i*tamaño
            color = "white" if not matriz[i][j] else "gray"
            canvas.create_rectangle(x, y, x+tamaño, y+tamaño, fill=color, outline="black")

            if matriz[i][j]:
                canvas.create_text(x+tamaño//2, y+tamaño//2, text="X", fill="black", font=("Arial", 7, "bold"))
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    #Estadisticas -- -- -- -- -- -- -- --
    total = filas * columnas
    ocupados = sum(seat for row in matriz for seat in row)
    porcentaje = (ocupados / total) * 100 if total else 0
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    info = f"Asientos: {total}\nOcupados: {ocupados}\n% Ocupación: {porcentaje:.1f}%"
    label = Label(ventana_estado, text=info, font=("Arial", 9))
    label.pack(pady=10)



#Ventana Principal
ventana = Tk()
ventana.title("Sistema de reserva de vuelos")

# Definir tamaño
ventana.geometry("375x375")
ventana.resizable(False, False)




#botones
Button(ventana, text="1. Crear nuevo vuelo", command=Crear_nuevo_vuelo).place(x=25, y=25, width=125, height=50)
Button(ventana, text="2. Asignar origen/destino y precio al vuelo", command=origen_destino_precio).place(x=25, y=80, width=245, height=50)
Button(ventana, text="3. ver estado del vuelo", command=estado_vuelo).place(x=25, y=135, width=125, height=50)

ventana.mainloop()