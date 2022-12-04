garages.forEach(garage => {
    garage.fields.location  = garage.fields.location.split(', ')


    garage.fields.location = garage.fields.location.filter(function(value, index, arr){ 
        return !isNaN(value);
    });

    for (let i = 0; i < garage.fields.location.length; i++) {
        garage.fields.location[i] = parseFloat(garage.fields.location[i])
    }

});

window.initMap = function () {

let map = new google.maps.Map(document.getElementById('map'), {
    zoom: 6,
    center: new google.maps.LatLng(52, 19.145136),
    mapTypeId: google.maps.MapTypeId.ROADMAP
});

let infowindow = new google.maps.InfoWindow();

let marker, i;

//INITIALIZE AUTOMCOMPLETE SEARCH
function activatePlacesSearch() {

let input = document.getElementById('search-input');
let autocomplete = new google.maps.places.Autocomplete(input);
autocomplete.bindTo("bounds", map);

autocomplete.addListener("place_changed", () => {
    infowindow.close();

    const place = autocomplete.getPlace();

    if (!place.geometry || !place.geometry.location) {
      // User entered the name of a Place that was not suggested and
      // pressed the Enter key, or the Place Details request failed.
      window.alert("Wybierz miejsce z listy rozwijalnej");
      return;
    }

    // If the place has a geometry, then present it on a map.
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(17);
    }
  });
}
activatePlacesSearch();

//ITER OVER GARAGES AND ADDING MARKERS
for (i = 0; i < garages.length; i++) {  
    marker = new google.maps.Marker({
    position: new google.maps.LatLng(garages[i].fields.location[0], garages[i].fields.location[1]),
    map: map
    });
    
    google.maps.event.addListener(marker, 'click', (function(marker, i) {
    return function() {
        informationHref = '/garage/information/' + garages[i].pk
        reservationHref = '/order/reserve/' + garages[i].pk
        let websiteStringUrl
        if (garages[i].fields.website_url == '')
            websiteStringUrl = "Brak informacji o stronie internetowej"
        else
            websiteStringUrl = '<a href="' + garages[i].fields.website_url + '">'+ garages[i].fields.website_url + ' </a>'

        if (garages[i].fields.description == '')
            garages[i].fields.description = "Brak opisu warsztatu"

        infowindow.setContent(
            '<div id="bodyContent">'+
            '<h5>' + garages[i].fields.name + '</h5>'+
            '<p class="mb-1">' + garages[i].fields.full_address + '</p>'+
            websiteStringUrl +
            '<p class="mt-1" > Opis warsztatu: ' + garages[i].fields.description + '</p>'+
            '<hr>'+
            '<a class="link-button me-2" href="' + reservationHref + '">Umów wizytę <i class="fa-solid fa-calendar-days ms-1 mb-4"></i> </a>' +
            '<a class="link-button" href="' + informationHref + '">Więcej informacji <i class="fa-solid fa-circle-info ms-1"></i> </a>' +
            '</div>'
            );
        infowindow.open(map, marker);
    }
    })(marker, i));
}}