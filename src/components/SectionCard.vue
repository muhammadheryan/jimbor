<script setup>
defineProps({
  title: {
    type: String,
    default: '',
  },
  subtitle: {
    type: String,
    default: '',
  },
  accent: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <section class="w-full max-w-full p-6 border border-surface-outline rounded-[28px] bg-gradient-to-b from-[rgba(22,27,34,0.98)] to-[rgba(15,20,27,0.98)] shadow-custom" :class="{ 'border-[rgba(88,166,255,0.18)]': accent === 'blue' }">
    <div v-if="title || subtitle" class="flex items-start justify-between gap-4 mb-[18px]">
      <div>
        <h2 v-if="title" class="m-0 text-xl font-extrabold">{{ title }}</h2>
        <p v-if="subtitle" class="m-0 mt-1.5 leading-[1.5] text-text-muted">{{ subtitle }}</p>
      </div>

      <slot name="header-actions" />
    </div>

    <slot />
  </section>
</template>
