const { db, auth } = require("../firebase/firebase");
const { addRecipes } = require("./generateRecipes");
const { addUser } = require("./generateUsers");

const uploadDataToDatabase = async () => {
  try {
    const recipesRef = db.collection("recipes");
    const users = addUser(5);

    if (!Array.isArray(users) || users.length === 0) {
      console.log("No users generated");
    }

    for (const user of users) {
      const userAuth = await auth.createUser({
        email: user.email,
        password: user.password,
        displayName: user.username,
      });

      await db.collection("users").doc(userAuth.uid).set({
        username: user.username,
        email: user.email,
        createdAt: user.createdAt,
      });

      const recipes = addRecipes(5, user.username);

      if (!Array.isArray(recipes) || recipes.length === 0) {
        console.log("No recipes generated");
        continue;
      }

      const batch = db.batch();

      for (const recipe of recipes) {
        const recipeRef = recipesRef.doc();
        batch.set(recipeRef, recipe);
      }

      await batch.commit();
    }
  } catch (error) {
    console.log(error.message);
  }
};

module.exports = {
  uploadDataToDatabase,
};
