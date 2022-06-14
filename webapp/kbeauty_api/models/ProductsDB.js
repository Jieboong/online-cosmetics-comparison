const mongoose = require('mongoose')
require('mongoose-double')(mongoose);
const {Schema}= mongoose;

var SchemaTypes = mongoose.Schema.Types;

const productdbSchema = new Schema({
    _id : SchemaTypes.ObjectId,
	big_category : String,
    brand : String,
    color_options : Map,
    link : String,
    name : String,
    original_price : Number,
    shipping : Array,
    small_category : String,
    date : String,
    discount_price : Number,
    image : String,
    store : String,
    id : String,
    o_id : String,
    discount_percent : SchemaTypes.Decimal128,
    volume : String,
    quantity : String
}, {collection: "cosmetics"})

const productDB = mongoose.model('cosmetics', productdbSchema)

module.exports = productDB