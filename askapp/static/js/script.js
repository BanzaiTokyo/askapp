function voteAgainTomorrow() {
  alert('You can only vote on 3 articles per day. Please feel free to vote again tomorrow')
  return false
}
function threadLikeResponse(data) {
  if (!data.can_like_thread)
    link.addClass('disabled')
  if (!data.can_upvote_threads)
      $('.threadlike').off('click').on('click', voteAgainTomorrow)
}
function postLikeResponse(data) {
  if (!data.can_like_post)
    link.addClass('disabled')
}
$(document).ready(function(){
  $('.btn.a').on('click', function (e) {
   e.preventDefault();
   link = $(this);
   $.ajax({
    type: "POST",
    url: link.attr('href'),
    contentType: "application/json; charset=utf-8"
   })
   .done(function(data) {
     link.siblings('.num-points').text(data.points)
     if (link.attr('href').indexOf('/thread/') !== -1)
       threadLikeResponse(data)
     else
       postLikeResponse(data)
   });
   return false;
 });
});
