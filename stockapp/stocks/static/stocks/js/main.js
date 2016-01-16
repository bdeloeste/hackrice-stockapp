/*
Template Name: Effacy - Creative One Page Template
Author: ThemeBite
Author URI: http://themebite.com/
Version: 1.0
Developed and Designed By: ThemeBite + bits by Bryan Deloeste
*/
$(document).ready(function() {

    var google_price = 0.00;
    var microsoft_price = 0.00;
    var facebook_price = 0.00;

    var pusher = new Pusher('b87e84a0194862d39bdd', {
      encrypted: true
    });
    var channel = pusher.subscribe('test_channel');
    channel.bind('my_event', function(data) {
    console.log(data);
    if (google_price + data.google >= 0) google_price += data.google;
    if (microsoft_price + data.microsoft >= 0) microsoft_price += data.microsoft;
    if (facebook_price + + data.facebook >= 0) facebook_price += data.facebook;

     $(".google-price").text("$ " + ((google_price).toFixed(2)).toString());
     $(".microsoft-price").text("$ " + ((microsoft_price).toFixed(2)).toString());
     $(".facebook-price").text("$ " + ((facebook_price).toFixed(2)).toString());
    });
});
