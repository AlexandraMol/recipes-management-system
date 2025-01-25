var admin = require("firebase-admin");

var serviceAccount = process.env.FIREBASE_TOKEN;

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

db = admin.firestore();

module.exports = { db };
