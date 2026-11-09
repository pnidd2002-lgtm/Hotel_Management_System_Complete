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
    run_t = p.add_run(f"CORE ALGORITHM HIGHLIGHT: {title}\n")
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
    set_cell_background(cell, "1E1E1E")  # Dark VS Code style
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
            elif "CLASH" in str(val) or "BLOCKED" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(220, 38, 38)
            elif "SAFE" in str(val) or "APPROVED" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129)
            elif "LKR" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(184, 134, 11)
            else:
                r.font.color.rgb = RGBColor(60, 64, 67)

def build_core_logic_doc():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    base_dir = r"C:\Users\PASINDU\Desktop\Interim"
    
    # Header Title
    tp = doc.add_paragraph()
    tp.paragraph_format.space_after = Pt(2)
    r1 = tp.add_run("DUTCH POINT NEGOMBO • SYSTEM ARCHITECTURE & CODE MANUAL\n")
    r1.font.name = 'Calibri'
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(184, 134, 11)
    
    r2 = tp.add_run("CORE BUSINESS LOGIC & ALGORITHMIC SPECIFICATION GUIDE")
    r2.font.name = 'Calibri'
    r2.font.size = Pt(18)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(15, 44, 89)
    
    mp = doc.add_paragraph()
    mp.paragraph_format.space_after = Pt(12)
    rm = mp.add_run("Plain English Explanations, Code Walkthroughs, Edge Cases & Viva Defense Guide\nAuthor: Pasindu Nirmal Iddamalgoda (Student ID: E269559) • Lead Developer")
    rm.font.name = 'Calibri'
    rm.font.size = Pt(9.5)
    rm.font.italic = True
    rm.font.color.rgb = RGBColor(100, 116, 139)
    
    hr_p = doc.add_paragraph()
    hr_p.paragraph_format.space_after = Pt(12)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="0F2C59"/></w:pBdr>')
    hr_p._p.get_or_add_pPr().append(pBdr)

    # =========================================================================
    # MODULE 1: DOUBLE-BOOKING PREVENTION
    # =========================================================================
    format_heading(doc, "1. Module 01: Double-Booking Prevention & Concurrency Guard", level=1)
    format_body_p(doc, 
        "Double-booking is the most critical operational failure mode in hospitality software. It occurs when two distinct guests reserve the same physical suite for overlapping calendar dates. If an automated system lacks rigorous interval validation, both guests arrive simultaneously expecting the same accommodations.")

    add_callout_box(doc, "The Golden Rule of Date Overlap in Simple English",
        "Two reservations CLASH if and only if BOTH conditions are true:\n"
        "1. The existing booking starts BEFORE the new booking ends (ExistingCheckIn < NewCheckOut)\n"
        "2. The existing booking ends AFTER the new booking starts (ExistingCheckOut > NewCheckIn)\n\n"
        "If BOTH are TRUE -> They OVERLAP! (System BLOCKS with HTTP 409 Conflict)\n"
        "If EITHER is FALSE -> They DO NOT overlap! (System APPROVES and saves booking)")

    format_heading(doc, "1.1 Mathematical Derivation & Case Analysis", level=2)
    format_body_p(doc, 
        "Consider an active confirmed booking for Room #201: October 10 to October 15. The table below proves how the two-part condition handles every possible real-world guest reservation scenario:")

    tbl_cases = doc.add_table(rows=7, cols=5)
    w_cases = [1.2, 1.3, 1.2, 1.2, 1.6]
    h_cases = ["Scenario", "New Guest Dates", "CheckIn < End?", "CheckOut > Start?", "System Decision"]
    d_cases = [
        ("Inside Stay", "Oct 12 to Oct 14", "Oct 10 < Oct 14 (T)", "Oct 15 > Oct 12 (T)", "CLASH 🚫 (BLOCKED)"),
        ("Overlap Start", "Oct 08 to Oct 12", "Oct 10 < Oct 12 (T)", "Oct 15 > Oct 08 (T)", "CLASH 🚫 (BLOCKED)"),
        ("Overlap End", "Oct 13 to Oct 18", "Oct 10 < Oct 18 (T)", "Oct 15 > Oct 13 (T)", "CLASH 🚫 (BLOCKED)"),
        ("Full Enclosure", "Oct 08 to Oct 20", "Oct 10 < Oct 20 (T)", "Oct 15 > Oct 08 (T)", "CLASH 🚫 (BLOCKED)"),
        ("Adjacent Prior", "Oct 05 to Oct 10", "Oct 10 < Oct 10 (F)", "Oct 15 > Oct 05 (T)", "SAFE ✅ (Leaves Oct 10 morning)"),
        ("Adjacent Next", "Oct 15 to Oct 20", "Oct 10 < Oct 20 (T)", "Oct 15 > Oct 15 (F)", "SAFE ✅ (Arrives Oct 15 afternoon)")
    ]
    style_table(tbl_cases, w_cases, h_cases, d_cases)

    format_heading(doc, "1.2 Backend C# Implementation in BookingsController.cs", level=2)
    code_m1 = """// ASP.NET Core C# - BookingsController.cs (Lines 152-169)
var conflictingBooking = await _context.Bookings
    .Include(b => b.Customer)
    .Where(b => b.RoomId == request.RoomId &&
               (b.BookingStatus == "Confirmed" || b.BookingStatus == "Checked-In") &&
                b.CheckInDate < checkOut &&
                b.CheckOutDate > checkIn)
    .FirstOrDefaultAsync();

if (conflictingBooking != null)
{
    return Conflict(new
    {
        message = $"DOUBLE BOOKING PREVENTED: Room {room.RoomNumber} ({room.RoomType}) is already booked " +
                  $"from {conflictingBooking.CheckInDate:yyyy-MM-dd} to {conflictingBooking.CheckOutDate:yyyy-MM-dd}.",
        conflictBookingId = conflictingBooking.BookingId
    });
}"""
    format_code_block(doc, code_m1, "Code Listing 1.1: Double-Booking Guard enforcing Allen's Interval Algebra via EF Core")

    # =========================================================================
    # MODULE 2: DYNAMIC AVAILABILITY ENGINE
    # =========================================================================
    format_heading(doc, "2. Module 02: Dynamic Multi-Variable Availability & Search Engine", level=1)
    format_body_p(doc, 
        "A common amateur mistake in hotel software is mutating a static 'Status' column on the Room table from 'Available' to 'Occupied'. This fails completely because a room can be occupied on October 10th, but completely vacant on October 18th!")

    add_callout_box(doc, "Dynamic Availability Projection in Simple English",
        "Instead of changing the room table, the backend dynamically calculates availability on the fly:\n"
        "1. The guest enters: Check-In Date, Check-Out Date, Guest Count.\n"
        "2. The database finds all Room IDs that have a booking conflicting with that specific date window.\n"
        "3. Any room NOT in that conflicting list is marked IsAvailable = true.\n"
        "4. Rooms are also filtered by party size: Capacity >= Guests.\n"
        "Result: Fast, real-time availability without corrupting static room records.")

    format_heading(doc, "2.1 Backend C# Implementation in RoomsController.cs", level=2)
    code_m2 = """// ASP.NET Core C# - RoomsController.cs (Lines 44-65)
var conflictingBookings = await _context.Bookings
    .Where(b => b.BookingStatus == "Confirmed" || b.BookingStatus == "Checked-In")
    .Where(b => b.CheckInDate < cout && b.CheckOutDate > cin)
    .Select(b => b.RoomId)
    .Distinct()
    .ToListAsync();

var results = rooms.Select(r => new
{
    r.RoomId,
    r.RoomNumber,
    r.RoomType,
    r.PricePerNight,
    r.Capacity,
    DisplayStatus = conflictingBookings.Contains(r.RoomId) ? "Occupied" : r.Status,
    IsAvailable = !conflictingBookings.Contains(r.RoomId) && r.Status == "Available"
});"""
    format_code_block(doc, code_m2, "Code Listing 2.1: Dynamic In-Memory Room Projection based on Requested Date Intervals")

    # =========================================================================
    # MODULE 3: FINANCIAL CALCULATION & LKR ENGINE
    # =========================================================================
    format_heading(doc, "3. Module 03: Deterministic Financial Billing & LKR Currency Engine", level=1)
    format_body_p(doc, 
        "Financial calculations in hospitality systems must adhere to strict accounting standards to prevent rounding discrepancies and guest billing disputes. The Dutch Point Negombo system standardizes all billing into Sri Lankan Rupees (LKR) with decimal(18,2) database precision.")

    format_bullet(doc, "Nights Computation Formula", "Nights = max(1, (CheckOutDate.Date - CheckInDate.Date).Days). Single day-use stays default to 1 night.")
    format_bullet(doc, "Total Amount Formula", "TotalAmount = Nights * Room.PricePerNight (e.g., 2 Nights * LKR 65,000 = LKR 130,000).")
    format_bullet(doc, "Headcount Capacity Guard", "Ensures request.NumberOfGuests <= room.Capacity; otherwise returns HTTP 400 Bad Request.")
    format_bullet(doc, "Floating-Point Safety", "All monetary types are stored as C# decimal (128-bit exact fixed-point) rather than double/float, eliminating binary precision drift.")

    code_m3 = """// ASP.NET Core C# - BookingsController.cs (Lines 171-175)
int nights = (checkOut - checkIn).Days;
if (nights <= 0) nights = 1;
decimal totalAmount = nights * room.PricePerNight;

var newBooking = new Booking
{
    CustomerId = request.CustomerId,
    RoomId = request.RoomId,
    CheckInDate = checkIn,
    CheckOutDate = checkOut,
    TotalAmount = totalAmount,
    BookingStatus = "Confirmed"
};"""
    format_code_block(doc, code_m3, "Code Listing 3.1: Deterministic Stay Duration and Total Amount Billing in LKR")

    # =========================================================================
    # MODULE 4: FRONT-DESK OCCUPANCY TRACKER
    # =========================================================================
    format_heading(doc, "4. Module 04: Front-Desk Occupancy Tracker & Roster Engine", level=1)
    format_body_p(doc, 
        "Front-desk staff require rapid operational visibility during peak arrival hours (12:00 PM - 3:00 PM). The Occupancy Tracker provides dual operational modes to facilitate both immediate check-in and multi-day turnover management.")

    format_bullet(doc, "Single Target Date Mode", "Queries active stays where CheckInDate <= TargetDate AND CheckOutDate > TargetDate. Instantly isolates who is in the hotel on that exact calendar day.")
    format_bullet(doc, "Synchronized Date Range Mode", "Links directly with the search bar, allowing receptionists to see who occupies suites over an incoming guest's entire travel itinerary.")
    format_bullet(doc, "Guest Manifest Projection", "Returns primary guest name, verified contact phone (+94), confirmed email, paid billing in LKR, and special housekeeping notes.")

    code_m4 = """// ASP.NET Core C# - BookingsController.cs (Lines 80-85)
var queryDate = targetDate?.Date ?? DateTime.UtcNow.Date;
var query = _context.Bookings
    .Include(b => b.Room)
    .Include(b => b.Customer)
    .Where(b => b.BookingStatus == "Confirmed" || b.BookingStatus == "Checked-In")
    .Where(b => b.CheckInDate <= queryDate && b.CheckOutDate > queryDate);"""
    format_code_block(doc, code_m4, "Code Listing 4.1: Single-Date Occupancy Inspection for Front-Desk Hospitality Terminals")

    # =========================================================================
    # MODULE 5: ADMINISTRATIVE GOVERNANCE & METRICS
    # =========================================================================
    format_heading(doc, "5. Module 05: Administrative Governance, Audit & KPI Metrics", level=1)
    format_body_p(doc, 
        "The administrative module provides executive-level governance, financial reporting, and operational auditing across the entire resort inventory.")

    format_bullet(doc, "Total Yield Aggregation", "Sum of all Confirmed and Checked-In booking totals: TotalRevenue = sum(b.TotalAmount) where status != 'Cancelled'.")
    format_bullet(doc, "Occupancy Percentage", "OccupancyRate = (ActiveOccupiedRooms / TotalRooms) * 100%. Expresses current resort utilization.")
    format_bullet(doc, "Soft Cancellation & State Restoration", "Admins can cancel reservations or restore previously cancelled bookings without destroying historical customer audit trails.")
    format_bullet(doc, "Security Baseline Separation", "Client-side role drop-downs were removed from the public portal, enforcing strict server-side validation for administrative operations.")

    # =========================================================================
    # 6. VIVA VOCE CHEAT SHEET
    # =========================================================================
    format_heading(doc, "6. Viva Voce Defense Cheat-Sheet (Examiner Q&A)", level=1)
    format_body_p(doc, 
        "Use these concise, professional answers when examiners question your technical implementation during the viva voce:")

    qas = [
        ("Examiner: 'How did you prevent double-booking?'", 
         "Answer: 'Sir/Madam, we enforce interval overlap logic at the database level: an existing booking clashes if ExistingCheckIn < RequestedCheckOut and ExistingCheckOut > RequestedCheckIn. If found, the API returns an HTTP 409 Conflict error.'"),
        ("Examiner: 'Why not just change the room status to Occupied in the room table?'", 
         "Answer: 'Because room occupancy is temporal, not permanent. A room occupied today will be vacant next week. Mutating the room table causes permanent lockouts. We dynamically project availability per date range.'"),
        ("Examiner: 'What currency does the system use?'", 
         "Answer: 'The system strictly operates in Sri Lankan Rupees (LKR) using C# decimal(18,2) types to eliminate binary rounding errors.'"),
        ("Examiner: 'How do you prevent guests from acting as Admin?'", 
         "Answer: 'We removed client-side role pickers from the public UI. Administrative operations are isolated behind secure authenticated endpoints.'")
    ]
    for q, a in qas:
        format_bullet(doc, q, a)

    out_docx = os.path.join(base_dir, "Dutch_Point_Negombo_Core_Business_Logic_and_Algorithms_Guide.docx")
    doc.save(out_docx)
    print(f"DOCX created: {out_docx}")

if __name__ == "__main__":
    build_core_logic_doc()
