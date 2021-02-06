let map;

function initMap() {
  console.log('InitMap')  
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 52.5200, lng: 13.4050 },
    zoom: 8,
  });
}