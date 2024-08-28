frappe.ready(function() {
    // Function to handle the API response and render both table and chart
    function handleApiResponse(response) {
        const data = response.message;

        if (data && data.energy_consumption) {
            const columns = data.energy_consumption.columns;
            const rows = data.energy_consumption.data;
            
            // Generate table
            const tableContainer = document.getElementById("consumption-report");
            let table = "<table class='table table-striped'>";
            table += "<thead><tr>";
            columns.forEach(column => {
                table += `<th style="width:${column.width}px;">${column.label}</th>`;
            });
            table += "</tr></thead>";

            table += "<tbody>";
            rows.forEach(row => {
                table += "<tr>";
                columns.forEach(column => {
                    table += `<td>${row[column.fieldname]}</td>`;
                });
                table += "</tr>";
            });
            table += "</tbody></table>";
            tableContainer.innerHTML = table;

            // Prepare data for the chart
            const labels = rows.map(row => row[columns[0].fieldname]); // Assuming first column as labels
            const consumptionData = rows.map(row => row[columns[2].fieldname]); // Assuming consumption amount is the third column
            
            // Render the chart
            const ctx = document.getElementById('energyChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Energy Consumption',
                        data: consumptionData,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } else {
            document.getElementById("consumption-report").innerText = "No data available.";
        }
    }

    // Call API and process response
    frappe.call({
        method: "renewable_app.API.api.get_consumption_report",
        callback: function(response) {
            handleApiResponse(response);
        },
        error: function(error) {
            console.error("Error fetching consumption report:", error);
            document.getElementById("consumption-report").innerText = "Failed to load data.";
        }
    });
});







