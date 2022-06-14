const express = require('express')
const mongoose = require('mongoose')
const app = express()
const cors = require('cors')


let url = "mongodb://bigdata:2022bigdata@54.84.173.222:27017/bigdata"

mongoose.connect(url, {
    authSource: "admin",
    user: "bigdata",
    pass: "2022bigdata"
}).then(()=>{
    console.log("Db connected!")
})


app.use(express.json())
app.use(cors())
app.use('/api', require('./routes/product'))
app.use('/api', require('./routes/category'))
app.use('/api', require('./routes/comment'))
app.use('/api', require('./routes/price'))

app.get('/', (req, res)=>{
    res.send("Hello world")
})

app.listen(3000,'0.0.0.0', () => {
    console.log(`Example app listening at http://localhost:3000`)
  })