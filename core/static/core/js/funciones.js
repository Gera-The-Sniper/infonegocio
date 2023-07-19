function confirmar(valor) {
    Swal.fire({
        "title":"¿Seguro desea eliminarlo?",
        "icon":"warning",
        "showCancelButton":true,
        "cancelButtonText":"No, cancelar",
        "confirmButtonText":"Sí, eliminar",
        "reverseButtons":true
    })
    .then(function(result) {
        if (result.isConfirmed) {
            window.location.href="eliminar/"+valor

        }
    })
}

function filtro()
{
var tecla = event.key;
if (['.','e','-'].includes(tecla))
   event.preventDefault()
}