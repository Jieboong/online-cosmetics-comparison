const express = require('express')
const router = express.Router()
const priceDB = require('../models/PriceDB')

router.get('/price', async (req, res)=>{
    await priceDB.find({"id": "oA000000161650"}).exec().then((product)=>{
        res.send(product)
    })
})


router.get('/price/:id', async (req, res)=>{
    await priceDB.find({"id": req.params.id}).exec().then((product)=>{
       res.send(product)
    })
})




module.exports = router;