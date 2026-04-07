<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import StatCard from '../components/StatCard.vue'
import { programBuilderData, exerciseLibraryList } from '../data/mockData'

const route = useRoute()
const router = useRouter()

const isCreateMode = computed(() => route.path === '/programs/create')
const programId = computed(() => route.params.programId)

// Form state
const programName = ref('')
const programDescription = ref('')
const isActive = ref(false)
const splits = ref([])

onMounted(() => {
  if (!isCreateMode.value) {
    // Load mock data
    programName.value = programBuilderData.name
    programDescription.value = programBuilderData.description
    // Deep clone to allow editing without mutating mock directly
    splits.value = JSON.parse(JSON.stringify(programBuilderData.splits))
    
    // Add sets field if not present in mock
    splits.value.forEach(split => {
      split.exercises.forEach(ex => {
        // extract target sets from meta if exists
        let match = (ex.meta || '').match(/(\d+)\s+sets/)
        if (!ex.sets) {
            ex.sets = match ? parseInt(match[1]) : 3
        }
        if (!ex.name) ex.name = ''
      })
    })
  } else {
    // Empty state
    splits.value = [
      { name: 'Day 1', note: '', exercises: [] }
    ]
  }
})

// Splitting logic for Drag & Drop
const draggingSplitIndex = ref(null)

const onSplitDragStart = (e, index) => {
  draggingSplitIndex.value = index
  e.dataTransfer.effectAllowed = 'move'
  e.target.classList.add('dragging')
}

const onSplitDragEnd = (e) => {
  draggingSplitIndex.value = null
  e.target.classList.remove('dragging')
}

const onSplitDrop = (e, index) => {
  if (draggingSplitIndex.value === null || draggingSplitIndex.value === index) return
  const item = splits.value.splice(draggingSplitIndex.value, 1)[0]
  splits.value.splice(index, 0, item)
  draggingSplitIndex.value = null
}

const draggingExercise = ref(null) // { splitIndex, exerciseIndex }

const onExerciseDragStart = (e, splitIndex, exerciseIndex) => {
  draggingExercise.value = { splitIndex, exerciseIndex }
  e.dataTransfer.effectAllowed = 'move'
  // using setTimeout to prevent drag ghost removal issue
  setTimeout(() => e.target.classList.add('dragging'), 0)
}

const onExerciseDragEnd = (e) => {
  draggingExercise.value = null
  e.target.classList.remove('dragging')
}

const onExerciseDrop = (e, splitIndex, exerciseIndex) => {
  if (!draggingExercise.value) return
  if (draggingExercise.value.splitIndex === splitIndex && draggingExercise.value.exerciseIndex === exerciseIndex) return
  
  const fromSplit = draggingExercise.value.splitIndex
  const fromEx = draggingExercise.value.exerciseIndex
  
  const item = splits.value[fromSplit].exercises.splice(fromEx, 1)[0]
  splits.value[splitIndex].exercises.splice(exerciseIndex, 0, item)
  draggingExercise.value = null
}

const moveSplitUp = (index) => {
  if (index > 0) {
    const temp = splits.value[index];
    splits.value[index] = splits.value[index - 1];
    splits.value[index - 1] = temp;
  }
}
const moveSplitDown = (index) => {
  if (index < splits.value.length - 1) {
    const temp = splits.value[index];
    splits.value[index] = splits.value[index + 1];
    splits.value[index + 1] = temp;
  }
}
const moveExerciseUp = (splitIndex, exerciseIndex) => {
  if (exerciseIndex > 0) {
    const temp = splits.value[splitIndex].exercises[exerciseIndex];
    splits.value[splitIndex].exercises[exerciseIndex] = splits.value[splitIndex].exercises[exerciseIndex - 1];
    splits.value[splitIndex].exercises[exerciseIndex - 1] = temp;
  }
}
const moveExerciseDown = (splitIndex, exerciseIndex) => {
  if (exerciseIndex < splits.value[splitIndex].exercises.length - 1) {
    const temp = splits.value[splitIndex].exercises[exerciseIndex];
    splits.value[splitIndex].exercises[exerciseIndex] = splits.value[splitIndex].exercises[exerciseIndex + 1];
    splits.value[splitIndex].exercises[exerciseIndex + 1] = temp;
  }
}

