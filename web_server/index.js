var express = require('express');
var path = require('path');
var app = express();
var server = require('http').createServer(app);
app.use(express.static(path.join(__dirname, '/public')));

// viewed at http://localhost:8080
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/public/index.html'));
});


server.listen(8080, function () {
  console.log('Example app listening on port 8080!')
})
