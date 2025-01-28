<template>
  <div>
    <!-- TODO: loading component -->
    <div v-if="loading">Loading...</div>
    <!-- TODO: Extract this template code to re use at explore -->
    <div v-else class="recipe-container">
      <v-card
        v-for="recipe in recipes"
        :key="recipe.name"
        class="mx-auto"
        max-width="344"
      >
        <v-img
          height="200px"
          src="https://images.pexels.com/photos/691114/pexels-photo-691114.jpeg?cs=srgb&dl=pexels-dana-tentis-118658-691114.jpg&fm=jpg"
          cover
        ></v-img>

        <v-card-title> {{ recipe.name }} </v-card-title>

        <v-card-subtitle>
          {{ recipe.category.join(", ") }}
        </v-card-subtitle>

        <v-card-actions>
          <v-btn color="black" text="Explore"></v-btn>
          <div>
            <span class="card-button">🗑️</span>
            <span class="card-button">✏️</span>
          </div>
        </v-card-actions>
      </v-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {
  VCard,
  VImg,
  VCardTitle,
  VCardSubtitle,
  VCardActions,
  VBtn,
} from "vuetify/components";
import { mapGetters } from "vuex";

export default {
  name: "HomePage",
  data() {
    return {
      recipes: [],
      loading: true,
    };
  },
  components: {
    VCard,
    VImg,
    VCardTitle,
    VCardSubtitle,
    VCardActions,
    VBtn,
  },
  computed: {
    ...mapGetters(["currentUser"]),
  },

  mounted() {
    this.getRecipes();
  },

  methods: {
    async getRecipes() {
      try {
        const token = await this.currentUser.getIdToken(); // TODO: Sa vad de ce la refresh se pierde userul
        const response = await axios.get(
          `http://localhost:3000/api/recipe/${this.currentUser.displayName}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );
        if (response.status === 200) {
          this.recipes = response.data.data;
        }
      } catch (error) {
        console.log(error);
        this.recipes = [];
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style>
.recipe-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 5px;
  align-items: center;
}

.v-card {
  flex: 1 2 90%;
  margin: 5px;
}

.v-card-actions {
  display: flex;
  justify-content: space-between;
}

.card-button {
  cursor: pointer;
  padding: 5px;
}

.card-button:hover {
  background-color: antiquewhite;
}
</style>
