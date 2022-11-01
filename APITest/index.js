const res = require('express/lib/response');

const express = require('express');
const app = express();
const PORT = 8080;
const http = require("http");
const hostname = "192.168.1.7"; // change to your ipv4 address for testing, run "ipconfig" in cmd to find it

// const server = http.createServer(function(req, res){});

// server.listen(PORT, hostname, function(error){
//     if (error) {
//         console.log("error ", error)
//     } else {
//         console .log("server is running")
//     }
// });

Mode = "idle";
ButtonPress = "";

app.use(express.json());

app.get('/tshirt', (req, res) => {
    res.status(200).send({
        tshirt: '👕',
        size: 'large'
    })
});

app.post('/tshirt/:id', (req, res) => {

    const { id } = req.params;
    const { logo } = req.body;

    if (!logo) {
        res.status(418).send({ message: 'We need a logo!' })
    }

    res.send({
        tshirt: `👕 with your ${logo} and ID of ${id}`,
    });
});

app.get('/MovementMode', (req, res) => {
    res.send({Mode})
});

app.get('/ChangeMoveMode/:NewMode', (req, res) => {
    Mode = req.params.NewMode;
    res.send({Mode});
});

app.get('/ButtonPress/:button', (req, res) => {
    ButtonPress = req.params.button;
    console.log({ButtonPress})
});

app.get('/GetButton', (req, res) => {
    res.send({ButtonPress});
});

app.get('/MovmentPress/:movement', (req, res) => {
    MovementPress = req.params.movement;
    console.log({MovementPress})
});

app.get('/GetMovement', (req, res) => {
    res.send(MovementPress);
});

app.listen(
    PORT, hostname,
    () => console.log(`it's alive on http://${hostname}:${PORT}`)
)