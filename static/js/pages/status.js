var map = L.map('map').setView([-5.66417, -37.79889], 17);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 17,
    attribution: '© OpenStreetMap'
}).addTo(map);

const camadaVias = L.layerGroup().addTo(map);
const camadaOcorrencias = L.layerGroup().addTo(map);

let dadosGlobais = null;
let pinUsuario = null;

function criarIconeStatus(item) {
    let classe = "pin-ativa";
    let simbolo = "!";

    if (item.tipo && item.tipo.toUpperCase() === "ACIDENTE") {
        classe = "pin-emergencia";
        simbolo = "!";
    } else if (item.status === "EM_ANDAMENTO") {
        classe = "pin-andamento";
        simbolo = "⏳";
    } else if (item.status === "RESOLVIDA" || item.status === "ENCERRADA") {
        classe = "pin-finalizada";
        simbolo = "✓";
    } else if (item.status === "ABERTA") {
        classe = "pin-ativa";
        simbolo = "!";
    }

    return L.divIcon({
        className: "",
        html: `<div class="pin-status ${classe}"><span>${simbolo}</span></div>`,
        iconSize: [42, 42],
        iconAnchor: [21, 42],
        popupAnchor: [0, -42]
    });
}

const iconePin = L.divIcon({
    html: `<div style="
        width: 20px; height: 20px;
        background: #e63946;
        border: 3px solid #fff;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    "></div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 20],
    className: ''
});

const ehPaginaRegistro = document.querySelector('form.ipt');

if (ehPaginaRegistro) {
    map.on('click', function (e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;

        if (pinUsuario) map.removeLayer(pinUsuario);

        pinUsuario = L.marker([lat, lng], { icon: iconePin })
            .addTo(map)
            .bindPopup(`
                <strong>Local selecionado</strong><br>
                Lat: ${lat.toFixed(6)}<br>
                Lng: ${lng.toFixed(6)}
            `)
            .openPopup();

        document.getElementById('id_latitude').value = lat;
        document.getElementById('id_longitude').value = lng;
    });
}

function atualizarDashboard() {
    fetch('/api/vias/mapa/')
        .then(response => {
            if (!response.ok) throw new Error("Erro na rede");
            return response.json();
        })
        .then(data => {
            dadosGlobais = data;

            camadaVias.clearLayers();
            if (data.vias && data.vias.length > 0) {
                L.geoJSON(data.vias, {
                    style: { color: "#3388ff", weight: 3, opacity: 0.6 }
                }).addTo(camadaVias);
            }

            camadaOcorrencias.clearLayers();

            if (data.ocorrencias) {
                data.ocorrencias.forEach(item => {
                    if (!['ABERTA','EM_ANDAMENTO','RESOLVIDA','ENCERRADA'].includes(item.status)) return;
                    if (item.latitude == null || item.longitude == null) return;

                    const marker = L.marker([item.latitude, item.longitude], { icon: criarIconeStatus(item) });
                    const endereco = item.via_detalhe ? item.via_detalhe.nome : 'Não informado';

                    marker.bindPopup(`
                        <div class="custom-popup">
                            <strong style="color: #e63946;">Ocorrência #${item.id}</strong><br>
                            <b>Endereço:</b> ${endereco}<br>
                            <b>Descrição:</b> ${item.descricao}<br>
                            <hr style="margin: 5px 0">
                            <span style="font-size: 10px; color: #666;">Sincronizado às: ${new Date().toLocaleTimeString()}</span>
                        </div>
                    `);
                    camadaOcorrencias.addLayer(marker);
                });
            }

            renderizarOcorrencias();
        })
        .catch(err => console.error("Falha ao atualizar mapa:", err));
}

if (!ehPaginaRegistro) {
    atualizarDashboard();
    setInterval(atualizarDashboard, 15000);
}

function renderizarOcorrencias() {
    if (!dadosGlobais || !dadosGlobais.ocorrencias) return;

    const lista = document.getElementById("lista-status");
    if (!lista) return;

    lista.innerHTML = "";

    if (dadosGlobais.ocorrencias.length === 0) {
        lista.innerHTML = "<p class='sem-ocorrencias'>Sem ocorrências no momento</p>";
        return;
    }

    const abertas = dadosGlobais.ocorrencias.filter(i =>
        i.status === "ABERTA" || i.status === "EM_ANDAMENTO"
    );
    const fechadas = dadosGlobais.ocorrencias.filter(i =>
        i.status === "RESOLVIDA" || i.status === "ENCERRADA"
    );

    const temPermissao = (typeof tipoUsuario !== 'undefined') &&
        (tipoUsuario === "AGENTE" || tipoUsuario === "ADMIN");

    const colunaAcaoHeader = temPermissao ? "<th>Ação</th>" : "";

    const cabecalho = `
        <thead>
            <tr>
                <th>Tipo</th>
                <th>Endereço</th>
                <th>Descrição</th>
                <th>Horário</th>
                <th>Status</th>
                ${colunaAcaoHeader}
            </tr>
        </thead>
    `;

    function gerarLinhas(items) {
        return items.map(item => {
            const horario = item.horario_incidente
                ? item.horario_incidente.slice(0, 5)
                : "Sem horário";
            const endereco = item.via_detalhe ? item.via_detalhe.nome : "Não informado";
            const badgeClass = item.status === "EM_ANDAMENTO" ? "em_andamento"
                : item.status === "ABERTA" ? "aberta" : "fechada";
            const colunaAcao = temPermissao
                ? `<td><button class="btn-status" onclick="abrirModalStatus(${item.id}, '${item.status}')">Alterar</button></td>`
                : "";

            return `
                <tr>
                    <td>${item.tipo}</td>
                    <td>${endereco}</td>
                    <td>${item.descricao || "Sem descrição"}</td>
                    <td>${horario}</td>
                    <td><span class="badge ${badgeClass}">${item.status.replace("_", " ")}</span></td>
                    ${colunaAcao}
                </tr>
            `;
        }).join("");
    }

    lista.innerHTML = `
        <div class="titulo-status abertas">Ocorrências ativas</div>
        ${abertas.length === 0
            ? "<p class='sem-ocorrencias'>Nenhuma ocorrência ativa</p>"
            : `<table class="tabela-ocorrencias">${cabecalho}<tbody>${gerarLinhas(abertas)}</tbody></table>`
        }
        <div class="titulo-status fechadas">Ocorrências finalizadas</div>
        ${fechadas.length === 0
            ? "<p class='sem-ocorrencias'>Nenhuma ocorrência finalizada</p>"
            : `<table class="tabela-ocorrencias">${cabecalho}<tbody>${gerarLinhas(fechadas)}</tbody></table>`
        }
    `;
}

window.addEventListener("load", () => {
    setTimeout(() => map.invalidateSize(), 500);
});

window.addEventListener("resize", () => {
    map.invalidateSize();
});

function abrirModalStatus(id, statusAtual) {
    document.getElementById('modal-oc-id').value = id;
    document.getElementById('modal-status-select').value = statusAtual;
    document.getElementById('modalStatusOverlay').classList.add('aberto');
}

function fecharModalStatus() {
    document.getElementById('modalStatusOverlay').classList.remove('aberto');
}

const formStatus = document.getElementById('form-status');
if (formStatus) {
    formStatus.addEventListener('submit', async function(e) {
        e.preventDefault();
        const id = document.getElementById('modal-oc-id').value;
        const novoStatus = document.getElementById('modal-status-select').value;
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const response = await fetch(`/ocorrencias/${id}/atualizar-status/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `status=${novoStatus}`
        });

        if (response.ok || response.redirected) {
            fecharModalStatus();
            atualizarDashboard();
        }
    });
}

if (formStatus) {
    formStatus.addEventListener('submit', async function(e) {
        e.preventDefault();
        const id = document.getElementById('modal-oc-id').value;
        const novoStatus = document.getElementById('modal-status-select').value;
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const response = await fetch(`/ocorrencias/${id}/atualizar-status/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `status=${novoStatus}`
        });

        fecharModalStatus();

        // atualiza o dado localmente sem esperar o fetch completo
        if (dadosGlobais) {
            const oc = dadosGlobais.ocorrencias.find(o => o.id == id);
            if (oc) oc.status = novoStatus;
            renderizarOcorrencias();
        }

        // depois sincroniza com o servidor em background
        atualizarDashboard();
    });
}