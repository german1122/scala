
(function () {
  'use strict'

  feather.replace()


  // Graphs
  var ctx = document.getElementById('myChart2')
  //Variable para reporte 
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["Arrendamiento Puro", "Crédito Global", 'Crédito Prendario', 'Pasivos'],
      datasets: [{
        data: ["{{ap_cartera[0] | tojson}}", "{{global_cartera[0] | tojson}}", "{{credito_cartera[0] | tojson}}" ,"{{inversion_cartera[0] | tojson}}" ],
        lineTension: 0,
        backgroundColor: [
      '#012169',
      'rgb(54, 162, 235)',
      '#169BD7'
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
        display: false
      }
    }
  })
})()
