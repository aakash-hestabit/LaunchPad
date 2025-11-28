import { Router } from "express";
import { ProductController } from "../controllers/product.controller.js";

const router = Router();

router
  .route("/:id")
  .get(ProductController.getOne)
  .delete(ProductController.delete);

router.route("/").get(ProductController.list);


export default router