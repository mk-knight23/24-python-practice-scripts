# Python Practice

A terminal-based system for learning Python. Now with a web dashboard, progress tracking, quizzes, and achievements.

**Live Demo**: [GitHub Pages](https://mk-knight23.github.io/24-python-practice-scripts/)

---

## Tech Stack

- **Language**: Python 3.10+
- **CLI**: Pure Python (no dependencies)
- **Database**: SQLite (stdlib)
- **Web Dashboard**: HTML/CSS/JS with Tailwind CDN
- **Charts**: Chart.js
- **Deployment**: GitHub Pages, Vercel

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLI Interface Layer                           │
│  Python CLI + Text-based Menu System + Input/Output           │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                          │
│  Exercise Runner + Quiz System + Achievement Engine            │
│  + Analytics + Settings Management                             │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Data Layer                                 │
│  SQLite Database + JSON Export/Import + Profile Management     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Web Dashboard Layer                          │
│  HTML/CSS/JS + Tailwind CDN + Chart.js + LocalStorage          │
└─────────────────────────────────────────────────────────────────┘
```

### Project Structure

```
57-learn-python-practice/
├── skills/                      # Python exercises by difficulty
│   ├── basics/                  # 6 fundamental exercises
│   │   ├── 001_hello.py         # Hello World & print
│   │   ├── 002_variables.py     # Variables & types
│   │   ├── 003_conditionals.py # If statements
│   │   ├── 004_loops.py         # For & while loops
│   │   ├── 005_lists.py         # List operations
│   │   └── 006_functions.py     # Function basics
│   ├── core/                    # 5 intermediate exercises
│   │   ├── 001_dict.py          # Dictionaries
│   │   ├── 002_files.py         # File handling
│   │   ├── 003_errors.py        # Exception handling
│   │   ├── 004_classes.py       # OOP basics
│   │   └── 005_modules.py       # Import & modules
│   └── advanced/                # 4 advanced exercises
│       ├── 001_inheritance.py   # Class inheritance
│       ├── 002_decorators.py    # Function decorators
│       ├── 003_generators.py    # Generators & yield
│       └── 004_context.py       # Context managers
│
├── cli/                         # CLI application
│   ├── runner.py                # Main menu & navigation
│   ├── utils.py                 # Terminal helpers & UI
│   ├── progress.py              # Progress tracking (legacy JSON)
│   ├── database.py              # SQLite database layer
│   ├── quiz.py                  # Quiz system engine
│   ├── achievements.py          # Achievement tracking
│   ├── settings.py              # User settings & preferences
│   └── analytics.py             # Progress analytics & insights
│
├── viewer/                      # Browser-based code viewer
│   └── index.html               # Exercise reference viewer
│
├── dashboard.html               # Main web dashboard
│
├── design-system/               # Design guidelines
│   └── MASTER.md                # Design system rules
│
├── tests/                       # Test files
│   └── test_*.py                # Exercise tests
│
├── .github/workflows/
│   ├── ci.yml                   # CI workflow
│   └── deploy.yml               # GitHub Pages deployment
│
├── package.json                 # NPM scripts
├── vercel.json                  # Vercel configuration
├── netlify.toml                 # Netlify configuration
├── requirements.txt             # Python dependencies (none)
└── README.md                    # This file
```

### CLI Architecture

```typescript
{
  cli: {
    approach: "Text-based menu system",
    implementation: "Pure Python with no external dependencies",
    features: [
      "Number-based navigation",
      "Single-key shortcuts",
      "Blinking cursor (█) for terminal feel",
      "Plain text output (no syntax highlighting)",
      "Color-coded responses",
      "Input validation",
      "Help system"
    ],
    modules: {
      runner: {
        purpose: "Main menu and navigation",
        features: [
          "Display menu options",
          "Handle user input",
          "Navigate between sections",
          "Execute exercises",
          "Exit handling"
        ]
      },
      utils: {
        purpose: "Terminal helpers and UI utilities",
        features: [
          "Text formatting",
          "Clear screen",
          "Pause/continue",
          "Input validation",
          "Error display"
        ]
      }
    }
  }
}
```

### Database Architecture

```typescript
{
  database: {
    type: "SQLite (Python stdlib)",
    file: "progress.db",
    schema: {
      profiles: {
        table: "profiles",
        fields: [
          "id (INTEGER PRIMARY KEY)",
          "name (TEXT UNIQUE)",
          "difficulty (TEXT)",
          "theme (TEXT)",
          "daily_goal (INTEGER)",
          "created_at (TIMESTAMP)"
        ]
      },
      progress: {
        table: "progress",
        fields: [
          "id (INTEGER PRIMARY KEY)",
          "profile_id (INTEGER)",
          "exercise_path (TEXT)",
          "completed (BOOLEAN)",
          "attempts (INTEGER)",
          "time_spent (INTEGER)",
          "last_attempt (TIMESTAMP)",
          "FOREIGN KEY (profile_id) REFERENCES profiles(id)"
        ]
      },
      quiz_scores: {
        table: "quiz_scores",
        fields: [
          "id (INTEGER PRIMARY KEY)",
          "profile_id (INTEGER)",
          "category (TEXT)",
          "score (INTEGER)",
          "total (INTEGER)",
          "wrong_answers (JSON)",
          "timestamp (TIMESTAMP)",
          "FOREIGN KEY (profile_id) REFERENCES profiles(id)"
        ]
      },
      achievements: {
        table: "achievements",
        fields: [
          "id (INTEGER PRIMARY KEY)",
          "profile_id (INTEGER)",
          "achievement_id (TEXT)",
          "unlocked_at (TIMESTAMP)",
          "FOREIGN KEY (profile_id) REFERENCES profiles(id)"
        ]
      }
    },
    features: [
      "Automatic schema creation",
      "Data migration from JSON",
      "Profile switching",
      "Export to JSON",
      "Import from JSON",
      "Backup/restore",
      "Time tracking"
    ],
    operations: {
      create: "Create new user profile",
      switch: "Switch between profiles",
      save: "Save progress to database",
      load: "Load progress from database",
      export: "Export profile data as JSON",
      import: "Import profile data from JSON",
      reset: "Reset profile progress"
    }
  }
}
```

### Quiz System Architecture

```typescript
{
  quiz: {
    implementation: "Interactive quiz engine",
    categories: [
      "basics",
      "core",
      "advanced"
    ],
    features: [
      "Multiple choice questions",
      "Difficulty levels",
      "Score tracking",
      "Wrong answer review",
      "Explanations",
      "History log",
      "Category filtering"
    ],
    questionStructure: {
      question: "string",
      options: "string[] (4 choices)",
      correctAnswer: "number (0-3)",
      explanation: "string",
      category: "string",
      difficulty: "string"
    },
    scoring: {
      correct: "+1 point",
      incorrect: "0 points",
      display: "X/Y format (e.g., 8/10)",
      percentage: "Calculated from score/total"
    },
    workflow: "Select category → Answer questions → View results → Review wrong answers → Save score"
  }
}
```

### Achievement System Architecture

```typescript
{
  achievements: {
    implementation: "Badge and milestone tracking",
    types: [
      {
        type: "completion",
        examples: [
          "First Exercise Complete",
          "Basics Mastered",
          "Core Mastered",
          "Advanced Mastered",
          "All Complete"
        ]
      },
      {
        type: "streak",
        examples: [
          "3-Day Streak",
          "7-Day Streak",
          "30-Day Streak"
        ]
      },
      {
        type: "time",
        examples: [
          "1 Hour of Learning",
          "10 Hours of Learning",
          "100 Hours of Learning"
        ]
      },
      {
        type: "quiz",
        examples: [
          "Quiz Beginner",
          "Quiz Expert",
          "Perfect Score"
        ]
      }
    ],
    features: [
      "Auto-unlock on conditions met",
      "Progress indicators",
      "Achievement gallery",
      "Unlock timestamps",
      "Shareable export"
    ],
    dataStructure: {
      id: "string (unique identifier)",
      name: "string (display name)",
      description: "string",
      icon: "string (emoji or ASCII)",
      category: "string (completion, streak, time, quiz)",
      condition: "function (checks if achieved)",
      requirements: "object (specific requirements)"
    }
  }
}
```

### Analytics Architecture

```typescript
{
  analytics: {
    implementation: "Progress analytics and insights",
    metrics: [
      "Total exercises completed",
      "Exercises by category",
      "Time spent learning",
      "Average attempts per exercise",
      "Quiz scores",
      "Learning streaks",
      "Category progress percentages"
    ],
    features: [
      "Visual charts (Chart.js)",
      "Time-based analysis",
      "Streak tracking",
      "Category breakdown",
      "Progress trends",
      "Exportable data"
    ],
    charts: [
      {
        type: "bar",
        data: "Exercises by category",
        x: "Category",
        y: "Count"
      },
      {
        type: "line",
        data: "Learning over time",
        x: "Date",
        y: "Exercises completed"
      },
      {
        type: "doughnut",
        data: "Category completion",
        segments: "Basics, Core, Advanced"
      },
      {
        type: "line",
        data: "Quiz scores",
        x: "Attempt",
        y: "Score"
      }
    ]
  }
}
```

### Settings Architecture

```typescript
{
  settings: {
    implementation: "User preferences management",
    options: [
      {
        name: "difficulty",
        type: "enum",
        values: ["easy", "medium", "hard"],
        default: "medium"
      },
      {
        name: "theme",
        type: "enum",
        values: ["light", "dark"],
        default: "dark"
      },
      {
        name: "daily_goal",
        type: "integer",
        default: 3,
        description: "Exercises per day"
      },
      {
        name: "sound_enabled",
        type: "boolean",
        default: true
      },
      {
        name: "show_tips",
        type: "boolean",
        default: true
      }
    ],
    features: [
      "Per-profile settings",
      "Real-time application",
      "Export with profile data",
      "Reset to defaults"
    ]
  }
}
```

### Web Dashboard Architecture

```typescript
{
  webDashboard: {
    type: "Single-page HTML application",
    technologies: [
      "HTML5",
      "CSS3",
      "JavaScript (Vanilla)",
      "Tailwind CSS (CDN)",
      "Chart.js (CDN)",
      "LocalStorage"
    ],
    sections: [
      {
        name: "Overview",
        features: [
          "Total progress",
          "Current streak",
          "Recent achievements",
          "Quick stats"
        ]
      },
      {
        name: "Exercises",
        features: [
          "Exercise list by category",
          "Status indicators",
          "Filter by category",
          "Search exercises",
          "Mark as complete"
        ]
      },
      {
        name: "Quiz",
        features: [
          "Select category",
          "Interactive quiz",
          "Score display",
          "Wrong answer review",
          "Quiz history"
        ]
      },
      {
        name: "Achievements",
        features: [
          "Achievement gallery",
          "Unlock status",
          "Progress indicators",
          "Earn dates"
        ]
      },
      {
        name: "Analytics",
        features: [
          "Visual charts",
          "Progress trends",
          "Time analysis",
          "Category breakdown"
        ]
      },
      {
        name: "Settings",
        features: [
          "Profile selection",
          "Theme toggle",
          "Difficulty setting",
          "Daily goal",
          "Export/Import data"
        ]
      }
    ],
    dataFlow: {
      input: "User interaction",
      process: "JavaScript logic",
      storage: "LocalStorage",
      sync: "SQLite database (via import/export)"
    }
  }
}
```

### Exercise Architecture

```typescript
{
  exercises: {
    structure: "Standalone .py files",
    naming: "XXX_name.py (3-digit prefix)",
    format: {
      header: "# Purpose: [what this does]",
      example: "# Example: [output example]",
      why: "# Why: [human explanation]",
      code: "# -- actual code below --",
      tests: "if __name__ == '__main__': # test cases"
    },
    categories: [
      {
        name: "basics",
        count: 6,
        topics: [
          "Hello World & print",
          "Variables & types",
          "If statements",
          "Loops",
          "Lists",
          "Functions"
        ],
        difficulty: "Beginner"
      },
      {
        name: "core",
        count: 5,
        topics: [
          "Dictionaries",
          "File handling",
          "Exception handling",
          "Classes",
          "Modules"
        ],
        difficulty: "Intermediate"
      },
      {
        name: "advanced",
        count: 4,
        topics: [
          "Inheritance",
          "Decorators",
          "Generators",
          "Context managers"
        ],
        difficulty: "Advanced"
      }
    ],
    features: [
      "Standalone execution",
      "Self-documenting",
      "Practical examples",
      "Test cases included",
      "No external dependencies",
      "Editable and modifiable"
    ]
  }
}
```

### Data Flow Architecture

```
CLI Interface → User Input → Business Logic
     ↓              ↓              ↓
   Display       Validate      Process Request
     ↓              ↓              ↓
   Menu          Execute         Query/Write
     ↓              ↓              ↓
 Navigation      Exercise      SQLite Database
     ↓              ↓              ↓
  Next/Prev       Output         Results
     ↓              ↓              ↓
   Update          Display       Return
     ↓              ↓              ↓
  Profile          CLI          Continue
```

### Design System Architecture

```typescript
{
  designSystem: {
    philosophy: "Honest, accessible, practical",
    principles: [
      "No frameworks",
      "No external dependencies",
      "Plain text over syntax highlighting",
      "Editable over polished",
      "Practical over theoretical",
      "ASCII over images"
    ],
    colorPalette: {
      text: "Black/White (terminal)",
      background: "Default terminal",
      accent: "None (minimalist)",
      success: "Green (for completed)",
      error: "Red (for errors)"
    },
    uiElements: [
      {
        element: "Menu",
        style: "Numbered list",
        example: "1. Option One"
      },
      {
        element: "Cursor",
        style: "Blinking █",
        blinkInterval: "1.2s (intentional)"
      },
      {
        element: "Code",
        style: "Plain text",
        reason: "Feels editable, not finished"
      },
      {
        element: "Icons",
        style: "ASCII art only",
        examples: ["✓", "✗", "→", "←", "█"]
      }
    ]
  }
}
```

### Profile Management Architecture

```typescript
{
  profiles: {
    purpose: "Multiple user support",
    features: [
      "Create new profile",
      "Switch between profiles",
      "Delete profiles",
      "Per-profile progress",
      "Per-profile settings",
      "Per-profile achievements",
      "Profile export/import"
    ],
    data: {
      name: "string (unique)",
      difficulty: "string",
      theme: "string",
      dailyGoal: "number",
      created: "timestamp",
      lastActive: "timestamp"
    }
  }
}
```

### Export/Import Architecture

```typescript
{
  exportImport: {
    purpose: "Data portability and backup",
    format: "JSON",
    structure: {
      profile: "Profile information",
      progress: "Exercise progress",
      quizScores: "Quiz history",
      achievements: "Unlocked achievements",
      settings: "User settings",
      exportDate: "timestamp"
    },
    features: [
      "Export all profile data",
      "Import from backup",
      "Migrate between devices",
      "Restore deleted data",
      "Share progress"
    ]
  }
}
```

### CI/CD Pipeline

```yaml
Push to main → Test → Deploy
     ↓          ↓         ↓
  Trigger    Python CI   GitHub Pages
            (Tests)    Static Hosting
```

- **Test**: Run pytest on test files
- **Deploy**: Upload static files to GitHub Pages

### Multi-Platform Deployment

| Platform | URL | Type |
|----------|-----|------|
| GitHub Pages | https://mk-knight23.github.io/24-python-practice-scripts/ | Static Hosting |
| Vercel | https://57-starter-python-practice.vercel.app/ | Serverless |

### Extension Points

```typescript
{
  newExercises: [
    "Add more basics exercises",
    "Add more core exercises",
    "Add more advanced exercises",
    "Add specialized tracks (web, data, automation)"
  ],
  newFeatures: [
    "Add video explanations",
    "Add interactive code editor",
    "Add peer code review",
    "Add certification exams"
  ],
  newIntegrations: [
    "Add GitHub integration",
    "Add VS Code extension",
    "Add mobile app"
  ]
}
```

### Key Architectural Decisions

**Why Python 3.10+?**
- Modern Python features
- Type hints support
- Pattern matching (3.10+)
- Widespread adoption

**Why SQLite for Database?**
- Python stdlib (no dependencies)
- Single file storage
- Fast for this use case
- Easy backup/restore
- Migration from JSON

**Why No External Dependencies?**
- Easy to install and run
- Works offline
- Low maintenance burden
- Learn Python, not frameworks
- Portable across systems

**Why CLI + Web Dashboard?**
- CLI for focused learning
- Web for visual progress
- Complementary experiences
- No duplication of features
- Data synchronization via import/export

**Why Plain Text Code?**
- Feels editable, not finished
- Forces understanding
- Works everywhere
- No IDE requirements
- Copy-paste friendly

### Design Philosophy

```typescript
{
  learning: {
    style: "Practice-based, not theory-based",
    principles: [
      "Learn by doing",
      "Break it, fix it",
      "Understand why, not just how",
      "Start simple, go deep",
      "No shortcuts"
    ]
  },
  technology: {
    principles: [
      "Minimal dependencies",
      "Maximum compatibility",
      "Clear code over clever code",
      "Stdlib over packages",
      "Simple over complex"
    ]
  },
  userExperience: {
    principles: [
      "Fast to start",
      "Easy to understand",
      "Rewarding progress",
      "No friction",
      "Get out of the way"
    ]
  }
}
```

### Navigation Flow

```
CLI Launch → Select Profile → Main Menu
    ↓             ↓               ↓
  Setup        Create/Switch    ↓
                            [1] Exercises
                            [2] Quiz
                            [3] Achievements
                            [4] Analytics
                            [5] Settings
                            [6] Exit
    ↓
  Select → Run Exercise → Mark Complete → Update Progress
    ↓
  Continue Learning → Check Achievements → Track Time
```

## Live Links

## Live Links

- **GitHub**: https://github.com/mk-knight23/24-python-practice-scripts
- **Vercel**: https://57-starter-python-practice.vercel.app ✅

### Deployment Platforms
- ✅ Vercel (configured: prj_TBxkbImMi5QZuSOkXrHSiYaox6P3)

---

```
    ____        _   _                 ____                _     
   |  _ \ _   _| |_| |__   ___ _ __  |  _ \ _   _ _______| | ___
   | |_) | | | | __| '_ \ / _ \ '__| | |_) | | | | |_  /_  / |/ _ \
   |  __/| |_| | |_| | | |  __/ |    |  __/| |_| |/ / / /| |  __/
   |_|    \__, |\__|_| |_|\___|_|    |_|    \__,_/___/___|_|\___|
          |___/                                                 
