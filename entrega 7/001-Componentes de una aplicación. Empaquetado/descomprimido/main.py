import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ExifTags  # Para trabajar con imágenes y extraer EXIF
from datetime import datetime

class PhotoRenamerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Photo Renamer")
        self.geometry("600x400")  # Aumentamos un poco la altura para el nuevo botón
        self.resizable(False, False)
        
        # -- Logo --
        # Intenta cargar un logo; si falla, simplemente no se muestra
        try:
            # Asegúrate de que 'download.jpg' exista o cambia la ruta
            self.logo_image = tk.PhotoImage(file="download.jpg")
            self.logo_label = tk.Label(self, image=self.logo_image)
            self.logo_label.pack(pady=10)
        except Exception:
            pass  # No mostrar logo si ocurre algún error
        
        # -- Variable para almacenar la ruta de la carpeta seleccionada --
        self.folder_path = tk.StringVar()
        
        # -- Botón para seleccionar la carpeta destino --
        self.select_folder_button = ttk.Button(
            self, 
            text="Select Target Folder", 
            command=self.select_folder
        )
        self.select_folder_button.pack(pady=5)
        
        # -- Botón para Previsualizar el renombrado (NUEVA FUNCIÓN) --
        self.preview_button = ttk.Button(
            self,
            text="Preview Renaming",
            command=self.preview_renaming
        )
        self.preview_button.pack(pady=5)
        
        # -- Botón para iniciar el proceso de renombrado --
        self.start_button = ttk.Button(
            self, 
            text="Start Renaming", 
            command=self.start_renaming
        )
        self.start_button.pack(pady=5)
        
        # -- Etiqueta para mostrar el progreso --
        self.progress_label = tk.Label(self, text="Progress:")
        self.progress_label.pack(pady=(20, 0))
        
        # -- Barra de progreso --
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self, 
            orient="horizontal", 
            length=300, 
            mode="determinate", 
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack()
        
    def select_folder(self):
        """
        Abre un cuadro de diálogo para seleccionar la carpeta destino.
        Si se selecciona una carpeta, se guarda en self.folder_path y se muestra un mensaje.
        """
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.folder_path.set(selected_folder)
            messagebox.showinfo("Folder Selected", f"Selected folder:\n{selected_folder}")
        
    def start_renaming(self):
        """
        Inicia el proceso de renombrado.
        Verifica que se haya seleccionado una carpeta y luego llama a rename_photos.
        """
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("No Folder Selected", "Please select a folder first.")
            return
        
        self.rename_photos(folder)
    
    def preview_renaming(self):
        """
        NUEVA FUNCIÓN: Muestra una ventana con la previsualización de los nuevos nombres
        que se asignarían a cada imagen según sus metadatos EXIF.
        """
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("No Folder Selected", "Please select a folder first.")
            return
        
        # Obtener lista de imágenes con extensiones válidas
        extensions = (".jpg", ".jpeg", ".png")
        all_files = os.listdir(folder)
        images = [f for f in all_files if f.lower().endswith(extensions)]
        
        if not images:
            messagebox.showinfo("No Images Found", "No JPG/PNG images found in the selected folder.")
            return
        
        # Construir la lista de previsualización
        preview_lines = []
        for image_name in images:
            old_path = os.path.join(folder, image_name)
            new_filename = self.get_new_filename(old_path, image_name)
            if new_filename and new_filename != image_name:
                preview_lines.append(f"{image_name}  ->  {new_filename}")
            else:
                preview_lines.append(f"{image_name}  ->  (no change)")
        
        # Crear una nueva ventana para mostrar la previsualización
        preview_window = tk.Toplevel(self)
        preview_window.title("Preview Renaming")
        preview_window.geometry("400x300")
        
        preview_text = tk.Text(preview_window, wrap="word")
        preview_text.pack(expand=True, fill="both", padx=10, pady=10)
        
        preview_text.insert("end", "\n".join(preview_lines))
        preview_text.config(state="disabled")  # No permitir edición
        
    def rename_photos(self, folder):
        """
        Recorre todos los archivos de imagen en la carpeta y, basándose en el EXIF,
        intenta renombrarlos a un formato 'YYYYMMDD_HHMMSS.ext'.
        Si no se encuentra información EXIF relevante, mantiene el nombre original.
        """
        # Obtener lista de imágenes
        extensions = (".jpg", ".jpeg", ".png")
        all_files = os.listdir(folder)
        images = [f for f in all_files if f.lower().endswith(extensions)]
        
        total_images = len(images)
        if total_images == 0:
            messagebox.showinfo("No Images Found", "No JPG/PNG images found in the selected folder.")
            return
        
        # Recorrer cada imagen y procesar el renombrado
        for i, image_name in enumerate(images, start=1):
            old_path = os.path.join(folder, image_name)
            new_filename = self.get_new_filename(old_path, image_name)
            
            # Renombrar solo si se generó un nuevo nombre distinto al original
            if new_filename and new_filename != image_name:
                new_path = os.path.join(folder, new_filename)
                
                # Si ya existe un archivo con el nuevo nombre, se salta para evitar colisiones
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
            
            # Actualizar la barra de progreso
            progress_percent = (i / total_images) * 100
            self.progress_var.set(progress_percent)
            self.update_idletasks()
        
        messagebox.showinfo("Done", "Renaming operation completed.")
        
    def get_new_filename(self, file_path, original_filename):
        """
        Intenta extraer la fecha y hora original ('DateTimeOriginal') de los metadatos EXIF.
        Si se encuentra, devuelve un nuevo nombre formateado como 'YYYYMMDD_HHMMSS.ext'.
        Si no, devuelve el nombre original.
        """
        try:
            img = Image.open(file_path)
            exif_data = img._getexif()
            
            if exif_data is None:
                return original_filename  # No hay datos EXIF
            
            # Convertir las etiquetas EXIF a nombres legibles
            exif_dict = {
                ExifTags.TAGS.get(tag_id, tag_id): value
                for tag_id, value in exif_data.items()
            }
            
            # Buscar la etiqueta 'DateTimeOriginal'
            date_str = exif_dict.get('DateTimeOriginal', None)
            if not date_str:
                return original_filename  # Si no existe, se mantiene el nombre
            
            # Parsear la cadena de fecha (formato "YYYY:MM:DD HH:MM:SS")
            date_time_obj = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
            new_basename = date_time_obj.strftime("%Y%m%d_%H%M%S")
            
            # Conservar la extensión original en minúsculas
            _, ext = os.path.splitext(original_filename)
            new_filename = new_basename + ext.lower()
            
            return new_filename
        
        except Exception:
            # Si ocurre algún error (por ejemplo, en la lectura de EXIF o el parseo), se retorna el nombre original
            return original_filename


if __name__ == "__main__":
    app = PhotoRenamerApp()
    app.mainloop()
