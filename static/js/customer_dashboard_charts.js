var options = {
  series: [2500, 2500, 500],
  chart: {
  width: 450,
  type: 'pie',
},
labels: ['Części', 'Koszty naprawy', 'Inne'],
legend: {
  position: 'right'
},
responsive: [
  {
  breakpoint: 500,
  options: {
    chart: {
      width: 420
    },
    legend: {
      position: 'right'
    }
  },
  breakpoint: 992,
  options: {
    chart: {
      width: 350
    },
    legend: {
      position: 'bottom'
    }
  }
}]
};

var chart = new ApexCharts(document.querySelector("#sumOfCarCosts"), options);
chart.render();