const express = require('express')
const router = express.Router()
const categoryDB = require('../models/CategoryDB')
const productDB = require('../models/ProductsDB')

router.get('/category', async (req, res)=>{
    await categoryDB.findOne().exec().then((product)=>{
        res.send(product.data)
    })
})


router.get('/category/:name', async (req, res)=>{
    await productDB.find({'big_category': req.params.name}).limit(3000).exec().then((product)=>{
        res.send(product)
    })
})





module.exports = router;