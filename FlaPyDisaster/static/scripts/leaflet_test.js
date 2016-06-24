// Globals
var mymap;
var popup = L.popup();
disableScrollPropagation('mapid')


function leaflet_init() {
    //window.alert("Hello Leaflet")
    mymap = L.map('mapid',
        {
            zoomControl: 'True'
        }).setView([51.505, -0.09], 13);

    //L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    //    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    //    maxZoom: 18,
    //    id: 'mapbox.mapbox-streets-v7',
    //    accessToken: 'sk.eyJ1IjoidW5nYXdhdGt0IiwiYSI6ImNpcHU1b3NzZTA4dGtoN25yZ3p5anBtcDYifQ.sUzXRTPDTqg1QwZvvefNVQ'
    //}).addTo(mymap);

    L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoidW5nYXdhdGt0IiwiYSI6ImNpcHU1aXJ0bDA5MHJma20yN3QwaGthZW8ifQ.oCspKOOXmELA6ETDQK8J1w').addTo(mymap);

    //popup 

    add_handlers()
}

// Add event handlers for map
function add_handlers() {
    window.alert("handlers")
    mymap.on('click', onMapClick);
    mymap.on('scrollWheelZoom', scroll_alert)
}

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(mymap);
}

function scroll_alert() {
    window.alert("Scrolled")
    console.log("Scrolled.")
}
