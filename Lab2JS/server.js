const express = require('express')
const userAgent = require('express-useragent')
const ip = require("ip");
const app = express()
const port = 3000
const bodyParser = require('body-parser');
const fs = require('fs')
app.use(bodyParser.json());
app.use(userAgent.express());

app.use('/static', express.static('static'))

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/passwordGenerator.html')
})

app.post('/downloadPassword', (req, res) => {
    let password = req.body.password;   
    let userAgent = JSON.stringify(req.useragent);     
    let userIP = ip.address();                      
    fs.appendFileSync('passwords.txt', "IP: " + userIP + "; " + userAgent + ": " + password + "\n");
    res.json({ message:'Пароль сохранен.'});
});

app.listen(port, () => {
    console.log('Сервер был развёрнут. Порт: ' + port)
})