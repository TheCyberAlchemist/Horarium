$(function(){
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
    $(".draggable").draggable({
        revert: true,
        cursor: "move",
        cursorAt:{top:56,left:56},
        drag: function( event, ui ) {
            var select = $(this);
            event_link = select.attr("event_link");
            name = select.attr("name");
            color = select.attr("color");
        }
    }).disableSelection();
    // console.log("hii");
    $( ".droppable" ).droppable({
        drop: function( event, ui ) {
        let obj = $( this );
        obj.html(name)
        obj.css({"background-color":color})
        obj.attr({"name":name ,"color":color,"event_link":event_link});
        // obj.click(function() {
        //   open(event_link);
        // });
        }
    });
    $('.save').click(function(){
        var myRows = [];
        var headersText = [];
        var $headers = $("th");
        var $rows = $("tbody tr").each(function(index) {
          $cells = $(this).find("td");
          myRows[index] = {};

          $cells.each(function(cellIndex) {
            // Set the header text
            if(headersText[cellIndex] === undefined) {
              headersText[cellIndex] = $($headers[cellIndex]).text();
            }
            // Update the row object with the header/cell combo
            myRows[index][headersText[cellIndex]] = $(this).attr("color");
            // myRows[index][headersText[comboellIndex]] = $(this).attr("link");
          });    
        })
        let state = JSON.stringify(myRows,null," ");
        console.log(state);
        // super($item, container);
        $.ajax({
            type: "POST",
            data: state,
            url: ""
        });
        // alert(state);
    });
});
// $(function() {
//         var csrftoken = Cookies.get('csrftoken');

//     function csrfSafeMethod(method) {
//         // these HTTP methods do not require CSRF protection
//         return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//     }

//     // Ensure jQuery AJAX calls set the CSRF header to prevent security errors
//     $.ajaxSetup({
//         beforeSend: function(xhr, settings) {
//             if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//                 xhr.setRequestHeader("X-CSRFToken", csrftoken);
//             }
//         }
// });

