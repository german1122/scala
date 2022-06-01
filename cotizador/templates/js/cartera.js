
//success
//Nueva Gráfica representativa del Balance General a largo plazo Grosso Modo
(function () {
  'use strict'

  feather.replace()

/*[{%for data in ap_cartera%}{{data[0] | tojson}},{%endfor%}]*/
  // Graphs
  var ctx = document.getElementById('cartera')
  //Variable para reporte diario:
  /*var daily = document.getElementById('cartera_daily')*/
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [
        {
          label: 'Colocación',
          data: [{%for data in ap_proyectos%}{{data[0] | tojson}},{%endfor%}],
          type: 'bar',
          backgroundColor: '#012169',
          labels: [{%for data in ap_nombres%}{{data[0] | tojson}},{%endfor%}]
        },
        {
          label: 'Acumulado de Colocación',
          data: [{%for data in ap_cartera%}{{data[0] | tojson}},{%endfor%}],
          type: 'line',
          backgroundColor: 'rgb(54, 162, 235)',
        },
        {
          label: 'Cuentas por Cobrar por Proyecto',
          data: [{%for data in ap_cpcsum%}{{data[0] | tojson}},{%endfor%}],
          type: 'line',
          fill: false,
          backgroundColor: '#4A154B',
          borderColor: '#CE375C'
        }
      ],
      labels: [{%for data in ap_labels%}{{data | tojson}},{%endfor%}]

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



/*
//ATTEMPT TWO
//Nueva Gráfica representativa del Balance General a largo plazo Grosso Modo
(function () {
  'use strict'

  feather.replace()


  // Graphs
  var ctx = document.getElementById('cartera')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [{{labels | tojson}}],
      datasets: [{
        data: [{{cartera | tojson}}],
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
*/



/*
//success
//Nueva Gráfica representativa del Balance General a largo plazo Grosso Modo
(function () {
  'use strict'

  feather.replace()


  // Graphs
  var ctx = document.getElementById('cartera')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [{%for data in ap_labels%}{{data | tojson}},{%endfor%}],
      datasets: [{
        data: [{%for data in ap_cartera%}{{data[0] | tojson}},{%endfor%}],

        /*data: [{{cartera | tojson}}],*/
        /*lineTension: 0,
        backgroundColor: [
      '#012169'

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


//ATTEMPT ONE

//Nueva Gráfica representativa del Balance General a largo plazo Grosso Modo
(function () {
  'use strict'

  feather.replace()


  // Graphs
  var ctx = document.getElementById('cartera')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
                  {% for item in ap_labels %}
                      {montos: '{{ item | tojson }}'},
                  {% endfor %}
              ],
      datasets: [{
        data: [
                    {% for item in ap_cartera %}
                        {montos: '{{ item | tojson }}'},
                    {% endfor %}
                ],
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
*/
