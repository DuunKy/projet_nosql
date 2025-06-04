const BASE_URL = 'http://127.0.0.1:5000/api/v1';

async function getDrivers() {
  const res = await fetch(`${BASE_URL}/drivers`);
  const data = await res.json();
  return data;
}
