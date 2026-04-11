// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ["@nuxt/ui", "@nuxtjs/color-mode"],
  compatibilityDate: "2025-07-15",
  colorMode: {
    classSuffix: "",
  },
  devtools: { enabled: true },
  css: ["./app/assets/css/main.css"],
});
