let LastOrdersProfitDateAndTime = []
let LastOrdersProfitValues = []
let lastMonthsProfitMonths = []
let lastMonthsProfitValues = []

lastOrdersProfitData.forEach(element => {
  LastOrdersProfitDateAndTime.push([element[0], element[1]])
  LastOrdersProfitValues.push(element[2])
});

for (let key in lastMonthsProfitData) {
  lastMonthsProfitMonths.push(lastMonthsProfitData[key][0])
  lastMonthsProfitValues.push(lastMonthsProfitData[key][1])
}

let lastOrdersProfit = {
  series: [{
  data: LastOrdersProfitValues,
  name: "Zysk",
}],
  chart: {
  height: 350,
  type: 'bar',
  fontFamily: 'Roboto, sans-serif',
  events: {
    click: function(chart, w, e) {
      // console.log(chart, w, e)
    }
  },
},
plotOptions: {
  bar: {
    columnWidth: '45%',
    distributed: true,
  }
},
dataLabels: {
  enabled: false
},
legend: {
  show: false
},
title: {
  text: "Zysk z ostatnich zleceń",
  align: "center",
  style: {
    fontSize:  '20px',
  }
},
xaxis: {
  categories: LastOrdersProfitDateAndTime,
  labels: {
    style: {
      fontSize: '12px'
    }
  }
}
};

var chart = new ApexCharts(document.querySelector("#lastOrdersProfit"), lastOrdersProfit);
chart.render();


let lastMonthsProfit = {
  series: [{
  data: lastMonthsProfitValues,
  name: "Zysk",
}],
  chart: {
  type: 'bar',
  height: 350,
  fontFamily: 'Roboto, sans-serif',
},
plotOptions: {
  bar: {
    borderRadius: 4,
    horizontal: true,
  }
},
dataLabels: {
  enabled: false
},
xaxis: {
  categories: lastMonthsProfitMonths,
},
title: {
  text: "Zysk z ostatnich miesięcy",
  align: "center",
  style: {
    fontSize:  '20px',
  }
},
};

var chart = new ApexCharts(document.querySelector("#lastMonthsProfit"), lastMonthsProfit);
chart.render();