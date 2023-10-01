// Variables globales para las instancias de los gráficos
let chartDeporte;
let chartDia;

// Se crea una vez al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    let ctxDeporte = document.getElementById('chartDeporte').getContext('2d');
    chartDeporte = new Chart(ctxDeporte, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Cantidad de préstamos',
                data: [],
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

    let ctxDia = document.getElementById('chartDia').getContext('2d');
    chartDia = new Chart(ctxDia, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Préstamos por día',
                data: [],
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
    // Transformar datos para Chart.js
    let labels = Object.keys(data);
    let values = Object.values(data);

    // Actualizar la instancia del gráfico con los nuevos datos
    chartDeporte.data.labels = labels;
    chartDeporte.data.datasets[0].data = values;
    chartDeporte.update();
}

function renderizarGraficoPorDia(data) {
    const labels = Object.keys(data);
    const values = Object.values(data);

    // Actualizar la instancia del gráfico con los nuevos datos
    chartDia.data.labels = labels;
    chartDia.data.datasets[0].data = values;
    chartDia.update();
}
