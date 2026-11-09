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

def add_qa_card_docx(doc, q_num, question, why_ask, answer_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, "FFFFFF")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="0F2C59"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    r_q = p.add_run(f"Q{q_num}: {question}\n")
    r_q.font.name = 'Calibri'
    r_q.font.size = Pt(10.5)
    r_q.font.bold = True
    r_q.font.color.rgb = RGBColor(15, 44, 89)
    
    r_why = p.add_run(f"Why the examiner asks this: {why_ask}\n\n")
    r_why.font.name = 'Calibri'
    r_why.font.size = Pt(9)
    r_why.font.italic = True
    r_why.font.color.rgb = RGBColor(184, 134, 11)
    
    r_ans_label = p.add_run("Winning Model Answer:\n")
    r_ans_label.font.name = 'Calibri'
    r_ans_label.font.size = Pt(9.5)
    r_ans_label.font.bold = True
    r_ans_label.font.color.rgb = RGBColor(15, 44, 89)
    
    r_ans = p.add_run(answer_text)
    r_ans.font.name = 'Calibri'
    r_ans.font.size = Pt(9.5)
    r_ans.font.color.rgb = RGBColor(40, 44, 52)
    
    # Add a spacer paragraph after table
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(6)

def format_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    run = h.runs[0]
    run.font.name = 'Calibri'
    if level == 1:
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 44, 89)
    elif level == 2:
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(184, 134, 11)
    return h

