const express = require("express");
const router = express.Router();
const elementController = require("../controllers/element.contoller.js");



router.post("/", elementController.createElement);

router.get("/", elementController.getAllElements);

module.exports = router;
