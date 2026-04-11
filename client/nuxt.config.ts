// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ["@nuxt/ui"],
  compatibilityDate: "2025-07-15",
  colorMode: {
    classSuffix: "",
  },
  devtools: { enabled: true },
  css: ["./app/assets/css/main.css"],
});
