<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <header class="flex flex-col gap-3">
    <div>
      <h1 class="m-0 text-[clamp(2.1rem,10vw,3rem)] leading-[0.94] font-black tracking-[0.04em] uppercase text-green">{{ title }}</h1>
      <p v-if="description" class="max-w-[72ch] m-0 mt-2 text-text-soft leading-[1.6]">{{ description }}</p>
    </div>
  </header>
</template>
