$(function(){
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
    $( ".droppable" ).droppable({
        drop: function( event, ui ) {
        let obj = $( this );
        obj.html(name)
        obj.css({"background-color":color})
        obj.attr({"name":name ,"color":color,"event_link":event_link});
        let s = obj.serialize()
        // obj.click(function() {
        //   open(event_link);
        // });
        console.log(s);
        }
    });
});