<template>
  <main class="admin-page">
    <section class="admin-hero">
      <div>
        <p class="eyebrow">Admin panel</p>
        <h1>Application dashboard</h1>
        <p>Overview of users, recipes and platform interactions.</p>
      </div>
    </section>

    <section class="kpi-grid">
      <div v-for="card in kpiCards" :key="card.label" class="kpi-card">
        <span>{{ card.label }}</span>
        <strong>{{ card.value }}</strong>
        <small>{{ card.info }}</small>
      </div>
    </section>

    <section class="charts-grid">
      <v-card class="dashboard-card">
        <h2>Recipes by category</h2>
        <Bar :data="categoryChartData" :options="chartOptions" />
      </v-card>

      <v-card class="dashboard-card">
        <h2>Recipes by difficulty</h2>
        <Doughnut :data="difficultyChartData" :options="chartOptions" />
      </v-card>

      <v-card class="dashboard-card">
        <h2>Public vs private</h2>
        <Pie :data="visibilityChartData" :options="chartOptions" />
      </v-card>

      <v-card class="dashboard-card">
        <h2>User engagement trend</h2>
        <Line :data="engagementChartData" :options="chartOptions" />
      </v-card>
    </section>

    <section class="tables-grid">
      <v-card class="dashboard-card">
        <h2>User activity</h2>

        <v-table>
          <thead>
            <tr>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Recipes</th>
              <th>Views</th>
              <th>Likes</th>
              <th>Score</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="user in users" :key="user.email">
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>

              <td>
                <v-chip
                  size="small"
                  :class="user.role === 'Admin' ? 'admin-chip' : 'user-chip'"
                >
                  {{ user.role }}
                </v-chip>
              </td>

              <td>
                <v-chip
                  size="small"
                  :class="
                    user.status === 'Active' ? 'active-chip' : 'disabled-chip'
                  "
                >
                  {{ user.status }}
                </v-chip>
              </td>

              <td>{{ user.recipes }}</td>
              <td>{{ user.views }}</td>
              <td>{{ user.likes }}</td>

              <td>
                <v-chip size="small">
                  {{ user.score }}
                </v-chip>
              </td>

              <td>
                <div class="table-actions">
                  <v-btn
                    size="small"
                    variant="text"
                    @click="viewActivity(user)"
                  >
                    View activity
                  </v-btn>

                  <v-btn
                    size="small"
                    variant="text"
                    color="red"
                    @click="toggleStatus(user)"
                  >
                    {{ user.status === "Active" ? "Disable" : "Enable" }}
                  </v-btn>

                  <v-btn
                    size="small"
                    variant="text"
                    :disabled="user.role === 'Admin'"
                    @click="makeAdmin(user)"
                  >
                    Make admin
                  </v-btn>
                </div>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card>

      <v-card class="dashboard-card">
        <h2>Top public recipes</h2>

        <v-table>
          <thead>
            <tr>
              <th>Recipe</th>
              <th>Author</th>
              <th>Views</th>
              <th>Likes</th>
              <th>Rating</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="recipe in topRecipes" :key="recipe.name">
              <td>{{ recipe.name }}</td>
              <td>{{ recipe.author }}</td>
              <td>{{ recipe.views }}</td>
              <td>{{ recipe.likes }}</td>
              <td>{{ recipe.rating }} ⭐</td>
            </tr>
          </tbody>
        </v-table>
      </v-card>
    </section>
  </main>
</template>

<script>
import { VCard, VTable, VChip, VBtn } from "vuetify/components";
import { Bar, Doughnut, Pie, Line } from "vue-chartjs";

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
);

