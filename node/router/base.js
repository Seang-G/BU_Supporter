module.exports = function(app) {

    app.get('/hello', function(req, res) {
        res.send('Hello World');
    });
    app.get('/about', function(req, res) {
        res.send('About us');
    });

}