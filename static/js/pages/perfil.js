/**
 * Função para abrir/fechar o modal
 * @param {boolean} show - true para abrir, false para fechar
 */
function toggleModal(show) {
    const modal = document.getElementById('changeAccountModal');
    if (modal) {
        modal.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Função principal para disparar o e-mail via POST
 * @param {string} tipo - 'AGENTE' ou 'ADMIN'
 * @param {string} urlSolicitacao - A URL gerada pelo Django no HTML
 */
function dispararSolicitacao(tipo, urlSolicitacao) {
    // 1. Localiza o Token CSRF no HTML (obrigatório para POST no Django)
    const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
    
    if (!csrfElement) {
        alert("Erro de segurança: Token CSRF não encontrado na página.");
        return;
    }

    const csrftoken = csrfElement.value;

    // 2. Faz a chamada para o servidor
    fetch(urlSolicitacao, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        // Envia o tipo escolhido para a View
        body: new URLSearchParams({
            'tipo': tipo
        })
    })
    .then(response => {
        if (response.ok) {
            alert(`✅ Solicitação para ${tipo} enviada com sucesso ao Trânsito Apodi!`);
            toggleModal(false);
        } else {
            // Se o Django retornar erro (ex: 400 ou 500)
            alert("❌ Erro ao processar solicitação. Verifique se você está logado.");
        }
    })
    .catch(error => {
        console.error("Erro na requisição:", error);
        alert("❌ Erve de conexão. O servidor está offline?");
    });
}

// Fecha o modal se o usuário clicar fora da caixa branca
window.onclick = function(event) {
    const modal = document.getElementById('changeAccountModal');
    if (event.target === modal) {
        toggleModal(false);
    }
};