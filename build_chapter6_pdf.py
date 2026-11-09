import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
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
            self.drawString(54, 750, "Chapter 06: Critical Evaluation, Reflection & Future Work — Dutch Point Negombo")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "BIT (Hons) Software Engineering • Interim Report Critical Evaluation")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()

def create_chapter6_pdf():
    out_pdf = r"C:\Users\PASINDU\Desktop\Interim\Chapter_06_Critical_Evaluation_Reflection_and_Future_Work.pdf"
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
    style_h1 = ParagraphStyle(
        'Heading1_Custom', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=13, leading=16,
        textColor=c_navy, spaceBefore=12, spaceAfter=5, keepWithNext=True
    )
    style_h2 = ParagraphStyle(
        'Heading2_Custom', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=c_gold, spaceBefore=9, spaceAfter=3, keepWithNext=True
    )
    style_body = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=c_dark, spaceAfter=5
    )
    style_bullet = ParagraphStyle(
        'Bullet_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.8, leading=12.5,
        textColor=c_dark, leftIndent=12, spaceAfter=3
    )
    style_code = ParagraphStyle(
        'Code_Custom', parent=styles['Normal'],
        fontName='Courier', fontSize=7.5, leading=10,
        textColor=colors.HexColor("#E2E8F0")
    )
    style_callout_t = ParagraphStyle(
        'CalloutTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=11,
        textColor=c_navy, spaceAfter=2
    )
    style_callout_b = ParagraphStyle(
        'CalloutBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11.5,
        textColor=c_dark
    )

    story = []

    def add_callout(title, body_text):
        content = [
            Paragraph(f"<b>CRITICAL HIGHLIGHT:</b> {title}", style_callout_t),
            Spacer(1, 2),
            Paragraph(body_text, style_callout_b)
        ]
        t = Table([[content]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
            ('BOX', (0,0), (-1,-1), 0.5, c_border),
            ('LINELEFT', (0,0), (0,-1), 3.5, c_navy),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

    def add_code_block(code_str, caption=""):
        p = Paragraph(code_str.replace('\n', '<br/>').replace(' ', '&nbsp;'), style_code)
        t = Table([[p]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#334155")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
        if caption:
            c_p = Paragraph(f"<i>{caption}</i>", ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=7.5, leading=9, textColor=c_slate, alignment=1))
            story.append(Spacer(1, 1))
            story.append(c_p)
        story.append(Spacer(1, 6))

    # COVER HEADER
    story.append(Paragraph("DUTCH POINT NEGOMBO • SOFTWARE ENGINEERING INTERIM DISSERTATION", style_pretitle))
    story.append(Paragraph("Chapter 06: Critical Evaluation, Reflection & Future Roadmap", style_title))
    story.append(Paragraph("Self-Reflection, ASP.NET Core & API Testing Bottlenecks, BCrypt Hashing, 2FA & Phase 2 Roadmaps<br/><b>Author:</b> Pasindu Nirmal Iddamalgoda (Student ID: E269559) • Lead Developer", style_meta))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_navy, spaceBefore=0, spaceAfter=10))

    # 6.1 CRITICAL EVALUATION
    story.append(Paragraph("6.1 Critical Evaluation of the Developed System", style_h1))
    story.append(Paragraph(
        "Chapter 06 delivers a rigorous, self-critical appraisal of the Dutch Point Negombo hotel management system. Academic standards require identifying both technical successes and real-world operational bottlenecks encountered during full-stack development.",
        style_body
    ))
    add_callout(
        "Key Interim Triumphs vs Original Baseline",
        "• <b>Concurrency Integrity:</b> Successfully trapped double-booking race conditions using Allen's Interval Algebra at the database query tier.<br/>"
        "• <b>Multi-Tier Decoupling:</b> Proved the viability of a modern decoupled architecture (React 19 + ASP.NET Core C# + PostgreSQL).<br/>"
        "• <b>Financial Precision:</b> Standardized all room rates and billing in Sri Lankan Rupees (LKR) with decimal(18,2) precision."
    )

    # 6.2 TECHNICAL REFLECTION
    story.append(Paragraph("6.2 Technical Reflection: ASP.NET Core & API Testing Challenges", style_h1))
    story.append(Paragraph("<b>6.2.1 ASP.NET Core Learning Difficulties</b>", style_h2))
    story.append(Paragraph("• <b>Asynchronous Pipeline (async/await):</b> Overcame early Kestrel thread starvation caused by blocking <code>.Result</code> calls by migrating completely to non-blocking streaming (<code>.ToListAsync()</code>, <code>.CountAsync()</code>).", style_bullet))
    story.append(Paragraph("• <b>Circular Entity References:</b> Resolved JSON serializer crashes caused by bidirectional navigation properties between Customer and Booking by engineering flat Data Transfer Objects (DTOs).", style_bullet))
    story.append(Paragraph("• <b>Dependency Injection Scoping:</b> Addressed DbContext concurrency exceptions by properly configuring Scoped service lifetimes in Program.cs.", style_bullet))
    story.append(Paragraph("• <b>CORS Middleware Bottleneck:</b> Resolved browser cross-origin blocks between Vite (port 5173) and ASP.NET Core (port 5000) using <code>app.UseCors('AllowAll')</code>.", style_bullet))

    story.append(Paragraph("<b>6.2.2 API Testing & Integration Bottlenecks</b>", style_h2))
    story.append(Paragraph("• <b>DateTime Timezone Shift:</b> Fixed an issue where Sri Lanka's UTC+5:30 offset shifted dates backward by 1 day by enforcing UTC midnight (<code>DateTime.UtcNow.Date</code>) normalization.", style_bullet))
    story.append(Paragraph("• <b>Semantic HTTP Status Mapping:</b> Refactored generic 200 OK responses to return strict REST codes (HTTP 409 Conflict for double bookings, HTTP 400 for capacity limits).", style_bullet))
    story.append(Paragraph("• <b>Concurrency Stress Testing:</b> Used Postman runner to simulate rapid concurrent booking submissions, validating database-level transactional locking.", style_bullet))

    # TABLE OF CHALLENGES & REMEDIES
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 6.1: Technical Bottlenecks and Applied Solutions</b>", style_body))
    diff_data = [
        [Paragraph("<b>Challenge Area</b>", style_body), Paragraph("<b>Observed Bottleneck</b>", style_body), Paragraph("<b>Applied Solution</b>", style_body)],
        [Paragraph("Async Deadlocks", style_body), Paragraph("Sluggish response under load", style_body), Paragraph("Refactored to async/await streaming", style_body)],
        [Paragraph("Circular JSON Loops", style_body), Paragraph("500 Internal Error on /api/bookings", style_body), Paragraph("Decoupled via flat DTO projection models", style_body)],
        [Paragraph("DateTime Drift", style_body), Paragraph("Bookings saved on wrong calendar day", style_body), Paragraph("Normalized to UTC DateOnly at API entry", style_body)],
        [Paragraph("CORS Block", style_body), Paragraph("React requests blocked by browser", style_body), Paragraph("Registered AddCors middleware in Program.cs", style_body)],
        [Paragraph("Double Booking", style_body), Paragraph("In-memory race conditions", style_body), Paragraph("Database interval overlap query returning HTTP 409", style_body)]
    ]
    t_diff = Table(diff_data, colWidths=[120, 180, 204])
    t_diff.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg]),
    ]))
    story.append(t_diff)
    story.append(Spacer(1, 6))

    # 6.3 FUTURE ENHANCEMENTS
    story.append(Paragraph("6.3 Future System Enhancements (Phase 2 Production Roadmap)", style_h1))
    story.append(Paragraph(
        "Commercial production hardening requires upgrading the current working prototype with enterprise security and administrative tooling:",
        style_body
    ))

    story.append(Paragraph("<b>1. Production Password Hashing & JWT Security Architecture</b>", style_h2))
    story.append(Paragraph(
        "Demonstration credentials will be replaced with salted <b>BCrypt.Net-Next</b> (work factor 12) or Argon2id hashing, paired with signed JWT authentication tokens stored in HttpOnly, SameSite=Strict cookies to eliminate XSS risks.",
        style_body
    ))

    code_sec = (
        "// BCrypt Password Hashing in AuthController.cs\n"
        "newUser.PasswordHash = BCrypt.HashPassword(request.Password, workFactor: 12);\n\n"
        "// Login Verification against stored hash\n"
        "bool isValid = BCrypt.Verify(request.Password, user.PasswordHash);\n"
        "if (!isValid) return Unauthorized(new { message = \"Invalid credentials.\" });"
    )
    add_code_block(code_sec, "Proposed BCrypt Salted Password Hashing Integration")

    story.append(Paragraph("<b>2. Two-Factor Authentication (2FA / Multi-Factor Authentication)</b>", style_h2))
    story.append(Paragraph(
        "• <b>TOTP (RFC 6238):</b> Administrators must verify a 6-digit ephemeral token via Google/Microsoft Authenticator before accessing inventory and financial controls.<br/>"
        "• <b>SMS OTP Fallback:</b> High-value guest bookings in Sri Lankan Rupees (LKR) will trigger an automated SMS OTP via Twilio to verified mobile numbers (+94).",
        style_body
    ))

    story.append(Paragraph("<b>3. Advanced Executive Admin Dashboard & Analytics Portal</b>", style_h2))
    story.append(Paragraph(
        "• <b>Visual Telemetry (Chart.js / Recharts):</b> Interactive charts tracking Monthly Revenue Yield in LKR, ADR, and RevPAR.<br/>"
        "• <b>Interactive Room Schedule Gantt Timeline:</b> Visual 30-day horizontal grid allowing front-desk staff to drag-and-drop suite allocations and monitor housekeeping turnovers.<br/>"
        "• <b>Automated PDF Folio Invoicing:</b> Server-side PDF invoice generation with automated tax breakdowns (VAT / Tourism Levy).",
        style_body
    ))

    story.append(Paragraph("<b>4. Direct Payment Gateway Integration (PayHere / Stripe)</b>", style_h2))
    story.append(Paragraph(
        "Real-time tokenized card processing in LKR with a 15-minute temporary reservation hold, transitioning to Confirmed only upon receipt of a signed webhook payment confirmation.",
        style_body
    ))

    # 6.4 VIVA VOCE CHEAT SHEET
    story.append(Spacer(1, 4))
    story.append(Paragraph("6.4 Viva Voce Defense Script (Reflections & Future Plans)", style_h1))
    add_callout(
        "30-Second Viva Answer for Chapter 6",
        "<i>\"Sir/Madam, our biggest technical challenges were adapting to ASP.NET Core's asynchronous threading model, resolving circular JSON serialization in EF Core, and eliminating timezone date shifts between React and C#.<br/>"
        "For our Phase 2 production roadmap, we have designed three essential upgrades: first, implementing BCrypt work-factor-12 password hashing with JWT token rotation; second, enforcing Two-Factor Authentication (TOTP via Google Authenticator) for administrative accounts; and third, expanding the admin module into an executive visual dashboard with interactive Gantt timeline room scheduling and automated LKR payment gateway integration.\"</i>"
    )

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Chapter 06 PDF build successful:", out_pdf)

if __name__ == "__main__":
    create_chapter6_pdf()
