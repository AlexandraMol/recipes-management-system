const { faker } = require("@faker-js/faker");

const generateUser = () => ({
  email: faker.internet.email(),
  password: "password",
  username: faker.internet.username(),
  createdAt: new Date().toISOString(),
});
const addUser = (number = 0) => {
  const users = [];
  for (let i = 0; i < number; i++) {
    const user = generateUser();
    users.push(user);
  }
  return users;
};

module.exports = {
  addUser,
};
