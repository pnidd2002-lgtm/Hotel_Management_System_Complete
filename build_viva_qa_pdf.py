import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        if self._pageNumber > 1:
            self.drawString(54, 750, "Dutch Point Negombo — Interim Viva Voce Defense Guide (Top 12 Questions)")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "BIT (Hons) Software Engineering • Interim Viva Voce Preparation Manual")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()

def create_viva_qa_pdf():
    out_pdf = r"C:\Users\PASINDU\Desktop\Interim\Dutch_Point_Negombo_Viva_Voce_Examiner_QA_Guide.pdf"
    doc = SimpleDocTemplate(
        out_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    c_navy = colors.HexColor("#0F2C59")
    c_gold = colors.HexColor("#B8860B")
    c_dark = colors.HexColor("#1E293B")
    c_slate = colors.HexColor("#475569")
    c_bg = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#CBD5E1")
    c_green = colors.HexColor("#10B981")
    c_blue = colors.HexColor("#2563EB")

    style_pretitle = ParagraphStyle(
        'PreTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=12,
        textColor=c_gold, spaceAfter=4
    )
    style_title = ParagraphStyle(
        'MainTitle', parent=styles['Title'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=c_navy, alignment=0, spaceAfter=6
    )
    style_meta = ParagraphStyle(
        'MetaSubtitle', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=9, leading=13,
        textColor=c_slate, spaceAfter=12
    )
    style_cat = ParagraphStyle(
        'Category_Heading', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=13, leading=16,
        textColor=c_navy, spaceBefore=14, spaceAfter=6, keepWithNext=True
    )
    style_q_title = ParagraphStyle(
        'Q_Title', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=13,
        textColor=c_navy, spaceBefore=6, spaceAfter=2
    )
    style_why = ParagraphStyle(
        'Why_Text', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8.5, leading=11.5,
        textColor=c_gold, spaceAfter=4
    )
    style_ans = ParagraphStyle(
        'Ans_Text', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=c_dark
    )

    story = []

    def add_qa_card(q_num, question, why_ask, answer_text):
        content = [
            Paragraph(f"<b>Q{q_num}: {question}</b>", style_q_title),
            Paragraph(f"<b>Why the examiner asks this:</b> {why_ask}", style_why),
            Spacer(1, 2),
            Paragraph(f"<b>Winning Model Answer:</b><br/>{answer_text}", style_ans)
        ]
        t = Table([[content]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
            ('BOX', (0,0), (-1,-1), 0.8, c_border),
            ('LINELEFT', (0,0), (0,-1), 3.5, c_navy),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))

    # COVER HEADER
    story.append(Paragraph("ESOFT METRO CAMPUS • FACULTY OF COMPUTING • BIT (HONS) DEGREE", style_pretitle))
    story.append(Paragraph("Interim Viva Voce Defense Guide: Top 12 Questions & Answers", style_title))
    story.append(Paragraph(
        "Dutch Point Negombo Web-Based Hotel Management System • Technical Rationale, Code Evidence & Examiner Q&A<br/>"
        "<b>Team Lead:</b> I.D.P.N Iddamalgoda (E269559) • <b>Team Members:</b> H.M.Y.R Herath (E267614), Y.M.A.Y Bandara (E267609), A.G.H.H Jinadasa (E267612)",
        style_meta
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_navy, spaceBefore=0, spaceAfter=10))

    # =========================================================================
    # CATEGORY 1: CORE ALGORITHM & CONCURRENCY
    # =========================================================================
    story.append(Paragraph("1. Core Business Logic & Concurrency Control", style_cat))
    
    add_qa_card(
        1,
        "How did you prevent double-booking in your system?",
        "Checks whether you implemented real backend validation or just relied on frontend date pickers.",
        "<i>\"Sir/Madam, we prevent double booking at the database query tier in <code>BookingsController.cs</code> using Allen’s Interval Algebra. Before saving a booking, the backend queries whether any existing confirmed booking satisfies both conditions: <code>ExistingCheckIn &lt; RequestedCheckOut</code> <b>AND</b> <code>ExistingCheckOut &gt; RequestedCheckIn</code>. If both evaluate to true, an overlap exists. The system halts the transaction, writes zero records to MySQL, and returns an <b>HTTP 409 Conflict</b> error carrying diagnostic conflict details to the frontend.\"</i>"
    )

    add_qa_card(
        2,
        "What happens if two users click 'Confirm Booking' at the exact same second for the same room?",
        "Tests your understanding of distributed race conditions and database transaction concurrency.",
        "<i>\"Even if both users see the room as available and open the modal simultaneously, MySQL executes the transactions sequentially under ACID transaction isolation. The first transaction commits successfully. When the second transaction executes, its date-overlap check queries the updated database state, detects the collision, and rejects the second user with an HTTP 409 Conflict without corrupting room inventory.\"</i>"
    )

    add_qa_card(
        3,
        "Why didn't you just change the Room table status to 'Occupied' when a room is booked?",
        "A classic examiner trap! Amateur systems mutate a static status column, causing permanent room lockouts.",
        "<i>\"Because room availability is <b>temporal</b>, not permanent. A room occupied today will be completely vacant next week. If we change the room table's status to 'Occupied', the room becomes permanently unavailable for all future dates. Instead, our system uses <b>dynamic in-memory projection</b>: we query only the bookings overlapping with the user's specific requested dates, leaving the static room record intact.\"</i>"
    )

    # =========================================================================
    # CATEGORY 2: ARCHITECTURE & TECHNOLOGY INTEGRATION
    # =========================================================================
    story.append(Paragraph("2. System Architecture & Component Integration", style_cat))

    add_qa_card(
        4,
        "How does your React frontend communicate with your ASP.NET Core backend?",
        "Verifies if you understand client-server networking, port allocation, and REST API standards.",
        "<i>\"They communicate over HTTP using asynchronous RESTful JSON endpoints. The React frontend runs on Vite on port <code>5173</code>, and the ASP.NET Core backend listens on port <code>5000</code>. When a user interacts with the UI, React uses <code>fetch()</code> to send requests to endpoints like <code>http://localhost:5000/api/rooms</code>. We configured <b>CORS middleware (<code>app.UseCors('AllowAll')</code>)</b> in <code>Program.cs</code> to permit cross-origin communication between the two ports.\"</i>"
    )

    add_qa_card(
        5,
        "Why did you choose a Decoupled 3-Tier Architecture instead of a traditional monolithic MVC?",
        "Tests your ability to provide academic and technical justification for your architectural choices.",
        "<i>\"A decoupled architecture separates concerns cleanly: React 19 handles the presentation state via its Virtual DOM without full page reloads, ASP.NET Core encapsulates business validation, and MySQL 8.0 ensures ACID transactional persistence. This allows independent scalability, easier testing via Swagger, and the flexibility to connect future mobile apps to the same API.\"</i>"
    )

    # =========================================================================
    # CATEGORY 3: SECURITY & IDENTITY GOVERNANCE (RBAC)
    # =========================================================================
    story.append(Paragraph("3. Security & Role-Based Access Control (RBAC)", style_cat))

    add_qa_card(
        6,
        "How do you prevent a regular customer from registering as an Administrator?",
        "Checks for privilege escalation vulnerabilities in your user onboarding pipeline.",
        "<i>\"We enforce a server-side anti-privilege escalation guard in <code>AuthController.cs</code>. In the registration endpoint, the backend strictly hardcodes <code>newUser.Role = 'Customer'</code>, completely ignoring any role submitted by the client payload. Administrative accounts cannot be self-registered online; they can only be pre-seeded directly in the database.\"</i>"
    )

    add_qa_card(
        7,
        "Why are passwords stored as plain text in this build, and how will you fix it?",
        "They will notice the plain-text password in AuthController.cs and test your awareness of security standards.",
        "<i>\"Sir/Madam, plain-text credentials were maintained temporarily during the 55% interim stage solely to facilitate rapid examiner testing and evaluation. As documented in our Chapter 06 Future Roadmap, Phase 2 will replace this with salted <b>BCrypt.Net (work factor 12)</b> hashing and signed <b>JWT (JSON Web Tokens)</b> to comply with Sri Lanka’s Personal Data Protection Act No. 9 of 2022.\"</i>"
    )

    # =========================================================================
    # CATEGORY 4: DATABASE INTEGRITY & FINANCIAL PRECISION
    # =========================================================================
    story.append(Paragraph("4. Database Design & Relational Data Integrity", style_cat))

    add_qa_card(
        8,
        "What happens if an admin tries to delete a room that already has active guest reservations?",
        "Tests whether your system enforces relational referential integrity or allows orphaned records.",
        "<i>\"The system strictly prevents it. In <code>RoomsController.cs</code>, before executing a deletion, the backend checks <code>.AnyAsync(b =&gt; b.RoomId == id &amp;&amp; b.BookingStatus == 'Confirmed')</code>. If active bookings exist, the backend aborts with an HTTP 400 Bad Request error. Furthermore, our MySQL schema enforces foreign key rules (<code>ON DELETE RESTRICT</code>) to prevent orphaned financial records.\"</i>"
    )

    add_qa_card(
        9,
        "Why did you use DECIMAL(10,2) instead of FLOAT or DOUBLE for room prices in LKR?",
        "Tests your knowledge of financial computing and floating-point arithmetic precision.",
        "<i>\"In financial systems, binary floating-point types (<code>float</code> and <code>double</code>) suffer from IEEE 754 precision drift and rounding errors. We used <code>DECIMAL(10,2)</code> in MySQL and <code>decimal</code> in C# because they represent exact fixed-point values, ensuring accurate billing in Sri Lankan Rupees (LKR).\"</i>"
    )

    # =========================================================================
    # CATEGORY 5: TESTING, REFLECTIONS & FUTURE ROADMAP
    # =========================================================================
    story.append(Paragraph("5. Quality Assurance, Reflections & Phase 2 Roadmap", style_cat))

    add_qa_card(
        10,
        "How did you test your backend APIs before connecting them to React?",
        "Verifies whether your development followed a disciplined Software Engineering QA methodology.",
        "<i>\"We integrated <b>Swagger UI and OpenAPI</b> directly at <code>http://localhost:5000/swagger</code>, alongside <b>Postman</b>. This allowed us to test all CRUD endpoints, model validations, and simulate double-booking boundary cases independently before integrating the frontend.\"</i>"
    )

    add_qa_card(
        11,
        "What was your biggest technical challenge during development?",
        "Tests self-reflection, problem-solving maturity, and authentic developer experience.",
        "<i>\"Our main hurdle was adapting to ASP.NET Core's asynchronous threading pipeline and resolving circular entity loops in Entity Framework Core when serializing related <code>Customer</code> and <code>Booking</code> data. We solved this by designing clean, flat Data Transfer Objects (DTOs). We also resolved a date timezone offset bug where Sri Lanka's UTC+5:30 offset shifted dates backward by one day, which we fixed by enforcing <code>DateTime.UtcNow.Date</code> normalization.\"</i>"
    )

    add_qa_card(
        12,
        "What is remaining for your final submission (Phase 2)?",
        "Checks if you have a realistic, well-defined plan to reach 100% completion.",
        "<i>\"For Phase 2, we will deliver four key production modules: 1. Salted BCrypt password hashing and JWT authentication; 2. Two-Factor Authentication (TOTP via Google Authenticator) for administrators; 3. An executive analytics dashboard with interactive room schedule timelines; 4. Direct online payment gateway integration (PayHere / Stripe) for live LKR card settlements.\"</i>"
    )

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Viva QA PDF successfully created:", out_pdf)

if __name__ == "__main__":
    create_viva_qa_pdf()
