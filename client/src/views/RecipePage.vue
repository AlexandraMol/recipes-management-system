<template>
  <v-container v-if="!loading" fluid class="recipe-page-container">
    <div class="recipe-layout">
      <!-- LEFT: MAIN RECIPE -->
      <v-card class="recipe-details-card" elevation="0">
        <div class="image-wrapper">
          <v-img
            :src="recipe.imageUrl"
            height="360"
            cover
            class="recipe-image"
          />

          <v-btn
            v-if="!isOwnRecipe"
            icon
            class="favorite-btn"
            @click="toggleFavorite"
          >
            <v-icon :color="isFavorite ? 'red' : 'grey'">
              {{ isFavorite ? "mdi-heart" : "mdi-heart-outline" }}
            </v-icon>
          </v-btn>
        </div>

        <div class="recipe-content">
          <div class="recipe-heading">
            <div>
              <h1>{{ recipe.name }}</h1>
              <p class="recipe-author">
                Created by <strong>{{ recipe.username }}</strong>
              </p>
            </div>

            <div class="category-section">
              <v-chip
                v-for="category in recipe.category"
                :key="category"
                size="small"
                class="category-chip"
              >
                {{ category }}
              </v-chip>
            </div>
          </div>

          <!-- RATING -->
          <div class="rating-section">
            <div class="rating-summary">
              <v-icon color="amber-darken-2">mdi-star</v-icon>
              <strong>{{ Number(averageRating).toFixed(1) }}</strong>
              <span>({{ numberOfRatings }} ratings)</span>
            </div>

            <div v-if="!isOwnRecipe" class="rating-input">
              <span>Your rating:</span>
              <v-rating
                v-model="userRating"
                density="compact"
                color="amber"
                hover
                @update:modelValue="submitRating"
              />
            </div>

            <span v-else class="own-recipe-label"> Your recipe </span>
          </div>

          <!-- RECIPE INFO -->
          <div class="info-grid">
            <div class="info-card">
              <v-icon>mdi-clock-outline</v-icon>
              <span>Preparation time</span>
              <strong>{{ recipe.preparationTime }} min</strong>
            </div>

            <div class="info-card">
              <v-icon>mdi-chef-hat</v-icon>
              <span>Difficulty</span>
              <strong>{{ recipe.difficulty }}</strong>
            </div>

            <div class="info-card">
              <v-icon>mdi-eye-outline</v-icon>
              <span>Visibility</span>
              <strong>{{ recipe.visibility }}</strong>
            </div>
          </div>

          <!-- INGREDIENTS -->
          <section class="recipe-section">
            <h2>
              <v-icon>mdi-food-apple-outline</v-icon>
              Ingredients
            </h2>

            <div class="ingredients-list">
              <div
                v-for="(ingredient, index) in recipe.ingredients"
                :key="index"
                class="ingredient-item"
              >
                <span>{{ ingredient.name }}</span>
                <strong>
                  {{ ingredient.quantity }} {{ ingredient.unit }}
                </strong>
              </div>
            </div>
          </section>

          <!-- STEPS -->
          <section class="recipe-section">
            <h2>
              <v-icon>mdi-book-open-page-variant-outline</v-icon>
              Instructions
            </h2>

            <div class="steps-list">
              <div
                v-for="(step, index) in recipe.steps"
                :key="index"
                class="step-card"
              >
                <span class="step-number">
                  {{ String(index + 1).padStart(2, "0") }}
                </span>

                <p>{{ step.description }}</p>
              </div>
            </div>
          </section>

          <div class="recipe-footer">
            <v-btn variant="outlined" color="black" @click="$router.push('/')">
              <v-icon start>mdi-arrow-left</v-icon>
              Back to Home
            </v-btn>
          </div>
        </div>
      </v-card>

      <!-- RIGHT: RECOMMENDATIONS -->
      <aside class="recommendations-panel">
        <div class="recommendations-heading">
          <h2>You might also like</h2>
          <p>Discover something delicious next.</p>
        </div>

        <div class="recommendations-grid">
          <div
            v-for="recommended in recommendedRecipes.slice(0, 4)"
            :key="recommended.id"
            class="recommendation-card"
            @click="openRecommendation(recommended.id)"
          >
            <v-img
              :src="recommended.imageUrl"
              height="110"
              cover
              class="recommendation-image"
            />

            <div class="recommendation-content">
              <h3>{{ recommended.name }}</h3>

              <div class="recommendation-meta">
                <span>
                  <v-icon size="14">mdi-clock-outline</v-icon>
                  {{ recommended.preparationTime }} min
                </span>

                <span>
                  <v-icon size="14" color="amber-darken-2"> mdi-star </v-icon>
                  {{ Number(recommended.averageRating || 0).toFixed(1) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </v-container>

  <div v-else class="loading-container">
    <v-progress-circular indeterminate color="primary" size="48" />
  </div>
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
  VIcon,
  VCardActions,
  VBtn,
  VRating,
  VChip,
  VProgressCircular,
} from "vuetify/components";

import axios from "axios";
import { mapGetters } from "vuex";
import RecommendationsCarousel from "@/components/RecommendationsCarousel.vue";

export default {
  name: "RecipePage",

  props: ["id"],

  components: {
    VContainer,
    VRow,
    VCol,
    VCard,
    VImg,
    VCardTitle,
    VCardSubtitle,
    VDivider,
    VIcon,
    VCardActions,
    VBtn,
    VRating,
    VChip,
    RecommendationsCarousel,
    VProgressCircular,
  },

  data() {
    return {
      recipe: {},
      loading: true,
      isFavorite: false,
      averageRating: 0,
      numberOfRatings: 0,
      userRating: 0,
      recommendedRecipes: [],
    };
  },

  computed: {
    ...mapGetters(["currentUser"]),

    isOwnRecipe() {
      return this.recipe.username === this.currentUser?.displayName;
    },
  },

  mounted() {
    this.getRecipe();
  },

  watch: {
    id() {
      this.recipe = {};
      this.userRating = 0;
      this.loading = true;
      this.getRecipe();
    },
  },

  methods: {
    openRecommendation(recipeId) {
      this.$router.push(`/recipe/${recipeId}`);
    },

    async getRecipe() {
      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.get(
          `http://localhost:5000/api/recipe/recipe/${this.id}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          },
        );

        if (response.status === 200) {
          this.recipe = response.data.data;

          this.averageRating = this.recipe.averageRating || 0;
          this.numberOfRatings = this.recipe.numberOfRatings || 0;
          this.isFavorite = this.recipe.isFavorite || false;

          await this.getRecipeStatus();
          await this.saveViewInteraction();
        }
      } catch (error) {
        console.log(error);
        this.recipe = {};
      } finally {
        this.loading = false;
      }
    },

    async submitRating(rating) {
      if (this.isOwnRecipe || !rating) return;

      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.post(
          `http://localhost:5000/api/recipe/rating/${this.id}`,
          {
            username: this.currentUser.displayName,
            rating: rating,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        this.averageRating = response.data.averageRating;
        this.numberOfRatings = response.data.numberOfRatings;

        await axios.post(
          "http://localhost:5000/api/recipe/interaction",
          {
            username: this.currentUser.displayName,
            recipeId: this.id,
            interactionType: "rating",
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );
      } catch (error) {
        console.error("Rating failed:", error);
        await this.getRecipeStatus();
      }
    },

    async saveViewInteraction() {
      try {
        if (this.recipe.username === this.currentUser.displayName) return;

        const token = await this.currentUser.getIdToken();

        await axios.post(
          "http://localhost:5000/api/recipe/interaction",
          {
            username: this.currentUser.displayName,
            recipeId: this.id,
            interactionType: "view",
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );
      } catch (error) {
        console.log(error);
      }
    },

    async toggleFavorite() {
      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.post(
          `http://localhost:5000/api/recipe/favorite/${this.id}`,
          {
            username: this.currentUser.displayName,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        await axios.post(
          "http://localhost:5000/api/recipe/interaction",
          {
            username: this.currentUser.displayName,
            recipeId: this.id,
            interactionType: "favorite",
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        this.isFavorite = response.data.isFavorite;
      } catch (error) {
        console.log(error);
      }
    },

    async getRecipeStatus() {
      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.get(
          `http://localhost:5000/api/recipe/status/${this.id}/${this.currentUser.displayName}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        this.isFavorite = response.data.isFavorite;
        this.userRating = response.data.userRating;
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style scoped>
.recipe-page-container {
  max-width: 1600px;
  padding: 36px 32px;
  background: var(--color-light);
  min-height: 100vh;
}

.recipe-layout {
  display: grid;
  grid-template-columns: minmax(0, 6fr) minmax(0, 4fr);
  align-items: start;
  gap: 24px;
}

/* Main recipe */

.recipe-details-card {
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--surface);
  min-width: 0;
}

.image-wrapper {
  position: relative;
}

.recipe-image {
  width: 100%;
}

.favorite-btn {
  position: absolute;
  top: 18px;
  right: 18px;
  background: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.16);
}

.recipe-content {
  padding: 32px;
}

.recipe-heading {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  flex-wrap: wrap;
}

.recipe-heading h1 {
  color: var(--color-blue);
  font-size: clamp(26px, 2.5vw, 36px);
  font-weight: 900;
  line-height: 1.2;
}

.recipe-author {
  margin-top: 8px;
  color: var(--text-muted);
}

.category-section {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.category-chip {
  background: #fff0df !important;
  color: var(--color-primary) !important;
  font-weight: 700;
}

/* Rating */

.rating-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  margin: 26px 0;
  padding-bottom: 22px;
  border-bottom: 1px solid #eee5dd;
}

.rating-summary,
.rating-input {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-summary strong {
  font-size: 20px;
}

.rating-summary span,
.rating-input span {
  color: var(--text-muted);
  font-size: 13px;
}

.own-recipe-label {
  color: var(--text-muted);
  font-size: 13px;
  font-style: italic;
}

/* Info cards */

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 32px;
}

.info-card {
  background: var(--surface-soft);
  border-radius: 16px;
  padding: 18px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 7px;
}

.info-card .v-icon {
  color: var(--color-primary);
}

.info-card span {
  font-size: 12px;
  color: var(--text-muted);
}

.info-card strong {
  font-size: 14px;
  color: var(--color-dark);
}

/* Ingredients and instructions */

.recipe-section {
  margin-top: 32px;
}

.recipe-section h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--color-blue);
  font-size: 22px;
  font-weight: 900;
  margin-bottom: 18px;
}

.recipe-section h2 .v-icon {
  color: var(--color-primary);
}

.ingredients-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.ingredient-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  background: var(--surface-soft);
  border-radius: 12px;
  font-size: 14px;
}

.ingredient-item strong {
  white-space: nowrap;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.step-card {
  display: flex;
  align-items: flex-start;
  gap: 18px;
  padding: 20px;
  background: var(--surface-soft);
  border-radius: 16px;
}

.step-number {
  color: var(--color-primary);
  font-size: 22px;
  font-weight: 900;
  flex-shrink: 0;
}

.step-card p {
  margin: 0;
  line-height: 1.7;
  color: var(--color-dark);
}

.recipe-footer {
  display: flex;
  justify-content: flex-start;
  margin-top: 32px;
}

/* Recommendations */

.recommendations-panel {
  background: var(--surface);
  border-radius: var(--radius-lg);
  padding: 20px;
  min-width: 0;
  position: sticky;
  top: 64px;
}

.recommendations-heading {
  margin-bottom: 20px;
}

.recommendations-heading h2 {
  color: var(--color-blue);
  font-size: 21px;
  font-weight: 900;
}

.recommendations-heading p {
  color: var(--text-muted);
  font-size: 13px;
  margin-top: 6px;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.recommendation-card {
  background: var(--surface-soft);
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  min-width: 0;
}

.recommendation-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(10, 11, 15, 0.1);
}

.recommendation-image {
  width: 100%;
}

.recommendation-content {
  padding: 10px;
}

.recommendation-content h3 {
  font-size: 12px;
  font-weight: 800;
  color: var(--color-blue);
  line-height: 1.4;
  margin-bottom: 8px;

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.recommendation-meta {
  display: flex;
  justify-content: space-between;
  gap: 6px;
  flex-wrap: wrap;
  font-size: 11px;
  color: var(--text-muted);
}

.recommendation-meta span {
  display: flex;
  align-items: center;
  gap: 3px;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

/* Responsive */

@media (max-width: 1100px) {
  .recipe-layout {
    grid-template-columns: 1fr;
  }

  .recommendations-panel {
    position: static;
  }

  .recommendations-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 700px) {
  .recipe-page-container {
    padding: 16px;
  }

  .recipe-content {
    padding: 20px;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .ingredients-list,
  .recommendations-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .rating-section {
    align-items: flex-start;
    flex-direction: column;
  }

  .step-card {
    padding: 14px;
  }
}

@media (max-width: 420px) {
  .ingredients-list {
    grid-template-columns: 1fr;
  }
}
</style>
