<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import { apiRoutes } from '../services/api'
import { splitSelectorData } from '../data/mockData'

const router = useRouter()
const pendingAction = ref(null)

const dialogTitle = computed(() => {
  if (!pendingAction.value) {
    return ''
  }

  if (pendingAction.value.status === 'Next') return 'Start next split?'
  return pendingAction.value.status === 'Done' ? 'Repeat completed split?' : 'Skip current split?'
})

const dialogMessage = computed(() => {
  if (!pendingAction.value) {
    return ''
  }

  if (pendingAction.value.status === 'Next') {
    return `Are you ready to start ${pendingAction.value.name}? This will open your active workout session.`
  }

  return pendingAction.value.status === 'Done'
    ? `You already finished ${pendingAction.value.name}. Start it again anyway?`
    : `${pendingAction.value.name} is not the recommended next split. Skip the current rotation order and start it anyway?`
})

function startSplit(split) {
  router.push(`/workout/active?split=${encodeURIComponent(split.name)}`)
}

function handleSplitAction(split) {
  pendingAction.value = split
}

function confirmSplitAction() {
  if (!pendingAction.value) {
    return
  }

  startSplit(pendingAction.value)
  pendingAction.value = null
}

function closeDialog() {
  pendingAction.value = null
}
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <PageHero
      title="Split Selector"
      description="Choose the workout split you want to perform today."
    />

    <div class="grid gap-5">
      <article
        v-for="split in splitSelectorData.splits"
        :key="split.name"
        class="group p-6 border border-surface-outline rounded-[28px] bg-gradient-to-b from-[rgba(22,27,34,0.98)] to-[rgba(15,20,27,0.98)] shadow-custom transition-all"
        :class="{
          'border-[rgba(88,166,255,0.3)] shadow-[0_0_20px_rgba(88,166,255,0.1)]': split.status === 'Next',
          'opacity-70': split.status === 'Done'
        }"
      >
        <div class="flex items-center justify-between gap-4">
          <div class="min-w-0">
            <h3 class="m-0 text-xl font-extrabold uppercase tracking-tight">{{ split.name }}</h3>
            <p class="m-0 mt-1.5 text-text-muted text-sm">{{ split.description }}</p>
          </div>

          <div class="flex items-center gap-3 shrink-0">
            <span
              class="px-3 py-1.5 rounded-full text-[0.72rem] font-black uppercase tracking-wider border"
              :class="{
                'bg-blue/10 text-blue border-blue/20': split.status === 'Next',
                'bg-green/10 text-green border-green/20': split.status === 'Done',
                'bg-surface-soft text-text-muted border-surface-outline': split.status === 'Pending'
              }"
            >
              {{ split.status }}
            </span>

            <button
              class="w-11 h-11 flex items-center justify-center rounded-2xl transition-all active:scale-95"
              :class="split.status === 'Next' ? 'bg-gradient-to-b from-blue to-blue-strong text-bg shadow-lg' : 'bg-surface-soft border border-surface-outline text-text-muted hover:text-text'"
              type="button"
              @click="handleSplitAction(split)"
            >
              <svg class="w-6 h-6 fill-current" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M8 6.5V17.5L17 12L8 6.5Z" />
              </svg>
            </button>
          </div>
        </div>
      </article>
    </div>

    <!-- <SectionCard title="Backend route" subtitle="Used to color-code completed vs pending splits">
      <div class="api-note">
        <p><strong>GET</strong> {{ apiRoutes.programs.rotationStatus(':programId') }}</p>
      </div>
    </SectionCard> -->

    <div v-if="pendingAction" class="dialog-backdrop" @click.self="closeDialog">
      <section class="dialog-card">
        <h2 class="dialog-card__title">{{ dialogTitle }}</h2>
        <p class="dialog-card__copy">{{ dialogMessage }}</p>

        <div class="flex gap-3 mt-6">
          <button class="flex-1 inline-flex items-center justify-center gap-2 min-h-[48px] px-4 rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text transition-colors hover:bg-surface-soft-hover" type="button" @click="closeDialog">Cancel</button>
          <button class="flex-1 inline-flex items-center justify-center gap-2 min-h-[48px] px-4 rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg transition-opacity active:opacity-80" type="button" @click="confirmSplitAction">Continue</button>
        </div>
      </section>
    </div>
  </div>
</template>
