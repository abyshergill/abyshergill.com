Welcome to **Chapter 2**! Now that you know how to write headers and change text emphasis, it’s time to bring order to the chaos.

In this chapter, we will look at how Markdown organizes information using **Lists**, **Task Lists (Checklists)**, and **Blockquotes**. These are the bread and butter of meeting notes, to-do apps, and documentation files.

---

## Chapter 2: Lists, Task Lists, and Blockquotes

### Step 1: Unordered Lists (Bulleted Lists)

When the order of items doesn't matter (like a grocery list), you use an unordered list. In Markdown, you can use an asterisk (`*`), a minus sign (`-`), or a plus sign (`+`) followed by a space.

> 💡 **Pro-Tip:** Stick to one symbol throughout your document to keep your raw code looking clean. Most developers prefer the hyphen (`-`).

#### How to write it:

```markdown
- Chilled coffee beans
- Whole milk
- Vanilla syrup
```

#### Creating Nested Lists (Sub-items)

To create an indented sub-item, just press **Enter**, hit the **Spacebar two or four times** (or press **Tab**), and type your list symbol again.

#### How to write it:

```markdown
- Coffee Drinks
  - Espresso
  - Latte
    - Oat Milk Latte
- Tea Drinks
  - Matcha Green Tea
```

---

### Step 2: Ordered Lists (Numbered Lists)

When sequence matters (like a recipe or step-by-step instructions), use numbers followed by a period and a space.

Here is a bizarre but awesome Markdown quirk: **The actual numbers you type do not matter.** The Markdown parser automatically numbers them sequentially for the reader.

#### How to write it:

```markdown
1. Open the text editor.
1. Type out your Markdown notes.
1. Save the file with a `.md` extension.

```

#### How it renders to the user:

1. Open the text editor.
2. Type out your Markdown notes.
3. Save the file with a `.md` extension.

---

### Step 3: Task Lists (Checklists)

Task lists are incredibly useful for tracking progress on GitHub or in modern note-taking tools like Notion and Obsidian.

You build them by combining a regular list item with square brackets `[ ]`.

* For an **empty** checkbox, leave a space between the brackets: `[ ]`
* For a **checked** checkbox, place a lowercase `x` between the brackets: `[x]`

#### How to write it:

```markdown
- [x] Master basic formatting (Chapter 1)
- [ ] Learn lists and task lists (Chapter 2)
- [ ] Build the final project (Chapter 6)
```

---

### Step 4: Blockquotes

Blockquotes are used to highlight quotes, callout notes, or external references. To turn a paragraph into a blockquote, simply place a greater-than symbol (`>`) at the beginning of the line.

#### How to write it:

```markdown
As a wise developer once said:

> "The best error message is the one that never shows up because your code works seamlessly."

```

#### How it renders to the user:

As a wise developer once said:

> "The best error message is the one that never shows up because your code works seamlessly."

---

### Challenge Checkpoint

Let's see if you've got this down before we move to the next chapter. Try visualizing or sketching a Markdown block that includes:

1. A blockquote containing a piece of advice.
2. A numbered list inside or below that blockquote.
3. A 2-item checklist where one item is checked off and one is left blank.

