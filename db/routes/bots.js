const AWS = require('aws-sdk');
const moment = require('moment');

const { accessKeyId, secretAccessKey, region } = require('../config');

AWS.config.update({ accessKeyId, secretAccessKey, region });
var docClient = new AWS.DynamoDB.DocumentClient();

module.exports = app => {
    app.get('/bots', function(req, res, next) {
        const params = { TableName: 'Bots' };

        docClient.scan(params, function(err, data) {
            if (err) return next(err);
            res.send(data.Items);
        });
    });
}