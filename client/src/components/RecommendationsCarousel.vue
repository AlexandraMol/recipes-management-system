<template>
  <section v-if="recipes.length" class="recommendations-section">
    <div class="recommendations-header">
      <div>
        <h2>You may also like</h2>
        <p>AI-based recommendations similar to this recipe</p>
      </div>
    </div>

    <div class="recommendations-grid">
      <v-card
        v-for="recipe in visibleRecipes"
        :key="recipe.id"
        class="recommendation-card"
        @click="$router.push(`/recipe/${recipe.id}`)"
      >
        <v-img :src="recipe.imageUrl" height="140" cover />

        <div class="card-content">
          <h3>{{ recipe.name }}</h3>

          <p>
            {{ recipe.difficulty }} · {{ recipe.preparationTime }} min · ⭐
            {{ recipe.averageRating }}
          </p>

          <div class="categories">
            <v-chip
              v-for="category in recipe.category?.slice(0, 2)"
              :key="category"
              size="x-small"
            >
              {{ category }}
            </v-chip>
          </div>
        </div>
      </v-card>
    </div>
  </section>
</template>

<script>
import { VCard, VImg, VChip } from "vuetify/components";

export default {
  name: "RecommendationsCarousel",

  components: {
    VCard,
    VImg,
    VChip,
  },

  props: {
    recipes: {
      type: Array,
      default: () => [],
    },
  },

  computed: {
    visibleRecipes() {
      return this.recipes.slice(0, 4);
    },
  },
};
</script>

<style scoped>
.recommendations-section {
  margin-top: 32px;
}

.recommendations-header {
  margin-bottom: 16px;
}

.recommendations-header h2 {
  font-size: 22px;
  font-weight: 800;
  margin-bottom: 4px;
}

.recommendations-header p {
  color: #777;
  font-size: 14px;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.recommendation-card {
  border-radius: 18px;
  overflow: hidden;
  cursor: pointer;
  transition: 0.2s ease;
}

.recommendation-card:hover {
  transform: translateY(-4px);
}

.card-content {
  padding: 14px;
}

.card-content h3 {
  font-size: 15px;
  font-weight: 800;
  margin-bottom: 6px;
}

.card-content p {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

@media (max-width: 1000px) {
  .recommendations-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .recommendations-grid {
    grid-template-columns: 1fr;
  }
}
</style>
