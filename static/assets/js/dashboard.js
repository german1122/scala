/* globals Chart:false, feather:false */


/*

(function () {
  'use strict'

  feather.replace()
  // Flask variables
  var camara = '{{ camara }}';
  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [

        'diciembre',
        'enero',
        'febrero',
        'marzo',
        'abril',
        'mayo',


      ],
      datasets: [{
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          camara,

        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
})()
*/


(function () {
  'use strict'

  feather.replace()
  // flask variables   var x = 

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [

        'diciembre',
        'enero',
        'febrero',
        'marzo',
        'abril',
        'mayo',


      ],
      datasets: [{
        data: [0, 5, 3, 5, 9, 0 ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
})()

/* globals Chart:false, feather:false

(function () {
  'use strict'

  feather.replace()

  // Graphs
  var ctx = document.getElementById('myPie')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: [

        'Credito CPC',
        'Global CPC',
        'Inversión CPC',
        'Arrendamiento CPC',
      ],
      datasets: [{
        data: [
          '{{ creditos_cpc}}',
          '{{ global_cpc }}',
          '{{ inversion_cpc  }}',
          '{{ ap_cpc }}',
        ],
  })
})()

*/
/*
ap_cartera = JSON.parse({{datal | tojson}})
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Arrendamiento', 'Crédito Prendario', 'Crédito Global', 'Inversión'],
        datasets: [{
            label: 'Distribución de Cartera por tipo de Financiamiento',
            data: datal,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 2
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
*/
