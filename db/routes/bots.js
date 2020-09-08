const AWS = require('aws-sdk');
const moment = require('moment-timezone');

const { accessKeyId, secretAccessKey, 
    region } = require('../config').aws;

AWS.config.update({ accessKeyId, secretAccessKey, region });
var docClient = new AWS.DynamoDB.DocumentClient();

module.exports = app => {
    /**
     * Get all bots in db
     */
    app.get('/bots', function(req, res, next) {
        const params = { TableName: 'Bots' };

        docClient.scan(params, function(err, data) {
            if (err) return next(err);
            res.send(data.Items);
        });
    });
}