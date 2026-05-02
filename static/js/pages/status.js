//iniciando o mapa com o id do elemento div para informar onde o mapa será 'ilustrado', depois seleciona a latitude e a longitude de Apodi com o zoom, respectivamente
var map = L.map('map').setView([-5.66417, -37.79889], 17);

//camada do OpenStreetMap
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 17,
    attribution: '© OpenStreetMap'
}).addTo(map);

//criação dos containers para limpeza automática
//o layerGroup é o que permite apagar as ocorrências fechadas
const camadaVias = L.layerGroup().addTo(map);
const camadaOcorrencias = L.layerGroup().addTo(map);

//função que busca e desenha tudo
function atualizarDashboard() {
    fetch('/api/vias/mapa/')
        .then(response => {
            if (!response.ok) throw new Error("Erro na rede");
            return response.json();
        })
        .then(data => {
            console.log("Sincronizando dados de Apodi...");

            //desenhar vias
            camadaVias.clearLayers();
            if (data.vias && data.vias.length > 0) {
                L.geoJSON(data.vias, {
                    style: { color: "#3388ff", weight: 3, opacity: 0.6 }
                }).addTo(camadaVias);
            }

            //desenar ocorrências
            //limpar tudo para que as fechadas desapareçam
            camadaOcorrencias.clearLayers();

            if (data.ocorrencias) {
                data.ocorrencias.forEach(item => {
                    //só desenha se o status for 'aberto'
                    if (item.status === 'aberto') {
                        const marker = L.marker([item.latitude, item.longitude]);

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
        })
        .catch(err => console.error("Falha ao atualizar mapa:", err));
}

//execução e intervalo
atualizarDashboard(); //roda ao abrir a página
setInterval(atualizarDashboard, 15000); //atualiza a cada 15 segundos