const addSplit = () => {
  splits.value.push({
    name: `New Split ${splits.value.length + 1}`,
    note: '',
    exercises: []
  })
}

const removeSplit = (index) => {
  splits.value.splice(index, 1)
}

const isExerciseModalOpen = ref(false)
const searchQuery = ref('')
const targetSplitIndex = ref(-1)
const targetExerciseIndex = ref(-1)

const filteredExercises = computed(() => {
  if (!searchQuery.value) return exerciseLibraryList
  return exerciseLibraryList.filter(ex => 
    ex.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const openExerciseModal = (sIndex, eIndex) => {
  targetSplitIndex.value = sIndex
  targetExerciseIndex.value = eIndex
  searchQuery.value = ''
  isExerciseModalOpen.value = true
}

const selectExercise = (name) => {
  if (targetSplitIndex.value > -1 && targetExerciseIndex.value > -1) {
    splits.value[targetSplitIndex.value].exercises[targetExerciseIndex.value].name = name
  }
  isExerciseModalOpen.value = false
}

const addExercise = (splitIndex) => {
  splits.value[splitIndex].exercises.push({
    name: '',
    sets: 3,
    meta: '', // optional mock fields
    rest: '',
    target: ''
  })
  // Auto open modal for the new exercise
  openExerciseModal(splitIndex, splits.value[splitIndex].exercises.length - 1)
}

const removeExercise = (splitIndex, exerciseIndex) => {
  splits.value[splitIndex].exercises.splice(exerciseIndex, 1)
}

const saveProgram = () => {
  // Mock save
  router.push('/programs')
}

const totalSplits = computed(() => splits.value.length)
const totalExercises = computed(() => splits.value.reduce((acc, split) => acc + split.exercises.length, 0))
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <PageHero
      :title="isCreateMode ? 'Create Program' : `Edit ${programName}`"
      :description="isCreateMode ? 'Start a new training structure with splits and exercises.' : 'Update split details and manage the exercise order.'"
    />

    <!-- Section: Program Details (2 Columns) -->
    <SectionCard title="Program Details" subtitle="Basic metadata for the whole program">
      <div class="grid grid-cols-1 md:grid-cols-[1.5fr_1fr] gap-6 items-start">
        <!-- Left Col: Form -->
        <div class="flex flex-col gap-3">
          <label class="flex flex-col gap-2">
            <span class="text-text-muted text-[0.78rem] font-bold tracking-[0.08em] uppercase">Program name</span>
            <input class="w-full px-[18px] py-4 border border-surface-outline rounded-[18px] bg-surface-soft text-text outline-none" v-model="programName" type="text" placeholder="Example: Upper Lower 4x" />
          </label>
          <label class="flex flex-col gap-2">
            <span class="text-text-muted text-[0.78rem] font-bold tracking-[0.08em] uppercase">Description</span>
            <textarea class="w-full px-[18px] py-4 border border-surface-outline rounded-[18px] bg-surface-soft text-text outline-none" v-model="programDescription" rows="3" placeholder="Description of the program"></textarea>
          </label>
          <label class="flex items-center justify-between gap-4 p-4 border border-surface-outline rounded-[18px] bg-surface-soft cursor-pointer transition-colors hover:border-[rgba(88,166,255,0.4)]">
            <div class="flex flex-col">
              <span class="font-extrabold text-[1rem]">Active Program</span>
              <span class="text-text-muted text-[0.8rem]">Set this as your current workout rotation</span>
            </div>
            <div class="relative w-12 h-[26px] rounded-full transition-colors duration-200 ease-in-out shrink-0" :class="isActive ? 'bg-blue' : 'bg-surface-outline'">
              <span class="absolute top-[3px] left-[3px] w-5 h-5 bg-black rounded-full transition-transform duration-200 ease-in-out shadow-sm" :class="isActive ? 'translate-x-[22px]' : 'translate-x-0'"></span>
            </div>
            <input type="checkbox" class="sr-only" v-model="isActive" />
          </label>
        </div>
        
        <!-- Right Col: Quick Stats -->
        <div class="grid grid-cols-2 gap-5">
          <StatCard label="Total Splits" :value="String(totalSplits)" />
          <StatCard label="Total Exercises" :value="String(totalExercises)" />
        </div>
      </div>
    </SectionCard>

    <!-- Section: Splits -->
    <SectionCard title="Splits & Exercises" subtitle="Drag to reorder splits or exercises within splits">
      <template #header-actions>
        <button class="inline-flex items-center justify-center w-9 h-9 border border-surface-outline bg-surface-soft text-text rounded-xl" type="button" @click="addSplit" title="Add Split">
          <svg viewBox="0 0 24 24" class="w-5 h-5 fill-none stroke-current stroke-2 [stroke-linecap:round] [stroke-linejoin:round]">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </template>

      <div class="flex flex-col gap-3">
        <article
          v-for="(split, sIndex) in splits"
          :key="`split-${sIndex}`"
          class="flex flex-col gap-[14px] p-[18px] rounded-[22px] border border-surface-outline border-l-4 !border-l-blue bg-gradient-to-br from-[rgba(88,166,255,0.08)] to-surface-soft"
          draggable="true"
          @dragstart="onSplitDragStart($event, sIndex)"
          @dragover.prevent
          @drop="onSplitDrop($event, sIndex)"
          @dragend="onSplitDragEnd"
        >
          <div class="flex items-center gap-4 mb-3 w-full">
            <div class="cursor-grab text-text-muted text-[1.5rem] select-none p-2 active:cursor-grabbing max-sm:hidden" title="Drag to reorder split">≡</div>

            <div class="flex-1 flex flex-col sm:flex-row gap-2 w-full">
              <div class="flex items-center gap-2 w-full">
                <label class="flex flex-col gap-2 rounded-[18px] bg-[rgba(88,166,255,0.15)] border border-[rgba(88,166,255,0.4)] min-h-[46px] overflow-hidden" style="flex: 1; width: 100%;">
                  <input class="w-full h-full px-[18px] py-3 bg-transparent text-[1.05rem] font-extrabold text-blue uppercase tracking-wider placeholder:text-[rgba(88,166,255,0.5)] placeholder:normal-case placeholder:tracking-normal placeholder:font-normal outline-none" v-model="split.name" type="text" placeholder="Split Name" />
                </label>
                <div class="flex items-center justify-end shrink-0 w-fit sm:min-w-[auto] gap-2">
                  <button type="button" class="bg-transparent border-none text-text-muted cursor-pointer p-[2px_4px] text-[0.75rem] leading-none disabled:opacity-20 sm:hidden" @click.stop="moveSplitUp(sIndex)" :disabled="sIndex === 0">▲</button>
                  <button type="button" class="bg-transparent border-none text-text-muted cursor-pointer p-[2px_4px] text-[0.75rem] leading-none disabled:opacity-20 sm:hidden" @click.stop="moveSplitDown(sIndex)" :disabled="sIndex === splits.length - 1">▼</button>
                </div>
              </div>

              <div class="flex items-center gap-2 w-full">
                <label class="flex flex-col gap-2" style="flex: 1; width: 100%;">
                  <input class="w-full px-[18px] py-3 border border-surface-outline rounded-[18px] bg-surface-soft text-text outline-none" v-model="split.note" type="text" placeholder="Focus area" />
                </label>
                <div class="flex items-center justify-end shrink-0 w-fit sm:min-w-[auto] gap-2">
                  <button type="button" class="inline-flex items-center justify-center shrink-0 w-10 h-10 p-0 text-text-muted hover:text-danger hover:border-[rgba(248,81,73,0.4)] border border-transparent bg-transparent transition-colors rounded-xl" @click="removeSplit(sIndex)" title="Remove Split">
                    <svg class="w-4 h-4 fill-none stroke-current stroke-2 [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24">
                      <polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-2 pt-4 mt-2 border-t border-surface-outline">
            <div
              v-for="(exercise, eIndex) in split.exercises"
              :key="`ex-${sIndex}-${eIndex}`"
              class="flex items-center gap-3 bg-bg-elevated p-[8px_12px] rounded-xl border border-surface-outline"
              draggable="true"
              @dragstart.stop="onExerciseDragStart($event, sIndex, eIndex)"
              @dragover.prevent
              @drop.stop="onExerciseDrop($event, sIndex, eIndex)"
              @dragend.stop="onExerciseDragEnd"
            >
              <div class="cursor-grab text-text-muted text-[1.5rem] select-none p-2 active:cursor-grabbing max-sm:hidden" title="Drag to reorder exercise">≡</div>
              
              <div class="flex-1 flex flex-col sm:flex-row gap-2 w-full">
                <div class="flex items-center gap-2 w-full">
                  <label class="flex flex-col gap-2" style="flex: 1">
                    <div class="relative w-full">
                      <input 
                        class="w-full px-4 py-3 border border-surface-outline rounded-[18px] bg-surface-soft text-text outline-none cursor-pointer pr-10"
                        type="text" 
                        readonly
                        :value="exercise.name" 
                        placeholder="Select Exercise..." 
                        @click="openExerciseModal(sIndex, eIndex)"
                      />
                      <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted pointer-events-none" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    </div>
                  </label>
                </div>

                <div class="flex items-center gap-2 w-full justify-between">
                  <label class="flex items-center gap-2 justify-between" style="width: 100px;">
                    <input 
                      class="w-full px-3 py-3 border border-surface-outline rounded-[18px] bg-surface-soft text-text text-center pr-2 outline-none"
                      v-model="exercise.sets" 
                      type="number" 
                      min="1" 
                    />
                    <span class="text-text-muted text-[0.8rem]">sets</span>
                  </label>
                  
                  <div class="flex items-center justify-end shrink-0 w-fit sm:min-w-[auto] gap-2">
                    <button type="button" class="bg-transparent border-none text-text-muted cursor-pointer p-[2px_4px] text-[0.75rem] leading-none disabled:opacity-20 sm:hidden" @click.stop="moveExerciseUp(sIndex, eIndex)" :disabled="eIndex === 0">▲</button>
                    <button type="button" class="bg-transparent border-none text-text-muted cursor-pointer p-[2px_4px] text-[0.75rem] leading-none disabled:opacity-20 sm:hidden" @click.stop="moveExerciseDown(sIndex, eIndex)" :disabled="eIndex === split.exercises.length - 1">▼</button>
                    
                    <button type="button" class="inline-flex items-center justify-center shrink-0 w-10 h-10 p-0 text-text-muted hover:text-danger hover:border-[rgba(248,81,73,0.4)] border border-transparent bg-transparent transition-colors rounded-xl" @click="removeExercise(sIndex, eIndex)">
                      <svg class="w-4 h-4 fill-none stroke-current stroke-2 [stroke-linecap:round] [stroke-linejoin:round]" viewBox="0 0 24 24">
                        <polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <button class="inline-flex items-center justify-center gap-2 self-start text-[0.85rem] px-3 min-h-[36px] mt-1 font-bold cursor-pointer rounded-xl border-0 bg-[rgba(88,166,255,0.14)] text-blue transition-colors hover:bg-[rgba(88,166,255,0.22)]" type="button" @click="addExercise(sIndex)">+ Add Exercise</button>
          </div>
        </article>
      </div>
      
      <div class="flex flex-wrap items-stretch justify-end gap-4 mt-6 [&>*]:flex-1">
        <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" type="button" @click="saveProgram">
          {{ isCreateMode ? 'Create Program' : 'Save Changes' }}
        </button>
        <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" to="/programs">Cancel</RouterLink>
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
