var lastDaysProfit = {
  series: [
    {
      name: "Zysk",
      type: "column",
      data: [1300, 700, 350, 1400, 225, 775, 650],
    },
    {
      name: "Ilość wykonanych zleceń",
      type: "line",
      data: [1, 2, 3, 1, 4, 6, 4],
    },
  ],
  chart: {
    height: 350,
    type: "line",
    dropShadow: {
      enabled: true,
      color: '#000',
      top: 18,
      left: 7,
      blur: 5,
      opacity: 0.2
    },
    fontFamily: 'Roboto, sans-serif',
    toolbar: {
      show: false,
    },
  },
  colors: ["#77B6EA", "#458606"],
  dataLabels: {
    enabled: true,
  },
  stroke: {
    curve: "smooth",
  },
  title: {
    text: "Analiza ostatnich zleceń",
    align: "center",
    style: {
      fontSize:  '20px',
    }
  },
  xaxis: {
    labels: {
      show: true,
      rotate: -45,
      rotateAlways: true,
    },
    categories: [
      "26.08.22",
      "27.08.22",
      "28.08.22",
      "29.09.22",
      "30.08.22",
      "31.08.22",
      "01.09.22",
    ],
  },
  yaxis: [
    {
      axisTicks: {
        show: true,
      },
      axisBorder: {
        show: true,
        color: "#008FFB",
      },
      labels: {
        style: {
          colors: "#008FFB",
        },
      },
      title: {
        text: "Zyski",
        style: {
          color: "#008FFB",
          fontSize:  '16px',
        },
      },
      tooltip: {
        enabled: true,
      },
    },
    {
      seriesName: "Income",
      opposite: true,
      axisTicks: {
        show: true,
      },
      axisBorder: {
        show: true,
        color: "#458606",
      },
      labels: {
        style: {
          colors: "#545454",
        },
      },
      title: {
        text: "Ilość zleceń",
        style: {
          color: "#458606",
          fontSize:  '16px',
        },
      },
    },
  ],
  tooltip: {
    fixed: {
      enabled: true,
      position: "topLeft", // topRight, topLeft, bottomRight, bottomLeft
      offsetY: 30,
      offsetX: 60,
    },
  },
  legend: {
    horizontalAlign: "left",
    offsetX: 40,
    onItemClick: {
      toggleDataSeries: false
    },
  },
};

var chart = new ApexCharts(document.querySelector("#lastDaysProfit"), lastDaysProfit);
chart.render();
