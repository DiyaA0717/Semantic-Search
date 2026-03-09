async function search(){

const query = document.getElementById("query").value;

const res = await fetch("/search",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({query})
});

const data = await res.text();

document.getElementById("results").innerHTML =
"<b>Results:</b><br>"+data;

}
