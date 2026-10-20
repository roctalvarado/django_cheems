const pestanita = document.getElementById("btn-perfil");
pestanita.addEventListener('click', function () {
    const boton = document.getElementById('btn-perfil');
    const panel = document.getElementById('panel-perfil');

    console.log('scripts.js cargado', boton, panel);

    if (!boton || !panel) return;

    
        panel.classList.toggle('oculto');
    
});