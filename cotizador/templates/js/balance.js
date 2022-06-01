//Nueva Gráfica representativa del Balance General a largo plazo Grosso Modo
(function () {
  'use strict'

  feather.replace()


  // Graphs
  var ctx = document.getElementById('balance')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ["Arrendamiento Puro", "Crédito Global", 'Crédito Prendario', 'Pasivos'],
      datasets: [{
        label: 'Cuentas por Cobrar/pagar (largo plazo)',
        data: ["{{Ap_cpc[0] | tojson}}", "{{Global_cpc[0] | tojson}}", "{{Creditos_cpc[0] | tojson}}" ,"{{Inversion_cpp[0] | tojson}}" ],
        lineTension: 0,
        backgroundColor: [
      '#012169',

    ],
        borderColor: '#007bff',
        borderWidth: 0,
        pointBackgroundColor: '#007bff'
      },{
        type: 'bar',
        fill: true,
        label: 'Valor de Cartera',
        data: ["{{ap_cartera[0] | tojson}}", "{{global_cartera[0] | tojson}}", "{{credito_cartera[0] | tojson}}" ,"{{inversion_cartera[0] | tojson}}" ],
        lineTension: 0,
        backgroundColor: [
      '#169BD7', '#169BD7', '#169BD7', '#169BD7'
    ],
        borderColor: '#007bff',
        borderWidth: 0,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
          }
        }]
      },
      legend: {
        display: true
      }
    }
  })
})()
