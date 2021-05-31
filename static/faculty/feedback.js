var ENDPOINT = "./api";
// Array(11).fill("rgba(255, 99, 132, 0.2)"),
var opacity = "0.2";
my_charts = {};
function toggle_theme() {
	var el1 = document.getElementById("light"),
		el2 = document.getElementById("dark");
	//   console.log("hi");
	if (el1){
	if (el1.disabled) {
		// if dark
		console.log("was dark");
		opacity = "0.2";
		el1.disabled = false;
		el2.disabled = "disabled";
		localStorage.setItem("theme", "");
	} else {
		// if light
		console.log("was light");
		opacity = "0.4";
		el1.disabled = "disabled";
		el2.disabled = false;
		localStorage.setItem("theme", "dark");
	}
	}
	for(a in my_charts){
		my_charts[a].render();
	}
}
var subject_events;
function put_data(subject_events_json){
	subject_events = subject_events_json;
}
$(document).ready(function () {
	// AOS.init({
	// 	offset: 150,
	// });
	let cookie = localStorage.getItem("theme") || "";
	// console.log(cookie,"asdasd");
	if (cookie === "") {
		$("#slider1").prop("checked", true);
		toggle_theme();
	}else{
		opacity = '0.4';
	}
	for (a of subject_events){
		id_str = "day_rating__"+a['id'];
		my_charts[a['id']] = "asd";
		$.ajax({
			method: "GET",
			url: ENDPOINT,
			data : {
				'id' :a['id'],
			},
			success: function (data) {
				// console.log(data),
				drawBarGraph(data[0], data[1]);
				// drawBarGraph(data, "day_rating1");
			},
			error: function (error_data) {
				console.log(error_data);
			},
		});
	}
	function draw_line_graph(date,id){
		let mandatory_chart = [];
		var ctx = document.getElementById(id).getContext("2d");
		mandatory_chart[event_id] = new Chart(ctx, {
				type: "bar",
				data: {
					labels: labels,
					datasets: [
						{
							label: chartLabel,
							data: chartdata,
							backgroundColor: Array(11).fill(`rgba(255, 99, 132, ${opacity})`),
							borderColor: Array(11).fill("rgba(255, 99, 132, 1)"),
							borderWidth: 1,
						}
					]
				}
			});
	}
	function drawBarGraph(data, id, recursive = false) {
		// console.log(id);
		let event_id = id.split("__")[1];
		var labels = data.labels;
		var chartLabel = data.chartLabel;
		var chartdata = data.chartdata; 
		if (recursive) {
			my_charts[event_id].destroy();
		}
		if (data.ids) {
			var ids = data.ids;
		}
		if (data.button_id) {
			// console.log(data.button_name, data.button_id);
			$(data.button_id).off().on('click', function() {
				$.ajax({
					method: "GET",
					url: ENDPOINT,
					data: {
						'id' : event_id,
						graph_name: data.button_name,
					},
					success: function (data) {
						// change page of the selected chart div
						$("#" + data[1])
                            .parents(".row")
							.show(300);
						$("#" + id)
                            .parents(".row")
							.hide(300);
						console.log(data);
						drawBarGraph(data[0], data[1], true);
					},
					error: function (error_data) {
						console.log(error_data);
					},
				});
			});
		}
		var ctx = document.getElementById(id).getContext("2d");
		my_charts[event_id] = new Chart(ctx, {
			type: "bar",
			data: {
				labels: labels,
				datasets: [
					{
						label: chartLabel,
						data: chartdata,
						backgroundColor: Array(11).fill(`rgba(255, 99, 132, ${opacity})`),
						borderColor: Array(11).fill("rgba(255, 99, 132, 1)"),
						borderWidth: 1,
					},{
						label: "Q1",
						data: data.Q1,
						hidden: true,
						backgroundColor: Array(11).fill(`rgba(54, 162, 235, ${opacity})`),
						borderColor: Array(11).fill("rgba(54, 162, 235, 1)"),
						borderWidth: 1,
					},{
						label: "Q2",
						data: data.Q2,
						hidden: true,
						backgroundColor: Array(11).fill(`rgba(75, 192, 192, ${opacity})`),
						borderColor: Array(11).fill("rgba(75, 192, 192, 1)"),
						borderWidth: 1,
					},{
						label: "Q3",
						data: data.Q3,
						hidden: true,
						backgroundColor: Array(11).fill(`rgba(1,0,143, ${opacity})`),
						borderColor: Array(11).fill("rgba(1,0,143, 1)"),
						borderWidth: 1,
					},{
						label: "Q4",
						data: data.Q4,
						hidden: true,
						backgroundColor: Array(11).fill(`rgba(99, 252, 39,${opacity})`),
						borderColor: Array(11).fill("rgba(132, 218, 99,1)"),
						borderWidth: 1,
					},{
						label: "Q5",
						data: data.Q5,
						hidden: true,
						backgroundColor: Array(11).fill(`rgba(128,128,128, ${opacity})`),
						borderColor: Array(11).fill("rgb(128,128,128, 1)"),
						borderWidth: 1,
					},{
						label: "Q6",
						data: data.Q6,
						hidden: true,
						backgroundColor: Array(11).fill(`rgba(244, 9, 249, ${opacity})`),
						borderColor: Array(11).fill("rgb(172, 9, 175, 1)"),
						borderWidth: 1,
					},{
						label: "Q7",
						data: data.Q7,
						hidden: true,
						backgroundColor: Array(11).fill(`rgba(255, 0, 0, ${opacity})`),
						borderColor: Array(11).fill("rgba(255,0,0, 1)"),
						borderWidth: 1,
					},{
						label: "Q8",
						data: data.Q8,
						hidden: true,
						backgroundColor: Array(11).fill(`rgba(250,255,7, ${opacity})`),
						borderColor: Array(11).fill("rgba(250,255,7, 1)"),
						borderWidth: 1,
					},{
						label: "Q9",
						data: data.Q9,
						hidden: true,
						backgroundColor: Array(11).fill(`rgba(0, 255, 192, ${opacity})`),
						borderColor: Array(11).fill("rgba(0, 255, 192, 1)"),
						borderWidth: 1,
					},
					
				],
			},
			options: {
                responsive: true,
    			maintainAspectRatio: false,
                responsiveAnimationDuration: 0,
				onClick: function (evt, i) {
					e = i[0];
					if (ids && e) {
						var label_name = ids[e._index];
						var chart_id = this.canvas.id;
						console.log(chart_id + " " + label_name);
						$.ajax({
							method: "GET",
							url: ENDPOINT,
							data: {
								id: chart_id.split("__")[1],
								graph_name: chart_id.split("__")[0] + " " + label_name,
							},
							success: function (data) {
								// change page of the selected chart div
								$("#" + data[1])
									.parents(".row")
									.show(300);
								$("#" + chart_id)
                                    .parents(".row")
									.hide(300);
								// $("#show_week").click(function(){
								// 	console.log("button clicked");
								// 	$("#"+chart_id).parent().parent().show(300);
								// 	$("#"+data[1]).parent().parent().hide(300);
								// 	// $(".week_rating").css({"margin-top":'50px'});
								// });
								drawBarGraph(data[0], data[1], true);
							},
							error: function (error_data) {
								console.log(error_data);
							},
						});
					}
				},
				scales: {
					yAxes: [
						{
							display : true,
							scaleLabel : {
								display : true,
								labelString : 'Ratings '
							},
							ticks: {
								beginAtZero: true,
								suggestedMax: 5,
							},
						},
					],

					xAxes: [
						{
							display : true,
							scaleLabel : {
								display : true,
								labelString : 'Time Period '
							},
						},
					],
				},
				tooltips: {
					callbacks: {
							label: function(chart_id) {
								var avg_of = "Average of ";
								console.log(chart_id);
								switch (chart_id.datasetIndex) {
									case 0:
										return chart_id.label;
									case 1:
										return avg_of + data.len1[chart_id.index];
									case 2:
										return avg_of + data.len2[chart_id.index];
									case 3:
										return avg_of + data.len3[chart_id.index];
									case 4:
										return avg_of + data.len4[chart_id.index];
									case 5:
										return avg_of + data.len5[chart_id.index];
									case 6:
										return avg_of + data.len6[chart_id.index];
									case 7:
										return avg_of + data.len7[chart_id.index];
									case 8:
										return avg_of + data.len8[chart_id.index];
									case 9:
										return avg_of + data.len9[chart_id.index];
									default:
										break;
								}
								
							}
						}
					}
			},
		});
	}
});
