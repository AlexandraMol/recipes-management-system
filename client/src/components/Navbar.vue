<template>
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
      <div class="button-container">
        <v-btn @click="() => redirect('/explore')" text v-if="!isMobile">
          Explore
        </v-btn>
        <v-btn @click="() => redirect('/explore')" icon v-else>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>

        <v-btn @click="() => redirect('/add-recipe')" text v-if="!isMobile">
          Add Recipe
        </v-btn>
        <v-btn @click="() => redirect('/add-recipe')" icon v-else>
          <v-icon>mdi-plus-box</v-icon>
        </v-btn>

        <v-btn @click="logoutUser" text v-if="!isMobile"> Logout </v-btn>
        <v-btn @click="logoutUser" icon v-else>
          <v-icon>mdi-logout</v-icon>
        </v-btn>
      </div>
    </template>
  </v-app-bar>
</template>

<script>
import {
  VAppBar,
  VToolbarTitle,
  VSpacer,
  VBtn,
  VIcon,
} from "vuetify/components";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "App",
  computed: {
    ...mapGetters(["isLoggedIn"]),
  },
  data() {
    return {
      isMobile: false,
    };
  },
  mounted() {
    this.checkScreenSize();
    window.addEventListener("resize", this.checkScreenSize);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkScreenSize);
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
    checkScreenSize() {
      this.isMobile = window.innerWidth <= 500;
    },
  },
  components: {
    VAppBar,
    VToolbarTitle,
    VSpacer,
    VBtn,
    VIcon,
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

.button-container {
  display: flex;
  gap: 10px;
}

@media (max-width: 450px) {
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
