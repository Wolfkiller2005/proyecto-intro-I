from tkinter import *
from tkinter import simpledialog, messagebox

vuelos = []          # lista global con todos los vuelos
contador_vuelos = 1  

def Crear_nuevo_vuelo():
    global contador_vuelos, vuelos

    filas = simpledialog.askinteger("Crear vuelo", "Cantidad de filas:")

    # Validaciones -- -- -- -- -- -- -- -- -- --
    if filas is None:
        return
    
    if filas >  50:
        messagebox.showerror("Error","Numero de filas invalidas, no puden pasar de 50")
        return
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    columnas = simpledialog.askinteger("Crear vuelo", "Cantidad de columnas:")

    # Validaciones -- -- -- -- -- -- -- -- -- --
    if columnas is None:
        return

    if columnas >  20:
        messagebox.showerror("Error","Numero de columnas invalidas, no puden pasar de 20")
        return

    if not filas or not columnas or filas < 1 or columnas < 1:
        messagebox.showerror("Error", "Datos inválidos.")
        return
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
    
    num_vuelo = simpledialog.askinteger("Asignar datos", "Número interno del vuelo:")

    # Validaciones -- -- -- -- -- -- -- -- -- --
    if num_vuelo is None:
        return

    if num_vuelo < 1 or num_vuelo > len(vuelos):
        messagebox.showerror("Error", "Número de vuelo inválido.")
        return
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    vuelo = vuelos[num_vuelo - 1]  # La lista empieza en el indice 0

    codigo = simpledialog.askstring("Código", "Ingrese el código del vuelo (ej. CM123):")
    if codigo is None:
        return
    
    origen = simpledialog.askstring("Origen", "Ingrese el origen:")
    if origen is None:
        return

    destino = simpledialog.askstring("Destino", "Ingrese el destino:")
    if destino is None:
        return
    
    precio = simpledialog.askinteger("Precio", "Ingrese el precio del boleto:")
    if precio is None:
        return


    



#Ventana Principal
ventana = Tk()
ventana.title("Sistema de reserva de vuelos")

# Definir tamaño
ventana.geometry("175x170")
ventana.resizable(False, False)




#botones
Button(ventana, text="1. Crear nuevo vuelo", command=Crear_nuevo_vuelo).place(x=25, y=25, width=125, height=50)
Button(ventana, text="1. Origen del vuelo", command=origen_destino_precio).place(x=25, y=80, width=125, height=50)

ventana.mainloop()