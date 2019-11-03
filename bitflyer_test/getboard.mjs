var request = require('request');
var crypto = require('crypto');

var API_KEY = require('./key');

const getBitcoinMidPrice = function(){
    var path = '/v1/getboard';
    var query = '';
    var url = 'https://api.bitflyer.com' + path + query;
    request(url, function (err, response, payload) {
        let body = JSON.parse(payload)
        console.log("Mid Price: " + body.mid_price)
    });
}

const getBitcoinLatestPrice = function(){
    var path = '/v1/getticker';
    var query = '';
    var url = 'https://api.bitflyer.com' + path + query;
    request(url, function (err, response, payload) {
        let body = JSON.parse(payload)
        console.log("Latest Price: " + body.ltp)
    });
}

const getBoardState = function(){
    var path = '/v1/getboardstate';
    var query = '';
    var url = 'https://api.bitflyer.com' + path + query;
    request(url, function (err, response, payload) {
        let body = JSON.parse(payload)
        console.log("Health: " + body.health)
        console.log("State: " + body.state)
    });
}

const getBalance = function(){

    var timestamp = Date.now().toString();
    var method = 'GET';
    var path = '/v1/me/getbalance'
    var text = timestamp + method + path;
    var sign = crypto.createHmac('sha256', API_KEY.secret).update(text).digest('hex')

    var options = {
        url: 'https://api.bitflyer.com' + path,
        method: method,
        headers: {
            'ACCESS-KEY': API_KEY.key,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-SIGN': sign
        }
    };

    request(options, function (err, response, payload) {
        let body = JSON.parse(payload)
        console.log("JPY: " + body[0].amount)
        console.log("BTC: " + body[1].amount)
        // console.log(payload)
    });
}

getBalance()

// getBitcoinMidPrice()
// getBitcoinLatestPrice()
// getBoardState()
