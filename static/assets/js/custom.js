(function ($) {
    "use strict";
    var mainApp = {

        main_fun: function () {
            var updateClock = function() {
                var date = new Date();
                $("#clock").text(("0"+date.getHours()).slice(-2)+":"+("0"+date.getMinutes()).slice(-2));
            };
            updateClock();
            setInterval(function(){
                updateClock();
            },1000);

        },

        initialization: function () {
            mainApp.main_fun();

        }

    };

    $(document).ready(function () {
        mainApp.main_fun();
    });

}(jQuery));
