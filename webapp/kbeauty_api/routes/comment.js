const express = require('express')
const router = express.Router()
const commentDB = require('../models/CommentDB')

router.get('/comments', async (req, res)=>{
    await commentDB.find().exec().then((product)=>{
        res.send(product)
    })
})

router.get('/comment/:name', async (req, res)=>{
    await commentDB.find({'big_category': req.params.name}).exec().then((product)=>{
        res.send(product)
    })
})






module.exports = router;