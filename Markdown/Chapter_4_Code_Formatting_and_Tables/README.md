Welcome to **Chapter 4**! This is the absolute favorite chapter for programmers, technical writers, and data analysts.

In this chapter, we explore how to display **Code Elements** (both inline and in blocks with syntax highlighting) and how to construct clean data **Tables** without touching complex HTML or Excel formulas.

---

## Chapter 4: Code Formatting & Tables

### Step 1: Inline Code

Sometimes you don't want to format an entire paragraph as code—you just want to highlight a single variable, command, or file name inside a normal sentence. To do this, wrap the target text in **single backticks (```)**.

> ⚠️ **The Backtick Trap:** A backtick is *not* a single quote (`'`). On most standard keyboards, you can find the backtick key right below the **Esc** key, sharing a button with the tilde (`~`).

#### How to write it:

```markdown
To install the package, type `npm install backend-hub` into your terminal.
```

#### How it renders to the user:

To install the package, type `npm install backend-hub` into your terminal.

---

### Step 2: Code Blocks & Syntax Highlighting

If you need to display multiple lines of code, wrapping them line-by-line is tedious. Instead, use a fenced code block by wrapping the entire block in **triple backticks (`````)** on the lines before and after your code.

To make it look truly professional, write the name of the programming language immediately after the opening triple backticks. The Markdown parser will apply automatic **syntax highlighting** (coloring keywords, strings, and variables correctly).

#### How to write it:

```markdown
```python
def calculate_area(radius):
    pi = 3.14159
    return pi * (radius ** 2)
```

```

#### How it renders to the user:
```python
def calculate_area(radius):
    pi = 3.14159
    return pi * (radius ** 2)
```

---

### Step 3: Tables

Tables allow you to organize complex data points cleanly. In Markdown, tables are built using **pipes (`|`)** to separate columns and **hyphens (`-`)** to create headers.

#### The Anatomy of a Basic Table:

1. The first line contains your column headers, separated by pipes.
2. The second line is the **divider line** (a row of hyphens separated by pipes). This line tells Markdown, *"Everything above me is a header, and everything below me is data."*
3. The remaining lines contain your data.

#### How to write it:

```markdown
| Item ID | Product Name | Stock Level | Price |
|---|---|---|---|
| #1024 | Mechanical Keyboard | 14 Available | $89.00 |
| #2089 | Wireless Mouse | Out of Stock | $45.00 |

```

#### How it renders to the user:

| Item ID | Product Name | Stock Level | Price |
| --- | --- | --- | --- |
| #1024 | Mechanical Keyboard | 14 Available | $89.00 |
| #2089 | Wireless Mouse | Out of Stock | $45.00 |

#### Controlling Column Alignment

By default, table content aligns to the left. You can alter this alignment by adding **colons (`:`)** to the divider line row:

* **Left Align (Default):** `:---`
* **Right Align:** `---:`
* **Center Align:** `:---:`

#### How to write it:

```markdown
| Left Aligned | Center Aligned | Right Aligned |
| :--- | :---: | ---: |
| Text | More Text | Price Tag |
| Alpha | Beta | $100.00 |
```

#### How it renders to the user:

| Left Aligned | Center Aligned | Right Aligned |
| --- | --- | --- |
| Text | More Text | Price Tag |
| Alpha | Beta | $100.00 |
---

### Challenge Checkpoint

Let's see if you can blend these structural elements together:

1. Write a sentence that includes the inline code flag for a file named `settings.py`.
2. Draft a simple 2-column table tracking *Language* and *Difficulty Level*, making the difficulty column **centered**.