<script setup>
defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: String,
    required: true,
  },
  note: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <article class="w-full max-w-full p-[18px] min-w-0 border border-surface-outline rounded-[28px] bg-gradient-to-b from-[rgba(22,27,34,0.98)] to-[rgba(15,20,27,0.98)] shadow-custom">
    <p class="m-0 text-text-muted text-[0.78rem] tracking-[0.12em] uppercase">{{ label }}</p>
    <p class="m-0 mt-2.5 text-[clamp(1.9rem,4vw,3rem)] font-black leading-none break-words">{{ value }}</p>
    <p v-if="note" class="m-0 mt-1 text-sm text-text-muted">{{ note }}</p>
  </article>
</template>
