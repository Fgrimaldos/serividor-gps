function cargarMapa() {
  fetch("/data.json")
    .then(res => res.json())
    .then(gpsData => {
      if (!gpsData.length) {
        alert("No hay datos GPS");
        return;
      }

      const map = L.map('map').setView([gpsData[0].lat, gpsData[0].lon], 14);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18
      }).addTo(map);

      const ruta = gpsData.map(p => [p.lat, p.lon]);
      L.polyline(ruta, { color: 'blue' }).addTo(map);

      ruta.forEach((p, i) => {
        const info = gpsData[i];

        if (i === ruta.length - 1) {
          const marker = L.marker(p).addTo(map);
          marker.bindPopup(`
            <b>📍 Última posición:</b><br>
            ${info.timestamp}<br>
            <img src="https://servidor-gps.up.railway.app/ultima.jpg?ts=${Date.now()}" width="200">
          `).openPopup();
        } else {
          L.marker(p).addTo(map).bindPopup(`📍 ${info.timestamp}`);
        }
      });

      map.fitBounds(ruta);
    });
}

function borrarPuntos() {
  if (confirm("¿Estas seguro de que quieres borrar todos los puntos GPS?")) {
    fetch("/borrar", { method: "DELETE" })
      .then(res => res.json())
      .then(res => {
        alert("Puntos eliminados");
        location.reload();
      })
      .catch(err => {
        console.error("Error al borrar:", err);
        alert("No se pudo borrar los puntos.");
      });
  }
}

cargarMapa(); 
setInterval(() => {
  const img = document.getElementById("cam-image");
  if (img) {
    img.src = "https://servidor-gps.up.railway.app/ultima.jpg?ts=" + Date.now();
  }
}, 5000);
