
//success
//Nueva Gráfica representativa del Balance General a largo plazo Grosso Modo
(function () {
  'use strict'

  feather.replace()


  // Graphs
  var ctx = document.getElementById('cartera-anual')
  //Variable para reporte diario:
  /*var daily = document.getElementById('cartera_daily')*/
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [
        {
          label: 'Valor de Cartera',
          data: [{%for data in ap_liquid%}{{data[0] | tojson}},{%endfor%}],
          type: 'bar',
          fill: false,
          backgroundColor: '#012169',
          labels: [{%for data in ap_liquidf%}{{data[0] | tojson}},{%endfor%}]
        },
        /*{
          label: 'Acumulado Cartera',
          data: [{%for data in ap_cartera%}{{data[0] | tojson}},{%endfor%}],
          type: 'line',
          backgroundColor: 'rgb(54, 162, 235)',
        },*/
        {
          label: 'Cuentas por Cobrar por Proyecto',
          data: [{%for data in ap_liquidc%}{{data[0] | tojson}},{%endfor%}],
          type: 'line',
          fill: true,
          backgroundColor: 'rgb(54, 162, 235)',
          borderColor: '#007DC3'
        }
      ],
      labels: [{%for data in ap_liquidn%}{{data[0] | tojson}},{%endfor%}]

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
