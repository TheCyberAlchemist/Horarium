var STUDENT_SATISFACTION_URL = "./satisfaction";
var m_data;
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
            m_data = data;
			// drawBarGraph(data, "day_rating1");
            for(let i of data) { 
                // dates.push(new Date(i['t']))
                dates.push(i['t'])
            }
            for(let i of data) { avg.push(i['ave']);avg.push(1) }

			draw_line_graph("student_satisfaction", data);
		}, 
		error: function (error_data) {
			console.log(error_data);
		},
	});
    function draw_line_graph(id,data){
        // use data for chart and see console.log 
        var ctx = document.getElementById(id).getContext("2d");
        var timeFormat = 'YYYY/MM/DD';
        var background_1 = ctx.createLinearGradient(0, 0, 0, 600);
        var border_1 = ctx.createLinearGradient(0, 0, 0, 600);
        background_1.addColorStop(0, 'rgba(0, 0, 255,0.4)');
        background_1.addColorStop(1, 'rgba(255, 0, 0,0.4)');
        border_1.addColorStop(0, 'rgba(102, 0, 255,1)');
        border_1.addColorStop(1, 'rgba(255, 80, 80,1)');

        var satisfaction_chart = new Chart(ctx, {
          type: "line",
          data: {
            datasets: [
                {
                    label: 'Avg. Satisfaction of Students ',
                    /*backgroundColor: 'rgba(131, 253, 116,0.4)',
                    borderColor: 'rgba(28, 255, 0,1)',*/
                    backgroundColor: background_1,
                    borderColor : border_1,
                    data : m_data,
                }
            ]
            },
          options: {
              responsive: true,
              tension: 0.3,
              maintainAspectRatio: false,
            scales: {
                xAxes: [{
                    type:"time",
                    time:{
                        format: timeFormat,
                        tooltipFormat: 'll',
                        unit:"month",
                    },
                    scaleLabel: {
                        display:true,
                        labelString: 'Date'
                    }
                }],
                yAxes: [{
                    ticks : {
                        min: 1,
                        max: 5,
                    },
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

