const AWS = require('aws-sdk');
const moment = require('moment');
const multer = require('multer');
const fs = require('fs');

const uuidv4 = require('./_uuid');
const { accessKeyId, secretAccessKey, region, bucket,
    DATETIME_FORMAT } = require('../config');

AWS.config.update({ accessKeyId, secretAccessKey, region, bucket });
var docClient = new AWS.DynamoDB.DocumentClient();
var s3 = new AWS.S3();

const upload = multer({ dest: '/tmp/' });

module.exports = app => {
    app.route('/ads')
        .get(function(req, res, next) {     // Fetch all Ads from db
            const params = { TableName: 'Ads' };

            docClient.scan(params, function(err, data) {
                if (err) return next(err);
                res.send(data.Items);
            });
        })
        .post(upload.single('file'), function(req, res, next) {     // Creates a new Ad
            const { file } = req;

            // These are all allowed fields
            const { bot, link, headline, html, base64 } = req.body;

            // These are required fields
            if (!bot || !link || !headline) {
                return res.status(400).send('Missing required field(s)');
            }

            const saveAd = function(params) {
                docClient.put(params, function(err) {
                    if (err) return next(err);
                    res.sendStatus(200);
                });
            };

            var item = { bot, link, headline, html, base64 };
            var dbParams = { TableName: 'Ads' };

            item.id = uuidv4();
            item.datetime = moment(new Date()).format(DATETIME_FORMAT);

            if (!file) {
                return saveAd({ ...dbParams, Item: item });
            }

            var fileExtension = 'png'
            const filePath = file.path,
                s3Params = {
                    Bucket: bucket,
                    Body: fs.createReadStream(filePath),
                    Key: Date.now() + '_' + file.originalname + '.' + fileExtension
                };
            
            s3.upload(s3Params, function(err, data) {
                fs.unlink(filePath, () => {});
                if (err) return next(err);
                
                item.file = data.Location;
                saveAd({ ...dbParams, Item: item });
            })
        });
}