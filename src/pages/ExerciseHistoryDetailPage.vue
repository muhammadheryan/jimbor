<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import { historyData } from '../data/mockData'

const route = useRoute()

const historyYear = 2026
const monthIndexMap = {
  Jan: 0,
  Feb: 1,
  Mar: 2,
  Apr: 3,
  May: 4,
  Jun: 5,
  Jul: 6,
  Aug: 7,
  Sep: 8,
  Oct: 9,
  Nov: 10,
  Dec: 11,
}

const statusStyles = {
  Fresh: 'pill--success',
  Normal: 'pill--primary',
  Tired: 'pill--warning',
  Sick: 'pill--danger',
}

const chartFrame = {
  width: 760,
  height: 380,
  paddingTop: 20,
  paddingRight: 56,
  paddingBottom: 44,
  paddingLeft: 56,
}

const exerciseName = computed(() => decodeURIComponent(route.params.exerciseName ?? ''))

const buildEmptyExerciseDetail = (name) => ({
  name: name || 'Exercise',
  summary: 'No data yet',
  note: 'No recorded sessions for this exercise yet.',
  sessions: [],
})

const exerciseDetail = computed(
  () =>
    historyData.exerciseLibrary.find((item) => item.name.toLowerCase() === exerciseName.value.toLowerCase()) ??
    buildEmptyExerciseDetail(exerciseName.value),
)

const parseSessionDetail = (detail) => {
  const match = detail.match(/(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)\s*@\s*(\d+(?:\.\d+)?)kg/i)

  if (!match) {
    return { sets: 0, reps: 0, weight: 0 }
  }

  return {
    sets: Number(match[1]),
    reps: Number(match[2]),
    weight: Number(match[3]),
  }
}

const parseSessionDate = (dateLabel) => {
  const [monthLabel, dayLabel] = String(dateLabel ?? '').replace(',', '').split(' ')
  const monthIndex = monthIndexMap[monthLabel]
  const day = Number(dayLabel)

  if (monthIndex === undefined || Number.isNaN(day)) {
    return null
  }

  return new Date(historyYear, monthIndex, day)
}

const toIsoDate = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

const formatShortDate = (date) =>
  date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  })

const parsedSessions = computed(() =>
  exerciseDetail.value.sessions
    .map((session) => {
      const parsedDate = parseSessionDate(session.date)

      if (!parsedDate) {
        return null
      }

      const metrics = parseSessionDetail(session.detail)

      return {
        ...session,
        ...metrics,
        timestamp: parsedDate.getTime(),
        isoDate: toIsoDate(parsedDate),
        axisLabel: formatShortDate(parsedDate),
      }
    })
    .filter(Boolean)
    .sort((a, b) => a.timestamp - b.timestamp),
)

const rangeStart = ref('')
const rangeEnd = ref('')
const activeRangePreset = ref('all')

const minAvailableDate = computed(() => parsedSessions.value[0]?.isoDate ?? '')
const maxAvailableDate = computed(() => parsedSessions.value.at(-1)?.isoDate ?? '')

watch(
  exerciseDetail,
  () => {
    rangeStart.value = minAvailableDate.value
    rangeEnd.value = maxAvailableDate.value
    activeRangePreset.value = 'all'
  },
  { immediate: true },
)

const normalizedRange = computed(() => {
  const fallbackStart = parsedSessions.value[0]?.timestamp ?? 0
  const fallbackEnd = parsedSessions.value.at(-1)?.timestamp ?? 0
  const rawStart = rangeStart.value ? new Date(`${rangeStart.value}T00:00:00`).getTime() : fallbackStart
  const rawEnd = rangeEnd.value ? new Date(`${rangeEnd.value}T23:59:59`).getTime() : fallbackEnd

  return rawStart <= rawEnd ? { start: rawStart, end: rawEnd } : { start: rawEnd, end: rawStart }
})

const filteredChartSessions = computed(() =>
  parsedSessions.value.filter(
    (session) => session.timestamp >= normalizedRange.value.start && session.timestamp <= normalizedRange.value.end,
  ),
)

const filteredSessionHistory = computed(() => [...filteredChartSessions.value].sort((a, b) => b.timestamp - a.timestamp))
const historyPage = ref(1)
const historyPageSize = 5
const selectedSessionDetail = ref(null)
const isChartFullscreen = ref(false)
const activeChartPointIndex = ref(-1)
const isChartScrubbing = ref(false)

