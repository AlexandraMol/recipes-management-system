import { createStore } from "vuex";
import { auth } from "@/firebase";
import {
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut,
} from "firebase/auth";

export default createStore({
  state: {
    user: JSON.parse(localStorage.getItem("user")) || null, //TODO: refactor so that user is not saved in local storage
  },
  getters: {
    isLoggedIn: (state) => !!state.user,
    currentUser: (state) => state.user,
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user;
      localStorage.setItem("user", JSON.stringify(user));
    },
    CLEAR_USER(state) {
      state.user = null;
      localStorage.removeItem("user");
    },
  },
  actions: {
    async login({ commit }, { email, password }) {
      try {
        const userCredential = await signInWithEmailAndPassword(
          auth,
          email,
          password
        );
        commit("SET_USER", userCredential.user);
      } catch (error) {
        console.error("Login error:", error.message);
        throw error;
      }
    },
    async logout({ commit }) {
      try {
        await signOut(auth);
        commit("CLEAR_USER");
      } catch (error) {
        console.error("Logout error:", error.message);
        throw error;
      }
    },
    fetchUser({ commit }) {
      onAuthStateChanged(auth, (user) => {
        if (user) {
          commit("SET_USER", user);
        } else {
          commit("CLEAR_USER");
        }
      });
    },
  },
  modules: {},
});
