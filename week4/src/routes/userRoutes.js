import { Router } from "express";
import { validateUser } from "../middlewares/validate.js";
import { UserController } from "../controllers/user.controller.js";
const router = Router();

router.route("/").post(validateUser, UserController.create);

export default router;