const latestSession = computed(() => filteredChartSessions.value.at(-1) ?? null)
const bestWeight = computed(() =>
  filteredChartSessions.value.length ? Math.max(...filteredChartSessions.value.map((session) => session.weight)) : 0,
)
const averageReps = computed(() => {
  if (!filteredChartSessions.value.length) {
    return 0
  }

  const totalReps = filteredChartSessions.value.reduce((sum, session) => sum + session.reps, 0)
  return totalReps / filteredChartSessions.value.length
})

const applyQuickRange = (days) => {
  if (!parsedSessions.value.length) {
    return
  }

  if (days === 'all') {
    rangeStart.value = minAvailableDate.value
    rangeEnd.value = maxAvailableDate.value
    activeRangePreset.value = 'all'
    return
  }

  const endDate = new Date(maxAvailableDate.value)
  const startDate = new Date(endDate)
  startDate.setDate(startDate.getDate() - Number(days) + 1)

  const boundedStart =
    startDate.getTime() < new Date(minAvailableDate.value).getTime() ? new Date(minAvailableDate.value) : startDate

  rangeStart.value = toIsoDate(boundedStart)
  rangeEnd.value = maxAvailableDate.value
  activeRangePreset.value = `${days}d`
}

const buildDomain = (values, minimumPadding = 0) => {
  if (!values.length) {
    return { min: 0, max: 1 }
  }

  const minValue = Math.min(...values)
  const maxValue = Math.max(...values)

  if (minValue === maxValue) {
    return {
      min: Math.max(0, minValue - 1 - minimumPadding),
      max: maxValue + 1 + minimumPadding,
    }
  }

  const spread = maxValue - minValue
  return {
    min: Math.max(0, minValue - spread * 0.12 - minimumPadding),
    max: maxValue + spread * 0.12 + minimumPadding,
  }
}

const weightDomain = computed(() => buildDomain(filteredChartSessions.value.map((session) => session.weight), 0))
const repDomain = computed(() => buildDomain(filteredChartSessions.value.map((session) => session.reps), 0.4))

const plotWidth = chartFrame.width - chartFrame.paddingLeft - chartFrame.paddingRight
const plotHeight = chartFrame.height - chartFrame.paddingTop - chartFrame.paddingBottom

const projectY = (value, domain) => {
  const span = domain.max - domain.min || 1
  const normalizedValue = (value - domain.min) / span
  return chartFrame.paddingTop + plotHeight - normalizedValue * plotHeight
}

const chartPoints = computed(() =>
  filteredChartSessions.value.map((session, index, sessions) => {
    const x =
      sessions.length === 1
        ? chartFrame.paddingLeft + plotWidth / 2
        : chartFrame.paddingLeft + (index * plotWidth) / (sessions.length - 1)

    return {
      ...session,
      x,
      weightY: projectY(session.weight, weightDomain.value),
      repsY: projectY(session.reps, repDomain.value),
    }
  }),
)

const activeChartPoint = computed(() => {
  if (!chartPoints.value.length) {
    return null
  }

  const fallbackIndex = chartPoints.value.length - 1
  const safeIndex =
    activeChartPointIndex.value >= 0 && activeChartPointIndex.value < chartPoints.value.length
      ? activeChartPointIndex.value
      : fallbackIndex

  return chartPoints.value[safeIndex] ?? null
})

