import { z } from "zod";

export const productValidationSchema = z.object({
  title: z
    .string()
    .min(1, "Title is required")
    .max(150, "Title cannot exceed 150 characters")
    .trim(),
  
  description: z
    .string()
    .min(10, "Description must be at least 10 characters long")
    .max(1000, "Description cannot exceed 1000 characters")
    .trim(),
  
  price: z
    .number()
    .min(0, "Price cannot be negative")
    .max(10000, "Price cannot exceed 10000")
    .int("Price must be an integer"),
  
  discount: z
    .number()
    .min(0, "Discount cannot be negative")
    .max(90, "Discount cannot exceed 90%"),
  
  stock: z
    .number()
    .min(0, "Stock cannot be negative")
    .int("Stock must be an integer"),
  
  category: z
    .string()
    .min(1, "Category is required")
    .trim(),
});