```

---

## How to Run Locally

```bash
# Clone the repository
git clone https://github.com/mk-knight23/24-python-practice-scripts.git
cd 24-python-practice-scripts

# Run the CLI
python cli/runner.py

# Or use npm
npm start

# Open web dashboard
open dashboard.html
```

---

## What Will I Learn?

The practical stuff. The things you'll actually use.

**Basics** - Variables, types, conditionals, loops, lists. The vocabulary of the language.

**Core** - Functions, file handling, error handling, dictionaries. The tools you use every day.

**Advanced** - Classes, inheritance, decorators, generators. For when simple isn't enough.

Each exercise is a standalone `.py` file. Read it, run it, break it, fix it.

---

## New Features (v4.0)

### 🗄️ SQLite Database
- Persistent user profiles and progress
- Automatic migration from old JSON format
- Time tracking and analytics
- Export/import functionality

### 🎯 Quiz Mode
- Test your knowledge with interactive quizzes
- Three difficulty levels (basics, core, advanced)
- Score tracking and history
- Review incorrect answers with explanations

### 🏆 Achievements System
- Earn badges for milestones
- Track completion by category
- Unlock special achievements
- Progress indicators for next goals

### 📊 Analytics Dashboard
- Visual progress charts
- Time tracking analysis
- Learning streaks
- Category breakdown

### ⚙️ Settings & Profiles
- Multiple user profiles
- Difficulty levels
- Theme preferences
- Daily learning goals
- Export data to JSON

### 🌐 Web Dashboard
- Modern responsive interface
- Real-time progress visualization
- Interactive charts
- Dark/light themes
- Mobile-friendly

---

## Who Is This For?

- You've written "Hello, World" and want to go deeper
- You learn by doing, not watching
- You prefer text over video
- You want to understand *why*, not just *how*

If you've never seen code before, start with an introductory course first. This is practice, not theory.

---

## How Do I Use It?

### Option 1: The CLI (Recommended)

```bash
python cli/runner.py
```

Navigate exercises with the number keys. View source, run code, or open files in your editor.

### Option 2: Run Files Directly

```bash
python skills/basics/001_hello.py
```

Every file runs standalone. Open them in your editor, modify, experiment.

### Option 3: The Web Dashboard

Open `dashboard.html` in any browser. Features:
- Visual progress tracking
- Interactive quiz mode
- Achievements gallery
- Analytics charts
- Settings management
- Export/import data

---

## Directory Structure

```
skills/
  basics/           - 6 exercises
  core/             - 5 exercises
  advanced/         - 4 exercises

