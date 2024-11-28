let map;
let userLocation = { lat: 0, lng: 0 }; // Localização inicial do usuário
let directionsRenderer = null;  // Gerenciador de rotas no mapa

// Função para obter o token JWT armazenado no localStorage
function getToken() {
    return localStorage.getItem("jwt_token"); // Supondo que o token esteja armazenado no localStorage
}

function initMap() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            userLocation.lat = position.coords.latitude;
            userLocation.lng = position.coords.longitude;

            map = new google.maps.Map(document.getElementById("map"), {
                zoom: 15,
                center: userLocation,
            });

            new google.maps.Marker({
                position: userLocation,
                map: map,
                title: "Você está aqui",
            });

            // Carregar todas as paradas do banco de dados (pins verdes)
            fetch(`/api/all-stops`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${getToken()}`,  // Adiciona o token JWT no cabeçalho
                }
            })
                .then(response => response.json())
                .then(data => {
                    console.log("Todas as paradas: ", data);
                    if (data && data.length > 0) {
                        data.forEach(stop => {
                            const stopLocation = stop.coordinates;

                            // Adicionar marcador verde para todas as paradas do banco
                            const marker = new google.maps.Marker({
                                position: stopLocation,
                                map: map,
                                title: stop.name,
                                icon: {
                                    url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png" // Pino verde
                                }
                            });

                            // Adicionar evento para traçar rota ao clicar
                            marker.addListener("click", function () {
                                console.log("Clicou na parada (verde): ", stop.name);
                                drawRoute(userLocation, stopLocation);
                            });
                        });
                    }
                })
                .catch(error => console.error("Erro ao buscar todas as paradas:", error));
        }, function (error) {
            console.error("Erro ao obter a localização do usuário:", error);
        });
    } else {
        alert("Geolocalização não é suportada pelo seu navegador.");
    }
}

// Função para desenhar a rota entre a localização do usuário e a parada
function drawRoute(start, end) {
    console.log("Desenhando rota de", start, "para", end);

    // Remover rota anterior, se houver
    if (directionsRenderer) {
        directionsRenderer.setMap(null);
    }

    const directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer(); // Nova instância
    directionsRenderer.setMap(map);

    const request = {
        origin: start,  // Localização do usuário
        destination: end,  // Localização da parada
        travelMode: google.maps.TravelMode.WALKING  // Caminhando
    };

    directionsService.route(request, function(result, status) {
        if (status === 'OK') {
            directionsRenderer.setDirections(result);  // Exibe a rota no mapa
            console.log("Rota desenhada com sucesso!");
        } else {
            console.error("Erro ao calcular a rota:", status);
        }
    });
}
