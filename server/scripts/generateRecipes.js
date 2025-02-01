const { faker } = require("@faker-js/faker");

const generateRecipe = () => ({
  category: faker.helpers.arrayElements(
    ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"],
    3
  ),
  difficulty: faker.helpers.arrayElement(["Easy", "Medium", "Hard"]),
  ingredients: faker.helpers.multiple(
    () => ({
      name: faker.food.ingredient(),
      quantity: faker.number.int({ min: 1, max: 10 }),
    }),
    { count: { min: 3, max: 7 } }
  ),
  name: faker.food.dish(),
  preparationTime: faker.number.int({ min: 10, max: 120 }),
  steps: faker.helpers.multiple(
    () => ({
      description: faker.lorem.sentence(),
    }),
    { count: { min: 1, max: 3 } }
  ),
  visibility: faker.helpers.arrayElement(["Public", "Private"]),
});
const addRecipes = (numRecipes = 5, username) => {
  const recipes = [];
  for (let i = 0; i < numRecipes; i++) {
    const recipe = generateRecipe();
    recipe.username = username;
    recipes.push(recipe);
  }
  return recipes;
};

module.exports = {
  addRecipes,
};
