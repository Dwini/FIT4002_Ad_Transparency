const AWS = require('aws-sdk');
const moment = require('moment');

const uuidv4 = require('./_uuid');
const { DATETIME_FORMAT } = require('../config');
const { accessKeyId, secretAccessKey, 
    region } = require('../config').aws;

AWS.config.update({ accessKeyId, secretAccessKey, region });
var docClient = new AWS.DynamoDB.DocumentClient();

module.exports = app => {
    app.route('/logs')
        .get(function(req, res, next) {
            /**
             * Fetch all Logs from db
             */
            const params = { TableName: 'Logs' };

            docClient.scan(params, function(err, data) {
                if (err) return next(err);
                res.send(data.Items);
            });
        })
        .post(function(req, res, next) {    // Creates a new Log of bots actions
            /**
             * Creates a new Log of bots actions
             * @param bot           - Username of bot that performed action
             * @param url           - URL of action
             * @param actions       - Actions that were performed, e.g. 'visit', 'search'
             * @param search_term   - OPTIONAL. If search performed this stores
             *                      the term that was searched
             */

            // Allowed fileds
            const { bot, url, actions, search_term } = req.body; 

            // Required fields
            if (!bot || !url || !actions) { 
                return res.status(400).send('Missing required field(s)');
            }

            const Item = { 
                bot, url, actions, search_term,
                id: uuidv4(),
                datetime: moment(new Date()).format(DATETIME_FORMAT)
            };
            const params = { TableName: 'Logs', Item };

            docClient.put(params, function(err) {
                if (err) return next(err);
                res.sendStatus(200);
            });
        });
}