var ENDPOINT = '/faculty/api';

function toggle_theme() {
	var el1 = document.getElementById("light"),
	  el2 = document.getElementById("dark");
  //   console.log("hi");
	if (el1.disabled) {   // if dark
	  localStorage.setItem("theme", "");
	  el1.disabled = false;
	  el2.disabled = "disabled";
	} else {              // if light
	  el1.disabled = "disabled";
	  el2.disabled = false;
	  localStorage.setItem("theme", "dark");
	} 
}

$(document).ready(function () {
	AOS.init({
		offset : 150,
	});
	let cookie = localStorage.getItem("theme") || "";
	// console.log(cookie,"asdasd");
	if (cookie === ""){
		$("#slider1").prop("checked",true);
			// console.log("hi");
		toggle_theme();
	}
	
	$.ajax({
		method: "GET",
		url: ENDPOINT,
		// data : {
		// },
		success: function(data) {
			drawBarGraph(data[0], 'month_rating');
			drawBarGraph(data[1],'month_response');
			console.log("drawing");
		},
		error: function(error_data) {
		console.log(error_data);
		}
	});
	var myChart;
	function drawBarGraph(data, id,recursive = false) {
		var labels = data.labels;
		var chartLabel = data.chartLabel;
		var chartdata = data.chartdata;
		if (data.ids)
			var ids = data.ids;
		console.log(data);
		var ctx = document.getElementById(id).getContext('2d');
		if (recursive){
			myChart.destroy();
		}
		myChart = new Chart(ctx, {
			type: 'bar',
			data: {
			labels: labels,
			datasets: [{
				label: chartLabel,
				data: chartdata,
				backgroundColor: [
				'rgba(255, 99, 132, 0.2)',
				'rgba(54, 162, 235, 0.2)',
				'rgba(255, 206, 86, 0.2)',
				'rgba(75, 192, 192, 0.2)',
				'rgba(153, 102, 255, 0.2)',
				'rgba(255, 159, 64, 0.2)'
				],
				borderColor: [
				'rgba(255, 99, 132, 1)',
				'rgba(54, 162, 235, 1)',
				'rgba(255, 206, 86, 1)',
				'rgba(75, 192, 192, 1)',
				'rgba(153, 102, 255, 1)',
				'rgba(255, 159, 64, 1)'
				],
				borderWidth: 1
			}]
			},
			options: {
				onClick : function (evt, i) {
					e = i[0];
					if ( ids && e){
						var label_name = ids[e._index];
						var chart_id = this.canvas.id
						console.log(chart_id + " " + label_name);
						// console.log(xhRT_ID);
						$.ajax({
							method: "GET",
							url: ENDPOINT,
							data : {
								graph_name : chart_id + " " + label_name
							},
							success: function(data) {
								// change page of the selected chart div
								drawBarGraph(data[0],data[1],true)
							},
							error: function(error_data) {
							console.log(error_data);
							}
						});
					}
				},
			scales: {
				yAxes: [{
				ticks: {
					beginAtZero: true,
					suggestedMax:5,
				}
				}]
			}
			}
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