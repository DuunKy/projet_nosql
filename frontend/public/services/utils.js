import {chartInstance, constructors, baseURL} from "./variables.js";


export function showLoader(document) {
    document.getElementById("loader").style.display = "block";
    document.getElementById("chartContainer").classList.add("d-none");
    if (chartInstance) chartInstance.destroy();
}

export function hideLoader(document) {
    document.getElementById("loader").style.display = "none";
}

export function getRandomColor() {
    const r = Math.floor(Math.random() * 200);
    const g = Math.floor(Math.random() * 200);
    const b = Math.floor(Math.random() * 200);
    return `rgba(${r}, ${g}, ${b}, 0.8)`;
}

export async function fetchJSON(url) {
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error();
        return await res.json();
    } catch {
        return null;
    }
}