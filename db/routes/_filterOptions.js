/**
 * Adds filtering for Dynamodb queries
 */
module.exports = function(bot) {
    return {
        FilterExpression: '#b = :b',
        ExpressionAttributeNames: { '#b': 'bot' },
        ExpressionAttributeValues: { ':b': bot }
    };
}