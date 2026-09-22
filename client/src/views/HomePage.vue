<template>
  <Loading v-if="loading" />

  <main v-else class="home-page">
    <section class="hero-section">
      <div>
        <p class="eyebrow">Be Your Own Chef</p>
        <h1>Welcome back, {{ username }}!</h1>
        <p class="hero-subtitle">
          Discover new ideas, revisit recipes and continue building your own
          cookbook.
        </p>
      </div>

      <v-btn class="primary-btn" @click="$router.push('/add-recipe')">
        <v-icon start>mdi-plus</v-icon>
        Add recipe
      </v-btn>
    </section>

    <section class="home-section">
      <div class="section-header">
        <div>
          <h2>Recommended for you</h2>
          <p>Based on your preferences and recipe history.</p>
        </div>
      </div>

      <div class="recipes-scroll">
        <RecipeCard
          v-for="recipe in recommendedRecipes.slice(0, 10)"
          :key="recipe.id"
          :recipe="recipe"
          :isOwnRecipe="false"
        />
      </div>
    </section>

    <section class="home-section">
      <div class="section-header">
        <div>
          <h2>Recently viewed</h2>
          <p>Continue from where you left off.</p>
        </div>
      </div>

      <div v-if="recentlyViewedRecipes.length" class="recipes-scroll">
        <RecipeCard
          v-for="recipe in recentlyViewedRecipes.slice(0, 10)"
          :key="recipe.id"
          :recipe="recipe"
          :isOwnRecipe="false"
        />
      </div>

      <div v-else class="empty-state">
        <h3>No recently viewed recipes yet</h3>
        <p>Open a recipe and it will appear here.</p>
        <v-btn class="primary-btn" @click="$router.push('/explore')">
          Explore recipes
        </v-btn>
      </div>
    </section>

    <section class="home-section">
      <div class="section-header">
        <div>
          <h2>Your recipes</h2>
          <p>Manage the recipes you created.</p>
        </div>

        <v-btn variant="text" @click="$router.push('/profile')">
          View all
        </v-btn>
      </div>

      <div v-if="recipes.length" class="recipes-grid">
        <RecipeCard
          v-for="recipe in recipes.slice(0, 4)"
          :key="recipe.id"
          :recipe="recipe"
          :isOwnRecipe="true"
        />
      </div>

      <div v-else class="empty-state">
        <h3>No recipes yet</h3>
        <p>Create your first recipe and start your personal cookbook.</p>
        <v-btn class="primary-btn" @click="$router.push('/add-recipe')">
          Create recipe
        </v-btn>
      </div>
    </section>
  </main>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
import RecipeCard from "@/components/RecipeCard.vue";
import Loading from "@/components/Loading.vue";
import { VBtn, VIcon } from "vuetify/components";

export default {
  name: "HomePage",

  components: {
    RecipeCard,
    Loading,
    VBtn,
    VIcon,
  },

  data() {
    return {
      recipes: [],
      recommendedRecipes: [],
      recentlyViewedRecipes: [],
      loading: true,
      username: "",
    };
  },
  emits: ["recipe-deleted"],
  computed: {
    ...mapGetters(["currentUser"]),
  },

  mounted() {
    this.getRecipes();
    this.getRecentlyViewedRecipes();
  },

  methods: {
    async getRecipes() {
      try {
        const token = await this.currentUser.getIdToken();
        this.username = this.currentUser.displayName;

        const response = await axios.get(
          `http://localhost:5000/api/recipe/${this.currentUser.displayName}`,
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
        console.log(error);
        this.recipes = [];
      } finally {
        this.loading = false;
      }
    },
    async getRecentlyViewedRecipes() {
      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.get(
          `http://localhost:5000/api/recipe/recently-viewed/${this.currentUser.displayName}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          },
        );

        if (response.status === 200) {
          this.recentlyViewedRecipes = response.data.data;
        }
      } catch (error) {
        console.log(error);
        this.recentlyViewedRecipes = [];
      }
    },
  },
};
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  padding: 42px 7vw;
  background: var(--color-light);
  font-family: "Poppins", sans-serif;
}

.hero-section {
  background: var(--color-blue);
  color: white;
  border-radius: 28px;
  padding: 34px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}

.eyebrow {
  color: var(--color-secondary);
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.14em;
  margin-bottom: 6px;
}

.hero-section h1 {
  font-size: 38px;
  font-weight: 900;
  margin: 0;
}

.hero-subtitle {
  margin-top: 10px;
  opacity: 0.78;
  max-width: 600px;
}

.home-section {
  margin-top: 34px;
  background: #fffdfb;
  border-radius: 26px;
  padding: 28px;
  box-shadow: 0 10px 30px rgba(10, 11, 15, 0.06);
}

.section-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.section-header h2 {
  color: var(--color-blue);
  font-size: 24px;
  font-weight: 900;
  margin: 0;
}

.section-header p {
  color: #756d66;
  margin-top: 4px;
}

.recipe-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}

.primary-btn {
  background: var(--color-primary) !important;
  color: white !important;
  border-radius: 999px;
  font-weight: 800;
}

.empty-state {
  border: 1px dashed #d9c8b8;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  background: #fffaf5;
}

.empty-state h3 {
  color: var(--color-blue);
  font-weight: 900;
}

.empty-state p {
  color: #756d66;
  margin: 8px 0 18px;
}

@media (max-width: 1100px) {
  .recipe-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .hero-section {
    align-items: flex-start;
    flex-direction: column;
  }
}

@media (max-width: 650px) {
  .home-page {
    padding: 24px 14px;
  }

  .recipe-grid {
    grid-template-columns: 1fr;
  }

  .hero-section h1 {
    font-size: 28px;
  }
}
</style>
