const AWS = require('aws-sdk');
const moment = require('moment');

const { accessKeyId, secretAccessKey, region, bucket, 
    DATETIME_FORMAT } = require('./config');

AWS.config.update({ accessKeyId, secretAccessKey, region });
// var dynamodb = new AWS.DynamoDB();
var docClient = new AWS.DynamoDB.DocumentClient();
var s3 = new AWS.S3();

// Credits: https://stackoverflow.com/a/2117523
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

module.exports = app => {
    app.get('/bots', function(req, res, next) {
        const params = { TableName: 'Bots' };

        docClient.scan(params, function(err, data) {
            if (err) return next(err);
            res.send(data.Items);
        });
    });

    app.route('/ads')
        .get(function(req, res, next) {
            // Get all Ads from db
            const params = { TableName: 'Ads' };

            docClient.scan(params, function(err, data) {
                if (err) return next(err);
                res.send(data.Items);
            });
        })
        .post(function(req, res, next) {
            // Create new Ad
            const { bot, link, headline, html, file_id, base64 } = req.body;

            // Check all required values given
            if (!bot || !link || !headline) {
                return res.status(400).send('Missing required field');
            }

            const item = { bot, link, headline, html, file_id, base64 };
            item.id = uuidv4();
            item.datetime = moment(new Date()).format(DATETIME_FORMAT);

            const params = { TableName: 'Ads', Item: item };

            docClient.put(params, function(err) {
                if (err) return next(err);
                res.sendStatus(200);
            });
        });

    app.route('/logs')
        .get(function(req, res, next) {
            // Get all Logs from db
            const params = { TableName: 'Logs' };

            docClient.scan(params, function(err, data) {
                if (err) return next(err);
                res.send(data.Items);
            });
        })
        .post(function(req, res, next) {
            // Create new Log
            const { bot, url, actions, search_term } = req.body;

            // Check all required values given
            if (!bot || !url || !actions) {
                return res.sendStatus(400);
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