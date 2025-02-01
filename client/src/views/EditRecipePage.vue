<template>
  <div>
    <RecipeForm
      v-if="this.recipe"
      :existingRecipe="this.recipe"
      :isEditing="true"
    />
    <Loading v-else></Loading>
  </div>
</template>

<script>
import axios from "axios";
import RecipeForm from "@/components/RecipeForm.vue";
import { mapGetters } from "vuex";
import Loading from "@/components/Loading.vue";

export default {
  components: {
    RecipeForm,
    Loading,
  },
  computed: {
    ...mapGetters(["currentUser"]),
  },
  data() {
    return {
      recipe: null,
      loading: true,
    };
  },
  mounted() {
    this.getRecipe();
  },
  methods: {
    async getRecipe() {
      const recipeId = this.$route.params.id;

      try {
        const token = await this.currentUser.getIdToken();
        const response = await axios.get(
          `http://localhost:3000/api/recipe/recipe/${recipeId}`,
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
        console.log(error.message);
        this.recipe = null;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
