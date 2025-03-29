document.getElementById("calcForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const a = document.getElementById("a").value;
  const b = document.getElementById("b").value;
  const operation = document.getElementById("operation").value;

  const response = await fetch("/api/calc", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ a, b, operation })
  });

  const data = await response.json();
  document.getElementById("resultValue").textContent = data.result;
  document.getElementById("resultContainer").style.display = "block";
});
