<template>
  <header class="sticky top-0 z-50 bg-white dark:bg-gray-950 border-b border-gray-100 dark:border-gray-900 transition-colors duration-200">
    <nav class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-14">

        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center gap-2.5">
          <div class="w-6 h-6 bg-gray-900 dark:bg-white rounded-md transition-colors duration-200"></div>
          <span class="text-sm font-semibold text-gray-900 dark:text-white hidden sm:inline">Fintech Wallet</span>
        </NuxtLink>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-6">
          <NuxtLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            {{ link.label }}
          </NuxtLink>
        </div>

        <!-- Right side -->
        <div class="flex items-center gap-3">

          <!-- Dark / Light toggle -->
          <button
            @click="toggleColorMode"
            class="p-1.5 rounded-lg text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-900 transition-colors duration-200"
            :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
          >
            <!-- Sun icon (shown in dark mode) -->
            <svg v-if="isDark" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M12 5a7 7 0 100 14A7 7 0 0012 5z" />
            </svg>
            <!-- Moon icon (shown in light mode) -->
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12.79A9 9 0 1111.21 3a7 7 0 009.79 9.79z" />
            </svg>
          </button>

          <!-- Auth (desktop) -->
          <div class="hidden md:flex items-center gap-3">
            <NuxtLink
              to="/auth/login"
              class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Login
            </NuxtLink>
            <NuxtLink
              to="/auth/register"
              class="text-sm font-medium px-3.5 py-1.5 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg hover:opacity-80 transition-opacity"
            >
              Sign Up
            </NuxtLink>
          </div>

          <!-- Mobile Menu Button -->
          <button
            @click="isMobileMenuOpen = !isMobileMenuOpen"
            class="md:hidden p-1.5 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            <svg v-if="!isMobileMenuOpen" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

        </div>
      </div>

      <!-- Mobile Menu -->
      <transition
        enter-active-class="transition-all duration-200 ease-out"
        leave-active-class="transition-all duration-150 ease-in"
        enter-from-class="opacity-0 -translate-y-2"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div v-if="isMobileMenuOpen" class="md:hidden py-4 border-t border-gray-100 dark:border-gray-900 flex flex-col gap-1">
          <NuxtLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            @click="isMobileMenuOpen = false"
            class="px-2 py-2 text-sm text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors rounded-lg"
          >
            {{ link.label }}
          </NuxtLink>

          <div class="border-t border-gray-100 dark:border-gray-900 mt-2 pt-3 flex flex-col gap-2">
            <NuxtLink
              to="/auth/login"
              @click="isMobileMenuOpen = false"
              class="px-2 py-2 text-sm text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Login
            </NuxtLink>
            <NuxtLink
              to="/auth/register"
              @click="isMobileMenuOpen = false"
              class="px-3.5 py-2 text-sm font-medium text-center bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg hover:opacity-80 transition-opacity"
            >
              Sign Up
            </NuxtLink>
          </div>
        </div>
      </transition>

    </nav>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// @nuxtjs/color-mode
const colorMode = useColorMode()

const isDark = computed(() => colorMode.value === 'dark')

const toggleColorMode = () => {
  colorMode.preference = isDark.value ? 'light' : 'dark'
}

const isMobileMenuOpen = ref(false)

const navLinks = [
  { to: '/features', label: 'Features' },
  { to: '/pricing', label: 'Pricing' },
  { to: '/about', label: 'About' },
]
</script>