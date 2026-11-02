import { createStore } from "vuex";
import axios from "axios";
import { auth } from "@/firebase";

import {
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut,
} from "firebase/auth";

export default createStore({
  state: {
    user: null,
    role: null,
    authReady: false,
    selectedFilters: [],
  },

  getters: {
    isLoggedIn: (state) => !!state.user,
    currentUser: (state) => state.user,
    isAdmin: (state) => state.role === "admin",
    authReady: (state) => state.authReady,
    getSelectedFilters: (state) => state.selectedFilters || [],
  },

  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },

    CLEAR_USER(state) {
      state.user = null;
      state.role = null;
    },

    SET_ROLE(state, role) {
      state.role = role;
    },

    SET_AUTH_READY(state, value) {
      state.authReady = value;
    },

    SET_FILTERS(state, filters) {
      state.selectedFilters = filters;
    },
  },

  actions: {
    async fetchUserRole({ state, commit }) {
      if (!state.user) {
        commit("SET_ROLE", null);
        return;
      }

      try {
        const token = await state.user.getIdToken();

        const response = await axios.get("http://localhost:5000/api/user/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        commit("SET_ROLE", response.data.role || "user");
      } catch (error) {
        commit("SET_ROLE", null);
        throw error;
      }
    },

    async login({ commit, dispatch }, { email, password }) {
      try {
        const userCredential = await signInWithEmailAndPassword(
          auth,
          email,
          password,
        );

        commit("SET_USER", userCredential.user);
        await dispatch("fetchUserRole");
      } catch (error) {
        console.error("Login error:", error.message);
        throw error;
      }
    },

    async logout({ commit }) {
      await signOut(auth);
      commit("CLEAR_USER");
    },

    getUser({ commit, dispatch }) {
      return new Promise((resolve) => {
        const unsubscribe = onAuthStateChanged(
          auth,
          async (user) => {
            unsubscribe();

            if (user) {
              commit("SET_USER", user);

              try {
                await dispatch("fetchUserRole");
              } catch (error) {
                console.error("Failed to load user role:", error);
              }
            } else {
              commit("CLEAR_USER");
            }

            commit("SET_AUTH_READY", true);
            resolve();
          },
          (error) => {
            unsubscribe();
            console.error("Auth initialization failed:", error);
            commit("CLEAR_USER");
            commit("SET_AUTH_READY", true);
            resolve();
          },
        );
      });
    },

    updateFilters({ commit }, filters) {
      commit("SET_FILTERS", filters);
    },
  },
});