export default {
  name: "AdminDashboard",

  components: {
    VCard,
    VTable,
    VChip,
    Bar,
    Doughnut,
    Pie,
    Line,
    VBtn,
  },

  data() {
    return {
      kpiCards: [
        {
          label: "Total users",
          value: "128",
          info: "+12 this month",
        },
        {
          label: "Total recipes",
          value: "342",
          info: "public and private",
        },
        {
          label: "Total interactions",
          value: "4.8K",
          info: "views, likes, ratings",
        },
        {
          label: "Average rating",
          value: "4.6",
          info: "platform average",
        },
      ],

      users: [
        {
          username: "alexandra",
          email: "alexandra@email.com",
          role: "Admin",
          status: "Active",
          recipes: 12,
          views: 420,
          likes: 86,
          ratings: 34,
          score: 850,
        },
        {
          username: "emma",
          email: "emma@email.com",
          role: "User",
          status: "Active",
          recipes: 8,
          views: 310,
          likes: 64,
          ratings: 20,
          score: 620,
        },
        {
          username: "maria",
          email: "maria@email.com",
          role: "User",
          status: "Disabled",
          recipes: 15,
          views: 590,
          likes: 120,
          ratings: 46,
          score: 1050,
        },
      ],

      topRecipes: [
        {
          name: "Blueberry Pancakes",
          author: "emma",
          views: 230,
          likes: 89,
          rating: 4.9,
        },
        {
          name: "Creamy Chicken Pasta",
          author: "alexandra",
          views: 190,
          likes: 72,
          rating: 4.7,
        },
        {
          name: "Chocolate Lava Cake",
          author: "maria",
          views: 170,
          likes: 68,
          rating: 4.8,
        },
      ],

      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    };
  },
  methods: {
    viewActivity(user) {
      console.log("View activity for:", user.username);
    },

    toggleStatus(user) {
      user.status = user.status === "Active" ? "Disabled" : "Active";
    },

    makeAdmin(user) {
      user.role = "Admin";
    },
  },
  computed: {
    categoryChartData() {
      return {
        labels: ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"],
        datasets: [
          {
            label: "Recipes",
            data: [34, 46, 52, 21, 39],
            backgroundColor: [
              "#C23000",
              "#FCB10A",
              "#14235E",
              "#F7F2ED",
              "#0A0B0F",
            ],
          },
        ],
      };
    },

    difficultyChartData() {
      return {
        labels: ["Easy", "Medium", "Hard"],
        datasets: [
          {
            data: [145, 126, 71],
            backgroundColor: ["#FCB10A", "#C23000", "#14235E"],
          },
        ],
      };
    },

    visibilityChartData() {
      return {
        labels: ["Public", "Private"],
        datasets: [
          {
            data: [218, 124],
            backgroundColor: ["#14235E", "#C23000"],
          },
        ],
      };
    },

    engagementChartData() {
      return {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [
          {
            label: "Interactions",
            data: [320, 480, 620, 900, 1250, 1480],
            borderColor: "#C23000",
            backgroundColor: "#FCB10A",
            tension: 0.35,
          },
        ],
      };
    },
  },
};
</script>

<style scoped>
.admin-page {
  min-height: 100vh;
  padding: 42px 7vw;
  background: var(--color-light);
  font-family: "Poppins", sans-serif;
}

.admin-hero {
  background: var(--color-blue);
  color: white;
  border-radius: 28px;
  padding: 34px;
}

.eyebrow {
  color: var(--color-secondary);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 12px;
}

.admin-hero h1 {
  font-size: 38px;
  font-weight: 900;
  margin: 0;
}

.admin-hero p {
  opacity: 0.78;
  margin-top: 8px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-top: 30px;
}

.kpi-card {
  background: #fffdfb;
  border-radius: 22px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(10, 11, 15, 0.06);
  border-left: 6px solid var(--color-primary);
}

.kpi-card span {
  color: #756d66;
  font-size: 14px;
}

.kpi-card strong {
  display: block;
  color: var(--color-blue);
  font-size: 34px;
  font-weight: 900;
  margin-top: 8px;
}

.kpi-card small {
  color: #756d66;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-top: 30px;
}

.dashboard-card {
  border-radius: 24px;
  padding: 24px;
  height: 360px;
}

.dashboard-card h2 {
  color: var(--color-blue);
  font-weight: 900;
  margin-bottom: 18px;
}

.tables-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  margin-top: 30px;
}

.tables-grid .dashboard-card {
  height: auto;
}

.table-actions {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.admin-chip {
  background: #14235e !important;
  color: white !important;
}

.user-chip {
  background: #f7f2ed !important;
  color: #14235e !important;
}

.active-chip {
  background: #e7f7ed !important;
  color: #1f7a3f !important;
}

.disabled-chip {
  background: #fde8e8 !important;
  color: #b42318 !important;
}

@media (max-width: 1100px) {
  .kpi-grid,
  .charts-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 700px) {
  .admin-page {
    padding: 24px 14px;
  }

  .kpi-grid,
  .charts-grid {
    grid-template-columns: 1fr;
  }

  .admin-hero h1 {
    font-size: 30px;
  }
}
</style>
