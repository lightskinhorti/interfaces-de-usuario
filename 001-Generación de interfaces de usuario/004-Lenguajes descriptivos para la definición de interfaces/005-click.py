import tkinter as tk

ventana = tk.Tk()

def disparo():
    print("bang!")

tk.Button(ventana,text="Boton",padx=15,pady=15,command=disparo).pack(padx=40,pady=40)

ventana.mainloop()
