<script setup>
import { ref, computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import { apiRoutes } from '../services/api'
import { exerciseLibraryList, historyData } from '../data/mockData'

const heatmapColors = ['var(--surface-soft)', '#0e4429', '#006d32', '#26a641', '#39d353']
const chartPoints = ['18%', '30%', '42%', '60%', '75%', '92%']

const statusStyles = {
  Fresh: 'pill--success',
  Normal: 'pill--primary',
  Tired: 'pill--warning',
  Sick: 'pill--danger',
}

const router = useRouter()
const exerciseSearchQuery = ref('')
const isExerciseSearchOpen = ref(false)

const filteredExercises = computed(() => {
  if (!exerciseSearchQuery.value) return exerciseLibraryList
  return exerciseLibraryList.filter((exerciseName) =>
    exerciseName.toLowerCase().includes(exerciseSearchQuery.value.toLowerCase()),
  )
})

const openExerciseHistory = (exerciseName) => {
  isExerciseSearchOpen.value = false
  router.push(`/history/exercises/${encodeURIComponent(exerciseName)}`)
}

const openExerciseSearch = () => {
  exerciseSearchQuery.value = ''
  isExerciseSearchOpen.value = true
}

const closeExerciseSearch = () => {
  isExerciseSearchOpen.value = false
}

// Calendar Logic
const displayDate = ref(new Date('2026-04-01T00:00:00Z')) // Defaulting to April 2026 to match mock UI state
const currentSystemDate = new Date()

const currentMonthStr = computed(() => {
  return displayDate.value.toLocaleString('default', { month: 'short' })
})
const currentFullMonthStr = computed(() => {
  return displayDate.value.toLocaleString('default', { month: 'long', year: 'numeric' })
})

const prevMonth = () => {
  const current = displayDate.value
  displayDate.value = new Date(current.getFullYear(), current.getMonth() - 1, 1)
}
const nextMonth = () => {
  const current = displayDate.value
  displayDate.value = new Date(current.getFullYear(), current.getMonth() + 1, 1)
}

const calendarDays = computed(() => {
  const ds = displayDate.value
  const year = ds.getFullYear()
  const month = ds.getMonth()
  const daysInMonthLocal = new Date(year, month + 1, 0).getDate()
  
  // getDay() is 0 (Sun) to 6 (Sat)
  // We want 0 (Mon) to 6 (Sun)
  let startDayLocal = new Date(year, month, 1).getDay()
  startDayLocal = startDayLocal === 0 ? 6 : startDayLocal - 1
  
  const days = []
  for (let i = 0; i < startDayLocal; i++) {
    days.push(null)
  }
  
  const monthStr = ds.toLocaleString('default', { month: 'short' })
  
  for (let i = 1; i <= daysInMonthLocal; i++) {
    const isToday = currentSystemDate.getDate() === i && 
                    currentSystemDate.getMonth() === month && 
                    currentSystemDate.getFullYear() === year

    const dailyWorkouts = historyData.recentWorkouts.filter(w => w.title.startsWith(`${monthStr} ${i} -`))
    days.push({
      date: i,
      isToday,
      workouts: dailyWorkouts,
      hasWorkout: dailyWorkouts.length > 0
    })
  }
  return days
})

// Command Palette Modal State
const isCommandPaletteOpen = ref(false)
const selectedDayWorkouts = ref([])
const selectedDayDate = ref(null)

const openCommandPalette = (day) => {
  if (day && day.hasWorkout) {
    selectedDayWorkouts.value = day.workouts
    selectedDayDate.value = day.date
    isCommandPaletteOpen.value = true
  }
}

const closeCommandPalette = () => {
  isCommandPaletteOpen.value = false
}
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <PageHero
      title="History"
      description="Review workout history, exercise progression, and monthly consistency from one page."
    />

    <div class="grid gap-5 grid-cols-[repeat(auto-fit,minmax(300px,1fr))] md:grid-cols-2">
      <!-- Calendar View replacing old Recent Workouts list -->
      <SectionCard title="Recent workouts" subtitle="Click on a highlighted day">
        <div class="bg-surface-soft p-4 rounded-[24px] border border-surface-outline shadow-custom">
          <div class="flex justify-between items-center mb-4 px-2">
            <h3 class="m-0 font-bold text-lg">{{ currentFullMonthStr }}</h3>
            <div class="flex gap-2">
              <button @click="prevMonth" class="w-8 h-8 rounded-full bg-[rgba(255,255,255,0.05)] border border-surface-outline flex items-center justify-center hover:bg-[rgba(255,255,255,0.1)] transition-colors">
                <svg class="w-4 h-4 stroke-current stroke-2 fill-none" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
              </button>
              <button @click="nextMonth" class="w-8 h-8 rounded-full bg-[rgba(255,255,255,0.05)] border border-surface-outline flex items-center justify-center hover:bg-[rgba(255,255,255,0.1)] transition-colors">
                <svg class="w-4 h-4 stroke-current stroke-2 fill-none" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>
              </button>
            </div>
          </div>
          
          <div class="calendar grid grid-cols-7 gap-2">
            <div class="text-center text-[0.75rem] font-bold text-text-muted mb-1">Mo</div>
            <div class="text-center text-[0.75rem] font-bold text-text-muted mb-1">Tu</div>
            <div class="text-center text-[0.75rem] font-bold text-text-muted mb-1">We</div>
            <div class="text-center text-[0.75rem] font-bold text-text-muted mb-1">Th</div>
            <div class="text-center text-[0.75rem] font-bold text-text-muted mb-1">Fr</div>
            <div class="text-center text-[0.75rem] font-bold text-text-muted mb-1">Sa</div>
            <div class="text-center text-[0.75rem] font-bold text-text-muted mb-1">Su</div>

            <div v-for="(day, index) in calendarDays" :key="index"
                 class="aspect-square flex items-center justify-center rounded-[12px] md:rounded-[14px] text-sm font-medium relative transition-all duration-300"
                 :class="[
                   day && !day.hasWorkout && !day.isToday ? 'hover:bg-surface border border-transparent hover:border-surface-outline cursor-default opacity-80' : '',
                   day?.hasWorkout && !day.isToday ? 'cursor-pointer border-transparent bg-[rgba(88,166,255,0.15)] hover:bg-[rgba(88,166,255,0.25)] text-blue font-bold shadow-sm' : '',
                   day?.isToday ? 'border-2 border-blue bg-[rgba(88,166,255,0.1)] text-blue font-extrabold cursor-pointer' : '',
                   day && !day.hasWorkout && !day.isToday ? 'text-text-muted bg-[rgba(255,255,255,0.02)]' : ''
                 ]"
                 @click="openCommandPalette(day)">
              <span v-if="day">{{ day.date }}</span>
              <span v-if="day?.hasWorkout" class="absolute bottom-[10%] w-[5px] h-[5px] rounded-full" :class="day?.isToday ? 'bg-blue' : 'bg-blue'"></span>
            </div>
          </div>
        </div>
      </SectionCard>

      <SectionCard title="Exercise History" subtitle="Search an exercise to open its detail page.">
        <div class="flex flex-col gap-4">
          <button
            type="button"
            class="inline-flex w-full min-h-[52px] items-center justify-center gap-2 rounded-[18px] border border-[rgba(88,166,255,0.24)] bg-[rgba(88,166,255,0.14)] px-5 font-bold text-blue transition-colors hover:bg-[rgba(88,166,255,0.22)]"
            @click="openExerciseSearch"
          >
            <svg class="h-4 w-4 stroke-current stroke-2 fill-none" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="7" />
              <path d="m20 20-3.5-3.5" />
            </svg>
            Search Exercises
          </button>
        </div>
      </SectionCard>
    </div>

    <!-- <div class="grid gap-5 grid-cols-[repeat(auto-fit,minmax(300px,1fr))] md:grid-cols-2">
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
    </div> -->

    <!-- <SectionCard title="Backend routes" subtitle="Main history endpoints already mapped">
      <div class="api-note api-note--tall">
        <p><strong>GET</strong> {{ apiRoutes.history.stats }}</p>
        <p><strong>GET</strong> {{ apiRoutes.history.heatmap }}</p>
        <p><strong>GET</strong> {{ apiRoutes.history.exercise(':exerciseName') }}</p>
        <p><strong>GET</strong> {{ apiRoutes.history.chart(':exerciseName') }}</p>
      </div>
    </SectionCard> -->

    <div v-if="isExerciseSearchOpen" class="fixed inset-0 z-[1300] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm" @click.self="closeExerciseSearch">
      <section class="w-full max-w-[460px] max-h-[80vh] flex flex-col p-6 rounded-[28px] bg-bg-elevated border border-surface-outline shadow-custom">
        <div class="flex items-center justify-between mb-5">
          <h2 class="m-0 text-xl font-extrabold">Select Exercise</h2>
          <button class="p-2 bg-transparent text-text-muted cursor-pointer border-0" @click="closeExerciseSearch">
            <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>

        <div class="relative mb-4">
          <label class="sr-only" for="exercise-search-modal">Search exercise history</label>
          <input
            id="exercise-search-modal"
            v-model="exerciseSearchQuery"
            class="w-full h-[48px] pl-11 pr-4 rounded-xl bg-surface border border-surface-outline text-text font-medium outline-none focus:border-blue transition-colors"
            placeholder="Search exercises..."
            type="text"
            autofocus
          />
          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </div>

        <div class="flex-1 overflow-y-auto pr-1 flex flex-col gap-2 custom-scrollbar">
          <button
            v-for="exerciseName in filteredExercises"
            :key="exerciseName"
            class="w-full text-left p-4 rounded-xl bg-surface-soft border border-surface-outline text-text font-bold hover:bg-surface-soft-hover hover:border-blue transition-colors cursor-pointer"
            @click="openExerciseHistory(exerciseName)"
          >
            {{ exerciseName }}
          </button>

          <div v-if="filteredExercises.length === 0" class="py-12 text-center text-text-muted">
            <p>No results for "{{ exerciseSearchQuery }}"</p>
          </div>
        </div>
      </section>
    </div>

    <!-- Command Palette for Workouts on Selected Day -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="isCommandPaletteOpen" 
             class="fixed inset-0 z-[100] flex flex-col justify-end md:justify-center items-center bg-[rgba(0,0,0,0.6)] backdrop-blur-md"
             @click.self="closeCommandPalette">
          <div class="w-full max-w-md bg-surface border border-surface-outline md:rounded-[28px] rounded-t-[28px] rounded-b-none shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden flex flex-col max-h-[85vh] animate-slide-up md:animate-none">
            <div class="px-6 py-5 border-b border-surface-outline flex justify-between items-center bg-surface-soft">
              <div>
                <h3 class="m-0 font-extrabold text-xl tracking-tight">Workouts on</h3>
                <p class="m-0 text-text-muted mt-0.5">{{ currentMonthStr }} {{ selectedDayDate }}, 2026</p>
              </div>
              <button @click="closeCommandPalette" class="w-10 h-10 flex items-center justify-center rounded-full bg-[rgba(255,255,255,0.05)] border border-surface-outline hover:bg-[rgba(255,255,255,0.1)] hover:scale-105 transition-all text-text-muted">
                <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </button>
            </div>
            
            <div class="p-4 md:p-6 flex flex-col gap-4 overflow-y-auto">
              <div v-if="selectedDayWorkouts.length === 0" class="text-center py-8 text-text-muted">
                <p>No workouts recorded this day.</p>
              </div>
              
              <RouterLink v-for="workout in selectedDayWorkouts" :key="workout.title" 
                       :to="`/history/workout/${encodeURIComponent(workout.title)}`"
                       class="block p-5 bg-gradient-to-b from-[rgba(255,255,255,0.05)] to-transparent border border-surface-outline rounded-[24px] shadow-sm transform transition-all hover:-translate-y-1 hover:shadow-custom hover:border-[rgba(88,166,255,0.4)] cursor-pointer group no-underline">
                <div class="flex justify-between items-start mb-3">
                  <h4 class="m-0 text-lg font-bold group-hover:text-blue transition-colors">{{ workout.title.split('-')[1]?.trim() || workout.title }}</h4>
                  <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[rgba(255,255,255,0.05)] text-text text-[0.75rem] font-bold border border-surface-outline" :class="statusStyles[workout.flag]">
                    <span class="w-1.5 h-1.5 rounded-full bg-current"></span>
                    {{ workout.flag }}
                  </span>
                </div>
                <p class="m-0 text-text-muted text-sm leading-relaxed">{{ workout.meta }}</p>
                
                <div class="mt-4 pt-4 border-t border-[rgba(255,255,255,0.05)] flex items-center justify-between">
                  <span class="text-[0.8rem] text-text-muted font-medium">View detailed summary</span>
                  <svg class="w-4 h-4 text-text-muted group-hover:text-blue transition-colors stroke-current stroke-2 fill-none" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14m-7-7l7 7-7 7"/></svg>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.animate-slide-up {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}
</style>
