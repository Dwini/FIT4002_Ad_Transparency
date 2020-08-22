const express = require('express');
const bodyParser = require('body-parser')

const PORT = 8080;
const HOST = '0.0.0.0';

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use('/', express.static('public'));

require('./routes/ads')(app);
require('./routes/bots')(app);
require('./routes/logs')(app);
require('./routes/search_terms')(app);

app.listen(PORT, HOST)
console.log(`Running at http://${HOST}:${PORT}`);