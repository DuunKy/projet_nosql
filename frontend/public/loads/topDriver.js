import {showLoader, hideLoader, getRandomColor, fetchJSON} from "../services/utils.js";
import {chartInstance, constructors, baseURL, createChart} from "../services/variables.js";

async function loadTopDriversForConstructor(constructorId) {
    showLoader(document);
    const data = await fetchJSON(`${baseURL}constructors/${constructorId}/top-drivers`);
    hideLoader(document);

    if (!data || data.length === 0) {
        document.getElementById("performanceData").innerHTML = "<p class='text-warning'>Aucun pilote trouvé.</p>";
        return;
    }

    const ctx = document.getElementById("evoChart").getContext("2d");
    createChart( new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.map(p => p.driverName || "Inconnu"),
            datasets: [{
                label: "Points",
                data: data.map(p => p.totalPoints),
                backgroundColor: data.map(() => getRandomColor())
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Top pilotes de ${constructorId}`
                },
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true, title: { display: true, text: "Points" } },
                x: { title: { display: true, text: "Pilotes" } }
            }
        }
    }));

    document.getElementById("chartContainer").classList.remove("d-none");
}

export default loadTopDriversForConstructor;