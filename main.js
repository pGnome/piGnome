var twilio = require('twilio');
twilio.initialize('ACfb95b68c67b1c421fb351e537fd09421', '6d3a13db188b7d2603b8bfbf75c59f41');

// Include Cloud Code module dependencies
Parse.Cloud.define("sendSMS", function(request, response) {


    var WaterLevel = Parse.Object.extend("Barrel");
    var query = new Parse.Query(WaterLevel);
    query.descending("createdAt").limit(1);
    query.find({
        success: function(object) {
            // Successfully retrieved the object.
        },
        error: function(error) {
            alert("Error: " + error.code + " " + error.message);
        }
    });
    
    // Send an SMS message
    twilio.sendSMS({
        to: +16177635155,
        from: request.params.To,
        body: 'Please fill the rain barrel with enough water'
    }, {
        success: function(httpResponse) {
            response.success("SMS sent!");
        },
        error: function(httpResponse) {
            response.error("Uh oh, something went wrong");
        }
    });

});