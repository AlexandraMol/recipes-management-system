<template>
  <v-container class="recipe-page-container">
    <v-row justify="center">
      <v-col cols="12" md="9" lg="7">
        <v-card class="recipe-card" elevation="8">
          <div class="image-wrapper">
            <v-img
              height="280px"
              :src="recipe.imageUrl"
              cover
              class="recipe-image"
            />

            <v-btn icon class="favorite-btn" @click="toggleFavorite">
              <v-icon :color="isFavorite ? 'red' : 'grey'">
                {{ isFavorite ? "mdi-heart" : "mdi-heart-outline" }}
              </v-icon>
            </v-btn>
          </div>

          <div class="recipe-content">
            <v-card-title class="recipe-title">
              {{ recipe.name }}
            </v-card-title>

            <v-card-subtitle class="recipe-author">
              Created by: <strong>{{ recipe.username }}</strong>
            </v-card-subtitle>

            <div class="rating-section">
              <v-rating
                v-model="averageRating"
                density="compact"
                half-increments="false"
                hover
                @update:modelValue="submitRating"
              />

              <span class="rating-text">
                {{ averageRating }} / 5 · {{ numberOfRatings }} ratings
              </span>
            </div>

            <div class="info-grid">
              <div class="info-card">
                <v-icon>mdi-clock-outline</v-icon>
                <span>Time</span>
                <strong>{{ recipe.preparationTime }} min</strong>
              </div>

              <div class="info-card">
                <v-icon>mdi-fire</v-icon>
                <span>Difficulty</span>
                <strong>{{ recipe.difficulty }}</strong>
              </div>

              <div class="info-card">
                <v-icon>mdi-eye</v-icon>
                <span>Visibility</span>
                <strong>{{ recipe.visibility }}</strong>
              </div>
            </div>

            <div class="category-section">
              <v-chip
                v-for="category in recipe.category"
                :key="category"
                class="ma-1"
                size="small"
              >
                {{ category }}
              </v-chip>
            </div>

            <v-divider class="my-5" />

            <section>
              <h3 class="section-title">😋 Ingredients</h3>

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

            <v-divider class="my-5" />

            <section>
              <h3 class="section-title">📖 Steps</h3>

              <div class="steps-list">
                <div
                  v-for="(step, index) in recipe.steps"
                  :key="index"
                  class="step-card"
                >
                  <span class="step-number">Step {{ index + 1 }}</span>
                  <p>{{ step.description }}</p>
                </div>
              </div>
            </section>

            <v-divider class="my-5" />

            <v-card-actions class="justify-center">
              <v-btn color="black" @click="$router.push('/')">
                Back to Home
              </v-btn>
            </v-card-actions>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <RecommendationsCarousel
      :recipes="recommendedRecipes"
    ></RecommendationsCarousel>
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
  VIcon,
  VCardActions,
  VBtn,
  VRating,
  VChip,
} from "vuetify/components";

import axios from "axios";
import { mapGetters } from "vuex";
import RecommendationsCarousel from "@/components/RecommendationsCarousel.vue";
export const recommendedRecipesMock = [
  {
    id: "1",
    name: "Canelé",
    username: "Alexandra",
    imageUrl:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSU_oD8dlW6wCPw113c__z8M5Y824-zdOKjH0Za20JAo_M3CWWcubX1guipDrCacawgVedYxcV3Ip28jsUvEMSwsWeIw4avcS-hknBIDg&s=10",
    difficulty: "Easy",
    preparationTime: 25,
    category: ["Dessert"],
    averageRating: 4.77,
    numberOfRatings: 32,
  },
  {
    id: "2",
    name: "Blueberry Pancakes",
    username: "Emma",
    imageUrl: "https://images.unsplash.com/photo-1528207776546-365bb710ee93",
    difficulty: "Easy",
    preparationTime: 20,
    category: ["Breakfast", "Dessert"],
    averageRating: 4.9,
    numberOfRatings: 87,
  },
  {
    id: "3",
    name: "French Toast",
    username: "John",
    imageUrl:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjVpeNUfUF0CVleX6gyAWxdr28QNZGvy3aR5Vu5Nl4aTUCQ0V10J9d_5TRU8jJT1pbob5S6RHfYOQnuFdArCjWflir-nXQ_XNY-SVsMDUhWw&s=10",
    difficulty: "Medium",
    preparationTime: 35,
    category: ["Breakfast", "Dessert"],
    averageRating: 4.55,
    numberOfRatings: 45,
  },
  {
    id: "4",
    name: "Chocolate Lava Cake",
    username: "Maria",
    imageUrl: "https://images.unsplash.com/photo-1563805042-7684c019e1cb",
    difficulty: "Hard",
    preparationTime: 50,
    category: ["Dessert"],
    averageRating: 4.88,
    numberOfRatings: 120,
  },
  {
    id: "5",
    name: "Avocado Toast",
    username: "Daniel",
    imageUrl: "https://images.unsplash.com/photo-1541519227354-08fa5d50c44d",
    difficulty: "Easy",
    preparationTime: 10,
    category: ["Breakfast", "Snack"],
    averageRating: 4.3,
    numberOfRatings: 21,
  },
];
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
  },

  data() {
    return {
      recipe: {},
      loading: true,
      isFavorite: false,
      averageRating: 0,
      numberOfRatings: 0,
      averageRating: 0,
      recommendedRecipes: recommendedRecipesMock,
    };
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

    async submitRating() {
      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.post(
          `http://localhost:5000/api/recipe/rating/${this.id}`,
          {
            username: this.currentUser.displayName,
            rating: this.averageRating,
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
            interactionType: "rating",
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        this.averageRating = response.data.averageRating;
        this.numberOfRatings = response.data.numberOfRatings;
      } catch (error) {
        console.log(error);
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
  padding-top: 32px;
  padding-bottom: 32px;
}

.recipe-card {
  border-radius: 24px;
  overflow: hidden;
}

.image-wrapper {
  position: relative;
}

.recipe-image {
  width: 100%;
}

.favorite-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
}

.recipe-content {
  padding: 28px;
}

.recipe-title {
  justify-content: center;
  text-align: center;
  font-size: 28px;
  font-weight: 800;
}

.recipe-author {
  text-align: center;
  margin-top: 4px;
}

.rating-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  margin: 16px 0 24px;
}

.rating-text {
  font-size: 14px;
  color: #666;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin: 24px 0;
}

.info-card {
  background: #f7f7f7;
  border-radius: 18px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.info-card span {
  font-size: 13px;
  color: #777;
}

.category-section {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.section-title {
  font-size: 18px;
  font-weight: 800;
  margin-bottom: 14px;
}

.ingredients-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ingredient-item {
  display: flex;
  justify-content: space-between;
  background: #fafafa;
  border-radius: 14px;
  padding: 12px 16px;
}

.step-card {
  background: #fafafa;
  border-radius: 16px;
  padding: 18px;
  margin-bottom: 14px;
}

.step-number {
  display: block;
  font-weight: 800;
  margin-bottom: 8px;
}

.step-card p {
  margin: 0;
  line-height: 1.6;
}

@media (max-width: 700px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .recipe-content {
    padding: 20px;
  }
}
</style>