const buildLinePath = (points, key) =>
  points.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x} ${point[key]}`).join(' ')

const weightPath = computed(() => buildLinePath(chartPoints.value, 'weightY'))
const repPath = computed(() => buildLinePath(chartPoints.value, 'repsY'))

const axisTicks = computed(() =>
  Array.from({ length: 4 }, (_, index) => {
    const ratio = index / 3
    const y = chartFrame.paddingTop + ratio * plotHeight
    const weightValue = weightDomain.value.max - ratio * (weightDomain.value.max - weightDomain.value.min)
    const repValue = repDomain.value.max - ratio * (repDomain.value.max - repDomain.value.min)

    return {
      y,
      weightLabel: `${weightValue.toFixed(weightValue >= 100 ? 0 : 1).replace(/\.0$/, '')} kg`,
      repLabel: `${repValue.toFixed(repValue >= 10 ? 0 : 1).replace(/\.0$/, '')} reps`,
    }
  }),
)

const rangeSummary = computed(() => {
  if (!filteredChartSessions.value.length) {
    return 'No sessions in this range.'
  }

  const startLabel = filteredChartSessions.value[0]?.axisLabel
  const endLabel = filteredChartSessions.value.at(-1)?.axisLabel
  return `${startLabel} to ${endLabel}`
})

const totalHistoryPages = computed(() => Math.max(1, Math.ceil(filteredSessionHistory.value.length / historyPageSize)))
const paginatedSessionHistory = computed(() => {
  const startIndex = (historyPage.value - 1) * historyPageSize
  return filteredSessionHistory.value.slice(startIndex, startIndex + historyPageSize)
})

watch(filteredSessionHistory, () => {
  historyPage.value = 1
})

watch(
  chartPoints,
  (points) => {
    if (!points.length) {
      activeChartPointIndex.value = -1
      return
    }

    if (activeChartPointIndex.value < 0 || activeChartPointIndex.value >= points.length) {
      activeChartPointIndex.value = points.length - 1
    }
  },
  { immediate: true },
)

const goToPreviousHistoryPage = () => {
  historyPage.value = Math.max(1, historyPage.value - 1)
}

const goToNextHistoryPage = () => {
  historyPage.value = Math.min(totalHistoryPages.value, historyPage.value + 1)
}

const openSessionDetail = (session) => {
  selectedSessionDetail.value = session
}

const closeSessionDetail = () => {
  selectedSessionDetail.value = null
}

const openChartFullscreen = () => {
  isChartFullscreen.value = true
}

const closeChartFullscreen = () => {
  isChartFullscreen.value = false
}

const setFullscreenScrollLock = (locked) => {
  if (typeof document === 'undefined') {
    return
  }

  document.documentElement.style.overflow = locked ? 'hidden' : ''
  document.documentElement.style.overscrollBehavior = locked ? 'none' : ''
  document.body.style.overflow = locked ? 'hidden' : ''
  document.body.style.overscrollBehavior = locked ? 'none' : ''
}

const clamp = (value, min, max) => Math.min(Math.max(value, min), max)

const updateChartPointFromPointer = (event) => {
  if (!chartPoints.value.length) {
    return
  }

  const bounds = event.currentTarget?.getBoundingClientRect?.()
  if (!bounds?.width) {
    return
  }

  const ratio = clamp((event.clientX - bounds.left) / bounds.width, 0, 1)
  const index = chartPoints.value.length === 1 ? 0 : Math.round(ratio * (chartPoints.value.length - 1))
  activeChartPointIndex.value = index
}

const beginChartScrub = (event) => {
  isChartScrubbing.value = true
  event.currentTarget?.setPointerCapture?.(event.pointerId)
  updateChartPointFromPointer(event)
}

const handleChartScrubMove = (event) => {
  if (!chartPoints.value.length || (!isChartScrubbing.value && event.pointerType !== 'mouse')) {
    return
  }

  updateChartPointFromPointer(event)
}

const endChartScrub = (event) => {
  if (event?.pointerId !== undefined) {
    event.currentTarget?.releasePointerCapture?.(event.pointerId)
  }

  isChartScrubbing.value = false
}

const getChartTooltipStyle = (point, maxWidth = 196, sidePadding = 12) => {
  if (!point) {
    return {}
  }

  const safeX = clamp(point.x, sidePadding + maxWidth / 2, chartFrame.width - sidePadding - maxWidth / 2)

  return {
    left: `${(safeX / chartFrame.width) * 100}%`,
    top: `${chartFrame.paddingTop + 12}px`,
    width: `min(${maxWidth}px, calc(100% - ${sidePadding * 2}px))`,
    transform: 'translateX(-50%)',
  }
}

watch(isChartFullscreen, (isOpen) => {
  setFullscreenScrollLock(isOpen)
})

onBeforeUnmount(() => {
  setFullscreenScrollLock(false)
})
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <PageHero
      :title="exerciseDetail.name"
      :description="exerciseDetail.note"
    />

    <div class="flex justify-end gap-2 w-full">

      <div class="flex flex-wrap gap-2">
        <button
          type="button"
          class="inline-flex min-h-[42px] items-center justify-center rounded-[14px] px-4 font-bold transition-colors"
          :class="activeRangePreset === '7d' ? 'bg-[rgba(88,166,255,0.16)] text-blue border border-[rgba(88,166,255,0.24)]' : 'bg-surface-soft text-text-muted border border-surface-outline'"
          @click="applyQuickRange(7)"
        >
          7D
        </button>
        <button
          type="button"
          class="inline-flex min-h-[42px] items-center justify-center rounded-[14px] px-4 font-bold transition-colors"
          :class="activeRangePreset === '30d' ? 'bg-[rgba(88,166,255,0.16)] text-blue border border-[rgba(88,166,255,0.24)]' : 'bg-surface-soft text-text-muted border border-surface-outline'"
          @click="applyQuickRange(30)"
        >
          30D
        </button>
        <button
          type="button"
          class="inline-flex min-h-[42px] items-center justify-center rounded-[14px] px-4 font-bold transition-colors"
          :class="activeRangePreset === 'all' ? 'bg-[rgba(88,166,255,0.16)] text-blue border border-[rgba(88,166,255,0.24)]' : 'bg-surface-soft text-text-muted border border-surface-outline'"
          @click="applyQuickRange('all')"
        >
          All
        </button>
      </div>
    </div>

    <!-- <div class="grid gap-5 grid-cols-[repeat(auto-fit,minmax(220px,1fr))]">
      <article class="p-[18px] bg-surface-soft border border-surface-outline rounded-[24px] shadow-custom">
        <p class="m-0 text-[0.78rem] uppercase tracking-[0.12em] text-text-muted">Latest Weight</p>
        <h2 class="m-0 mt-2 text-[2rem] font-black text-green">{{ latestSession ? `${latestSession.weight} kg` : '-' }}</h2>
        <p class="m-0 mt-2 text-text-muted">{{ latestSession ? latestSession.detail : 'No data in selected range.' }}</p>
      </article>

      <article class="p-[18px] bg-surface-soft border border-surface-outline rounded-[24px] shadow-custom">
        <p class="m-0 text-[0.78rem] uppercase tracking-[0.12em] text-text-muted">Best Weight</p>
        <h2 class="m-0 mt-2 text-[2rem] font-black text-blue">{{ bestWeight ? `${bestWeight} kg` : '-' }}</h2>
        <p class="m-0 mt-2 text-text-muted">Highest recorded weight in the current range.</p>
      </article>

      <article class="p-[18px] bg-surface-soft border border-surface-outline rounded-[24px] shadow-custom">
        <p class="m-0 text-[0.78rem] uppercase tracking-[0.12em] text-text-muted">Average Reps</p>
        <h2 class="m-0 mt-2 text-[2rem] font-black text-text">{{ averageReps ? averageReps.toFixed(1) : '-' }}</h2>
        <p class="m-0 mt-2 text-text-muted">Average reps across the selected sessions.</p>
      </article>
    </div> -->

    <SectionCard title="Progress Chart" subtitle="Weight and reps by training date." class="p-4 md:p-5">
      <div class="flex flex-col gap-5">
        <div class="flex items-center justify-between gap-3">
          <div class="min-w-0 flex-1">
            <p class="m-0 text-text-soft">{{ rangeSummary }}</p>
          </div>

          <button
            type="button"
            class="inline-flex shrink-0 min-h-[42px] items-center justify-center gap-2 rounded-[14px] border border-surface-outline bg-surface-soft px-4 font-bold text-text md:hidden"
            @click="openChartFullscreen"
          >
            <svg class="w-4 h-4 fill-none stroke-current stroke-2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
              <path d="M8 3H5a2 2 0 0 0-2 2v3" />
              <path d="M16 3h3a2 2 0 0 1 2 2v3" />
              <path d="M8 21H5a2 2 0 0 1-2-2v-3" />
              <path d="M16 21h3a2 2 0 0 0 2-2v-3" />
            </svg>
            Full Screen
          </button>
        </div>

        <div v-if="chartPoints.length" class="-mx-1 rounded-[28px] border border-surface-outline bg-[linear-gradient(180deg,rgba(88,166,255,0.08)_0%,rgba(15,20,27,0.96)_100%)] p-3 md:p-4">
          <div class="mb-4 flex flex-wrap items-center gap-4">
            <div class="inline-flex items-center gap-2 text-sm text-text-soft">
              <span class="h-3 w-3 rounded-full bg-green"></span>
              Weight
            </div>
            <div class="inline-flex items-center gap-2 text-sm text-text-soft">
              <span class="h-3 w-3 rounded-full bg-blue"></span>
              Reps
            </div>
          </div>

          <div class="relative">
            <div
              v-if="activeChartPoint"
              class="pointer-events-none absolute z-10 rounded-[16px] border border-[rgba(15,23,42,0.1)] bg-white/95 px-2.5 py-2 text-slate-900 shadow-[0_14px_26px_rgba(15,23,42,0.16)] backdrop-blur-sm md:rounded-[18px] md:px-3 md:py-2.5 md:shadow-[0_16px_30px_rgba(15,23,42,0.18)]"
              :style="getChartTooltipStyle(activeChartPoint, 116, 10)"
            >
              <p class="m-0 hidden text-[0.6rem] font-bold uppercase tracking-[0.12em] text-slate-500 md:block">Selected Session</p>
              <p class="m-0 text-[0.7rem] font-extrabold md:mt-1 md:text-[0.82rem]">{{ activeChartPoint.date }}</p>
              <p class="m-0 mt-0.5 hidden text-[0.68rem] leading-[1.3] text-slate-600 md:block md:text-[0.72rem] md:leading-[1.35]">{{ activeChartPoint.detail }}</p>
              <div class="mt-1.5 flex items-center gap-2 md:gap-3">
                <div>
                  <p class="m-0 text-[0.58rem] font-bold uppercase tracking-[0.12em] text-slate-400">Weight</p>
                  <p class="m-0 mt-0.5 text-[0.82rem] font-black text-green md:text-[1.05rem]">{{ activeChartPoint.weight }} kg</p>
                </div>
                <div>
                  <p class="m-0 text-[0.58rem] font-bold uppercase tracking-[0.12em] text-slate-400">Reps</p>
                  <p class="m-0 mt-0.5 text-[0.82rem] font-black text-blue md:text-[1.05rem]">{{ activeChartPoint.reps }}</p>
                </div>
              </div>
            </div>

            <svg :viewBox="`0 0 ${chartFrame.width} ${chartFrame.height}`" class="w-full overflow-visible">
              <g>
                <line
                  v-for="tick in axisTicks"
                  :key="`grid-${tick.y}`"
                  :x1="chartFrame.paddingLeft"
                  :x2="chartFrame.width - chartFrame.paddingRight"
                  :y1="tick.y"
                  :y2="tick.y"
                  stroke="rgba(240,246,252,0.08)"
                  stroke-dasharray="4 6"
                />
              </g>

              <g>
                <text
                  v-for="tick in axisTicks"
                  :key="`weight-${tick.y}`"
                  :x="chartFrame.paddingLeft - 12"
                  :y="tick.y + 4"
                  fill="rgba(240,246,252,0.62)"
                  font-size="11"
                  text-anchor="end"
                >
                  {{ tick.weightLabel }}
                </text>

                <text
                  v-for="tick in axisTicks"
                  :key="`reps-${tick.y}`"
                  :x="chartFrame.width - chartFrame.paddingRight + 12"
                  :y="tick.y + 4"
                  fill="rgba(240,246,252,0.62)"
                  font-size="11"
                  text-anchor="start"
                >
                  {{ tick.repLabel }}
                </text>
              </g>

              <g>
                <path :d="weightPath" fill="none" stroke="var(--green)" stroke-linecap="round" stroke-linejoin="round" stroke-width="3.5" />
                <path :d="repPath" fill="none" stroke="var(--blue)" stroke-linecap="round" stroke-linejoin="round" stroke-width="3.5" />
              </g>

              <g v-if="activeChartPoint">
                <line
                  :x1="activeChartPoint.x"
                  :x2="activeChartPoint.x"
                  :y1="chartFrame.paddingTop"
                  :y2="chartFrame.height - chartFrame.paddingBottom"
                  stroke="rgba(88,166,255,0.72)"
                  stroke-width="2"
                  stroke-dasharray="6 6"
                />
                <circle
                  :cx="activeChartPoint.x"
                  :cy="chartFrame.height - chartFrame.paddingBottom"
                  r="9"
                  fill="rgba(88,166,255,0.22)"
                  stroke="var(--blue)"
                  stroke-width="2"
                />
              </g>

              <g>
                <g v-for="point in chartPoints" :key="`weight-point-${point.isoDate}`">
                  <circle :cx="point.x" :cy="point.weightY" :r="activeChartPoint?.isoDate === point.isoDate ? 7.5 : 6" fill="var(--green)" />
                  <circle :cx="point.x" :cy="point.weightY" :r="activeChartPoint?.isoDate === point.isoDate ? 14 : 11" fill="rgba(57,211,83,0.12)" />
                </g>

                <g v-for="point in chartPoints" :key="`rep-point-${point.isoDate}`">
                  <circle :cx="point.x" :cy="point.repsY" :r="activeChartPoint?.isoDate === point.isoDate ? 7.5 : 6" fill="var(--blue)" />
                  <circle :cx="point.x" :cy="point.repsY" :r="activeChartPoint?.isoDate === point.isoDate ? 14 : 11" fill="rgba(88,166,255,0.12)" />
                </g>
              </g>

              <g>
                <text
                  v-for="point in chartPoints"
                  :key="`label-${point.isoDate}`"
                  :x="point.x"
                  :y="chartFrame.height - 10"
                  :fill="activeChartPoint?.isoDate === point.isoDate ? 'rgba(240,246,252,0.92)' : 'rgba(240,246,252,0.62)'"
                  font-size="11"
                  text-anchor="middle"
                  :font-weight="activeChartPoint?.isoDate === point.isoDate ? '700' : '500'"
                >
                  {{ point.axisLabel }}
                </text>
              </g>

              <rect
                :x="chartFrame.paddingLeft"
                :y="chartFrame.paddingTop"
                :width="plotWidth"
                :height="plotHeight"
                fill="transparent"
                class="cursor-ew-resize touch-none"
                @pointerdown="beginChartScrub"
                @pointermove="handleChartScrubMove"
                @pointerup="endChartScrub"
                @pointercancel="endChartScrub"
              />
            </svg>
          </div>
        </div>

        <div v-else class="rounded-[24px] border border-surface-outline bg-surface-soft px-5 py-10 text-center text-text-muted">
          No chart data in this date range.
        </div>
      </div>
    </SectionCard>

    <SectionCard title="Session History" subtitle="Date, weight, and reps for the selected range.">
      <div v-if="filteredSessionHistory.length" class="flex flex-col gap-4">
        <div class="overflow-hidden rounded-[24px] border border-surface-outline bg-surface-soft">
          <div class="overflow-x-auto">
            <table class="min-w-full border-collapse">
              <thead>
                <tr class="border-b border-surface-outline bg-[rgba(255,255,255,0.03)] text-left">
                  <th class="px-4 py-3 text-[0.78rem] font-bold uppercase tracking-[0.12em] text-text-muted">Date</th>
                  <th class="px-4 py-3 text-[0.78rem] font-bold uppercase tracking-[0.12em] text-text-muted">Weight</th>
                  <th class="px-4 py-3 text-[0.78rem] font-bold uppercase tracking-[0.12em] text-text-muted">Reps</th>
                  <th class="px-4 py-3 text-[0.78rem] font-bold uppercase tracking-[0.12em] text-text-muted">Detail</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="session in paginatedSessionHistory"
                  :key="`${session.isoDate}-${session.detail}`"
                  class="border-b border-[rgba(240,246,252,0.05)] last:border-b-0"
                >
                  <td class="px-4 py-4 text-sm font-bold text-text">{{ session.date }}</td>
                  <td class="px-4 py-4 text-sm text-text-soft">{{ session.weight }} kg</td>
                  <td class="px-4 py-4 text-sm text-text-soft">{{ session.reps }}</td>
                  <td class="px-4 py-4 text-sm text-text-soft">
                    <button
                      type="button"
                      class="inline-flex min-h-[38px] items-center justify-center rounded-[12px] border border-[rgba(88,166,255,0.24)] bg-[rgba(88,166,255,0.12)] px-3 font-bold text-blue transition-colors hover:bg-[rgba(88,166,255,0.2)]"
                      @click="openSessionDetail(session)"
                    >
                      View
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="flex items-center justify-between gap-3">
          <p class="m-0 text-sm text-text-muted">Page {{ historyPage }} of {{ totalHistoryPages }}</p>

          <div class="flex gap-2">
            <button
              type="button"
              class="inline-flex min-h-[42px] items-center justify-center rounded-[14px] border border-surface-outline bg-surface-soft px-4 font-bold text-text transition-colors disabled:cursor-not-allowed disabled:opacity-50"
              :disabled="historyPage === 1"
              @click="goToPreviousHistoryPage"
            >
              Prev
            </button>
            <button
              type="button"
              class="inline-flex min-h-[42px] items-center justify-center rounded-[14px] border border-surface-outline bg-surface-soft px-4 font-bold text-text transition-colors disabled:cursor-not-allowed disabled:opacity-50"
              :disabled="historyPage === totalHistoryPages"
              @click="goToNextHistoryPage"
            >
              Next
            </button>
          </div>
        </div>
      </div>

      <div v-else class="rounded-[20px] border border-surface-outline bg-surface-soft px-5 py-10 text-center text-text-muted">
        No sessions found for this date range.
      </div>
    </SectionCard>

    <div v-if="selectedSessionDetail" class="fixed inset-0 z-[1300] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm" @click.self="closeSessionDetail">
      <section class="w-full max-w-[460px] max-h-[80vh] flex flex-col p-6 rounded-[28px] bg-bg-elevated border border-surface-outline shadow-custom">
        <div class="flex items-center justify-between mb-5 gap-4">
          <div>
            <h2 class="m-0 text-xl font-extrabold">Session Detail</h2>
            <p class="m-0 mt-1 text-sm text-text-muted">{{ selectedSessionDetail.date }}</p>
          </div>
          <button class="p-2 bg-transparent text-text-muted cursor-pointer border-0" @click="closeSessionDetail">
            <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>

        <div class="flex flex-col gap-4 overflow-y-auto">
          <article class="rounded-[22px] border border-surface-outline bg-surface-soft p-4">
            <p class="m-0 text-[0.78rem] uppercase tracking-[0.12em] text-text-muted">Notes</p>
            <p class="m-0 mt-2 text-text leading-[1.6]">{{ selectedSessionDetail.detail }}</p>
          </article>

          <article class="rounded-[22px] border border-surface-outline bg-surface-soft p-4">
            <p class="m-0 text-[0.78rem] uppercase tracking-[0.12em] text-text-muted">Condition</p>
            <div class="mt-3">
              <span class="inline-flex items-center gap-2 w-fit px-3 py-2 rounded-full bg-surface text-text-muted text-[0.8rem] font-bold" :class="statusStyles[selectedSessionDetail.flag] || 'pill--warning'">
                {{ selectedSessionDetail.flag }}
              </span>
            </div>
          </article>

          <article class="rounded-[22px] border border-surface-outline bg-surface-soft p-4">
            <p class="m-0 text-[0.78rem] uppercase tracking-[0.12em] text-text-muted">Summary</p>
            <div class="mt-3 grid grid-cols-2 gap-3">
              <div class="rounded-[18px] bg-[rgba(255,255,255,0.03)] p-3">
                <p class="m-0 text-[0.75rem] uppercase tracking-[0.1em] text-text-muted">Weight</p>
                <p class="m-0 mt-2 text-lg font-bold text-text">{{ selectedSessionDetail.weight }} kg</p>
              </div>
              <div class="rounded-[18px] bg-[rgba(255,255,255,0.03)] p-3">
                <p class="m-0 text-[0.75rem] uppercase tracking-[0.1em] text-text-muted">Reps</p>
                <p class="m-0 mt-2 text-lg font-bold text-text">{{ selectedSessionDetail.reps }}</p>
              </div>
            </div>
          </article>
        </div>
      </section>
    </div>

    <div v-if="isChartFullscreen" class="fixed inset-0 z-[1350] overflow-hidden overscroll-none bg-black/80 backdrop-blur-sm md:hidden">
      <div class="absolute inset-0 overflow-hidden overscroll-none touch-none">
        <div
          class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rotate-90 origin-center overflow-hidden"
          :style="{ width: 'calc(100dvh - 24px)', height: 'calc(100dvw - 24px)' }"
        >
          <div class="flex h-full w-full flex-col overflow-hidden rounded-[24px] border border-surface-outline bg-bg-elevated p-3 shadow-custom">
          <div class="mb-4 flex items-center justify-between gap-4">
            <div class="flex flex-wrap items-center gap-4">
              <div class="inline-flex items-center gap-2 text-sm text-text-soft">
                <span class="h-3 w-3 rounded-full bg-green"></span>
                Weight
              </div>
              <div class="inline-flex items-center gap-2 text-sm text-text-soft">
                <span class="h-3 w-3 rounded-full bg-blue"></span>
                Reps
              </div>
            </div>
            <div class="flex items-center gap-3">
              <p class="m-0 text-right text-sm text-text-muted">{{ rangeSummary }}</p>
              <button class="p-2 bg-transparent text-text-muted cursor-pointer border-0" @click="closeChartFullscreen">
                <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              </button>
            </div>
          </div>

          <div v-if="chartPoints.length" class="min-h-0 flex-1 overflow-hidden rounded-[24px] border border-surface-outline bg-[linear-gradient(180deg,rgba(88,166,255,0.08)_0%,rgba(15,20,27,0.96)_100%)] p-3">
            <div class="relative h-full overflow-hidden">
              <div
                v-if="activeChartPoint"
                class="pointer-events-none absolute z-10 rounded-[16px] border border-[rgba(15,23,42,0.1)] bg-white/95 px-3 py-2 text-slate-900 shadow-[0_16px_30px_rgba(15,23,42,0.18)] backdrop-blur-sm"
                :style="getChartTooltipStyle(activeChartPoint, 112, 10)"
              >
                <p class="m-0 text-[0.68rem] font-extrabold">{{ activeChartPoint.date }}</p>
                <div class="mt-1.5 flex items-center gap-2">
                  <div>
                    <p class="m-0 text-[0.56rem] font-bold uppercase tracking-[0.12em] text-slate-400">Weight</p>
                    <p class="m-0 mt-0.5 text-[0.8rem] font-black text-green">{{ activeChartPoint.weight }} kg</p>
                  </div>
                  <div>
                    <p class="m-0 text-[0.56rem] font-bold uppercase tracking-[0.12em] text-slate-400">Reps</p>
                    <p class="m-0 mt-0.5 text-[0.8rem] font-black text-blue">{{ activeChartPoint.reps }}</p>
                  </div>
                </div>
              </div>

              <svg :viewBox="`0 0 ${chartFrame.width} ${chartFrame.height}`" class="h-full w-full overflow-hidden">
              <g>
                <line
                  v-for="tick in axisTicks"
                  :key="`fullscreen-grid-${tick.y}`"
                  :x1="chartFrame.paddingLeft"
                  :x2="chartFrame.width - chartFrame.paddingRight"
                  :y1="tick.y"
                  :y2="tick.y"
                  stroke="rgba(240,246,252,0.08)"
                  stroke-dasharray="4 6"
                />
              </g>

              <g>
                <text
                  v-for="tick in axisTicks"
                  :key="`fullscreen-weight-${tick.y}`"
                  :x="chartFrame.paddingLeft - 12"
                  :y="tick.y + 4"
                  fill="rgba(240,246,252,0.62)"
                  font-size="11"
                  text-anchor="end"
                >
                  {{ tick.weightLabel }}
                </text>

                <text
                  v-for="tick in axisTicks"
                  :key="`fullscreen-reps-${tick.y}`"
                  :x="chartFrame.width - chartFrame.paddingRight + 12"
                  :y="tick.y + 4"
                  fill="rgba(240,246,252,0.62)"
                  font-size="11"
                  text-anchor="start"
                >
                  {{ tick.repLabel }}
                </text>
              </g>

              <g>
                <path :d="weightPath" fill="none" stroke="var(--green)" stroke-linecap="round" stroke-linejoin="round" stroke-width="3.5" />
                <path :d="repPath" fill="none" stroke="var(--blue)" stroke-linecap="round" stroke-linejoin="round" stroke-width="3.5" />
              </g>

              <g v-if="activeChartPoint">
                <line
                  :x1="activeChartPoint.x"
                  :x2="activeChartPoint.x"
                  :y1="chartFrame.paddingTop"
                  :y2="chartFrame.height - chartFrame.paddingBottom"
                  stroke="rgba(88,166,255,0.72)"
                  stroke-width="2"
                  stroke-dasharray="6 6"
                />
                <circle
                  :cx="activeChartPoint.x"
                  :cy="chartFrame.height - chartFrame.paddingBottom"
                  r="9"
                  fill="rgba(88,166,255,0.22)"
                  stroke="var(--blue)"
                  stroke-width="2"
                />
              </g>

              <g>
                <g v-for="point in chartPoints" :key="`fullscreen-weight-point-${point.isoDate}`">
                  <circle :cx="point.x" :cy="point.weightY" :r="activeChartPoint?.isoDate === point.isoDate ? 7.5 : 6" fill="var(--green)" />
                  <circle :cx="point.x" :cy="point.weightY" :r="activeChartPoint?.isoDate === point.isoDate ? 14 : 11" fill="rgba(57,211,83,0.12)" />
                </g>

                <g v-for="point in chartPoints" :key="`fullscreen-rep-point-${point.isoDate}`">
                  <circle :cx="point.x" :cy="point.repsY" :r="activeChartPoint?.isoDate === point.isoDate ? 7.5 : 6" fill="var(--blue)" />
                  <circle :cx="point.x" :cy="point.repsY" :r="activeChartPoint?.isoDate === point.isoDate ? 14 : 11" fill="rgba(88,166,255,0.12)" />
                </g>
              </g>

              <g>
                <text
                  v-for="point in chartPoints"
                  :key="`fullscreen-label-${point.isoDate}`"
                  :x="point.x"
                  :y="chartFrame.height - 10"
                  :fill="activeChartPoint?.isoDate === point.isoDate ? 'rgba(240,246,252,0.92)' : 'rgba(240,246,252,0.62)'"
                  font-size="11"
                  text-anchor="middle"
                  :font-weight="activeChartPoint?.isoDate === point.isoDate ? '700' : '500'"
                >
                  {{ point.axisLabel }}
                </text>
              </g>

              <rect
                :x="chartFrame.paddingLeft"
                :y="chartFrame.paddingTop"
                :width="plotWidth"
                :height="plotHeight"
                fill="transparent"
                class="cursor-ew-resize touch-none"
                @pointerdown="beginChartScrub"
                @pointermove="handleChartScrubMove"
                @pointerup="endChartScrub"
                @pointercancel="endChartScrub"
              />
              </svg>
            </div>
          </div>

          <div v-else class="flex flex-1 items-center justify-center rounded-[24px] border border-surface-outline bg-surface-soft px-5 py-10 text-center text-text-muted">
            No chart data in this date range.
          </div>
        </div>
        </div>
      </div>
    </div>
  </div>
</template>
