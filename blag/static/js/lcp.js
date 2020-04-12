/* global google */
(function (exports) {
    'use strict';

    function createLoader (map) {
        return function (coord, label) {
            var infowindow = new google.maps.InfoWindow({
                content: "<span>" + label + "</span>"
            });
            var marker = new google.maps.Marker({
                position: coord,
                map: map,
            });
            google.maps.event.addListener(marker, 'mouseover', function() {
              infowindow.open(map, marker);
            });
            google.maps.event.addListener(marker, 'mouseout', function () {
              infowindow.close();
            });
            return marker;
        };
    }


    exports.initMap = function () {
        getJson('/lcp/peaks', function (data) {
            var map = new google.maps.Map(document.getElementById('map'), {
                zoom: 2,
                center: {lat: 45, lng: 0},
                mapTypeId: 'satellite',
            });
            // var loader = createLoader(map);
            // for (var i = 0; i < data.peaks.length; i++) {
            //     var peak = data.peaks[i];
            //     var coordinates = {
            //         lat: peak.coordinates[0],
            //         lng: peak.coordinates[1],
            //     };
            //     loader(coordinates, peak.name);
            // }
            var heatmap = new google.maps.visualization.HeatmapLayer({
                data: data,
                radius: 10,
                opacity: 1,
            });
            heatmap.setMap(map);
        });
    };
    function getJson(url, callback) {
      callback([
          {location: new google.maps.LatLng(61.524010, 105.318756), weight: 30310},
          {location: new google.maps.LatLng(7.289574, 81.674355), weight: 150},
      ]);
    }
})(window);
