import { z } from "zod";

export const userValidationSchema = z.object({
  username: z
    .string()
    .min(3, "Username must be at least 3 characters long")
    .max(30, "Username cannot exceed 30 characters")
    .regex(
      /^[a-z0-9]+$/,
      "Username can only contain lowercase letters and numbers"
    )
    .trim(),

  email: z
    .email("Invalid email format")
    .min(5, "Email must be at least 5 characters long")
    .max(100, "Email cannot exceed 100 characters")
    .trim(),

  firstname: z
    .string()
    .min(2, "First name must be at least 2 characters long")
    .max(50, "First name cannot exceed 50 characters")
    .trim(),

  lastname: z
    .string()
    .max(50, "Last name cannot exceed 50 characters")
    .trim()
    .optional(),

  password: z
    .string()
    .min(6, "Password must be at least 6 characters long")
    .max(100, "Password cannot exceed 100 characters"),

  role: z.enum(["user", "seller", "admin"]).default("user"),
});
