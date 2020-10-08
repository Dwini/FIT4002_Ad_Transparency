const express = require('express');
const bodyParser = require('body-parser')
const moment = require('moment-timezone');

const PORT = 8080;
const HOST = '0.0.0.0';

moment.tz.setDefault("Australia/Melbourne");

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json('application/json'));

require('./routes/ads')(app);
require('./routes/bots')(app);
require('./routes/logs')(app);
require('./routes/errors')(app);
require('./routes/search_terms')(app);
require('./routes/bot_scheduler')(app);
require('./routes/heartbeat')(app);

app.listen(PORT, HOST)
console.log(`Running at http://localhost:${PORT}`);
