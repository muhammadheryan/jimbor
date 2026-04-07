export const loginData = {
  title: 'Progress you can see',
  description:
    'Start workouts in seconds, review your last sets instantly, and keep your consistency visible with the heatmap.',
}

export const dashboardData = {
  nextSplit: {
    name: 'PULL',
    program: 'Push Pull Legs',
    note: 'Last session: PUSH - yesterday, 19:24',
    lastSplit: 'PUSH',
    status: ['Push', 'Pull', 'Leg'],
  },
  stats: [
    { label: 'Streak', value: '3 weeks', note: 'Tracked consistently for 3 straight weeks' },
    { label: 'April', value: '18 session', note: '2 more than March' },
  ],
  heatmap: [
    [0, 1, 2, 3, 4, 0, 2, 3, 0, 4, 1, 0],
    [0, 0, 1, 2, 3, 4, 2, 1, 0, 3, 4, 0],
    [1, 2, 0, 4, 3, 0, 1, 2, 3, 0, 4, 1],
  ],
  recentWorkouts: [
    { title: 'Apr 4 - PUSH', meta: '18 sets - 8,420 kg volume', flag: 'Fresh' },
    { title: 'Apr 3 - PULL', meta: '16 sets - Bench and lats day', flag: 'Fresh' },
    { title: 'Apr 1 - LEG', meta: '14 sets - Lower energy but done', flag: 'Tired' },
  ],
}

export const activeWorkoutData = {
  session: {
    title: 'PUSH DAY',
    subtitle: 'Push Pull Legs - Active Workout',
    duration: '00:45:12',
    flag: 'Fresh',
    mode: 'Default',
  },
  queue: [
    {
      name: 'Bench Press',
      badge: '3 target sets',
      sets: [
        { number: 1, weight: '60 kg', reps: 10, notes: 'smooth' },
        { number: 2, weight: '60 kg', reps: 9, notes: 'focus' },
        { number: 3, weight: '60 kg', reps: 8, notes: 'tough' },
      ],
      history: [
        { date: 'Apr 1', summary: '3x10 @ 60kg', flag: 'Fresh' },
        { date: 'Mar 29', summary: '3x8 @ 57.5kg', flag: 'Fresh' },
        { date: 'Mar 26', summary: '3x10 @ 57.5kg', flag: 'Tired' },
        { date: 'Mar 24', summary: '3x10 @ 55kg', flag: 'Fresh' },
        { date: 'Mar 22', summary: '3x8 @ 55kg', flag: 'Beast' },
      ],
      helper: 'Dual input: scroll picker or tap to type',
    },
    {
      name: 'Incline DB Press',
      badge: 'new entry',
      sets: [
        { number: 1, weight: '24 kg', reps: 12, notes: 'easy' },
        { number: 2, weight: 'tap', reps: 'tap', notes: 'optional' },
      ],
      history: [],
      helper: 'History opens as soon as exercise is added',
    },
    {
      name: 'Shoulder Press',
      badge: '3 target sets',
      sets: [
        { number: 1, weight: '40 kg', reps: 10, notes: 'controlled' },
        { number: 2, weight: '40 kg', reps: 9, notes: 'hard' },
      ],
      history: [
        { date: 'Apr 1', summary: '3x8 @ 37.5kg', flag: 'Fresh' },
        { date: 'Mar 29', summary: '3x10 @ 35kg', flag: 'Fresh' },
      ],
      helper: 'Use the last warm-up as your reference set',
    },
    {
      name: 'Lateral Raise',
      badge: '4 target sets',
      sets: [
        { number: 1, weight: '10 kg', reps: 15, notes: 'strict' },
        { number: 2, weight: '10 kg', reps: 14, notes: 'burning' },
      ],
      history: [{ date: 'Apr 1', summary: '4x15 @ 8kg', flag: 'Fresh' }],
      helper: 'Keep the motion strict and controlled',
    },
    {
      name: 'Cable Fly',
      badge: '3 target sets',
      sets: [],
      history: [],
      helper: 'Add your first set when you reach this station',
    },
    {
      name: 'Tricep Pushdown',
      badge: '3 target sets',
      sets: [],
      history: [],
      helper: 'Save one rep in reserve for the first set',
    },
  ],
}

