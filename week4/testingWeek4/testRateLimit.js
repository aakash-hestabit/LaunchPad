const total_rqsts = 12;

for (let i = 1; i <= total_rqsts; i++) {
  try {
    const res = await fetch("http://localhost:3001/");

    const text = await res.text();

    console.log(`Request #${i}: status = ${res.status}, body = ${text}`);
  } catch (err) {
    console.log(`Request #${i}: ERROR`, err);
  }
}