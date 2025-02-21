import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import zipfile      # Para extraer archivos del paquete ZIP
import os           # Para operaciones del sistema de archivos
import threading    # Para ejecutar tareas en segundo plano sin bloquear la interfaz
import subprocess   # Para ejecutar comandos del sistema (ej. crear accesos directos o lanzar la aplicación)
import sys          # Para acceder al intérprete de Python
import platform     # Para detectar el sistema operativo
import shutil       # NUEVA FUNCIÓN: Verificar espacio libre en disco

# Intentar importar winshell y pywin32 para la creación de accesos directos en Windows.
# Si falla la importación, se deshabilita la funcionalidad en Windows.
try:
    import winshell
    from win32com.client import Dispatch
    WINDOWS_SHORTCUT_AVAILABLE = True
except ImportError:
    WINDOWS_SHORTCUT_AVAILABLE = False

###########################################################################
# Clase Installer
# Ventana principal del instalador, que administra las distintas pantallas.
###########################################################################
class Installer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg='#282828')  # Fondo oscuro para un look moderno
        
        self.title("Instalador")
        self.geometry("500x450")  # Tamaño fijo de la ventana
        self.resizable(False, False)  # La ventana no se puede redimensionar
        
        # Variable para almacenar la ruta de instalación; por defecto se usa el directorio actual
        self.install_path = tk.StringVar(value=os.getcwd())
        
        self.frames = {}  # Diccionario para almacenar las distintas pantallas del instalador
        
        # Crear e inicializar todas las pantallas del instalador
        for F in (WelcomeScreen, SelectFolderScreen, ProgressScreen, SuccessScreen):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Mostrar la pantalla de bienvenida inicialmente
        self.show_frame(WelcomeScreen)

    def show_frame(self, frame_class):
        """
        Muestra la pantalla indicada y, si tiene el método 'on_show', lo ejecuta.
        """
        frame = self.frames[frame_class]
        frame.tkraise()  # Lleva la pantalla al frente
        if hasattr(frame, 'on_show'):
            frame.on_show()

###########################################################################
# Clase WelcomeScreen
# Pantalla de bienvenida del instalador.
###########################################################################
class WelcomeScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#282828')
        
        # Mensaje de bienvenida
        title_label = tk.Label(self, text="Bienvenido al instalador de saturn",
                               font=("Arial", 16, "bold"), fg="white", bg="#282828")
        title_label.pack(pady=20)
        
        # Descripción breve del proceso de instalación
        description_label = tk.Label(self, text="Sigue los pasos para instalar\nel programa de Saturn.",
                                     fg="white", bg="#282828")
        description_label.pack(pady=10)
        
        # Botón "Next" para avanzar a la siguiente pantalla
        next_button = ttk.Button(self, text="Next", command=self.go_next)
        next_button.pack(pady=20)
        
        self.parent = parent

    def go_next(self):
        """Avanza a la siguiente pantalla (SelectFolderScreen)."""
        self.parent.show_frame(SelectFolderScreen)

