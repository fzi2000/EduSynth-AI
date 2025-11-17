document.getElementById("predictForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    let formData = new FormData(this);
    let data = Object.fromEntries(formData.entries());

    // Send request to Flask backend
    let response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    let result = await response.json();

    document.getElementById("result").innerHTML = `
        <h3>Prediction Result</h3>
        <p><strong>Risk Level:</strong> ${result.risk}</p>
        <p><strong>Probability:</strong> ${result.probability}%</p>
    `;
});
