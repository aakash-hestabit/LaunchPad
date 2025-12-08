const Element = require("../models/Element.js");

const createElement = async (content) => {
  const newElement = new Element({ content });
  return await newElement.save();
};

const getAllElements = async () => {
  return await Element.find();
};

module.exports = {
  createElement,
  getAllElements,
};
