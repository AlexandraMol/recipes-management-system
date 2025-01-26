<template>
  <v-container
    class="d-flex justify-center align-center text-center"
    style="height: 70vh"
  >
    <div class="description">
      <h1 class="text-h3 mb-4">Welcome to our website!</h1>
      <p class="text-h6">
        <b>FoodMood</b> is the perfect app for food lovers, chefs, and home
        cooks alike. It's your go-to platform when you want to store, share and
        explore from around the world.
      </p>
      <p class="text-h6">Join the FoodMood Community Today!</p>
      <v-btn @click="goToRegister" class="register-button" color="black" large
        >Register</v-btn
      >
    </div>
  </v-container>
</template>
<script>
import { VBtn, VContainer } from "vuetify/components";
export default {
  name: "LandingPage",
  components: {
    VBtn,
    VContainer,
  },
  methods: {
    goToRegister() {
      this.$router.push("/register");
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

.register-button {
  width: 200px;
}
</style>
