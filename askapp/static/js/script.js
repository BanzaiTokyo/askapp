function voteAgainTomorrow(verb, votes_per_day) {
  $('#votes_per_day').text(votes_per_day)
  $('#vote_verb').text(verb)
  $('#voteTomorrow').modal('show')
  return false
}
function alreadyVoted(e) {
  e.preventDefault();
  $('#alreadyVoted').modal('show')
  return false
}
function toggleVoteButtons(data, link) {
    var upvote = link.parent().children('.glyphicon-chevron-up'), downvote = link.parent().children('.glyphicon-chevron-down')
    if (data.can_like_thread)
        upvote.addClass('threadlike').removeClass('voted')
    else
        upvote.removeClass('threadlike').addClass('voted')
    if (data.can_upvote_threads)
        $('.votetomorrow').removeClass('votetomorrow').addClass('threadlike')
    else
        $('.threadlike').removeClass('threadlike').addClass('votetomorrow')
    if (data.can_dislike_thread)
        downvote.addClass('threaddislike').removeClass('voted')
    else
        downvote.removeClass('threaddislike').addClass('voted')
    if (data.can_downvote_threads)
        $('.downvotetomorrow').removeClass('downvotetomorrow').addClass('threaddislike')
    else
        $('.threaddislike').removeClass('threaddislike').addClass('downvotetomorrow')
}
function threadLikeResponse(data, link) {
  toggleVoteButtons(data, link)
}
function threadDislikeResponse(data, link) {
  toggleVoteButtons(data, link)
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
    <span aria-hidden="true">&times</span>\
    </button>\
    <h4 class="modal-title" id="modalLabelSmall">Sorry</h4>\
    </div>\
    <div class="modal-body">\
    You can only <span id="vote_verb"></span>vote on <span id="votes_per_day"></span> articles per day. Please feel free to vote again tomorrow\
    </div>\
    </div>\
    </div>\
    </div>')
}
function alreadyVotedDialog() {
  $('body').append('\
    <div class="modal fade" id="alreadyVoted" tabindex="-1" role="dialog" aria-labelledby="modalLabelSmall" aria-hidden="true">\
    <div class="modal-dialog modal-sm">\
    <div class="modal-content">\
    <div class="modal-header">\
    <button type="button" class="close" data-dismiss="modal" aria-label="Close">\
    <span aria-hidden="true">&times</span>\
    </button>\
    <h4 class="modal-title" id="modalLabelSmall">Sorry</h4>\
    </div>\
    <div class="modal-body">\
    You have already voted on this article\
    </div>\
    </div>\
    </div>\
    </div>')
}
function voteOnThread(e) {
   e.preventDefault()
   link = $(this)
   $.ajax({
    type: "POST",
    url: link.data('href'),
    contentType: "application/json charset=utf-8"
   })
   .done(function(data) {
     link.siblings('.num-points').text(data.points)
     if (link.data('href').indexOf('/thread/') !== -1) {
         if (link.hasClass('threadlike'))
            threadLikeResponse(data, link)
         else
            threadDislikeResponse(data, link)
     }
     else
       postLikeResponse(data)
   })
   return false
}
$(document).ready(function(){
 $(document).on('click', '.btn.threadlike,.btn.threaddislike,.btn.postlike', voteOnThread)
 $(document).on('click', '.votetomorrow', function() {return voteAgainTomorrow('up', level_upvotes)})
 $(document).on('click', '.downvotetomorrow', function() {return voteAgainTomorrow('down', level_downvotes)})
 $(document).on('click', '.voted', alreadyVoted)
 voteDenyDialog()
 alreadyVotedDialog()
})
