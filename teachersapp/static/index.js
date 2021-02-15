let map;

function initMap() {
  console.log('InitMap')  
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 52.5200, lng: 13.4050 },
    zoom: 8,
  });

    // Add some markers to the map.
    // Note: The code uses the JavaScript Array.prototype.map() method to
    // create an array of markers based on a given "locations" array.
    // The map() method here has nothing to do with the Google Maps API.
    markers = locations.map(function(location, i) {
      var marker = new google.maps.Marker({
        position: location, 
        map,
        icon : "https://cdn.shopify.com/s/files/1/1290/3375/files/red.png?9786828044575241658"
      });
      google.maps.event.addListener(marker, 'click', function(evt) {
        //infoWindow.setContent(location.info);
        //infoWindow.open(map, marker);
        console.log('Marker clicked');
      });
      return marker;
    });

    /*console.log(markers);
    console.log(markers.length);*/
}