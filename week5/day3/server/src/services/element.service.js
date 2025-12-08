const elementRepository = require("../repositories/element.repository.js");

const addElement = async (content) => {
  if (!content) {
    throw new Error("Content is required");
  }
  return await elementRepository.createElement(content);
};

const getAllElements = async () => {
  return await elementRepository.getAllElements();
};
module.exports = {
  addElement,
  getAllElements,
};
