<template>
  <div class="min-h-screen flex items-center justify-center bg-white dark:bg-gray-950 px-4 transition-colors duration-200">
    <div class="w-full max-w-sm">

      <!-- Heading -->
      <h1 class="text-2xl font-semibold text-gray-900 dark:text-white mb-1">
        Create an account
      </h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-8">
        Enter your email or phone to get started.
      </p>

      <!-- Input -->
      <div class="mb-4">
        <label for="contact" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Email or Phone
        </label>
        <input
          id="contact"
          v-model="contact"
          type="text"
          placeholder="name@example.com"
          class="w-full px-4 py-2.5 text-sm text-gray-900 dark:text-white bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg outline-none focus:border-gray-400 dark:focus:border-gray-600 transition-colors placeholder-gray-400 dark:placeholder-gray-600"
          @input="validateInput"
        />
        <p
          v-if="validationMessage"
          :class="validationStatus === 'valid' ? 'text-green-600 dark:text-green-500' : 'text-red-500 dark:text-red-400'"
          class="mt-2 text-xs"
        >
          {{ validationMessage }}
        </p>
      </div>

      <!-- Button -->
      <button
        @click="handleSubmit"
        :disabled="!canSubmit"
        class="w-full py-2.5 px-4 bg-gray-900 dark:bg-white text-white dark:text-gray-900 text-sm font-medium rounded-lg transition-opacity disabled:opacity-40 disabled:cursor-not-allowed hover:enabled:opacity-80"
      >
        <span v-if="!isLoading">Continue</span>
        <span v-else class="flex items-center justify-center gap-2">
          <svg class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Processing...
        </span>
      </button>

      <!-- Divider -->
      <p class="text-center text-xs text-gray-400 dark:text-gray-600 mt-6">
        Already have an account?
        <NuxtLink to="/auth/login" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors">
          Sign in
        </NuxtLink>
      </p>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const contact = ref('')
const isLoading = ref(false)
const validationStatus = ref<'valid' | 'invalid' | null>(null)
const validationMessage = ref('')
const inputType = ref<'email' | 'phone'>('email')

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const phoneRegex = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/

const validateInput = () => {
  const value = contact.value.trim()
  if (!value) {
    validationStatus.value = null
    validationMessage.value = ''
    return
  }
  if (emailRegex.test(value)) {
    validationStatus.value = 'valid'
    validationMessage.value = 'Valid email address'
    inputType.value = 'email'
  } else if (phoneRegex.test(value.replace(/\s/g, ''))) {
    validationStatus.value = 'valid'
    validationMessage.value = 'Valid phone number'
    inputType.value = 'phone'
  } else {
    validationStatus.value = 'invalid'
    validationMessage.value = 'Please enter a valid email or phone number'
  }
}

const canSubmit = computed(() => validationStatus.value === 'valid' && !isLoading.value)

const handleSubmit = async () => {
  if (!canSubmit.value) return
  isLoading.value = true
  await new Promise(resolve => setTimeout(resolve, 1000))
  isLoading.value = false
}
</script>