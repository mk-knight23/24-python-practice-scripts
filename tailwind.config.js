/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                python: "#2563eb",
                dark: "#020617",
            },
        },
    },
    plugins: [],
}
