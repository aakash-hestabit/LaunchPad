import qs from "querystring";

const largeData = { text: "A".repeat(17000) }; // 17kb > 16kb

fetch("http://localhost:3001/", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: qs.stringify(largeData),
})
  .then((res) =>
    res.text().then((text) => console.log(res.status, res.statusText, text))
  )
  .catch((err) => console.error(err));
