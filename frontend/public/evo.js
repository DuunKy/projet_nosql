import loadPerformanceChart from "./loads/performance.js";
import loadConstructorStandings from "./loads/constructorStandings.js";
import loadTopDriversForConstructor from "./loads/topDriver.js";
import loadChartForSeason from "./loads/seasons.js";
import loadLapTimesChart from "./loads/lapTime.js";
import loadRetirements from "./loads/Retirements.js";
import {fetchJSON} from "./services/utils.js";
import {chartInstance, constructors, baseURL, setConstructors} from "./services/variables.js";


// Initialisation du sélecteur de requêtes ---------------------------------------------------------------------------- QuerySelector
function initQuerySelector() {
    const querySelect = document.getElementById("querySelect");
    const queries = {
        "performance": "Évolution performance d'une écurie",
        "standings": "Classement final des écuries",
        "standing-evolution": "Évolution du classement",
        "top-drivers": "Pilotes les plus performants",
        "lap-times-circuit": "Temps au tour par pilote sur un circuit",
        "retirements": "Abandons d'une écurie"
    };

    for (const [key, label] of Object.entries(queries)) {
        const option = document.createElement("option");
        option.value = key;
        option.textContent = label;
        querySelect.appendChild(option);
    }
}

async function initConstructors() {
    if (constructors.length === 0) {
        const data = await fetchJSON(baseURL + "constructors");
        if (data) setConstructors(data.data)
    }
}

// Initialisation des sélecteurs de paramètres ------------------------------------------------------------------------- BuildSelectors
async function buildSelectors(query) {
    await initConstructors();

    const container = document.getElementById("paramSelectors");
    container.innerHTML = "";

    // Saison
    if (["performance", "standing-evolution", "standings", "standings", "lap-times-circuit", "retirements"].includes(query)) {
        const seasonSelect = document.createElement("select");
        seasonSelect.id = "seasonSelect";
        seasonSelect.className = "form-select d-inline-block w-auto me-2";
        seasonSelect.innerHTML = `<option selected disabled>-- Saison --</option>`;
        const seasons = await fetchJSON(baseURL + "seasons");
        if (seasons?.data) {
            seasons.data.sort((a, b) => b.year - a.year).forEach(s => {
                const opt = document.createElement("option");
                opt.value = s.year;
                opt.textContent = s.year;
                seasonSelect.appendChild(opt);
            });
        }
        container.appendChild(seasonSelect);
        seasonSelect.addEventListener("change", onParamsChange);
    }

    // Écurie
    if (["performance", "top-drivers", "standings", "lap-times-circuit", "retirements"].includes(query)) {
        const constSelect = document.createElement("select");
        constSelect.id = "constructorSelect";
        constSelect.className = "form-select d-inline-block w-auto";
        constSelect.innerHTML = `<option selected disabled>-- Écurie --</option>`;
        constructors.forEach(c => {
            const opt = document.createElement("option");
            opt.value = c.constructorId;
            opt.textContent = c.name;
            constSelect.appendChild(opt);
        });
        container.appendChild(constSelect);
        constSelect.addEventListener("change", onParamsChange);
    }

    if (query === "lap-times-circuit") {
        // Circuit
        const circuitSelect = document.createElement("select");
        circuitSelect.id = "circuitSelect";
        circuitSelect.className = "form-select d-inline-block w-auto me-2";
        circuitSelect.innerHTML = `<option selected disabled>-- Circuit --</option>`;
        const circuits = await fetchJSON(baseURL + "circuits");
        if (circuits?.data) {
            circuits.data.forEach(c => {
                const opt = document.createElement("option");
                opt.value = c.circuitId;
                opt.textContent = c.name;
                circuitSelect.appendChild(opt);
            });
        }
        container.appendChild(circuitSelect);
        circuitSelect.addEventListener("change", onParamsChange);

        // Pilote
        const driverSelect = document.createElement("select");
        driverSelect.id = "driverSelect";
        driverSelect.className = "form-select d-inline-block w-auto me-2";
        driverSelect.innerHTML = `<option selected disabled>-- Pilote --</option>`;
        const drivers = await fetchJSON(baseURL + "drivers");
        if (drivers?.data) {
            drivers.data.forEach(d => {
                const opt = document.createElement("option");
                opt.value = d.driverId;
                opt.textContent = `${d.forename} ${d.surname}`;
                driverSelect.appendChild(opt);
            });
        }
        container.appendChild(driverSelect);
        driverSelect.addEventListener("change", onParamsChange);

        async function updateDriversForConstructor() {
            const constructorId = document.getElementById("constructorSelect")?.value;
            const season = document.getElementById("seasonSelect")?.value;
            const driverSelect = document.getElementById("driverSelect");

            if (!constructorId || !season) return;

            // Réinitialise
            driverSelect.innerHTML = `<option selected disabled>-- Pilote --</option>`;

            const res = await fetchJSON(`${baseURL}constructors/${constructorId}/drivers?season=${season}`);
            if (res?.data) {
                res.data.forEach(driver => {
                    const opt = document.createElement("option");
                    opt.value = driver.driverId;
                    opt.textContent = `${driver.forename} ${driver.surname}`;
                    driverSelect.appendChild(opt);
                });
            }
        }

    }
}

// Gestion des changements de requête et de paramètres ---------------------------------------------------------------- OnQueryChange & OnParamsChange
function onQueryChange() {
    const query = document.getElementById("querySelect").value;
    buildSelectors(query);
}

function onParamsChange() {
    const query = document.getElementById("querySelect").value;
    const season = document.getElementById("seasonSelect")?.value;
    const constructorId = document.getElementById("constructorSelect")?.value;

    document.getElementById("performanceData").innerHTML = "";

    switch (query) {
        case "performance":
            if (season && constructorId) loadPerformanceChart(constructorId, season);
            break;
        case "standings":
            if (season) loadConstructorStandings(season);
            break;
        case "standing-evolution":
            if (season) loadChartForSeason(season);
            break;
        case "top-drivers":
            if (constructorId) loadTopDriversForConstructor(constructorId);
            break;
        case "lap-times-circuit":
            const driverId = document.getElementById("driverSelect")?.value;
            const circuitId = document.getElementById("circuitSelect")?.value;
            if (season && constructorId && driverId && circuitId) {
                loadLapTimesChart(constructorId, circuitId, driverId, season);
            }
            break;
        case "retirements":
            if (season && constructorId) loadRetirements(constructorId, season);
            break;
    }
}

// Chargement initial des sélecteurs et du graphique par défaut -------------------------------------------------------- LOADS


initQuerySelector();
document.getElementById('querySelect').addEventListener('change', onQueryChange);
