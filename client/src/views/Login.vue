<template>
  <div class="container-auth">
    <h1>Login Form</h1>
    <v-form v-model="valid" @submit.prevent="submitLogin">
      <v-text-field
        v-model="email"
        :rules="emailRules"
        label="E-mail"
        required
      ></v-text-field>
      <v-text-field
        v-model="password"
        :rules="passwordRules"
        type="password"
        label="Password"
        required
      ></v-text-field>
      <v-btn type="submit" class="mt-2" color="black" block>Submit</v-btn>
    </v-form>
    <!-- TODO: Add toaster for errors -->
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import {
  VForm,
  VContainer,
  VRow,
  VCol,
  VTextField,
  VBtn,
} from "vuetify/components";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "Register",
  components: {
    VForm,
    VContainer,
    VRow,
    VCol,
    VTextField,
    VBtn,
  },
  data: () => ({
    valid: false,
    errorMessage: "",
    email: "",
    emailRules: [
      (value) => {
        if (value) {
          return true;
        }
        return "E-mail is required.";
      },
    ],
    password: "",
    passwordRules: [
      (value) => {
        if (value) {
          return true;
        }
        return "Password is required.";
      },
    ],
  }),
  computed: {
    ...mapGetters(["isLoggedIn"]),
  },

  methods: {
    ...mapActions(["login"]),
    async submitLogin() {
      if (this.valid) {
        alert(`Form data:\nEmail: ${this.email}\nPassword: ${this.password}`);
        //TODO: refactor when route to backend is done
        try {
          await this.login({ email: this.email, password: this.password });

          this.$router.push("/home");
        } catch (error) {
          this.errorMessage = "Invalid email or password.";
        }
      } else {
        return;
      }
    },
  },
};
</script>
