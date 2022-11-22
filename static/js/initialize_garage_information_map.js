const mapDiv = document.querySelector('#map');




let map;

const myLatLng = { lat: garageLatitue, lng: garageLongitude };


window.initMap = function () {
map = new google.maps.Map(mapDiv, {
    center: myLatLng,
    zoom: 14,
    });

new google.maps.Marker({
    position: myLatLng,
    map,
    title: "Twój warsztat",
    });
}

