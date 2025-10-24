from tkinter import *
from tkinter import simpledialog, messagebox

vuelos = []          # lista global con todos los vuelos
contador_vuelos = 1  

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