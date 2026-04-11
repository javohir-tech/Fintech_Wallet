<script setup>
const colorMode = useColorMode()
const appConfig = useAppConfig()

const colors = [
  { label: 'Ko\'k', value: 'blue', class: 'bg-blue-500' },
  { label: 'Binafsha', value: 'violet', class: 'bg-violet-500' },
  { label: 'Yashil', value: 'green', class: 'bg-green-500' },
  { label: 'Qizil', value: 'red', class: 'bg-red-500' },
  { label: 'To\'q sariq', value: 'orange', class: 'bg-orange-500' },
  { label: "oq", value: "neutral", class : "bg-black dark:bg-white"}
]

const activeColor = ref('blue')

function setColor(color) {
  activeColor.value = color.value
  appConfig.ui.colors.primary = color.value
}

function toggleDark() {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark'
}
</script>

<template>
  <header
    class="flex items-center justify-between px-6 py-3 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">

    <!-- Logo -->
    <div class="text-lg font-bold text-primary">FintechWallet</div>

    <!-- O'rta: Rang tanlash -->
    <div class="flex items-center gap-2">
      <span class="text-sm text-gray-500 dark:text-gray-400 mr-1">Rang:</span>
      <button v-for="color in colors" :key="color.value" :title="color.label" :class="[
        color.class,
        'w-6 h-6 rounded-full transition-all duration-200',
        activeColor === color.value
          ? 'ring-2 ring-offset-2 ring-gray-400 scale-110'
          : 'opacity-70 hover:opacity-100'
      ]" @click="setColor(color)" />
    </div>

    <!-- O'ng: Dark/Light toggle -->
    <UButton variant="ghost" color="neutral" :icon="colorMode.value === 'dark'
      ? 'i-heroicons-sun-20-solid'
      : 'i-heroicons-moon-20-solid'" @click="toggleDark" />

  </header>
</template>