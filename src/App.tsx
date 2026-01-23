import { motion, AnimatePresence } from 'framer-motion';
import { Terminal, BookOpen, Code2, Play, CheckCircle2, ChevronRight, Search, Zap, Star, Layout, Database, Globe, Command, Shield } from 'lucide-react';
import { useState } from 'react';

const LESSONS = [
    { id: 1, title: "Data Structures", level: "Beginner", time: "45m", icon: <Database className="w-5 h-5" />, color: "bg-blue-500" },
    { id: 2, title: "Algorithm Efficiency", level: "Intermediate", time: "1h 20m", icon: <Zap className="w-5 h-5" />, color: "bg-amber-500" },
    { id: 3, title: "Web Frameworks", level: "Advanced", time: "2h 15m", icon: <Globe className="w-5 h-5" />, color: "bg-emerald-500" },
    { id: 4, title: "Security Protocols", level: "Advanced", time: "1h 10m", icon: <Shield className="w-5 h-5" />, color: "bg-red-500" }
];

const CODE_SNIPPS = [
    { title: "Binary Search", code: "def binary_search(arr, x):\n    low = 0\n    high = len(arr) - 1\n    while low <= high:\n        mid = (high + low) // 2\n        if arr[mid] < x:\n            low = mid + 1\n        elif arr[mid] > x:\n            high = mid - 1\n        else:\n            return mid\n    return -1" },
    { title: "Quick Sort", code: "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)" }
];

