
//success
//Nueva Gráfica representativa del Balance General a largo plazo Grosso Modo
(function () {
  'use strict'

  feather.replace()


  // Graphs
  var ctx = document.getElementById('profit-loss')
  //Variable para reporte diario:
  /*var daily = document.getElementById('cartera_daily')*/
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      datasets: [
        {
          label: 'Intereses/mes',
          data: [{%for data in intereses_h%}{{data[0] | tojson}},{%endfor%}],
          backgroundColor: '#012169'
        },
        /*{
          label: 'Acumulado Cartera',
          data: [{%for data in ap_cartera%}{{data[0] | tojson}},{%endfor%}],
          type: 'line',
          backgroundColor: 'rgb(54, 162, 235)',
        },*/
        {
          label: 'Amortizaciones/mes',
          data: [{%for data in amortizaciones_h%}{{data[0] | tojson}},{%endfor%}],
          backgroundColor: 'rgb(54, 162, 235)',
          borderColor: '#007DC3'
        }
      ],
      labels: [{%for data in fechas_h%}{{data[0] | tojson}},{%endfor%}]

    },
    options: {
      events: ["mousemove", "mouseout", "click", "touchstart", "touchmove", "touchend"],
      responsive: true,
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
          }
        }]
      },
      legend: {
        display: true,
      },
      /*tooltips: {
            callbacks: {
                label: function(tooltipItem, data) {
                    var dataset = data.datasets[tooltipItem.datasetIndex];
                    var index = tooltipItem.index;
                    return dataset.labels[index] + ': ' + dataset.data[index];
                }
            }
        }
*/
    }
  })
})()
