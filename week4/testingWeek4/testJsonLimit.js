const largeData = { text: "A".repeat(11000) }; // sending payload of 11kb when limit is 10kb

fetch('http://localhost:3001/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(largeData)
})
.then(res => console.log(res.status, res.statusText, res.text()))
.catch(err => console.error(err));
