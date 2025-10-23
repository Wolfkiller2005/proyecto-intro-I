import tkinter as tk

ventana = tk.Tk()
ventana.geometry("300x200")

# Botón colocado en (50, 50)
tk.Button(ventana, text="Botón en (50,50)").place(x=50, y=50)

# Otro botón en (150, 100)
tk.Button(ventana, text="Botón en (150,100)").place(x=150, y=100)

ventana.mainloop()