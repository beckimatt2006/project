let map = null;
let routeLine = null;
let markers = [];
console.log("script.js loaded ");

window.addEventListener("load", () => {
  console.log("window load fired ");
  console.log("Leaflet L exists?", typeof L !== "undefined");
  const el = document.getElementById("map");
  console.log("#map exists?", !!el);
  if (el) console.log("#map rect:", el.getBoundingClientRect());
});
function initMap() {
  if (map) return;

  if (typeof L === "undefined") {
    console.error("Leaflet not loaded: L is undefined");
    return;
  }

  const el = document.getElementById("map");
  if (!el) {
    console.error("Map div not found: #map");
    return;
  }

  console.log("Initializing Leaflet map...");

  map = L.map("map").setView([25.2532, 55.3657], 3);

  L.tileLayer(
  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
  {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 18
  }).addTo(map);

  L.control.scale().addTo(map);

  setTimeout(() => map.invalidateSize(), 150);
}
function clearRoute() {
  if (routeLine) {
    map.removeLayer(routeLine);
    routeLine = null;
  }
  markers.forEach(m => map.removeLayer(m));
  markers = [];
}

function drawRoute(routeCoords) {
  initMap();
  clearRoute();

  const latlngs = routeCoords.map(p => [p.latitude, p.longitude]);

  routeCoords.forEach(p => {
    const m = L.marker([p.latitude, p.longitude]).addTo(map).bindPopup(p.code);
    markers.push(m);
  });

  routeLine = L.polyline(latlngs, {
  color: "#22c55e",   
  weight: 5,
  opacity: 0.85,
  dashArray: "8 6"     
  }).addTo(map);
  routeLine.setStyle({
  className: "glow-line"
  });
  map.fitBounds(routeLine.getBounds(), { padding: [30, 30] });
}

async function runSim() {
  initMap();

  const data = {
    origin: document.getElementById("origin").value,
    destination: document.getElementById("destination").value,
    aircraft_type: document.getElementById("aircraft").value,
    weather_factor: 1.0
  };

  const res = await fetch("http://127.0.0.1:8000/api/optimize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  if (!res.ok) {
    const msg = await res.text();
    alert("API error: " + msg);
    return;
  }

  const result = await res.json();

  
  if (typeof renderSummary === "function" && result.best) {
    renderSummary(result.best);
  }

  
  if (result.route_coords) {
    drawRoute(result.route_coords);
  } else {
    alert("No route_coords returned from API");
  }

  
  if (result.graph) {
    const img = document.getElementById("graph");
    if (img) img.src = "http://127.0.0.1:8000/" + result.graph + "?t=" + Date.now();
    document.getElementById("graphBox").style.display = "block";
  }
}

window.addEventListener("load", () => {
  initMap();
});

function formatNumber(n) {
  return Number(n).toLocaleString(undefined, { maximumFractionDigits: 2 });
}
function renderSummary(best) {
  const routeStr = best.route.join(" → ");
  const summaryHTML = `
    <h2>Optimal Route</h2>
    <p><strong>Route:</strong> ${routeStr}</p>
    <p><strong>Total Distance:</strong> ${formatNumber(best.distance_km)} km</p>
    <p><strong>Total Fuel:</strong> ${formatNumber(best.fuel_kg)} kg</p>
    <p><strong>Total Carbon Emission:</strong> ${formatNumber(best.carbon_kg)} kg CO2</p>
    <p><strong>Safety Score:</strong> ${formatNumber(best.safety_score)} /100</p>
  `;
  document.getElementById("routeHeader").innerHTML = summaryHTML;
  document.getElementById("routeHeader").style.display = "block";
} 