###########################################################################
# Clase SelectFolderScreen
# Pantalla para seleccionar la carpeta de instalación.
###########################################################################
class SelectFolderScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#282828')
        
        # Instrucción para el usuario
        instruction_label = tk.Label(self, text="Seleccione la carpeta de instalación",
                                     font=("Arial", 12, "bold"), fg="white", bg="#282828")
        instruction_label.pack(pady=20)
        
        # Contenedor para el campo de entrada y botón "Buscar..."
        folder_frame = tk.Frame(self)
        folder_frame.pack(pady=5)
        
        # Campo de entrada para la ruta, con estilo personalizado
        self.folder_entry = tk.Entry(folder_frame, textvariable=parent.install_path, width=40,
                                     bg="#3c3c3c", fg="white", insertbackground="white")
        self.folder_entry.pack(side="left", padx=(0, 10))
        
        # Botón para abrir el explorador de archivos y seleccionar la carpeta
        browse_button = ttk.Button(folder_frame, text="Buscar...", command=self.browse_folder)
        browse_button.pack(side="left")
        
        # Etiqueta para mostrar mensajes de error si la carpeta no es válida
        self.error_label = tk.Label(self, text="", fg="red", font=("Arial", 10))
        self.error_label.pack(pady=5)
        
        # Botón "Next", inicialmente deshabilitado hasta que la carpeta sea válida
        self.next_button = ttk.Button(self, text="Next", command=self.go_next)
        self.next_button.pack(pady=20)
        self.next_button.config(state="disabled")
        
        self.parent = parent
        # Se añade un "trace" a la variable de la carpeta para validar cada cambio
        self.parent.install_path.trace_add('write', self.on_path_change)
        self.check_folder_empty()

    def browse_folder(self):
        """Abre el cuadro de diálogo para seleccionar una carpeta de instalación."""
        folder = filedialog.askdirectory(initialdir=os.getcwd(), title="Seleccionar carpeta de instalación")
        if folder:
            self.parent.install_path.set(folder)
    
    def on_path_change(self, *args):
        """Se ejecuta cada vez que cambia la ruta de instalación."""
        self.check_folder_empty()
    
    def check_folder_empty(self):
        """
        Verifica si la carpeta seleccionada está vacía.
        Habilita el botón "Next" solo si la carpeta está vacía y se tienen los permisos adecuados.
        """
        path = self.parent.install_path.get()
        if os.path.isdir(path):
            try:
                if not os.listdir(path):
                    self.next_button.config(state="normal")
                    self.error_label.config(text="")
                else:
                    self.next_button.config(state="disabled")
                    self.error_label.config(text="La carpeta seleccionada no está vacía. Seleccione otra.")
            except PermissionError:
                self.next_button.config(state="disabled")
                self.error_label.config(text="No tienes permisos para acceder a esta carpeta.")
        else:
            self.next_button.config(state="disabled")
            self.error_label.config(text="Ruta inválida.")

    def go_next(self):
        """Avanza a la pantalla de progreso."""
        self.parent.show_frame(ProgressScreen)

