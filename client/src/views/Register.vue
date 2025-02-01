<template>
  <div class="container-auth">
    <Toaster ref="toaster" />
    <h1>Register Form</h1>
    <v-form v-model="valid" @submit.prevent="submitRegister">
      <v-text-field
        v-model="email"
        :rules="emailRules"
        label="E-mail"
        required
      ></v-text-field>
      <v-text-field
        v-model="username"
        :counter="10"
        :rules="usernameRules"
        label="Username"
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
import Toaster from "@/components/Toaster.vue";
import axios from "axios";

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
    username: "",
    usernameRules: [
      (value) => {
        if (value) {
          return true;
        }
        return "Name is required.";
      },
      (value) => {
        if (value?.length <= 10) {
          return true;
        }
        return "Name must be less than 10 characters.";
      },
    ],
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
      (value) => {
        if (value?.length >= 6) {
          return true;
        }
        return "Password must be more than 6 characters.";
      },
    ],
  }),
  methods: {
    async submitRegister() {
      // TODO: treat errors with toasters
      if (this.valid) {
        try {
          const response = await axios.post(
            "http://localhost:3000/api/auth/register",
            {
              email: this.email,
              password: this.password,
              username: this.username,
            }
          );
          if (response.status === 201) {
            this.$router.push("/login");
          }
        } catch (error) {
          console.log(error);
          this.$refs.toaster.showToast(
            error?.response?.data?.error || error.message
          );
        }
      } else {
        return;
      }
    },
  },
};
</script>
