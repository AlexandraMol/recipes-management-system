<template>
  <div class="recipe-form-page">
    <Toaster ref="toaster" />

    <v-card class="recipe-form-card" elevation="8">
      <div class="form-header">
        <div>
          <p class="recipe-management">Recipe Management</p>
          <h1>{{ isEditing ? "Edit Recipe" : "Create Recipe" }}</h1>
          <p class="subtitle">
            Add the details, ingredients and preparation steps for your recipe.
          </p>
        </div>

        <v-chip class="privacy-toggle">
          {{ recipe.visibility || "Private" }}
        </v-chip>
      </div>

      <v-form class="recipe-form" v-model="valid" @submit.prevent="submitForm">
        <v-container fluid>
          <section class="form-section">
            <h3 class="add-recipe-info">General information</h3>

            <div class="grid two-columns">
              <v-text-field
                v-model="recipe.name"
                label="Recipe name"
                variant="outlined"
                :rules="[(v) => !!v || 'Name is required']"
              />

              <v-select
                v-model="recipe.visibility"
                :items="['Public', 'Private']"
                label="Visibility"
                variant="outlined"
                :rules="[(v) => !!v || 'Visibility is required']"
              />
            </div>

            <v-textarea
              v-model="recipe.description"
              label="Description"
              variant="outlined"
              rows="3"
              :rules="[(v) => !!v || 'Recipe description is required']"
            />

            <div class="image-upload-layout">
              <div class="image-preview">
                <v-img
                  v-if="imagePreviewUrl || recipe.imageUrl"
                  :src="imagePreviewUrl || recipe.imageUrl"
                  cover
                  height="220"
                />

                <div v-else class="empty-image">
                  <v-icon size="42">mdi-image-plus</v-icon>
                  <span>No image selected</span>
                </div>
              </div>

              <div class="image-upload-content">
                <h3 class="add-recipe-info">Recipe image</h3>
                <p>
                  Upload a clear image of the final dish. This will be displayed
                  on recipe cards and detail pages.
                </p>

                <v-file-input
                  label="Choose image"
                  accept="image/*"
                  variant="outlined"
                  prepend-icon="mdi-camera"
                  @update:modelValue="handleImageUpload"
                />
              </div>
            </div>

            <div class="grid three-columns">
              <v-select
                v-model="recipe.difficulty"
                :items="['Easy', 'Medium', 'Hard']"
                label="Difficulty"
                variant="outlined"
                :rules="[(v) => !!v || 'Difficulty is required']"
              />

              <v-text-field
                v-model="recipe.preparationTime"
                label="Preparation time"
                suffix="min"
                type="number"
                variant="outlined"
                :rules="[(v) => !!v || 'Preparation time is required']"
              />

              <v-select
                v-model="recipe.category"
                label="Category"
                :items="['Breakfast', 'Lunch', 'Dinner', 'Snack', 'Dessert']"
                multiple
                chips
                variant="outlined"
                :rules="[(v) => !!v?.length || 'Category is required']"
              />
            </div>
          </section>

          <section class="form-section">
            <div class="section-heading">
              <h3 class="add-recipe-info">Ingredients</h3>

              <v-btn color="primary-btn" variant="flat" @click="addIngredient">
                <v-icon start>mdi-plus</v-icon>
                Add ingredient
              </v-btn>
            </div>

            <div
              v-for="(ingredient, index) in recipe.ingredients"
              :key="index"
              class="dynamic-card"
            >
              <div class="dynamic-card-number">
                {{ index + 1 }}
              </div>

              <div class="grid ingredient-grid">
                <v-text-field
                  v-model="ingredient.name"
                  label="Ingredient name"
                  variant="outlined"
                  density="comfortable"
                  :rules="[(v) => !!v || 'Ingredient name is required']"
                />

                <v-text-field
                  v-model="ingredient.quantity"
                  label="Quantity"
                  type="number"
                  variant="outlined"
                  density="comfortable"
                  :rules="[(v) => !!v || 'Quantity is required']"
                />

                <v-select
                  v-model="ingredient.unit"
                  :items="['g', 'kg', 'ml', 'l', 'pcs', 'tbsp', 'tsp']"
                  label="Unit"
                  variant="outlined"
                  density="comfortable"
                  :rules="[(v) => !!v || 'Unit is required']"
                />

                <v-btn
                  icon
                  variant="text"
                  color="red"
                  @click="removeIngredient(index)"
                >
                  <v-icon>mdi-delete-outline</v-icon>
                </v-btn>
              </div>
            </div>

            <p v-if="!recipe.ingredients.length" class="empty-state">
              No ingredients added yet.
            </p>
          </section>

          <section class="form-section">
            <div class="section-heading">
              <h3 class="add-recipe-info">Preparation steps</h3>

              <v-btn color="primary-btn" variant="flat" @click="addStep">
                <v-icon start>mdi-plus</v-icon>
                Add step
              </v-btn>
            </div>

            <div
              v-for="(step, index) in recipe.steps"
              :key="index"
              class="dynamic-card step-card"
            >
              <div class="dynamic-card-number">
                {{ index + 1 }}
              </div>

              <v-textarea
                v-model="step.description"
                label="Step description"
                rows="3"
                variant="outlined"
                :rules="[(v) => !!v || 'Step description is required']"
              />

              <v-btn
                class="remove-step-btn"
                variant="text"
                color="red"
                @click="removeStep(index)"
              >
                <v-icon start>mdi-delete-outline</v-icon>
                Remove step
              </v-btn>
            </div>

            <p v-if="!recipe.steps.length" class="empty-state">
              No preparation steps added yet.
            </p>
          </section>

          <div class="form-actions">
            <v-btn variant="outlined" @click="cancelForm"> Cancel </v-btn>

            <v-btn variant="outlined" type="submit">
              {{ isEditing ? "Update Recipe" : "Create Recipe" }}
            </v-btn>
          </div>
        </v-container>
      </v-form>
    </v-card>
  </div>
