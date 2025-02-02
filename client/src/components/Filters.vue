<template>
  <div class="filters-container">
    <v-chip-group
      v-model="selected"
      multiple
      @update:modelValue="updateFilters"
    >
      <v-chip
        v-for="filter in filters"
        :key="filter"
        :value="filter"
        variant="elevated"
        color="primary"
      >
        {{ filter }}
      </v-chip>
    </v-chip-group>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { VChipGroup, VChip } from "vuetify/components";

export default {
  data() {
    return {
      selected: [],
      filters: ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"],
    };
  },
  components: {
    VChipGroup,
    VChip,
  },
  computed: {
    ...mapGetters(["getSelectedFilters"]),
  },
  watch: {
    selected(newFilters) {
      this.updateFilters(newFilters);
    },
  },
  mounted() {
    this.selected = [...this.getSelectedFilters];
  },
  methods: {
    ...mapActions(["updateFilters"]),
  },
};
</script>

<style>
.filters-container {
  display: flex;
  justify-content: center;
}
</style>
