Welcome to **Chapter 3**! Now that your documents are cleanly formatted and organized, it's time to connect them to the rest of the world.

In this chapter, we will learn how to inject **Links** and **Images** into your files. The syntax for these two features is incredibly similar, which makes them easy to learn but easy to mix up if you don't look closely.

---

## Chapter 3: Links and Images

### Step 1: Adding Links (Hyperlinks)

To turn a piece of text into a clickable link, you use a combination of square brackets `[ ]` and parentheses `( )`.

* Use **Square Brackets `[ ]**` for the human-readable text (the label).
* Use **Parentheses `( )**` for the actual URL/destination.

#### How to write it:

```markdown
Search for answers on [Google](https://www.google.com).
```

#### How it renders to the user:

Search for answers on [Google](https://www.google.com).

> 💡 **The Mnemonic Device:** How do you remember which bracket comes first? Think of alphabetical order: **B**rackets `[]` come before **P**arentheses `()`.

#### Quick URLs (Autolinks)

If you just want to dump a raw URL onto the page and make it instantly clickable, you can wrap it in less-than and greater-than signs `< >`.

```markdown
Send me an email at <hello@example.com> or visit <https://github.com>.
```

---

### Step 2: Adding Images

The syntax for an image is almost identical to a link, with **one crucial addition**: you must place an exclamation mark (`!`) at the very beginning.

* The **Square Brackets `[ ]**` now hold the **Alt Text** (the text displayed if the image fails to load, or read aloud by screen readers for accessibility).
* The **Parentheses `( )**` hold the file path or URL to the image.

#### How to write it:

```markdown
![Markdown Logo](https://upload.wikimedia.org/wikipedia/commons/4/48/Markdown-mark.svg)
```

---

### Step 3: Images with Links (Clickable Images)

What if you want a user to click on an image and be taken to a website? You nest the image syntax completely *inside* the link syntax!

* Wrap the entire image tag inside the text portion `[ ]` of a regular link.

#### How to write it:

```markdown
[![Clickable Markdown Logo](https://upload.wikimedia.org/wikipedia/commons/4/48/Markdown-mark.svg)](https://en.wikipedia.org/wiki/Markdown)
```

*(When a user clicks this rendered logo, it will open the Wikipedia page for Markdown).*

---

### Step 4: Reference-style Links (Keep Code Clean)

If you have a long paragraph with ten different links, your raw Markdown text can quickly become an unreadable mess of long URLs. Reference-style links allow you to keep your text incredibly clean.

Instead of writing the URL inline, you give the link a nickname. Then, you define the URLs at the very bottom of your document.

#### How to write it:

```markdown
I love using [Obsidian][1] for daily note-taking and [GitHub][2] for storing my software projects.

... (at the very bottom of your document) ...

[1]: https://obsidian.md
[2]: https://github.com
```

---

### Challenge Checkpoint

Let's see if you can spot the differences before moving forward. Try writing or visualizing:

1. A regular link to your favorite website.
2. An image of a cat with the alt text "A cute kitten".
3. A reference link nickname setup.