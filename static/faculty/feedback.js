var ENDPOINT = "./api";
var MANDATORY = "./mandatory";
var AVERAGE_ALL = "./ave_all";
// Array(11).fill("rgba(255, 99, 132, 0.2)"),
var opacity = "0.2";
var my_charts = {};
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
var subject_events,my_types;
function put_data(subject_events_json,my_types_json){
	subject_events = subject_events_json;
	my_types = my_types_json;
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
	for (let a of subject_events){
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
		$.ajax({
			method: "GET",
			url: AVERAGE_ALL,
			data : {
				'id' :a['id'],
			},
			success: function (data) {
				console.log(data);
				let temp_data = {}
				Object.assign(temp_data, data)
				temp_data.chartdata = [];
				temp_data.labels = [];
				for (i in data.chartdata) {
					if (data.chartdata[i] > 0){
						temp_data.chartdata.push(data.chartdata[i])
						temp_data.labels.push(data.labels[i])
					}
				}
				console.log(temp_data);
				draw_radar_graph(temp_data,"progress__"+a['id'])

				let temp_dict = [];
				for (i = 0; i < data.chartdata.length; i++) {
					temp_dict.push({"label":data.labels[i],"rating":data.chartdata[i]})
				}
				temp_dict.sort(function(a, b) {
					return ((a.rating < b.rating) ? -1 : ((a.rating == b.rating) ? 0 : 1))
				})
				// console.log(temp_dict);
				data.chartdata = [];
				data.labels = [];
				for(let i of temp_dict.splice(temp_dict.length-4,4)){
					if (i.rating > 0){
						data.chartdata.push(i.rating)
						data.labels.push(i.label)
					}
				}
				// for (i = 0; i < data.chartdata.length; i++) {
				// 	let data_i = data.chartdata[i]
				// 	if (data_i < 3 && data_i > 0) {
				// 	  temp_data.push(data_i);
				// 	  temp_labels.push(data.labels[i]);
				// 	}
				// }
				// data.chartdata = temp_data;
				// data.labels = temp_labels;
				draw_polarArea_graph(data,"improvement__"+a['id']);
			},
			error: function (error_data) {
				console.log(error_data);
			},
		});
	}
	for (let type of my_types){
		let id_str = "mandatory_feedback__"+type['id'];
		$.ajax({
			method: "GET",
			url: MANDATORY,
			data : {
				'id' :type['id'],
			},
			success: function (data) {
				// console.log(data),
				draw_line_graph(data,id_str);
				// drawBarGraph(data, "day_rating1");
			},
			error: function (error_data) {
				console.log(error_data);
			},
		});
	}

	function draw_line_graph(data,id){
		// let mandatory_chart = [];
		var labels = data.labels;
		var chartLabel = data.chartLabel;
		var chartdata = data.chartdata; 

		let type_id = id.split("__")[1];
		var ctx = document.getElementById(id).getContext("2d");
		new Chart(ctx, {
			type: "line",
			data: {
				labels: labels,
				datasets: [
					{
						label: chartLabel,
						data: chartdata,
						// backgroundColor: Array(11).fill(""),
                        fill : false,
						// tension: 0.01,
                        borderColor: "rgba(75, 192, 192,.7)",
                        borderWidth: 3,
					}
				],
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				responsiveAnimationDuration: 0,
                animation : {
                    easing: "easeInOutBack"
                },
				scales: {
					yAxes: [
						{
							display : true,
							scaleLabel : {
								display : true,
								labelString : 'Ratings',
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
								labelString : 'Questions'
							},
						},
					],
				},
				tooltips: {
					callbacks: {
						label: function(chart_id) {
							var avg_of = `Average of ${data.feedback_count}`;
							return avg_of;
						}
					}
				}
			}
		});
	}

	function drawBarGraph(data, id, recursive = false) {
		// console.log(id);
		let event_id = id.split("__")[1];
		var labels = data.labels;
		var chartLabel = data.chartLabel;
		var chartdata = data.chartdata; 
		// console.log(data.chartdata)
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
                        backgroundColor: Array(11).fill(`rgba(255, 116, 2, ${opacity})`), 
						borderColor: Array(11).fill("rgba(255, 116, 2, 1)"),
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
                        backgroundColor: Array(11).fill(`rgba(255, 99, 132, ${opacity})`),
						borderColor: Array(11).fill("rgba(255, 99, 132, 1)"),
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
                animation : {
                    easing: "easeInOutBack"
                },
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
								// console.log(chart_id);
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

	function draw_radar_graph(data,id){
		var labels = data.labels;
		var chartLabel = data.chartLabel;
		var chartdata = data.chartdata;
		var ctx = document.getElementById(id).getContext("2d");
		new Chart(ctx, {
			type: "radar",
			data: {
			  labels: labels,
			  datasets: [
				{
				  label: chartLabel,
				  pointHoverRadius: 20,
				  hoverBorderDash: 100,
				  pointHoverBorderColor: "lightgreen",
				  tension: 0,
				  hoverBackgroundColor: "rgba(54, 162, 235, 0.2)",
				  pointBackgroundColor: "rgba(54, 162, 235, 0.2)",
				  backgroundColor: "rgba(255, 99, 132, 0.2)",
				  borderColor: "rgb(255, 99, 132)",
				  data: chartdata,
				},
			  ],
			},
			options: {
                scale : {
                    ticks : {
                        beginAtZero : false,
                        max : 5,
                        min : 1,
                    }
                },
			  suggestedMin: 1,
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
		  });
	}

	function draw_polarArea_graph(data,id){
		var labels = data.labels;
		var chartdata = data.chartdata;
		var ctx = document.getElementById(id).getContext("2d");
		new Chart(ctx, {
		type: "polarArea",
		data: {
		labels: labels,
		datasets: [
			{
			hoverBorderColor: "purple",
			hoverBorderWidth: 2,
			backgroundColor: barColors,
			data: chartdata,
			borderColor : "hsla(0, 0%, 66%, 0.877)"
			},
		],
		},
		options: {
		responsive: true,
		maintainAspectRatio: false,
		hoverBorderWidth: 100,
        scale : {
            ticks : {
                beginAtZero : false,
                max : 5,
                min : 1,
            }
        },
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
		});
	}
});
