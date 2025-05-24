import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "dist", // where Chrome expects files
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: "src/main.jsx" // entry point
      },
      output: {
        entryFileNames: "assets/index.js" // fixed name for manifest.json
      }
    }
  }
});
