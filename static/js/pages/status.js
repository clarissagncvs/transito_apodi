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


    if (
        item.tipo &&
        item.tipo.toUpperCase() === "ACIDENTE"
    ) {
        classe = "pin-emergencia";
        simbolo = "!";
    }


    else if (item.status === "EM_ANDAMENTO") {
        classe = "pin-andamento";
        simbolo = "⏳";
    }


    else if (
        item.status === "RESOLVIDA" ||
        item.status === "ENCERRADA"
    ) {
        classe = "pin-finalizada";
        simbolo = "✓";
    }


    else if (item.status === "ABERTA") {
        classe = "pin-ativa";
        simbolo = "!";
    }

    return L.divIcon({
        className: "",
        html: `
            <div class="pin-status ${classe}">
                <span>${simbolo}</span>
            </div>
        `,
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

        if (pinUsuario) {
            map.removeLayer(pinUsuario);
        }

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
            console.log("DADOS RECEBIDOS:", data);
            dadosGlobais = data;
            console.log("Sincronizando dados de Apodi...");

            camadaVias.clearLayers();
            if (data.vias && data.vias.length > 0) {
                L.geoJSON(data.vias, {
                    style: { color: "#3388ff", weight: 3, opacity: 0.6 }
                }).addTo(camadaVias);
            }

            camadaOcorrencias.clearLayers();

            if (data.ocorrencias) {
                data.ocorrencias.forEach(item => {
                    if (
                        item.status === 'ABERTA' ||
                        item.status === 'EM_ANDAMENTO' ||
                        item.status === 'RESOLVIDA' ||
                        item.status === 'ENCERRADA'
                    ) {
                        if (item.latitude == null || item.longitude == null) return;

                        const marker = L.marker(
                            [item.latitude, item.longitude],
                            {
                                icon: criarIconeStatus(item)
                            }
                        );

                        const popupConteudo = `
                            <div class="custom-popup">
                                <strong style="color: #e63946;">Ocorrência #${item.id}</strong><br>
                                <b>Endereço:</b> ${item.endereco}<br>
                                <b>Descrição:</b> ${item.descricao}<br>
                                <hr style="margin: 5px 0">
                                <span style="font-size: 10px; color: #666;">Sincronizado às: ${new Date().toLocaleTimeString()}</span>
                            </div>
                        `;

                        marker.bindPopup(popupConteudo);
                        camadaOcorrencias.addLayer(marker);
                    }
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
    console.log("renderizarOcorrencias foi chamada");
    if (!dadosGlobais || !dadosGlobais.ocorrencias) return;

    const lista = document.getElementById("lista-status");
    if (!lista) return;

    lista.innerHTML = "";

    if (!dadosGlobais.ocorrencias || dadosGlobais.ocorrencias.length === 0) {
        lista.innerHTML = "<p class='sem-ocorrencias'>Sem ocorrências no momento</p>";
        return;
    }

    dadosGlobais.ocorrencias.forEach(item => {
        const div = document.createElement("div");
        div.classList.add("ocorrencia");

        div.innerHTML = `
            <div class="tipo">${item.tipo}</div>
            <div class="endereco">${item.endereco}</div>
            <div class="horario">
            ${item.horario
                ? new Date(item.horario).toLocaleTimeString("pt-BR", {
                    hour: "2-digit",
                    minute: "2-digit"
                })
                : "Sem horário"
            }
            </div>
        `;

        lista.appendChild(div);
    });
}

window.addEventListener("load", () => {
    setTimeout(() => map.invalidateSize(), 500);
});

window.addEventListener("resize", () => {
    map.invalidateSize();
});