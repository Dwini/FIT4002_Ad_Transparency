const AWS = require('aws-sdk');
const moment = require('moment-timezone');
const multer = require('multer');
const fs = require('fs');

const uuidv4 = require('./_uuid');
const sorter = require('./_sorter');
const filterOptions = require('./_filterOptions');
const { DATETIME_FORMAT } = require('../config')
const { accessKeyId, secretAccessKey, region, 
    bucket } = require('../config').aws;

AWS.config.update({ accessKeyId, secretAccessKey, region });
var docClient = new AWS.DynamoDB.DocumentClient();
var s3 = new AWS.S3();

const upload = multer({ dest: '/tmp/' });

module.exports = app => {
    app.route('/ads')
        .get(function(req, res, next) {
            /** 
             * Fetch all Ads from db.
             * @param query.bot - Username of bot to filter by
             */
            var params = { TableName: 'Ads' };

            const { bot } = req.query;
            if (bot) {
                params = { ...params, ...filterOptions(bot) };
            };

            docClient.scan(params, function(err, data) {
                if (err) return next(err);
                res.send(data.Items.sort(sorter));
            });
        })
        .post(upload.single('file'), function(req, res, next) {
            /**
             * Creates a new Ad
             * @param body.bot       - Username of bot that captured ad
             * @param body.link      - URL of ad
             * @param body.headline  - Title of ad
             * @param body.html      - OPTIONAL. HTML string of ad
             * @param body.base64    - OPTIONAL. Base64 string of picture of ad
             * @param body.file      - OPTIONAL. Picture or any other file
             *      associated with the ad
             */
            const { file } = req;

            // Allowed fields
            const { bot, link, headline, html, base64 } = req.body;

            // Required fields
            if (!bot || !link || !headline) {
                return res.status(400).send('Missing required field(s)');
            }

            const saveAd = function(params) {
                docClient.put(params, function(err) {
                    if (err) return next(err);
                    res.sendStatus(200);
                });
            };

            var dbParams = { TableName: 'Ads' };
            var Item = { 
                bot, link, headline, html, base64,
                id: uuidv4(),
                datetime: moment(new Date()).format(DATETIME_FORMAT)
            };

            if (!file) {
                dbParams.Item = Item
                return saveAd(dbParams);
            }

            const filePath = file.path;
            const s3Params = {
                Bucket: bucket,
                Body: fs.createReadStream(filePath),
                Key: Date.now() + '_' + file.originalname
            };
            
            s3.upload(s3Params, function(err, data) {
                fs.unlink(filePath, () => {});
                if (err) return next(err);
                
                Item.file = data.Location;
                dbParams.Item = Item
                saveAd(dbParams);
            });
        });
}