const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api'

async function request(path, options = {}) {
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  }

  if (config.body && typeof config.body !== 'string') {
    config.body = JSON.stringify(config.body)
  }

  const response = await fetch(`${API_BASE_URL}${path}`, config)

  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || 'Request failed')
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

export const apiRoutes = {
  auth: {
    login: '/auth/login',
    register: '/auth/register',
    refresh: '/auth/refresh',
    me: '/auth/me',
  },
  programs: {
    list: '/programs',
    create: '/programs',
    detail: (programId) => `/programs/${programId}`,
    update: (programId) => `/programs/${programId}`,
    remove: (programId) => `/programs/${programId}`,
    addDay: (programId) => `/programs/${programId}/days`,
    updateDay: (programId, dayId) => `/programs/${programId}/days/${dayId}`,
    removeDay: (programId, dayId) => `/programs/${programId}/days/${dayId}`,
    addExercise: (programId, dayId) => `/programs/${programId}/days/${dayId}/exercises`,
    updateExercise: (programId, dayId, exerciseId) =>
      `/programs/${programId}/days/${dayId}/exercises/${exerciseId}`,
    removeExercise: (programId, dayId, exerciseId) =>
      `/programs/${programId}/days/${dayId}/exercises/${exerciseId}`,
    reorderExercises: (programId, dayId) =>
      `/programs/${programId}/days/${dayId}/exercises/reorder`,
    rotationStatus: (programId) => `/programs/${programId}/rotation-status`,
  },
  workouts: {
    list: '/workouts',
    create: '/workouts',
    update: (workoutId) => `/workouts/${workoutId}`,
    remove: (workoutId) => `/workouts/${workoutId}`,
    addSet: (workoutId) => `/workouts/${workoutId}/sets`,
    updateSet: (workoutId, setId) => `/workouts/${workoutId}/sets/${setId}`,
    removeSet: (workoutId, setId) => `/workouts/${workoutId}/sets/${setId}`,
  },
  history: {
    exercise: (exerciseName) => `/history/exercise/${encodeURIComponent(exerciseName)}`,
    chart: (exerciseName) => `/history/exercise/${encodeURIComponent(exerciseName)}/chart`,
    heatmap: '/history/heatmap',
    stats: '/history/stats',
  },
  pt: {
    invite: '/pt/invite',
    accept: '/pt/accept',
    members: '/pt/members',
    memberWorkouts: (memberId) => `/pt/members/${memberId}/workouts`,
    memberHeatmap: (memberId) => `/pt/members/${memberId}/heatmap`,
    revokeAccess: (accessId) => `/pt/access/${accessId}`,
    addComment: (memberId, workoutId) => `/pt/members/${memberId}/workouts/${workoutId}/comments`,
  },
}

export const api = {
  get: (path) => request(path),
  post: (path, body) => request(path, { method: 'POST', body }),
  put: (path, body) => request(path, { method: 'PUT', body }),
  patch: (path, body) => request(path, { method: 'PATCH', body }),
  delete: (path) => request(path, { method: 'DELETE' }),
}

export { API_BASE_URL }
