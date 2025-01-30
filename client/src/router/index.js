import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";
import LandingPage from "@/views/LandingPage.vue";
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import HomePage from "@/views/HomePage.vue";
import ExplorePage from "@/views/ExplorePage.vue";
import AddRecipePage from "@/views/AddRecipePage.vue";
import PageNotFound from "@/views/PageNotFound.vue";
import RecipePage from "@/views/RecipePage.vue";

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
  {
    path: "/explore",
    name: "Explore",
    component: ExplorePage,
    meta: { requiresAuth: true },
  },
  {
    path: "/add-recipe",
    name: "AddRecipe",
    component: AddRecipePage,
    meta: { requiresAuth: true },
  },
  {
    path: "/recipe/:id",
    component: RecipePage,
    props: true,
  },
  {
    path: "/:catchAll(.*)",
    component: PageNotFound,
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
