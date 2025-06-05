import { showLoader, hideLoader, fetchJSON } from "../services/utils.js";
import { baseURL } from "../services/variables.js";

async function loadRetirements(constructorId, season) {
    showLoader(document);
    const data = await fetchJSON(`${baseURL}constructors/${constructorId}/retirements?season=${season}`);
    hideLoader(document);

    const container = document.getElementById("performanceData");
    container.innerHTML = ""; // reset

    if (!data || data.length === 0) {
        container.innerHTML = "<p class='text-warning'>Aucun abandon trouvé.</p>";
        document.getElementById("chartContainer").classList.add("d-none");
        return;
    }

    // Construire le rapport HTML
    let html = `<h3>Rapport des abandons pour l'écurie ${constructorId} - Saison ${season}</h3>`;
    html += `<ul class="list-group">`;

    data.forEach(item => {
        html += `
            <li class="list-group-item">
                <strong>Pilote ${item.driverId}</strong> - <em>${item.retirementCount} abandon(s)</em>
                <br>
                <strong>Raisons :</strong>
                <ul>
                    ${item.reasons.map(reason => `<li>${reason}</li>`).join('')}
                </ul>
            </li>
        `;
    });

    html += `</ul>`;

    container.innerHTML = html;
    document.getElementById("chartContainer").classList.remove("d-none");
}

export default loadRetirements;
