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
        var timeFormat = 'YYYY/MM/DD';
        var satisfaction_chart = new Chart(ctx, {
          type: "line",
          data: {
            datasets: [
                {
                    label: 'Avg. Satisfaction of Students ',
                    backgroundColor: 'rgba(255, 99, 132,0.1)',
                    borderColor: 'rgb(255, 199, 132)',
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
                    min: 0,
                    max: 5,
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

