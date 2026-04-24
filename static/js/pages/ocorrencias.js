function selecionar(valor) {
    const input = document.getElementById('ocorrencia');
    input.value = valor;
    document.querySelector('.lista-ocorrencias').style.display = 'none';
}

document.getElementById('ocorrencia').addEventListener('focus', () => {
    document.querySelector('.lista-ocorrencias').style.display = 'block';
});