###########################################################################
# Clase ProgressScreen
# Pantalla que muestra el progreso de la extracción del archivo ZIP.
###########################################################################
class ProgressScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#282828')  # Fondo oscuro
        
        # Título de la pantalla de progreso
        title_label = tk.Label(self, text="Installing...", font=("Arial", 14, "bold"),
                               fg="white", bg="#282828")
        title_label.pack(pady=20)
        
        # Barra de progreso para mostrar el avance de la extracción
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)
        
        # Etiqueta para mostrar el estado actual de la extracción
        self.status_label = tk.Label(self, text="Preparing to install...", font=("Arial", 10),
                                     fg="white", bg="#282828")
        self.status_label.pack(pady=5)
        
        # Botón "Next" para avanzar, deshabilitado hasta que se complete la extracción
        self.next_button = ttk.Button(self, text="Next", command=self.go_next)
        self.next_button.pack(pady=20)
        self.next_button.config(state="disabled")
        
        self.parent = parent
        self.installation_started = False  # Evita iniciar la extracción varias veces

    def on_show(self):
        """
        Se ejecuta cuando se muestra esta pantalla.
        Inicia la extracción del paquete ZIP en un hilo separado para no bloquear la interfaz.
        """
        if not self.installation_started:
            self.installation_started = True
            threading.Thread(target=self.start_extraction, daemon=True).start()

    def check_disk_space(self, path, required_space):
        """
        NUEVA FUNCIÓN: Verifica si la carpeta 'path' tiene al menos 'required_space' bytes libres.
        Retorna True si hay suficiente espacio; de lo contrario, False.
        """
        try:
            usage = shutil.disk_usage(path)
            return usage.free >= required_space
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar espacio en disco:\n{str(e)}")
            return False

    def start_extraction(self):
        """
        Extrae el contenido del archivo ZIP (paquete.zip) en la carpeta de instalación.
        Actualiza la barra de progreso y muestra el estado de la extracción.
        Antes de comenzar, verifica que haya suficiente espacio en disco.
        """
        archivo_original = "paquete.zip"  # Nombre del archivo ZIP
        salida = self.parent.install_path.get()  # Carpeta de instalación seleccionada

        # Determinar la ruta completa del archivo ZIP, relativo al script actual
        script_dir = os.path.dirname(os.path.abspath(__file__))
        zip_path = os.path.join(script_dir, archivo_original)

        # Verificar que el archivo ZIP exista
        if not os.path.isfile(zip_path):
            messagebox.showerror("Error", f"Cannot find '{archivo_original}' in '{script_dir}'.")
            self.status_label.config(text="Installation failed.")
            return

        # Verificar que haya al menos 100 MB libres en la carpeta de instalación
        required_space = 100 * 1024 * 1024  # 100 MB
        if not self.check_disk_space(salida, required_space):
            messagebox.showerror("Error", "No hay suficiente espacio en disco para instalar el paquete.")
            self.status_label.config(text="Installation failed: insufficient disk space.")
            return

        try:
            with zipfile.ZipFile(zip_path, 'r') as zipped:
                # Obtener la lista de archivos para calcular el progreso
                file_list = zipped.namelist()
                total_files = len(file_list)
                
                # Extraer cada archivo y actualizar la barra de progreso y el estado
                for i, file in enumerate(file_list, start=1):
                    zipped.extract(file, salida)
                    progress_value = int((i / total_files) * 100)
                    self.progress["value"] = progress_value
                    self.status_label.config(text=f"Extracting {file} ({i}/{total_files})")
                    self.parent.update_idletasks()  # Actualiza la UI para mostrar los cambios
                
            # Si la extracción fue exitosa, se actualiza el estado y se habilita el botón para continuar
            self.status_label.config(text="Extraction completed.")
            self.next_button.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during extraction:\n{str(e)}")
            self.status_label.config(text="Installation failed.")

    def go_next(self):
        """Avanza a la pantalla final de éxito."""
        self.parent.show_frame(SuccessScreen)

