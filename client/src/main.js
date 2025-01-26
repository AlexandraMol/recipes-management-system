import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";
import { createVuetify } from "vuetify";

const vuetify = createVuetify();

const app = createApp(App);

app.use(store).use(vuetify).use(router);

store.dispatch("fetchUser");

app.mount("#app");
