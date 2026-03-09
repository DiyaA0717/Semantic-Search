async function search() {

const query = document.getElementById("query").value;

const res = await fetch("http://localhost:5000/search", {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify({ query: query })
});

const data = await res.json();

document.getElementById("results").innerHTML =
"<b>Results:</b><br><pre>" + JSON.stringify(data, null, 2) + "</pre>";

}
