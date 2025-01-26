import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";
import { createVuetify } from "vuetify";

const vuetify = createVuetify();

createApp(App).use(store).use(vuetify).use(router).mount("#app");