export const recapData = {
  date: 'April 5, 2026',
  duration: '1h 12m',
  flag: 'Fresh',
  summary: [
    { label: 'Total sets', value: '18' },
    { label: 'Total reps', value: '156' },
    { label: 'Volume', value: '8,420 kg' },
    { label: 'Heatmap score', value: 'Level 4' },
  ],
  prs: [
    { name: 'Bench Press', value: '65 x 8', note: 'Estimated one-rep max is trending up.' },
    { name: 'Overhead Press', value: '40 x 10', note: 'Beat your last top set by 2 reps.' },
  ],
}

export const programsData = {
  activeProgram: {
    name: 'Push Pull Legs',
    splits: 3,
    exercises: 18,
    nextSplit: 'PULL',
    note: 'Used 4x this week',
  },
  programs: [
    {
      name: 'Push Pull Legs',
      subtitle: 'PUSH - PULL - LEG',
      tags: ['18 exercises', 'Updated today'],
      status: 'Active',
      id: 'ppl',
    },
    {
      name: 'Upper Lower',
      subtitle: 'UPPER - LOWER',
      tags: ['12 exercises', 'Used last month'],
      status: 'Inactive',
      id: 'upper-lower',
    },
    {
      name: 'Full Body A/B',
      subtitle: 'DAY A - DAY B',
      tags: ['9 exercises', 'Needs review'],
      status: 'Draft',
      id: 'full-body-ab',
    },
  ],
}

export const programBuilderData = {
  name: 'Push Pull Legs',
  description:
    'Classic 3-day rotation focused on strength and hypertrophy with room for ad-hoc accessories.',
  stats: [
    { label: 'Splits', value: '3' },
    { label: 'Exercises', value: '8' },
    { label: 'Rotation', value: 'PPL' },
  ],
  splitDraft: {
    name: 'UPPER A',
    schedule: 'Mon / Thu',
    focus: 'Chest, back, shoulders',
  },
  splits: [
    {
      name: 'PUSH',
      note: 'Chest, shoulders, triceps',
      exercises: [
        { name: 'Bench Press', meta: '4 sets - 6-8 reps', rest: '120 sec', target: 'Top set first' },
        { name: 'Incline DB Press', meta: '3 sets - 8-10 reps', rest: '90 sec', target: 'Controlled eccentric' },
        { name: 'Shoulder Press', meta: '3 sets - 8-10 reps', rest: '90 sec', target: 'Leave 1 rep in reserve' },
      ],
    },
    {
      name: 'PULL',
      note: 'Lats, upper back, biceps',
      exercises: [
        { name: 'Lat Pulldown', meta: '4 sets - 8-10 reps', rest: '90 sec', target: 'Drive elbows down' },
        { name: 'Cable Row', meta: '3 sets - 10-12 reps', rest: '75 sec', target: 'Pause at contraction' },
      ],
    },
    {
      name: 'LEG',
      note: 'Quads, glutes, hamstrings',
      exercises: [
        { name: 'Hack Squat', meta: '4 sets - 8-10 reps', rest: '120 sec', target: 'Full depth' },
      ],
    },
  ],
}

export const splitSelectorData = {
  programName: 'Push Pull Legs',
  note: 'Completed splits are dimmed. The next recommended split is highlighted.',
  splits: [
    { name: 'PULL', description: '6 exercises - lats, rows, rear delts, biceps', status: 'Next' },
    { name: 'PUSH', description: '5 exercises - chest, shoulders, triceps', status: 'Done' },
    { name: 'LEG', description: '7 exercises - quads, hamstrings, glutes, calves', status: 'Pending' },
  ],
}

