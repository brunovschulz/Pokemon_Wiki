function initializeChart(atributos, chartElementId) {

    //console.log(atributos)

    const atr = atributos.slice(0, -1);

    const labels = atr.map(attr => attr[0]);
    const dataValues = atr.map(attr => attr[1]);

    const colors = dataValues.map(value => {
        if (value > 90) return 'green';
        if (value >= 60) return 'yellow';
        return 'red';
    });

    const ctx = document.getElementById(chartElementId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Atributos de Combate',
                data: dataValues,
                backgroundColor: colors,
                borderColor: 'black',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: true }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 160
                }
            }
        }
    });
}
