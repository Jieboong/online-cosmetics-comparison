const mongoose = require('mongoose')
require('mongoose-double')(mongoose);
const {Schema}= mongoose;

var SchemaTypes = mongoose.Schema.Types;

const categorydbSchema = new Schema({
    _id : String,
	data: Array
})

const categoryDB = mongoose.model('category', categorydbSchema)

module.exports = categoryDB
