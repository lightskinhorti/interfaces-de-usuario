// Seleccionamos todas las tablas que tienen la clase 'jvtabla'
let tablas = document.querySelectorAll(".jvtabla");

// Iteramos sobre cada tabla para aplicar la funcionalidad
// de ordenamiento dinámico

tablas.forEach(function(tabla) {
    let contenido = []; // Almacena el contenido de la tabla en un array de objetos
    let indices = []; // Almacena los nombres de las columnas para referencia
    let cabeceras = tabla.querySelectorAll("thead tr th"); // Seleccionamos las cabeceras

    // Recorremos las cabeceras para asignar eventos de ordenamiento
    cabeceras.forEach(function(cabecera, colIndex) {
        indices.push(cabecera.textContent.trim()); // Guardamos los nombres de las columnas
        
        // Agregamos un evento para ordenar cuando se haga clic en una cabecera
        cabecera.onclick = function() {
            console.log("Ordenando por columna: " + cabecera.textContent);
            tabla.querySelector("tbody").innerHTML = ""; // Vaciamos el cuerpo antes de actualizar
            
            // Ordenamos el array de contenido basándonos en la columna seleccionada
            contenido.sort(function(a, b) {
                let valA = a[indices[colIndex]].toLowerCase();
                let valB = b[indices[colIndex]].toLowerCase();
                
                // Si los valores son números, los convertimos antes de comparar
                if (!isNaN(valA) && !isNaN(valB)) {
                    valA = parseFloat(valA);
                    valB = parseFloat(valB);
                }
                
                return valA > valB ? 1 : valA < valB ? -1 : 0;
            });
            
            // Llamamos a la función para actualizar la tabla con el contenido ordenado
            poblarTabla(colIndex);
        };
    });

    // Recorremos las filas del cuerpo de la tabla para extraer su contenido
    let registros = tabla.querySelectorAll("tbody tr");
    registros.forEach(function(registro) {
        let linea = {}; // Objeto para almacenar los datos de una fila
        let celdas = registro.querySelectorAll("td");
        
        // Asociamos cada celda con su cabecera correspondiente
        celdas.forEach(function(celda, index) {
            linea[indices[index]] = celda.textContent.trim();
        });
        
        contenido.push(linea); // Añadimos la fila procesada al array principal
    });
    
    console.log(contenido); // Mostramos en consola el contenido extraído
    poblarTabla(); // Poblar la tabla por primera vez

    // Función para actualizar la tabla con los datos ordenados
    function poblarTabla(colIndex = -1) {
        let theadRow = tabla.querySelector("thead tr");
        theadRow.innerHTML = ""; // Limpiamos las cabeceras antes de redibujarlas
        
        let cabezal1 = document.createElement("th");
        cabezal1.textContent = "#";
        theadRow.appendChild(cabezal1);
        
        indices.forEach(function(campo, index) {
            let cabezal = document.createElement("th");
            cabezal.textContent = campo;
            
            // Aplicamos estilos para indicar la columna ordenada
            if (index === colIndex) {
                cabezal.style.backgroundColor = "lightblue"; // Nueva función: destaca la columna ordenada
            }
            
            cabezal.onclick = function() {
                console.log("Ordenando por columna: " + cabezal.textContent);
                tabla.querySelector("tbody").innerHTML = "";
                
                contenido.sort(function(a, b) {
                    let valA = a[indices[index]].toLowerCase();
                    let valB = b[indices[index]].toLowerCase();
                    
                    if (!isNaN(valA) && !isNaN(valB)) {
                        valA = parseFloat(valA);
                        valB = parseFloat(valB);
                    }
                    
                    return valA > valB ? 1 : valA < valB ? -1 : 0;
                });
                
                poblarTabla(index);
            };
            
            theadRow.appendChild(cabezal);
        });
        
        // Limpiamos el cuerpo de la tabla antes de insertar las filas ordenadas
        let tbody = tabla.querySelector("tbody");
        tbody.innerHTML = "";
        
        let contador = 1;
        contenido.forEach(function(linea) {
            let fila = document.createElement("tr");
            
            let celda1 = document.createElement("td");
            celda1.textContent = contador;
            fila.appendChild(celda1);
            contador++;
            
            indices.forEach(function(campo) {
                let celda = document.createElement("td");
                celda.textContent = linea[campo];
                fila.appendChild(celda);
            });
            
            tbody.appendChild(fila);
        });
    }
});
