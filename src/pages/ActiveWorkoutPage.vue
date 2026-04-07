<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { activeWorkoutData } from '../data/mockData'
import PageHero from '../components/PageHero.vue'

const router = useRouter()
const route = useRoute()

const splitName = computed(() => route.query.split || activeWorkoutData.session.title)
const workoutQueue = ref(JSON.parse(JSON.stringify(activeWorkoutData.queue)))
const selectedExerciseName = ref(workoutQueue.value[0]?.name ?? null)
const isFlagMenuOpen = ref(false)

const dayFlags = [
  {
    label: 'Fresh',
    tone: 'success',
    paths: ['M12 4.5L14.2 9L19 9.7L15.5 13.1L16.3 18L12 15.7L7.7 18L8.5 13.1L5 9.7L9.8 9Z'],
  },
  {
    label: 'Normal',
    tone: 'primary',
    paths: ['M12 6V18', 'M6 12H18'],
  },
  {
    label: 'Tired',
    tone: 'warning',
    paths: ['M8 15C9 13.7 10.4 13 12 13C13.6 13 15 13.7 16 15', 'M9 9.5H9.01', 'M15 9.5H15.01', 'M5 12C5 8.13 8.13 5 12 5C15.87 5 19 8.13 19 12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12Z'],
  },
  {
    label: 'Beast',
    tone: 'danger',
    paths: ['M12 5L14 9.5L19 10L15 13.3L16.2 19L12 16.3L7.8 19L9 13.3L5 10L10 9.5Z', 'M12 8.2L12.9 10.3L15.2 10.5L13.4 12.1L13.9 14.3L12 13.2L10.1 14.3L10.6 12.1L8.8 10.5L11.1 10.3Z'],
  },
]

