import mongoose, { Schema } from "mongoose";
import bcrypt from "bcrypt";

const addressSchema = new Schema(
  {
    street: { type: String, required: true, trim: true },
    city: { type: String, required: true, trim: true },
    state: { type: String, trim: true },
    postalCode: {
      type: String,
      required: true,
      trim: true,
    },
    country: { type: String, required: true, trim: true },
  },
  { _id: false }
);

const cartItemSchema = new Schema(
  {
    productId: { type: Schema.Types.ObjectId, ref: "Product", required: true },
    quantity: { type: Number, default: 1, min: 1 },
    price: { type: Number, required: true },
  },
  { _id: false }
);

const userSchema = new Schema(
  {
    username: {
      type: String,
      required: true,
      lowercase: true,
      unique: true,
      index: true,
      trim: true,
    },

    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      trim: true,
      match: [/^\S+@\S+\.\S+$/, "Invalid email format"],
    },

    firstname: { type: String, required: true, trim: true },
    lastname: { type: String, trim: true },

    role: {
      type: String,
      enum: ["user", "seller", "admin"],
      default: "user",
    },

    products: [
      {
        type: Schema.Types.ObjectId,
        ref: "Product",
      },
    ],

    addresses: [addressSchema],
    cart: [cartItemSchema],

    password: {
      type: String,
      required: true,
      minlength: 6,
    },

    refreshToken: {
      type: String,
    },
    refreshTokenExpiresAt: {
      type: Date,
      expiresAfterSeconds: 60 * 60 * 24 * 7,
      index: true,
      default: null,
    },
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
    versionKey: false,
  }
);

userSchema.pre("save", async function (next) {
  if (!this.isModified("password")) return next();
  this.password = await bcrypt.hash(this.password, 10);
});

userSchema.methods.isPasswordCorrect = async function (password) {
  return bcrypt.compare(password, this.password);
};

userSchema.virtual("fullName").get(function () {
  return `${this.firstname} ${this.lastname || ""}`.trim();
});

userSchema.virtual("cartTotal").get(function () {
  return (
    this.cart?.reduce((sum, item) => sum + item.price * item.quantity, 0) || 0
  );
});

userSchema.index({ email: 1, username: 1 });

userSchema.index({ role: 1, createdAt: -1 });

userSchema.index({
  firstname: "text",
  lastname: "text",
  username: "text",
});

userSchema.post("save", function (doc) {
  console.log(`User created/updated: ${doc._id}`);
});

userSchema.post("findOneAndDelete", async function (doc) {
  if (!doc) return;
  console.log(`Cleanup for user ${doc._id}`);
});

export const User = mongoose.model("User", userSchema);
