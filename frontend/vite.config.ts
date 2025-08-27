import path from "path"
import frappeui from "frappe-ui/vite";
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    frappeui({
      frappeProxy: {
        port: 8080,
        source: "^/(app|login|api|assets|files|pages|builder_assets)",
      },
    }),
    {
      name: "inject-csrf-token",
      transformIndexHtml(html) {
        return html.replace(
          "</body>",
          `<script>window.csrf_token = '{{ frappe.session.csrf_token }}';</script></body>`
        );
      },
    },
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  build: {
    chunkSizeWarningLimit: 1500,
    outDir: `../urugano/public/frontend`,
    emptyOutDir: true,
    target: "es2015",
    sourcemap: true,
  },
});