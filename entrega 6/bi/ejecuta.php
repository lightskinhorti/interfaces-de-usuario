<style>
    /* Estilos generales */
    body {
        font-family: Arial, sans-serif;
        margin: 20px;
        background-color: #f9f9f9;
    }

    /* Estilos para la tabla */
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        background-color: #ffffff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    th, td {
        padding: 12px;
        text-align: left;
        border: 1px solid #ddd;
    }

    th {
        background-color: crimson;
        color: white;
    }

    tr:nth-child(even) {
        background-color: #f2f2f2;
    }

    tr:hover {
        background-color: #eaf4ff;
    }

    .row-number {
        font-weight: bold;
        text-align: center;
    }
</style>

<?php
// Parámetros de conexión a la base de datos
$host = "localhost";
$username = "crimson";
$password = "crimson";
$database = "crimson";

// Crear la conexión a la base de datos
$conn = new mysqli($host, $username, $password, $database);

// Verificar si la conexión fue exitosa
if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

// Verificar si el parámetro 'sql' está presente en la URL
if (!isset($_GET['sql'])) {
    die("Error: No se proporcionó ninguna consulta SQL.");
}

// Capturar y limpiar la consulta SQL para prevenir inyecciones
$sql = trim($_GET['sql']);
if (empty($sql)) {
    die("Error: La consulta SQL está vacía.");
}

// Preparar la consulta para evitar inyección SQL
$stmt = $conn->prepare($sql);
if (!$stmt) {
    die("Error en la consulta: " . $conn->error);
}

// Ejecutar la consulta preparada
if (!$stmt->execute()) {
    die("Error al ejecutar la consulta: " . $stmt->error);
}

// Obtener los resultados
$result = $stmt->get_result();

/**
 * Función para generar el HTML de la tabla con los resultados
 */
function generateTableHTML($result) {
    if ($result && $result->num_rows > 0) {
        $html = "<table>";

        // Obtener y mostrar los nombres de las columnas
        $html .= "<tr><th>#</th>";
        $columns = $result->fetch_fields();
        foreach ($columns as $column) {
            $html .= "<th>" . htmlspecialchars($column->name) . "</th>";
        }
        $html .= "</tr>";

        // Generar las filas de la tabla con los datos obtenidos
        $rowNumber = 1;
        while ($row = $result->fetch_assoc()) {
            $html .= "<tr>";
            $html .= "<td class='row-number'>" . $rowNumber++ . "</td>";
            foreach ($row as $value) {
                $html .= "<td>" . htmlspecialchars($value) . "</td>";
            }
            $html .= "</tr>";
        }

        $html .= "</table>";
        return $html;
    } else {
        return "<p>No se encontraron resultados.</p>";
    }
}

// Generar el HTML de la tabla
$tableHTML = generateTableHTML($result);

// Mostrar la tabla en la página
echo $tableHTML;

// Si hay resultados, mostrar el botón de descarga
if ($result && $result->num_rows > 0) {
    $encodedTableHTML = base64_encode($tableHTML);
    echo "<form method='post' action='download.php'>";
    echo "<input type='hidden' name='table' value='" . $encodedTableHTML . "'>";
    echo "<button type='submit'>Descargar como HTML</button>";
    echo "</form>";
}

// Cerrar la conexión y la consulta
$stmt->close();
$conn->close();
?>
