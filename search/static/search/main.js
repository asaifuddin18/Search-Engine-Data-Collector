/* globals Chart:false, feather:false */
document.getElementById('submitAnnotation').addEventListener("click", function() {
    var annotation_string = "";
        var temp = document.getElementById("list-tab");
        var list = temp.getElementsByTagName("li");
        for(var i = 0; i < 10; i++) {
            //alert(list[i].getAttribute("class").toString() == "list-group-item");
            if (list[i].getAttribute("class").toString() == "list-group-item") {
                annotation_string = annotation_string.concat('0');
            } else {
                annotation_string = annotation_string.concat('1');
            }
        }
        document.location.href = document.URL.split('/')[0] + 'edit/' + annotation_string;
        //document.location.href
});
$(function toggleAnnotations(){
  $('.list-group li').click(function(e) {
      e.preventDefault()
      $that = $(this);
      if ($that.hasClass('selected')) {
      $that.removeClass('selected');
      } else {
      $that.addClass('selected');
      }
    
  });
})

    function sendAnnotations(){
        alert('button clicked');
        var annotation_string = "";
        var list = document.getElementById("list-tab");
        for(i = 0; i < 10; i++) {
            if (list[i].hasClass('selected')) {
                annotation_string.append('1');
            } else {
                annotation_string.append('0');
            }
        }
        document.location.href = document.URL + annotation_string;
  }
