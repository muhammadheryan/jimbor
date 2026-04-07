<script setup>
import { computed, ref, watch } from 'vue'
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
  height: 320,
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

const latestSession = computed(() => filteredChartSessions.value.at(-1) ?? null)
const bestWeight = computed(() =>
  filteredChartSessions.value.length ? Math.max(...filteredChartSessions.value.map((session) => session.weight)) : 0,
)
const averageSets = computed(() => {
  if (!filteredChartSessions.value.length) {
    return 0
  }

  const totalSets = filteredChartSessions.value.reduce((sum, session) => sum + session.sets, 0)
  return totalSets / filteredChartSessions.value.length
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
const setDomain = computed(() => buildDomain(filteredChartSessions.value.map((session) => session.sets), 0.4))

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
      setsY: projectY(session.sets, setDomain.value),
    }
  }),
)

const buildLinePath = (points, key) =>
  points.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x} ${point[key]}`).join(' ')

const weightPath = computed(() => buildLinePath(chartPoints.value, 'weightY'))
const setPath = computed(() => buildLinePath(chartPoints.value, 'setsY'))

const axisTicks = computed(() =>
  Array.from({ length: 4 }, (_, index) => {
    const ratio = index / 3
    const y = chartFrame.paddingTop + ratio * plotHeight
    const weightValue = weightDomain.value.max - ratio * (weightDomain.value.max - weightDomain.value.min)
    const setValue = setDomain.value.max - ratio * (setDomain.value.max - setDomain.value.min)

    return {
      y,
      weightLabel: `${weightValue.toFixed(weightValue >= 100 ? 0 : 1).replace(/\.0$/, '')} kg`,
      setLabel: `${setValue.toFixed(setValue >= 10 ? 0 : 1).replace(/\.0$/, '')} sets`,
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
        <p class="m-0 text-[0.78rem] uppercase tracking-[0.12em] text-text-muted">Average Sets</p>
        <h2 class="m-0 mt-2 text-[2rem] font-black text-text">{{ averageSets ? averageSets.toFixed(1) : '-' }}</h2>
        <p class="m-0 mt-2 text-text-muted">Average number of sets across the selected sessions.</p>
      </article>
    </div> -->

    <SectionCard title="Progress Chart" subtitle="Weight and sets by training date.">
      <div class="flex flex-col gap-5">
        <div class="flex flex-col gap-2">
          <div class="flex flex-col gap-2">
            <p class="m-0 text-text-soft">{{ rangeSummary }}</p>
          </div>
        </div>

        <div v-if="chartPoints.length" class="rounded-[28px] border border-surface-outline bg-[linear-gradient(180deg,rgba(88,166,255,0.08)_0%,rgba(15,20,27,0.96)_100%)] p-4 md:p-5">
          <div class="mb-4 flex flex-wrap items-center gap-4">
            <div class="inline-flex items-center gap-2 text-sm text-text-soft">
              <span class="h-3 w-3 rounded-full bg-green"></span>
              Weight
            </div>
            <div class="inline-flex items-center gap-2 text-sm text-text-soft">
              <span class="h-3 w-3 rounded-full bg-blue"></span>
              Sets
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
                :key="`sets-${tick.y}`"
                :x="chartFrame.width - chartFrame.paddingRight + 12"
                :y="tick.y + 4"
                fill="rgba(240,246,252,0.62)"
                font-size="11"
                text-anchor="start"
              >
                {{ tick.setLabel }}
              </text>
            </g>

            <g>
              <path :d="weightPath" fill="none" stroke="var(--green)" stroke-linecap="round" stroke-linejoin="round" stroke-width="3.5" />
              <path :d="setPath" fill="none" stroke="var(--blue)" stroke-linecap="round" stroke-linejoin="round" stroke-width="3.5" />
            </g>

            <g>
              <g v-for="point in chartPoints" :key="`weight-point-${point.isoDate}`">
                <circle :cx="point.x" :cy="point.weightY" r="6" fill="var(--green)" />
                <circle :cx="point.x" :cy="point.weightY" r="11" fill="rgba(57,211,83,0.12)" />
              </g>

              <g v-for="point in chartPoints" :key="`set-point-${point.isoDate}`">
                <circle :cx="point.x" :cy="point.setsY" r="6" fill="var(--blue)" />
                <circle :cx="point.x" :cy="point.setsY" r="11" fill="rgba(88,166,255,0.12)" />
              </g>
            </g>

            <g>
              <text
                v-for="point in chartPoints"
                :key="`label-${point.isoDate}`"
                :x="point.x"
                :y="chartFrame.height - 10"
                fill="rgba(240,246,252,0.62)"
                font-size="11"
                text-anchor="middle"
              >
                {{ point.axisLabel }}
              </text>
            </g>
          </svg>
        </div>

        <div v-else class="rounded-[24px] border border-surface-outline bg-surface-soft px-5 py-10 text-center text-text-muted">
          No chart data in this date range.
        </div>
      </div>
    </SectionCard>

    <SectionCard title="Session History" subtitle="Date, weight, and sets for the selected range.">
      <div v-if="filteredSessionHistory.length" class="flex flex-col gap-4">
        <div class="overflow-hidden rounded-[24px] border border-surface-outline bg-surface-soft">
          <div class="overflow-x-auto">
            <table class="min-w-full border-collapse">
              <thead>
                <tr class="border-b border-surface-outline bg-[rgba(255,255,255,0.03)] text-left">
                  <th class="px-4 py-3 text-[0.78rem] font-bold uppercase tracking-[0.12em] text-text-muted">Date</th>
                  <th class="px-4 py-3 text-[0.78rem] font-bold uppercase tracking-[0.12em] text-text-muted">Weight</th>
                  <th class="px-4 py-3 text-[0.78rem] font-bold uppercase tracking-[0.12em] text-text-muted">Sets</th>
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
                  <td class="px-4 py-4 text-sm text-text-soft">{{ session.sets }}</td>
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
                <p class="m-0 text-[0.75rem] uppercase tracking-[0.1em] text-text-muted">Sets</p>
                <p class="m-0 mt-2 text-lg font-bold text-text">{{ selectedSessionDetail.sets }}</p>
              </div>
            </div>
          </article>
        </div>
      </section>
    </div>
  </div>
</template>
