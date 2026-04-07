<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import { programBuilderData } from '../data/mockData'

const route = useRoute()

const isCreateMode = computed(() => route.path.endsWith('/new'))
const selectedSplit = computed(() => {
  if (isCreateMode.value) {
    return {
      name: '',
      note: '',
      exercises: [
        { name: '', meta: '', rest: '', target: '' },
        { name: '', meta: '', rest: '', target: '' },
      ],
    }
  }

  const splitName = decodeURIComponent(route.params.splitName ?? '')
  return programBuilderData.splits.find((split) => split.name.toLowerCase() === splitName.toLowerCase()) ?? programBuilderData.splits[0]
})
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
            <div class="builder-editor__head">
              <div>
                <p class="text-text-muted text-[0.78rem] tracking-[0.12em] uppercase m-0">Exercise {{ exerciseIndex + 1 }}</p>
                <h3>{{ exercise.name || 'New Exercise' }}</h3>
              </div>
            </div>

            <div class="field-stack">
              <label class="flex flex-col gap-2">
                <span>Exercise name</span>
                <input :value="exercise.name" type="text" placeholder="Example: Bench Press" />
              </label>

              <label class="flex flex-col gap-2">
                <span>Set and rep target</span>
                <input :value="exercise.meta" type="text" placeholder="4 sets - 6-8 reps" />
              </label>

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
        <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" type="button">+ Add Exercise</button>
        <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" type="button">{{ isCreateMode ? 'Save Split' : 'Update Split' }}</button>
      </div>
    </SectionCard>
  </div>
</template>
