import json, re

with open("views_data.json", "r", encoding="utf-8") as f:
    views = json.load(f)

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
  <title>PCDP Portal</title>
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
      bottom: 5.5rem;
      right: 1.5rem;
      background: #1e293b;
      color: white;
      padding: 0.75rem 1.25rem;
      border-radius: 0.75rem;
      box-shadow: 0 10px 25px -3px rgba(0,0,0,0.3);
      z-index: 10000;
      opacity: 0;
      transform: translateY(10px);
      transition: all 0.25s ease-in-out;
      pointer-events: none;
      font-size: 0.875rem;
    }}
    .toast-msg.show {{
      opacity: 1;
      transform: translateY(0);
    }}
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(148, 163, 184, 0.4);
      border-radius: 9999px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: rgba(148, 163, 184, 0.7);
    }}
  </style>
</head>
<body class="bg-background text-slate-900 overflow-hidden font-sans">
  <div class="w-screen h-screen flex relative">

    <!-- Mobile Sidebar Drawer Backdrop -->
    <div id="mobileDrawerBackdrop" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40 hidden md:hidden transition-opacity"></div>

    <!-- Sidebar Navigation (Desktop & Mobile Drawer) -->
    <aside id="appSidebar" class="no-print AppSidebar hidden md:flex fixed md:relative z-50 inset-y-0 left-0 w-max min-w-[5.5rem] bg-secondary flex-col items-center p-5 overflow-y-auto transition-transform duration-300">
      <div class="mb-4 flex items-center justify-between w-full md:justify-center">
        <a href="#dashboard" class="flex items-center gap-2">
          <img width="40" src="./assets/images/logo.e99a8edb9e376c3ed2e5.png" alt="logo" class="object-contain hover:scale-105 transition-transform">
        </a>
        <button id="closeMobileSidebar" class="md:hidden text-slate-400 hover:text-white p-1">
          <i class="bx bx-x text-2xl"></i>
        </button>
      </div>

      <!-- Sidebar Menu Items: Evenly distributed matching user layout -->
      <nav class="flex-1 flex flex-col items-center justify-between w-full py-4">
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

        <div data-nav="activity" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all" title="PS Activity / My Leaves">
          <i class="bx bx-collection" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium shadow-md whitespace-nowrap">PS Activity / Leaves</span>
        </div>

        <div data-nav="practice" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all" title="Practice Courses">
          <i class="bx bxs-book-open" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium shadow-md whitespace-nowrap">Practice Courses</span>
        </div>

        <div data-nav="academics" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all" title="Academics">
          <i class="bx bxs-graduation" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium shadow-md whitespace-nowrap">Academics</span>
        </div>

        <div data-nav="code-review" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all" title="Code Review">
          <i class="bx bx-code-alt" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium shadow-md whitespace-nowrap">Code Review</span>
        </div>

        <div data-nav="logout" class="nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-red-600 hover:text-white text-iconColor transition-all" title="Logout">
          <i class="bx bx-log-out" style="font-size: 26px;"></i>
          <span class="hidden md:group-hover:block z-50 fixed ml-[42px] px-3 py-1.5 rounded-lg bg-red-600 text-white text-xs font-medium shadow-md whitespace-nowrap">Logout</span>
        </div>
      </nav>
    </aside>

    <!-- Main Content Container -->
    <main class="flex-1 flex flex-col h-screen w-full overflow-hidden bg-background">
      <!-- Top Navigation Bar matching Video -->
      <header class="no-print w-full bg-white px-4 py-2.5 min-h-[4rem] flex items-center justify-between shadow-sm z-20 border-b border-slate-100">
        <div class="flex gap-4 items-center">
          <button id="mobileMenuBtn" class="text-2xl text-slate-700 hover:text-primary cursor-pointer block md:hidden p-1 rounded-lg focus:outline-none" aria-label="Toggle menu">
            <i class="bx bx-menu text-3xl"></i>
          </button>
          <div class="flex items-center gap-2">
            <span class="font-bold text-lg tracking-tight text-slate-800">PCDP Portal</span>
          </div>
        </div>

        <!-- Student Profile Card matching Video with real photo -->
        <div id="profileBadge" class="flex gap-2.5 items-center bg-[#eff2fe] hover:bg-[#e4e8fc] border border-violet-100/80 py-1 px-2.5 rounded-xl cursor-pointer transition-all select-none">
          <div class="w-8 h-8 rounded-full overflow-hidden bg-[#534AB7] flex items-center justify-center font-bold text-xs shadow-inner">
            <img src="./assets/images/student_avatar.png" alt="Karthikeyan" class="w-full h-full object-cover">
          </div>
          <div class="sm:flex hidden flex-col text-left pr-1">
            <h2 class="text-[11px] font-medium text-slate-500 leading-tight">2024UCS1132</h2>
            <h2 class="text-[13px] font-bold text-slate-900 leading-tight">KARTHIKEYAN S</h2>
          </div>
          <i class="bx bx-chevron-down text-slate-400 text-base hidden sm:block"></i>
        </div>
      </header>

      <!-- Dynamic Page Content -->
      <div id="contentContainer" class="flex-1 w-full overflow-y-auto pb-24 lg:pb-6">
        <!-- Rendered view injected here -->
      </div>
    </main>

    <!-- Floating Global Support / Audio Headphone Button matching Video -->
    <!-- Portal Voice / Students Desk Floating Button at Bottom Right Corner -->
    <button id="globalSupportBtn" class="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-[#7D53F6] hover:bg-[#6c42e6] text-white shadow-2xl flex items-center justify-center hover:scale-110 active:scale-95 transition-all z-50 cursor-pointer border-2 border-white/80" title="Portal Voice / Students Desk">
      <i class="bx bx-headphone text-2xl"></i>
    </button>

    <!-- Floating Mobile Bottom Dock matching Video -->
    <div class="pointer-events-none fixed inset-x-0 bottom-0 z-40 flex justify-center px-3 pb-[max(0.75rem,env(safe-area-inset-bottom))] lg:hidden">
      <div class="pointer-events-auto relative flex max-w-[min(100%,420px)] items-center gap-2.5 rounded-[1.75rem] border border-white/80 bg-white/95 px-3.5 py-2 shadow-[0_12px_40px_rgba(15,23,42,0.18)] backdrop-blur-xl">
        <!-- Dashboard Home Button -->
        <button type="button" data-mobile-nav="dashboard" title="Home" class="flex h-11 w-11 items-center justify-center rounded-2xl transition-transform active:scale-90" style="background-color: rgba(125, 83, 246, 0.12); color: rgb(125, 83, 246);">
          <i class="bx bxs-home text-[22px]"></i>
        </button>
        <!-- Courses Available Button -->
        <button type="button" data-mobile-nav="courses" title="Courses Available" class="flex h-11 w-11 items-center justify-center rounded-2xl transition-transform active:scale-90" style="background-color: rgb(225, 245, 238); color: rgb(15, 110, 86);">
          <i class="bx bxs-report text-[22px]"></i>
        </button>
        <!-- Practice Courses Button -->
        <button type="button" data-mobile-nav="practice" title="Practice Courses" class="flex h-11 w-11 items-center justify-center rounded-2xl transition-transform active:scale-90" style="background-color: rgb(230, 241, 251); color: rgb(24, 95, 165);">
          <i class="bx bx-walk text-[22px]"></i>
        </button>
        <!-- PS Activity / More Button with dashed border -->
        <button type="button" data-mobile-nav="activity" title="PS Activity & Tools" class="flex h-11 w-11 items-center justify-center rounded-2xl border border-dashed bg-white active:scale-90" style="border-color: rgba(125, 83, 246, 0.5); color: rgb(125, 83, 246);">
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
      <div id="modalBody" class="p-5 text-slate-600 text-sm leading-relaxed max-h-[75vh] overflow-y-auto">
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

    // Full Leaves Dataset matching Video (31 entries)
    const DEFAULT_LEAVES = [
      {{
        id: 1,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Oct 1, 2026",
        fromTime: "04:30 PM",
        toDate: "Oct 5, 2026",
        toTime: "08:40 AM",
        gateOut: "Oct 1, 2026, 05:10 PM",
        gateIn: "Oct 4, 2026, 07:52 PM",
        duration: "4 days",
        remarks: "Leave",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 2,
        leaveType: "GP",
        type: "Leave",
        fromDate: "Sep 24, 2026",
        fromTime: "12:30 PM",
        toDate: "Sep 30, 2026",
        toTime: "08:30 AM",
        gateOut: "Sep 24, 2026, 02:38 PM",
        gateIn: "Sep 29, 2026, 08:44 PM",
        duration: "6 days",
        remarks: "GP",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 3,
        leaveType: "Sick Leave",
        type: "Leave",
        fromDate: "Sep 23, 2026",
        fromTime: "01:00 PM",
        toDate: "Sep 23, 2026",
        toTime: "04:30 PM",
        gateOut: "-",
        gateIn: "-",
        duration: "1 day",
        remarks: "Stomach upset",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 4,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Sep 12, 2026",
        fromTime: "04:30 PM",
        toDate: "Sep 15, 2026",
        toTime: "08:30 AM",
        gateOut: "Sep 12, 2026, 05:00 PM",
        gateIn: "Sep 15, 2026, 07:46 AM",
        duration: "3 days",
        remarks: "Leave",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 5,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Aug 22, 2026",
        fromTime: "04:30 PM",
        toDate: "Aug 28, 2026",
        toTime: "08:30 AM",
        gateOut: "Aug 22, 2026, 05:15 PM",
        gateIn: "Aug 28, 2026, 07:22 AM",
        duration: "6 days",
        remarks: "Leave",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 6,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Aug 12, 2026",
        fromTime: "04:30 PM",
        toDate: "Aug 17, 2026",
        toTime: "08:30 AM",
        gateOut: "Aug 12, 2026, 05:20 PM",
        gateIn: "Aug 16, 2026, 07:06 PM",
        duration: "6 days",
        remarks: "Leave",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 7,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Aug 12, 2026",
        fromTime: "04:30 PM",
        toDate: "Aug 13, 2026",
        toTime: "08:30 AM",
        gateOut: "-",
        gateIn: "-",
        duration: "2 days",
        remarks: "Leave",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }}
      }},
      {{
        id: 8,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Aug 9, 2026",
        fromTime: "08:30 AM",
        toDate: "Aug 9, 2026",
        toTime: "06:00 PM",
        gateOut: "Aug 9, 2026, 09:10 AM",
        gateIn: "Aug 9, 2026, 03:41 PM",
        duration: "1 day",
        remarks: "Leave",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 9,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Aug 8, 2026",
        fromTime: "04:30 PM",
        toDate: "Aug 10, 2026",
        toTime: "08:30 AM",
        gateOut: "-",
        gateIn: "-",
        duration: "2 days",
        remarks: "Leave",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }}
      }},
      {{
        id: 10,
        leaveType: "Sick Leave",
        type: "Leave",
        fromDate: "Aug 6, 2026",
        fromTime: "08:30 AM",
        toDate: "Aug 6, 2026",
        toTime: "04:30 PM",
        gateOut: "-",
        gateIn: "-",
        duration: "1 day",
        remarks: "Fever",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 11,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Jul 26, 2026",
        fromTime: "04:30 PM",
        toDate: "Jul 30, 2026",
        toTime: "08:30 AM",
        gateOut: "Jul 26, 2026, 05:00 PM",
        gateIn: "Jul 29, 2026, 08:15 PM",
        duration: "4 days",
        remarks: "Home visit",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 12,
        leaveType: "GP",
        type: "Leave",
        fromDate: "Jul 18, 2026",
        fromTime: "01:00 PM",
        toDate: "Jul 18, 2026",
        toTime: "07:30 PM",
        gateOut: "Jul 18, 2026, 01:10 PM",
        gateIn: "Jul 18, 2026, 06:40 PM",
        duration: "1 day",
        remarks: "Outing",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 13,
        leaveType: "OnDuty - NPTEL Exam",
        type: "Leave",
        fromDate: "Jul 10, 2026",
        fromTime: "08:00 AM",
        toDate: "Jul 10, 2026",
        toTime: "06:00 PM",
        gateOut: "Jul 10, 2026, 08:15 AM",
        gateIn: "Jul 10, 2026, 05:20 PM",
        duration: "1 day",
        remarks: "Exam Center: Coimbatore",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 14,
        leaveType: "Sick Leave",
        type: "Leave",
        fromDate: "Jun 28, 2026",
        fromTime: "09:00 AM",
        toDate: "Jun 28, 2026",
        toTime: "04:30 PM",
        gateOut: "-",
        gateIn: "-",
        duration: "1 day",
        remarks: "Severe headache",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 15,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Jun 15, 2026",
        fromTime: "04:30 PM",
        toDate: "Jun 20, 2026",
        toTime: "08:30 AM",
        gateOut: "Jun 15, 2026, 05:10 PM",
        gateIn: "Jun 19, 2026, 08:30 PM",
        duration: "5 days",
        remarks: "Leave",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 16,
        leaveType: "GP",
        type: "Leave",
        fromDate: "Jun 05, 2026",
        fromTime: "02:00 PM",
        toDate: "Jun 05, 2026",
        toTime: "08:00 PM",
        gateOut: "Jun 05, 2026, 02:15 PM",
        gateIn: "Jun 05, 2026, 07:45 PM",
        duration: "1 day",
        remarks: "GP Outing",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 17,
        leaveType: "Emergency Leave",
        type: "Leave",
        fromDate: "May 20, 2026",
        fromTime: "11:00 AM",
        toDate: "May 24, 2026",
        toTime: "08:30 AM",
        gateOut: "May 20, 2026, 11:45 AM",
        gateIn: "May 23, 2026, 07:15 PM",
        duration: "4 days",
        remarks: "Family emergency",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 18,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "May 10, 2026",
        fromTime: "04:30 PM",
        toDate: "May 12, 2026",
        toTime: "08:30 AM",
        gateOut: "-",
        gateIn: "-",
        duration: "2 days",
        remarks: "Personal",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }}
      }},
      {{
        id: 19,
        leaveType: "OnDuty - Sports",
        type: "Leave",
        fromDate: "Apr 25, 2026",
        fromTime: "07:00 AM",
        toDate: "Apr 26, 2026",
        toTime: "08:00 PM",
        gateOut: "Apr 25, 2026, 07:15 AM",
        gateIn: "Apr 26, 2026, 07:30 PM",
        duration: "2 days",
        remarks: "Zonal Tournament",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 20,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Apr 12, 2026",
        fromTime: "04:30 PM",
        toDate: "Apr 16, 2026",
        toTime: "08:30 AM",
        gateOut: "Apr 12, 2026, 05:00 PM",
        gateIn: "Apr 15, 2026, 08:20 PM",
        duration: "4 days",
        remarks: "Tamil New Year Holiday",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 21,
        leaveType: "Sick Leave",
        type: "Leave",
        fromDate: "Apr 02, 2026",
        fromTime: "09:00 AM",
        toDate: "Apr 02, 2026",
        toTime: "05:00 PM",
        gateOut: "-",
        gateIn: "-",
        duration: "1 day",
        remarks: "Clinic rest",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 22,
        leaveType: "GP",
        type: "Leave",
        fromDate: "Mar 22, 2026",
        fromTime: "01:30 PM",
        toDate: "Mar 22, 2026",
        toTime: "07:30 PM",
        gateOut: "Mar 22, 2026, 01:45 PM",
        gateIn: "Mar 22, 2026, 07:10 PM",
        duration: "1 day",
        remarks: "GP Outing",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 23,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Mar 10, 2026",
        fromTime: "04:30 PM",
        toDate: "Mar 14, 2026",
        toTime: "08:30 AM",
        gateOut: "Mar 10, 2026, 05:10 PM",
        gateIn: "Mar 13, 2026, 07:50 PM",
        duration: "4 days",
        remarks: "Leave",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 24,
        leaveType: "OnDuty - Offcampus Placement",
        type: "Leave",
        fromDate: "Feb 27, 2026",
        fromTime: "07:30 AM",
        toDate: "Feb 28, 2026",
        toTime: "06:30 PM",
        gateOut: "Feb 27, 2026, 07:45 AM",
        gateIn: "Feb 28, 2026, 06:15 PM",
        duration: "2 days",
        remarks: "Hackathon Finals",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 25,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Feb 14, 2026",
        fromTime: "04:30 PM",
        toDate: "Feb 17, 2026",
        toTime: "08:30 AM",
        gateOut: "Feb 14, 2026, 05:20 PM",
        gateIn: "Feb 16, 2026, 08:10 PM",
        duration: "3 days",
        remarks: "Leave",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 26,
        leaveType: "Sick Leave",
        type: "Leave",
        fromDate: "Feb 05, 2026",
        fromTime: "08:30 AM",
        toDate: "Feb 05, 2026",
        toTime: "04:30 PM",
        gateOut: "-",
        gateIn: "-",
        duration: "1 day",
        remarks: "Dental appointment",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 27,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Jan 24, 2026",
        fromTime: "04:30 PM",
        toDate: "Jan 27, 2026",
        toTime: "08:30 AM",
        gateOut: "Jan 24, 2026, 05:05 PM",
        gateIn: "Jan 26, 2026, 07:40 PM",
        duration: "3 days",
        remarks: "Republic Day Long Weekend",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 28,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Jan 12, 2026",
        fromTime: "04:30 PM",
        toDate: "Jan 19, 2026",
        toTime: "08:30 AM",
        gateOut: "Jan 12, 2026, 05:15 PM",
        gateIn: "Jan 18, 2026, 08:30 PM",
        duration: "7 days",
        remarks: "Pongal Vacation",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 29,
        leaveType: "GP",
        type: "Leave",
        fromDate: "Jan 03, 2026",
        fromTime: "01:00 PM",
        toDate: "Jan 03, 2026",
        toTime: "07:00 PM",
        gateOut: "Jan 03, 2026, 01:15 PM",
        gateIn: "Jan 03, 2026, 06:50 PM",
        duration: "1 day",
        remarks: "Shopping",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 30,
        leaveType: "Leave",
        type: "Leave",
        fromDate: "Dec 23, 2025",
        fromTime: "04:30 PM",
        toDate: "Dec 28, 2025",
        toTime: "08:30 AM",
        gateOut: "Dec 23, 2025, 05:00 PM",
        gateIn: "Dec 27, 2025, 07:30 PM",
        duration: "5 days",
        remarks: "Winter break",
        parentStatus: "Approved",
        status: "Approved",
        mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }},
      {{
        id: 31,
        leaveType: "Sick Leave",
        type: "Leave",
        fromDate: "Dec 10, 2025",
        fromTime: "08:30 AM",
        toDate: "Dec 10, 2025",
        toTime: "04:30 PM",
        gateOut: "-",
        gateIn: "-",
        duration: "1 day",
        remarks: "Cold & viral fever",
        parentStatus: "Approved",
        status: "Approved",
        warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
      }}
    ];


    const STORAGE_KEY = "pcdp_leaves_records_v3";
    let leavesData = [];
    try {{
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {{
        leavesData = JSON.parse(stored);
      }}
    }} catch(e) {{
      console.error("Error loading stored leaves:", e);
    }}
    if (!leavesData || !Array.isArray(leavesData) || leavesData.length === 0) {{
      leavesData = DEFAULT_LEAVES;
      try {{
        localStorage.setItem(STORAGE_KEY, JSON.stringify(leavesData));
      }} catch(e) {{}}
    }}
        let leavesCurrentPage = 1;
    let leavesPageSize = 10;
    let leavesSearchFilter = "";

    // Code Review Rubric Database matching Video (Frames 55 & 36)
    const reviewData = {{
      "HTML / CSS - Level 1": {{
        slot: "06 Jan 2026 (01:30 pm - 03:20 pm)",
        justification: "grid layout little bit different , media query not applied",
        rubrics: [
          {{ label: "Code Quality", score: "30/40" }},
          {{ label: "Key Requirements", score: "20/25" }},
          {{ label: "Expected Output", score: "30/35" }}
        ]
      }},
      "Programming C++ - Level 3": {{
        slot: "10 Aug 2026 (11:20 am - 12:20 pm)",
        justification: "The program works for most cases, but the logic for handling duplicate scores needs correction. While determining the first, second, and third largest values, duplicate elements must be ignored. Ensure that ranking is based only on distinct values, so repeated scores do not occupy multiple ranking positions.",
        rubrics: [
          {{ label: "Pass Mark", score: "0/50" }}
        ]
      }},
      "Java Script - Level 1": {{
        slot: "05 Mar 2026 (08:45 am - 10:25 am)",
        justification: "All DOM manipulation test cases passed. Excellent logic structure and clean variable naming conventions.",
        rubrics: [
          {{ label: "Code Quality", score: "35/40" }},
          {{ label: "Key Requirements", score: "25/25" }},
          {{ label: "Expected Output", score: "35/35" }}
        ]
      }},
      "Programming C++ Level - 1": {{
        slot: "17 Feb 2026 (01:30 pm - 02:40 pm)",
        justification: "Output not printed properly for cases where the cost exceeds 30.",
        rubrics: [
          {{ label: "Code Quality", score: "25/40" }},
          {{ label: "Key Requirements", score: "20/25" }},
          {{ label: "Expected Output", score: "15/35" }}
        ]
      }},
      "C Programming Level - 4": {{
        slot: "03 Mar 2025 (10:30 am - 11:30 am)",
        justification: "Reverse logic not working for rounded sum(i.e 30,50)",
        rubrics: [
          {{ label: "Code Quality", score: "20/40" }},
          {{ label: "Key Requirements", score: "18/25" }},
          {{ label: "Expected Output", score: "22/35" }}
        ]
      }}
    }};

    // Modal Controller
    const modal = document.getElementById("portalModal");
    const modalTitle = document.getElementById("modalTitle");
    const modalBody = document.getElementById("modalBody");
    const modalFooter = document.getElementById("modalFooter");
    const modalCloseBtn = document.getElementById("modalCloseBtn");

    function openModal(title, contentHtml, footerHtml = null) {{
      modalTitle.innerText = title;
      modalBody.innerHTML = contentHtml;
      if (footerHtml === false) {{
        modalFooter.style.display = "none";
      }} else {{
        modalFooter.style.display = "flex";
        if (footerHtml !== null) {{
          modalFooter.innerHTML = footerHtml;
        }} else {{
          modalFooter.innerHTML = '<button onclick="closeModal()" class="w-full py-2.5 rounded-xl font-semibold bg-[#7D53F6] hover:bg-[#6c42e6] text-white text-sm transition-all shadow-sm">Close</button>';
        }}
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
      setTimeout(() => toast.classList.remove("show"), 3200);
    }}

    // Portal Voice / Students Desk Floating Button Handler
    document.getElementById("globalSupportBtn")?.addEventListener("click", () => {{
      openModal("Portal Voice / Students Desk", `
        <div class="space-y-4 text-xs text-slate-600">
          <div class="flex items-center gap-3.5 p-3.5 bg-violet-50 rounded-2xl border border-violet-100">
            <div class="w-12 h-12 rounded-2xl bg-[#7D53F6] text-white flex items-center justify-center text-2xl shadow-md">
              <i class="bx bx-headphone"></i>
            </div>
            <div>
              <h4 class="font-bold text-slate-900 text-sm">Portal Voice & Students Desk</h4>
              <p class="text-[11px] text-slate-500">24/7 Student Grievance & Academic Support</p>
            </div>
          </div>
          <div class="space-y-2.5 border-t border-slate-100 pt-3 text-xs">
            <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100">
              <span class="font-medium text-slate-700">Hostel Care Desk:</span>
              <span class="font-mono text-primary font-bold">Ext: 4402 / 4405</span>
            </div>
            <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100">
              <span class="font-medium text-slate-700">PCDP Assessment Help:</span>
              <span class="font-mono text-primary font-bold">pcdp-support@bitsathy.ac.in</span>
            </div>
            <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100">
              <span class="font-medium text-slate-700">Assigned Faculty Mentor:</span>
              <span class="font-medium text-slate-800">CS10789 - Dhivya P</span>
            </div>
            <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100">
              <span class="font-medium text-slate-700">Chief Hostel Warden:</span>
              <span class="font-medium text-slate-800">ME11077 - josephsilvester</span>
            </div>
          </div>
        </div>
      `, `
        <button onclick="closeModal()" class="w-full py-2.5 rounded-xl font-semibold bg-[#7D53F6] hover:bg-[#6c42e6] text-white text-sm transition-all shadow-sm cursor-pointer">Close</button>
      `);
    }});

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

    // Profile Click Popup - Exact User Profile Modal matching reference screenshot
    document.getElementById("profileBadge")?.addEventListener("click", () => {{
      openModal("User Profile", `
        <div class="flex flex-col items-center justify-center pt-2 pb-2">
          <!-- Circular Profile Photo with outer soft ring matching uploaded screenshot -->
          <div class="w-48 h-48 sm:w-56 sm:h-56 rounded-full p-2 bg-gradient-to-b from-blue-50/70 to-violet-50/50 border border-slate-200/60 shadow-sm flex items-center justify-center mb-6">
            <div class="w-full h-full rounded-full overflow-hidden bg-white shadow-inner flex items-center justify-center">
              <img src="./assets/images/student_avatar.png" alt="KARTHIKEYAN S" class="w-full h-full object-cover">
            </div>
          </div>

          <!-- User Details Table matching uploaded layout -->
          <div class="w-full max-w-md space-y-0 text-sm font-sans divide-y divide-slate-100 border-t border-slate-100">
            <div class="flex items-center py-3 px-1">
              <span class="w-32 font-bold text-slate-800 text-sm tracking-tight">Id</span>
              <span class="text-slate-600 font-medium text-sm">2024UCS1132</span>
            </div>
            <div class="flex items-center py-3 px-1">
              <span class="w-32 font-bold text-slate-800 text-sm tracking-tight">User Id</span>
              <span class="text-slate-600 font-medium text-sm">7376241CS231</span>
            </div>
            <div class="flex items-center py-3 px-1">
              <span class="w-32 font-bold text-slate-800 text-sm tracking-tight">Name</span>
              <span class="text-slate-800 font-medium text-sm uppercase tracking-wide">KARTHIKEYAN S</span>
            </div>
          </div>

          <!-- Full Width Purple Close Button matching uploaded screenshot -->
          <div class="w-full max-w-md mt-6">
            <button onclick="closeModal()" type="button" class="w-full py-3 rounded-xl font-semibold bg-[#7D53F6] hover:bg-[#6c42e6] text-white text-base shadow-sm transition-all text-center cursor-pointer">
              Close
            </button>
          </div>
        </div>
      `, false);
    }});

    // Mobile Bottom Dock Navigation
    document.querySelectorAll("[data-mobile-nav]").forEach(btn => {{
      btn.addEventListener("click", () => {{
        const target = btn.getAttribute("data-mobile-nav");
        switchView(target);
      }});
    }});

    // Quick Modals
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
              <div class="text-2xl font-bold text-[#534AB7]">47,730</div>
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
                <div class="flex justify-between mb-1"><span class="text-slate-600">Weekly Assessments & Practice</span><span class="font-bold text-slate-800">16,240 pts</span></div>
                <div class="w-full bg-slate-100 rounded-full h-2"><div class="bg-violet-500 h-2 rounded-full" style="width: 34%"></div></div>
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
          </div>
        </div>
      `);
    }}

    function openResponsiveBreakdown() {{
      openModal("Responsive Score Breakdown", `
        <div class="space-y-4">
          <div class="flex items-center justify-between p-4 rounded-xl" style="background: rgb(225, 245, 238);">
            <div>
              <div class="text-2xl font-bold" style="color: rgb(15, 110, 86);">84 / 100</div>
              <div class="text-xs font-semibold" style="color: rgb(15, 110, 86);">Platform Responsiveness Score</div>
            </div>
            <span class="text-xs font-bold px-2 py-1 rounded bg-emerald-600 text-white">Top 10%</span>
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

    // ==========================================
    // LEAVES SYSTEM (Exact Video Replication)
    // ==========================================
    function getStatusBadge(status) {{
      if (status === "Rejected") {{
        return `<span class="bg-[#ef4444] text-white text-[11px] px-3 py-0.5 rounded-full font-semibold shadow-sm inline-block">Rejected</span>`;
      }}
      if (status === "Pending") {{
        return `<span class="bg-[#f59e0b] text-white text-[11px] px-3 py-0.5 rounded-full font-semibold shadow-sm inline-block">Pending</span>`;
      }}
      return `<span class="bg-[#16a34a] text-white text-[11px] px-3 py-0.5 rounded-full font-semibold shadow-sm inline-block">Approved</span>`;
    }}

    function getParentStatusBadge(status) {{
      if (status === "Pending") {{
        return `<span class="bg-[#f59e0b] text-white text-[11px] px-3 py-0.5 rounded-full font-semibold shadow-sm inline-block">Pending</span>`;
      }}
      return `<span class="bg-[#16a34a] text-white text-[11px] px-3 py-0.5 rounded-full font-semibold shadow-sm inline-block">Approved</span>`;
    }}

    function renderLeavesTable() {{
      const tbody = document.getElementById("leavesTableBody");
      if (!tbody) return;

      const q = leavesSearchFilter.toLowerCase().trim();
      const filtered = leavesData.filter(l => {{
        if (!q) return true;
        return l.leaveType.toLowerCase().includes(q) ||
               l.remarks.toLowerCase().includes(q) ||
               l.status.toLowerCase().includes(q) ||
               l.duration.toLowerCase().includes(q);
      }});

      const totalItems = filtered.length;
      const totalPages = Math.max(1, Math.ceil(totalItems / leavesPageSize));
      if (leavesCurrentPage > totalPages) leavesCurrentPage = totalPages;

      const startIdx = (leavesCurrentPage - 1) * leavesPageSize;
      const endIdx = Math.min(startIdx + leavesPageSize, totalItems);
      const pageSlice = filtered.slice(startIdx, endIdx);

      if (pageSlice.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="7" class="text-center py-10 text-slate-400 text-sm">No leave records match your search criteria.</td></tr>`;
      }} else {{
        tbody.innerHTML = pageSlice.map(leave => `
          <tr class="hover:bg-slate-50/80 transition-colors cursor-pointer leave-row" data-id="${{leave.id}}">
            <td class="py-3 px-4 font-medium text-slate-800 flex items-center gap-1.5 whitespace-nowrap">
              <i class="bx bx-chevron-right text-slate-400 text-base"></i>
              <span>${{leave.leaveType}}</span>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <span class="bg-[#0284c7] text-white text-[11px] px-3 py-0.5 rounded-full font-semibold shadow-sm inline-block">${{leave.type}}</span>
            </td>
            <td class="py-3 px-4 text-slate-700 whitespace-nowrap font-medium">${{leave.fromDate}}</td>
            <td class="py-3 px-4 text-slate-700 whitespace-nowrap font-medium">
              <div>${{leave.toDate}}</div>
              ${{leave.gateIn && leave.gateIn !== '-' ? `<div class="text-[11px] text-slate-400 font-normal">(Gate In: ${{leave.gateIn}})</div>` : ''}}
            </td>
            <td class="py-3 px-4 text-slate-600 whitespace-nowrap font-medium">${{leave.duration}}</td>
            <td class="py-3 px-4 text-slate-700 whitespace-nowrap font-medium">${{leave.remarks}}</td>
            <td class="py-3 px-4 text-center whitespace-nowrap">${{getStatusBadge(leave.status)}}</td>
          </tr>
        `).join("");
      }}

      // Count label matching Video
      const countLabel = document.getElementById("leavesCountLabel");
      if (countLabel) {{
        if (totalItems === 0) {{
          countLabel.innerText = "Showing 0 of 0 entries";
        }} else {{
          countLabel.innerText = `Showing ${{startIdx + 1}} to ${{endIdx}} of ${{totalItems}} entries`;
        }}
      }}

      // Pagination buttons matching Video
      const paginContainer = document.getElementById("leavesPaginationButtons");
      if (paginContainer) {{
        let paginHtml = `
          <button id="prevLeavesPage" ${{leavesCurrentPage <= 1 ? 'disabled' : ''}} class="px-2.5 py-1 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-600 disabled:opacity-40 disabled:cursor-not-allowed">Previous</button>
        `;

        for (let p = 1; p <= totalPages; p++) {{
          if (p === leavesCurrentPage) {{
            paginHtml += `<button class="w-7 h-7 rounded-lg bg-[#5b50e6] text-white font-bold text-xs shadow-sm">${{p}}</button>`;
          }} else {{
            paginHtml += `<button data-page="${{p}}" class="w-7 h-7 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 font-medium text-xs leaves-page-btn">${{p}}</button>`;
          }}
        }}

        paginHtml += `
          <button id="nextLeavesPage" ${{leavesCurrentPage >= totalPages ? 'disabled' : ''}} class="px-2.5 py-1 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-600 disabled:opacity-40 disabled:cursor-not-allowed">Next</button>
        `;

        paginContainer.innerHTML = paginHtml;

        document.getElementById("prevLeavesPage")?.addEventListener("click", () => {{
          if (leavesCurrentPage > 1) {{
            leavesCurrentPage--;
            renderLeavesTable();
          }}
        }});

        document.getElementById("nextLeavesPage")?.addEventListener("click", () => {{
          if (leavesCurrentPage < totalPages) {{
            leavesCurrentPage++;
            renderLeavesTable();
          }}
        }});

        paginContainer.querySelectorAll(".leaves-page-btn").forEach(btn => {{
          btn.addEventListener("click", () => {{
            leavesCurrentPage = Number(btn.getAttribute("data-page"));
            renderLeavesTable();
          }});
        }});
      }}

      // Attach row click to open Leave Details Modal matching Frame 32 & 22
      tbody.querySelectorAll(".leave-row").forEach(row => {{
        row.addEventListener("click", () => {{
          const id = Number(row.getAttribute("data-id"));
          const item = leavesData.find(l => l.id === id);
          if (item) openLeaveDetailsModal(item);
        }});
      }});
    }}

    // Open Leave Details Modal matching Frame 32 & 22
    function openLeaveDetailsModal(leave) {{
      let approvalHtml = '';
      if (leave.status === "Pending") {{
        approvalHtml = `
          <div class="text-center py-6 text-slate-500">
            <i class="bx bx-time text-4xl text-slate-400 mb-2 inline-block animate-pulse"></i>
            <p class="text-xs font-medium text-slate-600">Approval workflow is being processed...</p>
          </div>
        `;
      }} else {{
        const wardenCard = leave.warden ? `
          <div class="border border-slate-200/90 rounded-2xl p-4 bg-white shadow-sm space-y-1">
            <div class="flex items-center justify-between mb-1">
              <span class="font-bold text-slate-800 text-sm">Hostel Warden</span>
              <span class="${{leave.warden.status === 'Approved' ? 'bg-[#16a34a]' : 'bg-[#ef4444]'}} text-white text-[11px] px-3 py-0.5 rounded-full font-semibold shadow-sm">${{leave.warden.status}}</span>
            </div>
            <div class="text-xs text-slate-500 font-medium">${{leave.warden.name}}</div>
            <div class="text-xs text-slate-700 font-semibold pt-1">Approved by: <span class="font-normal text-slate-600">${{leave.warden.name}}</span></div>
          </div>
        ` : '';

        const mentorCard = leave.mentor ? `
          <div class="border border-slate-200/90 rounded-2xl p-4 bg-white shadow-sm space-y-1">
            <div class="flex items-center justify-between mb-1">
              <span class="font-bold text-slate-800 text-sm">Mentor</span>
              <span class="${{leave.mentor.status === 'Approved' ? 'bg-[#16a34a]' : 'bg-[#ef4444]'}} text-white text-[11px] px-3 py-0.5 rounded-full font-semibold shadow-sm">${{leave.mentor.status}}</span>
            </div>
            <div class="text-xs text-slate-500 font-medium">${{leave.mentor.name}}</div>
            <div class="text-xs text-slate-700 font-semibold pt-1">Approved by: <span class="font-normal text-slate-600">${{leave.mentor.name}}</span></div>
          </div>
        ` : '';

        approvalHtml = `
          <div class="space-y-2.5">
            ${{wardenCard}}
            ${{mentorCard}}
          </div>
        `;
      }}

      const content = `
        <div class="space-y-4">
          <!-- Leave Information Subtitle -->
          <h4 class="text-sm font-bold text-slate-800 tracking-tight">Leave Information</h4>

          <!-- Two-column grid matching Frame 32 -->
          <div class="grid grid-cols-2 gap-y-3.5 gap-x-6 text-xs">
            <div>
              <span class="text-slate-500 block mb-0.5">Leave Type</span>
              <span class="font-semibold text-slate-800 text-sm">${{leave.leaveType}}</span>
            </div>
            <div>
              <span class="text-slate-500 block mb-0.5">Type</span>
              <span class="bg-[#7D53F6] text-white text-[11px] px-3 py-0.5 rounded-full font-semibold shadow-sm inline-block">${{leave.type}}</span>
            </div>

            <div>
              <span class="text-slate-500 block mb-0.5">From Date</span>
              <span class="font-medium text-slate-800">${{leave.fromDate}}, ${{leave.fromTime}}</span>
            </div>
            <div>
              <span class="text-slate-500 block mb-0.5">To Date</span>
              <span class="font-medium text-slate-800">${{leave.toDate}}, ${{leave.toTime}}</span>
            </div>

            <div>
              <span class="text-slate-500 block mb-0.5">Gate Out</span>
              <span class="font-medium text-slate-800">${{leave.gateOut}}</span>
            </div>
            <div>
              <span class="text-slate-500 block mb-0.5">Gate In</span>
              <span class="font-medium text-slate-800">${{leave.gateIn}}</span>
            </div>

            <div>
              <span class="text-slate-500 block mb-0.5">Duration</span>
              <span class="font-medium text-slate-800">${{leave.duration}}</span>
            </div>
            <div>
              <span class="text-slate-500 block mb-0.5">Status</span>
              <span class="${{leave.status === 'Approved' || leave.status === 'Completed' ? 'bg-[#16a34a]' : (leave.status === 'Rejected' ? 'bg-[#ef4444]' : 'bg-[#f59e0b]')}} text-white text-[11px] px-3 py-0.5 rounded-full font-semibold shadow-sm inline-block">${{leave.status}}</span>
            </div>

            <div class="col-span-2">
              <span class="text-slate-500 block mb-0.5">Remarks</span>
              <span class="font-semibold text-slate-800">${{leave.remarks}}</span>
            </div>
          </div>

          <!-- Approval Status Section -->
          <div class="pt-2">
            <h4 class="text-sm font-bold text-slate-800 tracking-tight mb-2.5">Approval Status</h4>
            ${{approvalHtml}}
          </div>
        </div>
      `;

      openModal(`Leave Details - ${{leave.leaveType}}`, content, `
        <button onclick="closeModal()" class="w-full py-2.5 rounded-xl font-semibold bg-[#7D53F6] hover:bg-[#6c42e6] text-white text-sm transition-all shadow-sm">Close</button>
      `);
    }}

    // Open Working Apply for Leave Form Modal matching Reference Video exactly
    function openApplyLeaveModal() {{
      const now = new Date();
      const pad = (n) => String(n).padStart(2, '0');
      const todayIso = `${{now.getFullYear()}}-${{pad(now.getMonth()+1)}}-${{pad(now.getDate())}}T09:00`;
      const nextDate = new Date(now.getTime() + 4 * 24 * 60 * 60 * 1000);
      const nextIso = `${{nextDate.getFullYear()}}-${{pad(nextDate.getMonth()+1)}}-${{pad(nextDate.getDate())}}T17:00`;

      const content = `
        <form id="applyLeaveForm" class="space-y-4 text-xs font-sans" onsubmit="return false;">
          <div>
            <label class="block font-semibold text-slate-700 mb-1.5 text-xs">Leave Type</label>
            <div class="relative">
              <select id="formLeaveType" class="w-full px-3.5 py-2.5 bg-[#f0f4f9] border border-slate-200 focus:border-[#7D53F6] rounded-xl text-xs sm:text-sm font-medium text-slate-800 focus:outline-none appearance-none cursor-pointer pr-10">
                <option value="Sick Leave">Sick Leave</option>
                <option value="Emergency Leave">Emergency Leave</option>
                <option value="OnDuty - Events">OnDuty - Events</option>
                <option value="OnDuty - Project Competition">OnDuty - Project Competition</option>
                <option value="OnDuty - Internship">OnDuty - Internship</option>
                <option value="OnDuty - Paper Presenation">OnDuty - Paper Presenation</option>
                <option value="OnDuty - Technical Competition">OnDuty - Technical Competition</option>
                <option value="OnDuty - NSS/NCC">OnDuty - NSS/NCC</option>
                <option value="OnDuty - Sports">OnDuty - Sports</option>
                <option value="OnDuty - NPTEL Exam">OnDuty - NPTEL Exam</option>
                <option value="OnDuty - Offcampus Placement">OnDuty - Offcampus Placement</option>
                <option value="Onduty - Training Course">Onduty - Training Course</option>
                <option value="Onduty - Govt Exams">Onduty - Govt Exams</option>
                <option value="GP">GP</option>
                <option value="Leave" selected>Leave</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-slate-400">
                <div class="h-4 w-[1px] bg-slate-300 mr-2.5"></div>
                <i class="bx bx-chevron-down text-xl text-slate-500"></i>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3.5">
            <div>
              <label class="block font-semibold text-slate-700 mb-1.5 text-xs">From Date</label>
              <input type="datetime-local" id="formFromDate" value="${{todayIso}}" class="w-full px-3 py-2 bg-[#f0f4f9] border border-slate-200 rounded-xl text-xs text-slate-800 font-medium focus:outline-none focus:border-[#7D53F6]">
            </div>
            <div>
              <label class="block font-semibold text-slate-700 mb-1.5 text-xs">To Date</label>
              <input type="datetime-local" id="formToDate" value="${{nextIso}}" class="w-full px-3 py-2 bg-[#f0f4f9] border border-slate-200 rounded-xl text-xs text-slate-800 font-medium focus:outline-none focus:border-[#7D53F6]">
            </div>
          </div>

          <div>
            <label class="block font-semibold text-slate-700 mb-1.5 text-xs">Remarks</label>
            <input type="text" id="formRemarks" placeholder="Enter reason for leave" class="w-full px-3.5 py-2.5 bg-[#f0f4f9] border border-slate-200 focus:border-[#7D53F6] rounded-xl text-xs text-slate-800 placeholder:text-slate-400 focus:outline-none font-medium">
          </div>
        </form>
      `;

      openModal("Apply for Leave", content, `
        <div class="w-full grid grid-cols-2 gap-3">
          <button onclick="closeModal()" type="button" class="w-full py-3 rounded-xl font-bold bg-[#ff5c5c] hover:bg-[#ff4747] text-white text-sm shadow-sm transition-all text-center cursor-pointer">Cancel</button>
          <button id="submitLeaveBtn" type="button" class="w-full py-2.5 rounded-xl font-bold bg-[#7452fc] hover:bg-[#633ff0] text-white text-xs sm:text-sm leading-tight shadow-sm transition-all text-center flex items-center justify-center cursor-pointer"><span>Submit Leave<br class="sm:hidden"> Request</span></button>
        </div>
      `);

      // Handle Submit with automatic approval and backend localStorage persistence
      document.getElementById("submitLeaveBtn")?.addEventListener("click", () => {{
        const leaveType = document.getElementById("formLeaveType")?.value || "Leave";
        const fromVal = document.getElementById("formFromDate")?.value || todayIso;
        const toVal = document.getElementById("formToDate")?.value || nextIso;
        const remarksVal = document.getElementById("formRemarks")?.value.trim() || leaveType;

        const d1 = new Date(fromVal);
        const d2 = new Date(toVal);
        const diffMs = Math.max(0, d2 - d1);
        const diffDays = Math.max(1, Math.ceil(diffMs / (1000 * 60 * 60 * 24)));
        const durationStr = `${{diffDays}} ${{diffDays === 1 ? 'day' : 'days'}}`;

        const options = {{ month: 'short', day: 'numeric', year: 'numeric' }};
        const fromFormattedDate = d1.toLocaleDateString('en-US', options);
        const toFormattedDate = d2.toLocaleDateString('en-US', options);
        const fromFormattedTime = d1.toLocaleTimeString('en-US', {{ hour: '2-digit', minute: '2-digit' }});
        const toFormattedTime = d2.toLocaleTimeString('en-US', {{ hour: '2-digit', minute: '2-digit' }});

        // Create new leave record with status Approved immediately
        const newLeave = {{
          id: Date.now(),
          leaveType: leaveType,
          type: "Leave",
          fromDate: fromFormattedDate,
          fromTime: fromFormattedTime,
          toDate: toFormattedDate,
          toTime: toFormattedTime,
          gateOut: "-",
          gateIn: "-",
          duration: durationStr,
          remarks: remarksVal,
          parentStatus: "Approved",
          status: "Approved",
          mentor: {{ name: "CS10789 - Dhivya P", status: "Approved" }},
          warden: {{ name: "ME11077 - josephsilvester", status: "Approved" }}
        }};

        // Prepend to leavesData array
        leavesData.unshift(newLeave);

        // Persist to localStorage
        try {{
          localStorage.setItem(STORAGE_KEY, JSON.stringify(leavesData));
        }} catch(e) {{
          console.error("Failed to save leave to localStorage:", e);
        }}

        leavesCurrentPage = 1;

        closeModal();
        showToast("Leave request submitted and approved automatically!");

        if (currentView === "leaves") {{
          renderLeavesTable();
        }} else {{
          switchView("leaves");
        }}
      }});
    }}

    // Switch View function with realistic transition
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
          item.className = "nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-red-600 hover:text-white text-iconColor transition-all";
        }} else {{
          item.className = "nav-item group flex gap-2 items-center p-2.5 rounded-xl cursor-pointer hover:bg-primary hover:text-white text-iconColor transition-all";
        }}
      }});

      // Update mobile dock buttons active status
      document.querySelectorAll("[data-mobile-nav]").forEach(btn => {{
        const target = btn.getAttribute("data-mobile-nav");
        if (target === viewName) {{
          btn.style.boxShadow = "0 0 0 2px rgba(125, 83, 246, 0.5)";
          btn.style.transform = "scale(1.05)";
        }} else {{
          btn.style.boxShadow = "none";
          btn.style.transform = "scale(1)";
        }}
      }});

      // Close mobile drawer if open
      toggleMobileMenu(false);

      // Inject View HTML
      container.innerHTML = VIEWS[viewName];
      container.scrollTop = 0;

      // Update Hash
      if (location.hash !== "#" + viewName) {{
        history.replaceState(null, "", "#" + viewName);
      }}

      // If switching to leaves, show brief spinner transition matching video (Frame 52)
      if (viewName === "leaves") {{
        const loader = document.getElementById("leavesLoadingState");
        const content = document.getElementById("leavesMainContent");
        if (loader && content) {{
          loader.classList.remove("hidden");
          loader.classList.add("flex");
          content.classList.add("hidden");
          setTimeout(() => {{
            loader.classList.add("hidden");
            loader.classList.remove("flex");
            content.classList.remove("hidden");
          }}, 350);
        }}
      }}

      // Attach View-specific event handlers
      bindViewEvents(viewName);
    }}

    // Bind Interactive Handlers
    function bindViewEvents(viewName) {{
      if (viewName === "leaves") {{
        renderLeavesTable();

        // Apply Leave button click
        document.getElementById("openApplyLeaveBtn")?.addEventListener("click", openApplyLeaveModal);

        // Search input filter
        const searchInput = document.getElementById("leavesSearchInput");
        searchInput?.addEventListener("input", (e) => {{
          leavesSearchFilter = e.target.value;
          leavesCurrentPage = 1;
          renderLeavesTable();
        }});

        // Entries per page select
        const perPageSelect = document.getElementById("leavesPerPageSelect");
        perPageSelect?.addEventListener("change", (e) => {{
          leavesPageSize = Number(e.target.value);
          leavesCurrentPage = 1;
          renderLeavesTable();
        }});

        // Filter icons
        container.querySelectorAll(".filter-icon").forEach(icon => {{
          icon.addEventListener("click", (e) => {{
            e.stopPropagation();
            const col = icon.getAttribute("data-col");
            openModal(`Filter by ${{col}}`, `
              <div class="space-y-2 text-xs">
                <button onclick="leavesSearchFilter=''; leavesCurrentPage=1; renderLeavesTable(); closeModal();" class="w-full text-left p-2 rounded-lg hover:bg-slate-100 font-medium">All Records</button>
                <button onclick="leavesSearchFilter='Leave'; leavesCurrentPage=1; renderLeavesTable(); closeModal();" class="w-full text-left p-2 rounded-lg hover:bg-slate-100 font-medium">Leave Only</button>
                <button onclick="leavesSearchFilter='GP'; leavesCurrentPage=1; renderLeavesTable(); closeModal();" class="w-full text-left p-2 rounded-lg hover:bg-slate-100 font-medium">GP Only</button>
                <button onclick="leavesSearchFilter='Sick Leave'; leavesCurrentPage=1; renderLeavesTable(); closeModal();" class="w-full text-left p-2 rounded-lg hover:bg-slate-100 font-medium">Sick Leave Only</button>
                <button onclick="leavesSearchFilter='Approved'; leavesCurrentPage=1; renderLeavesTable(); closeModal();" class="w-full text-left p-2 rounded-lg hover:bg-slate-100 font-medium">Approved Only</button>
                <button onclick="leavesSearchFilter='Completed'; leavesCurrentPage=1; renderLeavesTable(); closeModal();" class="w-full text-left p-2 rounded-lg hover:bg-slate-100 font-medium">Completed Only</button>
                <button onclick="leavesSearchFilter='Rejected'; leavesCurrentPage=1; renderLeavesTable(); closeModal();" class="w-full text-left p-2 rounded-lg hover:bg-slate-100 font-medium">Rejected Only</button>
              </div>
            `);
          }});
        }});
      }}

      if (viewName === "dashboard") {{
        // Points breakdown clicks
        const buttons = container.querySelectorAll("button");
        buttons.forEach(btn => {{
          const txt = btn.innerText || "";
          if (txt.includes("Activity Points") || txt.includes("47,730")) {{
            btn.addEventListener("click", openActivityBreakdown);
          }} else if (txt.includes("Opportunity Points") || txt.includes("460")) {{
            btn.addEventListener("click", openOpportunityBreakdown);
          }} else if (txt.includes("Responsive Score") || txt.includes("84")) {{
            btn.addEventListener("click", openResponsiveBreakdown);
          }}
        }});

        // Quick navigation buttons
        container.querySelectorAll('[data-dashboard-section="quickNav"] button').forEach(b => {{
          const t = b.innerText || "";
          if (t.includes("My Leaves")) b.addEventListener("click", () => switchView("leaves"));
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
              if (schedHeader) schedHeader.innerText = "Fri 9 Oct 2026";
              showToast("Jumped to Today: Fri 9 Oct 2026");
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
        const searchInput = container.querySelector("#courseSearchBar");
        if (searchInput) {{
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
          searchInput.addEventListener("input", filterCourses);
          container.querySelectorAll(".course-chip").forEach(chip => {{
            chip.addEventListener("click", function() {{
              container.querySelectorAll(".course-chip").forEach(c => c.classList.remove("active"));
              this.classList.add("active");
              filterCourses();
            }});
          }});
        }}

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
        const input = document.getElementById("practiceSearchBar");
        const pCards = container.querySelectorAll(".grid > div");
        input?.addEventListener("input", (e) => {{
          const val = e.target.value.toLowerCase().trim();
          pCards.forEach(c => {{
            c.style.display = (!val || c.innerText.toLowerCase().includes(val)) ? "flex" : "none";
          }});
        }});

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
              </div>
            `, `
              <button onclick="closeModal()" class="px-4 py-2 rounded-xl text-xs font-medium border border-slate-200 text-slate-600">Cancel</button>
              <button onclick="showToast('Starting assessment environment...'); closeModal();" class="px-4 py-2 rounded-xl text-xs font-semibold bg-[#7D53F6] text-white hover:opacity-90">Start Practice Test</button>
            `);
          }});
        }});
      }}

      if (viewName === "activity" || viewName === "academics") {{
        container.querySelectorAll(".group").forEach(card => {{
          card.addEventListener("click", () => {{
            const title = card.querySelector("h3")?.innerText || "Activity";
            if (title === "Movement Pass") openMovementPassModal();
            else if (title === "My Leaves") switchView("leaves");
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

        // Click row opens exact Rubric Review Modal matching Frame 55 & 36
        rows.forEach(row => {{
          row.addEventListener("click", () => {{
            const cells = row.querySelectorAll("td");
            if (cells.length >= 4) {{
              const cName = cells[1].innerText.trim();
              const slot = cells[2].innerText.trim();
              const comment = cells[3].innerText.trim();

              const known = reviewData[cName] || {{}};
              const actualSlot = known.slot || slot;
              const actualJustification = known.justification || comment || "The submitted solution was verified against required test cases and rubric criteria.";
              const rubrics = known.rubrics || [
                {{ label: "Code Quality", score: "30/40" }},
                {{ label: "Key Requirements", score: "20/25" }},
                {{ label: "Expected Output", score: "30/35" }}
              ];

              const rubricsHtml = rubrics.map(r => `
                <tr class="border-b border-slate-100">
                  <td class="py-2.5 px-3 font-medium text-slate-800">${{r.label}}</td>
                  <td class="py-2.5 px-3 font-bold text-slate-900">${{r.score}}</td>
                </tr>
              `).join("");

              openModal(cName, `
                <div class="space-y-4 text-xs">
                  <div>
                    <h5 class="font-bold text-slate-800 mb-1">Slot</h5>
                    <p class="text-slate-600 font-medium">${{actualSlot}}</p>
                  </div>
                  <div>
                    <h5 class="font-bold text-slate-800 mb-1">Justification</h5>
                    <p class="text-slate-600 leading-relaxed font-sans">${{actualJustification}}</p>
                  </div>
                  <div>
                    <h5 class="font-bold text-slate-800 mb-1.5">Rubric Scores</h5>
                    <div class="border border-slate-200 rounded-xl overflow-hidden">
                      <table class="w-full text-left border-collapse">
                        <thead>
                          <tr class="bg-slate-50 border-b border-slate-200 text-slate-700 font-bold">
                            <th class="py-2 px-3">Label</th>
                            <th class="py-2 px-3">Score</th>
                          </tr>
                        </thead>
                        <tbody>
                          ${{rubricsHtml}}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              `, `
                <button onclick="closeModal()" class="w-full py-2.5 rounded-xl font-semibold bg-[#7D53F6] hover:bg-[#6c42e6] text-white text-sm transition-all shadow-sm">Close</button>
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
