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

<style>
body {
  margin: 0;
}

.v-main {
  /* background: url("../public/background/landing.jpg"); */
  background: white;
  background-size: cover;
}

.v-btn:hover {
  transform: scale(1.05) perspective(1px);
}

.container-auth {
  display: flex;
  gap: 3em;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}
</style>
