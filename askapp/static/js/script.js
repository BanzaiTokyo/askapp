function voteAgainTomorrow() {
  $('#voteTomorrow').modal('show');
  return false
}
function threadLikeResponse(data) {
  if (!data.can_like_thread)
    link.addClass('disabled')
  if (!data.can_upvote_threads) {
    $('.threadlike').off('click').on('click', voteAgainTomorrow)
    voteDenyDialog()
  }
}
function postLikeResponse(data) {
  if (!data.can_like_post)
    link.addClass('disabled')
}
function voteDenyDialog() {
  $('body').append('\
    <div class="modal fade" id="voteTomorrow" tabindex="-1" role="dialog" aria-labelledby="modalLabelSmall" aria-hidden="true">\
    <div class="modal-dialog modal-sm">\
    <div class="modal-content">\
    <div class="modal-header">\
    <button type="button" class="close" data-dismiss="modal" aria-label="Close">\
    <span aria-hidden="true">&times;</span>\
    </button>\
    <h4 class="modal-title" id="modalLabelSmall">Sorry</h4>\
    </div>\
    <div class="modal-body">\
    You can only vote on 3 articles per day. Please feel free to vote again tomorrow\
    </div>\
    </div>\
    </div>\
    </div>');
}
$(document).ready(function(){
  $('.btn.a.threadlike,.btn.a.postlike').on('click', function (e) {
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
 $('.votetomorrow').on('click', voteAgainTomorrow)
 if ($('.votetomorrow').length)
   voteDenyDialog()
});
