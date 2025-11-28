import { ProductService } from "../services/product.service.js";

export class ProductController {
  static async create(req, res, next) {
    try {
      const product = await ProductService.createProduct(req.body);
      res.status(201).json({ success: true, data: product });
    } catch (err) {
      next(err);
    }
  }

  static async getOne(req, res, next) {
    try {
      const product = await ProductService.getProductById(req.params.id, {
        includeDeleted: req.query.includeDeleted === "true",
      });

      res.json({ success: true, data: product });
    } catch (err) {
      next(err);
    }
  }

  static async list(req, res, next) {
    try {
      const products = await ProductService.listProducts(req.query);
      res.json({ success: true, data: products });
    } catch (err) {
      next(err);
    }
  }

  static async update(req, res, next) {
    try {
      const product = await ProductService.updateProduct(
        req.params.id,
        req.body
      );
      res.json({ success: true, data: product });
    } catch (err) {
      next(err);
    }
  }

  static async delete(req, res, next) {
    try {
      const deleted = await ProductService.deleteProduct(req.params.id);
      res.json({
        success: true,
        message: "Product soft-deleted",
        data: deleted,
      });
    } catch (err) {
      next(err);
    }
  }
}
