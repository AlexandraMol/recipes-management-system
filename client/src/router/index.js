import { createRouter, createWebHistory } from "vue-router";
import { auth } from "../firebase";
import LandingPage from "@/views/LandingPage.vue";
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
