/**
 * TRÂNSITO APODI - Script de Gerenciamento de Usuários
 * Lógica para o Modal de Troca de Nível de Acesso
 */

// Configuração dos tipos para o modal
const TIPOS_USUARIO = {
    CIDADAO: {
        label: 'Cidadão',
        desc: 'Acesso básico — apenas registra ocorrências',
        icone: 'bi-person',
        classe: 'opcao-cidadao'
    },
    AGENTE: {
        label: 'Agente de Trânsito',
        desc: 'Gerencia ocorrências e semáforos',
        icone: 'bi-shield-check',
        classe: 'opcao-agente'
    },
    ADMIN: {
        label: 'Administrador',
        desc: 'Acesso total ao sistema',
        icone: 'bi-star',
        classe: 'opcao-admin'
    }
};

/**
 * Abre o modal e preenche as opções dinamicamente
 * @param {string} pk - ID do usuário
 * @param {string} username - Nome de exibição
 * @param {string} tipoAtual - Tipo atual (ADMIN, AGENTE, CIDADAO)
 */
function abrirModalTipo(pk, username, tipoAtual) {
    // 1. Define o nome do usuário no subtítulo do modal
    const elUsername = document.getElementById('modal-username');
    if (elUsername) elUsername.textContent = username;

    // 2. Limpa e reconstrói as opções no container
    const container = document.getElementById('modal-opcoes');
    if (!container) return;
    
    container.innerHTML = '';

    Object.entries(TIPOS_USUARIO).forEach(([valor, cfg]) => {
        const ehAtual = valor === tipoAtual;
        const div = document.createElement('div');
        
        // Aplica as classes de estilo definidas no seu CSS
        div.className = `opcao-tipo ${cfg.classe} ${ehAtual ? 'selecionada' : ''}`;
        
        div.innerHTML = `
            <div class="opcao-icone"><i class="bi ${cfg.icone}"></i></div>
            <div class="opcao-texto">
                <span class="opcao-nome">${cfg.label}</span>
                <span class="opcao-desc">${cfg.desc}</span>
            </div>
            <i class="bi bi-check2-circle opcao-check"></i>
        `;

        // Se não for o tipo atual, adiciona o evento de clique para salvar
        if (!ehAtual) {
            div.onclick = () => confirmarTrocaTipo(pk, valor);
        } else {
            div.style.cursor = 'default';
            div.title = 'Este já é o nível atual';
        }

        container.appendChild(div);
    });

    // 3. Exibe o modal adicionando a classe 'aberto'
    document.getElementById('modalOverlay').classList.add('aberto');
}

/**
 * Envia a alteração para o servidor via Fetch
 * @param {string} pk - ID do usuário
 * @param {string} novoTipo - O novo valor (ex: 'AGENTE')
 */
async function confirmarTrocaTipo(pk, novoTipo) {
    // 1. Capture o elemento que disparou o evento IMEDIATAMENTE
    // Usamos um seletor ou passamos o 'this' para evitar o erro de 'event is undefined'
    const elementoClicado = event.currentTarget;

    // Feedback visual de seleção
    const todasOpcoes = document.querySelectorAll('.opcao-tipo');
    todasOpcoes.forEach(el => el.classList.remove('selecionada'));
    elementoClicado.classList.add('selecionada');

    // 2. Captura o token CSRF (essencial para o Django aceitar o POST)
    const formTipo = document.getElementById('formTipo');
    const csrfInput = formTipo ? formTipo.querySelector('[name=csrfmiddlewaretoken]') : null;
    
    if (!csrfInput) {
        console.error("Token CSRF não encontrado no formulário #formTipo");
        return;
    }
    const csrfToken = csrfInput.value;

    // 3. Execução da chamada
    setTimeout(async () => {
        try {
            // Verifique se o prefixo da URL (ex: /usuarios/) está correto conforme seu app
            const response = await fetch(`/usuarios/atualizar-tipo/${pk}/${novoTipo}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            });

            if (response.ok) {
                // Sucesso: Recarrega a página para atualizar os badges da tabela
                window.location.reload();
            } else {
                const errorData = await response.status;
                console.error("Erro do servidor:", errorData);
                alert("Erro ao atualizar: O servidor não permitiu a alteração.");
                fecharModal();
            }
        } catch (error) {
            console.error("Erro na requisição:", error);
            alert("Erro de conexão ao tentar atualizar o usuário.");
        }
    }, 300);
}

/**
 * Fecha o modal limpando as classes
 */
function fecharModal() {
    const modal = document.getElementById('modalOverlay');
    if (modal) modal.classList.remove('aberto');
}

// Evento para fechar com a tecla ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') fecharModal();
});