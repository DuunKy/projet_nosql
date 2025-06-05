const baseURL = "http://127.0.0.1:5000/api/v1/";
const cache = {};

const showSpinner = () => {
  const spinner = document.getElementById("spinner");
  if (spinner) spinner.style.display = "block";
};

const hideSpinner = () => {
  const spinner = document.getElementById("spinner");
  if (spinner) spinner.style.display = "none";
};


async function fetchWithCache(url) {
  if (cache[url]) return cache[url];
  const response = await fetch(url);
  const data = await response.json();
  cache[url] = data;
  return data;
}

document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    link.classList.add('active');
    const endpoint = link.dataset.endpoint;
    if (endpoint) loadData(endpoint);
  });
});

async function loadData(endpoint) {
  showSpinner();
  try {
    const data = await fetchWithCache(baseURL + endpoint);
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

      case "qualifying": {
        try {
          const qualifyingData = data.data;

          // Extraire les ID uniques
          const uniqueDriverIds = [...new Set(qualifyingData.map(q => q.driverId))];
          const uniqueConstructorIds = [...new Set(qualifyingData.map(q => q.constructorId))];
          const uniqueRaceIds = [...new Set(qualifyingData.map(q => q.raceId))];

          // Charger toutes les ressources en parallèle
          const [driversResponses, constructorsResponses, racesResponses] = await Promise.all([
            Promise.all(uniqueDriverIds.map(id => fetchWithCache(`${baseURL}drivers?id=${id}`))),
            Promise.all(uniqueConstructorIds.map(id => fetchWithCache(`${baseURL}constructors?id=${id}`))),
            Promise.all(uniqueRaceIds.map(id => fetchWithCache(`${baseURL}races?id=${id}`)))
          ]);

          // Indexer les données pour accès rapide
          const driverMap = Object.fromEntries(driversResponses.map(r => [r.data[0]?.driverId, r.data[0]]));
          const constructorMap = Object.fromEntries(constructorsResponses.map(r => [r.data[0]?.constructorId, r.data[0]]));
          const raceMap = Object.fromEntries(racesResponses.map(r => [r.data[0]?.raceId, r.data[0]]));

          // Créer les cartes
          const cards = qualifyingData.map(q => {
            const driver = driverMap[q.driverId];
            const constructor = constructorMap[q.constructorId];
            const race = raceMap[q.raceId];

            if (!driver || !constructor || !race) {
              return renderCard(`<p class="text-danger">Erreur d'enrichissement des données (ID manquant).</p>`);
            }

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
          });

          html += cards.join('');
          html += `</div>`;
          document.getElementById("content").innerHTML = html;
        } catch (err) {
          console.error("Erreur lors du chargement des données de qualification :", err);
          document.getElementById("content").innerHTML = `
      <div class="alert alert-danger">Erreur lors du chargement des qualifications.</div>
    `;
        } finally {
          showSpinner(false);
        }
        return;
      }


      default:
        html += `<p>Aucun rendu défini pour ce type de données.</p>`;
    }

    html += `</div>`;
    document.getElementById("content").innerHTML = html;
  } catch (error) {
    console.error("Erreur lors du chargement :", error);
    document.getElementById("content").innerHTML = `
          <div class="alert alert-danger">Erreur de chargement des données depuis l'API.</div>
        `;
  } finally {
    hideSpinner();
  }
}