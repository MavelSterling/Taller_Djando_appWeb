let chartDeporte;
let chartDia;

document.addEventListener('DOMContentLoaded', () => {
    let ctxDeporte = document.getElementById('chartDeporte').getContext('2d');
    chartDeporte = new Chart(ctxDeporte, {
        type: 'bar',
        data: {},
        options: { /* opciones para el gráfico, si es necesario */ }
    });

    let ctxDia = document.getElementById('chartDia').getContext('2d');
    chartDia = new Chart(ctxDia, {
        type: 'line',
        data: {},
        options: { /* opciones para el gráfico, si es necesario */ }
    });
});

function actualizarGraficos() {
    let inicioFecha = document.getElementById("inicio_fecha").value;
    let finFecha = document.getElementById("fin_fecha").value;

    // Llamada para el reporte por deporte
    fetch(`/reporte-deporte/?inicio_fecha=${inicioFecha}&fin_fecha=${finFecha}`)
        .then(response => response.json())
        .then(data => renderizarGraficoDeporte(data));
    
    // Llamada para el reporte por día
    fetch(`/reporte-dia/?inicio_fecha=${inicioFecha}&fin_fecha=${finFecha}`)
        .then(response => response.json())
        .then(data => renderizarGraficoPorDia(data));
}

function renderizarGraficoDeporte(data) {
    let ctx = document.getElementById('chartDeporte').getContext('2d');

    // Transformar datos para Chart.js
    let labels = Object.keys(data);
    let values = Object.values(data);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Cantidad de préstamos',
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

}

function renderizarGraficoPorDia(data) {
    const ctx = document.getElementById('chartDia').getContext('2d');

    const labels = Object.keys(data);
    const values = Object.values(data);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Préstamos por día',
                data: values,
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

}
