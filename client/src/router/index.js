import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";
import { auth } from "../firebase";
import LandingPage from "@/views/LandingPage.vue";
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import HomePage from "@/views/HomePage.vue";

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
    beforeEnter: (to, from, next) => {
      const isLoggedIn = store.getters.isLoggedIn;
      if (isLoggedIn) {
        next("/home");
      } else {
        next();
      }
    },
    meta: { requiresAuth: false },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    meta: { requiresAuth: false },
  },
  {
    path: "/home",
    name: "Homepage",
    component: HomePage,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = store.getters.isLoggedIn;
  if (to.meta.requiresAuth && !isLoggedIn) {
    next("/login");
  } else {
    next();
  }
});

export default router;