</template>

<script>
import {
  VContainer,
  VForm,
  VTextField,
  VSelect,
  VBtn,
  VTextarea,
  VFileInput,
  VImg,
  VCard,
  VIcon,
  VChip,
} from "vuetify/components";

import axios from "axios";
import { mapGetters } from "vuex";
import Toaster from "@/components/Toaster.vue";
import { storage } from "@/firebase";
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";

export default {
  props: {
    existingRecipe: Object,
    isEditing: Boolean,
  },

  components: {
    VContainer,
    VForm,
    VTextField,
    VSelect,
    VBtn,
    VTextarea,
    VFileInput,
    VImg,
    VCard,
    VIcon,
    VChip,
    Toaster,
  },

  computed: {
    ...mapGetters(["currentUser"]),
  },

  data() {
    return {
      valid: false,
      selectedImageFile: null,
      imagePreviewUrl: "",
      recipe: this.existingRecipe
        ? { ...this.existingRecipe }
        : {
            name: "",
            description: "",
            difficulty: "",
            preparationTime: "",
            ingredients: [],
            steps: [],
            visibility: "Private",
            category: [],
            username: "",
            imageUrl: "",
          },
    };
  },

  methods: {
    addIngredient() {
      this.recipe.ingredients.push({
        name: "",
        quantity: "",
        unit: "g",
      });
    },

    removeIngredient(index) {
      this.recipe.ingredients.splice(index, 1);
    },

    addStep() {
      this.recipe.steps.push({ description: "" });
    },

    removeStep(index) {
      this.recipe.steps.splice(index, 1);
    },

    handleImageUpload(file) {
      const selectedFile = Array.isArray(file) ? file[0] : file;

      if (!selectedFile) return;

      this.selectedImageFile = selectedFile;
      this.imagePreviewUrl = URL.createObjectURL(selectedFile);
    },

    async uploadRecipeImage() {
      if (!this.selectedImageFile) return;

      const fileName = `recipes/${Date.now()}_${this.selectedImageFile.name}`;
      const storageRef = ref(storage, fileName);

      await uploadBytes(storageRef, this.selectedImageFile);

      const downloadURL = await getDownloadURL(storageRef);

      this.recipe.imageUrl = downloadURL;
    },

    cancelForm() {
      this.selectedImageFile = null;

      if (this.imagePreviewUrl) {
        URL.revokeObjectURL(this.imagePreviewUrl);
      }

      this.imagePreviewUrl = "";
      this.$router.back();
    },

    async submitForm() {
      if (!this.valid) return;

      this.recipe.username = this.currentUser.displayName;
      const token = await this.currentUser.getIdToken();

      try {
        await this.uploadRecipeImage();
        if (this.isEditing) {
          await axios.put(
            `http://localhost:5000/api/recipe/edit/${this.$route.params.id}`,
            this.recipe,
            {
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            },
          );
        } else {
          await axios.post(
            "http://localhost:5000/api/recipe/add",
            this.recipe,
            {
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            },
          );
        }

        this.$router.push("/home");
      } catch (error) {
        this.$refs.toaster.showToast(
          error?.response?.data?.error || error.message,
        );
      }
    },
  },
};
</script>

