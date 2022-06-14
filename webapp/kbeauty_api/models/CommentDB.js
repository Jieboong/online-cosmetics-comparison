const mongoose = require('mongoose')
require('mongoose-double')(mongoose);
const {Schema}= mongoose;

var SchemaTypes = mongoose.Schema.Types;

const commentDBSchema = new Schema({
    _id : SchemaTypes.ObjectId,
	name : String,
    id : String,
    token : Array 
}, {collection: 'comments'})

const commentDB = mongoose.model('comments', commentDBSchema)

module.exports = commentDB