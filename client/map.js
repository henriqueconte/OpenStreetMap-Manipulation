
var map = L.map('map').setView([45.15, 5.75], 13);

var layers = {
    'highway': { name: 'Highways', default: true },
    'amenity': { name: 'Amenity', default: true },
    'waterway': { name: 'Waterway', default: true }
};

var CartoDB_Positron = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
	subdomains: 'abcd',
	maxZoom: 19
});

var baseMaps = {"Fond de carte":  CartoDB_Positron};
map.addLayer(CartoDB_Positron);

var overlayOptions = {};

for (element in layers) {
    overlayOptions[element] = L.tileLayer.wms("http://localhost:4242/wms", {
        layers: element,
        format: 'image/png',
        transparent: true
    });
}

L.control.layers(baseMaps, overlayOptions).addTo(map);

for (element in overlayOptions) {
    if (layers[element].default) {
        map.addLayer(overlayOptions[element]);
    }
}
