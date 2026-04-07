<script setup>
import PageHero from '../components/PageHero.vue'
import SectionCard from '../components/SectionCard.vue'
import { apiRoutes } from '../services/api'
import { ptZoneData } from '../data/mockData'
</script>

<template>
  <div class="flex flex-col gap-6 min-w-0">
    <PageHero
      title="PT Zone"
      description="Invite trainers, manage read-only access, and review PT comments from one place."
    />

    <div class="grid gap-5 grid-cols-[repeat(auto-fit,minmax(300px,1fr))] md:grid-cols-2">
      <SectionCard title="Invite a PT" subtitle="Member-side access sharing">
        <p class="muted-copy">{{ ptZoneData.inviteText }}</p>

        <div class="flex flex-wrap items-center justify-end gap-4">
          <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-gradient-to-b from-blue to-blue-strong text-bg" type="button">Create Invite Code</button>
          <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" type="button">Share Link</button>
        </div>
      </SectionCard>

      <SectionCard title="Backend routes" subtitle="PT monitoring endpoint map">
        <div class="api-note api-note--tall">
          <p><strong>POST</strong> {{ apiRoutes.pt.invite }}</p>
          <p><strong>POST</strong> {{ apiRoutes.pt.accept }}</p>
          <p><strong>GET</strong> {{ apiRoutes.pt.members }}</p>
          <p><strong>DELETE</strong> {{ apiRoutes.pt.revokeAccess(':accessId') }}</p>
          <p><strong>POST</strong> {{ apiRoutes.pt.addComment(':memberId', ':workoutId') }}</p>
        </div>
      </SectionCard>
    </div>

    <SectionCard title="Active access" subtitle="Current PT connections">
      <div class="flex flex-col gap-3">
        <article v-for="access in ptZoneData.activeAccess" :key="access.name" class="p-[18px] bg-surface-soft border border-surface-outline rounded-[28px] max-w-full shadow-custom">
          <div>
            <h3>{{ access.name }}</h3>
            <p>{{ access.meta }}</p>
            <p class="muted-copy">{{ access.note }}</p>
          </div>
          <div class="stack-actions">
            <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border border-surface-outline bg-surface-soft text-text" type="button">View profile</button>
            <button class="inline-flex items-center justify-center gap-2 min-h-[48px] px-[18px] rounded-[18px] font-bold cursor-pointer border-0 bg-[rgba(248,81,73,0.14)] text-danger" type="button">Revoke</button>
          </div>
        </article>
      </div>
    </SectionCard>

    <SectionCard title="Comment thread" subtitle="Example PT feedback history">
      <div class="flex flex-col gap-3">
        <article v-for="comment in ptZoneData.comments" :key="comment.title" class="p-[18px] bg-surface-soft border border-surface-outline rounded-[28px] max-w-full shadow-custom">
          <div>
            <h3>{{ comment.title }}</h3>
            <p>{{ comment.body }}</p>
          </div>
        </article>
      </div>
    </SectionCard>
  </div>
</template>
