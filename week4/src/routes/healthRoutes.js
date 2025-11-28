import { Router } from "express";
import { demoRoute } from "../controllers/demoRoute.controller.js";
const router = Router();

router.route("/").get((req, res, next) => {
  try {
    throw new Error("this is a intended error at health route");
  } catch (e) {
    next(e);
  }
});
router.route("/demo").get(demoRoute);
router.route("/demo1").get((req, res) => {
  res.json("demo1 route");
});

export default router;
