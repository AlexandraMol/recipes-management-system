<template>
  <main class="profile-page">
    <section class="profile-hero">
      <div>
        <p class="eyebrow">User profile</p>
        <h1>{{ username }}</h1>
        <p>{{ email }}</p>
      </div>

      <v-btn
        class="primary-btn"
        @click="$router.push('/generate-shopping-list')"
      >
        <v-icon start>mdi-cart-outline</v-icon>
        Generate shopping list
      </v-btn>
    </section>

    <section class="profile-section">
      <div class="section-header">
        <div>
          <h2>Excluded ingredients</h2>
          <p>Manage allergies or ingredients you want to avoid.</p>
        </div>
      </div>

      <ExcludedIngredients />
    </section>

    <section class="profile-section">
      <div class="section-header">
        <div>
          <h2>Your recipes</h2>
          <p>Search, edit or delete your own recipes.</p>
        </div>

        <v-btn class="primary-btn" @click="$router.push('/add-recipe')">
          <v-icon start>mdi-plus</v-icon>
          Add recipe
        </v-btn>
      </div>

      <RecipeCollection
        :recipes="recipes"
        :isOwnRecipe="true"
        search-label="Search your recipes"
        empty-title="No recipes found"
        empty-text="Try changing your search filters or add a new recipe."
        icon="mdi-food-fork-drink"
        empty-action-text="Add recipe"
        empty-action-icon="mdi-plus"
        empty-action-route="/add-recipe"
        @recipe-deleted="removeRecipeFromList"
      />
    </section>

    <section class="profile-section">
      <div class="section-header">
        <div>
          <h2>Favorite recipes</h2>
          <p>Recipes you saved from the platform.</p>
        </div>
      </div>
      <RecipeCollection
        :recipes="favoriteRecipes"
        empty-title="No favorite recipes yet"
        empty-text="Explore recipes and save your favorites here."
        icon="mdi-heart-outline"
      />
    </section>

    <section class="profile-section">
      <div class="section-header">
        <div>
          <h2>Recently viewed</h2>
          <p>Recipes you opened recently.</p>
        </div>
      </div>

      <RecipeCollection
        :recipes="recentlyViewedRecipes"
        empty-title="No recently viewed recipes yet"
        empty-text="Open recipes from Explore and they will appear here."
        icon="mdi-history"
      />
    </section>
  </main>
</template>

<script>
import { mapGetters } from "vuex";
import { VBtn, VIcon } from "vuetify/components";
import ExcludedIngredients from "@/components/profile/ExcludedIngredients.vue";
import RecipeCollection from "@/components/recipes/RecipeCollection.vue";
import axios from "axios";

export default {
  name: "ProfilePage",

  components: {
    VBtn,
    VIcon,
    ExcludedIngredients,
    RecipeCollection,
  },

  data() {
    return {
      username: "",
      email: "",
      recipes: [],
      favoriteRecipes: [],
      recentlyViewedRecipes: [],
    };
  },

  computed: {
    ...mapGetters(["currentUser"]),
  },

  methods: {
    removeRecipeFromList(recipeId) {
      this.recipes = this.recipes.filter((recipe) => recipe.id !== recipeId);
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
    async getFavoriteRecipes() {
      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.get(
          `http://localhost:5000/api/recipe/favorites/${this.currentUser.displayName}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        if (response.status === 200) {
          this.favoriteRecipes = response.data.data;
        }
      } catch (error) {
        console.log(error);
        this.favoriteRecipes = [];
      }
    },
  },

  mounted() {
    this.username = this.currentUser?.displayName || "User";
    this.email = this.currentUser?.email || "";
    this.getRecipes();
    this.getRecentlyViewedRecipes();
    this.getFavoriteRecipes();
  },
};
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  padding: 42px 7vw;
  background: var(--color-light);
  font-family: "Poppins", sans-serif;
}

.profile-hero {
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

.profile-hero h1 {
  font-size: 38px;
  font-weight: 900;
  margin: 0;
}

.profile-hero p {
  opacity: 0.78;
}

.profile-section {
  margin-top: 30px;
  background: #fffdfb;
  border-radius: 26px;
  padding: 28px;
  box-shadow: 0 10px 30px rgba(10, 11, 15, 0.06);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
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

.primary-btn {
  background: var(--color-primary) !important;
  color: white !important;
  border-radius: 999px;
  font-weight: 800;
}

.placeholder-box {
  border: 1px dashed #d9c8b8;
  border-radius: 20px;
  background: #fffaf5;
  color: #7b6f65;
  padding: 24px;
  text-align: center;
}

@media (max-width: 800px) {
  .profile-page {
    padding: 24px 14px;
  }

  .profile-hero,
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .profile-hero h1 {
    font-size: 30px;
  }
}
</style>
