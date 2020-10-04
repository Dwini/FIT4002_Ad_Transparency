const AWS = require('aws-sdk');

const { accessKeyId, secretAccessKey, 
    region } = require('../config').aws;

AWS.config.update({ accessKeyId, secretAccessKey, region });
var docClient = new AWS.DynamoDB.DocumentClient();

module.exports = {
    getAllBots: function(callback) {
        const params = { TableName: 'Bots' };
        docClient.scan(params, callback);
    }
} 