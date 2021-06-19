/* Set up the initial map center and zoom level */
window.addEventListener('load', function () {


  var greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  var map_div = document.getElementById("map");
  var map = L.map(map_div, {
    center: [35.1264, 33.4299], // EDIT coordinates to re-center map
    zoom: 9,  // EDIT from 1 (zoomed out) to 18 (zoomed in)
    scrollWheelZoom: true,
    tap: false
  });
  /* display basemap tiles -- see others at https://leaflet-extras.github.io/leaflet-providers/preview/ */
  L.tileLayer(
    'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: ''
  }).addTo(map);

  //var number = String(prompt("Enter number of fire stations"));

  let fires_url = 'http://213.133.90.205:5001/fires'
  fetch(fires_url)
  .then(res => res.json())
  .then((out) => {
    fire_locations = out["data"];
    console.log("Saved fire locations");
  })
  .then((out) => {
    //preprocessing to find average weight
    total = 0;
    for (i = 0; i < fire_locations.length; i++) {
      total += fire_locations[i][2];
    }
    average = total/fire_locations.length;
    //console.log(average);
    for (i = 0; i < fire_locations.length; i++) {
      factor_difference = (fire_locations[i][2] - average) / average;
      //console.log(factor_difference);
      factor = 1 + factor_difference;
      console.log(factor);
      //console.log(factor);
      L.circle([fire_locations[i][1], fire_locations[i][0]], {
          color: "red",
          fillColor: "#f03",
          fillOpacity: 0.5,
          radius: 200.0 * factor
      }).addTo(map);
    }

  })
});

function sendData() {
  firestations = document.getElementById("firestations").value;
  country = document.getElementById("country").value;
  //Weights
  frp = document.getElementById('frp').checked ? "1":"0"
  elevation = document.getElementById('frp').checked ? "1":"0"
  vegetation = document.getElementById('frp').checked ? "1":"0"
  let url = 'http://213.133.90.205:5001/get?num=' + firestations + "&weight_control=" + frp + "," + elevation + "," + vegetation
  console.log(url);
  fetch(url)
  .then(res => res.json())
  .then((out) => {
    fire_stations = out;
    console.log("Done");
  })
  .then((out) => {
    //old_fire_stations = fire_stations["old"];
    new_fire_stations = fire_stations["new"];
    /*
    for (i = 0; i < old_fire_stations.length; i++) {
        L.marker([old_fire_stations[i][1], old_fire_stations[i][0]], {icon: greenIcon}).addTo(map) // EDIT marker coordinates
        .bindPopup("Current fire station \n" + String(old_fire_stations[i][1])+","+String(old_fire_stations[i][0])); // EDIT pop-up text message
        console.log("added!");
    }
    */

    console.log("adding new fire stations");
    for (i = 0; i < new_fire_stations.length; i++) {
        L.marker([new_fire_stations[i][1], new_fire_stations[i][0]]).addTo(map) // EDIT marker coordinates
        .bindPopup("New fire station \n" + String(new_fire_stations[i][1])+","+String(new_fire_stations[i][0])); // EDIT pop-up text message
        console.log("added!");
    }
  })
  .catch(err => { throw err });

  /*
  old_fire_stations = fire_stations["old"];
  new_fire_stations = fire_stations["new"];
  for (i = 0; i < old_fire_stations.length; i++) {
      L.marker([old_fire_stations[i][1], old_fire_stations[i][0]], {icon: greenIcon}).addTo(map) // EDIT marker coordinates
      .bindPopup(String(old_fire_stations[i][1])+","+String(old_fire_stations[i][0])); // EDIT pop-up text message
      console.log("added!");
  }

  console.log("adding new fire stations");
  for (i = 0; i < new_fire_stations.length; i++) {
      L.marker([new_fire_stations[i][1], new_fire_stations[i][0]]).addTo(map) // EDIT marker coordinates
      .bindPopup(String(new_fire_stations[i][1])+","+String(new_fire_stations[i][0])); // EDIT pop-up text message
      console.log("added!");
  }
  */


  /* Display a point marker with pop-up text */

}




  function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
      x.className += " responsive";
    } else {
      x.className = "topnav";
    }
  }
