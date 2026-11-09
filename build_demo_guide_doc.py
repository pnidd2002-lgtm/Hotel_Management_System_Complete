import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_callout_box(doc, title, text, bg_hex="F4F6F9", border_hex="0F2C59"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"PRO TIP / KEY TAKEAWAY: {title}\n")
    run_t.font.name = 'Calibri'
    run_t.font.size = Pt(10)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(15, 44, 89)
    
    run_b = p.add_run(text)
    run_b.font.name = 'Calibri'
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(60, 64, 67)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)

def add_code_box(doc, code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, "282C34")
    set_cell_margins(cell, top=80, bottom=80, left=140, right=140)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(code_text)
    r.font.name = 'Consolas'
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(220, 223, 228)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)

def add_custom_table(doc, col_widths, headers, data, header_bg="0F2C59"):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = Inches(col_widths[i])
        set_cell_background(hdr_cells[i], header_bg)
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(title)
        r.font.name = 'Calibri'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    # Data rows
    for row_idx, row_data in enumerate(data, start=1):
        row_cells = table.rows[row_idx].cells
        bg = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_data):
            row_cells[col_idx].width = Inches(col_widths[col_idx])
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=60, bottom=60, left=100, right=100)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Calibri'
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(15, 44, 89)
            else:
                r.font.color.rgb = RGBColor(50, 55, 65)
                
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)

def add_p(doc, text="", bold_prefix="", space_before=2, space_after=4, bullet=False):
    p = doc.add_paragraph(style='List Bullet' if bullet else 'Normal')
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Calibri'
        r_b.font.size = Pt(10)
        r_b.font.bold = True
        r_b.font.color.rgb = RGBColor(15, 44, 89)
    if text:
        r_t = p.add_run(text)
        r_t.font.name = 'Calibri'
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = RGBColor(40, 44, 52)
    return p

def add_main_title(doc, title, subtitle):
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(10)
    p_inst.paragraph_format.space_after = Pt(2)
    r1 = p_inst.add_run("ESOFT METRO CAMPUS • FACULTY OF COMPUTING\n")
    r1.font.name = 'Calibri'; r1.font.size = Pt(11); r1.font.bold = True
    r1.font.color.rgb = RGBColor(184, 134, 11)
    
    r2 = p_inst.add_run("BIT (Hons) in Software Engineering Degree Programme")
    r2.font.name = 'Calibri'; r2.font.size = Pt(9.5); r2.font.italic = True
    r2.font.color.rgb = RGBColor(100, 105, 115)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(4)
    r_t = p_title.add_run(title)
    r_t.font.name = 'Calibri'; r_t.font.size = Pt(18); r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(15, 44, 89)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(14)
    r_s = p_sub.add_run(subtitle)
    r_s.font.name = 'Calibri'; r_s.font.size = Pt(11); r_s.font.bold = True
    r_s.font.color.rgb = RGBColor(27, 54, 93)

