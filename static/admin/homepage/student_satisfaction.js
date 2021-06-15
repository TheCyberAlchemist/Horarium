var STUDENT_SATISFACTION_URL = "./satisfaction";

$(document).ready(function (){
	console.log("asdasd");
	$.ajax({
		method: "GET",
		url: STUDENT_SATISFACTION_URL,
		// data : {
		// 	'id' :a['id'],
		// },
		success: function (data) {
			console.log(data)
			// drawBarGraph(data, "day_rating1");
			draw_line_graph("student_satisfaction", data);
		},
		error: function (error_data) {
			console.log(error_data);
		},
	});
});

function draw_line_graph(id,data){
	// use data for chart and see console.log 
	var ctx = document.getElementById(id).getContext("2d");
    var myChart = new Chart(ctx, {
      type: "line",
      data: data,
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
		  x: {
				type: 'time',
				time: {
					displayFormats: {
						quarter: 'MMM YYYY',
						tooltipFormat: 'DD/MM/YY',
						unit: 'month',					
					}
				}
			}
        },
      },
    });
}