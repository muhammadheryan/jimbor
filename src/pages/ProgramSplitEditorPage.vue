<script setup>
import { computed, ref, onMounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import { programBuilderData, exerciseLibraryList } from '../data/mockData'

const route = useRoute()

const isExerciseModalOpen = ref(false)
const searchQuery = ref('')
const currentlyEditingExerciseIndex = ref(-1)

const filteredExercises = computed(() => {
  if (!searchQuery.value) return exerciseLibraryList
  return exerciseLibraryList.filter(ex => 
    ex.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const isCreateMode = computed(() => route.path.endsWith('/new'))
const selectedSplit = ref({
  name: '',
  note: '',
  exercises: [],
})

onMounted(() => {
  if (!isCreateMode.value) {
    const splitName = decodeURIComponent(route.params.splitName ?? '')
    const found = programBuilderData.splits.find((split) => split.name.toLowerCase() === splitName.toLowerCase())
    if (found) {
      // Create a reactive copy so we don't modify the source mock data directly until save
      selectedSplit.value = JSON.parse(JSON.stringify(found))
    }
  }
})

function openExerciseModal(index) {
  currentlyEditingExerciseIndex.value = index
  searchQuery.value = ''
  isExerciseModalOpen.value = true
}

function selectExercise(name) {
  // Add to library if not exists
  if (name && !exerciseLibraryList.some(ex => ex.toLowerCase() === name.toLowerCase())) {
    exerciseLibraryList.push(name)
  }

  if (currentlyEditingExerciseIndex.value === -1) {
    // Create new
    selectedSplit.value.exercises.push({ name, sets: 3, reps: '8-12', rest: '', target: '' })
  } else if (currentlyEditingExerciseIndex.value > -1) {
    // Update existing
    selectedSplit.value.exercises[currentlyEditingExerciseIndex.value].name = name
  }
  isExerciseModalOpen.value = false
}

function validateRepsRange(exercise) {
  if (exercise.reps && !exercise.reps.match(/^\d+-\d+$/)) {
    alert('Reps target must be in format number-number (e.g. 10-12)')
  }
}

function moveExerciseUp(index) {
  if (index > 0) {
    const temp = selectedSplit.value.exercises[index];
    selectedSplit.value.exercises[index] = selectedSplit.value.exercises[index - 1];
    selectedSplit.value.exercises[index - 1] = temp;
  }
}

function moveExerciseDown(index) {
  if (index < selectedSplit.value.exercises.length - 1) {
    const temp = selectedSplit.value.exercises[index];
    selectedSplit.value.exercises[index] = selectedSplit.value.exercises[index + 1];
    selectedSplit.value.exercises[index + 1] = temp;
  }
}

function removeExercise(index) {
  selectedSplit.value.exercises.splice(index, 1)
}

function addExerciseRow() {
  openExerciseModal(-1)
}
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <PageHero
      :title="isCreateMode ? 'Add Split' : `Edit ${selectedSplit.name}`"
      :description="isCreateMode ? 'Create a new split and fill its exercise queue.' : selectedSplit.note"
    />

    <div class="flex flex-wrap items-center justify-end gap-4">
      <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" to="/programs/builder">Back to Builder</RouterLink>
    </div>

    <div class="builder-summary">
      <SectionCard title="Split details" subtitle="Main identity for this split">
        <div class="field-stack">
          <label class="flex flex-col gap-2">
            <span>Split name</span>
            <input :value="selectedSplit.name" type="text" placeholder="Example: PUSH A" />
          </label>

          <label class="flex flex-col gap-2">
            <span>Focus area</span>
            <input :value="selectedSplit.note" type="text" placeholder="Chest, shoulders, triceps" />
          </label>
        </div>
      </SectionCard>

      <SectionCard title="Split guide" subtitle="Keep each day focused and easy to scan">
        <div class="flex flex-col gap-3">
          <article class="p-[18px] bg-surface-soft border border-surface-outline rounded-[28px] max-w-full shadow-custom">
            <h3>Exercise order matters</h3>
            <p>Place compounds first, then accessories, then isolation work.</p>
          </article>
        </div>
      </SectionCard>
    </div>

    <SectionCard title="Exercises" subtitle="Fill each exercise row for this split">
      <div class="flex flex-col gap-3">
        <article
          v-for="(exercise, exerciseIndex) in selectedSplit.exercises"
          :key="`${selectedSplit.name || 'new'}-${exerciseIndex}`"
          class="builder-split builder-split--active"
        >
          <div class="builder-editor">
            <div class="builder-editor__head flex items-center justify-between">
              <div>
                <p class="text-text-muted text-[0.78rem] tracking-[0.12em] uppercase m-0">Exercise {{ exerciseIndex + 1 }}</p>
                <h3>{{ exercise.name || 'New Exercise' }}</h3>
              </div>

              <div class="flex items-center gap-1 ml-1">
                <div class="flex flex-col gap-0.5">
                  <button type="button" class="inline-flex items-center justify-center w-7 h-[20px] p-0 text-text-muted hover:text-blue bg-surface-soft border border-surface-outline rounded-md transition-colors disabled:opacity-10 cursor-pointer" :disabled="exerciseIndex === 0" @click.stop="moveExerciseUp(exerciseIndex)">
                    <svg class="w-2.5 h-2.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"></polyline></svg>
                  </button>
                  <button type="button" class="inline-flex items-center justify-center w-7 h-[20px] p-0 text-text-muted hover:text-blue bg-surface-soft border border-surface-outline rounded-md transition-colors disabled:opacity-10 cursor-pointer" :disabled="exerciseIndex === selectedSplit.exercises.length - 1" @click.stop="moveExerciseDown(exerciseIndex)">
                    <svg class="w-2.5 h-2.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                  </button>
                </div>

                <button type="button" class="inline-flex items-center justify-center shrink-0 w-8 h-10 p-0 text-text-muted hover:text-danger rounded-xl transition-colors bg-transparent border-0 cursor-pointer" @click="removeExercise(exerciseIndex)">
                  <svg class="w-4 h-4 fill-none stroke-current stroke-2" viewBox="0 0 24 24">
                    <polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
            </div>

            <div class="field-stack">
              <label class="flex flex-col gap-2">
                <span>Exercise name</span>
                <div class="relative">
                  <input 
                    :value="exercise.name" 
                    type="text" 
                    readonly 
                    class="w-full cursor-pointer pr-10" 
                    placeholder="Example: Bench Press"
                    @click="openExerciseModal(exerciseIndex)" 
                  />
                  <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted pointer-events-none" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                </div>
              </label>

              <div class="flex gap-4">
                <label class="flex flex-col gap-2 flex-1">
                  <span>Sets</span>
                  <input v-model="exercise.sets" type="number" placeholder="4" />
                </label>

                <label class="flex flex-col gap-2 flex-[1.5]">
                  <span>Reps target</span>
                  <div class="relative">
                    <input 
                      v-model="exercise.reps" 
                      type="text" 
                      placeholder="10-12"
                      class="transition-colors"
                      :class="{ 'border-danger': exercise.reps && !exercise.reps.match(/^\d+-\d+$/) }"
                      @blur="validateRepsRange(exercise)"
                    />
                    <span v-if="exercise.reps && !exercise.reps.match(/^\d+-\d+$/)" class="absolute -bottom-5 left-0 text-[0.65rem] text-danger font-bold uppercase">Format: 10-12</span>
                  </div>
                </label>
              </div>

              <div class="builder-editor__grid">
                <label class="flex flex-col gap-2">
                  <span>Rest</span>
                  <input :value="exercise.rest" type="text" placeholder="90 sec" />
                </label>

                <label class="flex flex-col gap-2">
                  <span>Coaching cue</span>
                  <input :value="exercise.target" type="text" placeholder="Control the eccentric" />
                </label>
              </div>
            </div>
          </div>
        </article>
      </div>

      <div class="flex flex-wrap items-stretch justify-end gap-4 [&>*]:flex-1">
        <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-[rgba(88,166,255,0.14)] text-blue hover:bg-[rgba(88,166,255,0.22)]" type="button" @click="addExerciseRow">+ Add Exercise</button>
        <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" type="button">{{ isCreateMode ? 'Save Split' : 'Update Split' }}</button>
      </div>
    </SectionCard>

    <!-- Exercise Selection Modal -->
    <div v-if="isExerciseModalOpen" class="fixed inset-0 z-[1300] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm" @click.self="isExerciseModalOpen = false">
      <section class="w-full max-w-[460px] max-h-[80vh] flex flex-col p-6 rounded-[28px] bg-bg-elevated border border-surface-outline shadow-custom">
        <div class="flex items-center justify-between mb-5">
          <h2 class="m-0 text-xl font-extrabold">Select Exercise</h2>
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

        <div class="flex-1 overflow-y-auto pr-1 flex flex-col gap-2 custom-scrollbar">
          <button
            v-for="exerciseName in filteredExercises"
            :key="exerciseName"
            class="w-full text-left p-4 rounded-xl bg-surface-soft border border-surface-outline text-text font-bold hover:bg-surface-soft-hover hover:border-blue transition-colors cursor-pointer"
            @click="selectExercise(exerciseName)"
          >
            {{ exerciseName }}
          </button>
          
          <div v-if="filteredExercises.length === 0" class="py-12 text-center text-text-muted">
            <p>No results for "{{ searchQuery }}"</p>
            <button class="mt-2 text-blue font-bold px-4 py-2 bg-blue/10 rounded-lg border-0 cursor-pointer" @click="selectExercise(searchQuery)">
               Use "{{ searchQuery }}" anyway
            </button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
