/* =========================================================
   Last Catch — LOCATION
   Everything location-related:
   1. Asks the user for their location (GPS, with permission)
   2. Falls back to a default fishing town if location is blocked
   3. Calculates distance between two points (km)
   4. Draws a map with every catch as a colored freshness dot
   5. Lists nearby catches, spoiling soonest first
   Needs: Leaflet (loaded in index.html) and model2/model2.js (liveStatus, formatHours)
   ========================================================= */

// ---------- Global variables ----------
const DEFAULT_LOCATION = { lat: -34.80, lng: 20.05, name: "Struisbaai, Western Cape" };
let userLat = DEFAULT_LOCATION.lat;
let userLng = DEFAULT_LOCATION.lng;
let locationSource = "default";      // "gps" if the user shared location, otherwise "default"
let map = null;
let mapLayer = null;                 // holds the dots so they can be redrawn

// ---------- 1 + 2. Get the user's location ----------
function getLocation() {
  return new Promise(resolve => {
    if (!navigator.geolocation) return resolve(useDefault("this browser doesn't support location"));
    navigator.geolocation.getCurrentPosition(
      pos => {
        userLat = pos.coords.latitude;
        userLng = pos.coords.longitude;
        locationSource = "gps";
        resolve({ lat: userLat, lng: userLng, source: "gps" });
      },
      err => resolve(useDefault(err.code === 1 ? "location permission was denied" : "location unavailable")),
      { enableHighAccuracy: false, timeout: 8000, maximumAge: 5 * 60 * 1000 }
    );
  });
}

function useDefault(reason) {
  userLat = DEFAULT_LOCATION.lat;
  userLng = DEFAULT_LOCATION.lng;
  locationSource = "default";
  return { lat: userLat, lng: userLng, source: "default", reason };
}

function locationLabel() {
  return locationSource === "gps"
    ? "📍 Using your location"
    : `📍 Using demo location: ${DEFAULT_LOCATION.name} (share your location to see catches near you)`;
}

// ---------- 3. Distance between two points (Haversine formula) ----------
function distanceKm(lat1, lng1, lat2, lng2) {
  const R = 6371;                                   // Earth radius in km
  const toRad = d => d * Math.PI / 180;
  const dLat = toRad(lat2 - lat1), dLng = toRad(lng2 - lng1);
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

const esc = t => String(t).replace(/[&<>"]/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch]));

// ---------- Demo sellers so the map is never empty ----------
// Placed around the user's location. b and m come from running the real models on sample catches.
function makeDemoCatches() {
  const now = Date.now(), HOUR = 3600 * 1000;
  const samples = [
    { who: "Sipho M.",  fish: "Snoek",      kg: 30, iced: "no",  hoursAgo: 4,  desc: "gutted, cooler box, hot day",          dLat:  0.03, dLng:  0.05 },
    { who: "Anna V.",   fish: "Kob",        kg: 18, iced: "yes", hoursAgo: 10, desc: "bled and gutted, firm",                dLat: -0.06, dLng: -0.02 },
    { who: "Johan P.",  fish: "Harders",    kg: 45, iced: "no",  hoursAgo: 9,  desc: "kept in the shade, warm",              dLat:  0.10, dLng:  0.12 },
    { who: "Thandi N.", fish: "Yellowtail", kg: 22, iced: "yes", hoursAgo: 2,  desc: "ice slurry, just caught offshore",     dLat: -0.12, dLng:  0.15 },
    { who: "Lindiwe Z.",fish: "Crayfish",   kg: 8,  iced: "no",  hoursAgo: 5,  desc: "cooler box, overcast",                 dLat:  0.04, dLng: -0.09 },
    { who: "Nomsa D.",  fish: "Mussel",     kg: 12, iced: "no",  hoursAgo: 1,  desc: "picked this morning",                  dLat: -0.02, dLng:  0.07 },
  ];
  return samples.map((s, i) => {
    runModel1(s.fish, s.kg, s.iced, s.desc);          // real Model 1
    const r2 = runModel2(s.hoursAgo);                 // real Model 2
    return {
      id: -(i + 1), demo: true, seller: s.who, fishType: s.fish, weightKg: s.kg, storedInIce: s.iced === "yes",
      b: r2.b, m: r2.m, caughtAt: now - s.hoursAgo * HOUR,
      lat: userLat + s.dLat, lng: userLng + s.dLng,
    };
  });
}

// ---------- 4. The map ----------
function initMap(elementId) {
  if (typeof L === "undefined") {                     // Leaflet failed to load (offline)
    document.getElementById(elementId).innerHTML = "<p style='padding:16px'>Map unavailable (no internet connection).</p>";
    return null;
  }
  map = L.map(elementId).setView([userLat, userLng], 10);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18, attribution: "© OpenStreetMap contributors",
  }).addTo(map);
  mapLayer = L.layerGroup().addTo(map);
  return map;
}

function recenterMap() {
  if (map) map.setView([userLat, userLng], 10);
}

// Draws "you" plus every catch as a dot: color = freshness, size = weight
function drawCatchesOnMap(allCatches, extraHours = 0) {
  if (!map || !mapLayer) return;
  mapLayer.clearLayers();
  L.circleMarker([userLat, userLng], { radius: 8, color: "#fff", weight: 2, fillColor: "#3498db", fillOpacity: 1 })
    .bindTooltip("You").addTo(mapLayer);

  allCatches.filter(c => c.lat != null).forEach(c => {
    const s = liveStatus(c, extraHours);
    const km = distanceKm(userLat, userLng, c.lat, c.lng);
    const popup = `<b>${esc(c.fishType)}</b> · ${c.weightKg} kg${c.demo ? " (demo)" : ""}<br>
      Seller: ${esc(c.seller || "You")}<br>
      <b style="color:${s.stage.color}">${Math.round(s.score)}/100 · ${s.stage.name}</b><br>
      Caught ${formatHours(s.x)} ago · ${c.storedInIce ? "on ice" : "no ice"}<br>
      ${s.hoursLeft > 0 ? `Food-safe for ${formatHours(s.hoursLeft)}` : "By-product only (compost, fertilizer, bait)"}<br>
      ${km.toFixed(1)} km away`;
    L.circleMarker([c.lat, c.lng], {
      radius: 7 + Math.min(c.weightKg, 50) / 6, color: "#000", weight: 1, fillColor: s.stage.color, fillOpacity: 0.95,
    }).bindPopup(popup).addTo(mapLayer);
  });
}

// ---------- 5. Nearby list (spoiling soonest first) ----------
function nearbyListHtml(allCatches, extraHours = 0) {
  const rows = allCatches.filter(c => c.lat != null).map(c => {
    const s = liveStatus(c, extraHours);
    return { c, s, km: distanceKm(userLat, userLng, c.lat, c.lng) };
  }).sort((a, b) => a.s.hoursLeft - b.s.hoursLeft);
  if (!rows.length) return "<p class='muted'>No catches nearby.</p>";
  return rows.map(({ c, s, km }) => `
    <div class="nearby">
      <span class="dot" style="background:${s.stage.color}"></span>
      <b>${esc(c.fishType)}</b> · ${c.weightKg} kg · ${km.toFixed(1)} km
      <span class="muted"> · ${s.stage.name} · ${s.hoursLeft > 0 ? formatHours(s.hoursLeft) + " left" : "by-product only"}${c.demo ? " · demo" : ""}</span>
    </div>`).join("");
}

if (typeof module !== "undefined") module.exports = { distanceKm, getLocation, DEFAULT_LOCATION };
