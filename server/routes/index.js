const router = require("express").Router();
const authRouter = require("./authRoutes");
const recipeRouter = require("./recipeRoutes");

router.use("/auth", authRouter);
router.use("/recipe", recipeRouter);

module.exports = router;
