function replaceURLs(message) {
  if(!message) return;
 
  var urlRegex = /(((https?:\/\/)|(www\.))[^\s]+)/g;
  return message.replace(urlRegex, function (url) {
    var hyperlink = url;
    if (!hyperlink.match('^https?:\/\/')) {
      hyperlink = 'http://' + hyperlink;
    }
    return '<a href="' + hyperlink + '" target="_blank" rel="noopener noreferrer">' + url + '</a>'
  });
}
function get_sticky_note(pk,title,body){
	var txt3 = document.createElement("div");  // Create with DOM
	console.log(pk)
	txt3.classList.add(`note_id_${pk}`);
	txt3.classList.add(`sticky_note`);
  	txt3.innerHTML = `	
    <div class="card mb-3 feedback_form_card">
        <div class="card-body">
        <h5 class="card-title text-center">
		<button class="delete_note"  pk = "${pk}" style="background-color:red">
			delete
		</button></h5>
		<button class="btn" style="background-color:#066">
			${title}
		</button></h5>
        <p class="card-text">${replaceURLs(body)}</p>
        <!--<p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>-->
        </div>
    </div>`
	return txt3;
}

function append_sticky_note(note_obj){
	let title = note_obj['title']
	let body = note_obj['body']
	let pk = note_obj['pk']
	if (!title || !body || !pk)
		return false;

	card = get_sticky_note(pk,title,body);

	$("#sticky_notes_body").append(card);

	card.addEventListener("mouseover",function(){
		// get_event_cell_by_id(event.pk).effect("highlight", {}, 3000);
		// check w3school for args
	});
	card.getElementsByClassName("delete_note")[0].addEventListener("click",function(){
		delete_note(this)
	});
	
}
function delete_note(asd){
	var delete_button = jQuery(asd);
	// console.log()
	let pk = delete_button.attr('pk')
	$.ajax({
		method: "POST",
		url: "./delete_sticky_notes/",
		data : {
			'pk':pk
		},
		success: function (all_notes) {
			console.log(all_notes);
			clear_all_notes()
			for (note of all_notes){
				append_sticky_note(note)
			}
		},
		error: function (error_data) {
			console.log(error_data);
		},
	});
	// let card = delete_button.parents('.sticky_note');
	// console.log(card)
	
	
}
function clear_all_notes(){
	$("#sticky_notes_body").html("");
}
jQuery(function () {
	var csrftoken = Cookies.get('csrftoken');
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	// Ensure jQuery AJAX calls set the CSRF header to prevent security errors
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
	$("#sticky_note_form").on('submit',function(e) {
		e.preventDefault();
		let title = $(this).find("#title_input").val()
		let body = $(this).find("#body_input").val()
		$.ajax({
			method: "POST",
			url: "./get_put_sticky_notes/",
			data : {
				'title':title,
				'body':body
			},
			success: function (all_notes) {
				console.log(all_notes);
				$("#sticky_note_form").trigger('reset');
				clear_all_notes()
				for (note of all_notes){
					append_sticky_note(note)
				}
			},
			error: function (error_data) {
				console.log(error_data);
			},
		});
	})
	$.ajax({
		method: "GET",
		url: "./get_put_sticky_notes",
		// data : {
		// 	'id' :type['id'],
		// },
		success: function (data) {
			console.log(data)
			for (d of data){
				append_sticky_note(d)
			}
		},
		error: function (error_data) {
			console.log(error_data);
		},
	});
})
