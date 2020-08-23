module.exports = app => {
    app.get('/heartbeat', function(req, res, next) {
      res.json({
        'running': true,
      })
    });
}
