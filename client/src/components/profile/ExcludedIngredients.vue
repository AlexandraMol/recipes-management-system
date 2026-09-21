<template>
  <div class="excluded-box">
    <div class="input-row">
      <v-text-field
        v-model="ingredientInput"
        label="Add excluded ingredient or allergy"
        variant="outlined"
        density="comfortable"
        @keyup.enter="addIngredient"
      />

      <v-btn class="primary-btn" @click="addIngredient">
        <v-icon start>mdi-plus</v-icon>
        Add
      </v-btn>
    </div>

    <div v-if="excludedIngredients.length" class="chips">
      <v-chip
        v-for="ingredient in excludedIngredients"
        :key="ingredient"
        closable
        class="excluded-chip"
        @click:close="removeIngredient(ingredient)"
      >
        {{ ingredient }}
      </v-chip>
    </div>

    <p v-else class="empty-text">No excluded ingredients added yet.</p>

    <div class="actions">
      <v-btn
        variant="outlined"
        :disabled="!hasChanges"
        @click="saveExcludedIngredients"
      >
        Save preferences
      </v-btn>
    </div>
  </div>
</template>

<script>
import { VTextField, VBtn, VIcon, VChip } from "vuetify/components";

import axios from "axios";
import { mapGetters } from "vuex";

export default {
  name: "ExcludedIngredients",

  components: {
    VTextField,
    VBtn,
    VIcon,
    VChip,
  },

  data() {
    return {
      ingredientInput: "",
      excludedIngredients: [],
      originalIngredients: [],
    };
  },

  computed: {
    ...mapGetters(["currentUser"]),

    hasChanges() {
      return (
        JSON.stringify(this.excludedIngredients) !==
        JSON.stringify(this.originalIngredients)
      );
    },
  },

  mounted() {
    this.getExcludedIngredients();
  },

  methods: {
    addIngredient() {
      const value = this.ingredientInput.trim().toLowerCase();

      if (!value) return;

      if (!this.excludedIngredients.includes(value)) {
        this.excludedIngredients.push(value);
      }

      this.ingredientInput = "";
    },

    removeIngredient(ingredient) {
      this.excludedIngredients = this.excludedIngredients.filter(
        (item) => item !== ingredient,
      );
    },

    async getExcludedIngredients() {
      try {
        const token = await this.currentUser.getIdToken();

        const response = await axios.get(
          "http://localhost:5000/api/user/preferences",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        this.excludedIngredients =
          response.data.data?.excludedIngredients || [];

        this.originalIngredients = [...this.excludedIngredients];
      } catch (error) {
        console.error(error.message);
      }
    },

    async saveExcludedIngredients() {
      try {
        const token = await this.currentUser.getIdToken();

        await axios.put(
          "http://localhost:5000/api/user/preferences",
          {
            excludedIngredients: this.excludedIngredients,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        this.originalIngredients = [...this.excludedIngredients];
      } catch (error) {
        console.error(error.message);
      }
    },
  },
};
</script>

<style scoped>
.excluded-box {
  background: #fffaf5;
  border: 1px solid #eadccd;
  border-radius: 20px;
  padding: 22px;
}

.input-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  align-items: start;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

.excluded-chip {
  background: #f7f2ed !important;
  color: #14235e !important;
  font-weight: 600;
}

.empty-text {
  color: #7b6f65;
  font-style: italic;
  margin-top: 10px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.primary-btn {
  background: #c23000 !important;
  color: white !important;
  border-radius: 999px;
  font-weight: 800;
}

@media (max-width: 700px) {
  .input-row {
    grid-template-columns: 1fr;
  }
}
</style>
