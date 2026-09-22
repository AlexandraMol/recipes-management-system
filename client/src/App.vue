<template>
  <v-app>
    <Navbar></Navbar>
    <v-main>
      <router-view></router-view>
    </v-main>
    <v-footer app color="black" dark>
      <v-col class="text-center white--text"></v-col>
    </v-footer>
  </v-app>
</template>

<script>
import { VApp, VMain, VFooter, VCol } from "vuetify/components";
import Navbar from "@/components/Navbar.vue";
import "@/assets/main.css";

export default {
  name: "App",
  components: {
    VApp,
    VMain,
    VFooter,
    VCol,
    Navbar,
  },
};
</script>
