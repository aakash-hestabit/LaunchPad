import { Product } from "../models/Product.js";
import mongoose from "mongoose";

export class ProductRepository {
  static async create(payload) {
    try {
      const product = new Product(payload);
      await product.save();
      return product.toObject();
    } catch (err) {
      console.error("ProductRepository.create Error:", err);
      throw err;
    }
  }

  static async findById(id, options = {}) {
    if (!mongoose.isValidObjectId(id)) return null;

    return Product.findById(id)
      .select(options.select || "")
      .populate(options.populate || "")
      .lean();
  }

  static async update(id, updateData, options = { new: true }) {
    if (!mongoose.isValidObjectId(id)) return null;

    return Product.findByIdAndUpdate(id, updateData, {
      new: options.new,
      runValidators: true,
    });
  }

  static async delete(id) {
    if (!mongoose.isValidObjectId(id)) return null;

    return Product.findOneAndDelete({ _id: id });
  }

  static async findPaginated({ page = 1, limit = 10, filter = {}, sort = {} }) {
    const skip = (page - 1) * limit;

    const [items, total] = await Promise.all([
      Product.find(filter).sort(sort).skip(skip).limit(limit),
      Product.countDocuments(filter),
    ]);

    return {
      items,
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    };
  }

  static async findPaginatedCursor({
    cursor = null,
    limit = 10,
    filter = {},
    sort = { _id: 1 },
  }) {
    const query = { ...filter };

    if (cursor) {
      query._id = { $gt: cursor };
    }

    const items = await Product.find(query).sort(sort).limit(limit);

    return {
      items,
      nextCursor: items.length ? items[items.length - 1]._id : null,
      limit,
    };
  }
}
