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
import EditRecipePage from "@/views/EditRecipePage.vue";
import GenerateListPage from "@/views/GenerateListPage.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import AdminDashboard from "@/views/AdminDashboard.vue";

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
    path: "/recipe/edit/:id",
    name: "EditRecipe",
    component: EditRecipePage,
    meta: { requiresAuth: true },
  },
  {
    path: "/generate-shopping-list",
    name: "GenerateShoppingList",
    component: GenerateListPage,
    meta: { requiresAuth: true },
  },
  {
    path: "/profile",
    name: "Profile",
    component: ProfilePage,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    name: "Admin",
    component: AdminDashboard,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
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

const authInitialization = store.dispatch("getUser");

router.beforeEach(async (to, from, next) => {
  await authInitialization;

  if (to.meta.requiresAuth && !store.getters.isLoggedIn) {
    return next("/login");
  }

  if (to.meta.requiresAdmin) {
    if (store.state.role === null) {
      await store.dispatch("fetchUserRole");
    }

    if (!store.getters.isAdmin) {
      return next("/");
    }
  }

  next();
});

export default router;
