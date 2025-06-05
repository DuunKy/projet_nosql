export let chartInstance = null;
export function createChart(chart) {
    chartInstance = chart
}

export let constructors = [];

export function setConstructors(data) {
    constructors.length = 0;
    constructors.push(...data);
}


export const baseURL = "http://127.0.0.1:5000/api/v1/";