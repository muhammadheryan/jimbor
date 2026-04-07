/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                bg: 'var(--bg)',
                'bg-elevated': 'var(--bg-elevated)',
                surface: 'var(--surface)',
                'surface-soft': 'var(--surface-soft)',
                'surface-outline': 'var(--surface-outline)',
                'text': 'var(--text)',
                'text-muted': 'var(--text-muted)',
                'text-soft': 'var(--text-soft)',
                blue: 'var(--blue)',
                'blue-strong': 'var(--blue-strong)',
                green: 'var(--green)',
                'green-strong': 'var(--green-strong)',
                yellow: 'var(--yellow)',
                danger: 'var(--danger)',
            },
            boxShadow: {
                custom: 'var(--shadow)',
            },
            borderRadius: {
                xl: 'var(--radius-xl)',
                lg: 'var(--radius-lg)',
                md: 'var(--radius-md)',
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
