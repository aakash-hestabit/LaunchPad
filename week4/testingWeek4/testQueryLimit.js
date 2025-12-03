import qs from 'querystring';

const largeData = { text: "A".repeat(15000) }; // 17kb > 16kb

fetch('http://localhost:3000/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: qs.stringify(largeData)
})
.then(res => {console.log(res.status, res.statusText, text)})
.catch(err => console.error(err));
