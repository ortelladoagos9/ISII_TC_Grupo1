function buscar() {
    alert('Función de búsqueda próximamente disponible...');
}

function registrarUsuario(){
    alert('Función de registrarse próximamente disponible...');
}

function login(){
    alert('Función de iniciar sesion próximamente disponible...');
}

const destinos = [
    "Buenos Aires",
    "Mar del Plata",
    "Río de Janeiro",
    "Bariloche",
    "Córdoba",
    "Mendoza",
    "Iguazú",
    "Salta",
    "Ushuaia"
];

const destinoInput = document.getElementById('destino');
const sugerenciasContainer = document.getElementById('sugerencias');

destinoInput.addEventListener('input', function() {
    const input = destinoInput.value.toLowerCase();
    sugerenciasContainer.innerHTML = '';

    if (input.length === 0) {
        return;
    }

    const sugerenciasFiltradas = destinos.filter(destino => 
        destino.toLowerCase().includes(input)
    );

    sugerenciasFiltradas.forEach(destino => {
        const item = document.createElement('div');
        item.textContent = destino;
        item.classList.add('sugerencia-item');
        item.addEventListener('click', function() {
            destinoInput.value = destino;
            sugerenciasContainer.innerHTML = '';
        });
        sugerenciasContainer.appendChild(item);
    });
});

document.addEventListener('click', function(e) {
    if (!e.target.closest('.autocomplete-container')) {
        sugerenciasContainer.innerHTML = '';
    }
});
