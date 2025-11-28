const demoRoute = (req, res, next) => {
  try {
    throw new Error("this is demo routes error");
  } catch (e) {
    next(e);
  }
};

export { demoRoute };
