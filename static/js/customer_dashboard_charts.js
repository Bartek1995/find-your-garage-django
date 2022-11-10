carData.forEach(element => {
  const options = {
    series: [element.cost_of_parts, element.cost_of_repairs, element.cost_of_anothers],
    chart: {
    width: 350,
    type: 'pie',
  },
  labels: ['Części', 'Koszty naprawy', 'Inne'],
  legend: {
    position: 'bottom'
  },
  };
  const chart = new ApexCharts(document.querySelector("#sumOfCarCosts-" + element.id), options);
  chart.render();
});