export default function App() {
    const [activeLesson, setActiveLesson] = useState(LESSONS[0]);
    const [searchTerm, setSearchTerm] = useState('');

    return (
        <div className="min-h-screen">
            {/* Sidebar Navigation */}
            <aside className="fixed left-0 top-0 bottom-0 w-80 bg-[#0f172a] border-r border-white/5 p-8 hidden lg:block z-50">
                <div className="flex items-center gap-3 mb-10 px-2">
                    <div className="p-2 bg-python/20 rounded-lg">
                        <Terminal className="w-6 h-6 text-python" />
                    </div>
                    <span className="text-xl font-black text-white uppercase tracking-tighter">Py<span className="text-python">Learn</span></span>
                </div>

                <div className="space-y-1 mb-10">
                    {['Dashboard', 'My Library', 'Practice Lab', 'Community', 'Settings'].map((nav) => (
                        <button key={nav} className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold transition-all ${nav === 'Dashboard' ? 'bg-python text-white shadow-lg shadow-python/20' : 'text-slate-500 hover:bg-white/5 hover:text-white'}`}>
                            {nav === 'Dashboard' ? <Layout className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                            {nav}
                        </button>
                    ))}
                </div>

                <div className="mt-auto pt-10 border-t border-white/5">
                    <div className="lesson-card p-6 bg-gradient-to-br from-python/20 to-transparent">
                        <Star className="w-8 h-8 text-python mb-4" />
                        <h4 className="text-white font-bold mb-2">Pro Membership</h4>
                        <p className="text-xs text-slate-400 mb-4 leading-relaxed">Get access to 500+ premium python projects and labs.</p>
                        <button className="w-full py-2 bg-python text-white rounded-lg text-xs font-black uppercase tracking-widest hover:brightness-110 transition-all">Upgrade Now</button>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="lg:ml-80 p-8 lg:p-12 min-h-screen bg-[#0a0f1d]">
                {/* Header */}
                <header className="flex flex-col md:flex-row md:items-center justify-between gap-8 mb-16">
                    <div>
                        <h1 className="text-3xl font-black text-white uppercase tracking-tight mb-2">Welcome Back, <span className="text-python">MK</span></h1>
                        <p className="text-slate-500 text-sm font-medium italic">You've completed 72% of your Python Path. Keep it up!</p>
                    </div>

                    <div className="flex items-center gap-4">
                        <div className="relative group">
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 group-focus-within:text-python transition-colors" />
                            <input
                                type="text"
                                placeholder="Search lessons..."
                                className="bg-white/5 border border-white/10 rounded-2xl pl-12 pr-6 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-python/50 focus:border-python/50 w-full md:w-64 transition-all"
                            />
                        </div>
                        <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-python to-blue-400 p-[2px]">
                            <div className="w-full h-full bg-[#0a0f1d] rounded-2xl flex items-center justify-center overflow-hidden">
                                <img src="https://api.uifaces.co/our-content/donated/vY_Hqdrp.jpg" alt="Profile" className="w-full h-full object-cover" />
                            </div>
                        </div>
                    </div>
                </header>

                <div className="grid lg:grid-cols-3 gap-12">
                    {/* Left Column: Lessons */}
                    <div className="lg:col-span-2 space-y-12">
                        {/* Featured Lesson */}
                        <section>
                            <div className="flex items-center justify-between mb-8">
                                <h2 className="text-xl font-bold text-white uppercase tracking-widest flex items-center gap-3">
                                    <Play className="w-5 h-5 text-python fill-python" /> Featured Practice
                                </h2>
                                <span className="text-xs font-bold text-slate-500 uppercase tracking-widest cursor-pointer hover:text-white transition-colors">View All</span>
                            </div>

                            <div className="grid md:grid-cols-2 gap-6">
                                {LESSONS.map((lesson) => (
                                    <motion.div
                                        key={lesson.id}
                                        whileHover={{ y: -5 }}
                                        className={`lesson-card cursor-pointer group ${activeLesson.id === lesson.id ? 'border-python bg-python/5' : ''}`}
                                        onClick={() => setActiveLesson(lesson)}
                                    >
                                        <div className="flex justify-between items-start mb-6">
                                            <div className={`p-3 rounded-2xl ${lesson.color} text-white shadow-lg`}>
                                                {lesson.icon}
                                            </div>
                                            <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">{lesson.level}</span>
                                        </div>
                                        <h3 className="text-lg font-black text-white uppercase tracking-tight mb-2 group-hover:text-python transition-colors">{lesson.title}</h3>
                                        <div className="flex items-center gap-4 text-xs font-bold text-slate-500 uppercase tracking-widest">
                                            <span className="flex items-center gap-1"><BookOpen className="w-3 h-3" /> {lesson.time}</span>
                                            <span className="flex items-center gap-1 text-emerald-500"><CheckCircle2 className="w-3 h-3" /> 12 Tests</span>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </section>

                        {/* Lab Section */}
                        <section>
                            <div className="flex items-center justify-between mb-8">
                                <h2 className="text-xl font-bold text-white uppercase tracking-widest flex items-center gap-3">
                                    <Command className="w-5 h-5 text-python" /> Script Output Lab
                                </h2>
                            </div>

                            <div className="space-y-6">
                                {CODE_SNIPPS.map((snippet, i) => (
                                    <div key={i} className="code-block group overflow-hidden">
                                        <div className="flex justify-between items-center mb-6">
                                            <span className="text-xs font-bold uppercase text-python tracking-widest">{snippet.title}.py</span>
                                            <button className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                                                <Play className="w-4 h-4 text-emerald-400 fill-emerald-400 group-hover:scale-110 transition-transform" />
                                            </button>
                                        </div>
                                        <pre className="text-emerald-400/90 leading-relaxed overflow-x-auto">
                                            <code>{snippet.code}</code>
                                        </pre>
                                    </div>
                                ))}
                            </div>
                        </section>
                    </div>

                    {/* Right Column: Progress */}
                    <div className="space-y-12">
                        <section>
                            <div className="flex items-center gap-3 mb-8">
                                <h2 className="text-xl font-bold text-white uppercase tracking-widest">MY PROGRESS</h2>
                            </div>

                            <div className="lesson-card space-y-8">
                                <div className="text-center relative py-10">
                                    <svg className="w-40 h-40 mx-auto transform -rotate-90">
                                        <circle cx="80" cy="80" r="70" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-white/5" />
                                        <circle
                                            cx="80" cy="80" r="70"
                                            stroke="currentColor" strokeWidth="8" fill="transparent"
                                            strokeDasharray={440}
                                            strokeDashoffset={440 - (440 * 0.72)}
                                            strokeLinecap="round"
                                            className="text-python"
                                        />
                                    </svg>
                                    <div className="absolute inset-0 flex flex-col items-center justify-center mt-4">
                                        <span className="text-4xl font-black text-white">72%</span>
                                        <span className="text-[10px] font-black uppercase text-slate-500 tracking-widest">Mastery</span>
                                    </div>
                                </div>

                                <div className="space-y-4">
                                    <div className="flex justify-between items-center text-xs font-bold uppercase tracking-widest">
                                        <span className="text-slate-300">Total Scripts</span>
                                        <span className="text-white">124</span>
                                    </div>
                                    <div className="flex justify-between items-center text-xs font-bold uppercase tracking-widest">
                                        <span className="text-slate-300">Tests Passed</span>
                                        <span className="text-emerald-400">856</span>
                                    </div>
                                    <div className="flex justify-between items-center text-xs font-bold uppercase tracking-widest">
                                        <span className="text-slate-300">Level</span>
                                        <span className="text-python">Senior</span>
                                    </div>
                                </div>
                            </div>
                        </section>

                        <section>
                            <div className="flex items-center gap-3 mb-8">
                                <h2 className="text-xl font-bold text-white uppercase tracking-widest">STREAK</h2>
                            </div>
                            <div className="lesson-card bg-python/10 border-python/20 flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="p-3 bg-python text-white rounded-xl shadow-lg">
                                        <Code2 className="w-6 h-6" />
                                    </div>
                                    <div>
                                        <div className="text-2xl font-black text-white uppercase leading-none">14 DAYS</div>
                                        <div className="text-[10px] font-bold text-python uppercase tracking-widest">Keep going!</div>
                                    </div>
                                </div>
                                <Star className="w-8 h-8 text-python animate-pulse" />
                            </div>
                        </section>
                    </div>
                </div>
            </main>

            {/* Footer (Mobile Friendly) */}
            <footer className="lg:ml-80 border-t border-white/5 p-8 text-center">
                <p className="text-[10px] font-bold text-slate-600 uppercase tracking-[0.4em]">© 2026 PYLEARN // ACADEMY • 24/30 DISPATCHED</p>
            </footer>
        </div>
    );
}
