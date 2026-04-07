<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import StatCard from '../components/StatCard.vue'
import { historyWorkoutDetailData } from '../data/mockData'

const route = useRoute()
const router = useRouter()
const dateParam = route.params.date

const workoutTitle = computed(() => {
  if (!dateParam) return 'Workout Detail'
  const decoded = decodeURIComponent(dateParam)
  return decoded.split('-')[1]?.trim() || decoded
})

const recapData = historyWorkoutDetailData
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <div class="flex items-center gap-4">
      <button @click="router.back()" class="w-10 h-10 flex shrink-0 items-center justify-center rounded-full bg-surface-soft border border-surface-outline hover:bg-surface-outline transition-colors text-text-muted">
        <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <PageHero
        :title="workoutTitle"
        :description="`Session finished in ${recapData.duration}`"
        class="flex-1"
      />
    </div>

    <div class="grid gap-5 grid-cols-1 lg:grid-cols-[1fr_2fr]">
      <!-- Left: Summary -->
      <div class="flex flex-col gap-5">
        <SectionCard title="Session summary" subtitle="Performance overview">
          <div class="grid grid-cols-2 gap-5">
            <StatCard
              v-for="item in recapData.summary"
              :key="item.label"
              :label="item.label"
              :value="item.value"
            />
          </div>
        </SectionCard>
      </div>

      <!-- Right: Exercise List -->
      <SectionCard title="Logged exercises" subtitle="Sets, weight, and reps">
        <div class="flex flex-col gap-4">
          <div v-for="ex in recapData.exercises" :key="ex.name" 
               class="bg-surface-soft border border-surface-outline rounded-[24px] p-5 shadow-custom">
            <h3 class="m-0 mb-4 text-lg font-bold">{{ ex.name }}</h3>
            
            <div class="flex flex-col gap-2">
              <div v-for="(set, index) in ex.sets" :key="index" 
                   class="flex items-center justify-between py-2 border-b border-surface-outline last:border-0">
                <div class="flex items-center gap-3">
                  <span class="w-6 h-6 flex items-center justify-center bg-[rgba(255,255,255,0.05)] rounded-full text-[0.7rem] font-bold text-text-muted">
                    {{ index + 1 }}
                  </span>
                  <span class="font-bold text-lg text-text">{{ set.weight }}</span>
                </div>
                <div class="text-text-muted font-medium">
                  {{ set.reps }} <span class="text-xs uppercase tracking-wider opacity-60">reps</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </SectionCard>
    </div>
  </div>
</template>
