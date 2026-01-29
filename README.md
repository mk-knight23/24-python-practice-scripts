# Python Practice

A terminal-based system for learning Python. No frameworks. No videos. Just code.

**Live Demo**: [GitHub Pages](https://mk-knight23.github.io/24-python-practice-scripts/)

---

## Tech Stack

- **Language**: Python 3.10+
- **CLI**: Pure Python (no dependencies)
- **Viewer**: Static HTML/CSS (no frameworks)
- **Deployment**: GitHub Pages, Vercel

---

## Live Links

- **GitHub Pages**: https://mk-knight23.github.io/24-python-practice-scripts/
- **Vercel**: https://24-python-practice-scripts.vercel.app
- **Netlify**: N/A (static HTML viewer only)

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

# Or run individual exercises
python skills/basics/001_hello.py
```

---

## What Will I Learn?

The practical stuff. The things you'll actually use.

**Basics** - Variables, types, conditionals, loops, lists. The vocabulary of the language.

**Core** - Functions, file handling, error handling, dictionaries. The tools you use every day.

**Advanced** - Classes, inheritance, decorators, generators. For when simple isn't enough.

Each exercise is a standalone `.py` file. Read it, run it, break it, fix it.

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

### Option 3: The Web Viewer

Open `viewer/index.html` in any browser. A read-only reference when you don't have a terminal handy.

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

viewer/
  index.html        - Browser-based reference

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

### What I Didn't Build

- No progress tracking (your git commits tell that story)
- No quizzes (the code is the test)
- No social features (learning is solitary work)
- No certificates (the skills are the credential)

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
