const btnDark  = document.querySelector('.btn-dm');
const btnLight = document.querySelector('.btn-lm');

function aplicarTema(tema) {
    document.documentElement.setAttribute('data-theme', tema);
    localStorage.setItem('tema', tema);

    btnDark.classList.toggle('ativo', tema === 'dark');
    btnLight.classList.toggle('ativo', tema === 'light');
}

//carrega a preferência salva ao abrir a página
const temaSalvo = localStorage.getItem('tema') || 'light';
aplicarTema(temaSalvo);

btnDark.addEventListener('click',  () => aplicarTema('dark'));
btnLight.addEventListener('click', () => aplicarTema('light'));