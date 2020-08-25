const AWS = require('aws-sdk');
const moment = require('moment');
const uuidv4 = require('./_uuid');

const { accessKeyId, secretAccessKey, region, bucket, 
    DATETIME_FORMAT } = require('../config');

AWS.config.update({ accessKeyId, secretAccessKey, region });
var docClient = new AWS.DynamoDB.DocumentClient();

module.exports = app => {
    app.route('/logs')
        .get(function(req, res, next) {     // Fetch all Logs from db
            const params = { TableName: 'Logs' };

            docClient.scan(params, function(err, data) {
                if (err) return next(err);
                res.send(data.Items);
            });
        })
        .post(function(req, res, next) {    // Creates a new Log of bots actions
            // These are all allowed fields
            const { bot, url, actions, search_term } = req.body;

            // These are required fields
            if (!bot || !url || !actions) {
                return res.status(400).send('Missing required field(s)');
            }

            const item = { bot, url, actions, search_term };
            item.id = uuidv4();
            item.datetime = moment(new Date()).format(DATETIME_FORMAT);

            const params = { TableName: 'Logs', Item: item };

            docClient.put(params, function(err) {
                if (err) return next(err);
                res.sendStatus(200);
            });
        });
}