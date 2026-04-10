<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { activeWorkoutData, dashboardData, exerciseLibraryList, programBuilderData, historyData } from '../data/mockData'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'

const router = useRouter()
const route = useRoute()

const isActive = computed(() => !!(route.query.split || route.query.mode))
const splitName = computed(() => {
  if (route.query.mode === 'quickstart') return 'Custom Workout'
  return route.query.split || activeWorkoutData.session.title
})

const workoutQueue = ref([])

// Helper to find history for an exercise name
const getExerciseHistory = (name) => {
  const libEntry = historyData.exerciseLibrary.find(ex => ex.name.toLowerCase() === name.toLowerCase())
  if (libEntry && libEntry.sessions) {
    return libEntry.sessions.map(s => ({
      date: s.date,
      summary: s.detail,
      flag: s.flag
    }))
  }
  return []
}

// Initialize queue based on mode or split
if (route.query.mode === 'quickstart') {
  workoutQueue.value = []
} else if (route.query.split) {
  const chosenSplit = programBuilderData.splits.find(s => s.name.toLowerCase() === String(route.query.split).toLowerCase())
  if (chosenSplit) {
    workoutQueue.value = chosenSplit.exercises.map(ex => ({
      name: ex.name,
      badge: ex.meta || '',
      sets: [],
      history: getExerciseHistory(ex.name),
      helper: ex.target || '',
    }))
  } else {
    workoutQueue.value = JSON.parse(JSON.stringify(activeWorkoutData.queue))
  }
} else {
  workoutQueue.value = JSON.parse(JSON.stringify(activeWorkoutData.queue))
}

const selectedExerciseName = ref(workoutQueue.value[0]?.name ?? null)
const isFlagMenuOpen = ref(false)

