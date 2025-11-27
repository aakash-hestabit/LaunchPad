# Index Analysis for Product and User Schemas

---

## Product Schema

The product schema has the following indexes:

!["index screenshot for users schema"](image-1.png)


### Indexed Fields:

1. **\_id**: Regular index (unique)
2. **title_1**: Regular index
3. **category_1**: Regular index
4. **status_1**: Regular index
5. **slug_1**: Regular index (unique)
6. **status*1.createdAt*-1**: Compound index
7. **title_text_description_text**: Text index (Compound)

### Explanation:

- **Regular Index**: This type of index is created for most fields to speed up simple queries. For example, fields like `_id`, `title`, `category`, `status`, and `slug` are all indexed with a regular index. The `_id` field is also marked as `unique` to ensure each product has a unique identifier.

- **Compound Index**: The `status_1.createdAt_-1` is a compound index, meaning it indexes multiple fields together. In this case, it indexes `status_1` and `createdAt`. The order matters here because the index will first use `status` for sorting in ascending order (indicated by 1) and then `createdAt` for sorting in descending order (indicated by -1).

- **Text Index**: The `title_text_description_text` field is indexed with a text index. Text indexes are used to enable full-text search capabilities. They use stemming tokenization to break down words into their root forms, improving search results. The index also applies relevance scoring to rank documents based on their content's relevance to the search query. In this case, the fields `title`, `text`, and `description` are being indexed for text searches.

---

## User Schema

The user schema has the following indexes:
!["index screenshot for users schema"](image.png)

### Indexed Fields:

1. **\_id**: Regular index (unique)
2. **username_1**: Regular index (unique)
3. **email_1**: Regular index (unique)
4. **email_1_username_1**: Compound index
5. **role*1.createdAt*-1**: Compound index 
6. **firstname_text_lastname_text_username_text**: Text index
7. **refreshTokenExpiresAt_1**: Regular (TTL)

### Explanation:

- **TTL (Time To Live) Index**: The `refreshTokenExpiresAt_1` field is a TTL index.TTL indexes are applied only to date-type fields. MongoDB will automatically delete documents based on the time specified in the `refreshTokenExpiresAt` field, ensuring data is only retained for as long as needed.

---

## Sparse Index

a sparse index is an index that only includes documents with the indexed field present. If a document does not contain the indexed field, it will not be included in the index, making it useful for sparse data sets where some documents may lack certain fields. sparse indexes are particularly useful for optional fields or fields that only apply to a subset of documents.
