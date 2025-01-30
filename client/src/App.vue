<template>
  <v-app>
    <Navbar></Navbar>
    <v-main>
      <router-view></router-view>
    </v-main>
    <v-footer app color="black" dark>
      <v-col class="text-center white--text"
        >Made with ❤️ by Alexandra Molnar</v-col
      >
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
  background: white;
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
