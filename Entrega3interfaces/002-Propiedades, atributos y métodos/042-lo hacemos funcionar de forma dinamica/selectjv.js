// Texto a desplegar en las opciones
let texto = "Javier";

// Referencia al contenedor principal
let contenedor = document.querySelector("#contenedor");

// Creación del elemento <select>
let selector = document.createElement("select");
contenedor.appendChild(selector);

// Añadir opciones al selector basadas en la cadena de texto
for (let i = 0; i < texto.length; i++) {
  let opcion = document.createElement("option");
  opcion.textContent = texto[i]; // Texto de cada opción
  opcion.value = i; // Valor asociado a la opción
  selector.appendChild(opcion); // Agregar la opción al selector
}

// Transformar el selector usando la función personalizada
selectjv(selector);

// Función que convierte un <select> en un componente personalizado
function selectjv(selector) {
  let contenedores = []; // Array para almacenar los contenedores personalizados

  // Crear el contenedor principal para el nuevo select
  let nuevoContenedor = document.createElement("div");
  nuevoContenedor.classList.add("selectjv");
  contenedores.push(nuevoContenedor);

  // Reemplazar el <select> original con el contenedor personalizado
  selector.replaceWith(nuevoContenedor);

  // Crear la caja principal que muestra la opción seleccionada
  let caja = document.createElement("div");
  caja.classList.add("caja");
  caja.textContent = selector.querySelector("option:first-child").textContent; // Mostrar la primera opción por defecto
  nuevoContenedor.appendChild(caja);

  // Añadir el selector original al nuevo contenedor (oculto)
  nuevoContenedor.appendChild(selector);

  // Evento para desplegar las opciones al hacer clic en la caja
  caja.onclick = function (e) {
    e.stopPropagation(); // Evitar la propagación del evento al documento

    // Alternar el estado de desplegado
    caja.classList.toggle("radio2");

    // Crear el contenedor de resultados si no existe
    let resultados = document.createElement("div");
    resultados.classList.add("resultados");
    nuevoContenedor.appendChild(resultados);

    // Crear el buscador dentro de los resultados
    let buscador = document.createElement("input");
    buscador.setAttribute("type", "search");
    buscador.setAttribute("placeholder", "Busca...");
    resultados.appendChild(buscador);

    // Contenedor para los resultados filtrados
    let contenedorResultados = document.createElement("div");
    resultados.appendChild(contenedorResultados);

    // Evento: Filtro dinámico mientras se escribe
    buscador.onkeyup = function () {
      let busca = buscador.value.toLowerCase();
      contenedorResultados.innerHTML = ""; // Limpiar resultados previos

      let opciones = selector.querySelectorAll("option");
      opciones.forEach((opcion) => {
        if (opcion.textContent.toLowerCase().includes(busca)) {
          let item = document.createElement("p");
          item.textContent = opcion.textContent;

          // Evento: Actualizar la selección al hacer clic
          item.onclick = function () {
            caja.textContent = item.textContent;
            resultados.remove(); // Cerrar el menú
            actualizarSeleccion(selector, item.textContent);
          };

          contenedorResultados.appendChild(item);
        }
      });
    };

    // Inicializar el contenedor con todas las opciones
    let opciones = selector.querySelectorAll("option");
    opciones.forEach((opcion) => {
      let item = document.createElement("p");
      item.textContent = opcion.textContent;

      // Evento: Actualizar la selección al hacer clic
      item.onclick = function () {
        caja.textContent = item.textContent;
        resultados.remove(); // Cerrar el menú
        actualizarSeleccion(selector, item.textContent);
      };

      contenedorResultados.appendChild(item);
    });

    // Evitar cerrar el menú al interactuar con resultados
    resultados.onclick = (e) => e.stopPropagation();
  };

  // Evento global para cerrar el menú si se hace clic fuera
  document.onclick = function () {
    contenedores.forEach((contenedor) => {
      let resultados = contenedor.querySelector(".resultados");
      if (resultados) {
        resultados.remove();
      }
      let caja = contenedor.querySelector(".caja");
      caja.classList.remove("radio2");
    });
  };
}

// Función para actualizar la selección del <select>
function actualizarSeleccion(selector, textoSeleccionado) {
  let opciones = selector.querySelectorAll("option");
  opciones.forEach((opcion) => {
    if (opcion.textContent === textoSeleccionado) {
      opcion.setAttribute("selected", true);
    } else {
      opcion.removeAttribute("selected");
    }
  });
}
