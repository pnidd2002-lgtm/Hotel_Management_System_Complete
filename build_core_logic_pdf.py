import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
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
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Dutch Point Negombo — Core Business Logic & Algorithms Guide")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "BIT (Hons) Software Engineering • Interim Report Implementation Manual")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()

def create_pdf():
    out_pdf = r"C:\Users\PASINDU\Desktop\Interim\Dutch_Point_Negombo_Core_Business_Logic_and_Algorithms_Guide.pdf"
    doc = SimpleDocTemplate(
        out_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_navy = colors.HexColor("#0F2C59")
    c_gold = colors.HexColor("#B8860B")
    c_dark = colors.HexColor("#1E293B")
    c_slate = colors.HexColor("#475569")
    c_bg = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#CBD5E1")
    c_green = colors.HexColor("#10B981")
    c_red = colors.HexColor("#EF4444")

    # Typography styles
    style_pretitle = ParagraphStyle(
        'PreTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=c_gold,
        spaceAfter=4
    )

    style_title = ParagraphStyle(
        'MainTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_navy,
        alignment=0,
        spaceAfter=6
    )

    style_meta = ParagraphStyle(
        'MetaSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13,
        textColor=c_slate,
        spaceAfter=14
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=c_navy,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_gold,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.0,
        leading=13,
        textColor=c_dark,
        leftIndent=15,
        spaceAfter=4
    )

    style_code = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#E2E8F0")
    )

    style_callout_t = ParagraphStyle(
        'CalloutTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=c_navy,
        spaceAfter=3
    )

    style_callout_b = ParagraphStyle(
        'CalloutBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12,
        textColor=c_dark
    )

    story = []

    def add_callout(title, body_text):
        content = [
            Paragraph(f"<b>CORE HIGHLIGHT:</b> {title}", style_callout_t),
            Spacer(1, 2),
            Paragraph(body_text, style_callout_b)
        ]
        t = Table([[content]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
            ('BOX', (0,0), (-1,-1), 0.5, c_border),
            ('LINELEFT', (0,0), (0,-1), 4.0, c_navy),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))

    def add_code_block(code_str, caption=""):
        p = Paragraph(code_str.replace('\n', '<br/>').replace(' ', '&nbsp;'), style_code)
        t = Table([[p]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(t)
        if caption:
            c_p = Paragraph(f"<i>{caption}</i>", ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=8, leading=10, textColor=c_slate, alignment=1))
            story.append(Spacer(1, 2))
            story.append(c_p)
        story.append(Spacer(1, 8))

    # COVER / HEADER
    story.append(Paragraph("DUTCH POINT NEGOMBO • SOFTWARE ENGINEERING IMPLEMENTATION", style_pretitle))
    story.append(Paragraph("Core Business Logic & Algorithmic Specification", style_title))
    story.append(Paragraph("System Architecture, Real-Time Concurrency, Dynamic Billing & Viva Defense Guide<br/><b>Author:</b> Pasindu Nirmal Iddamalgoda (Student ID: E269559) • Lead Developer", style_meta))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_navy, spaceBefore=0, spaceAfter=12))

    # -------------------------------------------------------------
    # MODULE 1: DOUBLE-BOOKING PREVENTION
    # -------------------------------------------------------------
    story.append(Paragraph("1. Module 01: Double-Booking Prevention & Concurrency Guard", style_h1))
    story.append(Paragraph(
        "Double-booking is the most critical operational vulnerability in hotel management systems. It occurs when two separate guests successfully reserve the same physical suite for overlapping dates. The Dutch Point Negombo system eliminates this using temporal interval validation at the database query tier.",
        style_body
    ))

    add_callout(
        "The Double-Booking Rule in Simple English",
        "Two reservations CLASH if and only if BOTH conditions are true simultaneously:<br/>"
        "<b>1.</b> The existing booking starts <b>BEFORE</b> the new booking ends (<code>ExistingCheckIn &lt; NewCheckOut</code>)<br/>"
        "<b>2.</b> The existing booking ends <b>AFTER</b> the new booking starts (<code>ExistingCheckOut &gt; NewCheckIn</code>)<br/>"
        "• If BOTH are TRUE &rarr; <b>CLASH 🚫 (Blocked with HTTP 409 Conflict)</b><br/>"
        "• If EITHER is FALSE &rarr; <b>SAFE ✅ (New reservation approved)</b>"
    )

    story.append(Paragraph("<b>Scenario Analysis (Room #201: Booked Oct 10 to Oct 15)</b>", style_body))

    # Table of Scenarios
    scenarios_data = [
        [Paragraph("<b>Scenario</b>", style_body), Paragraph("<b>New Dates</b>", style_body), Paragraph("<b>CheckIn &lt; End?</b>", style_body), Paragraph("<b>CheckOut &gt; Start?</b>", style_body), Paragraph("<b>System Decision</b>", style_body)],
        [Paragraph("Inside Stay", style_body), Paragraph("Oct 12 &ndash; 14", style_body), Paragraph("10 &lt; 14 (True)", style_body), Paragraph("15 &gt; 12 (True)", style_body), Paragraph("<font color='#DC2626'><b>BLOCKED (409)</b></font>", style_body)],
        [Paragraph("Overlap Start", style_body), Paragraph("Oct 08 &ndash; 12", style_body), Paragraph("10 &lt; 12 (True)", style_body), Paragraph("15 &gt; 08 (True)", style_body), Paragraph("<font color='#DC2626'><b>BLOCKED (409)</b></font>", style_body)],
        [Paragraph("Overlap End", style_body), Paragraph("Oct 13 &ndash; 18", style_body), Paragraph("10 &lt; 18 (True)", style_body), Paragraph("15 &gt; 13 (True)", style_body), Paragraph("<font color='#DC2626'><b>BLOCKED (409)</b></font>", style_body)],
        [Paragraph("Full Enclosure", style_body), Paragraph("Oct 08 &ndash; 20", style_body), Paragraph("10 &lt; 20 (True)", style_body), Paragraph("15 &gt; 08 (True)", style_body), Paragraph("<font color='#DC2626'><b>BLOCKED (409)</b></font>", style_body)],
        [Paragraph("Adjacent Prior", style_body), Paragraph("Oct 05 &ndash; 10", style_body), Paragraph("10 &lt; 10 (False)", style_body), Paragraph("15 &gt; 05 (True)", style_body), Paragraph("<font color='#10B981'><b>SAFE (Departs 10th AM)</b></font>", style_body)],
        [Paragraph("Adjacent Next", style_body), Paragraph("Oct 15 &ndash; 20", style_body), Paragraph("10 &lt; 20 (True)", style_body), Paragraph("15 &gt; 15 (False)", style_body), Paragraph("<font color='#10B981'><b>SAFE (Arrives 15th PM)</b></font>", style_body)]
    ]
    t_scen = Table(scenarios_data, colWidths=[95, 85, 105, 105, 114])
    t_scen.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg]),
    ]))
    story.append(t_scen)
    story.append(Spacer(1, 8))

    csharp_m1 = (
        "// BookingsController.cs (Lines 152-169)\n"
        "var conflictingBooking = await _context.Bookings\n"
        "    .Include(b => b.Customer)\n"
        "    .Where(b => b.RoomId == request.RoomId &&\n"
        "               (b.BookingStatus == \"Confirmed\" || b.BookingStatus == \"Checked-In\") &&\n"
        "                b.CheckInDate < checkOut &&\n"
        "                b.CheckOutDate > checkIn)\n"
        "    .FirstOrDefaultAsync();\n\n"
        "if (conflictingBooking != null)\n"
        "{\n"
        "    return Conflict(new {\n"
        "        message = $\"DOUBLE BOOKING PREVENTED: Room {room.RoomNumber} already booked.\",\n"
        "        conflictBookingId = conflictingBooking.BookingId\n"
        "    });\n"
        "}"
    )
    add_code_block(csharp_m1, "Listing 1.1: Database Interval Overlap Query & HTTP 409 Conflict Abort")

    # -------------------------------------------------------------
    # MODULE 2: DYNAMIC ROOM AVAILABILITY
    # -------------------------------------------------------------
    story.append(Paragraph("2. Module 02: Dynamic Multi-Variable Availability & Search Engine", style_h1))
    story.append(Paragraph(
        "A critical software engineering design decision was avoiding static state mutation on the Room entity. Room availability is inherently temporal—a suite occupied today will be vacant next week. Mutating a static 'Status' column causes permanent lockouts. Instead, availability is computed via in-memory projection.",
        style_body
    ))

    add_callout(
        "Dynamic Projection Architecture",
        "• <b>Step 1:</b> System identifies all bookings overlapping with the user's specific check-in / check-out window.<br/>"
        "• <b>Step 2:</b> Extracts the unique set of occupied Room IDs (<code>.Distinct()</code>).<br/>"
        "• <b>Step 3:</b> Rooms not present in this occupied set are dynamically marked <code>IsAvailable = true</code>.<br/>"
        "• <b>Step 4:</b> Filters inventory by party size: <code>Capacity &ge; Guests</code>."
    )

    csharp_m2 = (
        "// RoomsController.cs (Lines 44-64)\n"
        "var conflictingBookings = await _context.Bookings\n"
        "    .Where(b => b.BookingStatus == \"Confirmed\" || b.BookingStatus == \"Checked-In\")\n"
        "    .Where(b => b.CheckInDate < cout && b.CheckOutDate > cin)\n"
        "    .Select(b => b.RoomId).Distinct().ToListAsync();\n\n"
        "var results = rooms.Select(r => new {\n"
        "    r.RoomId, r.RoomNumber, r.RoomType, r.PricePerNight, r.Capacity,\n"
        "    DisplayStatus = conflictingBookings.Contains(r.RoomId) ? \"Occupied\" : r.Status,\n"
        "    IsAvailable = !conflictingBookings.Contains(r.RoomId) && r.Status == \"Available\"\n"
        "});"
    )
    add_code_block(csharp_m2, "Listing 2.1: Dynamic In-Memory Room Projection based on Date Intervals")

    # -------------------------------------------------------------
    # MODULE 3: FINANCIAL CALCULATION & LKR ENGINE
    # -------------------------------------------------------------
    story.append(Paragraph("3. Module 03: Deterministic Financial Billing & LKR Engine", style_h1))
    story.append(Paragraph(
        "Hospitality billing requires exact deterministic precision. The Dutch Point Negombo system standardizes all transactions into Sri Lankan Rupees (LKR) with 128-bit decimal fixed-point arithmetic.",
        style_body
    ))

    story.append(Paragraph("• <b>Nights Computation:</b> <code>int nights = (checkOut - checkIn).Days; if (nights &lt;= 0) nights = 1;</code>", style_bullet))
    story.append(Paragraph("• <b>Bill Derivation:</b> <code>decimal totalAmount = nights * room.PricePerNight;</code> (e.g., 2 Nights &times; LKR 65,000 = LKR 130,000)", style_bullet))
    story.append(Paragraph("• <b>Headcount Validation:</b> <code>request.NumberOfGuests &le; room.Capacity</code> prevents suite over-occupancy violations.", style_bullet))
    story.append(Paragraph("• <b>Rounding Safety:</b> PostgreSQL column typed as <code>decimal(18,2)</code> eliminates IEEE 754 binary floating-point drift.", style_bullet))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MODULE 4: FRONT-DESK OCCUPANCY TRACKER
    # -------------------------------------------------------------
    story.append(Paragraph("4. Module 04: Front-Desk Real-Time Occupancy Tracker", style_h1))
    story.append(Paragraph(
        "Front-desk staff require instantaneous operational visibility during peak arrival hours. The Occupancy Tracker features dual operational filters:",
        style_body
    ))
    story.append(Paragraph("• <b>Single Target Date Mode:</b> Evaluates <code>CheckInDate &le; TargetDate AND CheckOutDate &gt; TargetDate</code> to isolate current in-house guests for any chosen day.", style_bullet))
    story.append(Paragraph("• <b>Range Sync Mode:</b> Links directly with the guest booking engine to inspect prospective turn-around conflicts.", style_bullet))
    story.append(Paragraph("• <b>Guest Manifest Projection:</b> Pulls guest name, verified Sri Lankan contact (+94), email, billing total (LKR), and housekeeping sanitization status.", style_bullet))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MODULE 5: ADMINISTRATIVE GOVERNANCE & RBAC
    # -------------------------------------------------------------
    story.append(Paragraph("5. Module 05: Administrative Governance & Audit Controls", style_h1))
    story.append(Paragraph(
        "Executive oversight is enforced through strict role separation and historical audit integrity:",
        style_body
    ))
    story.append(Paragraph("• <b>Client-Side Role Removal:</b> Public guests cannot toggle administrative privileges; admin routes are guarded by JWT authentication.", style_bullet))
    story.append(Paragraph("• <b>KPI Aggregation:</b> Live calculation of Total Yield in LKR (<code>sum(TotalAmount)</code>), resort occupancy percentage, and active guest headcounts.", style_bullet))
    story.append(Paragraph("• <b>Soft Cancellation & Restoration:</b> Bookings mutate status flags without destroying historical customer audit trails.", style_bullet))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # 6. VIVA VOCE CHEAT SHEET
    # -------------------------------------------------------------
    story.append(Paragraph("6. Viva Voce Defense Cheat-Sheet (Examiner Q&A)", style_h1))
    
    viva_qas = [
        [Paragraph("<b>Examiner Question</b>", style_body), Paragraph("<b>Recommended Viva Voce Answer</b>", style_body)],
        [
            Paragraph("<b>'How did you prevent double booking?'</b>", style_body),
            Paragraph("<i>'Sir/Madam, we enforce interval overlap logic at the database query level: a booking clashes if (ExistingCheckIn &lt; NewCheckOut) AND (ExistingCheckOut &gt; NewCheckIn). If found, the API rejects the request with an HTTP 409 Conflict error.'</i>", style_body)
        ],
        [
            Paragraph("<b>'Why not mutate a static Status column on the Room table?'</b>", style_body),
            Paragraph("<i>'Because room availability is temporal, not permanent. A room occupied today will be vacant next week. Mutating the room table causes permanent lockouts. We dynamically project availability per date range.'</i>", style_body)
        ],
        [
            Paragraph("<b>'What currency does the system use?'</b>", style_body),
            Paragraph("<i>'The system strictly operates in Sri Lankan Rupees (LKR) using C# decimal(18,2) types to eliminate binary rounding errors.'</i>", style_body)
        ],
        [
            Paragraph("<b>'How do you protect admin operations?'</b>", style_body),
            Paragraph("<i>'We removed client-side role pickers from the public UI. Administrative operations are isolated behind secure authenticated endpoints.'</i>", style_body)
        ]
    ]
    t_viva = Table(viva_qas, colWidths=[150, 354])
    t_viva.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg]),
    ]))
    story.append(t_viva)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build successful:", out_pdf)

if __name__ == "__main__":
    create_pdf()
