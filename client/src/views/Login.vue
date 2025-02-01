<template>
  <div class="container-auth">
    <Toaster ref="toaster" />
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
import Toaster from "@/components/Toaster.vue";

export default {
  name: "Register",
  components: {
    VForm,
    VContainer,
    VRow,
    VCol,
    VTextField,
    VBtn,
    Toaster,
  },
  data: () => ({
    valid: false,
    email: "",
    emailRules: [
      (value) => {
        if (value) {
          return true;
        }
        return "E-mail is required.";
      },
      (value) => {
        if (/.+@.+\..+/.test(value)) {
          return true;
        }
        return "E-mail must be valid.";
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
        try {
          await this.login({ email: this.email, password: this.password });

          this.$router.push("/home");
        } catch (error) {
          this.$refs.toaster.showToast("Invalid email or password.");
        }
      } else {
        return;
      }
    },
  },
};
</script>
