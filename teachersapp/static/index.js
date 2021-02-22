let map;
let markers;

function initMap() {
  console.log('InitMap')  
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 52.5200, lng: 13.4050 },
    zoom: 13,
    // disabling some controls. Reference: https://developers.google.com/maps/documentation/javascript/controls
    streetViewControl: false, 
    fullscreenControl: false,
    mapTypeControl: false,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  var mapStyles = [ 
    { 
        "featureType": "administrative", 
        "stylers": [ { "visibility": "off" } ] 
    },{ 
        "featureType": "road", 
        "elementType": "labels", 
        "stylers": [ { "visibility": "off" } ] 
    },{ 
        "featureType": "road", 
        "elementType": "geometry.stroke", 
        "stylers": [ { "visibility": "off" } ] 
    },{ 
        "featureType": "transit", 
        "stylers": [ { "visibility": "off" } ] 
    },{ 
        "featureType": "poi.attraction", 
        "stylers": [ { "visibility": "off" } ] 
    },{ 
        "featureType": "poi.business", 
        "stylers": [ { "visibility": "off" } ] 
    },{ 
        "featureType": "poi.government", 
        "stylers": [ { "visibility": "off" } ] 
    },{ 
        "featureType": "poi.medical", 
        "stylers": [ { "visibility": "off" } ] 
    },{ 
        "featureType": "poi.park", 
        "elementType": "labels", 
        "stylers": [ { "visibility": "off" } ]                  
    },{ 
        "featureType": "poi.place_of_worship", 
        "stylers": [ { "visibility": "off" } ] 
    },{ 
        "featureType": "poi.school", 
        "stylers": [ { "visibility": "off" } ] 
    },{ 
        "featureType": "poi.sports_complex", 
        "stylers": [ { "visibility": "off" } ] 
    },{ 
      "featureType": "road", 
      "elementType": "geometry.fill", 
      "stylers": [ 
          { "visibility": "on" }, 
          { "color": "#ffffff" }
      ] 
    },{ 
        "featureType": "landscape.man_made", 
        "stylers": [ 
            { "visibility": "on" }, 
            { "color": "#dbdbdb" } 
        ] 
    },{ 
        "featureType": "landscape.natural", 
        "elementType": "labels", 
        "stylers": [ { "visibility": "off" } ] 
    }
  ];  
  map.setOptions({ styles: mapStyles });

  google.maps.event.addListener(map, 'idle', function(){
    var zoom = map.getZoom();
    var center = map.getCenter();
    console.log("Map idle zoom:"+zoom);
    console.log("Map idle center:"+center);
    renderMarkers(center, zoom);
  });
}

// TODO: the radius values corresponding to each zoom level
// is just a guesstimation at the moment.
// I plan to place an actual circle in the map to visualize
// the radiuses for each level and adjust as needed.
var radiusToZoomLevel = [
  1000000, // zoom: 0
  1000000, // zoom: 1
  900000, // zoom: 2
  800000, // zoom: 3
  700000, // zoom: 4
  600000, // zoom: 5
  500000, // zoom: 6
  400000, // zoom: 7
  300000, // zoom: 8
  200000, // zoom: 9
  100000, // zoom: 10
  50000, // zoom: 11
  20000, // zoom: 12
  10000, // zoom: 13
  8000, // zoom: 14
  6000, // zoom: 15
  3000, // zoom: 16
  1500, // zoom: 17
  1000, // zoom: 18
  500,  // zoom: 19
  100   // zoom: 20
];

function renderMarkers(mapCenter, zoomLevel) {
  // If we had already some markers in the map, we need to clear them
  clearMarkers();

  // we call the backend to get the list of markers
  var params = {
    "lat" : mapCenter.lat(),
    "lng" : mapCenter.lng(),
    "radius" : radiusToZoomLevel[zoomLevel]
  }
  var url = "http://localhost:5000/api/get_profiles_in_radius?" + dictToURI(params) 
  loadJSON(url, function(response) {
    // Parse JSON string into object
      var actual_JSON = JSON.parse(response);
      console.log(actual_JSON);

      // place new markers in the map
      placeTeachingProfilesInMap(actual_JSON)
   });
}

var DEFAULT_ICON = {
  path: mapIcons.shapes.MAP_PIN,
  fillColor: '#dd7f7f',
  fillOpacity: 1,
  strokeColor: '#9c4343',
  strokeWeight: 1.5
}

var SELECTED_ICON = {
  path: mapIcons.shapes.MAP_PIN,
  fillColor: '#e73636',
  fillOpacity: 1,
  strokeColor: '#9c4343',
  strokeWeight: 1.5
}

//When the user clicks on a marker, it will become
// the selected one:
var selectedMarker = null;

function placeTeachingProfilesInMap(profiles) {
    // Add some markers to the map.
    // Note: The code uses the JavaScript Array.prototype.map() method to
    // create an array of markers based on the given "profiles" array.
    // The map() method here has nothing to do with the Google Maps API.
    markers = profiles.map(function(profile, i) {
      var marker = new mapIcons.Marker({
        map: map,
        position: profile.location, 
        icon: DEFAULT_ICON,
        map_icon_label: '<span class="map-icon map-icon-male"></span>'
      });

      //we attach the profile to the marker, so when the marker is selected
      //we can get all the profile data to fill the highlighted profile box under
      // the map 
      marker.profile = profile;

      google.maps.event.addListener(marker, 'click', function(evt) {
        markerClick(this);
      });

      return marker;
    });

    /*console.log(markers);
    console.log(markers.length);*/
}

function clearMarkers() {
  if (markers) {
    markers.map(function(marker, i) {
      marker.setMap(null);
    });
  }
    
  markers = new Array();
  selectedMarker = null;
}

function markerClick(marker) {
  console.log('Marker clicked');
  console.log(marker);

  // de-select the previously active marker, if present
  if (selectedMarker) selectedMarker.setIcon(DEFAULT_ICON);
  marker.setIcon(SELECTED_ICON);

  // Fill in the Highlighted Profile article with
  // the marker profile data:
  document.getElementById('hpUser').innerHTML=marker.profile.user_name;
  document.getElementById('hpAddress').innerHTML=marker.profile.address;
  document.getElementById('hpLanguages').innerHTML="Teaches "+marker.profile.languages;
  document.getElementById('hpTitle').innerHTML=marker.profile.title;
  document.getElementById('hpDescription').innerHTML=marker.profile.description;
  
  // upadete selected marker reference
  selectedMarker = marker;
}

function loadJSON(url, callback) {   
  var xobj = new XMLHttpRequest();
  
  xobj.overrideMimeType("application/json");
  xobj.open('GET', url, true); 
  xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
          // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
          callback(xobj.responseText);
        }
        //TODO: what to do in case of failures?
  };
  xobj.send(null);  
}

function dictToURI(dict) {
  var str = [];
  for(var p in dict){
     str.push(encodeURIComponent(p) + "=" + encodeURIComponent(dict[p]));
  }
  return str.join("&");
}