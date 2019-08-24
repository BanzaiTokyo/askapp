$(document).ready(function(){
  $('.btn.a').on('click', function (e) {
   e.preventDefault();
   link = $(this);
   $.ajax({
    type: "GET",
    url: link.attr('href'),
    contentType: "application/json; charset=utf-8"
   })
   .done(function(data) {
     link.siblings('.num-points').text(data.points)
   });
   return false;
 });
});