cli/
  runner.py         - Main menu interface
  utils.py          - Terminal helpers
  progress.py       - Progress tracking (legacy)
  database.py       - SQLite database layer
  quiz.py           - Quiz system
  achievements.py   - Badges and milestones
  settings.py       - User preferences
  analytics.py      - Progress analytics

viewer/
  index.html        - Browser-based reference

dashboard.html     - New web dashboard

design-system/
  MASTER.md         - The rules this system follows
```

---

## Design Notes

### Intentional Quirk: The Blinking Cursor

Every prompt ends with `█`. It's not functional. It's a reminder: you're in conversation with a machine. It blinks once every 1.2 seconds—not 1.0, because predictable rhythms feel robotic.

### Tradeoff: No Syntax Highlighting

Color-coded keywords make code look finished. Unapproachable. We use plain text so the code feels editable. You're looking at raw material, not a product.

### Limitation Accepted: No Images

If you can't draw it with ASCII or type it with a keyboard, it doesn't exist here. This keeps the system honest—everything must be expressible in code.

### What's Changed in v4.0

Previously, this system had:
- No progress tracking (your git commits tell that story)
- No quizzes (the code is the test)
- No social features (learning is solitary work)
- No certificates (the skills are the credential)

Now it includes:
- SQLite-based progress tracking with time analytics
- Interactive quiz mode for knowledge testing
- Achievement system for milestones
- Web dashboard for visual progress
- User profiles and settings
- Export/import functionality

While keeping the philosophy:
- Still no frameworks
- Still no social features
- Still no certificates (the skills are the credential)

---

## Philosophy

Learning happens in the gap between "I don't understand" and "Now I do." This system creates that gap, provides tools to cross it, then gets out of the way.

Every exercise has three parts:

1. **Purpose** - What this code does
2. **Example** - What running it looks like
3. **Why** - Why this matters (the human explanation)

The "Why" is the important part. Anyone can document syntax. Understanding why you'd use it—that's what makes you a programmer.

---

## Contributing

Found an error? Want to add an exercise? Open a pull request.

Guidelines:
- One concept per exercise
- Include Purpose, Example, and Why
- No external dependencies
- Follow the design system (black, white, gray only)

---

## License

MIT. Use it, modify it, teach with it. Just don't sell it as your own.

---

*Built by a human who was tired of flashy tutorials. For humans who want to learn the hard way—the right way.*

*Last updated: 2026-03-01*
