<template>
  <div class="container-auth">
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
    submitRegister() {
      if (this.valid) {
        alert(
          `Form data:\nUsername: ${this.username}\nEmail: ${this.email}\nPassword: ${this.password}`
        );
        //TODO: route to backend
        this.$router.push("/login");
      } else {
        return;
      }
    },
  },
};
</script>
