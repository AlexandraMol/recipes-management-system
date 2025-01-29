const router = require("express").Router();
const RecipeController = require("../controllers/recipeController");
const authorize = require("../middlewares/authorize");

router.post("/add", authorize, RecipeController.add);
router.put("/edit/:id", authorize, RecipeController.edit);
router.delete("/remove/:id", authorize, RecipeController.remove);
router.get("/recipe/:id", authorize, RecipeController.getRecipeById);
router.get("/:username", authorize, RecipeController.getUserRecipes);
router.get(
  "/otherRecipes/:username",
  authorize,
  RecipeController.getOtherUserRecipes
);

module.exports = router;
