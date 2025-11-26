import { Router } from "express";
import { demoRoute } from "../controllers/demoRouteController.js";
const router = Router();

router.route("/").get((req, res) => {
  res.status(200).json("the server is running fine");
  res.end();
});
router.route("/demo").get(demoRoute);
router.route("/demo1").get((req,res)=>{
  res.json("demo1 route");
});

export default router;
