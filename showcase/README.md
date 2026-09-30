# DevVault Showcase

A modern, standalone frontend showcase website for the [DevVault](https://github.com/samuelabera21/devvault-CLI) Python CLI project.

---

## Overview

DevVault Showcase is a static presentation website designed to document, demonstrate, and highlight the capabilities of **DevVault** (`samuel-devvault` on PyPI). It provides technical reviewers, developers, and recruiters with a rapid visual overview of DevVault's architecture, CLI experience, security model, and packaging.

---

## Purpose

The showcase website serves as an interactive presentation layer:
* **Interactive CLI Simulator**: Demonstrates real command syntax and authentic terminal output across configuration CRUD, profiles, secrets, validation, diffing, and subprocess execution.
* **Architecture Visualization**: Outlines the internal modular structure of `src/devvault/` (`cli.py`, `storage.py`, `security.py`, `config.py`, etc.).
* **Package Information**: Displays real PyPI package metadata, installation commands, license information, and release artifacts.
* **Engineering Standards**: Details the testing suite (99 automated tests), Ruff linting, MyPy type analysis, and GitHub Actions CI/CD workflows.

---

## Relationship to DevVault

> **Important**: This showcase is a standalone frontend documentation and presentation layer. It is **not** integrated with the DevVault CLI runtime, contains no backend, and does not execute system-level commands or store sensitive configuration.

---

## Design Direction

Inspired by the visual identity of the Python Package Index ([PyPI](https://pypi.org)) and modern developer tools:
* **Color Palette**: Python Blue (`#306998`), Python Yellow (`#ffd43b`), Deep Navy/Slate (`#0f172a`), and clean off-white surfaces (`#f8fafc`).
* **Typography**: Clean sans-serif (`Inter`) for headings and content, with high-legibility monospace (`JetBrains Mono`) for terminal commands and code blocks.
* **Engineering-First Aesthetics**: High contrast, responsive layouts, subtle micro-interactions, and zero fake marketing metrics.

---

## Tech Stack

* **Framework**: React 18 + TypeScript
* **Bundler**: Vite 6
* **Icons**: Lucide React
* **Styling**: Vanilla CSS with custom design tokens (no heavy CSS runtime or Tailwind dependencies)

---

## Project Structure

```
showcase/
├── public/
├── src/
│   ├── components/
│   │   ├── ArchitectureDiagram.tsx    # Module structure & responsibilities
│   │   ├── CliShowcase.tsx            # Multi-tab interactive terminal demo
│   │   ├── EngineeringPractices.tsx   # Testing, security & CI/CD highlights
│   │   ├── FeaturesGrid.tsx           # 8 core feature overview cards
│   │   ├── Footer.tsx                 # Links, credits & standalone disclaimer
│   │   ├── Hero.tsx                   # Main banner, version tag & quick install
│   │   ├── InstallationGuide.tsx      # pip, pipx & source install methods
│   │   ├── Navbar.tsx                 # Sticky navigation with PyPI & GitHub CTA
│   │   ├── PackageMeta.tsx            # PyPI-inspired metadata panel
│   │   ├── ProblemSolution.tsx        # .env sprawl vs DevVault architecture
│   │   └── TechStack.tsx              # Python, cryptography, pytest, ruff, mypy
│   ├── data/
│   │   └── projectData.ts             # Centralized typed metadata
│   ├── App.tsx                        # Master layout
│   ├── index.css                      # Design tokens & responsive styles
│   └── main.tsx                       # React DOM entry
├── index.html                         # Meta tags, SEO, font links
├── package.json
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts
└── README.md
```

---

## Local Development

1. Navigate to the showcase directory:
   ```bash
   cd showcase
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open `http://localhost:3000` in your browser.

---

## Production Build

Build the static distribution:
```bash
npm run build
```

Preview the production build locally:
```bash
npm run preview
```

The optimized static files are emitted to `showcase/dist/`.

---

## Netlify Deployment

To deploy this showcase independently to Netlify:

1. Link your GitHub repository in Netlify.
2. Configure the deployment settings:
   * **Base directory**: `showcase`
   * **Build command**: `npm run build`
   * **Publish directory**: `showcase/dist`
3. Deploy site.

---

## Links

* **PyPI Package**: [https://pypi.org/project/samuel-devvault/](https://pypi.org/project/samuel-devvault/)
* **GitHub Repository**: [https://github.com/samuelabera21/devvault-CLI](https://github.com/samuelabera21/devvault-CLI)
* **Author**: Samuel Abera
