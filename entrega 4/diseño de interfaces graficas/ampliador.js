// Definimos variables iniciales
let tamanio = 1;  // Tamaño inicial de la fuente
let cantidadcontraste = 1;  // Valor inicial del contraste
let contenedor = document.createElement("div");  // Creamos un contenedor para los botones
contenedor.classList.add("jvampliador");  // Le agregamos una clase CSS para el estilo

////////////////// AUMENTAR /////////////////

// Creamos el botón de aumentar el tamaño de fuente
let aumentar = document.createElement("button");
aumentar.textContent = "+";  // El texto del botón será "+"
contenedor.appendChild(aumentar);  // Agregamos el botón al contenedor

// Asignamos una acción al botón de aumentar
aumentar.onclick = function() {
    tamanio *= 1.1;  // Aumentamos el tamaño de la fuente en un 10% cada vez
    document.querySelector("body").style.fontSize = tamanio + "em";  // Aplicamos el nuevo tamaño al cuerpo de la página
}

////////////////// CONTRASTE /////////////////

// Creamos el botón de cambiar el contraste
let contraste = document.createElement("button");
contraste.textContent = "C";  // El texto del botón será "C"
contenedor.appendChild(contraste);  // Agregamos el botón al contenedor

// Asignamos una acción al botón de cambiar contraste
contraste.onclick = function() {
    cantidadcontraste = 80;  // Establecemos un valor de contraste a un 80%
    document.querySelector("body").style.filter = "contrast(" + cantidadcontraste + "%)";  // Aplicamos el filtro de contraste
}

////////////////// INVERTIR /////////////////

// Creamos el botón de invertir los colores
let invertir = document.createElement("button");
invertir.textContent = "I";  // El texto del botón será "I"
contenedor.appendChild(invertir);  // Agregamos el botón al contenedor

// Asignamos una acción al botón de invertir
invertir.onclick = function() {
    document.querySelector("body").style.filter = "invert(1)";  // Aplicamos un filtro para invertir los colores
}

////////////////// DISMINUIR /////////////////

// Creamos el botón de disminuir el tamaño de fuente
let disminuir = document.createElement("button");
disminuir.textContent = "-";  // El texto del botón será "-"
contenedor.appendChild(disminuir);  // Agregamos el botón al contenedor

// Asignamos una acción al botón de disminuir
disminuir.onclick = function() {
    tamanio *= 0.9;  // Disminuimos el tamaño de la fuente en un 10% cada vez
    document.querySelector("body").style.fontSize = tamanio + "em";  // Aplicamos el nuevo tamaño al cuerpo de la página
}

// Finalmente, agregamos el contenedor con todos los botones al cuerpo de la página
document.querySelector("body").appendChild(contenedor);
