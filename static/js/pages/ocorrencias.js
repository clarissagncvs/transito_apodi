//pega CSRF necessário no Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//função principal
async function enviarOcorrencia(event) {
    event.preventDefault(); //impede reload da página

    //tenta pegar os campos automaticamente sem depender de id
    const select = document.querySelector("select");
    const textarea = document.querySelector("textarea");

    const dados = {
        tipo: select ? select.value : "",
        descricao: textarea ? textarea.value : "",
        status: "pendente"
    };

    try {
        const resposta = await fetch("/api/ocorrencias/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(dados)
        });

        if (resposta.ok) {
            alert("Ocorrência enviada");
        } else {
            const erro = await resposta.json();
            console.error(erro);
            alert("Erro ao enviar");
        }

    } catch (erro) {
        console.error(erro);
        alert("Erro de conexão");
    }
}

//conecta automaticamente ao formulário ou botão
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const botao = document.querySelector("button");

    if (form) {
        form.addEventListener("submit", enviarOcorrencia);
    } else if (botao) {
        botao.addEventListener("click", enviarOcorrencia);
    }
});