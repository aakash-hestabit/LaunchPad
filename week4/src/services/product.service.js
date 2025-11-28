import { ProductRepository } from "../repositories/product.repository.js";
import ApiError from "../utils/apiError.js";
import { buildProductQuery } from "../utils/query-engine.js";

export class ProductService {
  static async createProduct(payload) {
    return await ProductRepository.create(payload);
  }

  static async getProductById(id, { includeDeleted = false } = {}) {
    const product = await ProductRepository.findById(id);

    if (!product || (!includeDeleted && product.deletedAt)) {
      throw new ApiError("Product not found", 404, "PRODUCT_NOT_FOUND");
    }

    return product;
  }

  static async updateProduct(id, data) {
    const updated = await ProductRepository.update(id, data);

    if (!updated) {
      throw new ApiError("Product not found", 404, "PRODUCT_NOT_FOUND");
    }

    return updated;
  }

  static async deleteProduct(id) {
    const deleted = await ProductRepository.delete(id);

    if (!deleted) {
      throw new ApiError(
        "Product not found or already deleted",
        404,
        "PRODUCT_NOT_FOUND"
      );
    }

    return deleted;
  }

  static async listProducts(query) {
    const {
      page = 1,
      limit = 10,
      sort = "createdAt:desc",
      cursor,
      includeDeleted = false,
    } = query;

    const { filter, sortQuery } = buildProductQuery(query, includeDeleted);
    console.log(includeDeleted);

    if (cursor) {
      return ProductRepository.findPaginatedCursor({
        cursor,
        limit,
        filter,
        sort: sortQuery,
      });
    }

    return ProductRepository.findPaginated({
      page,
      limit,
      filter,
      sort: sortQuery,
    });
  }
}
