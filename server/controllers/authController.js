const { db, auth } = require("../firebase/firebase");
const register = async (req, res) => {
  const { email, password, username } = req.body;

  try {
    const usernameValidation = await db
      .collection("users")
      .where("username", "==", username)
      .get();

    if (!usernameValidation.empty) {
      return res.status(400).json({ error: "This username is taken." });
    }

    const emailValidation = await auth.getUserByEmail(email).catch(() => null);

    if (emailValidation) {
      return res
        .status(400)
        .json({ error: "An account with this email already exists." });
    }

    const user = await auth.createUser({
      email,
      password,
      displayName: username,
    });

    await db.collection("users").doc(user.uid).set({
      username,
      email,
      createdAt: new Date().toISOString(),
    });

    return res.status(201).json({
      message: "User registered successfully!",
    });
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
};

module.exports = {
  register,
};
