var STUDENT_SATISFACTION_URL = "./satisfaction";

$(document).ready(function (){
    let dates = [];
    let avg = [];
	console.log("asdasd");
	$.ajax({
		method: "GET",
		url: STUDENT_SATISFACTION_URL,
		// data : {
		// 	'id' :a['id'],
		// },
		success: function (data) {
			// console.log(data);
			// drawBarGraph(data, "day_rating1");
            for(let i of data) { dates.push(i['t']) }
            for(let i of data) { avg.push(i['ave']) }

			draw_line_graph("student_satisfaction", data);
		}, 
		error: function (error_data) {
			console.log(error_data);
		},
	});
    function draw_line_graph(id,data){
        // use data for chart and see console.log 
        var ctx = document.getElementById(id).getContext("2d");
        var timeFormat = 'DD/MM/YYYY';
        var satisfaction_chart = new Chart(ctx, {
          type: "line",
          data: {
            labels : dates,
            datasets: [
                {
                    label: 'Avg. Satisfaction of Students ',
                    backgroundColor: 'rgba(255, 99, 132,0.1)',
                    borderColor: 'rgb(255, 199, 132)',
                    data : avg,
                }
            ]
            },
          options: {
              tension: 0.3,
              responsive: true,
              maintainAspectRatio: false,
            scales: {
                xAxes: [{
                    type:       "time",
                    time: {
                        format: timeFormat,
                        tooltipFormat: 'll'
                    },
                    scaleLabel: {
                        display:     true,
                        labelString: 'Date'
                    }
                }],
                //   xAxes: {
                //         type: 'time',
                //         time: {
                //             displayFormats: {
                //                 quarter: 'MMM YYYY',
                //                 tooltipFormat: 'DD/MM/YY',
                //                 unit: 'month',				
                //             }
                //         }
                //     }
                // },
                yAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'value'
                    }
                }],
            //   yAxes: {
            //     beginAtZero: true,
            //   },
          },
        },
        });
    }
});

