import {showLoader, hideLoader, getRandomColor, fetchJSON} from "../services/utils.js";
import {chartInstance, constructors, baseURL, createChart} from "../services/variables.js";


async function loadLapTimesChart(constructorId, circuitId, driverId, season) {
    showLoader(document);
    const url = `${baseURL}constructors/${constructorId}/${circuitId}/lap-times?season=${season}&driver=${driverId}`;
    const data = await fetchJSON(url);
    hideLoader(document);

    if (!data || data.length === 0) {
        document.getElementById("performanceData").innerHTML = "<p class='text-warning'>Aucune donnée disponible.</p>";
        return;
    }

    const ctx = document.getElementById("evoChart").getContext("2d");
    const labels = data.map(lap => `Tour ${lap.lap}`);
    const times = data.map(lap => lap.milliseconds / 1000); // Convert to seconds

    if (chartInstance) chartInstance.destroy();

    createChart( new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [{
                label: "Temps au tour (s)",
                data: times,
                borderColor: "rgba(255,99,132,1)",
                backgroundColor: "rgba(255,99,132,0.2)",
                fill: false,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Temps au tour - ${season}`
                }
            },
            scales: {
                y: { beginAtZero: false, title: { display: true, text: "Temps (s)" } },
                x: { title: { display: true, text: "Tour" } }
            }
        }
    }));

    document.getElementById("chartContainer").classList.remove("d-none");
}

export default loadLapTimesChart;