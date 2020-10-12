const AWS = require('aws-sdk');
const multer = require('multer');
const fs = require('fs');

const { accessKeyId, secretAccessKey, region, 
    bucket, logs_base_url } = require('../config').aws;

AWS.config.update({ accessKeyId, secretAccessKey, region });
var s3 = new AWS.S3();

const upload = multer({ dest: '/tmp/' });

module.exports = app => {
    app.route('/logs')
        .get(function(req, res, next) {
            /**
             * Fetch list of log files from S3
             * @param query.prefix - Prefix of logs to fetch. Currently logs are prefixed with 
             *      name: YYYY.MM.DD_HH.MM.SS. So to find logs from 12/10/2020 set
             *      prefix = 2020.10.12
             * TODO: Only return logs for the given day. 
             * Use ListObjectsV2 with prefix: https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html
             * 
             */

            var params = {
                Bucket: bucket,
                Delimiter: '/',
                Prefix: 'logs/'
            };

            s3.listObjects(params, function(err, data) {
                if (err) return next(err);

                var resp = data.Contents;
                resp.shift();       // First item is just logs directory
                resp = resp.map(elem => {
                    const filename = elem.Key.replace('logs/', '');
                    return {
                        filename,
                        link: logs_base_url + filename
                    };
                });

                res.send(resp);
            });
        })
        .post(upload.single('file'), function(req, res, next) {
            /**
             * Upload log file to S3
             */

            const { file } = req,
                filePath = file.path,
                params = {
                    Bucket: bucket,
                    Body: fs.createReadStream(filePath),
                    Key: 'logs/' + file.originalname
                };

            s3.upload(params, function(err, data) {
                fs.unlink(filePath, () => {});
                if (err) return next(err);
                res.sendStatus(200);
            });
        });
}