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
    //  $('.save').click(function(){
    //       var myrows = [];
    //       var headerstext = [];
    //       var $headers = $("th");
    //       var $rows = $("tbody tr").each(function(index) {
    //         $cells = $(this).find("td");
    //         myrows[index] = {};
    //
    //         $cells.each(function(cellindex) {
    //           // set the header text
    //           if(headerstext[cellindex] === undefined) {
    //             headerstext[cellindex] = $($headers[cellindex]).text();
    //           }
    //           // update the row object with the header/cell combo
    //           myrows[index][headerstext[cellindex]] = $(this).attr("name");
    //           // myrows[index][headerstext[comboellindex]] = $(this).attr("link");
    //         });
    //       })
    //       let state = json.stringify(myrows,null," ");
    //       console.log(state);
    //       // super($item, container);
    //       $.ajax({
    //           type: "post",
    //           data: state,
    //           url: ""
    //       });
    //       // alert(state);
    // });
    $('.save').click(function(){
      var table = $('table').tableToJSON(); // Convert the table into a javascript object
      console.log(table);
      alert(JSON.stringify(table));
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
