/* global google */
(function (exports) {
    'use strict';

    function getJson(url, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.setRequestHeader('accept', 'application/json');
        xhr.send(null);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status >= 200 && xhr.status < 300) {
                    callback(JSON.parse(xhr.responseText));
                } else {
                    // An error occurred during the request.
                    console.error('Error: ' + xhr.status, xhr.responseText);
                }
            }
        };
    }


    function createLoader (map) {
        return function (coord, label) {
            return new google.maps.Marker({
                position: coord,
                map: map,
                title: label,
            });
        };
    }


    exports.initMap = function () {
        getJson('/lcp/peaks', function (data) {
            var map = new google.maps.Map(document.getElementById('map'), {
                zoom: 4,
                center: {lat: -25.363, lng: 131.044},
            });
            var loader = createLoader(map);
            for (var i = 0; i < data.peaks.length; i++) {
                var peak = data.peaks[i];
                var coordinates = {
                    lat: peak.coordinates[0],
                    lng: peak.coordinates[1],
                };
                loader(coordinates, peak.name);
            }
        });
    };

})(window);
