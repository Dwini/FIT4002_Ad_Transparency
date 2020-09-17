const AWS = require('aws-sdk');
const moment = require('moment-timezone');

const { accessKeyId, secretAccessKey, 
    region } = require('../config').aws;

AWS.config.update({ accessKeyId, secretAccessKey, region });
var docClient = new AWS.DynamoDB.DocumentClient();

module.exports = app => {
    app.get('/bots', function(req, res, next) {
        /** Get all bots in db */
        const params = { TableName: 'Bots' };

        docClient.scan(params, function(err, data) {
            if (err) return next(err);
            res.send(data.Items);
        });
    });

    app.get('/bot/:username', function(req, res, next) { 
        /**
         * Get single bot details
         * @param params.username - Username of bot to get deatils of
         */
        const { username } = req.params,
            params = {
                TableName: 'Bots',
                Key: { username }
            };
        
        docClient.get(params, function(err, data) {
            if (err) return next(err);
            res.send(data.Item);
        });
    })
}