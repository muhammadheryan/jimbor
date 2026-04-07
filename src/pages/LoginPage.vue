<script setup>
import { RouterLink } from 'vue-router'
import { apiRoutes, API_BASE_URL } from '../services/api'
import { loginData } from '../data/mockData'
</script>

<template>
  <div class="grid items-center gap-6 min-h-screen p-6">
    <section class="w-full max-w-full p-6 border border-surface-outline rounded-[28px] bg-gradient-to-b from-[rgba(22,27,34,0.98)] to-[rgba(15,20,27,0.98)] shadow-custom">
      <p class="m-0 text-text-muted text-[0.78rem] tracking-[0.12em] uppercase">Gym tracker PWA</p>
      <h1 class="m-0 mt-2 font-black leading-[0.92] tracking-[0.04em] uppercase text-[clamp(3.4rem,10vw,5rem)]">JIMBOR</h1>
      <h2 class="m-0 mt-4 font-black leading-[0.92] tracking-[0.04em] uppercase text-[clamp(2.6rem,8vw,4.5rem)] max-w-[10ch]">{{ loginData.title }}</h2>
      <p class="max-w-[72ch] m-0 mt-4 text-text-soft leading-[1.6]">{{ loginData.description }}</p>
    </section>

    <section class="w-full max-w-full p-6 border border-surface-outline rounded-[28px] bg-gradient-to-b from-[rgba(22,27,34,0.98)] to-[rgba(15,20,27,0.98)] shadow-custom">
      <p class="m-0 text-text-muted text-[0.78rem] tracking-[0.12em] uppercase">Welcome back</p>
      <h2 class="m-0 mt-2 text-[1.25rem] font-extrabold">Login to your training log</h2>

      <form class="flex flex-col gap-4 mt-6" @submit.prevent>
        <label class="flex flex-col gap-2">
          <span class="text-text-muted text-[0.78rem] font-bold tracking-[0.08em] uppercase">Email</span>
          <input class="w-full px-[18px] py-4 border border-surface-outline rounded-[18px] bg-surface-soft text-text outline-none" type="email" placeholder="bro.jimbo@email.com" />
        </label>

        <label class="flex flex-col gap-2">
          <span class="text-text-muted text-[0.78rem] font-bold tracking-[0.08em] uppercase">Password</span>
          <input class="w-full px-[18px] py-4 border border-surface-outline rounded-[18px] bg-surface-soft text-text outline-none" type="password" placeholder="••••••••••••" />
        </label>

        <div class="flex items-center justify-between gap-4 mt-2">
          <label class="inline-flex items-center gap-2">
            <input class="accent-green" type="checkbox" checked />
            <span class="text-text-muted text-[0.8rem] font-bold">Keep me signed in</span>
          </label>

          <button type="button" class="p-0 bg-transparent text-blue font-bold cursor-pointer inline-flex items-center justify-center gap-2 border-0">Forgot?</button>
        </div>

        <RouterLink class="inline-flex items-center justify-center gap-2 w-full min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg text-center mt-2" to="/dashboard">Login</RouterLink>
      </form>

      <p class="mt-4 mb-0 text-text-muted text-center">No account yet? Create one</p>

      <div class="grid gap-2.5 mt-[18px] p-4 rounded-[18px] bg-[rgba(15,20,27,0.92)] text-text-muted text-sm break-words">
        <p class="m-0"><strong>Backend base URL:</strong> {{ API_BASE_URL }}</p>
        <p class="m-0"><strong>Login route:</strong> POST {{ apiRoutes.auth.login }}</p>
      </div>
    </section>
  </div>
</template>
