const AWS = require('aws-sdk');
const { accessKeyId, secretAccessKey, 
    region } = require('../config').aws;

AWS.config.update({ accessKeyId, secretAccessKey, region });
var docClient = new AWS.DynamoDB.DocumentClient();

module.exports = app => {
    app.route('/errors')
        .get(function(req, res, next) {
            /**
             * Get a list of errors
             */
            var params = { TableName: 'Errors' };

            docClient.scan(params, function(err, data) {
                if (err) return next(err);

                // Sort in order of date (newest first)
                const resp = data.Items.sort((a, b) => {
                    return a.log_file < b.log_file ? 1 : -1;
                });
                res.send(resp);
            })
        })
        .post(function(req, res, next) {
            /** 
             * Creates a new Error
             * @param body.log_file     - Log file of associated session
             * @param body.message      - Message of error that crashed the app
             * @param body.link         - URL of log file
             */
            
            // Allowed fields
            const { log_file, message, link } = req.body;

            // Required fields
            if (!log_file || !message || !link) {
                return res.status(400).send('Missing required field(s)');
            }

            const params = { 
                TableName: 'Errors', 
                Item: { log_file, message, link }
            };
            
            docClient.put(params, function(err) {
                if (err) return next(err);
                res.sendStatus(200);
            });
        });

    app.delete('/error/:log_file', function(req, res, next) {
        /**
         * Delete an error
         * @param param.log_file    - Log file of associated error.
         *      You can get a list of errors and their log files using
         *      the above get route.
         */
        const { log_file } = req.params;
        const params = { TableName: 'Errors', Key: { log_file } };

        docClient.delete(params, function(err) {
            if (err) return next(err);
            res.sendStatus(200);
        });
    });
}