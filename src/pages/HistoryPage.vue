<script setup>
import { RouterLink } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import StatCard from '../components/StatCard.vue'
import { apiRoutes } from '../services/api'
import { historyData } from '../data/mockData'

const heatmapColors = ['var(--surface-soft)', '#0e4429', '#006d32', '#26a641', '#39d353']
const chartPoints = ['18%', '30%', '42%', '60%', '75%', '92%']

const statusStyles = {
  Fresh: 'pill--success',
  Normal: 'pill--primary',
  Tired: 'pill--warning',
  Sick: 'pill--danger',
}
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <PageHero
      title="History"
      description="Review workout history, exercise progression, and monthly consistency from one page."
    />

    <SectionCard title="April overview" subtitle="Quick numbers for the current month">
      <div class="grid grid-cols-[repeat(auto-fit,minmax(180px,1fr))] gap-5">
        <StatCard
          v-for="item in historyData.overview"
          :key="item.label"
          :label="item.label"
          :value="item.value"
        />
      </div>
    </SectionCard>

    <div class="grid gap-5 grid-cols-[repeat(auto-fit,minmax(300px,1fr))] md:grid-cols-2">
      <SectionCard title="Recent workouts" subtitle="Newest sessions first">
        <div class="flex flex-col gap-3">
          <article v-for="workout in historyData.recentWorkouts" :key="workout.title" class="p-[18px] bg-surface-soft border border-surface-outline rounded-[28px] max-w-full shadow-custom">
            <div>
              <h3>{{ workout.title }}</h3>
              <p>{{ workout.meta }}</p>
            </div>
            <span class="inline-flex items-center gap-2 w-fit px-3 py-2 rounded-full bg-surface-soft text-text-muted text-[0.8rem] font-bold" :class="statusStyles[workout.flag] || 'pill--warning'">
              {{ workout.flag }}
            </span>
          </article>
        </div>
      </SectionCard>

      <SectionCard title="Exercise progression" subtitle="Open one exercise for detailed history">
        <div class="flex flex-col gap-3">
          <RouterLink
            v-for="exercise in historyData.exerciseLibrary"
            :key="exercise.name"
            class="list-card history-exercise-link"
            :to="`/history/exercises/${encodeURIComponent(exercise.name)}`"
          >
            <div>
              <h3>{{ exercise.name }}</h3>
              <p>{{ exercise.summary }}</p>
            </div>
            <span class="pill pill--primary">Open</span>
          </RouterLink>
        </div>
      </SectionCard>
    </div>

    <div class="grid gap-5 grid-cols-[repeat(auto-fit,minmax(300px,1fr))] md:grid-cols-2">
      <SectionCard title="Activity heatmap" subtitle="Tapable daily workout density">
        <div class="heatmap">
          <div v-for="(row, rowIndex) in historyData.heatmap" :key="rowIndex" class="heatmap__row">
            <span
              v-for="(cell, cellIndex) in row"
              :key="`${rowIndex}-${cellIndex}`"
              class="heatmap__cell"
              :style="{ background: heatmapColors[cell] }"
            />
          </div>
        </div>
      </SectionCard>

      <SectionCard title="Exercise chart sample" subtitle="Preview of the detail page chart">
        <div class="chart-card">
          <div class="chart-card__line">
            <span
              v-for="point in chartPoints"
              :key="point"
              class="chart-card__dot"
              :style="{ bottom: point }"
            />
          </div>
          <div class="chart-card__labels">
            <span v-for="label in historyData.chartLabels" :key="label">{{ label }}</span>
          </div>
        </div>
      </SectionCard>
    </div>

    <SectionCard title="Backend routes" subtitle="Main history endpoints already mapped">
      <div class="api-note api-note--tall">
        <p><strong>GET</strong> {{ apiRoutes.history.stats }}</p>
        <p><strong>GET</strong> {{ apiRoutes.history.heatmap }}</p>
        <p><strong>GET</strong> {{ apiRoutes.history.exercise(':exerciseName') }}</p>
        <p><strong>GET</strong> {{ apiRoutes.history.chart(':exerciseName') }}</p>
      </div>
    </SectionCard>
  </div>
</template>
