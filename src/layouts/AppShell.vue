<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Programs', to: '/programs' },
  { label: 'Active Workout', to: '/workout/active' },
  { label: 'History', to: '/history' },
  { label: 'PT Zone', to: '/pt-zone' },
]

const mobileItems = computed(() => [
  {
    label: 'Home',
    to: '/dashboard',
    icon: ['M4 11.5L12 5L20 11.5', 'M6.5 10.5V19H17.5V10.5', 'M10 19V14H14V19'],
  },
  {
    label: 'Programs',
    to: '/programs',
    icon: ['M5 6.5H19', 'M5 12H19', 'M5 17.5H19', 'M7 4.5V8.5', 'M17 10V14', 'M11 15.5V19.5'],
  },
  {
    label: 'Workout',
    to: '/workout/active',
    icon: ['M3.5 9.5H6.5V14.5H3.5', 'M17.5 9.5H20.5V14.5H17.5', 'M6.5 11H17.5', 'M8.5 8V16', 'M15.5 8V16'],
  },
  {
    label: 'History',
    to: '/history',
    icon: ['M12 6V12L16 14', 'M20 12A8 8 0 1 1 17.66 6.34', 'M20 4V8H16'],
  },
  {
    label: 'PT',
    to: '/pt-zone',
    icon: ['M12 12C13.93 12 15.5 10.43 15.5 8.5C15.5 6.57 13.93 5 12 5C10.07 5 8.5 6.57 8.5 8.5C8.5 10.43 10.07 12 12 12Z', 'M5.5 19C6.28 16.67 8.88 15 12 15C15.12 15 17.72 16.67 18.5 19', 'M18 9H22', 'M20 7V11'],
  },
])

const pageLabel = computed(() => navItems.find((item) => route.path.startsWith(item.to))?.label ?? 'Jimbor')
</script>

<template>
  <div class="min-h-screen overflow-x-hidden lg:grid lg:grid-cols-[var(--sidebar-width)_1fr] lg:gap-6 lg:p-6">
    <aside class="hidden lg:flex lg:flex-col lg:gap-6 lg:min-h-[calc(100vh-48px)] lg:p-6 lg:border lg:border-surface-outline lg:rounded-[32px] lg:bg-gradient-to-b lg:from-[rgba(22,27,34,0.98)] lg:to-[rgba(15,20,27,0.98)] lg:shadow-custom">
      <RouterLink class="inline-block text-[3rem] leading-[0.9] font-black tracking-[0.08em]" to="/dashboard">JIMBOR</RouterLink>
      <p class="text-text-muted">Gym tracker PWA</p>

      <nav class="flex flex-col gap-2.5">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="px-4 py-[14px] rounded-[18px] text-text-muted bg-surface-soft transition-colors"
          :class="{ 'bg-[rgba(88,166,255,0.16)] text-text font-bold': route.path.startsWith(item.to) }"
        >
          {{ item.label }}
        </RouterLink>
      </nav>

      <div class="mt-auto p-6 border border-surface-outline rounded-[28px] bg-gradient-to-b from-[rgba(22,27,34,0.98)] to-[rgba(15,20,27,0.98)] shadow-custom">
        <p class="m-0 text-text-muted text-[0.78rem] tracking-[0.12em] uppercase">Current focus</p>
        <h3 class="m-0 mt-1.5 text-xl font-extrabold">{{ pageLabel }}</h3>
        <p class="text-text-muted mt-2">Responsive layout automatically shifts between mobile stack and desktop panels.</p>
      </div>
    </aside>

    <div class="w-full min-w-0 px-4 pt-5 pb-[108px] lg:p-0 lg:pb-10">
      <div class="hidden lg:flex items-start justify-end gap-3 mb-6">
        <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" to="/programs/split-selector">Split Selector</RouterLink>
        <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer bg-gradient-to-b from-blue to-blue-strong text-bg" to="/programs/builder">Program Builder</RouterLink>
      </div>

      <main class="w-full">
        <slot />
      </main>
    </div>

    <nav class="fixed bottom-0 left-0 right-0 z-50 flex items-center justify-around px-4 py-3 pb-[calc(12px+env(safe-area-inset-bottom))] bg-[rgba(13,17,23,0.85)] backdrop-blur-xl border-t border-surface-outline lg:hidden">
      <RouterLink
        v-for="item in mobileItems"
        :key="item.to"
        :to="item.to"
        class="relative flex flex-col items-center justify-center min-w-[64px] h-12 text-text-muted transition-all duration-300"
        :class="{ 'text-blue': route.path.startsWith(item.to) }"
      >
        <div 
          class="absolute inset-0 scale-90 opacity-0 transition-all duration-300 rounded-2xl bg-[rgba(88,166,255,0.12)]"
          :class="{ 'scale-100 opacity-100': route.path.startsWith(item.to) }"
        ></div>
        
        <svg class="relative z-10 w-6 h-6 fill-none stroke-current stroke-[2.2]" viewBox="0 0 24 24" aria-hidden="true" stroke-linecap="round" stroke-linejoin="round">
          <path
            v-for="path in item.icon"
            :key="path"
            :d="path"
          />
        </svg>
        
        <div 
          class="absolute -bottom-1.5 w-1 h-1 rounded-full bg-blue transition-all duration-300 scale-0"
          :class="{ 'scale-100': route.path.startsWith(item.to) }"
        ></div>
        
        <span class="sr-only">{{ item.label }}</span>
      </RouterLink>
    </nav>
  </div>
</template>