const isExerciseModalOpen = ref(false)
const searchQuery = ref('')
const filteredExercises = computed(() => {
  if (!searchQuery.value) return exerciseLibraryList
  return exerciseLibraryList.filter(ex => 
    ex.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

function openExerciseModal() {
  searchQuery.value = ''
  isExerciseModalOpen.value = true
}

function selectExerciseForQueue(name) {
  // Add to library if not exists
  if (name && !exerciseLibraryList.some(ex => ex.toLowerCase() === name.toLowerCase())) {
    exerciseLibraryList.push(name)
  }

  const newExercise = {
    name,
    badge: 'new entry',
    sets: [],
    history: getExerciseHistory(name),
    helper: 'Fill the first set to start logging this exercise.',
  }

  workoutQueue.value.push(newExercise)
  selectedExerciseName.value = newExercise.name
  isExerciseModalOpen.value = false
}

const isStartSplitDialogOpen = ref(false)
const isQuickStartDialogOpen = ref(false)

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

const dayFlags = [
  {
    label: 'Sick',
    tone: 'danger',
    paths: ['M12 15h.01', 'M12 7v6', 'M10 3.5a2 2 0 1 1 4 0v1.5h-4z', 'M8 8a4 4 0 0 1 8 0v11a4 4 0 1 1-8 0z'],
  },
  {
    label: 'Tired',
    tone: 'warning',
    paths: ['M8 15C9 13.7 10.4 13 12 13C13.6 13 15 13.7 16 15', 'M9 9.5H9.01', 'M15 9.5H15.01', 'M5 12C5 8.13 8.13 5 12 5C15.87 5 19 8.13 19 12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12Z'],
  },
  {
    label: 'Normal',
    tone: 'primary',
    paths: ['M8 13C9 14.3 10.4 15 12 15C13.6 15 15 14.3 16 13', 'M9 9.5H9.01', 'M15 9.5H15.01', 'M5 12C5 8.13 8.13 5 12 5C15.87 5 19 8.13 19 12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12Z'],
  },
  {
    label: 'Fresh',
    tone: 'success',
    paths: ['M13 2L3 14h9l-1 8 10-12h-9l1-8z'],
  },
]

const currentFlag = ref(dayFlags.find((flag) => flag.label === activeWorkoutData.session.flag) ?? dayFlags[2]) // Default to Normal
const historyFlagMap = {
  Sick: dayFlags[0],
  Tired: dayFlags[1],
  Normal: dayFlags[2],
  Fresh: dayFlags[3],
}

const weightUnit = ref('kg')

function toggleUnit() {
  const oldUnit = weightUnit.value
  const newUnit = oldUnit === 'kg' ? 'lbs' : 'kg'
  const factor = newUnit === 'lbs' ? 2.20462 : 1 / 2.20462

  workoutQueue.value.forEach(exercise => {
    exercise.sets.forEach(set => {
      if (set.weight) {
        const numericWeight = parseFloat(String(set.weight).replace(/[^\d.]/g, ''))
        if (!isNaN(numericWeight)) {
          const converted = numericWeight * factor
          set.weight = converted % 1 === 0 ? converted.toString() : converted.toFixed(1)
        }
      }
    })
  })

  weightUnit.value = newUnit
}

function handleWeightInput(e, set) {
  const val = e.target.value.replace(/[^\d.]/g, '')
  set.weight = val
}

function handleRepsInput(e, set) {
  const val = e.target.value.replace(/\D/g, '')
  set.reps = val
}

const selectedExercise = computed(
  () => workoutQueue.value.find((exercise) => exercise.name === selectedExerciseName.value) ?? null,
)

const loggedSets = computed(() =>
  workoutQueue.value.reduce((total, exercise) => total + exercise.sets.filter((set) => set.weight || set.reps || set.notes).length, 0),
)

function toggleExercise(exerciseName) {
  selectedExerciseName.value = selectedExerciseName.value === exerciseName ? null : exerciseName
}

function selectFlag(flag) {
  currentFlag.value = flag
  isFlagMenuOpen.value = false
}

function addSet(exerciseName) {
  const exercise = workoutQueue.value.find((item) => item.name === exerciseName)
  if (!exercise) {
    return
  }

  // Validation: only add if the last set is already filled (weight or reps)
  if (exercise.sets.length > 0) {
    const lastSet = exercise.sets[exercise.sets.length - 1]
    if (!lastSet.weight || !lastSet.reps) {
       return // Do nothing if the last set is empty
    }
  }

  exercise.sets.push({
    number: exercise.sets.length + 1,
    weight: '',
    reps: '',
    notes: '',
  })
}

function isCurrentSet(exercise, set) {
  return exercise.sets[exercise.sets.length - 1]?.number === set.number
}

function canSaveSet(set) {
  return Boolean(set.weight && set.reps)
}

function saveCurrentSet(exerciseName, set) {
  const exercise = workoutQueue.value.find((item) => item.name === exerciseName)
  if (!exercise || !isCurrentSet(exercise, set) || !canSaveSet(set)) {
    return
  }

  addSet(exerciseName)
}

function addExercise() {
  const nextNumber = workoutQueue.value.length + 1
  const newExercise = {
    name: `New Exercise ${nextNumber}`,
    badge: 'new entry',
    sets: [{ number: 1, weight: '', reps: '', notes: '' }],
    history: [],
    helper: 'Fill the first set to start logging this exercise.',
  }

  workoutQueue.value.push(newExercise)
  selectedExerciseName.value = newExercise.name
}

function openExerciseHistory(exerciseName) {
  router.push(`/history/exercises/${encodeURIComponent(exerciseName)}`)
}

const isFinishModalOpen = ref(false)

function confirmFinish() {
  isFinishModalOpen.value = true
}

function finishWorkout() {
  router.push('/workout/recap')
}

const isNoteModalOpen = ref(false)
const editingExerciseName = ref('')
const editingSet = ref(null)
const tempNote = ref('')

function closeNoteModal() {
  isNoteModalOpen.value = false
  editingExerciseName.value = ''
  editingSet.value = null
  tempNote.value = ''
}

function openNoteModal(exercise, set) {
  editingExerciseName.value = exercise.name
  editingSet.value = set
  tempNote.value = set.notes || ''
  isNoteModalOpen.value = true
}

function saveNote() {
  if (editingSet.value) {
    editingSet.value.notes = tempNote.value
  }
  closeNoteModal()
}

const isHistoryModalOpen = ref(false)
const historyExercise = ref(null)

function openHistoryModal(exercise) {
  historyExercise.value = exercise
  isHistoryModalOpen.value = true
}
</script>

<template>
  <div class="flex flex-col gap-4 min-w-0">
    <!-- Active Workout View -->
    <div v-if="isActive" class="flex flex-col gap-4">
      <PageHero
        :title="String(splitName)"
        :description="route.query.mode === 'quickstart' ? 'Personalize your session with manual exercise logging.' : activeWorkoutData.session.subtitle"
        class="mb-2"
      />

      <div class="flex flex-wrap items-center justify-between gap-3 mt-1">
        <div class="flex items-center gap-2 px-3 py-2 rounded-xl bg-surface-soft border border-surface-outline text-sm">
          <span class="text-text-muted">Duration</span>
          <strong class="font-bold text-blue">{{ activeWorkoutData.session.duration }}</strong>
        </div>

        <div class="flex items-center gap-2 sm:gap-3">
          <div class="relative">
            <button
              class="flex items-center justify-center p-[6px_14px] gap-2 rounded-[16px] border border-surface-outline cursor-pointer transition-colors"
              :class="[`text-${currentFlag.tone}`, `bg-${currentFlag.tone}-soft`]"
              type="button"
              :aria-label="`Day flag: ${currentFlag.label}`"
              @click="isFlagMenuOpen = !isFlagMenuOpen"
            >
              <span class="font-bold text-[0.85rem] uppercase tracking-wider text-current">{{ currentFlag.label }}</span>
              <svg class="w-5 h-5 fill-none stroke-current stroke-[2.5] [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24" aria-hidden="true">
                <path
                  v-for="path in currentFlag.paths"
                  :key="path"
                  :d="path"
                />
              </svg>
            </button>

            <div v-if="isFlagMenuOpen" class="fixed inset-0 z-40 bg-transparent" @click="isFlagMenuOpen = false"></div>
            <div v-if="isFlagMenuOpen" class="absolute top-[calc(100%+8px)] right-0 sm:right-0 z-50 min-w-[160px] p-2 rounded-[18px] bg-surface border border-surface-outline shadow-custom flex flex-col gap-1">
              <button
                v-for="flag in dayFlags"
                :key="flag.label"
                class="w-full flex items-center gap-3 p-2.5 border-0 bg-transparent text-left cursor-pointer rounded-xl hover:bg-surface-soft font-bold transition-colors"
                :class="`text-${flag.tone}`"
                type="button"
                @click="selectFlag(flag)"
              >
                <span class="flex items-center justify-center w-6 h-6 shrink-0">
                  <svg class="w-5 h-5 fill-none stroke-current stroke-2 [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24" aria-hidden="true">
                    <path
                      v-for="path in flag.paths"
                      :key="path"
                      :d="path"
                    />
                  </svg>
                </span>
                <span>{{ flag.label }}</span>
              </button>
            </div>
          </div>

        </div>
      </div>

      <section class="flex flex-col gap-5">
        <article
          v-for="(exercise, index) in workoutQueue"
          :key="exercise.name"
          class="border border-surface-outline rounded-[28px] bg-gradient-to-b from-[rgba(22,27,34,0.98)] to-[rgba(15,20,27,0.98)] shadow-custom overflow-hidden transition-colors"
          :class="{ 'border-[rgba(88,166,255,0.18)] bg-gradient-to-b from-[rgba(88,166,255,0.06)] to-[rgba(15,20,27,0.98)]': exercise.name === selectedExerciseName }"
        >
          <button
            class="w-full flex items-center justify-between gap-3 p-[18px_20px] sm:p-[20px_24px] border-0 bg-transparent text-left text-text cursor-pointer"
            type="button"
            @click="toggleExercise(exercise.name)"
          >
            <div>
              <p class="m-0 text-text-muted text-[0.78rem] tracking-[0.12em] uppercase flex items-center gap-2">
                <span>Exercise {{ index + 1 }}</span>
                <span v-if="exercise.badge" class="opacity-60 font-medium lowercase tracking-normal flex items-center gap-2 before:content-['•'] before:opacity-40">
                  {{ exercise.badge }}
                </span>
              </p>
              <h2 class="m-0 mt-1 text-[1.3rem] font-extrabold">{{ exercise.name }}</h2>
            </div>

            <div class="flex items-center gap-1.5 sm:gap-2">
              <button 
                class="w-[38px] h-[38px] rounded-full border border-surface-outline bg-surface-soft flex items-center justify-center transition-colors hover:bg-surface-soft-hover shrink-0"
                type="button"
                @click.stop="openHistoryModal(exercise)"
                title="View History"
              >
                <svg class="w-4 h-4 stroke-current fill-none stroke-2 [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24">
                  <path d="M12 8v4l3 3"></path><circle cx="12" cy="12" r="9"></circle>
                </svg>
              </button>

            </div>
          </button>

          <div 
            class="grid transition-[grid-template-rows] duration-300 ease-in-out"
            :class="exercise.name === selectedExerciseName ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'"
          >
            <div class="overflow-hidden">
              <div class="p-[0_24px_24px_24px] flex flex-col gap-6 pt-2">
                <section class="flex flex-col gap-2 pt-2">
                  <div v-if="exercise.sets.length" class="flex items-center gap-2 sm:gap-3 text-text-muted text-[0.8rem] font-bold tracking-[0.08em] uppercase px-1 mb-2">
                    <span class="w-[48px] text-center">Set</span>
                    <button class="flex-1 text-center bg-transparent border-0 text-text-muted font-bold cursor-pointer hover:text-blue transition-colors group flex items-center justify-center gap-1" @click="toggleUnit">
                      {{ weightUnit }}
                      <svg class="w-3 h-3 opacity-40 group-hover:opacity-100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M7 15l5 5 5-5M7 9l5-5 5 5"/></svg>
                    </button>
                    <span class="flex-[0.8] text-center">Reps</span>
                    <span class="w-[96px] text-center">Actions</span>
                  </div>

                  <div
                    v-for="set in exercise.sets"
                    :key="`${exercise.name}-${set.number}`"
                    class="flex items-center gap-2 sm:gap-3"
                  >
                    <span class="flex items-center justify-center w-[48px] h-[48px] shrink-0 rounded-xl bg-surface-soft text-[1.1rem] font-extrabold text-text-muted">{{ set.number }}</span>

                    <label class="flex-1">
                      <input
                        :value="set.weight"
                        class="w-full h-[48px] px-3 sm:px-4 text-center border border-surface-outline rounded-xl bg-surface text-text font-bold outline-none focus:border-blue transition-colors"
                        type="text"
                        inputmode="decimal"
                        :placeholder="weightUnit"
                        @input="handleWeightInput($event, set)"
                      />
                    </label>

                    <label class="flex-[0.8]">
                      <input
                        :value="set.reps"
                        class="w-full h-[48px] px-3 sm:px-4 text-center border border-surface-outline rounded-xl bg-surface text-text font-bold outline-none focus:border-blue transition-colors"
                        type="text"
                        inputmode="numeric"
                        placeholder="reps"
                        @input="handleRepsInput($event, set)"
                      />
                    </label>

                    <div class="flex items-center justify-center gap-2 w-[96px] shrink-0">
                      <button
                        class="relative flex items-center justify-center w-[42px] h-[42px] rounded-xl border border-surface-outline bg-surface-soft text-text-muted transition-colors hover:bg-surface-soft-hover hover:text-text shrink-0"
                        :class="{ '!border-blue !bg-blue/10 !text-blue': set.notes }"
                        type="button"
                        title="Set notes"
                        :aria-label="`Open notes for ${exercise.name} set ${set.number}`"
                        @click.stop="openNoteModal(exercise, set)"
                      >
                        <svg class="w-4 h-4 stroke-current fill-none stroke-2 [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24">
                          <path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                        </svg>
                        <span v-if="set.notes" class="absolute top-1.5 right-1.5 w-2 h-2 bg-blue rounded-full border border-bg"></span>
                      </button>

                      <button
                        v-if="isCurrentSet(exercise, set)"
                        class="flex items-center justify-center w-[42px] h-[42px] rounded-xl border-0 transition-all duration-200 shrink-0"
                        :class="canSaveSet(set) ? 'bg-gradient-to-b from-blue to-blue-strong text-bg shadow-[0_12px_28px_rgba(31,111,235,0.32)] cursor-pointer hover:brightness-110 hover:-translate-y-[1px] active:translate-y-0 active:brightness-95' : 'bg-surface-soft text-text-muted cursor-not-allowed'"
                        type="button"
                        title="Save current set"
                        aria-label="Save current set"
                        :disabled="!canSaveSet(set)"
                        @click="saveCurrentSet(exercise.name, set)"
                      >
                        <svg class="w-4 h-4 stroke-current fill-none stroke-[2.5] [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24">
                          <path d="M20 6 9 17l-5-5"></path>
                        </svg>
                      </button>

                      <span
                        v-else
                        class="flex items-center justify-center w-[42px] h-[42px] rounded-xl bg-[rgba(88,166,255,0.14)] text-blue shrink-0"
                        title="Set saved"
                        aria-label="Set saved"
                      >
                        <svg class="w-4 h-4 stroke-current fill-none stroke-[2.5] [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24">
                          <path d="M20 6 9 17l-5-5"></path>
                        </svg>
                      </span>
                    </div>
                  </div>

                  <div v-if="!exercise.sets.length" class="flex items-center justify-end gap-3 mt-3 pt-4 border-t border-[rgba(240,246,252,0.04)]">
                    <button class="inline-flex items-center justify-center gap-1.5 min-h-[36px] px-[12px] py-[4px] rounded-[12px] text-[0.78rem] font-extrabold tracking-wide cursor-pointer border-0 bg-[rgba(88,166,255,0.12)] text-blue hover:bg-[rgba(88,166,255,0.2)] transition-colors shrink-0 uppercase" type="button" @click="addSet(exercise.name)">+ Add First Set</button>
                  </div>
                </section>
              </div>
            </div>
          </div>
        </article>
      </section>

      <button
        class="inline-flex items-center justify-center gap-2 min-h-[56px] px-[24px] w-full rounded-[22px] font-bold cursor-pointer border-0 bg-[rgba(88,166,255,0.14)] text-blue hover:bg-[rgba(88,166,255,0.22)] transition-colors mt-2"
        type="button"
        @click="openExerciseModal"
      >
        + Add Exercise
      </button>

      <section class="max-w-full w-full p-6 border border-surface-outline rounded-[28px] bg-gradient-to-b from-[rgba(22,27,34,0.98)] to-[rgba(15,20,27,0.98)] shadow-custom">
        <p class="text-text-muted m-0 mt-2 leading-[1.5]">Logged so far: <b>{{ loggedSets }} sets</b> across <b>{{ workoutQueue.length }} exercises</b>.</p>
        <div class="flex flex-wrap items-stretch gap-4 mt-4">
          <button class="flex-1 inline-flex items-center justify-center gap-2 min-h-[56px] px-[24px] rounded-[22px] font-black text-[1.1rem] cursor-pointer border-0 bg-gradient-to-b from-danger to-[#b91c1c] text-white transition-opacity active:opacity-80 shadow-custom" type="button" @click="confirmFinish">
            FINISH WORKOUT 🏁
          </button>
        </div>
      </section>

      <!-- Finish Confirmation Modal -->
      <div v-if="isFinishModalOpen" class="fixed inset-0 z-[1400] flex items-center justify-center p-6 bg-black/70 backdrop-blur-md" @click.self="isFinishModalOpen = false">
        <section class="w-full max-w-[400px] bg-bg-elevated border border-surface-outline p-8 rounded-[32px] shadow-custom text-center">
          <div class="w-20 h-20 bg-danger/10 text-danger rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-10 h-10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
          </div>
          <h2 class="m-0 text-2xl font-black mb-3">Finish Workout?</h2>
          <p class="text-text-muted mb-8 leading-relaxed">Have you completed all your sets? Once finished, you can't log any more sets for this session.</p>
          
          <div class="flex flex-col gap-3">
            <button 
              class="w-full min-h-[56px] rounded-[20px] font-extrabold bg-gradient-to-b from-danger to-danger-strong text-bg border-0 cursor-pointer text-[1.05rem]"
              @click="finishWorkout"
            >
              Yes, Finish Session
            </button>
            <button 
              class="w-full min-h-[56px] rounded-[20px] font-bold bg-surface-soft text-text border border-surface-outline cursor-pointer"
              @click="isFinishModalOpen = false"
            >
              Wait, I'm not done
            </button>
          </div>
        </section>
      </div>
    </div>

    <!-- Workout Selector View (Idle state) -->
    <div v-else class="flex flex-col gap-6">
      <PageHero
        title="Active Workout"
        description="Select a split from your program or start a quick session to begin logging."
      />

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
    </div>

    <!-- Modals -->
    <div v-if="isStartSplitDialogOpen" class="fixed inset-0 z-[1200] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm" @click.self="closeStartSplitDialog">
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

    <div v-if="isQuickStartDialogOpen" class="fixed inset-0 z-[1200] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm" @click.self="closeQuickStartDialog">
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

    <!-- Exercise Selection Modal -->
    <div v-if="isExerciseModalOpen" class="fixed inset-0 z-[1300] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm" @click.self="isExerciseModalOpen = false">
      <section class="w-full max-w-[460px] max-h-[80vh] flex flex-col p-6 rounded-[28px] bg-bg-elevated border border-surface-outline shadow-custom">
        <div class="flex items-center justify-between mb-5">
          <h2 class="m-0 text-xl font-extrabold">Add Exercise</h2>
          <button class="p-2 bg-transparent text-text-muted cursor-pointer border-0" @click="isExerciseModalOpen = false">
            <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>

        <div class="relative mb-4">
          <input
            v-model="searchQuery"
            class="w-full h-[48px] pl-11 pr-4 rounded-xl bg-surface border border-surface-outline text-text font-medium outline-none focus:border-blue transition-colors"
            placeholder="Search exercises..."
            type="text"
            autofocus
          />
          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </div>

        <div class="flex-1 overflow-y-auto pr-1 flex flex-col gap-2 [scrollbar-width:thin] [scrollbar-color:rgba(88,166,255,0.2)_transparent]">
          <button
            v-for="exercise in filteredExercises"
            :key="exercise"
            class="w-full text-left p-4 rounded-xl bg-surface-soft border border-surface-outline text-text font-bold hover:bg-surface-soft-hover hover:border-blue transition-colors cursor-pointer"
            @click="selectExerciseForQueue(exercise)"
          >
            {{ exercise }}
          </button>
          
          <div v-if="filteredExercises.length === 0" class="py-12 text-center text-text-muted">
            <p>No results for "{{ searchQuery }}"</p>
            <button class="mt-2 text-blue font-bold px-4 py-2 bg-blue/10 rounded-lg border-0 cursor-pointer" @click="selectExerciseForQueue(searchQuery)">
               Add "{{ searchQuery }}" anyway
            </button>
          </div>
        </div>
      </section>
    </div>
    <!-- Note Modal -->
    <div v-if="isNoteModalOpen" class="fixed inset-0 z-[1400] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm" @click.self="closeNoteModal">
      <section class="w-full max-w-[400px] flex flex-col p-6 rounded-[28px] bg-bg-elevated border border-surface-outline shadow-custom">
        <div class="flex items-center justify-between mb-4">
          <h2 class="m-0 text-xl font-extrabold">Set Note</h2>
        </div>
        
        <p v-if="editingSet" class="text-text-muted text-sm mb-4 uppercase tracking-wider font-bold">{{ editingExerciseName }} • Set {{ editingSet.number }}</p>
 
        <textarea
          v-model="tempNote"
          class="w-full min-h-[160px] p-4 text-left border border-surface-outline rounded-xl bg-surface text-text outline-none focus:border-blue transition-colors resize-none font-medium leading-relaxed"
          placeholder="Add cues, tempo, equipment settings, or observations for this set..."
          autofocus
        ></textarea>
 
        <div class="flex gap-3 mt-6">
          <button class="flex-1 inline-flex items-center justify-center gap-2 min-h-[48px] px-4 rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text transition-colors hover:bg-surface-soft-hover" type="button" @click="closeNoteModal">Cancel</button>
          <button class="flex-1 inline-flex items-center justify-center gap-2 min-h-[48px] px-4 rounded-[18px] font-bold cursor-pointer border-0 bg-blue text-bg active:opacity-80" type="button" @click="saveNote">Save Note</button>
        </div>
      </section>
    </div>

    <!-- History Modal -->
    <div v-if="isHistoryModalOpen" class="fixed inset-0 z-[1400] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm" @click.self="isHistoryModalOpen = false">
      <section class="w-full max-w-[420px] max-h-[80vh] flex flex-col p-6 rounded-[28px] bg-bg-elevated border border-surface-outline shadow-custom">
        <div class="flex items-center justify-between mb-5">
          <h2 class="m-0 text-xl font-extrabold">Recent History</h2>
          <button class="p-2 bg-transparent text-text-muted cursor-pointer border-0" @click="isHistoryModalOpen = false">
            <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
        
        <div v-if="historyExercise" class="flex flex-col gap-4 overflow-y-auto pr-1 [scrollbar-width:thin] [scrollbar-color:rgba(88,166,255,0.2)_transparent]">
          <p class="text-text-muted text-sm uppercase tracking-wider font-bold mb-1">{{ historyExercise.name }}</p>
          
          <div v-if="historyExercise.history && historyExercise.history.length" class="flex flex-col">
            <div
              v-for="(entry, eIdx) in historyExercise.history"
              :key="`${historyExercise.name}-${entry.date}-${entry.summary}`"
              class="flex items-center gap-3 py-3 border-b border-surface-outline last:border-0"
            >
              <div
                class="flex items-center justify-center w-8 h-8 shrink-0 rounded-lg bg-surface-soft"
                :class="`text-${(historyFlagMap[entry.flag] ?? dayFlags[3]).tone}`"
              >
                <svg class="w-5 h-5 fill-none stroke-current stroke-2 [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24">
                  <path
                    v-for="path in (historyFlagMap[entry.flag] ?? dayFlags[1]).paths"
                    :key="path"
                    :d="path"
                  />
                </svg>
              </div>
              <div class="flex flex-col flex-1 min-w-0">
                <strong class="text-[0.95rem] font-bold truncate">{{ entry.summary }}</strong>
                <span class="text-text-muted text-[0.7rem] font-bold uppercase tracking-wide">{{ entry.date }} • {{ entry.flag }}</span>
              </div>
            </div>
          </div>
          
          <div v-else class="py-12 text-center text-text-muted border border-dashed border-surface-outline rounded-3xl">
             <p class="m-0 italic">No previous history found for this exercise.</p>
          </div>

          <button class="w-full mt-4 min-h-[48px] rounded-xl font-bold border border-surface-outline bg-transparent text-blue hover:bg-blue/5 transition-colors" @click="openExerciseHistory(historyExercise.name)">View Full Analytics</button>
        </div>
      </section>
    </div>
  </div>
</template>
