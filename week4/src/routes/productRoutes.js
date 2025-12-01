import { Router } from "express";
import { ProductController } from "../controllers/product.controller.js";
import { validateProduct } from "../middlewares/validate.js";

const router = Router();

router
  .route("/:id")
  .get(ProductController.getOne)
  .delete(ProductController.delete);

router.route("/").get(ProductController.list).post(validateProduct,ProductController.create)

export default router;