###########################################################################
# Clase SuccessScreen
# Pantalla final que indica que la instalación se completó y ofrece opciones
# para lanzar la aplicación y crear accesos directos.
###########################################################################
class SuccessScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#282828')  # Fondo oscuro
        
        # Título de éxito
        success_label = tk.Label(self, text="Instalacion completada!", font=("Arial", 14, "bold"),
                                  fg="white", bg="#282828")
        success_label.pack(pady=20)
        
        # Mensaje descriptivo
        detail_label = tk.Label(self, text="Tu programa se ha instalado correctamente",
                                 font=("Arial", 10), fg="white", bg="#282828")
        detail_label.pack(pady=10)
        
        # Checkbox para iniciar la aplicación automáticamente (marcado por defecto)
        self.launch_var = tk.BooleanVar(value=True)
        self.launch_checkbox = tk.Checkbutton(self, text="Iniciar la aplicacion ahora", variable=self.launch_var,
                                              font=("Arial", 10), bg="#282828", fg="white", selectcolor="#282828")
        self.launch_checkbox.pack(pady=10)
        
        # Checkbox para crear un acceso directo en el escritorio (marcado por defecto)
        self.shortcut_var = tk.BooleanVar(value=True)
        self.shortcut_checkbox = tk.Checkbutton(self, text="Crear acceso directo", variable=self.shortcut_var,
                                                font=("Arial", 10), bg="#282828", fg="white", selectcolor="#282828")
        self.shortcut_checkbox.pack(pady=5)
        
        # Botón "Finish" para finalizar la instalación
        exit_button = ttk.Button(self, text="Finish", command=self.finish_installation)
        exit_button.pack(pady=20)
        
        self.parent = parent

    def finish_installation(self):
        """
        Finaliza la instalación.
        Si se selecciona, crea un acceso directo y lanza la aplicación (main.py).
        Finalmente, cierra el instalador.
        """
        if self.shortcut_var.get():
            threading.Thread(target=self.create_shortcut, daemon=True).start()
        if self.launch_var.get():
            self.launch_main_py()
        self.parent.destroy()

    def create_shortcut(self):
        """
        Crea un acceso directo en el escritorio según el sistema operativo.
        Soporta Windows, macOS y Linux.
        """
        current_os = platform.system()
        target_path = os.path.join(self.parent.install_path.get(), "main.py")
        shortcut_name = "My Application"  # Nombre del acceso directo
        
        if not os.path.isfile(target_path):
            messagebox.showerror("Error", f"Cannot find 'main.py' in '{self.parent.install_path.get()}'. Cannot create shortcut.")
            return
        
        if current_os == "Windows":
            self.create_windows_shortcut(target_path, shortcut_name)
        elif current_os == "Darwin":
            self.create_macos_shortcut(target_path, shortcut_name)
        elif current_os == "Linux":
            self.create_linux_shortcut(target_path, shortcut_name)
        else:
            messagebox.showerror("Error", f"Unsupported operating system: {current_os}. Cannot create shortcut.")

    def create_windows_shortcut(self, target_path, shortcut_name):
        """
        Crea un acceso directo en Windows utilizando winshell y pywin32.
        """
        if not WINDOWS_SHORTCUT_AVAILABLE:
            messagebox.showerror("Error", "winshell and pywin32 modules are not installed. Unable to create shortcut on Windows.")
            return
        
        try:
            desktop = winshell.desktop()  # Ruta del escritorio en Windows
            shortcut_path = os.path.join(desktop, f"{shortcut_name}.lnk")
            with winshell.shortcut(shortcut_path) as link:
                link.path = sys.executable
                link.arguments = f'\"{target_path}\"'
                link.description = "Launch My Application"
                link.icon_location = (sys.executable, 0)
            messagebox.showinfo("Success", "Desktop shortcut created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create Windows shortcut:\n{str(e)}")

    def create_macos_shortcut(self, target_path, shortcut_name):
        """
        Crea un alias en el escritorio de macOS utilizando AppleScript.
        """
        try:
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            alias_path = os.path.join(desktop, f"{shortcut_name}.app")
            # Definir el AppleScript sin backslashes innecesarios
            applescript = f'''tell application "Finder"
    make alias file to POSIX file "{target_path}" at POSIX file "{desktop}"
    set name of result to "{shortcut_name}.app"
end tell'''
            subprocess.run(['osascript', '-e', applescript], check=True)
            messagebox.showinfo("Success", "Desktop alias created successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to create macOS alias:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")

    def create_linux_shortcut(self, target_path, shortcut_name):
        """
        Crea un acceso directo en Linux creando un archivo .desktop en el escritorio.
        """
        try:
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            shortcut_path = os.path.join(desktop, f"{shortcut_name}.desktop")
            desktop_entry = f"""[Desktop Entry]
Type=Application
Name={shortcut_name}
Exec={sys.executable} "{target_path}"
Icon=utilities-terminal
Terminal=false
"""
            with open(shortcut_path, 'w') as f:
                f.write(desktop_entry)
            os.chmod(shortcut_path, 0o755)
            messagebox.showinfo("Success", "Desktop shortcut created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create Linux shortcut:\n{str(e)}")

    def launch_main_py(self):
        """
        Lanza el archivo main.py usando el mismo intérprete de Python en el directorio de instalación.
        """
        main_py_path = os.path.join(self.parent.install_path.get(), "main.py")
        if not os.path.isfile(main_py_path):
            messagebox.showerror("Error", f"Cannot find 'main.py' in '{self.parent.install_path.get()}'.")
            return
        try:
            subprocess.Popen([sys.executable, main_py_path], cwd=self.parent.install_path.get())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch 'main.py':\n{str(e)}")
            return

# Punto de entrada del programa: se crea la instancia del instalador y se inicia la interfaz gráfica.
if __name__ == "__main__":
    app = Installer()
    app.mainloop()
