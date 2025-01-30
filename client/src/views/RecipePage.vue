<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="mx-auto pa-5" elevation="6">
          <v-img
            height="250px"
            src="https://images.pexels.com/photos/691114/pexels-photo-691114.jpeg"
            cover
            class="mb-3"
          ></v-img>

          <v-card-title class="text-h5 font-weight-bold text-center">
            {{ this.recipe.name }}
          </v-card-title>

          <v-card-subtitle class="text-center">
            Created by: <strong>{{ recipe.username }}</strong>
          </v-card-subtitle>

          <v-divider class="my-4"></v-divider>

          <v-list>
            <v-list-item>
              <v-icon start>mdi-clock-outline</v-icon>
              <span
                ><strong>Preparation Time:</strong>
                {{ recipe.preparationTime }} min</span
              >
            </v-list-item>

            <v-list-item>
              <v-icon start>mdi-fire</v-icon>
              <span><strong>Difficulty:</strong> {{ recipe.difficulty }}</span>
            </v-list-item>

            <v-list-item>
              <v-icon start>mdi-eye</v-icon>
              <span><strong>Visibility:</strong> {{ recipe.visibility }}</span>
            </v-list-item>

            <v-list-item>
              <v-icon start>mdi-tag-multiple</v-icon>
              <span
                ><strong>Categories:</strong>
                {{ recipe?.category?.join(", ") }}</span
              >
            </v-list-item>
          </v-list>

          <v-divider class="my-4"></v-divider>

          <v-card-title class="text-h6"
            ><strong>😋 Ingredients</strong>
          </v-card-title>
          <v-list dense>
            <v-list-item
              v-for="(ingredient, index) in recipe.ingredients"
              :key="index"
            >
              <v-list-item-content>
                <v-list-item-title
                  >{{ ingredient.name }} -
                  {{ ingredient.quantity }}</v-list-item-title
                >
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-divider class="my-4"></v-divider>

          <v-card-title class="text-h6"
            ><strong>📖 Steps </strong></v-card-title
          >
          <v-list dense>
            <v-list-item v-for="(step, index) in recipe.steps" :key="index">
              <v-list-item-content>
                <v-list-item-title>Step {{ index + 1 }}</v-list-item-title>
                <v-spacer></v-spacer>
                <v-textarea
                  v-model="step.description"
                  rows="4"
                  >{{
                }}</v-textarea>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-divider class="my-4"></v-divider>

          <v-card-actions class="justify-center">
            <v-btn color="black" @click="$router.push('/')">
              Back to Home
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {
  VContainer,
  VRow,
  VCol,
  VCard,
  VImg,
  VCardTitle,
  VCardSubtitle,
  VDivider,
  VList,
  VListItem,
  VListItemIcon,
  VListItemContent,
  VListItemTitle,
  VListItemSubtitle,
  VIcon,
  VCardActions,
  VBtn,
  VTextarea,
} from "vuetify/components";

import axios from "axios";
import { mapGetters } from "vuex";
export default {
  name: "RecipePage",
  props: ["id"], // Receive ID from route
  data() {
    return {
      recipe: {},
      loading: true,
    };
  },
  components: {
    VContainer,
    VRow,
    VCol,
    VCard,
    VImg,
    VCardTitle,
    VCardSubtitle,
    VDivider,
    VList,
    VListItem,
    VListItemIcon,
    VListItemContent,
    VListItemTitle,
    VListItemSubtitle,
    VIcon,
    VCardActions,
    VBtn,
    VTextarea,
  },
  computed: {
    ...mapGetters(["currentUser"]),
  },
  mounted() {
    this.getRecipe();
  },
  methods: {
    async getRecipe() {
      try {
        const token = await this.currentUser.getIdToken();
        const response = await axios.get(
          `http://localhost:3000/api/recipe/recipe/${this.id}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );
        if (response.status === 200) {
          this.recipe = response.data.data;
        }
      } catch (error) {
        console.log(error);
        this.recipe = {};
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
.v-card {
  border-radius: 12px;
  overflow: hidden;
}

.recipe-page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1em;
}
</style>
