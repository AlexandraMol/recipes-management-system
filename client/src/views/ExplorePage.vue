<template>
  <Loading v-if="loading" />

  <main v-else class="explore-page">
    <div class="explore-header">
      <div>
        <p class="eyebrow">Explore</p>
        <h1>Discover recipes</h1>
        <p class="subtitle">
          Search by recipe, ingredient or category, or use advanced filters to
          find something that fits what you have available.
        </p>
      </div>
    </div>

    <div class="search-container">
      <SearchBar @results="handleSearchResults" />
    </div>

    <div v-if="recipes.length" class="recipes-grid">
      <RecipeCard
        v-for="recipe in recipes"
        :key="recipe.id"
        :recipe="recipe"
        :isOwnRecipe="false"
      />
    </div>

    <div v-else class="empty-state">
      <h3>No recipes found</h3>
      <p>Try changing your search or filters.</p>
    </div>
  </main>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

import RecipeCard from "@/components/RecipeCard.vue";
import Loading from "@/components/Loading.vue";
import SearchBar from "@/components/SearchBar.vue";

export default {
  name: "Explore",

  components: {
    RecipeCard,
    Loading,
    SearchBar,
  },

  data() {
    return {
      recipes: [],
      loading: true,
    };
  },

  computed: {
    ...mapGetters(["currentUser"]),
  },

  mounted() {
    this.getRecipes();
  },

  methods: {
    handleSearchResults(results) {
      this.recipes = results;
    },

    async getRecipes() {
      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.get(
          `http://localhost:5000/api/recipe/otherRecipes/${this.currentUser.displayName}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          },
        );

        if (response.status === 200) {
          this.recipes = response.data.data;
        }
      } catch (error) {
        console.error(error);
        this.recipes = [];
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.explore-page {
  min-height: 100vh;
  padding: 42px 7vw;
  background: var(--color-light);
  font-family: "Poppins", sans-serif;
}

.explore-header {
  margin-bottom: 26px;
}

.eyebrow {
  color: var(--color-primary);
  text-transform: uppercase;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.14em;
  margin-bottom: 6px;
}

.explore-header h1 {
  color: var(--color-blue);
  font-size: 38px;
  font-weight: 900;
  margin: 0;
}

.subtitle {
  color: #756d66;
  margin-top: 8px;
  max-width: 700px;
}

.search-container {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.empty-state {
  margin-top: 24px;
}

@media (max-width: 650px) {
  .explore-page {
    padding: 24px 14px;
  }

  .explore-header h1 {
    font-size: 30px;
  }
}
</style>
