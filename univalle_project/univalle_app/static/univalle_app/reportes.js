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
    const inicioFecha = document.getElementById('inicio_fecha').value;
    const finFecha = document.getElementById('fin_fecha').value;

    fetch(`/reporte-deporte/?inicio_fecha=${inicioFecha}&fin_fecha=${finFecha}`)
        .then(response => response.json())
        .then(data => {
            chartDeporte.data = {
                labels: Object.keys(data),
                datasets: [{
                    label: 'Artículos Prestados',
                    data: Object.values(data),
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            };
            chartDeporte.update();
        });

    fetch(`/reporte-dia/?inicio_fecha=${inicioFecha}&fin_fecha=${finFecha}`)
        .then(response => response.json())
        .then(data => {
            chartDia.data = {
                labels: Object.keys(data),
                datasets: [{
                    label: 'Artículos Prestados por Día',
                    data: Object.values(data),
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            };
            chartDia.update();
        });
}
