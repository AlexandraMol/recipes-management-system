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
  methods: {
    submitLogin() {
      if (this.valid) {
        alert(`Form data:\nEmail: ${this.email}\nPassword: ${this.password}`);
        //TODO: route to backend
        this.$router.push("/explore");
      } else {
        return;
      }
    },
  },
};
</script>
