const AWS = require('aws-sdk');

const { accessKeyId, secretAccessKey, 
    region } = require('../config').aws;
const { getAllBots } = require('./_shared');

AWS.config.update({ accessKeyId, secretAccessKey, region });
var docClient = new AWS.DynamoDB.DocumentClient();

module.exports = app => {
    app.get('/bots', function(req, res, next) {
        /** Get all bots in db */
        const callback = function(err, data) {
            if (err) return next(err);
            res.send(data.Items);
        };
        getAllBots(callback);
    });

    app.route('/bot/:username')
        .get(function(req, res, next) { 
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
        .post(function(req, res, next) {
            /**
             * Create or update a bot
             * @param params.username - Username of bot to create/update
             * @param body.password - (string)
             * @param body.name - (array of strings)
             * @param body.DOB - (string, format: DD-MM-YYYY)
             * @param body.gender - (string)
             * @param body.political_ranking - (integer)
             * @param body.other_terms_category - (integer)
             * @param body.location - (dictionary, needs to have 'latitude' and 'longitude' key/values)
             */

            const { username } = req.params;
            const { password, name, DOB, gender, political_ranking, 
                other_terms_category, location } = req.body;

            if (!username || !password || !name || !DOB || 
                !gender || !location || political_ranking == null || 
                other_terms_category == null) {
                return res.status(400).send('Missing required field(s)');
            }

            if (location.latitude == null || location.longitude == null) {
                return res.status(400).send('Location is invalid');
            }

            const Item = { username, password, name, DOB, gender, 
                political_ranking, other_terms_category, location };
            const params = { TableName: 'Bots', Item };

            docClient.put(params, function(err) {
                if (err) return next(err);
                res.sendStatus(200);
            });
        });
}