# PRODUCT API – Query Engine Documentation

## Base Route

GET /products

---

## Query Parameters

### 1. Search

?search=phone

- Runs case-insensitive regex search on:
  - name
  - description

### 2. Price Range

?minPrice=100&maxPrice=500

### 3. Tags

?tags=apple,samsung

- Matches any of the provided tags ($in query)

### 4. Sorting

?sort=price:asc
?sort=createdAt:desc

Format:
field:direction  
direction = asc | desc

### 5. Pagination

?page=2&limit=20

### 6. Cursor Pagination

?cursor=LAST_PRODUCT_ID&limit=10

### 7. Soft Deletes

Exclude deleted (default):
?includeDeleted=false

Include soft-deleted:
?includeDeleted=true

---

## Example

/products?search=phone&minPrice=100&maxPrice=900&tags=apple,samsung&sort=price:desc&page=1&limit=20
