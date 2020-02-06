$(document).ready(function() {
    var el = $('#new_logo');
    el.addClass('animation');
    setTimeout(function() {
        el.removeClass('animation');
    }, 1000);
        
$('#new_logo').on('mouseenter click', function() {
    var el = $(this);
    el.addClass('animation');
    setTimeout(function() {
        el.removeClass('animation');
   }, 1000);
   })
});