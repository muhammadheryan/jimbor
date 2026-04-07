<script setup>
import { RouterLink } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import StatCard from '../components/StatCard.vue'
import { apiRoutes } from '../services/api'
import { programsData } from '../data/mockData'
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <PageHero
      title="Programs Management"
      description="Create, activate, edit, and review your workout programs from one place."
    />

    <div class="grid gap-5 grid-cols-1 lg:grid-cols-2">
      <SectionCard :title="programsData.activeProgram.name" subtitle="Current program in rotation" accent="blue">
        <div class="grid grid-cols-[repeat(2,minmax(0,1fr))] gap-4">
          <div>
            <StatCard label="Splits" :value="String(programsData.activeProgram.splits)" />
          </div>

          <div>
            <StatCard label="Exercises" :value="String(programsData.activeProgram.exercises)" />
          </div>

          <div class="col-span-full">
            <StatCard label="Next split" :value="programsData.activeProgram.nextSplit" />
          </div>
        </div>

        <div class="flex flex-wrap items-stretch gap-4 mt-3 [&>*]:flex-1">
          <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" to="/programs/split-selector">Start Programs</RouterLink>
        </div>
      </SectionCard>
    </div>

    <SectionCard title="My Programs" subtitle="Manage draft, active, and archived structures">
      <div class="flex flex-wrap items-stretch gap-4 mb-4 [&>*]:flex-1">
        <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" to="/programs/create">Add Program</RouterLink>
      </div>

      <div class="grid grid-cols-[repeat(auto-fit,minmax(240px,1fr))] gap-5">
        <article v-for="program in programsData.programs" :key="program.id" class="w-full max-w-full p-6 border border-surface-outline rounded-[28px] bg-gradient-to-b from-[rgba(22,27,34,0.98)] to-[rgba(15,20,27,0.98)] shadow-custom">
          <div class="flex items-center justify-between gap-4">
            <h3 class="m-0 text-[1.25rem] font-extrabold">{{ program.name }}</h3>
            <div class="flex items-center gap-3">
              <span class="inline-flex items-center gap-2 w-fit px-3 py-2 rounded-full text-[0.8rem] font-bold" :class="program.status === 'Active' ? 'bg-[rgba(57,211,83,0.12)] text-green' : program.status === 'Draft' ? 'bg-[rgba(210,153,34,0.14)] text-yellow' : 'bg-surface-soft text-text-muted'">
                {{ program.status }}
              </span>
              <RouterLink class="inline-flex items-center justify-center w-9 h-9 rounded-xl border border-surface-outline bg-surface-soft text-text" :to="`/programs/${program.id}`" aria-label="Edit program">
                <svg class="w-[18px] h-[18px] fill-none stroke-current stroke-2 [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M4 20H8L18 10L14 6L4 16V20Z" />
                  <path d="M12.5 7.5L16.5 11.5" />
                  <path d="M14 6L16 4C16.8 3.2 18.2 3.2 19 4L20 5C20.8 5.8 20.8 7.2 20 8L18 10" />
                </svg>
              </RouterLink>
            </div>
          </div>

          <p class="text-text-muted mt-2 mb-4">{{ program.subtitle }}</p>

          <div class="flex flex-row flex-wrap gap-3">
            <span v-for="tag in program.tags" :key="tag" class="inline-flex items-center gap-2 w-fit px-3 py-2 rounded-full bg-surface-soft text-text-muted text-[0.8rem] font-bold">{{ tag }}</span>
          </div>
        </article>
      </div>
    </SectionCard>
  </div>
</template>
