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
      .where("username", "!=", req.params.username)
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

module.exports = {
  add,
  getUserRecipes,
  getOtherUserRecipes,
};
