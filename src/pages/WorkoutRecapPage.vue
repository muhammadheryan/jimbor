<script setup>
import { RouterLink } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import StatCard from '../components/StatCard.vue'
import { recapData } from '../data/mockData'
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
      <PageHero
        title="Workout Recap"
        :description="`${recapData.date} - ${recapData.duration}`"
      />
      
    <div class="grid gap-5 grid-cols-1 lg:grid-cols-2">
      <SectionCard title="Session summary" subtitle="Everything you logged in this workout">
        <div class="grid grid-cols-2 gap-5">
          <StatCard
            v-for="item in recapData.summary"
            :key="item.label"
            :label="item.label"
            :value="item.value"
          />
        </div>
      </SectionCard>

      <SectionCard title="New PRs" subtitle="Top personal records from today">
        <div v-if="recapData.prs && recapData.prs.length > 0" class="flex flex-col gap-3">
          <article v-for="item in recapData.prs" :key="item.name" class="p-[18px] bg-surface-soft border border-surface-outline rounded-[28px] max-w-full shadow-custom flex items-center justify-between gap-4">
            <div>
              <h3 class="m-0 text-[1.25rem] font-extrabold">{{ item.name }}</h3>
              <p class="mt-1.5 mb-0 text-text-muted">{{ item.note }}</p>
            </div>
            <strong class="m-0 mt-2.5 text-[clamp(1.9rem,4vw,3rem)] font-black leading-none break-words text-green shrink-0">{{ item.value }}</strong>
          </article>
        </div>
        <div v-else class="flex flex-col items-center justify-center py-10 px-4 text-center bg-surface-soft border border-dashed border-surface-outline rounded-[28px]">
          <div class="w-16 h-16 bg-blue/10 text-blue rounded-full flex items-center justify-center mb-4">
            <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path><path d="M4 22h16"></path><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path></svg>
          </div>
          <h3 class="m-0 text-lg font-bold mb-2">No PRs this time!</h3>
          <p class="m-0 text-text-muted leading-relaxed">Consistency is the key to greatness. Maintain your form and the records will follow soon! 🔥</p>
        </div>
      </SectionCard>
    </div>

    <div class="flex flex-col gap-4 mt-3">
      <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[56px] px-[18px] rounded-[22px] font-black text-[1.05rem] cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg shadow-custom" to="/dashboard">Save & Go Home</RouterLink>
    </div>
  </div>
</template>
