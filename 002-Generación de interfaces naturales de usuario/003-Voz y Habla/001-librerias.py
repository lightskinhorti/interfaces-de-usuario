import speech_recognition as sr

reconocimiento = sr.Recognizer()  # Creamos una instancia del objeto reconocedor

def reconocer():  # creo una función a la que llamar
    with sr.Microphone() as origen:  # Obtengo el audio del micrófono y lo llamo origen
        print("Ajustando ruido de fondo...")  # Mensaje para el usuario
        reconocimiento.adjust_for_ambient_noise(origen, duration=1)  # Mido el ruido de fondo durante 1 segundo
        print("Escuchamos...")
        audio = reconocimiento.listen(origen)  # Escuchar lo que dice el usuario

        try:  # Manejo de errores
            print("Reconociendo...")
            text = reconocimiento.recognize_google(audio)  # Reconocer el audio
            print(f"Reconocido: {text}")  # Mostrar el texto reconocido
        except sr.RequestError as e:  # Manejo de excepciones para errores de solicitud
            print(f"Error de solicitud: {e}")  # Mensaje más descriptivo
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")  # Mensaje más descriptivo

reconocer()  # Ejecuta la función
