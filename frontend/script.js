async function analyzeRoute(){

    const response = await fetch(
        "http://127.0.0.1:8000/api/routes/analyze",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                origin:
                    document.getElementById("origin").value,

                destination:
                    document.getElementById("destination").value,

                cargo_type:
                    document.getElementById("cargo").value,

                containers:
                    parseInt(
                        document.getElementById("containers").value
                    )
            })
        }
    );

    const data = await response.json();

    document.getElementById("result").innerHTML = `
        <div class="result-card">
            <h2>Recommended Route</h2>

            <p><b>Route:</b> ${data.recommended_route}</p>
            <p><b>Transit Days:</b> ${data.transit_time_days}</p>
            <p><b>Distance:</b> ${data.distance_nm} NM</p>
            <p><b>Transshipments:</b> ${data.transshipments}</p>
            <p><b>Freight:</b> $${data.base_freight_usd}</p>
            <p><b>Reason:</b> ${data.reason}</p>
        </div>
    `;
}
function generateManualQuotation() {

    const customer =
        document.getElementById("customerName").value;

    const origin =
        document.getElementById("manualOrigin").value;

    const destination =
        document.getElementById("manualDestination").value;

    const cargo =
        document.getElementById("manualCargo").value;

    const containers =
        parseInt(
            document.getElementById("manualContainers").value
        );

    const rate =
        parseFloat(
            document.getElementById("ratePerContainer").value
        );

    const additional =
        parseFloat(
            document.getElementById("additionalCharges").value
        ) || 0;

    const freightCost = containers * rate;

    const totalCost =
        freightCost + additional;

    document.getElementById(
        "manualQuotationResult"
    ).innerHTML = `

        <div class="quotation-card">

            <h3>Manual Quotation</h3>

            <p><b>Customer:</b> ${customer}</p>

            <p><b>Origin:</b> ${origin}</p>

            <p><b>Destination:</b> ${destination}</p>

            <p><b>Cargo:</b> ${cargo}</p>

            <p><b>Containers:</b> ${containers}</p>

            <p><b>Rate/Container:</b> $${rate}</p>

            <p><b>Additional Charges:</b> $${additional}</p>

            <hr>

            <h2>Total Freight Cost: $${totalCost}</h2>

        </div>

    `;
}