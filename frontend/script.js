const baseURL = "http://127.0.0.1:5000/api/v1/";


document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    link.classList.add('active');
    const endpoint = link.dataset.endpoint;
    loadData(endpoint);
  });
});

function loadData(endpoint) {
  fetch(baseURL + endpoint)
    .then(response => response.json())
    .then(data => {
      let html = `<h2 class="mb-4 text-capitalize">${endpoint}</h2><div class="row">`;

      switch (endpoint) {
        case "drivers":
          html += data.data.map(d => `
            <div class="col-md-6 col-lg-4">
              <div class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">${d.forename} ${d.surname}</h5>
                  <p class="card-text">
                    Nationalité : ${d.nationality}<br>
                    Date de naissance : ${d.dob}<br>
                    Numéro : ${d.number || 'N/A'}<br>
                    Code : ${d.code || 'N/A'}
                  </p>
                  <a href="${d.url}" target="_blank" class="btn btn-primary btn-sm">Wikipedia</a>
                </div>
              </div>
            </div>
          `).join('');
          break;

        case "constructors":
          html += data.data.map(c => `
            <div class="col-md-6 col-lg-4">
              <div class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">${c.name}</h5>
                  <p class="card-text">Nationalité : ${c.nationality}</p>
                </div>
              </div>
            </div>
          `).join('');
          break;

        case "circuits":
          html += data.data.map(c => `
            <div class="col-md-6 col-lg-4">
              <div class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">${c.name}</h5>
                  <p class="card-text">
                    Localisation : ${c.location}, ${c.country}
                  </p>
                </div>
              </div>
            </div>
          `).join('');
          break;

        case "seasons":
          html += data.data.map(s => `
            <div class="col-md-3 col-sm-4 col-6">
              <div class="card text-center shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">Saison ${s.year}</h5>
                </div>
              </div>
            </div>
          `).join('');
          break;
          
        case "results":
        html += data.data.map(r => `
            <div class="col-md-6 col-lg-4">
            <div class="card shadow-sm">
                <div class="card-body">
                <h5 class="card-title">Résultat #${r.resultId}</h5>
                <p class="card-text">
                    Course ID : ${r.raceId}<br>
                    Position : ${r.position}<br>
                    Temps : ${r.time}<br>
                    Tours : ${r.laps}<br>
                    Points : ${r.points}
                </p>
                </div>
            </div>
            </div>
        `).join('');
        break;

        case "races":
        html += data.data.map(race => `
            <div class="col-md-6 col-lg-4">
            <div class="card shadow-sm">
                <div class="card-body">
                <h5 class="card-title">${race.name} (${race.year})</h5>
                <p class="card-text">
                    Date : ${race.date} ${race.time !== "\\N" ? race.time : ""}<br>
                    Manche : ${race.round}<br>
                    <a href="${race.url}" target="_blank" class="btn btn-primary btn-sm">Wikipedia</a>
                </p>
                </div>
            </div>
            </div>
        `).join('');
        break;



        default:
          html += `<p>Aucun rendu défini pour ce type de données.</p>`;
      }

      html += `</div>`;
      document.getElementById("content").innerHTML = html;
    })
    .catch(error => {
      console.error("Erreur lors du chargement :", error);
      document.getElementById("content").innerHTML = `
        <div class="alert alert-danger">Erreur de chargement des données depuis l'API.</div>
      `;
    });
}
