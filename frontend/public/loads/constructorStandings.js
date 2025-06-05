import {showLoader, hideLoader, getRandomColor, fetchJSON} from "../services/utils.js";
import {chartInstance, constructors, baseURL, createChart} from "../services/variables.js";


async function loadConstructorStandings(season) {
    showLoader(document);
    const standingsData = await fetchJSON(`${baseURL}seasons/${season}/constructors/standings`);
    hideLoader(document);

    if (!standingsData || standingsData.length === 0) {
        document.getElementById("performanceData").innerHTML = "<p class='text-warning'>Aucune donnée disponible.</p>";
        return;
    }

    // Supprimer ancien graphique s'il existe
    if (chartInstance) chartInstance.destroy();

    const labels = [];
    const points = [];
    const colors = [];

    standingsData.forEach(item => {
        const name = constructors.find(c => c.constructorId === item.constructorId)?.name || item.constructorId;
        labels.push(name);
        points.push(item.points);
        colors.push(getRandomColor());
    });

    const ctx = document.getElementById("evoChart").getContext("2d");
    createChart( new Chart(ctx, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Points",
                data: points,
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Classement des écuries - Saison ${season}`
                },
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true, title: { display: true, text: "Points" } },
                x: { title: { display: true, text: "Écuries" } }
            }
        }
    }));

    document.getElementById("chartContainer").classList.remove("d-none");
    document.getElementById("performanceData").innerHTML = ""; // Nettoyage du tableau précédent
}

export default loadConstructorStandings;