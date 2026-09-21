<template>
  <v-container
    class="d-flex justify-center align-center text-center"
    style="height: 100%"
  >
    <v-img width="100px" src="background/chef.png"></v-img>
    <div class="description">
      <h1 class="text-h3 font-weight-bold mb-4">
        The recipe app for every home chef!
      </h1>
      <p class="text-h6">
        Find delicious recipes, cook with confidence, and share your creations -
        all in one app!
      </p>
      <v-container
        class="buttons-area d-flex justify-center align-center text-center"
      >
        <v-btn @click="goToRegister" class="button" color="black" large
          >Sign up</v-btn
        >
        <v-btn @click="goToLogin" class="button" color="white" large
          >Log in</v-btn
        >
      </v-container>
    </div>
  </v-container>
</template>
<script>
import { VBtn, VContainer, VImg } from "vuetify/components";
export default {
  name: "LandingPage",
  components: {
    VBtn,
    VContainer,
    VImg,
  },
  methods: {
    goToRegister() {
      this.$router.push("/register");
    },
    goToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>

<style>
.description {
  width: 60%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.buttons-area {
  gap: 20px;
}

.button {
  width: 200px;
}

.button:hover {
  transform: scale(1.05) perspective(1px);
}
</style>
