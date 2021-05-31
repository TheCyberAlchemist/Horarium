xValues = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9"];
yValues = [2.6, 3.2, 1.5, 1.0, 4.5, 2.0, 3.4, 1.9, 3.5];
console.log("in the getJSON part!!");

var i,final_value = [],final_value_x = [];

for (i = 0; i < yValues.length; i++) {
  //console.log(yValues[i])
  if (yValues[i] < 3) {
    var temp = yValues[i];
    final_value.push(temp);
    var temp2 = xValues[i];
    final_value_x.push(temp2);
  }
}
var barColors = [
  "rgba(255, 99, 132, 0.2)",
  "rgba(255, 159, 64, 0.2)",
  "rgba(201, 203, 207, 0.2)",
  "rgba(153, 102, 255, 0.2)",
  "rgba(75, 192, 192, 0.2)",
  "rgba(54, 162, 235, 0.2)",
  "rgba(153, 102, 255, 0.2)",
];

ch = document.getElementById("myChart");
new Chart(ch, {
  type: "polarArea",
  data: {
    labels: final_value_x,
    datasets: [
      {
        hoverBorderColor: "purple",
        hoverBorderWidth: 2,
        backgroundColor: barColors,
        data: final_value,
        borderColor : "hsla(0, 0%, 66%, 0.877)"
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    hoverBorderWidth: 100,
    animation: {
      animateRotate: true,
      animateScale: true,
    },
    arc: true,
    //animateScale : true,
    legend: { display: true },
    title: {
      display: true,
    //   text: "needs improvment in following questions!",
    },
  },
}); //end of my chart
ch1 = document.getElementById("myChart1");
new Chart(ch1, {
  type: "radar",
  data: {
    labels: xValues,
    datasets: [
      {
        // label: "your progress this month!!",
        pointHoverRadius: 20,
        hoverBorderDash: 100,
        pointHoverBorderColor: "lightgreen",
        tension: 0,
        hoverBackgroundColor: "rgba(54, 162, 235, 0.2)",
        pointBackgroundColor: "rgba(54, 162, 235, 0.2)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgb(255, 99, 132)",
        data: yValues,
      },
    ],
  },
  options: {
    suggestedMin: 0,
    suggestedMax: 5,
    scales: {
      r: {
        angleLines: {
          display: true,
        },
        suggestedMin: 0,
        suggestedMax: 5,
      },
    },
    arc: true,
    responsive: true,
    mantainAspectRatio:false,
    legend: { display: true },
    title: {
      display: true,
    //   text: "progress in all the areas!",
    },
  },
}); //end of my chart
