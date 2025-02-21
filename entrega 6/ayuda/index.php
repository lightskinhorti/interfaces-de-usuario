<style>
	/* Estilos básicos para mejorar la presentación */
	a {
		display: block;
	}
	body {
		font-family: sans-serif;
	}
	pre {
		color: white;
		background: black;
		padding: 20px;
		border-radius: 10px;
	}
</style>

<?php
/**
 * Función para crear un índice de directorios en formato de enlaces HTML.
 * Muestra una lista de carpetas dentro del directorio especificado, permitiendo
 * navegar fácilmente por la estructura del proyecto.
 *
 * @param string $folderPath Ruta del directorio a analizar.
 */
function creaIndice($folderPath) {
    if (!is_dir($folderPath)) {
        return; // Si la ruta no es un directorio válido, salimos de la función
    }

    /**
     * Función recursiva que escanea un directorio y lista sus subdirectorios.
     * Los directorios encontrados se muestran como enlaces navegables en HTML.
     *
     * @param string $path Ruta actual que se está escaneando.
     */
    function scanDirRecursively2($path) {
        $items = scandir($path); // Obtiene todos los archivos y carpetas en la ruta actual
        foreach ($items as $item) {
            // Ignorar las referencias a los directorios padre y actual (.. y .)
            if ($item === '.' || $item === '..') {
                continue;
            }

            $fullPath = $path . DIRECTORY_SEPARATOR . $item; // Construye la ruta completa
            if (is_dir($fullPath)) {
                // Muestra el directorio como un enlace navegable en la página
                echo "<a href='#" . htmlspecialchars($fullPath) . "'>" . htmlspecialchars($item) . "</a>";
                scanDirRecursively2($fullPath); // Llamada recursiva para analizar subdirectorios
            } 
        }
    }

    scanDirRecursively2($folderPath); // Inicia el escaneo desde la carpeta raíz especificada
}

/**
 * Función para analizar una carpeta y mostrar su contenido en la página.
 * Muestra los nombres de los archivos y el contenido de aquellos con extensiones específicas.
 *
 * @param string $folderPath Ruta del directorio a analizar.
 */
function parseFolderAndFiles($folderPath) {
    if (!is_dir($folderPath)) {
        return; // Si la ruta no es válida, terminamos la ejecución
    }

    /**
     * Función recursiva que escanea el contenido de un directorio.
     * Muestra los directorios como encabezados y los archivos con su contenido.
     *
     * @param string $path Ruta actual que se está escaneando.
     */
    function scanDirRecursively($path) {
        $items = scandir($path); // Obtiene los elementos dentro del directorio actual
        foreach ($items as $item) {
            // Omitir los directorios especiales "." y ".."
            if ($item === '.' || $item === '..') {
                continue;
            }

            $fullPath = $path . DIRECTORY_SEPARATOR . $item; // Construir la ruta completa
            if (is_dir($fullPath)) {
                // Mostrar el nombre del directorio como un encabezado HTML
                echo "<h3 id='" . htmlspecialchars($fullPath) . "'>" . htmlspecialchars($item) . "</h3>";
                scanDirRecursively($fullPath); // Llamada recursiva para analizar subdirectorios
            } elseif (is_file($fullPath)) {
                // Definir las extensiones de archivo a mostrar en formato especial
                $extensionesPermitidas = ['py', 'php'];
                $partesArchivo = explode(".", $item);
                $extension = strtolower(end($partesArchivo)); // Obtener la extensión en minúsculas

                // Mostrar el nombre del archivo
                echo "<strong>" . htmlspecialchars($item) . "</strong><br>";
                $contenido = file_get_contents($fullPath); // Obtener el contenido del archivo

                // Si el archivo es Python, mostrarlo con formato especial en <pre>
                if (in_array($extension, $extensionesPermitidas)) {
                    echo "<pre>" . nl2br(htmlspecialchars($contenido)) . "</pre>"; 
                } else {
                    // Para otros archivos, simplemente mostrar el contenido en un párrafo
                    echo "<p>" . nl2br(htmlspecialchars($contenido)) . "</p>"; 
                }
            }
        }
    }

    scanDirRecursively($folderPath); // Comenzar el escaneo desde la carpeta raíz especificada
}

// Definir la ruta de la carpeta a analizar
$folderPath = 'materiales';

// Generar el índice de directorios y mostrar el contenido de los archivos
creaIndice($folderPath);
parseFolderAndFiles($folderPath);
?>
