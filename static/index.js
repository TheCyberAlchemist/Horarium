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
            pk = select.attr("pk");
        }
    }).disableSelection();
    const newLocal = ".droppable";
    $( newLocal ).droppable({
        drop: function( event, ui ) {
        let obj = $( this );
        obj.html(name)
        obj.css({"background-color":color})
        obj.attr({"name":name ,"color":color,"event_link":event_link,"pk":pk});
        // making cells clickable
        // obj.click(function(){open(event_link);});
        }
    });
    let a;
    $('.save').click(function(){
      var table = $('.main_table').tableToJSON(
      {
        extractor : function(cellIndex, $cell) {
            if(cellIndex == '0' ){
                a = $cell.find('p').html().trim();
                p = $cell.attr('pk');
                return {
                  // name: $cell.find('span').text(),
                  time:a,
                  time_pk:p,
                };
            }
            else{
                return {
                    name: $cell.text().trim(),
                    event_pk: $cell.attr('pk'),
                    time_pk: p,
                    day: $cell.attr('day'),
                    //   time:a,
                };
            }
        }
      }); // Convert the table into a javascript object
      let state = JSON.stringify(table);
      console.log(state);
      // alert(state);
      $.ajax({
          type: "post",
          data: state,
          url: ""
      });
    });
});
