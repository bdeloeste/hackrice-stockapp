/*
Template Name: Effacy - Creative One Page Template
Author: ThemeBite
Author URI: http://themebite.com/
Version: 1.0
Developed and Designed By: ThemeBite + bits by Bryan Deloeste
*/
$(document).ready(function() {
    var pusher = new Pusher('b87e84a0194862d39bdd', {
      encrypted: true
    });
    var channel = pusher.subscribe('test_channel');
    channel.bind('my_event', function(data) {
      $(".google-price").text(data.message);
      console.log(data.message);
    });
});
