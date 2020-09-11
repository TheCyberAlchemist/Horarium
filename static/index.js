$(function(){
////////////// ajax setup   /////////////////////////
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
///////////////////////////////////////////////////////
////////////// draggable    /////////////////////////

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
///////////////////////////////////////////////////////
////////////// dropable    /////////////////////////

    const newLocal = ".droppable";
    $( newLocal ).droppable({
        drop: function( event, ui ) {
        let td = $( this );
        let div = td.find("div");   // get child div of td
        // td.html(name)
        // td.css({"background-color":color})
        td.attr({"name":name ,"color":color,"event_link":event_link,"pk":pk}); //set attirbute of td 
        div.html(name)
        div.css({"background-color":color})
        // making cells clickable
        // obj.click(function(){open(event_link);});
        }
    });
///////////////////////////////////////////////////////
////////////// save click     /////////////////////////
    $('.save').click(function(){
        let text;
      var table = $('.main_table').tableToJSON(// calling tableToJSON
      {
        extractor : function(cellIndex, $cell) {
            if(cellIndex == '0' ){// if it is t-heading
                text = $cell.find('p').html().trim();
                p = $cell.attr('pk');// get attribute period primary key
                return {
                  // name: $cell.find('span').text(),
                  time:text,
                  time_pk:p,
                };
            }
            else{
                return {
                    name: $cell.text().trim(),
                    event_pk: $cell.attr('pk'),// set attribute period primary key
                    time_pk: p,
                    day: $cell.attr('day'),// set attribute day
                };
            }
        }
      }); // Convert the table into a javascript object
      let state = JSON.stringify(table); // final JSON to be passed through ajax
      console.log(state);
      // alert(state);
      $.ajax({
          type: "post",
          data: state,
          url: ""
      });
    });
});
