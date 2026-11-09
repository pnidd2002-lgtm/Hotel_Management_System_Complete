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
    run_t = p.add_run(f"EVALUATION & REFLECTION HIGHLIGHT: {title}\n")
    run_t.font.name = 'Calibri'
    run_t.font.size = Pt(10)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(15, 44, 89)
    
    run_b = p.add_run(text)
    run_b.font.name = 'Calibri'
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(60, 64, 67)

def format_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    run = h.runs[0]
    run.font.name = 'Calibri'
    if level == 1:
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 44, 89)
    elif level == 2:
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(184, 134, 11)
    elif level == 3:
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(33, 37, 41)
    return h

def format_body_p(doc, text, bold_prefix="", space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 44, 89)
    r_body = p.add_run(text)
    r_body.font.name = 'Calibri'
    r_body.font.size = Pt(10)
    r_body.font.color.rgb = RGBColor(50, 50, 50)
    return p

def format_bullet(doc, title, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_t = p.add_run(title + ": ")
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(10)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(15, 44, 89)
    r_b = p.add_run(text)
    r_b.font.name = 'Calibri'
    r_b.font.size = Pt(10)
    r_b.font.color.rgb = RGBColor(60, 64, 67)
    return p

def format_code_block(doc, code_str, caption=""):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, "1E1E1E")  # Dark code style
    set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1
    r = p.add_run(code_str)
    r.font.name = 'Consolas'
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(220, 220, 220)
    
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        rc = p_cap.add_run(caption)
        rc.font.name = 'Calibri'
        rc.font.size = Pt(8.5)
        rc.font.italic = True
        rc.font.color.rgb = RGBColor(100, 116, 139)

def style_table(table, col_widths, headers, data, align_cols=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    hdr_row = table.rows[0]
    hdr_tr = hdr_row._tr.get_or_add_trPr()
    hdr_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    for i, title in enumerate(headers):
        cell = hdr_row.cells[i]
        cell.width = Inches(col_widths[i])
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(title)
        r.font.name = 'Calibri'
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx + 1]
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Inches(col_widths[c_idx])
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            if align_cols and c_idx in align_cols:
                p.alignment = align_cols[c_idx]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(str(val))
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(15, 44, 89)
            elif "Mitigated" in str(val) or "Resolved" in str(val) or "Phase 2" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129)
            elif "Challenge" in str(val) or "Bottleneck" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(220, 38, 38)
            else:
                r.font.color.rgb = RGBColor(60, 64, 67)

