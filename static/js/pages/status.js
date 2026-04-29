/* iniciando o mapa com o id do elemento div para informar onde o mapa será 'ilustrado', depois seleciona a latitude e a longitude de Apodi com o zoom, respectivamente */
var map = L.map('map').setView([-5.64953, -37.7958], 13);

/* adiciona a camada do OpenStreetMap */
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 13,
    attribution: '© OpenStreetMap'
}).addTo(map);