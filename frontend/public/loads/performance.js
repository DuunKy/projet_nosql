import {showLoader, hideLoader, getRandomColor, fetchJSON} from "../services/utils.js";
import {chartInstance, constructors, baseURL, createChart} from "../services/variables.js";

async function loadPerformanceChart(teamId, season) {
    showLoader(document);
    const data = await fetchJSON(`${baseURL}teams/${teamId}/performance?season=${season}`);
    hideLoader(document);

    if (!data || data.error) {
        document.getElementById("performanceData").innerHTML = `<p class="text-danger">${data?.error || "Erreur lors du chargement"}</p>`;
        return;
    }

    const labels = data.map(item => item.raceName);
    const points = data.map(item => item.points);

    const ctx = document.getElementById("evoChart").getContext("2d");
    createChart( new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Points par course",
                data: points,
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Performance ${teamId} - ${season}`
                }
            },
            scales: {
                y: { beginAtZero: true, title: { display: true, text: "Points" } },
                x: { title: { display: true, text: "Course" } }
            }
        }
    }));

    document.getElementById("chartContainer").classList.remove("d-none");
}

export default loadPerformanceChart;