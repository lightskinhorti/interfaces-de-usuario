import xml.etree.ElementTree as ET

# Cargar y parsear el archivo XML
arbol = ET.parse('archivo.xml')

# Obtener la raíz del XML
raiz = arbol.getroot()

# Recorrer los elementos de la raíz e imprimir cada etiqueta y su texto
for elemento in raiz:
    print(f"Etiqueta: {elemento.tag}, Texto: {elemento.text}")
