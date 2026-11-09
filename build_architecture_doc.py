import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

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
    run_t = p.add_run(f"KEY ARCHITECTURAL HIGHLIGHT: {title}\n")
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

def build_architecture_doc():
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
        "System Architecture & End-to-End Execution Flow Technical Report"
    )
    
    add_callout_box(
        doc,
        "DECOUPLED THREE-TIER ENTERPRISE ARCHITECTURE",
        "This document provides the exhaustive technical specification of the system architecture for the Dutch Point Negombo "
        "Web-Based Hotel Management System. It details the structural responsibilities of Tier 1 (React 18 SPA), Tier 2 (ASP.NET Core 8 Web API), "
        "and Tier 3 (MySQL 8.0), followed by an under-the-hood walkthrough of the complete request-response cycle, concurrency locking, and security controls."
    )
    
    # STUDENT TABLE
    add_sec_head(doc, "Project Metadata & Presenting Engineering Team")
    team_headers = ["Student Name", "Student ID", "Project Architectural Role", "Component Responsibility"]
    team_data = [
        ["I.D.P.N Iddamalgoda", "E269559", "Lead Developer & System Admin", "Three-Tier Integration, Security & Concurrency Verification"],
        ["H.M.Y.R Herath", "E267614", "Backend Software Engineer", "ASP.NET Core 8 Web API, C# Controllers & EF Core ORM Layer"],
        ["Y.M.A.Y Bandara", "E267609", "Frontend Software Engineer", "React 18 SPA Client, State Management & Asynchronous Fetch API"],
        ["A.G.H.H Jinadasa", "E267612", "QA & Requirements Engineer", "Architectural Testing, Load Validation & Requirements Traceability"]
    ]
    add_custom_table(doc, [1.6, 1.0, 1.9, 2.0], team_headers, team_data)

    # SECTION 1: ARCHITECTURAL OVERVIEW
    add_sec_head(doc, "1. Architectural Overview & Design Pattern")
    add_p(doc,
        "The Dutch Point Negombo Hotel Management System employs an enterprise-grade Three-Tier Decoupled Architecture. "
        "Unlike monolithic web applications where HTML generation, business calculations, and database queries are combined inside a single process, "
        "this system strictly separates presentation concerns, business rules, and persistent data storage into three distinct physical and logical layers:")
    
    arch_summary_headers = ["Architectural Layer", "Underlying Technology", "Execution Environment & Port", "Core Architectural Purpose"]
    arch_summary_data = [
        ["Tier 1: Presentation Tier", "React 18, Vite, Bootstrap 5, CSS3", "Client Web Browser (Port 5173 / Localhost)", "User experience, responsive rendering, form state management & JSON serialization."],
        ["Tier 2: Application Tier", "ASP.NET Core 8 Web API, C#, EF Core 8", "Host Server Runtime (Port 5000 / HTTP)", "RESTful routing, RBAC authorization, business rules, concurrency checks & ORM compilation."],
        ["Tier 3: Data Tier", "MySQL Server 8.0, InnoDB Storage Engine", "Database Daemon (Port 3306 / TCP)", "ACID-compliant storage, foreign key constraints, table indexing & transaction journaling."]
    ]
    add_custom_table(doc, [1.5, 1.6, 1.6, 1.8], arch_summary_headers, arch_summary_data)

    add_p(doc,
        "The decoupling between Tier 1 and Tier 2 is achieved through standardized, asynchronous RESTful APIs communicating over HTTP. "
        "The frontend has zero direct connection to the database, ensuring that client-side scripts can never execute arbitrary SQL or bypass business validation rules.")

    # SECTION 2: THE THREE TIERS IN DETAIL
    add_sec_head(doc, "2. Comprehensive Breakdown of the Three Architectural Tiers")

    add_subsec_head(doc, "2.1 Tier 1: Presentation Tier (Frontend Client)")
    add_p(doc, "The Presentation Tier is executed entirely on the client's device inside a modern web browser. Key architectural components include:")
    tier1_bullets = [
        ("Component-Based Single Page Application (SPA): ", "Constructed using React 18 and compiled with Vite. Navigation between views (Home, Luxury Rooms, Occupancy Tracker, My Bookings, Admin Dashboard) occurs without reloading the web page, ensuring near-instantaneous transitions."),
        ("Client-Side State Management: ", "Uses React Hooks (useState, useEffect, useMemo) to maintain real-time filter states (Check-In Date, Check-Out Date, Guest Headcount) and user session tokens in memory."),
        ("Responsive Layout & Boutique Styling: ", "Utilizes Bootstrap 5 grid systems combined with bespoke CSS variables to deliver an executive coastal boutique aesthetic tailored for Dutch Point Negombo."),
        ("Asynchronous REST Communications: ", "Fires asynchronous browser fetch() requests to the backend API, passing structured JSON payloads and dynamically rendering returned data into DOM elements.")
    ]
    for b_title, b_desc in tier1_bullets:
        add_p(doc, b_desc, bold_prefix=b_title, bullet=True)

    add_subsec_head(doc, "2.2 Tier 2: Application / Business Logic Tier (Backend API)")
    add_p(doc, "The Application Tier is built using C# and ASP.NET Core 8 Web API. It functions as the secure gatekeeper and brain of the system:")
    tier2_bullets = [
        ("Domain-Driven REST Controllers: ", "Incoming requests are categorized into specialized controllers: AuthController (JWT tokens and registration), RoomsController (inventory and status), BookingsController (transactional reservation lifecycle), and DashboardController (operational KPIs)."),
        ("Model Binding & Data Transfer Objects (DTOs): ", "Incoming JSON strings are automatically deserialized into strongly-typed C# DTOs (e.g., CreateBookingRequest, OccupiedRoomDto), validating data types and rejecting malformed inputs before reaching business logic."),
        ("Business Rule & Pricing Enforcement: ", "Computes stay totals strictly in Sri Lankan Rupees (LKR) using the formula: TotalAmount = Nights * PricePerNight. Validates headcount against room limits (Capacity >= NumberOfGuests)."),
        ("Transactional Concurrency Engine: ", "Prevents overbooking by verifying that requested stay intervals do not overlap with existing confirmed reservations inside an ACID database transaction."),
        ("Entity Framework Core (EF Core 8) ORM: ", "Translates high-level LINQ queries into optimized, parameterized SQL statements executed against the MySQL database.")
    ]
    for b_title, b_desc in tier2_bullets:
        add_p(doc, b_desc, bold_prefix=b_title, bullet=True)

    add_subsec_head(doc, "2.3 Tier 3: Data Tier (Relational Database Management System)")
    add_p(doc, "The Data Tier is managed by MySQL Server 8.0 running the normalized relational schema 'hotel_db':")
    tier3_bullets = [
        ("Normalized Relational Schema (3NF): ", "Organized into four primary business entities: customers (user identity and roles), rooms (physical suites, LKR rates, capacities), bookings (reservation dates, headcounts, statuses), and payments (financial vouchers)."),
        ("Referential Integrity Constraints: ", "Foreign keys strictly enforce parent-child relationships between Customers, Rooms, and Bookings. ON DELETE RESTRICT prevents accidental deletion of rooms or guest records tied to active financial reservations."),
        ("Financial Precision: ", "All monetary values are stored in DECIMAL(10,2) columns, preventing floating-point rounding errors during currency calculations in LKR."),
        ("ACID Transaction Guarantees: ", "Atomicity, Consistency, Isolation, and Durability ensure that reservations and payment records are written completely or rolled back entirely upon server failure.")
    ]
    for b_title, b_desc in tier3_bullets:
        add_p(doc, b_desc, bold_prefix=b_title, bullet=True)

    # PAGE BREAK
    doc.add_page_break()

    # SECTION 3: HOW IT HAPPENS (END-TO-END FLOW)
    add_sec_head(doc, "3. 'How It Happens': The Complete End-to-End Execution Flow")
    add_p(doc,
        "To understand how the three tiers collaborate during real-world operations, consider the complete execution lifecycle "
        "when a resort guest books Deluxe Suite 101 for October 10th to October 12th, 2026:")

    flow_headers = ["Phase & Step", "Executing Tier & File", "Action Performed Under the Hood", "Data Format / Protocol"]
    flow_data = [
        ["Step 1: User Input", "Tier 1: React Client (App.jsx)", "Guest selects check-in (2026-10-10), check-out (2026-10-12), 2 guests, and clicks 'Confirm Booking'.", "In-Memory React State"],
        ["Step 2: Request Packaging", "Tier 1: BookingModal.jsx", "Client serializes inputs into JSON: { customerId: 1, roomId: 3, checkInDate: '2026-10-10', ... } and initiates fetch().", "HTTP POST Payload (JSON)"],
        ["Step 3: Network Transport", "Network Layer (Port 5000)", "Request travels over TCP to ASP.NET Core listening on http://localhost:5000/api/bookings.", "TCP / IP Protocol"],
        ["Step 4: Middleware Routing", "Tier 2: Program.cs Pipeline", "CORS middleware inspects origin. Routing middleware maps URL to BookingsController.CreateBooking().", "ASP.NET Core Middleware"],
        ["Step 5: Model Binding", "Tier 2: BookingsController.cs", "ASP.NET Core deserializes JSON into C# CreateBookingRequest object. Validates checkIn < checkOut.", "Strongly-Typed C# Object"],
        ["Step 6: Capacity Verification", "Tier 2: BookingsController.cs", "Backend checks room capacity: Does Suite 101 hold 2 guests? (Capacity 2 >= 2 -> Approved).", "C# In-Memory Evaluation"],
        ["Step 7: Concurrency Query", "Tier 2: EF Core 8 (LINQ)", "Executes overlap LINQ check: Any existing booking where CheckIn < ReqOut AND CheckOut > ReqIn?", "LINQ to Entities Expression"],
        ["Step 8: SQL Parameterization", "Tier 2: EF Core Provider", "Translates LINQ to parameterized SQL: SELECT EXISTS(...) WHERE RoomId = @p0 AND ...", "Parameterized SQL Statement"],
        ["Step 9: Database Execution", "Tier 3: MySQL (hotel_db)", "MySQL engine executes query on Port 3306. Evaluates index. Returns false (Room is currently vacant).", "Binary Database Result Set"],
        ["Step 10: Financial Calculation", "Tier 2: BookingsController.cs", "Calculates stay: (Oct 12 - Oct 10) = 2 nights. Total = 2 * LKR 65,000 = LKR 130,000.", "C# Decimal Arithmetic"],
        ["Step 11: Transactional Insert", "Tier 3: MySQL Engine", "EF Core dispatches INSERT INTO bookings... MySQL writes record to disk and issues auto-increment ID 7.", "ACID SQL Transaction Commit"],
        ["Step 12: Success Response", "Tier 2: BookingsController.cs", "Serializes success payload: { message: 'Booking created!', bookingId: 7, totalAmount: 130000.00 } and returns HTTP 200.", "HTTP 200 OK (JSON)"],
        ["Step 13: UI Re-rendering", "Tier 1: App.jsx", "fetch() receives 200 OK. React closes modal, displays confirmation banner, and triggers live occupancy refresh.", "DOM Re-render (Virtual DOM)"]
    ]
    add_custom_table(doc, [1.4, 1.7, 2.2, 1.2], flow_headers, flow_data)

    add_subsec_head(doc, "3.1 Branching Logic: What Happens When a Collision Occurs?")
    add_p(doc,
        "If a second guest attempts to reserve the identical suite for overlapping dates (e.g., October 11th to 14th), "
        "Step 9 detects the existing record committed in Step 11. The backend immediately aborts execution, generates an HTTP 409 Conflict status, "
        "and returns the existing booking information. The React frontend intercepts the 409 status and renders a red alert banner, "
        "completely preventing the second reservation from reaching the database.")

    add_code_box(doc,
        "// Server-Side Concurrency Guard (BookingsController.cs)\n"
        "var conflictingBooking = await _context.Bookings\n"
        "    .Where(b => b.RoomId == request.RoomId &&\n"
        "               (b.BookingStatus == \"Confirmed\" || b.BookingStatus == \"Checked-In\") &&\n"
        "                b.CheckInDate < checkOut &&\n"
        "                b.CheckOutDate > checkIn)\n"
        "    .FirstOrDefaultAsync();\n\n"
        "if (conflictingBooking != null)\n"
        "{\n"
        "    return Conflict(new { message = \"Room is already booked for the selected dates.\" });\n"
        "}"
    )

    # SECTION 4: SECURITY CONTROLS
    add_sec_head(doc, "4. Architectural Security & Integrity Controls")
    add_p(doc, "The three-tier architecture incorporates multi-layered defense mechanisms:")
    sec_points = [
        ("Zero Client Trust Principle: ", "The browser client is treated as inherently untrusted. Critical calculations (room prices, stay durations, role permissions) are performed exclusively on the Application Tier. Room rates are queried directly from MySQL, preventing client-side price tampering."),
        ("Server-Side Role Isolation: ", "To eliminate OWASP Broken Access Control vulnerabilities, public registration endpoints ignore client-supplied role parameters and strictly hardcode the 'Customer' role on the server. Administrative roles can only be granted directly in the database."),
        ("SQL Injection Neutralization: ", "All database interactions occur via Entity Framework Core LINQ queries, which compile into strongly-parameterized SQL commands (@p0, @p1). User input is treated strictly as literal data, rendering SQL injection exploits impossible."),
        ("Cross-Origin Resource Sharing (CORS): ", "The ASP.NET Core pipeline explicitly whitelists the frontend development origin (http://localhost:5173), rejecting unauthorized cross-site API invocations.")
    ]
    for b_title, b_desc in sec_points:
        add_p(doc, b_desc, bold_prefix=b_title, bullet=True)

    # SECTION 5: ADVANTAGES & VIVA DEFENSE
    add_sec_head(doc, "5. Architectural Advantages & Viva Defense Justification")
    add_p(doc, "When defending the architectural design to the examination panel, emphasize these four core software engineering benefits:")

    adv_headers = ["Architectural Benefit", "Software Engineering Principle", "Practical Value to Dutch Point Negombo"]
    adv_data = [
        ["Separation of Concerns", "Modularity & Decoupling", "Frontend engineers can redesign the boutique UI without touching database schemas; backend engineers can optimize SQL queries without breaking the UI."],
        ["Platform Extensibility", "Reusability of Business Logic", "The same ASP.NET Core REST API can serve a native mobile app (iOS/Android) or front-desk desktop tablet in the future with zero backend changes."],
        ["Maintainability & Isolation", "Single Responsibility Principle", "Authentication issues in AuthController are isolated from reservation logic in BookingsController, minimizing software regression risks."],
        ["Optimal Resource Usage", "Client-Side Processing", "The browser handles DOM rendering, animations, and form validation, relieving the server from rendering HTML templates and enabling higher guest throughput."]
    ]
    add_custom_table(doc, [1.8, 1.8, 2.9], adv_headers, adv_data)

    out_docx = r"C:\Users\PASINDU\Desktop\Interim\Hotel_Management_System_Architecture_Documentation.docx"
    doc.save(out_docx)
    print(f"Generated successfully: {out_docx}")

if __name__ == "__main__":
    build_architecture_doc()
