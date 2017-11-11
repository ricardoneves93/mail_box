var express = require('express');
var path = require('path');
var basicAuth = require('express-basicauth');
var app = express();
var server = require('http').createServer(app);

var MongoClient = require('mongodb');
var monk = require('monk');


var db = monk('localhost:27017/mail');
const mail_state_collection = 'current_state_collection';
// Make our db accessible to our router
app.use(function(req,res,next){
    req.db = db;
    next();
});

app.use(basicAuth({username: 'admin', password: 'password' }));
app.use(express.static(path.join(__dirname, '/public')));

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/public/index.html'));
});

// returns the current state
app.get('/current_state', function(req, res) {
	var db = req.db;
    var mail_state = db.get(mail_state_collection);
    mail_state.findOne().then((doc) => {
    	console.log(doc);
    	res.setHeader('Content-Type', 'application/json');
    	res.send(JSON.stringify(doc));
    });
});


server.listen(8090, function () {
  console.log('Example app listening on port 8090!')
})
