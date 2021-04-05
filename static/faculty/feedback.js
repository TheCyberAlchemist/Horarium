var ENDPOINT = "/faculty/api";
function toggle_theme() {
	var el1 = document.getElementById("light"),
		el2 = document.getElementById("dark");
	//   console.log("hi");
	if (el1.disabled) {
		// if dark
		localStorage.setItem("theme", "");
		el1.disabled = false;
		el2.disabled = "disabled";
	} else {
		// if light
		el1.disabled = "disabled";
		el2.disabled = false;
		localStorage.setItem("theme", "dark");
	}
}

$(document).ready(function () {
	AOS.init({
		offset: 150,
	});
	let cookie = localStorage.getItem("theme") || "";
	// console.log(cookie,"asdasd");
	if (cookie === "") {
		$("#slider1").prop("checked", true);
		// console.log("hi");
		toggle_theme();
	}

	$.ajax({
		method: "GET",
		url: ENDPOINT,
		// data : {
		// },
		success: function (data) {
			drawBarGraph(data, "day_rating");
		},
		error: function (error_data) {
			console.log(error_data);
		},
	});
	var myChart;
	function drawBarGraph(data, id, recursive = false) {
		var labels = data.labels;
		var chartLabel = data.chartLabel;
		var chartdata = data.chartdata; 
		if (recursive) {
			myChart.destroy();
		}
		if (data.ids) {
			var ids = data.ids;
		}
		if (data.button_id) {
			console.log(data.button_name, data.button_id);
			$(data.button_id).off().on('click', function() {
				$.ajax({
					method: "GET",
					url: ENDPOINT,
					data: {
						graph_name: data.button_name,
					},
					success: function (data) {
						// change page of the selected chart div

						$("#" + data[1])
							.parent()
							.parent()
							.show(300);
						$("#" + id)
							.parent()
							.parent()
							.hide(300);

						// $("#show_week").click(function(){
						// 	console.log("button clicked");
						// 	$("#"+chart_id).parent().parent().show(300);
						// 	$("#"+data[1]).parent().parent().hide(300);
						// 	// $(".week_rating").css({"margin-top":'50px'});
						// });
						drawBarGraph(data[0], data[1], true);
						// console.log(data);
					},
					error: function (error_data) {
						console.log(error_data);
					},
				});
			});
		}
		var ctx = document.getElementById(id).getContext("2d");
		myChart = new Chart(ctx, {
			type: "bar",
			data: {
				labels: labels,
				datasets: [
					{
						label: chartLabel,
						data: chartdata,
						backgroundColor: [
							"rgba(255, 99, 132, 0.2)",
							"rgba(255, 99, 132, 0.2)",
							"rgba(255, 99, 132, 0.2)",
							"rgba(255, 99, 132, 0.2)",
							"rgba(255, 99, 132, 0.2)",
							"rgba(255, 99, 132, 0.2)",
							"rgba(255, 99, 132, 0.2)",
							"rgba(255, 99, 132, 0.2)",
							"rgba(255, 99, 132, 0.2)",
							"rgba(255, 99, 132, 0.2)",
							"rgba(255, 99, 132, 0.2)",
							"rgba(255, 99, 132, 0.2)",
						],
						borderColor: [
							"rgba(255, 99, 132, 1)",
							"rgba(255, 99, 132, 1)",
							"rgba(255, 99, 132, 1)",
							"rgba(255, 99, 132, 1)",
							"rgba(255, 99, 132, 1)",
							"rgba(255, 99, 132, 1)",
							"rgba(255, 99, 132, 1)",
							"rgba(255, 99, 132, 1)",
							"rgba(255, 99, 132, 1)",
							"rgba(255, 99, 132, 1)",
							"rgba(255, 99, 132, 1)",
                            
						],
						borderWidth: 1,
					},{
						label: "Q1",
						data: data.Q1,
						hidden: true,
						backgroundColor: [
							"rgba(54, 162, 235, 0.2)",
							"rgba(54, 162, 235, 0.2)",
							"rgba(54, 162, 235, 0.2)",
							"rgba(54, 162, 235, 0.2)",
							"rgba(54, 162, 235, 0.2)",
							"rgba(54, 162, 235, 0.2)",
							"rgba(54, 162, 235, 0.2)",
							"rgba(54, 162, 235, 0.2)",
							"rgba(54, 162, 235, 0.2)",
							
						],
						borderColor: [
							"rgba(54, 162, 235, 1)",
							"rgba(54, 162, 235, 1)",
							"rgba(54, 162, 235, 1)",
							"rgba(54, 162, 235, 1)",
							"rgba(54, 162, 235, 1)",
							"rgba(54, 162, 235, 1)",
							"rgba(54, 162, 235, 1)",
							"rgba(54, 162, 235, 1)",
							"rgba(54, 162, 235, 1)",
							
						],
						borderWidth: 1,
					},{
						label: "Q2",
						data: data.Q2,
						hidden: true,
						backgroundColor: [
							"rgba(255, 99, 132, 0.2)",
							"rgba(54, 162, 235, 0.2)",
							"rgba(75, 192, 192, 0.2)",
							"rgba(153, 102, 255, 0.2)",
							"rgba(255, 159, 64, 0.2)",
							"rgba(1,0,143, 0.2)",
							"rgba(99, 252, 39,0.2)",
							"rgba(128,128,128, 0.2)",
                            "rgba(244, 9, 249, 0.2)",
						    "rgba(255, 0, 0, 0.2)",
						],
						borderColor: [
							"rgba(255, 206, 86, 1)",
							"rgba(75, 192, 192, 1)",
							"rgba(153, 102, 255, 1)",
							"rgba(255, 159, 64, 1)",
							"rgba(1,0,143, 1)",
							"rgba(99, 252, 39,1)",
							"rgb(128,128,128, 1)",
                            "rgba(244, 9, 249, 1)",
							"rgba(255, 0, 0, 1)",
						],
						borderWidth: 1,
					},{
						label: "Q3",
						data: data.Q3,
						hidden: true,
						backgroundColor: [
							"rgba(1,0,143, 0.2)",
							"rgba(1,0,143, 0.2)",
							"rgba(1,0,143, 0.2)",
							"rgba(1,0,143, 0.2)",
							"rgba(1,0,143, 0.2)",
							"rgba(1,0,143, 0.2)",
							"rgba(1,0,143, 0.2)",
							"rgba(1,0,143, 0.2)",
							"rgba(1,0,143, 0.2)",
							"rgba(1,0,143, 0.2)",
						],
						borderColor: [
							"rgba(1,0,143, 1)",
							"rgba(1,0,143, 1)",
							"rgba(1,0,143, 1)",
							"rgba(1,0,143, 1)",
							"rgba(1,0,143, 1)",
							"rgba(1,0,143, 1)",
							"rgba(1,0,143, 1)",
							"rgba(1,0,143, 1)",
							"rgba(1,0,143, 1)",
							"rgba(1,0,143, 1)",
						],
						borderWidth: 1,
					},{
						label: "Q4",
						data: data.Q4,
						hidden: true,
						backgroundColor: [
							"rgba(99, 252, 39,0.2)",
							"rgba(99, 252, 39,0.2)",
							"rgba(99, 252, 39,0.2)",
							"rgba(99, 252, 39,0.2)",
							"rgba(99, 252, 39,0.2)",
							"rgba(99, 252, 39,0.2)",
							"rgba(99, 252, 39,0.2)",
							"rgba(99, 252, 39,0.2)",
							"rgba(99, 252, 39,0.2)",
							"rgba(99, 252, 39,0.2)",
						],
						borderColor: [
							"rgba(132, 218, 99,1)",
							"rgba(132, 218, 99,1)",
							"rgba(132, 218, 99,1)",
							"rgba(132, 218, 99,1)",
							"rgba(132, 218, 99,1)",
							"rgba(132, 218, 99,1)",
							"rgba(132, 218, 99,1)",
							"rgba(132, 218, 99,1)",
							"rgba(132, 218, 99,1)",
							"rgba(132, 218, 99,1)",
						],
						borderWidth: 1,
					},{
						label: "Q5",
						data: data.Q5,
						hidden: true,
						backgroundColor: [
							"rgba(128,128,128, 0.2)",
							"rgba(128,128,128, 0.2)",
							"rgba(128,128,128, 0.2)",
							"rgba(128,128,128, 0.2)",
							"rgba(128,128,128, 0.2)",
							"rgba(128,128,128, 0.2)",
							"rgba(128,128,128, 0.2)",
							"rgba(128,128,128, 0.2)",
							"rgba(128,128,128, 0.2)",
							"rgba(128,128,128, 0.2)",
						],
						borderColor: [
							"rgb(128,128,128, 1)",
							"rgb(128,128,128, 1)",
							"rgb(128,128,128, 1)",
							"rgb(128,128,128, 1)",
							"rgb(128,128,128, 1)",
							"rgb(128,128,128, 1)",
							"rgb(128,128,128, 1)",
							"rgb(128,128,128, 1)",
							"rgb(128,128,128, 1)",
							"rgb(128,128,128, 1)",
						],
						borderWidth: 1,
					},{
						label: "Q6",
						data: data.Q6,
						hidden: true,
						backgroundColor: [
							"rgba(244, 9, 249, 0.2)",
							"rgba(244, 9, 249, 0.2)",
							"rgba(244, 9, 249, 0.2)",
							"rgba(244, 9, 249, 0.2)",
							"rgba(244, 9, 249, 0.2)",
							"rgba(244, 9, 249, 0.2)",
							"rgba(244, 9, 249, 0.2)",
							"rgba(244, 9, 249, 0.2)",
							"rgba(244, 9, 249, 0.2)",
							"rgba(244, 9, 249, 0.2)",
						],
						borderColor: [
							"rgb(172, 9, 175, 1)",
							"rgb(172, 9, 175, 1)",
							"rgb(172, 9, 175, 1)",
							"rgb(172, 9, 175, 1)",
							"rgb(172, 9, 175, 1)",
							"rgb(172, 9, 175, 1)",
							"rgb(172, 9, 175, 1)",
							"rgb(172, 9, 175, 1)",
							"rgb(172, 9, 175, 1)",
							"rgb(172, 9, 175, 1)",
						],
						borderWidth: 1,
					},{
						label: "Q7",
						data: data.Q7,
						hidden: true,
						backgroundColor: [
							"rgba(255, 0, 0, 0.2)",
							"rgba(255, 0, 0, 0.2)",
							"rgba(255, 0, 0, 0.2)",
							"rgba(255, 0, 0, 0.2)",
							"rgba(255, 0, 0, 0.2)",
							"rgba(255, 0, 0, 0.2)",
							"rgba(255, 0, 0, 0.2)",
							"rgba(255, 0, 0, 0.2)",
							"rgba(255, 0, 0, 0.2)",
							"rgba(255, 0, 0, 0.2)",
						],
						borderColor: [
							"rgba(255,0,0, 1)",
							"rgba(255,0,0, 1)",
							"rgba(255,0,0, 1)",
							"rgba(255,0,0, 1)",
							"rgba(255,0,0, 1)",
							"rgba(255,0,0, 1)",
							"rgba(255,0,0, 1)",
							"rgba(255,0,0, 1)",
							"rgba(255,0,0, 1)",
							"rgba(255,0,0, 1)",
						],
						borderWidth: 1,
					},{
						label: "Q8",
						data: data.Q8,
						hidden: true,
						backgroundColor: [
							"rgba(250,255,7, 0.2)",
							"rgba(250,255,7, 0.2)",
							"rgba(250,255,7, 0.2)",
							"rgba(250,255,7, 0.2)",
							"rgba(250,255,7, 0.2)",
							"rgba(250,255,7, 0.2)",
							"rgba(250,255,7, 0.2)",
							"rgba(250,255,7, 0.2)",
							"rgba(250,255,7, 0.2)",
							"rgba(250,255,7, 0.2)",
						],
						borderColor: [
							"rgba(250,255,7, 1)",
							"rgba(250,255,7, 1)",
							"rgba(250,255,7, 1)",
							"rgba(250,255,7, 1)",
							"rgba(250,255,7, 1)",
							"rgba(250,255,7, 1)",
							"rgba(250,255,7, 1)",
							"rgba(250,255,7, 1)",
							"rgba(250,255,7, 1)",
							"rgba(250,255,7, 1)",
						],
						borderWidth: 1,
					},{
						label: "Q9",
						data: data.Q9,
						hidden: true,
						backgroundColor: [
							"rgba(0, 255, 192, 0.2)",
							"rgba(0, 255, 192, 0.2)",
							"rgba(0, 255, 192, 0.2)",
							"rgba(0, 255, 192, 0.2)",
							"rgba(0, 255, 192, 0.2)",
							"rgba(0, 255, 192, 0.2)",
							"rgba(0, 255, 192, 0.2)",
							"rgba(0, 255, 192, 0.2)",
							"rgba(0, 255, 192, 0.2)",
							"rgba(0, 255, 192, 0.2)",
							"rgba(0, 255, 192, 0.2)",
						],
						borderColor: [
							"rgba(0, 255, 192, 1)",
							"rgba(0, 255, 192, 1)",
							"rgba(0, 255, 192, 1)",
							"rgba(0, 255, 192, 1)",
							"rgba(0, 255, 192, 1)",
							"rgba(0, 255, 192, 1)",
							"rgba(0, 255, 192, 1)",
							"rgba(0, 255, 192, 1)",
							"rgba(0, 255, 192, 1)",
							"rgba(0, 255, 192, 1)",
							"rgba(0, 255, 192, 1)",
						],
						borderWidth: 1,
					},
					
				],
			},
			options: {
				// responsive: true,
    			maintainAspectRatio: false,
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
								graph_name: chart_id + " " + label_name,
							},
							success: function (data) {
								// change page of the selected chart div
								$("#" + data[1])
									.parent()
									.parent()
									.show(300);
								$("#" + chart_id)
									.parent()
									.parent()
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

// var ctx = $('#myChart');
// 	var myChart = new Chart(ctx, {
// 		type: 'bar',
// 		data: {
// 			labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
// 			datasets: [{
// 				label: '# of Votes',
// 				data: [12, 19, 3, 5, 2, 3],
// 				backgroundColor: [
// 					'rgba(255, 99, 132, 0.2)',
// 					'rgba(54, 162, 235, 0.2)',
// 					'rgba(255, 206, 86, 0.2)',
// 					'rgba(75, 192, 192, 0.2)',
// 					'rgba(153, 102, 255, 0.2)',
// 					'rgba(255, 159, 64, 0.2)'
// 				],
// 				borderColor: [
// 					'rgba(255, 99, 132, 1)',
// 					'rgba(54, 162, 235, 1)',
// 					'rgba(255, 206, 86, 1)',
// 					'rgba(75, 192, 192, 1)',
// 					'rgba(153, 102, 255, 1)',
// 					'rgba(255, 159, 64, 1)'
// 				],
// 				borderWidth: 1
// 			}]
// 		},
// 		options: {
// 			scales: {
// 				yAxes: [{
// 					ticks: {
// 						beginAtZero: true
// 					}
// 				}]
// 			}
// 		}
// 	});
// $(document).ready(function () {
// 	console.log("JQuery is working");
// 	/*AOS.init({
// 	  offset: 150,
// 	});*/

// 	var ctx = document.getElementById('myChart').getContext('2d');
// 	var chart = new Chart(ctx, {
// 		// The type of chart we want to create
// 		type: 'bar',

// 		// The data for our dataset
// 		data: {
// 			labels: [{%for i in qs%}'{{i.name}}',{%endfor%}],
// 			datasets: [{
// 				label: 'My First dataset',
// 				data: [{%for i in qs%} {{i.money}}, {%endfor%}],
// 				backgroundColor : ['#FCDC3B','#A2EC88','#97FFD7','#567FCE','#FF4D94','#FF3C2A'],
// 				borderColor : ['yellow','green','cyan','blue','pink','red','grey'],
// 				borderWidth : 2,
// 			}]
// 		},
// 		// Configuration options go here
// 		options: {}
// 	});
// 	////////////////Radar////////////////
// 	var ctx = document.getElementById('myChart2').getContext('2d');
// 	var chart = new Chart(ctx, {
// 		// The type of chart we want to create
// 		type: 'radar',

// 		// The data for our dataset
// 		data: {
// 			labels: [{%for i in qs%}'{{i.name}}',{%endfor%}],
// 			datasets: [{
// 				label: 'My First dataset',
// 				data: [{%for i in qs%} {{i.money}}, {%endfor%}],
// 				//backgroundColor : ['red','green','blue','pink','purple','orange','cyan'],
// 				backgroundColor : "pink",
// 				borderColor : "red"

// 			}]
// 		},
// 		// Configuration options go here
// 		options: {}
// 	});

//   });
