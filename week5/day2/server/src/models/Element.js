const mongoose = require('mongoose');

const elementSchema = new mongoose.Schema({
  content: {
    type: String,
    required: true,
    trim: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

const Element = mongoose.model('Element', elementSchema);

module.exports = Element;