def build_viva_qa_doc():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    base_dir = r"C:\Users\PASINDU\Desktop\Interim"
    
    tp = doc.add_paragraph()
    tp.paragraph_format.space_after = Pt(2)
    r1 = tp.add_run("ESOFT METRO CAMPUS • FACULTY OF COMPUTING • BIT (HONS) DEGREE\n")
    r1.font.name = 'Calibri'
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(184, 134, 11)
    
    r2 = tp.add_run("INTERIM VIVA VOCE DEFENSE GUIDE: TOP 12 EXAMINER QUESTIONS & MODEL ANSWERS")
    r2.font.name = 'Calibri'
    r2.font.size = Pt(17)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(15, 44, 89)
    
    mp = doc.add_paragraph()
    mp.paragraph_format.space_after = Pt(12)
    rm = mp.add_run("Dutch Point Negombo Web-Based Hotel Management System • Preparation & Defense Manual\n"
                    "Team Lead: I.D.P.N Iddamalgoda (E269559) • Team Members: H.M.Y.R Herath, Y.M.A.Y Bandara, A.G.H.H Jinadasa")
    rm.font.name = 'Calibri'
    rm.font.size = Pt(9.5)
    rm.font.italic = True
    rm.font.color.rgb = RGBColor(100, 116, 139)
    
    hr_p = doc.add_paragraph()
    hr_p.paragraph_format.space_after = Pt(12)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="0F2C59"/></w:pBdr>')
    hr_p._p.get_or_add_pPr().append(pBdr)

    # Cat 1
    format_heading(doc, "1. Core Business Logic & Concurrency Control (Guaranteed to be Asked)", level=1)
    add_qa_card_docx(doc, 1, "How did you prevent double-booking in your system?",
        "Checks whether you implemented real backend validation or just relied on frontend date pickers.",
        "\"Sir/Madam, we prevent double booking at the database query tier in BookingsController.cs using Allen's Interval Algebra. Before saving a booking, the backend queries whether any existing confirmed booking satisfies both conditions: ExistingCheckIn < RequestedCheckOut AND ExistingCheckOut > RequestedCheckIn. If both evaluate to true, an overlap exists. The system halts the transaction, writes zero records to MySQL, and returns an HTTP 409 Conflict error carrying diagnostic conflict details to the frontend.\"")

    add_qa_card_docx(doc, 2, "What happens if two users click 'Confirm Booking' at the exact same second for the same room?",
        "Tests your understanding of distributed race conditions and database transaction concurrency.",
        "\"Even if both users see the room as available and open the modal simultaneously, MySQL executes the transactions sequentially under ACID transaction isolation. The first transaction commits successfully. When the second transaction executes, its date-overlap check queries the updated database state, detects the collision, and rejects the second user with an HTTP 409 Conflict without corrupting room inventory.\"")

    add_qa_card_docx(doc, 3, "Why didn't you just change the Room table status to 'Occupied' when a room is booked?",
        "A classic examiner trap! Amateur systems mutate a static status column, causing permanent room lockouts.",
        "\"Because room availability is temporal, not permanent. A room occupied today will be completely vacant next week. If we change the room table's status to 'Occupied', the room becomes permanently unavailable for all future dates. Instead, our system uses dynamic in-memory projection: we query only the bookings overlapping with the user's specific requested dates, leaving the static room record intact.\"")

    # Cat 2
    format_heading(doc, "2. System Architecture & Component Integration", level=1)
    add_qa_card_docx(doc, 4, "How does your React frontend communicate with your ASP.NET Core backend?",
        "Verifies if you understand client-server networking, port allocation, and REST API standards.",
        "\"They communicate over HTTP using asynchronous RESTful JSON endpoints. The React frontend runs on Vite on port 5173, and the ASP.NET Core backend listens on port 5000. When a user interacts with the UI, React uses fetch() to send requests to endpoints like http://localhost:5000/api/rooms. We configured CORS middleware (app.UseCors('AllowAll')) in Program.cs to permit cross-origin communication between the two ports.\"")

    add_qa_card_docx(doc, 5, "Why did you choose a Decoupled 3-Tier Architecture instead of a traditional monolithic MVC?",
        "Tests your ability to provide academic and technical justification for your architectural choices.",
        "\"A decoupled architecture separates concerns cleanly: React 19 handles the presentation state via its Virtual DOM without full page reloads, ASP.NET Core encapsulates business validation, and MySQL 8.0 ensures ACID transactional persistence. This allows independent scalability, easier testing via Swagger, and the flexibility to connect future mobile apps to the same API.\"")

    # Cat 3
    format_heading(doc, "3. Security & Role-Based Access Control (RBAC)", level=1)
    add_qa_card_docx(doc, 6, "How do you prevent a regular customer from registering as an Administrator?",
        "Checks for privilege escalation vulnerabilities in your user onboarding pipeline.",
        "\"We enforce a server-side anti-privilege escalation guard in AuthController.cs. In the registration endpoint, the backend strictly hardcodes newUser.Role = 'Customer', completely ignoring any role submitted by the client payload. Administrative accounts cannot be self-registered online; they can only be pre-seeded directly in the database.\"")

    add_qa_card_docx(doc, 7, "Why are passwords stored as plain text in this build, and how will you fix it?",
        "They will notice the plain-text password in AuthController.cs and test your awareness of security standards.",
        "\"Sir/Madam, plain-text credentials were maintained temporarily during the 55% interim stage solely to facilitate rapid examiner testing and evaluation. As documented in our Chapter 06 Future Roadmap, Phase 2 will replace this with salted BCrypt.Net (work factor 12) hashing and signed JWT (JSON Web Tokens) to comply with Sri Lanka's Personal Data Protection Act No. 9 of 2022.\"")

    # Cat 4
    format_heading(doc, "4. Database Design & Relational Data Integrity", level=1)
    add_qa_card_docx(doc, 8, "What happens if an admin tries to delete a room that already has active guest reservations?",
        "Tests whether your system enforces relational referential integrity or allows orphaned records.",
        "\"The system strictly prevents it. In RoomsController.cs, before executing a deletion, the backend checks .AnyAsync(b => b.RoomId == id && b.BookingStatus == 'Confirmed'). If active bookings exist, the backend aborts with an HTTP 400 Bad Request error. Furthermore, our MySQL schema enforces foreign key rules (ON DELETE RESTRICT) to prevent orphaned financial records.\"")

    add_qa_card_docx(doc, 9, "Why did you use DECIMAL(10,2) instead of FLOAT or DOUBLE for room prices in LKR?",
        "Tests your knowledge of financial computing and floating-point arithmetic precision.",
        "\"In financial systems, binary floating-point types (float and double) suffer from IEEE 754 precision drift and rounding errors. We used DECIMAL(10,2) in MySQL and decimal in C# because they represent exact fixed-point values, ensuring accurate billing in Sri Lankan Rupees (LKR).\"")

    # Cat 5
    format_heading(doc, "5. Quality Assurance, Reflections & Phase 2 Roadmap", level=1)
    add_qa_card_docx(doc, 10, "How did you test your backend APIs before connecting them to React?",
        "Verifies whether your development followed a disciplined Software Engineering QA methodology.",
        "\"We integrated Swagger UI and OpenAPI directly at http://localhost:5000/swagger, alongside Postman. This allowed us to test all CRUD endpoints, model validations, and simulate double-booking boundary cases independently before integrating the frontend.\"")

    add_qa_card_docx(doc, 11, "What was your biggest technical challenge during development?",
        "Tests self-reflection, problem-solving maturity, and authentic developer experience.",
        "\"Our main hurdle was adapting to ASP.NET Core's asynchronous threading pipeline and resolving circular entity loops in Entity Framework Core when serializing related Customer and Booking data. We solved this by designing clean, flat Data Transfer Objects (DTOs). We also resolved a date timezone offset bug where Sri Lanka's UTC+5:30 offset shifted dates backward by one day, which we fixed by enforcing DateTime.UtcNow.Date normalization.\"")

    add_qa_card_docx(doc, 12, "What is remaining for your final submission (Phase 2)?",
        "Checks if you have a realistic, well-defined plan to reach 100% completion.",
        "\"For Phase 2, we will deliver four key production modules: 1. Salted BCrypt password hashing and JWT authentication; 2. Two-Factor Authentication (TOTP via Google Authenticator) for administrators; 3. An executive analytics dashboard with interactive room schedule timelines; 4. Direct online payment gateway integration (PayHere / Stripe) for live LKR card settlements.\"")

    out_docx = os.path.join(base_dir, "Dutch_Point_Negombo_Viva_Voce_Examiner_QA_Guide.docx")
    doc.save(out_docx)
    print("Viva QA DOCX successfully created:", out_docx)

if __name__ == "__main__":
    build_viva_qa_doc()