const currentFlag = ref(dayFlags.find((flag) => flag.label === activeWorkoutData.session.flag) ?? dayFlags[0])
const historyFlagMap = {
  Fresh: dayFlags[0],
  Normal: dayFlags[1],
  Tired: dayFlags[2],
  Beast: dayFlags[3],
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

  exercise.sets.push({
    number: exercise.sets.length + 1,
    weight: '',
    reps: '',
    notes: '',
  })
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

function finishWorkout() {
  router.push('/workout/recap')
}
</script>

<template>
  <div class="flex flex-col gap-4 min-w-0">
    <!-- Top Bar logic removed, hero is top -->

    <PageHero
      :title="String(splitName)"
      :description="activeWorkoutData.session.subtitle"
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
              class="flex items-center justify-center p-[6px_10px] gap-2 rounded-[16px] border border-surface-outline bg-surface-soft text-text cursor-pointer hover:border-[rgba(88,166,255,0.4)] transition-colors"
              :class="`text-${currentFlag.tone}`"
              type="button"
              :aria-label="`Day flag: ${currentFlag.label}`"
              @click="isFlagMenuOpen = !isFlagMenuOpen"
            >
              <span class="font-bold text-[0.8rem] uppercase tracking-wider text-text">{{ currentFlag.label }}</span>
              <svg class="w-5 h-5 fill-none stroke-current stroke-[2.5] [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24" aria-hidden="true">
                <path
                  v-for="path in currentFlag.paths"
                  :key="path"
                  :d="path"
                />
              </svg>
            </button>

            <div v-if="isFlagMenuOpen" class="absolute top-[calc(100%+8px)] right-0 sm:right-0 z-[100] min-w-[160px] p-2 rounded-[18px] bg-surface border border-surface-outline shadow-custom flex flex-col gap-1">
              <button
                v-for="flag in dayFlags"
                :key="flag.label"
                class="w-full flex items-center gap-3 p-2.5 border-0 bg-transparent text-text text-left cursor-pointer rounded-xl hover:bg-surface-soft font-bold transition-colors"
                type="button"
                @click="selectFlag(flag)"
              >
                <span class="flex items-center justify-center w-6 h-6 shrink-0" :class="`text-${flag.tone}`">
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

          <button class="inline-flex items-center justify-center gap-2 min-h-[44px] px-[18px] rounded-[16px] font-bold cursor-pointer border-0 bg-[rgba(248,81,73,0.14)] text-danger hover:bg-[rgba(248,81,73,0.2)] transition-colors" type="button" @click="finishWorkout">Finish</button>
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
          class="w-full flex items-center justify-between gap-4 p-[20px_24px] border-0 bg-transparent text-left text-text cursor-pointer"
          type="button"
          @click="toggleExercise(exercise.name)"
        >
          <div>
            <p class="m-0 text-text-muted text-[0.78rem] tracking-[0.12em] uppercase">Exercise {{ index + 1 }}</p>
            <h2 class="m-0 mt-1 text-[1.3rem] font-extrabold">{{ exercise.name }}</h2>
          </div>

          <span class="inline-flex items-center gap-2 w-fit px-3 py-2 rounded-full text-[0.8rem] font-bold" :class="exercise.name === selectedExerciseName ? 'bg-[rgba(88,166,255,0.18)] text-text' : 'bg-surface-soft text-text-muted'">
            {{ exercise.badge }}
          </span>
        </button>

        <div v-if="exercise.name === selectedExerciseName" class="p-[0_24px_24px_24px] flex flex-col gap-6">
          <section v-if="exercise.history.length" class="bg-[rgba(13,17,23,0.6)] rounded-[20px] p-5 border border-surface-soft mt-1">
            <div class="flex items-center justify-between gap-3 mb-4">
              <h3 class="m-0 text-[1.05rem] font-bold text-text-soft">Recent history</h3>
              <button class="p-0 bg-transparent text-blue font-bold cursor-pointer border-0" type="button" @click="openExerciseHistory(exercise.name)">Load more</button>
            </div>

            <div class="flex flex-col gap-3">
              <div
                v-for="entry in exercise.history"
                :key="`${exercise.name}-${entry.date}-${entry.summary}`"
                class="flex items-center gap-4 text-sm"
              >
                <span class="text-text-muted w-[60px] shrink-0">{{ entry.date }}</span>
                <strong class="flex-1 min-w-0 font-bold truncate">{{ entry.summary }}</strong>
                <span
                  class="flex items-center justify-center w-6 h-6 shrink-0"
                  :class="`text-${(historyFlagMap[entry.flag] ?? dayFlags[1]).tone}`"
                  :aria-label="entry.flag"
                  :title="entry.flag"
                >
                  <svg class="w-4 h-4 fill-none stroke-current stroke-2 [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24" aria-hidden="true">
                    <path
                      v-for="path in (historyFlagMap[entry.flag] ?? dayFlags[1]).paths"
                      :key="path"
                      :d="path"
                    />
                  </svg>
                </span>
              </div>
            </div>
          </section>

          <section class="flex flex-col gap-2">
            <div class="flex items-center text-text-muted text-[0.8rem] font-bold tracking-[0.08em] uppercase px-1 mb-2">
              <span class="w-[48px] text-center">Set</span>
              <span class="flex-1 text-center">Kg</span>
              <span class="flex-[0.8] text-center">Reps</span>
              <span class="flex-[1.2] pl-2">Notes</span>
            </div>

            <div
              v-for="set in exercise.sets"
              :key="`${exercise.name}-${set.number}`"
              class="flex items-center gap-2 sm:gap-3"
            >
              <span class="flex items-center justify-center w-[48px] h-[48px] shrink-0 rounded-xl bg-surface-soft text-[1.1rem] font-extrabold text-text-muted">{{ set.number }}</span>

              <label class="flex-1">
                <input
                  v-model="set.weight"
                  class="w-full h-[48px] px-3 sm:px-4 text-center border border-surface-outline rounded-xl bg-surface text-text font-bold outline-none focus:border-blue transition-colors"
                  type="text"
                  inputmode="decimal"
                  placeholder="kg"
                />
              </label>

              <label class="flex-[0.8]">
                <input
                  v-model="set.reps"
                  class="w-full h-[48px] px-3 sm:px-4 text-center border border-surface-outline rounded-xl bg-surface text-text font-bold outline-none focus:border-blue transition-colors"
                  type="text"
                  inputmode="numeric"
                  placeholder="reps"
                />
              </label>

              <label class="flex-[1.2]">
                <input
                  v-model="set.notes"
                  class="w-full h-[48px] px-3 sm:px-4 text-left border border-surface-outline rounded-xl bg-surface text-text outline-none focus:border-blue transition-colors"
                  type="text"
                  placeholder="notes"
                />
              </label>
            </div>

            <div class="flex items-center justify-between gap-4 mt-3 pt-4 border-t border-[rgba(240,246,252,0.04)]">
              <p class="text-text-muted text-[0.85rem] m-0 max-w-[200px] leading-snug">{{ exercise.helper }}</p>
              <button class="inline-flex items-center justify-center gap-2 min-h-[44px] px-[16px] py-[8px] rounded-[16px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg shrink-0" type="button" @click="addSet(exercise.name)">+ Add Set</button>
            </div>
          </section>
        </div>
      </article>
    </section>

    <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] w-full rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" type="button" @click="addExercise">
      + Add Exercise
    </button>

    <section class="max-w-full w-full p-6 border border-surface-outline rounded-[28px] bg-gradient-to-b from-[rgba(22,27,34,0.98)] to-[rgba(15,20,27,0.98)] shadow-custom">
      <p class="text-text-muted m-0 leading-[1.5]">Session save notes and recap flow can stay below this area once backend logging is connected.</p>
      <p class="text-text-muted m-0 mt-2 leading-[1.5]">Logged so far: {{ loggedSets }} sets across {{ workoutQueue.length }} exercises.</p>
      <div class="flex flex-wrap items-stretch gap-4 mt-4">
        <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" type="button" @click="selectedExercise && openExerciseHistory(selectedExercise.name)">Open Exercise Detail</button>
      </div>
    </section>
  </div>
</template>
