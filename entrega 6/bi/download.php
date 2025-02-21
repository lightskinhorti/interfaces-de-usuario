<?php
// Verificamos si la solicitud es de tipo POST y si se ha enviado el parámetro 'table'
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['table'])) {
    // Decodificamos el contenido base64 recibido para obtener la tabla en formato HTML
    $tableHTML = base64_decode($_POST['table']);

    // Establecemos las cabeceras para forzar la descarga de un archivo
    header('Content-Type: text/html'); // Indicamos que el tipo de contenido es HTML
    header('Content-Disposition: attachment; filename="table.html"'); // Nombre del archivo descargado

    // Construimos la estructura del documento HTML con la tabla recibida
    echo "<!DOCTYPE html>";
    echo "<html>";
    echo "<head><title>Downloaded Table</title></head>"; // Título de la página
    echo "<body>";
    echo $tableHTML; // Insertamos el contenido de la tabla dentro del cuerpo del documento
    echo "</body>";
    echo "</html>";
    
    // Finalizamos la ejecución del script para evitar cualquier salida adicional
    exit;
}
?>
