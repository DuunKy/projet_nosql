import {showLoader, hideLoader, getRandomColor, fetchJSON} from "../services/utils.js";
import {chartInstance, constructors, baseURL, createChart} from "../services/variables.js";

async function loadChartForSeason(season) {
    showLoader(document);
    const datasets = [];
    let labels = [];

    for (const c of constructors) {
        const evoData = await fetchJSON(`${baseURL}constructors/${c.constructorId}/standing-evolution?season=${season}`);
        if (!evoData?.evolution) continue;
        if (labels.length === 0) labels = evoData.evolution.map(e => "M" + e.round);

        datasets.push({
            label: c.name,
            data: evoData.evolution.map(e => e.position),
            borderColor: getRandomColor(),
            fill: false,
            tension: 0.3
        });
    }

    hideLoader(document);
    if (chartInstance) chartInstance.destroy();
    if (datasets.length === 0) return;

    const ctx = document.getElementById("evoChart").getContext("2d");
    createChart( new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Classement des écuries - ${season}`,
                    font: { size: 16 }
                },
                legend: {
                    position: 'bottom',
                    labels: { font: { size: 10 }, boxWidth: 12 }
                }
            },
            scales: {
                y: { reverse: true, ticks: { stepSize: 1 }, title: { display: true, text: 'Position' } },
                x: { title: { display: true, text: 'Manche' } }
            }
        }
    }));

    document.getElementById("chartContainer").classList.remove("d-none");
}

export default loadChartForSeason;