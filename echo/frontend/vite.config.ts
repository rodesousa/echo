import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { lingui } from "@lingui/vite-plugin";

const ReactCompilerConfig = {};

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: ["macros", ["babel-plugin-react-compiler"]],
      },
    }),
    lingui(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      // reddit fix lol: https://www.reddit.com/r/reactjs/comments/1g3tsiy/trouble_with_vite_tablericons_5600_requests/
      "@tabler/icons-react": "@tabler/icons-react/dist/esm/icons/index.mjs",
    },
  },
  build: {
    // Disable source maps in production for security and size
    sourcemap: false,

    // Set chunk size warning limit
    chunkSizeWarningLimit: 1000,

    // Optimize minification
    minify: "esbuild",

    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom", "react-router"],
          ui: ["@mantine/core", "@mantine/hooks"],
          // Split large libraries into separate chunks
          pdf: ["react-pdf", "@react-pdf/renderer"],
          markdown: ["react-markdown", "remark-gfm", "rehype-stringify"],
        },
      },
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000/",
        changeOrigin: true,
        rewrite: (path) => {
          console.log("Proxying request to", path);
          return path;
        },
      },
      "/directus": {
        target: "http://localhost:8055",
        changeOrigin: true,
        rewrite: (path) => {
          const newPath = path.replace(/^\/directus/, "/");
          console.log("Proxying request to", newPath);
          return newPath;
        },
      },
    },
  },
});
