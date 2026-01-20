/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                python: "#3776ab",
                dark: "#1e1e1e",
            },
        },
    },
    plugins: [],
}
