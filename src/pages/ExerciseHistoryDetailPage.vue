<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import { historyData } from '../data/mockData'

const route = useRoute()

const exerciseName = computed(() => decodeURIComponent(route.params.exerciseName ?? ''))
const exerciseDetail = computed(
  () => historyData.exerciseLibrary.find((item) => item.name.toLowerCase() === exerciseName.value.toLowerCase()) ?? historyData.exerciseLibrary[0],
)
const chartPoints = ['24%', '42%', '56%', '78%']
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <PageHero
      :title="exerciseDetail.name"
      :description="exerciseDetail.note"
    />

    <div class="flex flex-wrap items-center justify-end gap-4">
      <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" to="/history">Back to History</RouterLink>
    </div>

    <div class="grid gap-5 grid-cols-[repeat(auto-fit,minmax(300px,1fr))] md:grid-cols-2">
      <SectionCard title="Overview" subtitle="Latest performance snapshot">
        <div class="flex flex-col gap-3">
          <article class="p-[18px] bg-surface-soft border border-surface-outline rounded-[28px] max-w-full shadow-custom">
            <h3>{{ exerciseDetail.summary }}</h3>
            <p>{{ exerciseDetail.note }}</p>
          </article>
        </div>
      </SectionCard>

      <SectionCard title="Progression" subtitle="Recent top set trend">
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
            <span v-for="label in exerciseDetail.chartLabels" :key="label">{{ label }}</span>
          </div>
        </div>
      </SectionCard>
    </div>

    <SectionCard title="Session history" subtitle="Newest entries first">
      <div class="flex flex-col gap-3">
        <article
          v-for="session in exerciseDetail.sessions"
          :key="`${session.date}-${session.detail}`"
          class="list-card exercise-history-detail__row"
        >
          <div>
            <h3>{{ session.date }}</h3>
            <p>{{ session.detail }}</p>
          </div>

          <span class="inline-flex items-center gap-2 w-fit px-3 py-2 rounded-full bg-surface-soft text-text-muted text-[0.8rem] font-bold" :class="session.flag === 'Fresh' ? 'pill--success' : 'pill--warning'">
            {{ session.flag }}
          </span>
        </article>
      </div>
    </SectionCard>
  </div>
</template>