<style scoped>
.info-accent,
.section-heading .add-recipe-info,
.form-section .add-recipe-info {
  color: var(--color-blue);
}

.primary-btn {
  background: var(--color-primary);
  border-radius: 999px;
}

.v-btn.bg-black,
.v-btn[color="black"] {
  background-color: var(--color-primary);
}

.recipe-form {
  width: 100%;
}

.recipe-form-page {
  min-height: 100vh;
  padding: 48px 20px;
  display: flex;
  justify-content: center;
  background: var(--color-light);
  font-family: "Poppins", sans-serif;
}

.recipe-form-card {
  width: 100%;
  max-width: 980px;
  border-radius: 28px;
  overflow: hidden;
  background: white;
}

.privacy-toggle {
  color: white;
}

.form-header {
  padding: 32px;
  background: var(--color-blue);
  color: white;
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: flex-start;
}

.recipe-management {
  text-transform: uppercase;
  color: white;
  letter-spacing: 0.12em;
  font-size: 12px;
  opacity: 0.7;
  margin-bottom: 6px;
}

.form-header h1 {
  font-size: 34px;
  font-weight: 900;
  margin: 0;
}

.subtitle {
  margin-top: 8px;
  opacity: 0.75;
  max-width: 560px;
}

.form-section {
  padding: 28px 8px;
  border-bottom: 1px solid #eee;
}

.form-section .add-recipe-info {
  font-size: 20px;
  font-weight: 850;
  margin-bottom: 18px;
}

.grid {
  display: grid;
  gap: 16px;
}

.two-columns {
  grid-template-columns: repeat(2, 1fr);
}

.three-columns {
  grid-template-columns: 1fr 1fr 1.4fr;
}

.image-upload-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 22px;
  align-items: center;
  margin: 10px 0 24px;
}

.image-preview {
  height: 220px;
  border-radius: 22px;
  overflow: hidden;
  background: #f3f3f3;
  border: 1px dashed #ccc;
}

.empty-image {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  justify-content: center;
  color: #777;
}

.image-upload-content h4 {
  font-size: 18px;
  font-weight: 800;
  margin-bottom: 6px;
}

.image-upload-content p {
  color: #777;
  margin-bottom: 16px;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.dynamic-card {
  position: relative;
  background: var(--color-primary);
  border: 1px solid #eeeeee;
  border-radius: 20px;
  padding: 18px 18px 18px 56px;
  margin-bottom: 14px;
}

.dynamic-card-number {
  position: absolute;
  left: 18px;
  top: 20px;
  width: 28px;
  height: 28px;
  border-radius: 999px;
  background: #111;
  color: white;
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 13px;
}

.ingredient-grid {
  grid-template-columns: 1.5fr 0.8fr 0.8fr auto;
  align-items: center;
}

.step-card {
  padding-bottom: 12px;
}

.remove-step-btn {
  margin-left: auto;
  display: flex;
}

.empty-state {
  color: #888;
  font-style: italic;
  background: #fafafa;
  padding: 16px;
  border-radius: 14px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 26px 8px 10px;
}

@media (max-width: 800px) {
  .form-header {
    flex-direction: column;
  }

  .two-columns,
  .three-columns,
  .ingredient-grid,
  .image-upload-layout {
    grid-template-columns: 1fr;
  }

  .dynamic-card {
    padding-left: 18px;
    padding-top: 58px;
  }

  .recipe-form-page {
    padding: 24px 10px;
  }
}
</style>
