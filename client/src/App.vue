<template>
  <v-app>
    <!-- TODO: move this code in a separate file -->
    <v-app-bar app color="black" dark>
      <v-toolbar-title @click="() => redirect('/')">
        <span>👨‍🍳</span>
        <span class="app-title">FoodMood</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="!isLoggedIn" @click="() => redirect('/login')" text
        >Login</v-btn
      >
      <template v-else>
        <!-- TODO: change with icons for phones -->
        <v-btn @click="() => redirect('/explore')" text>Explore</v-btn>
        <v-btn @click="() => redirect('add-recipe')" text>Add Recipe</v-btn>
        <v-btn @click="logoutUser" text>Logout</v-btn>
      </template>
    </v-app-bar>
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
import {
  VApp,
  VAppBar,
  VToolbarTitle,
  VSpacer,
  VBtn,
  VMain,
  VFooter,
  VCol,
} from "vuetify/components";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "App",
  computed: {
    ...mapGetters(["isLoggedIn"]),
  },
  methods: {
    ...mapActions(["logout"]),
    redirect(path) {
      this.$router.push(path);
    },
    async logoutUser() {
      await this.logout();
      this.$router.push("/");
    },
  },
  components: {
    VApp,
    VAppBar,
    VToolbarTitle,
    VSpacer,
    VBtn,
    VMain,
    VFooter,
    VCol,
  },
};
</script>

<style>
body {
  margin: 0;
}

.v-toolbar-title:hover {
  cursor: pointer;
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

@media (max-width: 350px) {
  .app-title {
    display: none;
    visibility: hidden;
  }
}

.v-form {
  width: 25%;
}

@media (max-width: 500px) {
  .v-form {
    width: 50%;
  }
}
</style>
