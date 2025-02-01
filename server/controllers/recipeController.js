const { db } = require("../firebase/firebase");

const add = async (req, res) => {
  const { username, name } = req.body;

  try {
    const nameAndAuthorValidation = await db
      .collection("recipes")
      .where("name", "==", name)
      .where("username", "==", username)
      .get();

    if (!nameAndAuthorValidation.empty) {
      return res.status(400).json({ error: "This recipe already exists." });
    }

    await db.collection("recipes").add(req.body);

    return res.status(201).json({
      message: "Recipe added!",
    });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
};

const getUserRecipes = async (req, res) => {
  try {
    const userRecipes = await db
      .collection("recipes")
      .where("username", "==", req.params.username)
      .get();

    if (userRecipes.empty) {
      return res.status(200).json({
        data: [],
      });
    }

    const recipes = userRecipes.docs.map((doc) => ({
      id: doc.id,
      ...doc.data(),
    }));

    return res.status(200).json({
      data: recipes,
    });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
};

const getOtherUserRecipes = async (req, res) => {
  try {
    const userRecipes = await db
      .collection("recipes")
      .where("visibility", "==", "Public")
      .get();

    const filteredRecipes = userRecipes.docs.filter((doc) => {
      const recipe = doc.data();
      return recipe.username !== req.params.username;
    });

    if (filteredRecipes.empty) {
      return res.status(200).json({
        data: [],
      });
    }

    const recipes = filteredRecipes.map((doc) => ({
      id: doc.id,
      ...doc.data(),
    }));

    return res.status(200).json({ data: recipes });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
};

const getRecipeById = async (req, res) => {
  try {
    const recipe = await db.collection("recipes").doc(req.params.id).get();

    if (!recipe.exists) {
      return res.status(404).json({ message: "Recipe not found" });
    }

    return res.status(200).json({ data: recipe.data() });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
};

const remove = async (req, res) => {
  try {
    const recipe = await db.collection("recipes").doc(req.params.id).get();

    if (!recipe.exists) {
      return res.status(404).json({ message: "Recipe not found" });
    }

    await db.collection("recipes").doc(req.params.id).delete();

    return res.status(200).json({ message: "Recipe deleted" });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
};

const edit = async (req, res) => {
  try {
    const recipe = await db.collection("recipes").doc(req.params.id).get();

    if (!recipe.exists) {
      return res.status(404).json({ message: "Recipe not found" });
    }
    await db.collection("recipes").doc(req.params.id).update(req.body);

    return res.status(200).json({ message: "Recipe updated" });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
};

const generateShoppingList = async (req, res) => {
  try {
    const { recipeIds } = req.body;

    if (!recipeIds || recipeIds.length === 0) {
      return res.status(400).json({ message: "Missing recipes" });
    }

    let ingredientsToBuy = {};

    for (const recipeId of recipeIds) {
      const recipe = await db.collection("recipes").doc(recipeId).get();

      if (!recipe.exists) {
        continue;
      }

      const { ingredients } = recipe.data();

      ingredients.forEach(({ name, quantity }) => {
        const formattedName = name.toLowerCase();
        const formattedQuantity = parseInt(quantity) || 0;

        if (ingredientsToBuy[formattedName]) {
          ingredientsToBuy[formattedName] += formattedQuantity;
        } else {
          ingredientsToBuy[formattedName] = formattedQuantity;
        }
      });
    }

    const shoppingList = Object.entries(ingredientsToBuy).map(
      ([name, quantity]) => ({
        name,
        quantity: quantity,
      })
    );

    res.status(200).json({ data: shoppingList });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
};

module.exports = {
  add,
  edit,
  remove,
  getRecipeById,
  getUserRecipes,
  getOtherUserRecipes,
  generateShoppingList,
};
