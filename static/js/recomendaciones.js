// Código para ocultar y mostrar el formulario a decisión del usuario (recomendaciones)

document.addEventListener("DOMContentLoaded", function () {
    var toggleButton = document.getElementById("botonFormulario");
    var contenidoOculto = document.getElementById("formularioPersonalizacion");

    toggleButton.addEventListener("click", function () {
        if (contenidoOculto.style.display === "none") {
            contenidoOculto.style.display = "block";
        } else {
            contenidoOculto.style.display = "none";
        }
    });
});