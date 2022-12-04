module.exports = function(app, fs, request) {
    app.get('/getData', function(req, res) {
        
        let url = `https://fastapi-bu-usuyk.run.goorm.io/info/${req.query.id}`;
        const options = {
            uri: url,
            qs:{
                info_pwd:req.query.pw
            }
        }

        request.get(options, (error, response, body)=>{
            if (!error && response.statusCode == 200) {
                res.send(body);
            } else {
                res.status(response.satausCode).end();
                console.log("error = " + response.statusCode);
            }
        })

        // fetch(url)
        // .then((response)=>{
        // return response.json();
        // })
        // .then((data)=>{
        // console.log(data);
        // res.send(data);
        // })
        // .catch((err)=>{
        // console.log(err);
        // })
    })
}