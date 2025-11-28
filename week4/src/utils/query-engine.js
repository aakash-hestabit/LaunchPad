export function buildProductQuery(query, includeDeleted = false) {
  const filter = {};
  const includeDeletedBool = includeDeleted === true || includeDeleted === "true";
  if (query.search) {
    filter.$or = [
      { title: { $regex: query.search, $options: "i" } }
    ];
  }

  if (query.minPrice || query.maxPrice) {
    filter.price = {};
    if (query.minPrice) filter.price.$gte = Number(query.minPrice);
    if (query.maxPrice) filter.price.$lte = Number(query.maxPrice);
  }

  if (query.tags) {
    filter.description = { $in: query.tags.split(",") };
  }

  if (!includeDeletedBool) {
    filter.deletedAt = null;
  }

  let sortQuery = {};
  if (query.sort) {
    const [field, direction] = query.sort.split(":");
    sortQuery[field] = direction === "desc" ? -1 : 1;
  } else {
    sortQuery = { createdAt: -1 };
  }
  console.log(includeDeleted);
  console.log(filter.deletedAt);

  console.log(JSON.stringify(filter));

  return { filter, sortQuery };
}
