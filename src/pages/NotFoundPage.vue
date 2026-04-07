<template>
  <div class="auth-page auth-page--centered">
    <section class="auth-page__form-card">
      <p class="text-text-muted text-[0.78rem] tracking-[0.12em] uppercase m-0">404</p>
      <h1 class="m-0 text-[1.25rem] font-extrabold">Page not found</h1>
      <p class="muted-copy">The route does not exist yet. Try returning to login or dashboard.</p>
      <div class="flex flex-wrap items-center justify-end gap-4">
        <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" to="/login">Login</RouterLink>
        <RouterLink class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" to="/dashboard">Dashboard</RouterLink>
      </div>
    </section>
  </div>
</template>
