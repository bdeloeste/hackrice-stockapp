/*
Template Name: Effacy - Creative One Page Template
Author: ThemeBite
Author URI: http://themebite.com/
Version: 1.0
Developed and Designed By: ThemeBite + bits by Bryan Deloeste
*/
var total_cash = 100.00;
var google_price = 0.01;
var microsoft_price = 0.01;
var facebook_price = 0.01;

var google_stocks = 0;
var microsoft_stocks = 0;
var facebook_stocks = 0;

$(document).ready(function() {

    $(".total-cash").text("$ " + total_cash.toFixed(2).toString());

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

        var worth = (google_stocks * google_price) + (microsoft_stocks * microsoft_price) + (facebook_stocks * facebook_price) + total_cash
        $(".worth").text("$ " + ((worth).toFixed(2)).toString());
    });

    $("#google-button").click( function(e) {
            e.preventDefault();
            var googleAmount = parseInt($("#google-amount").val());
            var canPurchase = checkValidPurchase(googleAmount, 'google');
            if (canPurchase) {
                var price = parseFloat(googleAmount * google_price);
                google_stocks += googleAmount;
                total_cash -= price;
                $(".total-cash").text("$ " + total_cash.toFixed(2).toString());
                $(".google-stocks").text(google_stocks);
            }
        }
    );

    $("#google-sell-button").click( function(e) {
            e.preventDefault();
            var googleAmount = parseInt($("#google-amount").val());
            var canSell = checkValidSale(googleAmount, 'google');
            if (canSell) {
                var price = parseFloat(googleAmount * google_price);
                google_stocks -= googleAmount;
                total_cash += price;
                $(".total-cash").text("$ " + total_cash.toFixed(2).toString());
                $(".google-stocks").text(google_stocks);
            }
        }
    );

    $("#microsoft-button").click( function(e) {
            e.preventDefault();
            var microsoftAmount = parseInt($("#microsoft-amount").val());
            var canPurchase = checkValidPurchase(microsoftAmount, 'microsoft');
            if (canPurchase) {
                var price = parseFloat(microsoftAmount * microsoft_price);
                microsoft_stocks += microsoftAmount;
                total_cash -= price;
                $(".total-cash").text("$ " + total_cash.toFixed(2).toString());
                $(".microsoft-stocks").text(microsoft_stocks);
            }
        }
    );

    $("#microsoft-sell-button").click( function(e) {
            e.preventDefault();
            var microsoftAmount = parseInt($("#microsoft-amount").val());
            var canSell = checkValidSale(microsoftAmount, 'microsoft');
            if (canSell) {
                var price = parseFloat(microsoftAmount * microsoft_price);
                microsoft_stocks -= microsoftAmount;
                total_cash += price;
                $(".total-cash").text("$ " + total_cash.toFixed(2).toString());
                $(".microsoft-stocks").text(microsoft_stocks);
            }
        }
    );

    $("#facebook-button").click( function(e) {
            e.preventDefault();
            var facebookAmount = parseInt($("#facebook-amount").val());
            var canPurchase = checkValidPurchase(facebookAmount, 'facebook');
            if (canPurchase) {
                var price = parseFloat(facebookAmount * facebook_price);
                facebook_stocks += facebookAmount;
                total_cash -= price;
                $(".total-cash").text("$ " + total_cash.toFixed(2).toString());
                $(".facebook-stocks").text(facebook_stocks);
            }
        }
    );

    $("#facebook-sell-button").click( function(e) {
            e.preventDefault();
            var facebookAmount = parseInt($("#facebook-amount").val());
            var canSell = checkValidSale(facebookAmount, 'facebook');
            if (canSell) {
                var price = parseFloat(facebookAmount * facebook_price);
                facebook_stocks -= facebookAmount;
                total_cash += price;
                $(".total-cash").text("$ " + total_cash.toFixed(2).toString());
                $(".facebook-stocks").text(facebook_stocks);
            }
        }
    );
});

function checkValidSale(num, company) {
    switch(company) {
        case 'google':
            if (num <= google_stocks) return true;
            return false;
            break;
        case 'microsoft':
            if (num <= microsoft_stocks) return true;
            return false;
            break;
        case 'facebook':
            if (num <= facebook_stocks) return true;
            return false;
            break;
        default:
            console.log("Not a valid company name");
            return false;
            break;
    }
}

function checkValidPurchase(num, company) {
    switch(company) {
        case 'google':
            if (parseFloat(num * google_price) < total_cash) return true;
            return false;
            break;
        case 'microsoft':
            if (num * microsoft_price < total_cash) return true;
            return false;
            break;
        case 'facebook':
            if (num * facebook_price < total_cash) return true;
            return false;
            break;
        default:
            console.log("Not a valid company name");
            return false;
            break;
    }
}