export const historyData = {
  overview: [
    { label: 'Sessions', value: '8' },
    { label: 'Streak', value: '12' },
    { label: 'Best lift', value: '65x8' },
  ],
  recentWorkouts: [
    { title: 'Apr 4 - PUSH', meta: '18 sets - 8,420 kg volume', flag: 'Fresh' },
    { title: 'Apr 3 - PULL', meta: '16 sets - upper back focus', flag: 'Fresh' },
    { title: 'Apr 1 - LEG', meta: '14 sets - lower energy', flag: 'Tired' },
    { title: 'Mar 29 - PUSH', meta: '17 sets - incline emphasis', flag: 'Fresh' },
  ],
  exerciseLibrary: [
    {
      name: 'Bench Press',
      summary: 'Top set 65 x 8',
      note: 'Progress is steady across the last 5 sessions.',
      chartLabels: ['55x8', '57.5x10', '60x10', '65x8'],
      sessions: [
        { date: 'Apr 4', detail: '3x10 @ 60kg', flag: 'Fresh' },
        { date: 'Apr 1', detail: '3x10 @ 60kg', flag: 'Fresh' },
        { date: 'Mar 29', detail: '3x8 @ 57.5kg', flag: 'Fresh' },
        { date: 'Mar 26', detail: '3x10 @ 57.5kg', flag: 'Tired' },
      ],
    },
    {
      name: 'Lat Pulldown',
      summary: 'Top set 72.5 x 10',
      note: 'Back volume is consistent, elbow path looks stable.',
      chartLabels: ['60x12', '65x12', '70x10', '72.5x10'],
      sessions: [
        { date: 'Apr 3', detail: '4x10 @ 72.5kg', flag: 'Fresh' },
        { date: 'Mar 30', detail: '4x10 @ 70kg', flag: 'Fresh' },
        { date: 'Mar 27', detail: '4x12 @ 65kg', flag: 'Fresh' },
      ],
    },
    {
      name: 'Hack Squat',
      summary: 'Top set 140 x 8',
      note: 'Leg day output dips a little when recovery is low.',
      chartLabels: ['120x10', '130x10', '135x8', '140x8'],
      sessions: [
        { date: 'Apr 1', detail: '4x8 @ 140kg', flag: 'Tired' },
        { date: 'Mar 28', detail: '4x8 @ 135kg', flag: 'Fresh' },
        { date: 'Mar 24', detail: '4x10 @ 130kg', flag: 'Fresh' },
      ],
    },
  ],
  chartLabels: ['55x8', '57.5x10', '60x10', '65x8'],
  heatmap: [
    [0, 1, 2, 3, 4, 0, 2, 3, 0, 4, 1, 0],
    [0, 0, 1, 2, 3, 4, 2, 1, 0, 3, 4, 1],
    [1, 2, 0, 4, 3, 0, 1, 2, 3, 0, 4, 1],
    [0, 1, 2, 3, 4, 0, 2, 3, 0, 4, 1, 0],
  ],
}

export const exerciseLibraryList = [
  'Bench Press',
  'Incline DB Press',
  'Cable Fly',
  'Chest Dip',
  'Pec Deck',
  'Lat Pulldown',
  'Cable Row',
  'Face Pull',
  'Barbell Row',
  'Chest-Supported Row',
  'Hack Squat',
  'Romanian Deadlift',
  'Leg Press',
  'Leg Curl',
  'Leg Extension',
  'Walking Lunge',
  'Shoulder Press',
  'Lateral Raise',
  'Rear Delt Fly',
  'Upright Row',
  'Tricep Pushdown',
  'Skull Crusher',
  'Overhead Tricep Extension',
  'Bicep Curl',
  'Hammer Curl',
  'Preacher Curl',
  'Calf Raise',
  'Plank',
  'Cable Crunch',
]

export const ptZoneData = {
  inviteText:
    'Generate a 48-hour invite code so your trainer can view your workout history, heatmap, and progress.',
  activeAccess: [
    {
      name: 'Coach Andi',
      meta: 'Read-only access - 31 workouts viewed',
      note: 'Bench tempo looked more stable this week.',
    },
  ],
  comments: [
    { title: 'Apr 4 - Coach Andi', body: 'Bench lockout looked cleaner. Keep this pacing next week.' },
    { title: 'Apr 1 - Coach Andi', body: 'Great consistency finishing leg day even on a low-energy day.' },
    { title: 'Mar 29 - Coach Andi', body: 'Pull volume is trending well. Watch elbow fatigue.' },
  ],
}
