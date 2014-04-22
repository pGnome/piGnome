var twilio = require('twilio');
twilio.initialize('ACfb95b68c67b1c421fb351e537fd09421', '6d3a13db188b7d2603b8bfbf75c59f41');

// Include Cloud Code module dependencies
Parse.Cloud.define("sendSMS", function(request, response) {

    var threshold = 20;
    var isSent = false;
    var WaterLevel = Parse.Object.extend("Barrel");
    var query = new Parse.Query(WaterLevel);
    query.descending("createdAt").limit(1);
    query.find({
        success: function(results) {
            currentLevel = results[0].get("level");
            if (currentLevel < threshold-5 && !isSent){
                // Send an SMS message
                twilio.sendSMS({
                    to: +16177635155,
                    from: +18572541957,
                    body: 'Please fill the rain barrel with enough water'
                }, {
                    success: function(httpResponse) {
                        response.success("SMS sent!");
                        isSent = true;
                    },
                    error: function(httpResponse) {
                        response.error("Uh oh, something went wrong");
                    }
                });
            }
            else if (currentLevel > threshold+5){
                isSent = false;
            }
        },
        error: function(error) {
            alert("Error: " + error.code + " " + error.message);
        }
    });
    


});