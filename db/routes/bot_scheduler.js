const { getAllBots } = require('./_shared');

var bots = {};
getAllBots(function(err, data) {
    if (err) {
        throw Error('Failed to fetch bots');
    }
    data.Items.forEach(bot => {
        bots[bot.username] = 'Idle';
    });
});

module.exports = app => {
    app.get('/bot_scheduler/statuses', function(req, res, next) {
        /**
         * Get a list of bots that are not currently running
         */
        res.send(bots);
    });

    app.post('/bot_scheduler/update_status', function(req, res, next) {
        /**
         * Update a bot's status
         * @param body.username - Username of bot
         * @param body.status - Status to set
         */

        // TODO: Validation that status is valid
        const { username, status } = req.body;
        bots[username] = status;
        res.sendStatus(200);
    });
}