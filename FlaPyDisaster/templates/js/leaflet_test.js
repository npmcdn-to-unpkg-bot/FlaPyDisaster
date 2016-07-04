// Globals
var mymap;
var popup = L.popup();
var last_point_clicked;
var layers = {};

/*
Initialization function for leaflet page, runs on the html.body.onload
*/
function leaflet_init() {
    //window.alert("Hello Leaflet")
    init_map();

    //L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoidW5nYXdhdGt0IiwiYSI6ImNpcHU1aXJ0bDA5MHJma20yN3QwaGthZW8ifQ.oCspKOOXmELA6ETDQK8J1w').addTo(mymap);

    // Add a map tile layer to the leaflet map.  Uses the standard streets maps
    L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
        accessToken: 'pk.eyJ1IjoidW5nYXdhdGt0IiwiYSI6ImNpcHU1aXJ0bDA5MHJma20yN3QwaGthZW8ifQ.oCspKOOXmELA6ETDQK8J1w'
    }).addTo(mymap);

    // Create a layer to hold user placed markers through the standard function (which needs way more work)
    create_layer('marker_layer')

    // Create a standard geoJSON layer for lines, polygons, etx
    var myLayer = L.geoJson().addTo(mymap);
    layers['geoJSON'] = myLayer

    // Create a geogjson layer to handle points.  The function passed to "pointsToLayer" converts points to an orange circle, instead of markers.
    // Need to figure out how to update that style post creation
    var pointsLayer = L.geoJson([], {
        pointToLayer: function (feature, latlng) {
            var geojsonMarkerOptions = {
                radius: 8,
                fillColor: "#ff7800",
                color: "#000",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8
            };
            return L.circleMarker(latlng, geojsonMarkerOptions);
        }
    }).addTo(mymap)
    layers['point_geoJSON'] = pointsLayer

    // call a function that handles adding any required event handlers
    add_handlers()

    // prove we got here in the log
    console.log("Did leaflet init")
}

// Add event handlers for map
function add_handlers() {
    mymap.on('click', onMapClick);
}

/*
On Click handler to add a marker to the map on click if the control checkbox is checked.
Also stores the click location for debugging
*/
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

/*
Initialize leaflet map, setting the view to Somerville, MA, with a zoom level of 13
*/
function init_map() {
    mymap = L.map('mapid',
        {
            zoomControl: 'True'
        }).setView([42.39, -71.11], 13);
}

/*
Function to add a generic layer to the leaflet map, and store a reference to the layer
*/
function create_layer(layer_name){
    var Layer = L.layerGroup().addTo(mymap);
    layers[layer_name] = Layer
}

/*
function to clear the content from a leaflet layer.  Does NOT remove the layer
*/
function clear_layer(layer_name) {
    layers[layer_name].clearLayers()
}

/*
test function to place a marker at the last point click on the map
*/
function place_last_marker_test() {
    place_marker(last_point_clicked, true)
}

/*
Places a merker at the given point.
If 'log_point' is true, logs the placement to javascript and python the console.
Python server logging is accomplished through a JQuery ajax POST
*/
function place_marker(latlng, log_point) {

    // Add marker to map
    var marker = L.marker(latlng)
    layers['marker_layer'].addLayer(marker);

    // Log point to javascript console
    if (log_point) {
        var data = {};
        data["lat"] = latlng.lat.toString()
        data["lng"] = latlng.lng.toString()
        console.log(data)
    }

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

/*
Remove all layers from the map.  Need to convert this to a loop
*/
function clear_map() {
    clear_layer('marker_layer')
    clear_layer('geoJSON')
    clear_layer('point_geoJSON')
    
    // for layer in layers {clear layer} ?
    //for (var layer in layers) {
    //    clear_layer(layer[0])
    //}
}

/*
Little test event function to log the state of the add marker checkbox
*/
function alert_state() {
    var cb = document.getElementById('add_marker_CBX');
    
    console.log(cb.checked)
}

/*
Function to get a geoJSON line from the server and plot it on the leaflet map.
The color of the map is controlled by interpolating the properties.value value associated with the geoJSON object
*/
function geojson_test() {
    // JQuery getJSON call to python server to get geoJSON string
    $.getJSON("{{ url_for('leaflet_geojson_test') }}", {},
        function (data) {
            // Add new jsoon to layer
            layers['geoJSON'].addData(data.result).setStyle(
                function(feature){
                    return {
                        // Interpolate the color based on the value, and passed in max and min
                        color: get_interpolated_color(feature.properties.value, data.max, data.min),
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

/*
funtion to get a geoJSON multipoint layer from the server and plot it on the leaflet map.
*/
function geojson_points_test() {
    $.getJSON("{{ url_for('leaflet_geojson_points_test') }}", {},
        function (data) {
            // Add with static style.  Need to implement dynamic styles somehow
            layers['point_geoJSON'].addData(data.result)
        }
    )
}

/*
function to get an example leaflet style
*/
function get_simple_style_test() {
    var myStyle = {
        "color": "#ff7800",
        "weight": 5,
        "opacity": 0.65
    };

    return myStyle;
}

/*
return the interpolated color in rgb format for a leaflet style
*/
function get_interpolated_color(feature, max, min) {
    c = color_interp(value, max, min)
    return "rgb(" + c.r + ", " + c.g + ", " + c.b + ")"

}

/*
Function that uses linear interpolation between a max and min color/value pair to get the color associated with an input value.
Colors are interpolated in the RGB space, each channel separately
Opacity (A) can be toggled
if no color is supplied, th
*/
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