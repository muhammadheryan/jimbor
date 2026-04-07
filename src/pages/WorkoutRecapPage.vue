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
      :description="`${recapData.date} - ${recapData.duration} - Flag ${recapData.flag}`"
    />

    <div class="grid gap-5 grid-cols-1 lg:grid-cols-2">
      <SectionCard title="Session summary" subtitle="Everything you logged in this workout">
        <div class="grid grid-cols-[repeat(auto-fit,minmax(180px,1fr))] gap-5">
          <StatCard
            v-for="item in recapData.summary"
            :key="item.label"
            :label="item.label"
            :value="item.value"
          />
        </div>
      </SectionCard>

      <SectionCard title="New PRs" subtitle="Top personal records from today">
        <div class="flex flex-col gap-3">
          <article v-for="item in recapData.prs" :key="item.name" class="p-[18px] bg-surface-soft border border-surface-outline rounded-[28px] max-w-full shadow-custom flex items-center justify-between gap-4">
            <div>
              <h3 class="m-0 text-[1.25rem] font-extrabold">{{ item.name }}</h3>
              <p class="mt-1.5 mb-0 text-text-muted">{{ item.note }}</p>
            </div>
            <strong class="m-0 mt-2.5 text-[clamp(1.9rem,4vw,3rem)] font-black leading-none break-words text-green shrink-0">{{ item.value }}</strong>
          </article>
        </div>
      </SectionCard>
    </div>

    <div class="flex flex-col gap-4 mt-3">
      <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[56px] px-[18px] rounded-[22px] font-black text-[1.05rem] cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg shadow-custom" to="/dashboard">Save & Go Home</RouterLink>
    </div>
  </div>
</template>
