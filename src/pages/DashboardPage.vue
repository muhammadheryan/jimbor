<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import StatCard from '../components/StatCard.vue'
import { dashboardData } from '../data/mockData'

const router = useRouter()
const heatmapColors = ['var(--surface-soft)', '#0e4429', '#006d32', '#26a641', '#39d353']
const isStartSplitDialogOpen = ref(false)
const isQuickStartDialogOpen = ref(false)
const workoutFlags = {
  Fresh: {
    tone: 'success',
    paths: ['M12 4.5L14.2 9L19 9.7L15.5 13.1L16.3 18L12 15.7L7.7 18L8.5 13.1L5 9.7L9.8 9Z'],
  },
  Tired: {
    tone: 'warning',
    paths: ['M8 15C9 13.7 10.4 13 12 13C13.6 13 15 13.7 16 15', 'M9 9.5H9.01', 'M15 9.5H15.01', 'M5 12C5 8.13 8.13 5 12 5C15.87 5 19 8.13 19 12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12Z'],
  },
  Normal: {
    tone: 'primary',
    paths: ['M12 6V18', 'M6 12H18'],
  },
}

function openStartSplitDialog() {
  isStartSplitDialogOpen.value = true
}

function closeStartSplitDialog() {
  isStartSplitDialogOpen.value = false
}

function confirmStartSplit() {
  isStartSplitDialogOpen.value = false
  router.push(`/workout/active?split=${encodeURIComponent(dashboardData.nextSplit.name)}`)
}

function openQuickStartDialog() {
  isQuickStartDialogOpen.value = true
}

function closeQuickStartDialog() {
  isQuickStartDialogOpen.value = false
}

function confirmQuickStart() {
  isQuickStartDialogOpen.value = false
  router.push('/workout/active?mode=quickstart')
}
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <PageHero
      title="Jimbor"
      description="See your next split, weekly streak, heatmap consistency, and recent workouts in one place."
    />

    <div class="grid gap-5">
      <SectionCard class="border-[rgba(88,166,255,0.18)]" accent="blue">
        <div class="flex items-center justify-between gap-4">
          <div>
            <p class="m-0 text-text-muted text-[0.78rem] tracking-[0.12em] uppercase">{{ dashboardData.nextSplit.program }}</p>
            <h2 class="m-0 mt-1.5 text-xl font-extrabold leading-[1.1] uppercase">{{ dashboardData.nextSplit.name }}</h2>
            <p class="m-0 mt-1.5 text-text-muted">{{ dashboardData.nextSplit.note }}</p>
          </div>
        </div>

        <div class="grid gap-3 mt-6">
          <button class="w-full inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg transition-opacity active:opacity-80" type="button" @click="openStartSplitDialog">
            Start Split
          </button>
          <button class="w-full inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text transition-colors hover:bg-surface-soft-hover" type="button" @click="openQuickStartDialog">
            Start Empty Workout
          </button>
        </div>
      </SectionCard>

    <div class="grid grid-cols-2 gap-5">
      <StatCard
        v-for="item in dashboardData.stats"
        :key="item.label"
        :label="item.label"
        :value="item.value"
        :note="item.note"
      />
    </div>

    

    <SectionCard title="Activity heatmap" subtitle="Monthly view of your gym consistency">
        <div class="flex flex-col gap-2.5">
          <div v-for="(row, rowIndex) in dashboardData.heatmap" :key="rowIndex" class="grid grid-cols-12 gap-2">
            <span
              v-for="(cell, cellIndex) in row"
              :key="`${rowIndex}-${cellIndex}`"
              class="aspect-square rounded-lg"
              :style="{ background: heatmapColors[cell] }"
            />
          </div>
        </div>
      </SectionCard>
    </div>

    <SectionCard title="Recent workouts" subtitle="Newest sessions first">
      <template #header-actions>
        <RouterLink class="p-0 bg-transparent text-blue font-bold cursor-pointer" to="/history">View all</RouterLink>
      </template>

      <div class="flex flex-col gap-2">
        <article
          v-for="workout in dashboardData.recentWorkouts"
          :key="workout.title"
          class="flex items-center justify-between gap-3.5 px-4 py-3.5 rounded-[18px] bg-surface-soft"
        >
          <div class="min-w-0">
            <h3 class="m-0 text-base font-extrabold">{{ workout.title }}</h3>
            <p class="m-0 mt-1.5 text-text-muted text-[0.86rem]">{{ workout.meta }}</p>
          </div>

          <span
            class="inline-flex items-center justify-center w-10 h-10 shrink-0"
            :class="`text-${(workoutFlags[workout.flag] ?? workoutFlags.Normal).tone}`"
            :title="workout.flag"
            :aria-label="workout.flag"
          >
            <svg class="w-6 h-6 fill-none stroke-current stroke-2" viewBox="0 0 24 24" aria-hidden="true" stroke-linecap="round" stroke-linejoin="round">
              <path
                v-for="path in (workoutFlags[workout.flag] ?? workoutFlags.Normal).paths"
                :key="path"
                :d="path"
              />
            </svg>
          </span>
        </article>
      </div>
    </SectionCard>

    

    <div v-if="isStartSplitDialogOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm" @click.self="closeStartSplitDialog">
      <section class="w-full max-w-[400px] p-6 rounded-[28px] bg-bg-elevated border border-surface-outline shadow-custom">
        <h2 class="m-0 text-xl font-extrabold">Start next split?</h2>
        <p class="m-0 mt-3 mb-6 text-text-soft leading-relaxed">
          Start <strong>{{ dashboardData.nextSplit.name }}</strong> from the
          <strong>{{ dashboardData.nextSplit.program }}</strong> rotation?
        </p>

        <div class="flex gap-3 mt-6">
          <button class="flex-1 inline-flex items-center justify-center gap-2 min-h-[48px] px-4 rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text transition-colors hover:bg-surface-soft-hover" type="button" @click="closeStartSplitDialog">Cancel</button>
          <button class="flex-1 inline-flex items-center justify-center gap-2 min-h-[48px] px-4 rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg transition-opacity active:opacity-80" type="button" @click="confirmStartSplit">Start Split</button>
        </div>
      </section>
    </div>

    <div v-if="isQuickStartDialogOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm" @click.self="closeQuickStartDialog">
      <section class="w-full max-w-[400px] p-6 rounded-[28px] bg-bg-elevated border border-surface-outline shadow-custom">
        <h2 class="m-0 text-xl font-extrabold">Start empty workout?</h2>
        <p class="m-0 mt-3 mb-6 text-text-soft leading-relaxed">
          Open a blank workout session and add exercises manually without using the current program rotation?
        </p>

        <div class="flex gap-3 mt-6">
          <button class="flex-1 inline-flex items-center justify-center gap-2 min-h-[48px] px-4 rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text transition-colors hover:bg-surface-soft-hover" type="button" @click="closeQuickStartDialog">Cancel</button>
          <button class="flex-1 inline-flex items-center justify-center gap-2 min-h-[48px] px-4 rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg transition-opacity active:opacity-80" type="button" @click="confirmQuickStart">Start Empty Workout</button>
        </div>
      </section>
    </div>
  </div>
</template>