def build_chapter6_doc():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    base_dir = r"C:\Users\PASINDU\Desktop\Interim"
    
    # Document Cover / Title Header
    tp = doc.add_paragraph()
    tp.paragraph_format.space_after = Pt(2)
    r1 = tp.add_run("DUTCH POINT NEGOMBO • WEB-BASED HOTEL MANAGEMENT SYSTEM\n")
    r1.font.name = 'Calibri'
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(184, 134, 11)
    
    r2 = tp.add_run("CHAPTER 06: CRITICAL EVALUATION, REFLECTION & FUTURE ENHANCEMENTS")
    r2.font.name = 'Calibri'
    r2.font.size = Pt(18)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(15, 44, 89)
    
    mp = doc.add_paragraph()
    mp.paragraph_format.space_after = Pt(12)
    rm = mp.add_run("Comprehensive Technical Self-Reflection, ASP.NET Core & API Testing Challenges, Security Roadmap & 2FA\n"
                    "Academic Interim Report • BIT (Hons) in Software Engineering • Lead Developer: Pasindu Nirmal Iddamalgoda (E269559)")
    rm.font.name = 'Calibri'
    rm.font.size = Pt(9.5)
    rm.font.italic = True
    rm.font.color.rgb = RGBColor(100, 116, 139)
    
    hr_p = doc.add_paragraph()
    hr_p.paragraph_format.space_after = Pt(12)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="0F2C59"/></w:pBdr>')
    hr_p._p.get_or_add_pPr().append(pBdr)

    # =========================================================================
    # 6.1 CRITICAL EVALUATION OF THE DEVELOPED SYSTEM
    # =========================================================================
    format_heading(doc, "6.1 Critical Evaluation of the Developed System", level=1)
    format_body_p(doc, 
        "Chapter 06 delivers a rigorous, self-critical appraisal of the Dutch Point Negombo Web-Based Hotel Management System at the Interim milestone. Software engineering academic standards demand an honest evaluation of project achievements against original specifications, identifying both technical triumphs and operational limitations encountered during development.")

    add_callout_box(doc, "Interim System Achievements vs Scope Baseline",
        "1. Concurrency Integrity: The core objective—preventing catastrophic room double-bookings—was successfully realized using Allen's Interval Algebra at the database query tier.\n"
        "2. Multi-Tier Decoupling: A modern decoupled architecture (React 19 Frontend + ASP.NET Core Web API + Relational Database) was proven viable, eliminating monolithic tight coupling.\n"
        "3. Financial Transparency: All room rates, stay durations, and billing totals are strictly computed in Sri Lankan Rupees (LKR) with decimal(18,2) precision, eliminating rounding anomalies.\n"
        "4. Scope Discipline: Security vulnerabilities such as client-side role pickers were successfully identified and replaced with server-side Role-Based Access Control (RBAC).")

    # =========================================================================
    # 6.2 TECHNICAL REFLECTION: ASP.NET CORE & API TESTING DIFFICULTIES
    # =========================================================================
    format_heading(doc, "6.2 Technical Reflection & Developer Learning Curve", level=1)
    format_body_p(doc, 
        "Transitioning from client-side scripting and basic CRUD paradigms to an enterprise-grade backend built with ASP.NET Core, C#, and Entity Framework Core posed substantial conceptual and technical hurdles. Reflecting on these challenges demonstrates technical maturity and problem-solving resilience.")

    # 6.2.1 ASP.NET Core Learning Difficulties
    format_heading(doc, "6.2.1 Learning Difficulties Encountered with ASP.NET Core & C#", level=2)
    
    format_bullet(doc, "1. Strict Static Typing & Asynchronous Pipeline (async/await)", 
        "Coming from dynamically typed environments, mastering C#'s static type system and asynchronous task-based patterns (Task<IActionResult>, await, async) required significant mental realignment. In early iterations, blocking calls like .Result or .Wait() caused thread starvation on the ASP.NET Core Kestrel thread pool, leading to sluggish response times during concurrent room searches. This was resolved by adopting non-blocking asynchronous streaming (.ToListAsync(), .CountAsync(), .SumAsync()) throughout all controllers.")

    format_bullet(doc, "2. Entity Framework Core (EF Core) ORM Complexities", 
        "Object-Relational Mapping (ORM) introduced unexpected friction: \n"
        "• Circular Navigation References: When querying Bookings with .Include(b => b.Customer) and .Include(b => b.Room), the default JSON serializer threw fatal circular loop exceptions because Customer also possessed a collection of Bookings. This required configuring custom DTOs (Data Transfer Objects) and projection expressions to decouple entities from serialization payloads.\n"
        "• The N+1 Query Problem: In early tests, iterating over room records caused EF Core to issue secondary SQL SELECT queries for each individual booking. This was remediated by executing eager loading via .Include() and grouping logic within a single optimized SQL JOIN.")

    format_bullet(doc, "3. Dependency Injection (DI) & Middleware Pipeline", 
        "Configuring ASP.NET Core's Program.cs required deep understanding of service lifetimes. Early confusion between Scoped (per-request DbContext) and Transient services caused DbContext concurrency exceptions when multiple async tasks attempted to use the same database connection simultaneously. Properly scoping HotelDbContext resolved this issue.")

    format_bullet(doc, "4. Cross-Origin Resource Sharing (CORS) Bottlenecks", 
        "Because the React frontend runs on Vite (http://localhost:5173) and the ASP.NET Core backend operates on (http://localhost:5000), cross-origin requests were initially blocked by browser security headers. Configuring a permissive CORS policy (app.UseCors(\"AllowAll\")) before app.UseAuthorization() in the middleware pipeline was critical to establishing seamless client-server communication.")

    # 6.2.2 API Testing & Integration Issues
    format_heading(doc, "6.2.2 API Testing & Integration Bottlenecks", level=2)
    format_body_p(doc, 
        "Testing distributed RESTful endpoints revealed multiple integration bottlenecks between the React client and the ASP.NET Core backend:")

    format_bullet(doc, "1. Temporal DateTime Offset & Serialization Mismatch", 
        "A major testing bug occurred when date pickers in React transmitted dates as ISO-8601 strings with local timezone offsets (e.g., '2026-10-10T18:30:00.000Z'). Because Sri Lanka is UTC+5:30, unparsed UTC conversions shifted the date by minus one day in the database (recording October 9th instead of October 10th). This was resolved by strictly standardizing on DateOnly and UTC midnight (DateTime.UtcNow.Date), stripping timezone offsets before executing overlap queries.")

    format_bullet(doc, "2. Semantic HTTP Status Code Management", 
        "In early development, all API responses returned generic HTTP 200 OK, with error messages embedded in JSON (e.g., { status: 'error' }). This prevented the React frontend from utilizing native try/catch and status-based conditional alerts. During testing, the backend was refactored to adhere to strict REST semantics: HTTP 409 Conflict for double-booking overlaps, HTTP 400 Bad Request for headcount violations, and HTTP 404 Not Found for missing suites.")

    format_bullet(doc, "3. Concurrency Simulation under Load", 
        "Simulating race conditions (two browser sessions attempting to confirm Room #101 for October 10–15 within milliseconds of each other) using Postman runner proved that client-side validation alone was useless. Only the backend database-level interval query successfully trapped the race condition, returning 409 Conflict to the slower transaction.")

    # Table of Technical Difficulties & Solutions
    format_heading(doc, "6.2.3 Synthesis of Technical Challenges and Architectural Solutions", level=2)
    tbl_diff = doc.add_table(rows=6, cols=4)
    w_diff = [1.5, 1.8, 1.8, 1.4]
    h_diff = ["Technical Challenge Area", "Observed Symptom / Bottleneck", "Root Cause Analysis", "Applied Engineering Solution"]
    d_diff = [
        ("Asynchronous Deadlocks", "Sluggish response times during concurrent searches", "Misuse of synchronous .Result on async EF Core tasks", "Complete refactoring to async/await with non-blocking .ToListAsync()"),
        ("Circular JSON Exceptions", "API crashed with 500 Internal Error on /api/bookings", "Two-way navigational properties between Customer and Booking entities", "Implemented flat DTO projection models to strip entity back-references"),
        ("Date Timezone Drift", "Bookings shifted by -1 day in database (Oct 9 instead of Oct 10)", "Browser transmitted local UTC+5:30 offset parsed into UTC midnight", "Enforced strict .Date normalization and UTC synchronization at API entry"),
        ("CORS Pre-Flight Rejection", "Browser blocked all POST and PUT requests from React", "Missing CORS middleware and pre-flight OPTIONS handler in ASP.NET Core", "Registered AddCors with explicit origin policy in Program.cs pipeline"),
        ("Double-Booking Race Condition", "Two concurrent requests could book the same suite in memory", "Reliance on client-side state without database transactional locking", "Enforced Allen's interval check inside BookingsController returning HTTP 409")
    ]
    style_table(tbl_diff, w_diff, h_diff, d_diff)

    # =========================================================================
    # 6.3 LESSONS LEARNED & PERSONAL PROFESSIONAL DEVELOPMENT
    # =========================================================================
    format_heading(doc, "6.3 Lessons Learned & Professional Development", level=1)
    format_body_p(doc, 
        "Executing the Dutch Point Negombo system provided immense personal and academic growth for the lead developer:")

    format_bullet(doc, "1. The Primacy of Server-Side Validation", 
        "Client-side UI validation (HTML5 required attributes or React state) exists solely for user convenience and feedback; it provides zero actual security. All operational rules—capacity limits, date intervals, financial math, and role authorization—must be enforced deterministically at the backend boundary.")

    format_bullet(doc, "2. Data Modeling Discipline Over Cosmetic Design", 
        "A visually attractive frontend is worthless if the database schema is fragile. Investing significant effort into third normal form (3NF) relational normalization and foreign key cascading constraints prevented data corruption and orphaned records.")

    format_bullet(doc, "3. Iterative Testing with Swagger and Postman", 
        "Testing API endpoints independently before building React user interfaces isolated bugs early, saving dozens of hours of complex full-stack debugging.")

    # =========================================================================
    # 6.4 FUTURE SYSTEM ENHANCEMENTS (PHASE 2 ROADMAP)
    # =========================================================================
    format_heading(doc, "6.4 Future System Enhancements (Phase 2 Production Roadmap)", level=1)
    format_body_p(doc, 
        "While the current Interim system successfully realizes all core functional requirements, commercial production deployment demands enterprise-grade hardening. The following architectural upgrades constitute the Phase 2 development roadmap:")

    # 6.4.1 Proper Password Hashing
    format_heading(doc, "6.4.1 Cryptographic Password Hashing & JWT Security Architecture", level=2)
    format_body_p(doc, 
        "In the Interim prototype, demonstration credentials were kept in readable format to facilitate examiner evaluation and rapid testing. For production, plain-text storage is completely unacceptable under the General Data Protection Regulation (GDPR) and Sri Lanka Data Protection Act No. 9 of 2022.")

    add_callout_box(doc, "Production Cryptographic Strategy",
        "1. Adaptive Salted Hashing: Integrate BCrypt.Net-Next (work factor 12) or Argon2id to hash all customer and administrator passwords with a cryptographically secure random 128-bit salt.\n"
        "2. Protection Against Rainbow Tables: Unique salts ensure identical passwords produce radically different hashes, completely neutralizing pre-computed lookup tables.\n"
        "3. Secure JWT Authentication: Replace basic JSON authentication payloads with signed JSON Web Tokens (HMAC-SHA256) stored in HttpOnly, SameSite=Strict cookies to eliminate Cross-Site Scripting (XSS) token theft.")

    code_hash = """// Production Enhancement: BCrypt Hashing in AuthController.cs
using BCrypt.Net;

// 1. REGISTRATION: Hash password with automatic salt generation (Work factor = 12)
var newUser = new Customer
{
    FullName = request.FullName.Trim(),
    Email = request.Email.Trim().ToLower(),
    PasswordHash = BCrypt.HashPassword(request.Password, workFactor: 12),
    Role = "Customer",
    CreatedAt = DateTime.UtcNow
};

// 2. LOGIN: Cryptographically verify password against stored hash
var user = await _context.Customers.FirstOrDefaultAsync(u => u.Email == identifier);
if (user == null || !BCrypt.Verify(request.Password, user.PasswordHash))
{
    return Unauthorized(new { message = "Invalid email or password." });
}"""
    format_code_block(doc, code_hash, "Code Listing 6.1: Proposed Production Password Hashing with BCrypt.Net-Next")

    # 6.4.2 Two-Factor Authentication
    format_heading(doc, "6.4.2 Two-Factor Authentication (2FA / Multi-Factor Authentication)", level=2)
    format_body_p(doc, 
        "Because administrative access grants control over room pricing, reservation cancellations, and guest personal data, administrative accounts present a high-value attack target. Single-factor username/password authentication is vulnerable to credential stuffing and phishing.")

    format_bullet(doc, "Time-Based One-Time Password (TOTP - RFC 6238)", 
        "Administrators will be required to register a mobile authenticator app (Google Authenticator, Microsoft Authenticator). Upon entering valid primary credentials, the backend generates an ephemeral 30-second cryptographic token validated via Otp.NET. Access to the Inventory Management panel will remain locked until the 6-digit TOTP is confirmed.")

    format_bullet(doc, "SMS / Email OTP Fallback", 
        "For guests completing high-value suite bookings in Sri Lankan Rupees (LKR), an automated One-Time Password will be dispatched via Twilio SMS to their verified Sri Lankan mobile number (+94), preventing automated reservation spam and malicious inventory locking.")

    # 6.4.3 Dedicated Admin Dashboard
    format_heading(doc, "6.4.3 Advanced Executive Admin Dashboard & Analytics Portal", level=2)
    format_body_p(doc, 
        "The current interim implementation features an integrated room inventory view. Phase 2 will expand this into an enterprise-grade standalone executive portal featuring:")

    format_bullet(doc, "Interactive Visual Telemetry (Chart.js / Recharts)", 
        "Dynamic interactive graphs visualizing Monthly Revenue Yield in LKR, Average Daily Rate (ADR), and Revenue Per Available Room (RevPAR).")

    format_bullet(doc, "Interactive Room Schedule Gantt Timeline", 
        "A visual 30-day horizontal timeline allowing front-desk receptionists to drag and drop guest suite allocations, inspect housekeeping cleaning statuses, and manage room maintenance lockouts.")

    format_bullet(doc, "Automated PDF Folio & Invoice Generation", 
        "Server-side generation of branded PDF receipts, detailed tax breakdowns (VAT / Tourism Development Levy), and customer checkout folios using QuestPDF.")

    # 6.4.4 Payment Gateway Integration
    format_heading(doc, "6.4.4 Direct Online Payment Gateway Integration (IPG / PayHere / Stripe)", level=2)
    format_body_p(doc, 
        "To achieve a true commercial production standard, Phase 2 will integrate a certified Payment Gateway (such as PayHere Sri Lanka or Stripe). Currently, reservations are marked Confirmed upon booking creation. In Phase 2, a 15-minute temporary reservation lock will be initiated, which transitions to Confirmed only upon receipt of a cryptographically signed webhook notification confirming successful credit/debit card charge in Sri Lankan Rupees (LKR).")

    # =========================================================================
    # 6.5 SUMMARY & VIVA VOCE REFLECTION SCRIPT
    # =========================================================================
    format_heading(doc, "6.5 Chapter 06 Summary & Viva Voce Reflection Guide", level=1)
    
    add_callout_box(doc, "30-Second Viva Answer: Reflection, Difficulties & Future Work",
        "Examiner: 'Pasindu, what were your biggest technical difficulties during development, and what does the future build look like?'\n\n"
        "Your Answer:\n"
        "\"Sir/Madam, our primary technical hurdle was transitioning to ASP.NET Core's asynchronous paradigm and EF Core ORM navigation complexities—specifically solving circular JSON serialization and preventing date timezone shifts between React and C#.\n"
        "We also discovered during API testing that double-booking prevention must be strictly enforced at the database query level using Allen's interval algebra.\n"
        "For our Phase 2 production roadmap, we have designed three major enhancements:\n"
        "First, replacing demonstration credentials with industry-standard BCrypt work-factor-12 password hashing and JWT token rotation.\n"
        "Second, implementing Two-Factor Authentication (TOTP via Google Authenticator) for administrative accounts to protect financial records.\n"
        "Third, expanding the admin module into a dedicated visual dashboard with interactive Gantt timeline room scheduling and automated LKR payment gateway integration.\"")

    out_docx = os.path.join(base_dir, "Chapter_06_Critical_Evaluation_Reflection_and_Future_Work.docx")
    doc.save(out_docx)
    print(f"Chapter 06 DOCX successfully created: {out_docx}")

if __name__ == "__main__":
    build_chapter6_doc()
