# Requiere instalar las librerías necesarias:
# pip install SpeechRecognition pyaudio

import speech_recognition as sr  # Importamos la librería de reconocimiento de voz

# Función para inicializar el reconocedor de voz
def inicializar_reconocedor():
    """
    Crea y devuelve una instancia del reconocedor de voz.
    """
    return sr.Recognizer()

# Función para configurar el micrófono
def configurar_microfono(reconocedor, duracion_ajuste=1):
    """
    Ajusta el micrófono para medir el ruido ambiental y garantizar
    un reconocimiento de voz más preciso.
    
    Parámetros:
        reconocedor: Instancia de sr.Recognizer.
        duracion_ajuste: Duración en segundos para calibrar el ruido ambiental.
    
    Retorna:
        True si el micrófono fue configurado correctamente, False si no se detecta un micrófono.
    """
    try:
        with sr.Microphone() as microfono:  # Abre el micrófono dentro de un contexto seguro
            print("Configurando el micrófono... Por favor, guarda silencio.")
            reconocedor.adjust_for_ambient_noise(microfono, duration=duracion_ajuste)  # Ajusta el ruido de fondo
            print("Micrófono configurado correctamente.")
            return True
    except OSError as e:  # Error si no hay micrófono disponible
        print("Error: No se detectó un micrófono disponible.")
        print(f"Detalles del error: {e}")
        return False

# Función para escuchar un comando del usuario
def escuchar_comando(reconocedor, intentos=3):
    """
    Captura y reconoce el comando de voz del usuario.
    
    Parámetros:
        reconocedor: Instancia de sr.Recognizer.
        intentos: Número máximo de intentos para escuchar y reconocer un comando.
    
    Retorna:
        El comando reconocido como texto (en minúsculas), o None si no se pudo reconocer.
    """
    for intento in range(intentos):
        try:
            with sr.Microphone() as microfono:  # Abre el micrófono en cada intento
                print("Escuchando tu comando... (Intenta hablar claramente)")
                audio = reconocedor.listen(microfono)  # Captura el audio del usuario
            print("Procesando el comando...")
            comando = reconocedor.recognize_google(audio, language="es-ES")  # Reconoce el audio en español
            print(f"Comando reconocido: {comando}")
            return comando.lower()  # Devuelve el comando en minúsculas
        except sr.UnknownValueError:  # Error si no se puede entender el audio
            print(f"Error: No se pudo entender el audio. Intento {intento + 1} de {intentos}.")
        except sr.RequestError as e:  # Error si hay problemas con el servicio de Google
            print(f"Error: Problema con el servicio de reconocimiento. Detalles: {e}")
            return None
    print("No se pudo reconocer el comando después de varios intentos.")
    return None

# Función para ejecutar la operación basada en el comando reconocido
def procesar_comando(comando):
    """
    Realiza una acción basada en el comando de voz reconocido.
    
    Parámetros:
        comando: Texto del comando reconocido.
    """
    if not comando:  # Si no se reconoce un comando válido
        print("No se recibió un comando válido.")
        return

    # Comparación de comandos reconocidos y acciones correspondientes
    if "insertar" in comando:
        print("Operación reconocida: INSERTAR. Vamos a insertar un nuevo registro.")
    elif "listar" in comando:
        print("Operación reconocida: LISTAR. Mostrando la lista de registros.")
    elif "actualizar" in comando:
        print("Operación reconocida: ACTUALIZAR. Vamos a actualizar un registro.")
    elif "eliminar" in comando:
        print("Operación reconocida: ELIMINAR. Vamos a eliminar un registro.")
    else:
        print("El comando no se reconoció como una operación válida.")

# Función principal que coordina todo el proceso
def ejecutar_reconocimiento():
    """
    Configura el reconocedor, ajusta el micrófono y ejecuta
    el ciclo principal para escuchar y procesar comandos.
    """
    reconocedor = inicializar_reconocedor()  # Inicializa el reconocedor de voz
    
    if not configurar_microfono(reconocedor):  # Configura el micrófono
        return  # Finaliza si no hay micrófono disponible

    # Instrucciones iniciales para el usuario
    print("Tus opciones de comando:")
    print("1. Decir 'insertar' para añadir un registro.")
    print("2. Decir 'listar' para mostrar los registros.")
    print("3. Decir 'actualizar' para modificar un registro existente.")
    print("4. Decir 'eliminar' para borrar un registro.")
    print("Habla cuando escuches 'Escuchando tu comando'.")

    # Ciclo principal para escuchar y procesar comandos
    while True:
        comando = escuchar_comando(reconocedor)  # Escucha el comando del usuario
        procesar_comando(comando)  # Procesa el comando reconocido
        print("\n¿Quieres continuar? Si no, presiona Ctrl+C para salir.\n")

# Punto de entrada del programa
if __name__ == "__main__":
    ejecutar_reconocimiento()  # Llama a la función principal para iniciar el programa
