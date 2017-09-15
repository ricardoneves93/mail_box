var express = require('express');
var path = require('path');
var basicAuth = require('express-basicauth');
var app = express();
var server = require('http').createServer(app);

app.use(basicAuth({username: 'admin', password: 'password' }));
app.use(express.static(path.join(__dirname, '/public')));

// viewed at http://localhost:8080
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/public/index.html'));
});


server.listen(8090, function () {
  console.log('Example app listening on port 8090!')
})
