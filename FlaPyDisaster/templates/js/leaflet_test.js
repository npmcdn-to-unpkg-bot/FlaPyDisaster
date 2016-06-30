// Globals
var mymap;
var popup = L.popup();
var last_point_clicked;
var layers = {};

function init_map() {
    mymap = L.map('mapid',
        {
            zoomControl: 'True'
        }).setView([42.39, -71.11], 13);
}

function leaflet_init() {
    //window.alert("Hello Leaflet")
    init_map();

    //Add basic layers
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

    create_layer('marker_layer')
    var myLayer = L.geoJson().addTo(mymap);
    layers['geoJSON'] = myLayer

    //add handlers
    add_handlers()

    //prove we got here
    console.log("Did that")
}

function create_layer(layer_name){
    var Layer = L.layerGroup().addTo(mymap);
    layers[layer_name] = Layer
}

function clear_layer(layer_name) {
    layers[layer_name].clearLayers()
}

// Add event handlers for map
function add_handlers() {
    mymap.on('click', onMapClick);
    mymap.on('scrollWheelZoom', scroll_alert)
}

function onMapClick(e) {
    // Popup example
    //popup
    //    .setLatLng(e.latlng)
    //    .setContent("You clicked the map at " + e.latlng.toString())
    //    .openOn(mymap);

    last_point_clicked = e.latlng;

    var add_point_cbx = document.getElementById('add_marker');
    if (add_point_cbx.checked) {
        place_marker(e.latlng, true)
    }
}

function place_last_marker_test() {
    place_marker(last_point_clicked, true)
}

function place_marker(latlng, log_point) {
    var data = {};
    data["lat"] = latlng.lat.toString()
    data["lng"] = latlng.lng.toString()
    console.log(data)
    
    var marker = L.marker(latlng)
    layers['marker_layer'].addLayer(marker);

    // Ajax call if logging point to python, stick with this format probably, more standard
    if (log_point) {
        $.ajax({
            type: "POST"
            , url: "{{ url_for('leaflet_test_latlng') }}"
            , data: JSON.stringify(data, null, '\t')
            , contentType: 'application/json;charset=UTF-8'
            , success: function (result) { return undefined }
        });
    }
}

function clear_markers() {
    clear_layer('marker_layer')
    clear_layer('geoJSON')
}

function alert_state() {
    var cb = document.getElementById('add_marker');
    
    console.log(cb.checked)
}

function geojson_test() {
    $.getJSON("{{ url_for('leaflet_geojson_test') }}", {},
        function (data) {

            //myStyle = get_simple_style_test();

            // Add new jsoon to layer
            layers['geoJSON'].addData(data.result).setStyle(
                function(feature){
                    return {
                        color: get_graduated_style_test(feature, data.max, data.min),
                        weight: 5,
                        opacity: 1
                    }
                })
            /*
             var geojson_layer = L.geoJSON(data.result, {
                style: function(feature){
                    return {
                        color: get_graduated_style_test(feature, data.max, data.min),
                        weight: 5,
                        opacity: 1
                    }
                }
            }).addTo(mymap);
             */
        }
    )
}

function get_simple_style_test() {
    var myStyle = {
        "color": "#ff7800",
        "weight": 5,
        "opacity": 0.65
    };

    return myStyle;
}

function get_graduated_style_test(feature, max, min) {
    c = color_interp(feature.properties.value, max, min)
    return "rgb(" + c.r + ", " + c.g + ", " + c.b + ")"

}

function color_interp(value, max, min, color_max, color_min, incl_a) {
    incl_a = typeof incl_a !== 'undefined' ? color_max : false
    color_max = typeof color_max !== 'undefined' ? color_max : { a: 255, r: 255, g: 0, b: 0 }
    color_min = typeof color_min !== 'undefined' ? color_min : { a: 255, r: 0, g: 0, b: 255 }
    max = typeof max !== 'undefined' ? max : 100
    min = typeof min !== 'undefined' ? min : 0

    if (value >= max) {
        return color_max;
    }

    if (value <= min) {
        return color_min
    }

    a_new = incl_a ? Math.round(linear_interpolate(value, min, max, Math.min(color_min.a, color_max.a), Math.max(color_min.a, color_max.a))) : 255
    r_new = Math.round(linear_interpolate(value, min, max, Math.min(color_min.r, color_max.r), Math.max(color_min.r, color_max.r)))
    g_new = Math.round(linear_interpolate(value, min, max, Math.min(color_min.g, color_max.g), Math.max(color_min.g, color_max.g)))
    b_new = Math.round(linear_interpolate(value, min, max, Math.min(color_min.b, color_max.b), Math.max(color_min.b, color_max.b)))

    return { a: a_new, r: r_new, g: g_new, b: b_new }
}

function linear_interpolate(x, x0, x1, y0, y1)
{
    return  y0 + ((y1 - y0)*((x-x0) / (x1-x0)))
}