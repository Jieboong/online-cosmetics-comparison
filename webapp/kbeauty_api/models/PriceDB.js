const mongoose = require('mongoose')
require('mongoose-double')(mongoose);
const {Schema}= mongoose;

var SchemaTypes = mongoose.Schema.Types;

const pricedbSchema = new Schema({
    _id : SchemaTypes.ObjectId,
	id: String,
    data: String,
    discount_price: Number,
    store: String
}, {collection: "price"})

const priceDB = mongoose.model('price', pricedbSchema)

module.exports = priceDB