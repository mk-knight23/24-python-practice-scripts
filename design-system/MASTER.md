# Design System: Python Practice Terminal

> For humans. By a human who was tired of flashy tutorials.

---

## Color Palette

The terminal doesn't need colors. It needs clarity.

| Token | Hex | Usage |
|-------|-----|-------|
| `bg-primary` | `#000000` | Background, terminal surface |
| `bg-secondary` | `#333333` | Input areas, code blocks |
| `text-primary` | `#FFFFFF` | Main text, prompts |
| `text-secondary` | `#CCCCCC` | Secondary info, timestamps |
| `text-muted` | `#999999` | Hints, disabled states |
| `border` | `#666666` | Dividers, box outlines |

**No other colors. Ever.**

---

## Typography

**Primary:** JetBrains Mono, Courier New, monospace

**Scale:**
```
header:     1.5rem  (24px) - ASCII art, main titles
body:       1rem    (16px) - Exercise content, descriptions
small:      0.875rem (14px) - Metadata, file paths
mono:       0.9rem  - Code blocks, terminal output
```

**Line height:** 1.6 for reading, 1.2 for code

---

## Layout Rules

### Terminal Blocks

Every "card" or section uses ASCII-inspired borders:

```
+------------------+
|  HEADER TEXT     |
+------------------+
|                  |
|  Content here    |
|                  |
+------------------+
```

Or the simpler variant (preferred for inline):

```
--- section name ---
content here
-------------------
```

### Spacing

- Never use exact pixel values in comments
- "One blank line" = visual breath
- "Two blank lines" = section break
- Inconsistent spacing is *okay* - feels hand-written

---

## Components

### Code Blocks

```python
# Like this. Plain.
# No syntax highlighting colors, just the code.
def example():
    return "clarity"
```

### Exercise Cards

```
[01] exercise_name.py
     Purpose: One line description
     Why: Why this matters
```

### CLI Output

```
$ command
output line 1
output line 2
>> prompt
```

---

## The Intentional Quirk

**The "Breathing Cursor"**

Every prompt ends with a blinking cursor represented by `█` or `▌` depending on mood. Not because it's functional, but because it reminds you: you're in a conversation with the machine.

In HTML: use a CSS animation that blinks once every 1.2s (not 1s - too predictable)
In CLI: a static `>` or `>>` prompt (no blinking, save the CPU)

---

## The Tradeoff

**Accepted: No syntax highlighting**

Color-coded keywords make code feel "finished." This system uses plain text to make code feel editable. You're looking at the raw material, not the product.

**Benefit gained:** Uniform aesthetic, focus on structure over decoration.

---

## The Limitation

**No images, no icons**

If you can't draw it with ASCII or type it with a keyboard, it doesn't exist here. This keeps the system honest - everything must be expressible in code.

---

## File Naming

```
001_hello.py          # Basics: numbered
file_handler.py       # Core: descriptive
class_patterns.py     # Advanced: conceptual
```

Underscores only. No hyphens (harder to type in import statements).

---

## Comments Style

```python
# Good: explains *why*, not *what*
# Bad:  x = x + 1  # increment x

# Good: human uncertainty
#       not sure if this handles edge cases

# Good: conversational
#       let's try a simpler approach here
```

---

## Terminal Prompts

Always show the `$` or `>>` to indicate "this is runnable" vs "this is output."

```
$ python script.py    # command you type
Hello, World          # output you see
>> Next?              # system prompt
```

---

*Last updated: by hand, when it needed updating.*
