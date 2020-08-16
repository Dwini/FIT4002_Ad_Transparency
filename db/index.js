const express = require('express');
const bodyParser = require('body-parser')

const PORT = 8080;
const HOST = '0.0.0.0';

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));

require('./routes')(app);

app.listen(PORT, HOST)
console.log(`Running on http://${HOST}:${PORT}`);