import { userValidationSchema } from '../validators/userValidationSchema.js'
import {productValidationSchema} from '../validators/productValidationSchema.js'

export const validateUser = (req, res, next) => {
  try {
    userValidationSchema.parse(req.body);
    next();
  } catch (error) {
    next(error);
  }
};

export const validateProduct = (req, res, next) => {
  try {
    productValidationSchema.parse(req.body);
    next();
  } catch (error) {
    next(error);
  }
};
