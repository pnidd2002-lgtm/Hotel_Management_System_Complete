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
    run_t = p.add_run(f"ARCHITECTURAL HIGHLIGHT: {title}\n")
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
            elif "LKR" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(184, 134, 11)
            elif "PASS" in str(val) or "Active" in str(val) or "Success" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129)
            else:
                r.font.color.rgb = RGBColor(60, 64, 67)

def build_three_core_functions_doc():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    base_dir = r"C:\Users\PASINDU\Desktop\Interim"
    
    # Cover Header Title
    tp = doc.add_paragraph()
    tp.paragraph_format.space_after = Pt(2)
    r1 = tp.add_run("DUTCH POINT NEGOMBO • PRODUCT IMPLEMENTATION (CHAPTER 04)\n")
    r1.font.name = 'Calibri'
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(184, 134, 11)
    
    r2 = tp.add_run("ADMINISTRATIVE & CORE BUSINESS LOGIC IMPLEMENTATION SPECIFICATIONS")
    r2.font.name = 'Calibri'
    r2.font.size = Pt(18)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(15, 44, 89)
    
    mp = doc.add_paragraph()
    mp.paragraph_format.space_after = Pt(12)
    rm = mp.add_run("Detailed Technical Analysis, C# & React Source Walkthroughs, Database Integrity & Viva Guide\n"
                    "1. Admin Dynamic Room Inventory Management & Suite Creation Engine (RoomsController.cs)\n"
                    "2. Executive Real-Time KPI Analytics & Financial Yield Aggregator (DashboardController.cs)\n"
                    "3. Role-Based Access Control & Identity Governance (AuthController.cs)\n"
                    "Author: Pasindu Nirmal Iddamalgoda (Student ID: E269559) • Lead Developer")
    rm.font.name = 'Calibri'
    rm.font.size = Pt(9.5)
    rm.font.italic = True
    rm.font.color.rgb = RGBColor(100, 116, 139)
    
    hr_p = doc.add_paragraph()
    hr_p.paragraph_format.space_after = Pt(12)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="0F2C59"/></w:pBdr>')
    hr_p._p.get_or_add_pPr().append(pBdr)

    # =========================================================================
    # CORE FUNCTION 1: ADMIN ROOM INVENTORY CREATION & MANAGEMENT
    # =========================================================================
    format_heading(doc, "4.1 Core Function 01: Admin Dynamic Room Inventory & Suite Creation Engine", level=1)
    
    format_heading(doc, "4.1.1 Architectural Rationale & Problem Statement", level=2)
    format_body_p(doc, 
        "In a dynamic hospitality resort, room offerings, seasonal prices, and room allocations frequently evolve. A static hardcoded inventory severely limits hotel agility. The Dutch Point Negombo system empowers administrators with a dynamic Room Inventory Management module that allows staff to provision new suites and beachfront villas, assign nightly rates in Sri Lankan Rupees (LKR), configure party capacities, and bind high-resolution media assets directly into the PostgreSQL database.")

    add_callout_box(doc, "Core Purpose of the Admin Room Management Engine",
        "1. Dynamic Suite Provisioning: Administrators can instantly add new physical rooms or seasonal luxury villas without taking the system offline or running database scripts.\n"
        "2. Duplicate Room Number Guard: The backend checks for duplicate room numbers (e.g. Room #101) to prevent physical numbering collisions.\n"
        "3. Referential Integrity Safeguard: A room cannot be deleted if it has active bookings (Confirmed or Checked-In), preventing orphaned reservation records.\n"
        "4. Reactive Frontend Synchronization: Submitting a new suite automatically refreshes the public guest catalog in real-time without requiring a browser reload.")

    format_heading(doc, "4.1.2 Backend Implementation in RoomsController.cs (POST /api/rooms)", level=2)
    code_room = """// ASP.NET Core C# - RoomsController.cs (Lines 106-121)
[HttpPost]
public async Task<IActionResult> AddRoom([FromBody] Room room)
{
    if (!ModelState.IsValid)
        return BadRequest(ModelState);

    // 1. UNIQUE ROOM NUMBER VALIDATION (Prevent duplicate physical rooms)
    var exists = await _context.Rooms.AnyAsync(r => r.RoomNumber == room.RoomNumber);
    if (exists)
    {
        return Conflict(new { message = $"Room number {room.RoomNumber} already exists." });
    }

    // 2. DEFAULT STATE INITIALIZATION
    if (string.IsNullOrWhiteSpace(room.Status))
    {
        room.Status = "Available";
    }

    // 3. PERSISTENCE TO DATABASE
    _context.Rooms.Add(room);
    await _context.SaveChangesAsync();

    return CreatedAtAction(nameof(GetRoom), new { id = room.RoomId }, room);
}

// DELETE: Safeguard preventing room deletion if active bookings exist
[HttpDelete("{id}")]
public async Task<IActionResult> DeleteRoom(int id)
{
    var room = await _context.Rooms.FindAsync(id);
    if (room == null) return NotFound(new { message = "Room not found." });

    // REFERENTIAL INTEGRITY SAFEGUARD
    var hasActiveBookings = await _context.Bookings
        .AnyAsync(b => b.RoomId == id && (b.BookingStatus == "Confirmed" || b.BookingStatus == "Checked-In"));

    if (hasActiveBookings)
    {
        return BadRequest(new { message = "Cannot delete room with active bookings. Cancel or complete bookings first." });
    }

    _context.Rooms.Remove(room);
    await _context.SaveChangesAsync();
    return Ok(new { message = "Room removed successfully." });
}"""
    format_code_block(doc, code_room, "Code Listing 4.1: Suite Provisioning and Referential Integrity Safeguards in C#")

    format_heading(doc, "4.1.3 Frontend Integration in React (src/App.jsx)", level=2)
    format_body_p(doc, 
        "The client-side administration interface collects room attributes via a reactive form, performs client-side field validation, dispatches a POST request to the API, and immediately re-indexes the room inventory:")

    code_react_room = """// React 19 - src/App.jsx (Lines 151-175)
const handleAddRoom = async (e) => {
  e.preventDefault();
  try {
    const res = await fetch('http://localhost:5000/api/rooms', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        roomNumber: newRoomNumber,
        roomType: newRoomType,
        pricePerNight: parseFloat(newRoomPrice), // Nightly Rate in LKR
        capacity: parseInt(newRoomCapacity),     // Max Guests Allowed
        amenities: newRoomAmenities,
        imageName: newRoomImage,                 // e.g. "room_presidential.jpg"
        status: 'Available'
      })
    });

    if (res.ok) {
      setMessage(`Suite #${newRoomNumber} added successfully to inventory!`);
      // Reset form fields
      setNewRoomNumber(''); setNewRoomType(''); setNewRoomPrice(''); setNewRoomCapacity('');
      loadRooms(); // Instant live re-index across the entire web application
    } else {
      const err = await res.json();
      setMessage(err.message || 'Failed to add room.');
    }
  } catch (err) {
    console.error('Error adding room:', err);
  }
};"""
    format_code_block(doc, code_react_room, "Code Listing 4.2: Asynchronous Room Intake and Reactive State Re-Indexing in React")

    format_heading(doc, "4.1.4 Requirement Traceability", level=2)
    format_bullet(doc, "Functional Requirement", "Satisfies FR-08 (Inventory Maintenance & Administration).")
    format_bullet(doc, "Data Integrity", "Enforces unique room constraints and eliminates orphaned foreign keys during delete operations.")

    # =========================================================================
    # CORE FUNCTION 2: EXECUTIVE KPI ANALYTICS
    # =========================================================================
    format_heading(doc, "4.2 Core Function 02: Executive Real-Time KPI Analytics & Financial Revenue Aggregator", level=1)
    
    format_heading(doc, "4.2.1 Architectural Context & Purpose", level=2)
    format_body_p(doc, 
        "Hotel managers require live operational telemetry covering resort utilization, vacant inventory, and recognized income. The KPI analytical engine inside DashboardController.cs dynamically queries active bookings for today's UTC date, computes gross yield in Sri Lankan Rupees (LKR), and streams the recent reservation manifest without executing slow batch jobs.")

    format_bullet(doc, "Today's Occupied Rooms (Oc)", "Count of unique Room IDs with active Confirmed or Checked-In bookings covering today's date.")
    format_bullet(doc, "Available Walk-In Inventory", "TotalRooms - Oc. Accurately reflects rooms available for immediate walk-in guest check-in.")
    format_bullet(doc, "Resort Occupancy Percentage", "(Oc / TotalRooms) * 100%. Provides an instant operational metric for hotel directors.")
    format_bullet(doc, "Recognized Gross Revenue in LKR", "Sum of TotalAmount where BookingStatus != 'Cancelled'. Eliminates refunded stays.")

    code_kpi = """// ASP.NET Core C# - DashboardController.cs (Lines 20-43)
var today = DateTime.UtcNow.Date;

var totalRooms = await _context.Rooms.CountAsync();

var currentlyOccupiedRoomIds = await _context.Bookings
    .Where(b => (b.BookingStatus == "Confirmed" || b.BookingStatus == "Checked-In") &&
                b.CheckInDate <= today && b.CheckOutDate > today)
    .Select(b => b.RoomId)
    .Distinct()
    .ToListAsync();

var occupiedRoomsCount = currentlyOccupiedRoomIds.Count;
var availableRoomsCount = totalRooms - occupiedRoomsCount;

// Cumulative Financial Yield in LKR
var totalRevenue = await _context.Bookings
    .Where(b => b.BookingStatus != "Cancelled")
    .SumAsync(b => b.TotalAmount);"""
    format_code_block(doc, code_kpi, "Code Listing 4.3: Real-Time Operational KPI & Financial Aggregation in C#")

    # =========================================================================
    # CORE FUNCTION 3: RBAC & IDENTITY GOVERNANCE
    # =========================================================================
    format_heading(doc, "4.3 Core Function 03: Role-Based Access Control (RBAC) & Secure Identity Governance", level=1)
    
    format_heading(doc, "4.3.1 Security Engineering Rationale", level=2)
    format_body_p(doc, 
        "Strict boundary separation between public guest visitors and administrative staff is vital. The system implements a server-enforced anti-privilege escalation guard in AuthController.cs that ensures public registration payloads cannot assign administrative privileges. Furthermore, customer reservation queries are scoped to the individual CustomerId, guaranteeing guest privacy and data protection.")

    code_auth = """// ASP.NET Core C# - AuthController.cs (Lines 65-75)
// SERVER-ENFORCED ANTI-PRIVILEGE ESCALATION GUARD
// Public requests CANNOT assign themselves the "Admin" role.
var newUser = new Customer
{
    FullName = request.FullName.Trim(),
    Email = request.Email.Trim().ToLower(),
    Password = request.Password,
    Phone = request.Phone.Trim(),
    Address = request.Address?.Trim(),
    Role = "Customer", // Immutable server-side assignment
    CreatedAt = DateTime.UtcNow
};

_context.Customers.Add(newUser);
await _context.SaveChangesAsync();"""
    format_code_block(doc, code_auth, "Code Listing 4.4: Anti-Privilege Escalation Guard Enforcing Role='Customer'")

    # =========================================================================
    # SUMMARY TABLE & VIVA VOE
    # =========================================================================
    format_heading(doc, "4.4 Technical Comparison & Viva Voce Talking Points", level=1)
    
    tbl_comp = doc.add_table(rows=4, cols=4)
    w_comp = [1.5, 1.6, 1.8, 1.6]
    h_comp = ["Core Function", "Primary Component", "Key Technical Logic", "Business & HCI Impact"]
    d_comp = [
        ("Add New Rooms (Inventory Management)", "RoomsController.cs &\nApp.jsx (Admin View)", "Unique room number check & referential integrity deletion guard", "Enables hotel staff to dynamically scale room inventory & update LKR rates."),
        ("Executive KPI Analytics", "DashboardController.cs\n(GET /api/dashboard/stats)", "Asynchronous .SumAsync() & Allen's interval check for today's stays", "Provides directors with real-time revenue (LKR) and resort occupancy %."),
        ("Role-Based Access Control (RBAC)", "AuthController.cs &\nReact Protected Tabs", "Server-enforced Role='Customer' & multi-identifier resolver", "Prevents unauthorized admin escalation; unlocks Inventory tab for Admin.")
    ]
    style_table(tbl_comp, w_comp, h_comp, d_comp)

    add_callout_box(doc, "30-Second Viva Answer: Adding New Rooms",
        "Examiner: 'How does the Administrator add new rooms to the system?'\n\n"
        "Your Answer:\n"
        "\"Sir/Madam, when an administrator logs in, the application unlocks the protected Inventory tab.\n"
        "The administrator enters the suite number, category, nightly rate in Sri Lankan Rupees (LKR), party capacity, and photo asset.\n"
        "The ASP.NET Core backend validates the payload, checks for duplicate room numbers using .AnyAsync(), and commits the new suite to PostgreSQL.\n"
        "Upon successful creation, the React frontend immediately triggers loadRooms(), so the newly added suite instantly appears on both the Admin management roster and the public guest booking catalog without restarting the server.\"")

    out_docx = os.path.join(base_dir, "Chapter_04_Core_Functions_Specification.docx")
    doc.save(out_docx)
    print(f"Comprehensive Core Functions DOCX created: {out_docx}")

if __name__ == "__main__":
    build_three_core_functions_doc()
