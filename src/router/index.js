import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../pages/LoginPage.vue'
import DashboardPage from '../pages/DashboardPage.vue'
import ActiveWorkoutPage from '../pages/ActiveWorkoutPage.vue'
import WorkoutRecapPage from '../pages/WorkoutRecapPage.vue'
import ProgramsPage from '../pages/ProgramsPage.vue'
import ProgramDetailPage from '../pages/ProgramDetailPage.vue'
import SplitSelectorPage from '../pages/SplitSelectorPage.vue'
import HistoryPage from '../pages/HistoryPage.vue'
import ExerciseHistoryDetailPage from '../pages/ExerciseHistoryDetailPage.vue'
import HistoryWorkoutDetailPage from '../pages/HistoryWorkoutDetailPage.vue'
import PtZonePage from '../pages/PtZonePage.vue'
import NotFoundPage from '../pages/NotFoundPage.vue'

const routes = [
  { path: '/', redirect: '/login' },
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
    meta: { title: 'Login', layout: 'auth' },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardPage,
    meta: { title: 'Dashboard' },
  },
  {
    path: '/workout/active',
    name: 'active-workout',
    component: ActiveWorkoutPage,
    meta: { title: 'Active Workout' },
  },
  {
    path: '/workout/recap',
    name: 'workout-recap',
    component: WorkoutRecapPage,
    meta: { title: 'Workout Recap' },
  },
  {
    path: '/programs',
    name: 'programs',
    component: ProgramsPage,
    meta: { title: 'Programs' },
  },
  {
    path: '/programs/create',
    name: 'program-create',
    component: ProgramDetailPage,
    meta: { title: 'Create Program' },
  },
  {
    path: '/programs/:programId',
    name: 'program-detail',
    component: ProgramDetailPage,
    meta: { title: 'Program' },
  },
  {
    path: '/programs/split-selector',
    name: 'split-selector',
    component: SplitSelectorPage,
    meta: { title: 'Split Selector' },
  },
  {
    path: '/history',
    name: 'history',
    component: HistoryPage,
    meta: { title: 'History' },
  },
  {
    path: '/history/exercises/:exerciseName',
    name: 'exercise-history-detail',
    component: ExerciseHistoryDetailPage,
    meta: { title: 'Exercise History' },
  },
  {
    path: '/history/workout/:date',
    name: 'history-workout-detail',
    component: HistoryWorkoutDetailPage,
    meta: { title: 'Workout History Detail' },
  },
  {
    path: '/pt-zone',
    name: 'pt-zone',
    component: PtZonePage,
    meta: { title: 'PT Zone' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundPage,
    meta: { title: 'Page Not Found', layout: 'auth' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.afterEach((to) => {
  document.title = `Jimbor • ${to.meta.title ?? 'Gym Tracker'}`
})

export default router
