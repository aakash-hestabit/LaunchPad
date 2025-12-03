const largeData = { text: "A".repeat(11000) }; // 11kb > 10kb limit

fetch('http://localhost:3000/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(largeData)
})
.then(res => console.log(res.status, res.statusText, res.text()))
.catch(err => console.error(err));
