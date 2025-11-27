import { User } from "../models/User.js";
import mongoose from "mongoose";

export class UserRepository {
  static async create(payload) {
    try {
      const user = new User(payload);
      await user.save();
      return user.toObject();
    } catch (err) {
      console.error("UserRepository.create Error:", err);
      throw err;
    }
  }

  static async findById(id, options = {}) {
    if (!mongoose.isValidObjectId(id)) return null;

    return User.findById(id)
      .select(options.select || "")
      .populate(options.populate || "")
      .lean();
  }

  static async update(id, updateData, options = { new: true }) {
    if (!mongoose.isValidObjectId(id)) return null;

    return User.findByIdAndUpdate(id, updateData, {
      new: options.new,
      runValidators: true,
    });
  }

  static async delete(id) {
    if (!mongoose.isValidObjectId(id)) return null;

    return User.findOneAndDelete({ _id: id });
  }

  static async findPaginated({ page = 1, limit = 10, filter = {}, sort = {} }) {
    const skip = (page - 1) * limit;

    const [items, total] = await Promise.all([
      User.find(filter).sort(sort).skip(skip).limit(limit).lean().exec(),
      User.countDocuments(filter),
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

    const items = await User.find(query).sort(sort).limit(limit).lean();

    return {
      items,
      nextCursor: items.length ? items[items.length - 1]._id : null,
      limit,
    };
  }
}
