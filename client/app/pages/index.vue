<template>
  <div class="flex flex-col gap-4 max-w-md">
    <UButton color="primary">Primary Button</UButton>
    <UButton color="primary" variant="soft">Soft Button</UButton>
    <UButton color="primary" variant="outline">Outline Button</UButton>
    
    <UCard>
      <template #header>
        <p class="font-bold text-primary">Karta sarlavhasi</p>
      </template>
      Karta mazmuni
    </UCard>
  </div>
</template>