def add_sec_head(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.name = 'Calibri'; r.font.size = Pt(13); r.font.bold = True
    r.font.color.rgb = RGBColor(15, 44, 89)

def add_subsec_head(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    r.font.name = 'Calibri'; r.font.size = Pt(11); r.font.bold = True
    r.font.color.rgb = RGBColor(27, 54, 93)

def build_presentation_guide():
    doc = Document()
    
    # 1-inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    add_main_title(
        doc,
        "DUTCH POINT NEGOMBO • HOTEL MANAGEMENT SYSTEM",
        "Comprehensive System Demonstration & Viva Presentation Guide"
    )
    
    add_callout_box(
        doc,
        "ACADEMIC INTERIM MILESTONE (55% - 60% COMPLETION)",
        "This guide provides the exact spoken script, screen choreography, live database verification commands, "
        "and technical walkthrough for demonstrating the backend (ASP.NET Core 8), frontend (React SPA), and database (MySQL) "
        "during the Interim Viva examination. All currency calculations strictly reflect Sri Lankan Rupees (LKR)."
    )
    
    # STUDENT TABLE
    add_sec_head(doc, "Project Metadata & Presenting Team")
    team_headers = ["Student Name", "Student ID", "Project Role in Viva", "Key Demonstration Module"]
    team_data = [
        ["I.D.P.N Iddamalgoda", "E269559", "Lead Developer & System Admin", "Architecture, Admin Dashboard & Concurrency Verification"],
        ["H.M.Y.R Herath", "E267614", "Backend Software Engineer", "ASP.NET Core Web API, Controllers & LINQ Overlap Algorithm"],
        ["Y.M.A.Y Bandara", "E267609", "Frontend Software Engineer", "React SPA, UI/UX, Dynamic Filters & Live Booking Modal"],
        ["A.G.H.H Jinadasa", "E267612", "QA & Requirements Engineer", "Requirements Traceability Matrix (RTM) & Test Case Execution"]
    ]
    add_custom_table(doc, [1.6, 1.0, 1.9, 2.0], team_headers, team_data)

    # SECTION 1: PRE-DEMO SETUP
    add_sec_head(doc, "1. Pre-Demonstration Setup & Screen Preparation")
    add_p(doc, "Before inviting examiners to evaluate the demonstration, ensure that all services are active and four dedicated desktop windows are arranged for seamless switching (Alt+Tab):")
    
    setup_headers = ["Window / Tool", "Target URL / Command", "Display State", "Purpose in Demonstration"]
    setup_data = [
        ["Frontend UI", "http://localhost:5173", "Full Screen Browser", "Primary demonstration of customer registration, search, and booking."],
        ["Swagger REST API", "http://localhost:5000/swagger", "Browser Tab 2", "Shows RESTful endpoints, request/response models, and status codes."],
        ["MySQL Database", "hotel_db in Workbench / phpMyAdmin", "Split / Background", "Proves live transactional persistence and zero orphaned records."],
        ["Visual Studio / VS Code", "BookingsController.cs (Line 42-65)", "Minimized / Ready", "Code review of transactional double-booking prevention algorithm."]
    ]
    add_custom_table(doc, [1.3, 1.8, 1.4, 2.0], setup_headers, setup_data)

    add_subsec_head(doc, "1.1 Pre-Flight Health Check Commands (PowerShell)")
    add_p(doc, "Run these quick checks prior to the presentation to ensure ports and services are operating normally:")
    add_code_box(doc, 
        "# 1. Verify MySQL Service (Port 3306)\n"
        "Get-Service -Name MySQL*\n\n"
        "# 2. Launch Backend API (Port 5000)\n"
        "cd C:\\Users\\PASINDU\\Desktop\\Interim\\backend\n"
        "dotnet run --urls \"http://localhost:5000\"\n\n"
        "# 3. Launch Frontend Client (Port 5173)\n"
        "cd C:\\Users\\PASINDU\\Desktop\\Interim\\frontend\n"
        "npm run dev"
    )

    # SECTION 2: ARCHITECTURE & ROLE DIVISION
    add_sec_head(doc, "2. Presentation Strategy & Time Allocation")
    add_p(doc, "The presentation is timed for an optimal 12 to 14 minute interim demonstration window:")
    
    time_headers = ["Stage", "Duration", "Presenter", "Primary Objective"]
    time_data = [
        ["1. Architecture & Tech Stack", "1.5 Mins", "Pasindu Nirmal", "Introduce three-tier decoupled structure and interim progress."],
        ["2. Database Schema Inspection", "2.0 Mins", "Pasindu / Herath", "Show relational integrity, LKR room pricing, and empty test slate."],
        ["3. Backend API & Concurrency", "3.0 Mins", "H.M.Y.R Herath", "Explain C# controller logic and mathematical overlap formula."],
        ["4. Frontend Live Demonstration", "5.0 Mins", "Bandara & Pasindu", "Live registration, date/capacity search, booking, and double-booking block."],
        ["5. Admin Operations & RTM", "2.0 Mins", "Pasindu & Jinadasa", "Show Admin dashboard, revenue statistics, and RTM test alignment."],
        ["6. Examiner Q&A Defense", "Flexible", "All Team Members", "Defend architectural decisions, security controls, and final roadmap."]
    ]
    add_custom_table(doc, [1.5, 1.0, 1.5, 2.5], time_headers, time_data)

    # PAGE BREAK
    doc.add_page_break()

    # SECTION 3: STEP-BY-STEP SCRIPT
    add_sec_head(doc, "3. Step-by-Step Live Demonstration Script")

    add_subsec_head(doc, "Phase 1: Architecture & Technology Introduction (1.5 Mins)")
    add_p(doc, "Lead Developer & System Administrator (Pasindu Nirmal)", bold_prefix="Spoken By: ")
    add_p(doc, 
        "\"Good morning respected panel of lecturers. Today our team is presenting the Interim progress of the "
        "Dutch Point Negombo Web-Based Hotel Management System. As established in our interim deliverables, the system has reached "
        "55% to 60% completion, covering the core reservation lifecycle, user authentication, and inventory administration.\n\n"
        "Our system is architected as an enterprise Three-Tier solution:\n"
        "• Presentation Tier: A responsive Single Page Application built with React and Vite.\n"
        "• Application Tier: A secure, high-throughput REST API built on ASP.NET Core 8 and C#.\n"
        "• Data Tier: A relational MySQL database enforcing referential integrity and optimized indexes via Entity Framework Core.\n\n"
        "To provide a rigorous technical demonstration, we will not merely demonstrate clicking buttons on the UI; "
        "we will show you how each transaction originates in the browser, processes through the C# business logic, and mutates state in MySQL.\"")

    add_subsec_head(doc, "Phase 2: Database Layer Showcase (2 Mins)")
    add_p(doc, "Lead Developer (Pasindu) and Backend Engineer (Herath)", bold_prefix="Spoken By: ")
    add_p(doc, "Switch screen to MySQL Workbench / phpMyAdmin with database 'hotel_db' visible.", bold_prefix="Choreography: ")
    add_p(doc, "1. Run query: SELECT RoomId, RoomNumber, RoomType, PricePerNight, Capacity, Status FROM Rooms;", bold_prefix="Action 1: ")
    add_p(doc, 
        "\"Notice here in our database that all room prices are stored natively in Sri Lankan Rupees (LKR), ranging from "
        "LKR 28,000 for standard Deluxe Suites to LKR 140,000 for Presidential Ocean Villas. Each room has an enforced guest Capacity limit. "
        "This resolves the currency and capacity feedback raised during our early requirements gathering stage.\"")
    add_p(doc, "2. Run query: SELECT BookingId, RoomId, UserId, CheckInDate, CheckOutDate, Status FROM Bookings;", bold_prefix="Action 2: ")
    add_p(doc, 
        "\"Notice that Suite 101 currently has no reservations for the target test dates of October 10th to October 12th, 2026. "
        "We will now initiate a live transaction on the frontend and track this record into the database.\"")

    add_subsec_head(doc, "Phase 3: Backend REST API & Concurrency Logic (3 Mins)")
    add_p(doc, "Backend Software Engineer (H.M.Y.R Herath)", bold_prefix="Spoken By: ")
    add_p(doc, "Switch screen to Swagger UI (http://localhost:5000/swagger) and Visual Studio showing BookingsController.cs.", bold_prefix="Choreography: ")
    add_p(doc, 
        "\"In our ASP.NET Core application, we have separated operations into dedicated domain controllers: "
        "AuthController handles token generation and user registration; RoomsController manages inventory querying; "
        "and BookingsController encapsulates transactional reservation processing.\n\n"
        "The primary engineering hurdle in hospitality software is the prevention of double bookings when multiple users "
        "attempt to reserve the same physical suite for overlapping dates. Here is our transactional check inside BookingsController:\"")
    
    add_code_box(doc,
        "// Transactional Date Overlap Validation in C# / LINQ\n"
        "var isOverlapping = await _context.Bookings.AnyAsync(b =>\n"
        "    b.RoomId == request.RoomId &&\n"
        "    b.Status != \"Cancelled\" &&\n"
        "    b.CheckInDate < request.CheckOutDate &&\n"
        "    b.CheckOutDate > request.CheckInDate\n"
        ");\n\n"
        "if (isOverlapping)\n"
        "{\n"
        "    return Conflict(new { message = \"Room is already reserved for the selected dates.\" });\n"
        "}"
    )
    add_p(doc, 
        "\"This LINQ expression implements the standard mathematical interval intersection formula: a conflict exists if and only if "
        "an existing check-in is earlier than the requested check-out AND an existing check-out is later than the requested check-in. "
        "If true, the API rejects the request with HTTP 409 Conflict before any database write occurs.\"")

    # PAGE BREAK
    doc.add_page_break()

    add_subsec_head(doc, "Phase 4: Frontend Live Demonstration & End-to-End Workflow (5 Mins)")
    add_p(doc, "Frontend Software Engineer (Y.M.A.Y Bandara) & Pasindu Nirmal", bold_prefix="Spoken By: ")
    add_p(doc, "Switch browser to http://localhost:5173 in full-screen view.", bold_prefix="Choreography: ")

    add_p(doc, "Scenario A: Secure Registration & Role-Based Access Control (RBAC)", bold_prefix="Sub-Scenario A: ")
    add_p(doc, "Click 'Sign In' -> Click 'Register an Account'. Show the modal fields.", bold_prefix="Action: ")
    add_p(doc, 
        "\"Notice that our registration dialog contains fields for Full Name, Email, Password, Phone Number, and Address, "
        "but completely excludes any role selection dropdown. In our initial design, visitors could select their role. "
        "During security review, this was recognized as an OWASP Broken Access Control vulnerability. Now, our backend strictly hardcodes "
        "the 'Customer' role for all public registrations, completely preventing privilege escalation.\"")
    add_p(doc, "Register user: Kasun Silva | Email: kasun@demo.com | Password: Kasun@123 | Phone: 0771234567 | Address: Negombo.", bold_prefix="Live Action: ")
    add_p(doc, "Click 'Complete Registration'. System automatically logs Kasun in. The header shows 'Kasun Silva [Customer]'.", bold_prefix="Result: ")
    add_p(doc, "Switch to MySQL: Run SELECT UserId, FullName, Email, Role FROM Users WHERE Email='kasun@demo.com';. Show the lecturer that Kasun is stored with Role='Customer'.", bold_prefix="DB Proof: ")

    add_p(doc, "Scenario B: Multi-Variable Search, Guest Count & LKR Pricing", bold_prefix="Sub-Scenario B: ")
    add_p(doc, "Navigate to the search bar. Select Check-In: 2026-10-10, Check-Out: 2026-10-12 (2 Nights). Select Guest Count: 2 Guests.", bold_prefix="Action: ")
    add_p(doc, "Click 'Check Rates'. Point out the green 'AVAILABLE' badge on Deluxe Suite 101 and the rate: LKR 28,000 / Night.", bold_prefix="Result: ")
    add_p(doc, 
        "\"The system automatically calculates the stay total: 2 nights at LKR 28,000 per night equals LKR 56,000.\n"
        "Now, watch what happens if we change the Guest Count to 5 Guests. Deluxe Suite 101 (maximum capacity 2) disappears from the search results, "
        "and only larger Family Villas with Capacity >= 5 are displayed. This eliminates guest overcapacity errors.\"")

    add_p(doc, "Scenario C: Live Booking Creation & Instant Database Persistence", bold_prefix="Sub-Scenario C: ")
    add_p(doc, "Reset Guest Count to 2 Guests. Click 'Book Now' on Deluxe Suite 101.", bold_prefix="Action: ")
    add_p(doc, "Review the booking summary modal: 2 Guests, 2 Nights, Total Stay: LKR 56,000. Click 'Confirm Booking'.", bold_prefix="Action: ")
    add_p(doc, "A confirmation dialog appears: 'Reservation Confirmed! Booking ID: RES-1001'.", bold_prefix="Result: ")
    add_p(doc, "Switch to MySQL: Run SELECT BookingId, RoomId, UserId, TotalAmount, Status FROM Bookings ORDER BY BookingId DESC LIMIT 1;. Show the newly created row with TotalAmount=56000.00 and Status='Confirmed'.", bold_prefix="DB Proof: ")

    add_p(doc, "Scenario D: Concurrency Test - Live Overlapping Double-Booking Prevention", bold_prefix="Sub-Scenario D: ")
    add_p(doc, "Stay in the browser. Select dates that overlap with Kasun's booking: 2026-10-11 to 2026-10-14 for Deluxe Suite 101.", bold_prefix="Action: ")
    add_p(doc, "Click 'Book Now' -> 'Confirm Booking'.", bold_prefix="Action: ")
    add_p(doc, "The UI displays an immediate red warning alert: 'Room is already reserved for the selected dates. Please choose another date or room.'", bold_prefix="Result: ")
    add_p(doc, "Press F12 -> Network Tab -> Show the POST /api/Bookings request returning red HTTP 409 Conflict from ASP.NET Core.", bold_prefix="Inspector Proof: ")
    add_p(doc, 
        "\"This live test proves that our backend actively enforces transactional concurrency, protecting the resort from costly double-booking errors.\"")

    add_subsec_head(doc, "Phase 5: Admin Dashboard & Operational Controls (2 Mins)")
    add_p(doc, "Lead Developer & System Administrator (Pasindu Nirmal)", bold_prefix="Spoken By: ")
    add_p(doc, "Log out from Kasun's account. Click 'Sign In' and enter Admin credentials: Username: Pasindu | Password: Pasindu@123.", bold_prefix="Action: ")
    add_p(doc, "Point out the top navigation bar. Notice that 'Admin Dashboard' and 'Inventory Management' are now accessible.", bold_prefix="Result: ")
    add_p(doc, 
        "\"Upon logging in with the administrative identity, the navigation dynamically adapts. Inside the Admin Dashboard:\n"
        "• Operational KPI Cards: Displays Total Revenue (in LKR), Total Active Bookings, and Available vs Occupied Room counts.\n"
        "• Occupied Rooms Tracker: Suite 101 is clearly flagged as Occupied across October 10th to 12th.\n"
        "• Reservation Roster: Front-desk staff can inspect guest contact details, verify headcount, and execute manual check-ins or cancellations.\"")

    add_subsec_head(doc, "Phase 6: Traceability Matrix (RTM) & Test Verification (1.5 Mins)")
    add_p(doc, "QA & Requirements Engineer (A.G.H.H Jinadasa)", bold_prefix="Spoken By: ")
    add_p(doc, 
        "\"Every feature demonstrated today links directly back to the 5-stage Requirements Engineering process defined in Chapter 2 of our Interim Report:\n"
        "• Business Objective 1 (Automated Reservations) was verified via Test Case TC-01.\n"
        "• Business Objective 2 (Double-Booking Prevention) was verified via Test Case TC-04 (HTTP 409 Conflict).\n"
        "• Business Objective 3 (Role-Based Access Control) was verified via Test Case TC-05.\n"
        "• Business Objective 4 (Capacity & Headcount Enforcement) was verified via Test Case TC-09.\n\n"
        "All test cases executed live during this session have passed verification without defect. We are now on schedule to complete the remaining 40% of the project for the final viva.\"")

    # PAGE BREAK
    doc.add_page_break()

    # SECTION 4: VIVA Q&A DEFENSE
    add_sec_head(doc, "4. Lecturer Viva Q&A Defense (Examiner Cheat Sheet)")
    add_p(doc, "Prepare for these common technical questions asked by software engineering panels:")

    qa_list = [
        ("Q1: Why did you choose ASP.NET Core 8 Web API instead of Node.js / Express or PHP?",
         "ASP.NET Core provides enterprise-grade asynchronous throughput, compile-time type safety via C#, and native dependency injection. "
         "Furthermore, Entity Framework Core offers a robust Object-Relational Mapper (ORM) that natively parameterizes queries, completely eliminating SQL injection "
         "and managing transactional concurrency much more reliably than standard scripting languages."),
         
        ("Q2: How does your system protect against SQL Injection and Data Tampering?",
         "We do not concatenate raw SQL strings anywhere in our backend. All database queries use LINQ expressions compiled into parameterized SQL by EF Core. "
         "On the authentication layer, passwords are protected, and public registration endpoints strictly ignore any client-supplied role payloads, "
         "hardcoding the role to 'Customer' on the server."),
         
        ("Q3: Why was currency converted from US Dollars ($) to Sri Lankan Rupees (LKR)?",
         "Dutch Point Negombo is a boutique beachfront resort operating in Western Province, Sri Lanka. During our requirements gathering interview with the General Manager, "
         "management emphasized that front-desk operations and bank reconciliation occur strictly in Sri Lankan Rupees. Showing USD rates created a disconnect for domestic guests "
         "and required volatile exchange rate conversions. All pricing was permanently localized to LKR (LKR 28,000 to LKR 140,000 / night)."),
         
        ("Q4: How does the system handle high traffic if two users click 'Book Now' at the exact same millisecond?",
         "Our double-booking prevention algorithm executes inside an ACID database transaction. If two simultaneous HTTP POST requests arrive, the database transaction lock "
         "ensures the first request is committed while the second request evaluates the overlap condition, encounters the freshly committed row, and is gracefully rejected with HTTP 409 Conflict."),
         
        ("Q5: What exact features remain to be implemented for the Final (100%) submission?",
         "The remaining 40% of the project scope consists of four well-defined modules: "
         "(1) Online Payment Gateway (IPG) integration via PayHere sandbox; "
         "(2) Automated PDF invoice and receipt generation; "
         "(3) Automated SMS/Email reservation confirmation alerts; and "
         "(4) Advanced historical occupancy and revenue predictive analytics for resort management.")
    ]

    for q, a in qa_list:
        add_p(doc, a, bold_prefix=f"{q}\nAnswer: ", space_before=4, space_after=6)

    # SECTION 5: EMERGENCY CHECKLIST
    add_sec_head(doc, "5. Emergency Troubleshooting Checklist")
    add_p(doc, "If any technical issue arises during the presentation, stay calm and follow these quick recovery steps:")

    trouble_headers = ["Potential Issue", "Root Cause", "Quick Fix (Run in PowerShell / Terminal)"]
    trouble_data = [
        ["Port 5000 Already in Use", "Previous backend process still running", "Get-Process -Name backend | Stop-Process -Force"],
        ["MySQL Connection Refused", "MySQL Windows Service stopped", "Start-Service MySQL80 (or open XAMPP and click Start on MySQL)"],
        ["Frontend Fails to Connect", "CORS policy or backend offline", "Verify backend terminal displays 'Now listening on: http://localhost:5000'"],
        ["Overlapping Booking Not Blocked", "Status was set to 'Cancelled'", "Check MySQL Bookings table; cancelled reservations deliberately free up dates"]
    ]
    add_custom_table(doc, [1.8, 1.8, 2.9], trouble_headers, trouble_data)

    out_docx = r"C:\Users\PASINDU\Desktop\Interim\Hotel_Management_System_Presentation_and_Demonstration_Guide.docx"
    doc.save(out_docx)
    print(f"Generated successfully: {out_docx}")

if __name__ == "__main__":
    build_presentation_guide()
