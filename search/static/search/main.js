/* globals Chart:false, feather:false */

$(function(){
  console.log('ready');
  
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

