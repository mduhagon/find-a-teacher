let map;
let markers;

let geocoder;

let queryCenter; 
let queryZoom;

function initMap() {
  console.log('InitMap')
  
  geocoder = new google.maps.Geocoder();

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 52.5200, lng: 13.4050 }, //We start at the center of Berlin
    zoom: 13,
    minZoom: 6,
    maxZoom: 19,
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
    var newZoom = map.getZoom();
    var newCenter = map.getCenter();

    console.log("Map  event triggers, zoom:"+newZoom+", center: "+newCenter);

    // I want to avoid re-rendering the markers if the change
    // in position within the map is too small. Also, if we are zooming in
    // without changing the center significantly, there is also no need
    // to call the backend again for new points
    var distanceChange = (queryCenter == null) ? 0 : google.maps.geometry.spherical.computeDistanceBetween (queryCenter, newCenter);

    if (queryCenter == null || queryZoom == null || distanceChange > 100 || newZoom < queryZoom) { //if we have not queried for markers yet, query
      refreshMarkers(newCenter, newZoom);
    }  
  });
}

var radiusToZoomLevel = [
  800000, // zoom: 0
  800000, // zoom: 1
  800000, // zoom: 2
  800000, // zoom: 3
  800000, // zoom: 4
  800000, // zoom: 5 --- From 5 up it would not really be reachabe as I have constrained the zoom range
  800000, // zoom: 6
  400000, // zoom: 7
  200000, // zoom: 8
  100000, // zoom: 9
  51000, // zoom: 10
  26000, // zoom: 11
  13000, // zoom: 12
  6500, // zoom: 13
  3500, // zoom: 14
  1800, // zoom: 15
  900, // zoom: 16
  430, // zoom: 17
  210, // zoom: 18
  120,  // zoom: 19
];

function refreshMarkers(mapCenter, zoomLevel) {
  console.log("refreshing markers")
  //Update query cener and zoom so we know in referenec to what
  //we queried for markers the last time and can decide if a re-query is needed
  queryCenter = mapCenter;
  queryZoom = zoomLevel;

  // If we had already some markers in the map, we need to clear them
  clearMarkers();

  // This will helpt to understand the radius, its for debug only
  //createCircle(mapCenter,radiusToZoomLevel[zoomLevel]);

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

// To be able to better understand if the radius in which I search for 
// teachers is well adjussted to the level of zoom of the map, 
// I add this function to draw a circle showing the radius
function createCircle(latLng,radius) {
	options = getDefaultDrawingOptions();

	options['map']=map;
	options['center']=latLng;
	options['radius']=radius;

	var circle = new google.maps.Circle(options);
	circle.drawing_type = "circle";
}

function getDefaultDrawingOptions() {
  options = new Array();
  options['strokeColor']  = "#000000";
  options['strokeOpacity'] = 0.8;
  options['strokeWeight'] = 2;
  options['fillOpacity'] = 0;
  options['geodesic'] = false;
  options['editable'] = false;
  options['draggable'] = false;
	
	return options;
}

function searchAddressSubmit() {
  console.log('searchAddressSubmit');

  const address = document.getElementById("search_address").value;
  geocoder.geocode({ address: address }, (results, status) => {
    if (status === "OK") {
      document.getElementById('addressHelpBlock').innerHTML="Perfect! Here are the results near you:";
      map.setZoom(15);
      map.setCenter(results[0].geometry.location);
    } else {
      console.log("Geocode was not successful for the following reason: " + status);
      document.getElementById('addressHelpBlock').innerHTML="Sorry! That search did not work, try again!";
    }
  });

  //prevent refresh
  return false;
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