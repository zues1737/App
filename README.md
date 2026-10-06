# PCDP Portal (Placement & Career Development Portal)

A high-fidelity, complete reconstruction of the student **PCDP Portal** (`ps.bitsathy.ac.in`) built from the captured portal pages and sources.

---

## 🌟 Overview & Features

This application faithfully reproduces the entire PCDP experience with 100% pixel-perfect fidelity, retaining all original styles, Boxicons glyphs, colors, metrics, and student profile data:

- **Student Credentials & Profile**: Karthikeyan S (`2024UCS1132`, Reg: `7376241CS231`, CSE Dept, III Year).
- **Points & Metrics**:
  - **46,690** Activity Points (×4 Multiplier · Section `B#078`)
  - **460** Opportunity Points (Tier 1 Placement Ready)
  - **83 / 100** Platform Responsiveness Score
- **Interactive Schedule**:
  - Today's Committed Schedule (Tue 6 Oct 2026)
  - Clickable date strip with day/week switcher and "Jump to Today" feature.
- **61 Interactive Courses**:
  - Complete catalog of courses across all levels (Level 0 through Level 5).
  - Real-time search filter and Level tags (Level 0, 1, 2, Core, etc.).
  - Course details modal with interactive launch triggers.
- **18 Practice Courses**:
  - Real technical assessments with progress indicators and question counters.
  - Live search filter and assessment start modal.
- **PS Activities & Academics**:
  - Full suite of student modules: Academics, Movement Pass, Survey Evaluation, Placement, Leaves, Reports, Transport, Groups, and Attendance.
- **Code Review**:
  - Complete interactive data table with search filtering and reviewer feedback inspection.
- **Modals & Dialogs**:
  - Activity Points & Opportunity Points category breakdowns and recent transactions.
  - Responsive Score breakdown.
  - Digital Campus Movement Pass (Gate Pass QR).
  - Leave Application & Balance modal.
  - Sign out confirmation modal.
- **Responsive Layout**:
  - Desktop sidebar with tooltip popouts.
  - Mobile slide-out drawer menu and floating bottom navigation bar.

---

## 🚀 How to Run

### Option 1: Direct File / Zero-Dependency Mode
Double-click `index.html` or open `index.html` directly in any web browser (Chrome, Edge, Firefox). Everything runs completely offline with zero configuration.

### Option 2: Vite Development Server
```bash
npm run dev
```
Starts Vite dev server at `http://localhost:3000`.

### Option 3: Production Build & Preview
```bash
npm run build
npm run preview
```
The optimized production bundle is generated in the `dist/` directory.

---

## 📁 Directory Structure

```
pcdp/
├── assets/
│   ├── css/
│   │   ├── portal.css          # Combined Tailwind, Boxicons & custom styles
│   │   ├── boxicons.min.css
│   │   └── ...
│   ├── fonts/                  # Boxicons WOFF2, WOFF, TTF fonts
│   └── images/                 # 97 course thumbnails, logos, and badges
├── dist/                       # Production build output
├── public/                     # Static assets directory
├── index.html                  # Main application entry point
├── package.json                # Project scripts and dependencies
├── vite.config.js              # Vite build configuration
└── README.md                   # Documentation
```
