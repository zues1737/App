import json, re

with open("views_data.json", "r", encoding="utf-8") as f:
    views = json.load(f)

# Helper to escape backticks and dollar signs for template literal or script inclusion
def js_escape(s):
    return s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

views_js = "{\n"
for k, v in views.items():
    views_js += f'  "{k}": `{js_escape(v)}`,\n'
views_js += "}"

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PS Portal</title>
  <link rel="icon" href="./assets/images/logo.e99a8edb9e376c3ed2e5.png">
  <link rel="stylesheet" href="./assets/css/portal.css">
  <style>
    .filter-chip.active {{
      background-color: #185FA5 !important;
      color: #ffffff !important;
      border-color: #185FA5 !important;
    }}
    .toast-msg {{
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      background: #1e293b;
      color: white;
      padding: 0.75rem 1.25rem;
      border-radius: 0.5rem;
      box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2);
      z-index: 10000;
      opacity: 0;
      transform: translateY(10px);
      transition: all 0.25s ease-in-out;
      pointer-events: none;
    }}
    .toast-msg.show {{
      opacity: 1;
      transform: translateY(0);
    }}
  </style>
</head>
<body class="bg-background text-slate-900 overflow-hidden font-sans">
  <div class="w-screen h-screen flex relative">

    <!-- Mobile Sidebar Drawer Backdrop -->
    <div id="mobileDrawerBackdrop" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40 hidden md:hidden transition-opacity"></div>

    <!-- Sidebar Navigation -->
    <aside id="appSidebar" class="no-print AppSidebar hidden md:flex fixed md:relative z-50 inset-y-0 left-0 w-max min-w-[5.5rem] bg-secondary flex-col items-center p-5 overflow-y-auto transition-transform duration-300">
      <div class="mb-4 flex items-center justify-between w-full md:justify-center">
        <a href="#dashboard" class="flex items-center gap-2">
          <img width="40" src="./assets/images/logo.e99a8edb9e376c3ed2e5.png" alt="logo" class="object-contain hover:scale-105 transition-transform">
        </a>
        <button id="closeMobileSidebar" class="md:hidden text-slate-400 hover:text-white p-1">
          <i class="bx bx-x text-2xl"></i>
        </button>
      </div>

      <!-- Sidebar Menu Items -->
      <nav class="flex-1 flex flex-col items-center justify-center gap-7 w-full my-auto">
        <div data-nav="dashboard" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white bg-primary text-white transition-all shadow-sm" title="Dashboard">
          <i class="bx bxs-dashboard" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium shadow-md whitespace-nowrap">Dashboard</span>
        </div>

        <div data-nav="courses" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all" title="Courses Available">
          <i class="bx bxs-videos" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium shadow-md whitespace-nowrap">Courses Available</span>
        </div>

        <div data-nav="my-course" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all" title="My Course">
          <i class="bx bxl-youtube" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium shadow-md whitespace-nowrap">My Course</span>
        </div>

        <div data-nav="activity" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all" title="PS Activity">
          <i class="bx bx-collection" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium shadow-md whitespace-nowrap">PS Activity</span>
        </div>

        <div data-nav="practice" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all" title="Practice Courses">
          <i class="bx bxs-book-open" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium shadow-md whitespace-nowrap">Practice Courses</span>
        </div>

        <div data-nav="academics" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all" title="Academics">
          <i class="bx bx-education" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium shadow-md whitespace-nowrap">Academics</span>
        </div>

        <div data-nav="code-review" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all" title="Code Review">
          <i class="bx bx-code-alt" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium shadow-md whitespace-nowrap">Code Review</span>
        </div>

        <div data-nav="logout" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-red-600 hover:text-white text-iconColor transition-all mt-auto" title="Logout">
          <i class="bx bx-log-out" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-red-600 text-white text-xs font-medium shadow-md whitespace-nowrap">Logout</span>
        </div>
      </nav>
    </aside>

    <!-- Main Content Container -->
    <main class="flex-1 flex flex-col h-screen w-full overflow-hidden bg-background">
      <!-- Top Navigation Bar -->
      <header class="no-print w-full bg-white px-4 py-2.5 min-h-[4.25rem] flex items-center justify-between shadow-sm z-20 border-b border-slate-100">
        <div class="flex gap-4 items-center">
          <button id="mobileMenuBtn" class="text-2xl text-slate-700 hover:text-primary cursor-pointer block md:hidden p-1 rounded-lg focus:outline-none" aria-label="Toggle menu">
            <i class="bx bx-menu text-3xl"></i>
          </button>
          <div class="flex items-center gap-2">
            <span class="font-bold text-lg tracking-tight text-slate-800">PCDP Portal</span>
            <span class="hidden sm:inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-violet-100 text-violet-800">v2.0</span>
          </div>
        </div>

        <!-- Student Profile Pill -->
        <div id="profileBadge" class="flex gap-3 items-center bg-slate-50 hover:bg-slate-100 border border-slate-200/60 py-1.5 px-3 rounded-xl cursor-pointer transition-all select-none">
          <div class="w-9 h-9 rounded-full bg-[#534AB7] text-white flex items-center justify-center font-bold text-xs ring-2 ring-violet-200">KS</div>
          <div class="sm:flex hidden flex-col text-left">
            <h2 class="text-[12px] font-medium text-slate-500 leading-tight">2024UCS1132</h2>
            <h2 class="text-[14px] font-bold text-slate-900 leading-tight">KARTHIKEYAN S</h2>
          </div>
          <i class="bx bx-chevron-down text-slate-400 text-lg hidden sm:block"></i>
        </div>
      </header>

      <!-- Dynamic Page Content -->
      <div id="contentContainer" class="flex-1 w-full overflow-y-auto pb-24 lg:pb-6">
        <!-- Rendered view injected here -->
      </div>
    </main>

    <!-- Floating Mobile Bottom Bar -->
    <div class="pointer-events-none fixed inset-x-0 bottom-0 z-40 flex justify-center px-3 pb-[max(0.75rem,env(safe-area-inset-bottom))] lg:hidden">
      <div class="pointer-events-auto relative flex max-w-[min(100%,420px)] items-center gap-2 rounded-[1.75rem] border border-white/60 bg-white/95 px-3 py-2 shadow-[0_12px_40px_rgba(15,23,42,0.2)] backdrop-blur-xl">
        <button type="button" data-mobile-nav="dashboard" title="Home" class="flex h-11 w-11 items-center justify-center rounded-2xl transition-transform active:scale-90" style="background-color: rgba(125, 83, 246, 0.12); color: rgb(125, 83, 246);">
          <i class="bx bxs-home text-[22px]"></i>
        </button>
        <button type="button" data-mobile-action="leaves" title="My Leaves" class="flex h-11 w-11 items-center justify-center rounded-2xl transition-transform active:scale-90" style="background-color: rgb(225, 245, 238); color: rgb(15, 110, 86);">
          <i class="bx bxs-report text-[22px]"></i>
        </button>
        <button type="button" data-mobile-action="pass" title="Movement Pass" class="flex h-11 w-11 items-center justify-center rounded-2xl transition-transform active:scale-90" style="background-color: rgb(230, 241, 251); color: rgb(24, 95, 165);">
          <i class="bx bx-walk text-[22px]"></i>
        </button>
        <button type="button" data-mobile-action="customize" title="Customize" class="flex h-11 w-11 items-center justify-center rounded-2xl border border-dashed bg-white active:scale-90" style="border-color: rgba(125, 83, 246, 0.4); color: rgb(125, 83, 246);">
          <i class="bx bx-plus text-2xl"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- Reusable Modal Dialog -->
  <div id="portalModal" class="modal-overlay">
    <div class="modal-card">
      <div class="flex items-center justify-between p-4 border-b border-slate-100">
        <h3 id="modalTitle" class="font-bold text-lg text-slate-800">Details</h3>
        <button id="modalCloseBtn" class="text-slate-400 hover:text-slate-700 p-1 rounded-lg">
          <i class="bx bx-x text-2xl"></i>
        </button>
      </div>
      <div id="modalBody" class="p-5 text-slate-600 text-sm leading-relaxed">
        <!-- Injected modal content -->
      </div>
      <div id="modalFooter" class="p-4 border-t border-slate-100 flex justify-end gap-2 bg-slate-50 rounded-b-2xl">
        <button id="modalPrimaryBtn" class="px-4 py-2 rounded-xl text-xs font-semibold bg-primary text-white hover:opacity-90">Close</button>
      </div>
    </div>
  </div>

  <!-- Toast Notification -->
  <div id="toast" class="toast-msg">Notification</div>

  <!-- Master Application Script -->
  <script>
    const VIEWS = {views_js};

    // Modal Controller
    const modal = document.getElementById("portalModal");
    const modalTitle = document.getElementById("modalTitle");
    const modalBody = document.getElementById("modalBody");
    const modalFooter = document.getElementById("modalFooter");
    const modalCloseBtn = document.getElementById("modalCloseBtn");
    const modalPrimaryBtn = document.getElementById("modalPrimaryBtn");

    function openModal(title, contentHtml, footerHtml = null) {{
      modalTitle.innerText = title;
      modalBody.innerHTML = contentHtml;
      if (footerHtml !== null) {{
        modalFooter.innerHTML = footerHtml;
      }} else {{
        modalFooter.innerHTML = '<button onclick="closeModal()" class="px-4 py-2 rounded-xl text-xs font-semibold bg-[#7D53F6] text-white hover:opacity-90">Close</button>';
      }}
      modal.classList.add("active");
    }}

    function closeModal() {{
      modal.classList.remove("active");
    }}

    modalCloseBtn.addEventListener("click", closeModal);
    modal.addEventListener("click", (e) => {{
      if (e.target === modal) closeModal();
    }});
    document.addEventListener("keydown", (e) => {{
      if (e.key === "Escape") closeModal();
    }});

    // Toast Controller
    function showToast(msg) {{
      const toast = document.getElementById("toast");
      toast.innerText = msg;
      toast.classList.add("show");
      setTimeout(() => toast.classList.remove("show"), 2600);
    }}

    // Mobile Sidebar Drawer
    const mobileMenuBtn = document.getElementById("mobileMenuBtn");
    const appSidebar = document.getElementById("appSidebar");
    const mobileDrawerBackdrop = document.getElementById("mobileDrawerBackdrop");
    const closeMobileSidebar = document.getElementById("closeMobileSidebar");

    function toggleMobileMenu(open) {{
      if (open) {{
        appSidebar.classList.remove("hidden");
        mobileDrawerBackdrop.classList.remove("hidden");
      }} else {{
        appSidebar.classList.add("hidden");
        mobileDrawerBackdrop.classList.add("hidden");
      }}
    }}

    mobileMenuBtn?.addEventListener("click", () => toggleMobileMenu(true));
    closeMobileSidebar?.addEventListener("click", () => toggleMobileMenu(false));
    mobileDrawerBackdrop?.addEventListener("click", () => toggleMobileMenu(false));

    // Profile Click Popup
    document.getElementById("profileBadge")?.addEventListener("click", () => {{
      openModal("Student Profile", `
        <div class="flex items-center gap-4 mb-4">
          <div class="w-16 h-16 rounded-full bg-[#534AB7] text-white flex items-center justify-center font-bold text-xl shadow-md">KS</div>
          <div>
            <h4 class="text-base font-bold text-slate-900">KARTHIKEYAN S</h4>
            <div class="text-xs text-slate-500 font-mono mt-0.5">Roll No: 2024UCS1132</div>
            <div class="text-xs text-slate-500 font-mono">Reg No: 7376241CS231</div>
          </div>
        </div>
        <div class="space-y-2 border-t border-slate-100 pt-3 text-xs">
          <div class="flex justify-between py-1 border-b border-slate-50"><span class="text-slate-500">Department</span><span class="font-medium text-slate-800">Computer Science and Engineering</span></div>
          <div class="flex justify-between py-1 border-b border-slate-50"><span class="text-slate-500">Current Year</span><span class="font-medium text-slate-800">III Year</span></div>
          <div class="flex justify-between py-1 border-b border-slate-50"><span class="text-slate-500">Student Group</span><span class="font-bold text-[#534AB7]">B#078</span></div>
          <div class="flex justify-between py-1 border-b border-slate-50"><span class="text-slate-500">Skill Community</span><span class="font-medium text-slate-800">Big Data Analytics & Machine Learning (Sec 2)</span></div>
          <div class="flex justify-between py-1"><span class="text-slate-500">Learning Mode</span><span class="font-medium text-slate-800">Project-Based Learning Mode</span></div>
        </div>
      `);
    }});

    // Mobile Bottom Bar Actions
    document.querySelector('[data-mobile-action="leaves"]')?.addEventListener("click", () => openLeavesModal());
    document.querySelector('[data-mobile-action="pass"]')?.addEventListener("click", () => openMovementPassModal());
    document.querySelector('[data-mobile-action="customize"]')?.addEventListener("click", () => showToast("Widget customization is active. Drag cards to reorder."));
    document.querySelector('[data-mobile-nav="dashboard"]')?.addEventListener("click", () => switchView("dashboard"));

    // Quick Modals
    function openLeavesModal() {{
      openModal("My Leaves", `
        <div class="p-2 space-y-3">
          <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-3 text-emerald-800 text-xs">
            <strong>Leave Balance:</strong> 6 Days Available · 0 Pending Approvals
          </div>
          <p class="text-xs text-slate-600">You can apply for Medical Leave, OD (On Duty), or Casual Leave through this portal.</p>
          <div class="grid grid-cols-2 gap-2 pt-2">
            <button onclick="showToast('Leave application submitted for approval'); closeModal();" class="p-2.5 rounded-xl border border-emerald-300 bg-white hover:bg-emerald-50 text-emerald-700 font-semibold text-xs text-center transition-all">Apply OD</button>
            <button onclick="showToast('Leave application submitted for approval'); closeModal();" class="p-2.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs text-center transition-all">Apply Casual Leave</button>
          </div>
        </div>
      `);
    }}

    function openMovementPassModal() {{
      openModal("Movement Pass", `
        <div class="p-2 text-center space-y-3">
          <div class="inline-flex p-3 rounded-2xl bg-blue-50 text-blue-700 mb-1">
            <i class="bx bx-qr-scan text-4xl"></i>
          </div>
          <h4 class="font-bold text-slate-900 text-sm">Digital Campus Gate Pass</h4>
          <p class="text-xs text-slate-500">Authorized student movement pass for Academic Labs & Innovation Centers.</p>
          <div class="bg-slate-50 rounded-xl p-3 text-xs text-left space-y-1.5 border border-slate-200">
            <div class="flex justify-between"><span class="text-slate-500">Pass Status:</span><span class="font-bold text-emerald-600">● ACTIVE</span></div>
            <div class="flex justify-between"><span class="text-slate-500">Valid Until:</span><span class="font-medium text-slate-800">Today, 08:30 PM</span></div>
            <div class="flex justify-between"><span class="text-slate-500">Destination:</span><span class="font-medium text-slate-800">AI / Robotics Lab & Library</span></div>
          </div>
        </div>
      `);
    }}

    function openActivityBreakdown() {{
      openModal("Activity Points Breakdown", `
        <div class="space-y-4">
          <div class="flex items-center justify-between bg-[#EEEDFE] p-4 rounded-xl">
            <div>
              <div class="text-2xl font-bold text-[#534AB7]">46,690</div>
              <div class="text-xs font-semibold text-[#534AB7]">Total Activity Points</div>
            </div>
            <div class="text-right">
              <span class="text-xs font-bold px-2 py-1 rounded bg-[#534AB7] text-white">×4 Multiplier</span>
              <div class="text-[11px] text-slate-500 mt-1">Section B#078</div>
            </div>
          </div>
          <div>
            <h5 class="text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">Category Breakdown</h5>
            <div class="space-y-2 text-xs">
              <div>
                <div class="flex justify-between mb-1"><span class="text-slate-600">Hackathons & Competitions</span><span class="font-bold text-slate-800">18,400 pts</span></div>
                <div class="w-full bg-slate-100 rounded-full h-2"><div class="bg-indigo-600 h-2 rounded-full" style="width: 40%"></div></div>
              </div>
              <div>
                <div class="flex justify-between mb-1"><span class="text-slate-600">Weekly Assessments & Practice</span><span class="font-bold text-slate-800">15,200 pts</span></div>
                <div class="w-full bg-slate-100 rounded-full h-2"><div class="bg-violet-500 h-2 rounded-full" style="width: 32%"></div></div>
              </div>
              <div>
                <div class="flex justify-between mb-1"><span class="text-slate-600">S5 Mini Projects & Innovations</span><span class="font-bold text-slate-800">8,500 pts</span></div>
                <div class="w-full bg-slate-100 rounded-full h-2"><div class="bg-blue-500 h-2 rounded-full" style="width: 18%"></div></div>
              </div>
              <div>
                <div class="flex justify-between mb-1"><span class="text-slate-600">Core Engineering Assessments</span><span class="font-bold text-slate-800">4,590 pts</span></div>
                <div class="w-full bg-slate-100 rounded-full h-2"><div class="bg-emerald-500 h-2 rounded-full" style="width: 10%"></div></div>
              </div>
            </div>
          </div>
          <div class="border-t border-slate-100 pt-3">
            <h5 class="text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">Recent Transactions</h5>
            <div class="space-y-1.5 text-xs text-slate-600">
              <div class="flex justify-between p-2 rounded-lg bg-slate-50"><span>August GP challenge 2026 Milestone</span><span class="font-bold text-emerald-600">+1,200 AP</span></div>
              <div class="flex justify-between p-2 rounded-lg bg-slate-50"><span>Placement Weekly Assessment (Week 1)</span><span class="font-bold text-emerald-600">+800 AP</span></div>
              <div class="flex justify-between p-2 rounded-lg bg-slate-50"><span>Data Science Practice Assessment</span><span class="font-bold text-emerald-600">+450 AP</span></div>
            </div>
          </div>
        </div>
      `);
    }}

    function openOpportunityBreakdown() {{
      openModal("Opportunity Points Breakdown", `
        <div class="space-y-4">
          <div class="flex items-center justify-between p-4 rounded-xl" style="background: rgb(250, 238, 218);">
            <div>
              <div class="text-2xl font-bold" style="color: rgb(186, 117, 23);">460</div>
              <div class="text-xs font-semibold" style="color: rgb(186, 117, 23);">Total Opportunity Points</div>
            </div>
            <span class="text-xs font-bold px-2 py-1 rounded bg-amber-600 text-white">Tier 1 Placement Ready</span>
          </div>
          <div class="text-xs space-y-2 text-slate-600">
            <p>Opportunity Points reflect your eligibility priority for high-value campus placement drives, super-dream offers, and industry internships.</p>
            <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1">
              <div class="flex justify-between"><span class="text-slate-500">Tier 1 Drives Required:</span><span class="font-bold text-slate-800">400 OP (Achieved)</span></div>
              <div class="flex justify-between"><span class="text-slate-500">Dream Offer Multiplier:</span><span class="font-bold text-slate-800">1.25x</span></div>
            </div>
          </div>
        </div>
      `);
    }}

    function openResponsiveBreakdown() {{
      openModal("Responsive Score Breakdown", `
        <div class="space-y-4">
          <div class="flex items-center justify-between p-4 rounded-xl" style="background: rgb(225, 245, 238);">
            <div>
              <div class="text-2xl font-bold" style="color: rgb(15, 110, 86);">83 / 100</div>
              <div class="text-xs font-semibold" style="color: rgb(15, 110, 86);">Platform Responsiveness Score</div>
            </div>
            <span class="text-xs font-bold px-2 py-1 rounded bg-emerald-600 text-white">Top 10%</span>
          </div>
          <div class="text-xs space-y-2 text-slate-600">
            <div class="flex justify-between py-1 border-b border-slate-100"><span>Survey Response Speed:</span><span class="font-semibold text-slate-800">92%</span></div>
            <div class="flex justify-between py-1 border-b border-slate-100"><span>Assessment Punctuality:</span><span class="font-semibold text-slate-800">86%</span></div>
            <div class="flex justify-between py-1"><span>Daily Commitment Check-in:</span><span class="font-semibold text-slate-800">79%</span></div>
          </div>
        </div>
      `);
    }}

    function openLogoutModal() {{
      openModal("Confirm Logout", `
        <div class="text-center py-2">
          <i class="bx bx-log-out-circle text-5xl text-red-500 mb-2"></i>
          <h4 class="text-base font-bold text-slate-800">Sign Out of PCDP Portal?</h4>
          <p class="text-xs text-slate-500 mt-1">You will need to re-authenticate with your student credentials to log back in.</p>
        </div>
      `, `
        <button onclick="closeModal()" class="px-4 py-2 rounded-xl text-xs font-medium border border-slate-200 text-slate-600 hover:bg-slate-50">Cancel</button>
        <button onclick="showToast('Logged out successfully'); closeModal(); setTimeout(() => location.reload(), 1200);" class="px-4 py-2 rounded-xl text-xs font-semibold bg-red-600 text-white hover:bg-red-700">Logout</button>
      `);
    }}

    // Switch View function
    let currentView = "dashboard";
    const container = document.getElementById("contentContainer");

    function switchView(viewName) {{
      if (viewName === "logout") {{
        openLogoutModal();
        return;
      }}

      if (!VIEWS[viewName]) {{
        viewName = "dashboard";
      }}
      currentView = viewName;

      // Update sidebar active classes
      document.querySelectorAll(".nav-item").forEach(item => {{
        const target = item.getAttribute("data-nav");
        if (target === viewName) {{
          item.className = "nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white bg-primary text-white transition-all shadow-sm";
        }} else if (target === "logout") {{
          item.className = "nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-red-600 hover:text-white text-iconColor transition-all mt-auto";
        }} else {{
          item.className = "nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all";
        }}
      }});

      // Close mobile drawer if open
      toggleMobileMenu(false);

      // Inject View HTML
      container.innerHTML = VIEWS[viewName];
      container.scrollTop = 0;

      // Update Hash without jumping
      if (location.hash !== "#" + viewName) {{
        history.replaceState(null, "", "#" + viewName);
      }}

      // Attach View-specific event handlers
      bindViewEvents(viewName);
    }}

    // Bind Interactive Handlers
    function bindViewEvents(viewName) {{
      if (viewName === "dashboard") {{
        // Points breakdown clicks
        const buttons = container.querySelectorAll("button");
        buttons.forEach(btn => {{
          const txt = btn.innerText || "";
          if (txt.includes("Activity Points") || txt.includes("46,690")) {{
            btn.addEventListener("click", openActivityBreakdown);
          }} else if (txt.includes("Opportunity Points") || txt.includes("460")) {{
            btn.addEventListener("click", openOpportunityBreakdown);
          }} else if (txt.includes("Responsive Score") || txt.includes("83")) {{
            btn.addEventListener("click", openResponsiveBreakdown);
          }}
        }});

        // Quick navigation buttons
        container.querySelectorAll('[data-dashboard-section="quickNav"] button').forEach(b => {{
          const t = b.innerText || "";
          if (t.includes("My Leaves")) b.addEventListener("click", openLeavesModal);
          if (t.includes("Movement Pass")) b.addEventListener("click", openMovementPassModal);
          if (t.includes("Edit")) b.addEventListener("click", () => showToast("Quick Navigation reorder enabled"));
        }});

        // Schedule interactive dates
        const scheduleDates = container.querySelectorAll('[data-dashboard-section="schedule"] .cursor-pointer');
        scheduleDates.forEach(dateCard => {{
          dateCard.addEventListener("click", function() {{
            scheduleDates.forEach(d => {{
              d.className = d.className.replace("bg-[#185FA5] text-white !border-2 !border-[#185FA5]", "bg-white");
              d.querySelectorAll("*").forEach(el => {{
                if (el.classList.contains("text-white")) {{
                  el.classList.remove("text-white");
                  el.classList.add(el.tagName === "DIV" && el.innerText.length <= 2 ? "text-[#1e293b]" : "text-slate-500");
                }}
              }});
            }});
            this.className = "flex flex-col items-center justify-center w-9 h-10 border cursor-pointer transition-all bg-[#185FA5] border-[#185FA5] !border-2 !border-[#185FA5]";
            this.querySelectorAll("*").forEach(el => {{
              el.classList.remove("text-slate-500", "text-[#1e293b]");
              el.classList.add("text-white");
            }});
            const dayNum = this.querySelector(".text-\\\\[12px\\\\]")?.innerText || "";
            const dayName = this.querySelector(".text-\\\\[11px\\\\]")?.innerText || "";
            const schedHeader = container.querySelector('[data-dashboard-section="schedule"] .text-\\\\[11px\\\\].font-medium');
            if (schedHeader && dayNum) {{
              schedHeader.innerText = `${{dayName}} ${{dayNum}} Oct 2026`;
            }}
            showToast(`Schedule loaded for ${{dayName}} ${{dayNum}} Oct 2026`);
          }});
        }});

        // Jump to Today button
        container.querySelectorAll('[data-dashboard-section="schedule"] button').forEach(btn => {{
          if (btn.innerText.includes("Jump to Today")) {{
            btn.addEventListener("click", () => {{
              const schedHeader = container.querySelector('[data-dashboard-section="schedule"] .text-\\\\[11px\\\\].font-medium');
              if (schedHeader) schedHeader.innerText = "Tue 6 Oct 2026";
              showToast("Jumped to Today: Tue 6 Oct 2026");
            }});
          }}
          if (btn.innerText.trim() === "day" || btn.innerText.trim() === "week") {{
            btn.addEventListener("click", function() {{
              this.parentElement.querySelectorAll("button").forEach(b => {{
                b.style.background = "transparent";
                b.style.color = "rgb(100, 116, 139)";
              }});
              this.style.background = "rgb(30, 41, 59)";
              this.style.color = "rgb(255, 255, 255)";
              showToast(`Switched to ${{this.innerText.trim()}} view`);
            }});
          }}
        }});
      }}

      if (viewName === "courses" || viewName === "my-course") {{
        // Add Live Search Bar above courses
        const titleHeading = container.querySelector("h3.text-xl");
        if (titleHeading && !container.querySelector("#courseSearchBar")) {{
          const searchDiv = document.createElement("div");
          searchDiv.className = "my-4 flex flex-col sm:flex-row gap-3 items-center justify-between";
          searchDiv.innerHTML = `
            <div class="relative w-full sm:w-80">
              <i class="bx bx-search absolute left-3 top-2.5 text-slate-400 text-lg"></i>
              <input id="courseSearchBar" type="text" placeholder="Search courses (e.g. C++, AI, DBMS)..." 
                class="w-full pl-9 pr-3 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:outline-primary placeholder:text-slate-400">
            </div>
            <div class="flex gap-1.5 flex-wrap w-full sm:w-auto">
              <button class="course-chip px-3 py-1 rounded-lg text-xs font-medium border border-slate-200 bg-white hover:bg-slate-50 filter-chip active" data-level="all">All (61)</button>
              <button class="course-chip px-3 py-1 rounded-lg text-xs font-medium border border-slate-200 bg-white hover:bg-slate-50 filter-chip" data-level="Level 0">Level 0</button>
              <button class="course-chip px-3 py-1 rounded-lg text-xs font-medium border border-slate-200 bg-white hover:bg-slate-50 filter-chip" data-level="Level 1">Level 1</button>
              <button class="course-chip px-3 py-1 rounded-lg text-xs font-medium border border-slate-200 bg-white hover:bg-slate-50 filter-chip" data-level="Level 2">Level 2</button>
              <button class="course-chip px-3 py-1 rounded-lg text-xs font-medium border border-slate-200 bg-white hover:bg-slate-50 filter-chip" data-level="Core">Core</button>
            </div>
          `;
          titleHeading.parentElement.insertBefore(searchDiv, titleHeading.nextSibling);

          const searchInput = document.getElementById("courseSearchBar");
          const cards = container.querySelectorAll(".grid > div");

          function filterCourses() {{
            const query = searchInput.value.toLowerCase().trim();
            const activeChip = container.querySelector(".course-chip.active")?.getAttribute("data-level") || "all";
            cards.forEach(card => {{
              const text = card.innerText.toLowerCase();
              const matchesQuery = !query || text.includes(query);
              const matchesLevel = activeChip === "all" || text.includes(activeChip.toLowerCase());
              card.style.display = matchesQuery && matchesLevel ? "flex" : "none";
            }});
          }}

          searchInput?.addEventListener("input", filterCourses);
          container.querySelectorAll(".course-chip").forEach(chip => {{
            chip.addEventListener("click", function() {{
              container.querySelectorAll(".course-chip").forEach(c => c.classList.remove("active"));
              this.classList.add("active");
              filterCourses();
            }});
          }});
        }}

        // Clicking course cards
        container.querySelectorAll(".grid > div").forEach(card => {{
          card.addEventListener("click", () => {{
            const cTitle = card.querySelector("h3")?.innerText || "Course";
            const cImg = card.querySelector("img")?.src || "";
            openModal(cTitle, `
              <div class="space-y-3">
                ${{cImg ? `<img src="${{cImg}}" class="w-full h-44 object-cover rounded-xl mb-2">` : ''}}
                <div class="flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 text-xs font-semibold">Active Enrollment</span>
                  <span class="px-2 py-0.5 rounded bg-violet-50 text-violet-700 text-xs font-semibold">Gurugulam Certified</span>
                </div>
                <p class="text-xs text-slate-600">Personalized curriculum module with adaptive milestone assessments, code evaluations, and activity points accreditation.</p>
                <div class="bg-slate-50 p-3 rounded-xl border border-slate-100 text-xs space-y-1">
                  <div class="flex justify-between"><span class="text-slate-500">Assessment Status:</span><span class="font-bold text-slate-800">In Progress</span></div>
                  <div class="flex justify-between"><span class="text-slate-500">Available Practice Tests:</span><span class="font-bold text-slate-800">4 Modules</span></div>
                </div>
              </div>
            `, `
              <button onclick="closeModal()" class="px-4 py-2 rounded-xl text-xs font-medium border border-slate-200 text-slate-600 hover:bg-slate-50">Back</button>
              <button onclick="showToast('Launching course modules...'); closeModal();" class="px-4 py-2 rounded-xl text-xs font-semibold bg-[#7D53F6] text-white hover:opacity-90">Open Course Materials</button>
            `);
          }});
        }});
      }}

      if (viewName === "practice") {{
        // Practice cards search
        const titleArea = container.querySelector(".mb-4");
        if (titleArea && !container.querySelector("#practiceSearchBar")) {{
          const pSearch = document.createElement("div");
          pSearch.className = "w-full my-3";
          pSearch.innerHTML = `
            <div class="relative w-full max-w-sm">
              <i class="bx bx-search absolute left-3 top-2.5 text-slate-400 text-lg"></i>
              <input id="practiceSearchBar" type="text" placeholder="Filter practice courses (e.g. DBMS, Verbal)..." 
                class="w-full pl-9 pr-3 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:outline-primary placeholder:text-slate-400">
            </div>
          `;
          titleArea.appendChild(pSearch);

          const input = document.getElementById("practiceSearchBar");
          const pCards = container.querySelectorAll(".grid > div");
          input?.addEventListener("input", (e) => {{
            const val = e.target.value.toLowerCase().trim();
            pCards.forEach(c => {{
              c.style.display = (!val || c.innerText.toLowerCase().includes(val)) ? "flex" : "none";
            }});
          }});
        }}

        // Practice card clicks
        container.querySelectorAll(".grid > div").forEach(card => {{
          card.addEventListener("click", () => {{
            const pTitle = card.querySelector("h3")?.innerText || "Practice Test";
            const qCount = card.querySelector(".text-sm")?.innerText || "";
            const pPct = card.querySelector(".text-xs")?.innerText || "";
            openModal(pTitle, `
              <div class="space-y-3">
                <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <span class="text-xs font-semibold text-slate-700">${{qCount}}</span>
                  <span class="text-xs font-bold text-primary">${{pPct}} Completed</span>
                </div>
                <p class="text-xs text-slate-600">Practice questions are aligned with company recruitment standards and Technical Assessment frameworks.</p>
                <div class="bg-blue-50 border border-blue-200 p-3 rounded-xl text-blue-800 text-xs">
                  Timed test with automatic code reviewer and test-case verification.
                </div>
              </div>
            `, `
              <button onclick="closeModal()" class="px-4 py-2 rounded-xl text-xs font-medium border border-slate-200 text-slate-600">Cancel</button>
              <button onclick="showToast('Starting assessment environment...'); closeModal();" class="px-4 py-2 rounded-xl text-xs font-semibold bg-[#7D53F6] text-white hover:opacity-90">Start Practice Test</button>
            `);
          }});
        }});
      }}

      if (viewName === "activity" || viewName === "academics") {{
        // Activity card clicks
        container.querySelectorAll(".group").forEach(card => {{
          card.addEventListener("click", () => {{
            const title = card.querySelector("h3")?.innerText || "Activity";
            if (title === "Movement Pass") openMovementPassModal();
            else if (title === "My Leaves") openLeavesModal();
            else {{
              openModal(title, `
                <div class="space-y-3 text-xs">
                  <p class="text-slate-600">You are accessing the <strong>${{title}}</strong> module of the PCDP Student Activity system.</p>
                  <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                    <span class="text-emerald-700 font-semibold">● System Ready</span> · Real-time synchronization active.
                  </div>
                </div>
              `, `
                <button onclick="closeModal()" class="px-4 py-2 rounded-xl text-xs font-medium border border-slate-200 text-slate-600">Close</button>
                <button onclick="showToast('Opening ${{title}}...'); closeModal();" class="px-4 py-2 rounded-xl text-xs font-semibold bg-[#7D53F6] text-white">Proceed</button>
              `);
            }}
          }});
        }});

        // Activity search
        const actSearch = container.querySelector("input[placeholder*='Search activities']");
        if (actSearch) {{
          actSearch.addEventListener("input", (e) => {{
            const val = e.target.value.toLowerCase().trim();
            container.querySelectorAll(".group").forEach(c => {{
              c.style.display = (!val || c.innerText.toLowerCase().includes(val)) ? "block" : "none";
            }});
          }});
        }}
      }}

      if (viewName === "code-review") {{
        const searchInput = container.querySelector("input[placeholder='Search...']");
        const rows = container.querySelectorAll("tbody tr");
        if (searchInput) {{
          searchInput.addEventListener("input", (e) => {{
            const val = e.target.value.toLowerCase().trim();
            rows.forEach(r => {{
              r.style.display = (!val || r.innerText.toLowerCase().includes(val)) ? "" : "none";
            }});
          }});
        }}

        // Code review row clicks
        rows.forEach(row => {{
          row.addEventListener("click", () => {{
            const cells = row.querySelectorAll("td");
            if (cells.length >= 4) {{
              const cName = cells[1].innerText;
              const slot = cells[2].innerText;
              const comment = cells[3].innerText || "No additional reviewer comments recorded.";
              const status = cells[4].innerText;
              openModal(`Review Details: ${{cName}}`, `
                <div class="space-y-3 text-xs">
                  <div class="flex justify-between items-center bg-slate-50 p-3 rounded-xl border border-slate-100">
                    <div>
                      <div class="font-bold text-slate-900">${{cName}}</div>
                      <div class="text-slate-500 mt-0.5">${{slot}}</div>
                    </div>
                    <span class="px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 font-semibold text-[11px]">${{status}}</span>
                  </div>
                  <div>
                    <h5 class="font-bold text-slate-700 uppercase tracking-wider text-[11px] mb-1">Reviewer Feedback:</h5>
                    <div class="bg-amber-50/60 border border-amber-200/80 rounded-xl p-3 text-amber-900 leading-relaxed font-mono">
                      ${{comment}}
                    </div>
                  </div>
                </div>
              `);
            }}
          }});
        }});
      }}
    }}

    // Sidebar navigation clicks
    document.querySelectorAll(".nav-item").forEach(item => {{
      item.addEventListener("click", () => {{
        const target = item.getAttribute("data-nav");
        switchView(target);
      }});
    }});

    // Initialize from URL Hash or default to dashboard
    window.addEventListener("hashchange", () => {{
      const hash = location.hash.replace("#", "") || "dashboard";
      if (hash !== currentView) {{
        switchView(hash);
      }}
    }});

    const initView = location.hash.replace("#", "") || "dashboard";
    switchView(initView);
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated index.html successfully ({len(html_content)} bytes)")
