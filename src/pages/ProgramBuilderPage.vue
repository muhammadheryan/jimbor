<script setup>
import { computed, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import StatCard from '../components/StatCard.vue'
import { apiRoutes } from '../services/api'
import { programBuilderData, exerciseLibraryList } from '../data/mockData'

const route = useRoute()

const selectedSplitIndex = ref(0)
const selectedExerciseIndex = ref(0)

const isExerciseModalOpen = ref(false)
const searchQuery = ref('')
const filteredExercises = computed(() => {
  if (!searchQuery.value) return exerciseLibraryList
  return exerciseLibraryList.filter(ex => 
    ex.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const builderMode = computed(() => (route.query.mode === 'create' ? 'create' : 'edit'))
const builderTitle = computed(() => (builderMode.value === 'create' ? 'Create Program' : 'Program Builder'))
const builderDescription = computed(() =>
  builderMode.value === 'create'
    ? 'Start a new training structure with split setup, exercise templates, and target ranges.'
    : 'Update split names, exercise templates, target sets, and rep ranges in one place.',
)

const selectedSplit = computed(() => programBuilderData.splits[selectedSplitIndex.value] ?? null)
const selectedExercise = computed(() => selectedSplit.value?.exercises[selectedExerciseIndex.value] ?? null)

function openSplit(index) {
  selectedSplitIndex.value = index
  selectedExerciseIndex.value = 0
}

function editExercise(splitIndex, exerciseIndex) {
  selectedSplitIndex.value = splitIndex
  selectedExerciseIndex.value = exerciseIndex
}

function openExerciseModal() {
  searchQuery.value = ''
  isExerciseModalOpen.value = true
}

function selectExercise(name) {
  if (selectedExercise.value) {
    selectedExercise.value.name = name
  }
  isExerciseModalOpen.value = false
}
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <PageHero
      :title="builderTitle"
      :description="builderDescription"
    />

    <div class="builder-summary">
      <SectionCard :title="builderMode === 'create' ? 'Program setup' : 'Program details'" subtitle="Basic metadata for the whole program">
        <div class="field-stack">
          <label class="flex flex-col gap-2">
            <span>Program name</span>
            <input :value="builderMode === 'create' ? '' : programBuilderData.name" type="text" :placeholder="builderMode === 'create' ? 'Example: Upper Lower 4x' : ''" />
          </label>

          <label class="flex flex-col gap-2">
            <span>Description</span>
            <textarea rows="3">{{ builderMode === 'create' ? '' : programBuilderData.description }}</textarea>
          </label>
        </div>

        <div class="flex flex-wrap items-stretch justify-end gap-4 [&>*]:flex-1">
          <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" to="/programs">Back to Programs</RouterLink>
          <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" to="/programs/builder/splits/new">Continue to Split Setup</RouterLink>
        </div>
      </SectionCard>

      <SectionCard title="Quick stats" subtitle="High level structure before you publish">
        <div class="stats-grid stats-grid--two">
          <StatCard
            v-for="item in programBuilderData.stats"
            :key="item.label"
            :label="item.label"
            :value="item.value"
          />
        </div>
      </SectionCard>
    </div>

    <div class="builder-layout builder-layout--compact">
      <SectionCard title="Splits" subtitle="Select a split, then edit its exercises">
        <template #header-actions>
          <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" to="/programs/builder/splits/new">+ Add Split</RouterLink>
        </template>

        <div class="flex flex-col gap-3">
          <article
            v-for="(split, splitIndex) in programBuilderData.splits"
            :key="split.name"
            class="builder-split"
            :class="{ 'builder-split--active': splitIndex === selectedSplitIndex }"
          >
            <button class="builder-split__trigger" type="button" @click="openSplit(splitIndex)">
              <div>
                <h3>{{ split.name }}</h3>
                <p>{{ split.note }}</p>
              </div>
              <span class="inline-flex items-center gap-2 w-fit px-3 py-2 rounded-full bg-surface-soft text-text-muted text-[0.8rem] font-bold">{{ split.exercises.length }} exercises</span>
            </button>

            <div class="flex flex-col gap-3">
              <article
                v-for="(exercise, exerciseIndex) in split.exercises"
                :key="exercise.name"
                class="list-card builder-exercise"
                :class="{ 'builder-exercise--active': splitIndex === selectedSplitIndex && exerciseIndex === selectedExerciseIndex }"
              >
                <div>
                  <h3>{{ exercise.name }}</h3>
                  <p>{{ exercise.meta }}</p>
                </div>
                <button type="button" class="p-0 bg-transparent text-blue font-bold cursor-pointer inline-flex items-center justify-center gap-2 border-0" @click="editExercise(splitIndex, exerciseIndex)">Edit</button>
              </article>
            </div>

            <div class="flex flex-wrap items-stretch justify-end gap-4 [&>*]:flex-1">
              <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" :to="`/programs/builder/splits/${encodeURIComponent(split.name)}`">Manage Split</RouterLink>
              <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" :to="`/programs/builder/splits/${encodeURIComponent(split.name)}?exercise=${encodeURIComponent(split.exercises[0]?.name ?? '')}`">Exercise Page</RouterLink>
            </div>
          </article>
        </div>
      </SectionCard>

      <div class="builder-side-stack">
        <SectionCard title="Split creator" subtitle="Quick form to add a new split block">
          <div class="field-stack">
            <label class="flex flex-col gap-2">
              <span>Split name</span>
              <input :value="programBuilderData.splitDraft.name" type="text" />
            </label>

            <label class="flex flex-col gap-2">
              <span>Schedule cue</span>
              <input :value="programBuilderData.splitDraft.schedule" type="text" />
            </label>

            <label class="flex flex-col gap-2">
              <span>Focus area</span>
              <input :value="programBuilderData.splitDraft.focus" type="text" />
            </label>
          </div>

          <div class="flex flex-wrap items-stretch justify-end gap-4 [&>*]:flex-1">
            <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" type="button">Clear</button>
            <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" to="/programs/builder/splits/new">+ Add Split</RouterLink>
          </div>
        </SectionCard>

        <SectionCard title="Exercise editor" subtitle="Edit button highlights the selected exercise here">
          <template v-if="selectedSplit && selectedExercise">
            <div class="builder-editor">
              <div class="builder-editor__head">
                <div>
                  <p class="text-text-muted text-[0.78rem] tracking-[0.12em] uppercase m-0">{{ selectedSplit.name }}</p>
                  <h3>{{ selectedExercise.name }}</h3>
                </div>
                <span class="pill pill--primary">Editing</span>
              </div>

              <div class="field-stack">
                <label class="flex flex-col gap-2">
                  <span>Exercise name</span>
                  <div class="relative">
                    <input 
                      :value="selectedExercise.name" 
                      type="text" 
                      readonly 
                      class="w-full cursor-pointer pr-10"
                      @click="openExerciseModal" 
                    />
                    <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted pointer-events-none" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                  </div>
                </label>

                <label class="flex flex-col gap-2">
                  <span>Target sets and reps</span>
                  <input :value="selectedExercise.meta" type="text" />
                </label>

                <div class="builder-editor__grid">
                  <label class="flex flex-col gap-2">
                    <span>Rest</span>
                    <input :value="selectedExercise.rest" type="text" />
                  </label>

                  <label class="flex flex-col gap-2">
                    <span>Coaching cue</span>
                    <input :value="selectedExercise.target" type="text" />
                  </label>
                </div>
              </div>

              <div class="flex flex-wrap items-stretch justify-end gap-4 [&>*]:flex-1">
                <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" :to="`/programs/builder/splits/${encodeURIComponent(selectedSplit.name)}`">Open Split Page</RouterLink>
                <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" type="button">Save Exercise</button>
              </div>
            </div>
          </template>

          <p v-else class="muted-copy">Select one exercise from the split list to edit it here.</p>
        </SectionCard>

        <SectionCard title="Backend routes" subtitle="These are the routes used by the builder flow">
          <div class="api-note">
            <p><strong>POST</strong> {{ apiRoutes.programs.addDay(':programId') }}</p>
            <p><strong>PUT</strong> {{ apiRoutes.programs.updateDay(':programId', ':dayId') }}</p>
            <p><strong>POST</strong> {{ apiRoutes.programs.addExercise(':programId', ':dayId') }}</p>
            <p><strong>PUT</strong> {{ apiRoutes.programs.updateExercise(':programId', ':dayId', ':exerciseId') }}</p>
          </div>
        </SectionCard>
      </div>
    </div>

    <div class="flex flex-wrap items-stretch justify-end gap-4 [&>*]:flex-1">
      <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" type="button">Preview Program</button>
      <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" type="button">{{ builderMode === 'create' ? 'Create Program' : 'Save Program' }}</button>
    </div>

    <!-- Exercise Selection Modal -->
    <div v-if="isExerciseModalOpen" class="fixed inset-0 z-[110] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm" @click.self="isExerciseModalOpen = false">
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
