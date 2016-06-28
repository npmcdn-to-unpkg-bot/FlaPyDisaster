// Globals
var mymap;
var popup = L.popup();
var last_point_clicked;
var mainLayer;

function init_map() {
    mymap = L.map('mapid',
        {
            zoomControl: 'True'
        }).setView([42.39, -71.11], 13);
}

function leaflet_init() {
    //window.alert("Hello Leaflet")
    init_map();

    //L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    //    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    //    maxZoom: 18,
    //    id: 'mapbox.mapbox-streets-v7',
    //    accessToken: 'sk.eyJ1IjoidW5nYXdhdGt0IiwiYSI6ImNpcHU1b3NzZTA4dGtoN25yZ3p5anBtcDYifQ.sUzXRTPDTqg1QwZvvefNVQ'
    //}).addTo(mymap);

    //L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoidW5nYXdhdGt0IiwiYSI6ImNpcHU1aXJ0bDA5MHJma20yN3QwaGthZW8ifQ.oCspKOOXmELA6ETDQK8J1w').addTo(mymap);

    L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
        accessToken: 'pk.eyJ1IjoidW5nYXdhdGt0IiwiYSI6ImNpcHU1aXJ0bDA5MHJma20yN3QwaGthZW8ifQ.oCspKOOXmELA6ETDQK8J1w'
    }).addTo(mymap);

    mainLayer = L.layerGroup().addTo(mymap)
    console.log("Did that")
    add_handlers()
}

// Add event handlers for map
function add_handlers() {
    mymap.on('click', onMapClick);
    mymap.on('scrollWheelZoom', scroll_alert)
}

function onMapClick(e) {
    //popup
    //    .setLatLng(e.latlng)
    //    .setContent("You clicked the map at " + e.latlng.toString())
    //    .openOn(mymap);

    last_point_clicked = e.latlng;
}

function scroll_alert() {
    window.alert("Scrolled");
    console.log("Scrolled.");
}

function place_marker(latlng, log_point) {
    var data = {};
    data["lat"] = latlng.lat.toString()
    data["lng"] = latlng.lng.toString()
    console.log(data)
        
    if (log_point) {
        //$.post("{{ url_for('leaflet_test_latlng') }}", data)
        $.ajax({
            type: "POST"
            , url: "{{ url_for('leaflet_test_latlng') }}"
            , data: JSON.stringify(data, null, '\t')
            , contentType: 'application/json;charset=UTF-8'
            , success: function (result) { return undefined }
        });
    }
    mainLayer.addLayer(latlng);
}

function place_last_marker_test() {
    place_marker(last_point_clicked, true)
}

function clear_markers() {
    mainLayer.removeLayers();
}