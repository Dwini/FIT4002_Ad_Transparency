const moment = require('moment');
const { DATETIME_FORMAT } = require('../config')

/**
 * Given 2 database items, sorts them in 
 * order of newest to oldest
 */
module.exports = function(a, b) {
    const aDate = moment(a.datetime, DATETIME_FORMAT).valueOf();
    const bDate = moment(b.datetime, DATETIME_FORMAT).valueOf();
    return aDate < bDate ? 1 : -1
}