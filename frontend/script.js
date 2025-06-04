// Base de l'URL de l'API
const baseURL = "http://127.0.0.1:5000/api/v1/";

// Cache simple en mémoire pour éviter les requêtes redondantes
const cache = {};

async function fetchWithCache(url) {
  if (cache[url]) return cache[url];
  const response = await fetch(url);
  const data = await response.json();
  cache[url] = data;
  return data;
}

// Gère l'affichage dynamique à partir du menu
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    link.classList.add('active');
    const endpoint = link.dataset.endpoint;
    loadData(endpoint);
  });
});

function loadData(endpoint) {
  fetchWithCache(baseURL + endpoint)
    .then(async data => {
      let html = `<h2 class="mb-4 text-capitalize">${endpoint}</h2><div class="row">`;

      const renderCard = (content) => `
        <div class="col-md-6 col-lg-4">
          <div class="card shadow-sm">
            <div class="card-body">
              ${content}
            </div>
          </div>
        </div>
      `;

      switch (endpoint) {
        case "drivers":
          html += data.data.map(d => renderCard(`
            <h5 class="card-title">${d.forename} ${d.surname}</h5>
            <p class="card-text">
              Nationalité : ${d.nationality}<br>
              Date de naissance : ${d.dob}<br>
              Numéro : ${d.number || 'N/A'}<br>
              Code : ${d.code || 'N/A'}
            </p>
            <a href="${d.url}" target="_blank" class="btn btn-primary btn-sm">Wikipedia</a>
          `)).join('');
          break;

        case "constructors":
          html += data.data.map(c => renderCard(`
            <h5 class="card-title">${c.name}</h5>
            <p class="card-text">Nationalité : ${c.nationality}</p>
          `)).join('');
          break;

        case "circuits":
          html += data.data.map(c => renderCard(`
            <h5 class="card-title">${c.name}</h5>
            <p class="card-text">
              Localisation : ${c.location}, ${c.country}
            </p>
          `)).join('');
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
          html += data.data.map(r => renderCard(`
            <h5 class="card-title">Résultat #${r.resultId}</h5>
            <p class="card-text">
              Course ID : ${r.raceId}<br>
              Position : ${r.position}<br>
              Temps : ${r.time}<br>
              Tours : ${r.laps}<br>
              Points : ${r.points}
            </p>
          `)).join('');
          break;

        case "races":
          html += data.data.map(race => renderCard(`
            <h5 class="card-title">${race.name} (${race.year})</h5>
            <p class="card-text">
              Date : ${race.date} ${race.time !== "\\N" ? race.time : ""}<br>
              Manche : ${race.round}<br>
              <a href="${race.url}" target="_blank" class="btn btn-primary btn-sm">Wikipedia</a>
            </p>
          `)).join('');
          break;

        case "qualifying":
          const enrichedCards = await Promise.all(data.data.map(async q => {
            try {
              const [driverRes, constructorRes, raceRes] = await Promise.all([
                fetchWithCache(`${baseURL}drivers?id=${q.driverId}`),
                fetchWithCache(`${baseURL}constructors?id=${q.constructorId}`),
                fetchWithCache(`${baseURL}races?id=${q.raceId}`)
              ]);

              const driver = driverRes.data[0];
              const constructor = constructorRes.data[0];
              const race = raceRes.data[0];

              return renderCard(`
                <h5 class="card-title">
                  ${driver.forename} ${driver.surname} – ${constructor.name}
                </h5>
                <p class="card-text">
                  Course : ${race.name} (${race.year})<br>
                  Numéro : ${q.number}<br>
                  Position : ${q.position}<br>
                  Q1 : ${q.q1 || 'N/A'}<br>
                  Q2 : ${q.q2 || 'N/A'}<br>
                  Q3 : ${q.q3 || 'N/A'}
                </p>
              `);
            } catch (err) {
              console.error("Erreur d'enrichissement :", err);
              return renderCard(`<p class='text-danger'>Erreur de chargement des données pour une qualification.</p>`);
            }
          }));

          html += enrichedCards.join('');
          html += `</div>`;
          document.getElementById("content").innerHTML = html;
          return;

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
