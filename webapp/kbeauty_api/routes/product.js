const express = require('express')
const router = express.Router()
const productDB = require('../models/ProductsDB')

router.get('/products/', async (req, res)=>{
    await productDB.find().limit(3000).exec().then((product)=>{
        console.log(product.length)
        res.send(product)
    })
})


router.get('/products/:id', async (req, res)=>{
    await productDB.find({"id": req.params.id}).exec().then((product)=>{
        res.send(product)
    })
})

router.get('/detail/:id', async (req, res)=>{
    await productDB.findOne({"id": req.params.id}).exec().then((product)=>{
       res.send(product)
    })
})




module.exports = router;