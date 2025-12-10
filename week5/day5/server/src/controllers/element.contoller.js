const elementService = require("../services/element.service.js");

const createElement = async (req, res) => {
  try {
    const { content } = req.body;
    const newElement = await elementService.addElement(content);
    res.status(201).json(newElement);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

const getAllElements = async (req, res) => {
  try {
    const elements = await elementService.getAllElements();
    res.status(200).json(elements);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  createElement,
  getAllElements,
};
