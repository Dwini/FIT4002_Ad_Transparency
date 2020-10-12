const AWS = require('aws-sdk');
const moment = require('moment-timezone');
const multer = require('multer');
const fs = require('fs');
const util = require('util');

const { DATETIME_FORMAT } = require('../config')
const { accessKeyId, secretAccessKey, region, 
    bucket } = require('../config').aws;

AWS.config.update({ accessKeyId, secretAccessKey, region });
var docClient = new AWS.DynamoDB.DocumentClient();
var s3 = new AWS.S3();

const upload = multer({ dest: '/tmp/' });
const writeFile = util.promisify(fs.writeFile);

function uuidv4() {
    /**
     * Creates a version 4 UUID
     * Credits: https://stackoverflow.com/a/2117523
     */
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

module.exports = app => {
    app.route('/ads')
        .get(function(req, res, next) {
            /** 
            * Fetch all Ads from db.
            * @param query.date - Date of ads to retrieve. This should be a substring
            *      the format specified as DATETIME_FORMAT in config.js. For example to get
            *      ads for a specific set to: MM-YY or for a specific day use: DD-MM-YYYY
            * @param query.bot - (optional) Username of bot to filter by
            * TODO: Return ads for the given day only.
            * See: https://stackoverflow.com/questions/43793888/how-to-make-search-using-contains-with-dynamodb
            */
            const { bot, date } = req.query;
            
            if (!date) return res.status(400).send('Missing date field');
            
            var FilterExpression = 'contains(#date, :date)',
            ExpressionAttributeNames = { '#date': 'datetime' },
            ExpressionAttributeValues = { ':date': date };
            
            if (bot) {
                FilterExpression += ' AND #b = :b';
                ExpressionAttributeNames = { 
                    ...ExpressionAttributeNames, 
                    '#b': 'bot' 
                };
                ExpressionAttributeValues = { 
                    ...ExpressionAttributeValues, 
                    ':b': bot 
                };
            };
            
            const params = {
                TableName: 'Ads',
                FilterExpression,
                ExpressionAttributeNames,
                ExpressionAttributeValues
            };
            
            docClient.scan(params, function(err, data) {
                if (err) return next(err);

                // Sort in order of date (newest first)
                const resp = data.Items.sort((a, b) => {
                    const aDate = moment(a.datetime, DATETIME_FORMAT).valueOf();
                    const bDate = moment(b.datetime, DATETIME_FORMAT).valueOf();
                    return aDate < bDate ? 1 : -1;
                });
                res.send(resp);
            });
        })
        .post(upload.single('file'), async function(req, res, next) {
            /**
             * Creates a new Ad
             * @param body.bot       - Username of bot that captured ad
             * @param body.link      - URL of ad
             * @param body.headline  - Title of ad
             * @param body.html      - OPTIONAL. HTML string of ad
             * @param body.base64    - OPTIONAL. Base64 string of picture of ad
             * @param body.file      - OPTIONAL. Picture or any other file
             *      associated with the ad
             * TODO: Env var that disables sending to Dynamodb
             */
            const { file } = req;

            // Allowed fields
            const { bot, link, headline, html, base64 } = req.body;

            console.log(req.body);

            // Required fields
            if (!bot || !link || !headline) {
                return res.status(400).send('Missing required field(s)');
            }

            var Item = { 
                bot, link, headline, base64,
                id: uuidv4(),
                datetime: moment(new Date()).format(DATETIME_FORMAT)
            };
            var filename, filepath, s3Params, data;
            
            // Upload html as file if over 100 characters
            if (html.length > 100) {
                filename = Date.now() + '.html';
                filepath = '/tmp/' + filename;
                
                try {
                    await writeFile(filepath, html);
                } catch (err) {
                    return next(err);
                }
                
                s3Params = {
                    Bucket: bucket,
                    Body: fs.createReadStream(filepath),
                    Key: 'html/' + filename
                };

                try {
                    data = await s3.upload(s3Params).promise();
                } catch (err) {
                    fs.unlink(filepath, () => {});
                    return next(err);
                }
                
                fs.unlink(filepath, () => {});
                Item.html = data.Location; 
            } else {
                Item.html = html;
            }
            
            // Upload any file sent with this request
            if (file) {
                filename = Date.now() + '_' + file.originalname;
                filepath = file.path;
                s3Params = {
                    Bucket: bucket,
                    Body: fs.createReadStream(filepath),
                    Key: filename
                };

                try {
                    data = await s3.upload(s3Params).promise();
                } catch (err) {
                    fs.unlink(filepath, () => {});
                    return next(err);
                }

                fs.unlink(filepath, () => {});
                Item.file = data.Location;
            }

            console.log(Item);
            
            const params = { TableName: 'Ads', Item };
            docClient.put(params, function(err) {
                if (err) return next(err);
                res.sendStatus(200);
            });
            
            // if (!file) {
            //     dbParams.Item = Item
            //     return saveAd(dbParams);
            // }
            
            // const filePath = file.path;
            // const s3Params = {
            //     Bucket: bucket,
            //     Body: fs.createReadStream(filePath),
            //     Key: Date.now() + '_' + file.originalname
            // };
            
            // s3.upload(s3Params, function(err, data) {
            //     fs.unlink(filePath, () => {});
            //     if (err) return next(err);
            
            //     Item.file = data.Location;
            //     dbParams.Item = Item
            //     saveAd(dbParams);
            // });
        });
}