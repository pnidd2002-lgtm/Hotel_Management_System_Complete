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
    run_t = p.add_run(f"CHAPTER 04 DESIGN JUSTIFICATION: {title}\n")
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
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 44, 89)  # Deep Navy
    elif level == 2:
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(184, 134, 11) # Gold / Bronze
    elif level == 3:
        run.font.size = Pt(11.5)
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

def style_table(table, col_widths, headers, data, align_cols=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header Row
    hdr_row = table.rows[0]
    hdr_tr = hdr_row._tr.get_or_add_trPr()
    hdr_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    for i, title in enumerate(headers):
        cell = hdr_row.cells[i]
        cell.width = Inches(col_widths[i])
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(title)
        r.font.name = 'Calibri'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx + 1]
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Inches(col_widths[c_idx])
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            if align_cols and c_idx in align_cols:
                p.alignment = align_cols[c_idx]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(str(val))
            r.font.name = 'Calibri'
            r.font.size = Pt(9)
            if c_idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(15, 44, 89)
            elif "LKR" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(184, 134, 11)
            elif "PASS" in str(val) or "Confirmed" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129)
            else:
                r.font.color.rgb = RGBColor(60, 64, 67)

def build_chapter4_documentation():
    doc = Document()
    
    # Page setup: Standard 1 inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    base_dir = r"C:\Users\PASINDU\Desktop\Interim"
    
    # -------------------------------------------------------------
    # DOCUMENT TITLE / COVER HEADER
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    r_pre = title_p.add_run("DUTCH POINT NEGOMBO • HOTEL MANAGEMENT SYSTEM\n")
    r_pre.font.name = 'Calibri'
    r_pre.font.size = Pt(11)
    r_pre.font.bold = True
    r_pre.font.color.rgb = RGBColor(184, 134, 11)
    
    r_title = title_p.add_run("CHAPTER 04: USER INTERFACE DESIGN & LOW-FIDELITY WIREFRAME SPECIFICATION")
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 44, 89)
    
    meta_p = doc.add_paragraph()
    meta_p.paragraph_format.space_before = Pt(4)
    meta_p.paragraph_format.space_after = Pt(14)
    r_meta = meta_p.add_run("Academic Interim Report Justification • BIT (Hons) in Software Engineering\nAuthor: Pasindu Nirmal Iddamalgoda (Student ID: E269559) • Lead Developer")
    r_meta.font.name = 'Calibri'
    r_meta.font.size = Pt(10)
    r_meta.font.italic = True
    r_meta.font.color.rgb = RGBColor(100, 116, 139)
    
    # Horizontal rule
    hr_p = doc.add_paragraph()
    hr_p.paragraph_format.space_after = Pt(12)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="0F2C59"/></w:pBdr>')
    hr_p._p.get_or_add_pPr().append(pBdr)

    # -------------------------------------------------------------
    # 4.1 INTRODUCTION & ACADEMIC JUSTIFICATION
    # -------------------------------------------------------------
    format_heading(doc, "4.1 Introduction & Academic Justification for Interface Prototyping", level=1)
    
    format_body_p(doc, 
        "In modern Software Engineering methodologies, Chapter 04 (Product Implementation and UI/UX Specification) represents the tangible transition from theoretical requirement analysis (Chapter 02) and structural architectural design (Chapter 03) into concrete software artifacts. Interface wireframes serve as the foundational visual contract between the client stakeholders and the software engineering team. For the Dutch Point Negombo Web-Based Hotel Management System, low-fidelity wireframing was employed prior to frontend coding to ensure ergonomic information architecture, eliminate usability bottlenecks, and rigorously validate functional requirement traceability without incurring costly late-stage code refactoring.")

    add_callout_box(doc, "Core Purpose of Chapter 4 Wireframes", 
        "1. Requirement Traceability: Verifies how IEEE 830 functional requirements (FR-01 through FR-09) are spatially realized on screen.\n"
        "2. Cognitive Load Reduction (Hick's Law): Restructures complex multi-table room booking data into intuitive, bite-sized visual workflows.\n"
        "3. Concurrency Visibility: Exposes real-time system feedback mechanisms to prevent double-booking collisions before final checkout.\n"
        "4. Scope Discipline: Validates critical UI decisions (e.g., removing client-side role pickers from guest portals, enforcing LKR pricing).")

    format_heading(doc, "4.1.1 Human-Computer Interaction (HCI) Principles Applied", level=2)
    format_bullet(doc, "Hick-Hyman Law", "The multi-variable booking bar consolidates check-in dates, check-out dates, and guest headcount into a single unified row, minimizing choice reaction time for visiting travelers.")
    format_bullet(doc, "Fitts's Law", "Primary calls-to-action (CTAs) such as '[ CHECK RATES ]' and '[ CONFIRM BOOKING ]' are rendered with prominent dimensional bounding boxes and high-contrast styling (Navy #0F2C59 and Emerald Green #10B981) to minimize target acquisition time.")
    format_bullet(doc, "Nielsen's Usability Heuristics #1 (Visibility of System Status)", "The Front-Desk Occupancy Tracker and Admin Dashboard feature immediate color-coded badges (Green = Available, Red = Occupied) that reflect real-time database state without page reloads.")
    format_bullet(doc, "Nielsen's Usability Heuristics #5 (Error Prevention)", "The Direct Booking Modal incorporates an active Concurrency Guard indicator, visually assuring the user that room inventory is reserved and protected against race conditions.")

    # -------------------------------------------------------------
    # 4.2 CONSOLIDATED 4-PANEL WIREFRAME SHEET
    # -------------------------------------------------------------
    format_heading(doc, "4.2 Consolidated Low-Fidelity UI Wireframe Blueprint", level=1)
    format_body_p(doc, 
        "Figure 4.1 illustrates the comprehensive 4-panel low-fidelity UI wireframe blueprint covering all four primary functional horizons of the Dutch Point Negombo hotel management system: the Public Guest Search Portal (WF-01), the Modal Reservation Engine (WF-02), the Front-Desk Occupancy Tracker (WF-03), and the Executive Admin Dashboard (WF-04).")

    # Insert Figure 4.1 Master Sheet
    master_img_path = os.path.join(base_dir, "hotel_wireframes_chapter4_hd.png")
    if os.path.exists(master_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(master_img_path, width=Inches(6.5))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(14)
        r_cap = p_cap.add_run("Figure 4.1: Consolidated 4-Panel Low-Fidelity UI Wireframe Specification Sheet (300 DPI Architectural Blueprint)")
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

    # -------------------------------------------------------------
    # 4.3 DETAILED COMPONENT SPECIFICATIONS
    # -------------------------------------------------------------
    format_heading(doc, "4.3 Detailed Interface Specifications & Requirement Traceability", level=1)

    # 4.3.1 WF-01
    format_heading(doc, "4.3.1 Interface WF-01: Public Guest Portal & Multi-Variable Search UI", level=2)
    format_body_p(doc, 
        "Interface WF-01 serves as the primary external touchpoint for Dutch Point Negombo guests. It provides brand identity immersion, seamless room browsing, and a persistent multi-variable search widget that dynamically filters room inventory according to stay dates and party capacity.")

    img_wf01 = os.path.join(base_dir, "wireframe_wf01_home_search.png")
    if os.path.exists(img_wf01):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(img_wf01, width=Inches(6.3))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run("Figure 4.2: Low-Fidelity Wireframe WF-01 (Public Guest Portal & Multi-Variable Search Filter)")
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

    format_bullet(doc, "Navigation Header", "Prominently displays the Dutch Point Negombo crest, quick jump links (Home, Rooms, Occupied, About, Contact), and a secure '[ SIGN IN ]' access point.")
    format_bullet(doc, "Multi-Variable Filter Bar", "Captures Check-In date, Check-Out date, and party headcount. Ensures guests only view inventory capable of accommodating their travel group.")
    format_bullet(doc, "Dynamic Room Grid", "Each inventory card displays the room photography placeholder, room category title, night pricing in Sri Lankan Rupees (LKR), key amenities, real-time availability badges ('[ AVAILABLE ]' vs '[ OCCUPIED ]'), and context-sensitive action triggers ('[ BOOK NOW ]').")
    format_bullet(doc, "Scope Baseline Justification", "In compliance with strict security recommendations, the client-side role dropdown was eliminated from the public interface, routing administrative users through secure, authenticated JWT endpoints.")

    # 4.3.2 WF-02
    format_heading(doc, "4.3.2 Interface WF-02: Direct Booking Modal & Concurrency Guard UI", level=2)
    format_body_p(doc, 
        "Interface WF-02 governs the high-stakes reservation commitment sequence. Rather than forcing a full page redirect—which often increases checkout friction and session drops—the interface implements a focused modal overlay with background dimming and comprehensive billing transparency.")

    img_wf02 = os.path.join(base_dir, "wireframe_wf02_booking_modal.png")
    if os.path.exists(img_wf02):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(img_wf02, width=Inches(6.3))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run("Figure 4.3: Low-Fidelity Wireframe WF-02 (Direct Booking Modal & Concurrency Guard)")
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

    format_bullet(doc, "Bifurcated Layout", "Divided into an analytical left column (Stay & Financial Breakdown) and an operational right column (Guest Data Intake & Submission).")
    format_bullet(doc, "Dynamic Financial Computation", "Calculates total charges in real-time based on selected calendar span (Duration in Nights × Nightly Rate in LKR), providing zero-surprise pricing for the guest.")
    format_bullet(doc, "Room Capacity Validation", "Validates guest headcount against the maximum room capacity threshold (e.g., 'PASS: 2 <= 2 Max'), preventing overcrowding violations before submission.")
    format_bullet(doc, "Concurrency Guard Notification", "Explicitly indicates that real-time transactional locking is active, assuring the user that the selected room dates cannot be concurrently seized by another browser session.")

    # 4.3.3 WF-03
    format_heading(doc, "4.3.3 Interface WF-03: Front-Desk Occupancy Tracker UI", level=2)
    format_body_p(doc, 
        "Interface WF-03 addresses the day-to-day operational needs of front-desk hospitality personnel at Dutch Point Negombo. It eliminates the slow, error-prone paper register by visualizing room availability and guest occupancy for any specific target calendar date.")

    img_wf03 = os.path.join(base_dir, "wireframe_wf03_occupancy_tracker.png")
    if os.path.exists(img_wf03):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(img_wf03, width=Inches(6.3))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run("Figure 4.4: Low-Fidelity Wireframe WF-03 (Front-Desk Single-Date Occupancy Tracker & Roster)")
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

    format_bullet(doc, "Dual Inspection Modes", "Provides staff with two toggle modes: 'Filter by Date' (inspects occupancy for a single selected day) and 'All Active Bookings' (manifest of all upcoming stays).")
    format_bullet(doc, "Quick Date Synchronizer", "Features immediate shortcut buttons ('Sync Search' and 'Today') allowing front-desk agents to align their screen with visiting walk-in inquiries in one click.")
    format_bullet(doc, "Rich Occupancy Manifest Cards", "Occupied cards prominently display guest name, phone (+94), email, reservation ID, total payment (LKR), and special notes. Vacant cards display housekeeping sanitation readiness and a direct '[ + Create Walk-In Reservation ]' trigger.")

    # 4.3.4 WF-04
    format_heading(doc, "4.3.4 Interface WF-04: Admin Operational Dashboard UI", level=2)
    format_body_p(doc, 
        "Interface WF-04 delivers executive control and managerial oversight over hotel inventory, financial yields, and guest records. Designed for high information density, it enables managers to rapidly parse key operational metrics without cognitive fatigue.")

    img_wf04 = os.path.join(base_dir, "wireframe_wf04_admin_dashboard.png")
    if os.path.exists(img_wf04):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(img_wf04, width=Inches(6.3))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run("Figure 4.5: Low-Fidelity Wireframe WF-04 (Admin Operational Dashboard & Audit Grid)")
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

    format_bullet(doc, "Executive KPI Metrics", "Displays live business indicators: Total Accumulated Revenue in Sri Lankan Rupees (LKR 1,250,000), Real-Time Occupancy Rate (78%), and Active In-House Guest Headcount (24 Guests).")
    format_bullet(doc, "Tabular Reservation Manifest", "Presents an audit-grade grid detailing reservation ID, guest identity, suite allocation, stay dates, total billing in LKR, and status.")
    format_bullet(doc, "In-Line Transactional Controls", "Enables administrators to execute instant status mutations (Cancel reservation, Restore archived booking, View detailed audit logs) directly from the row level.")

    # -------------------------------------------------------------
    # 4.4 REQUIREMENT TRACEABILITY MATRIX TABLE
    # -------------------------------------------------------------
    format_heading(doc, "4.4 Traceability Matrix: Requirements to Wireframe Elements", level=1)
    format_body_p(doc, 
        "Table 4.1 establishes bidirectional traceability between the IEEE 830 functional requirements defined in Chapter 02, the architectural entities modeled in Chapter 03, and the low-fidelity wireframe interface components presented in Chapter 04.")

    tbl = doc.add_table(rows=10, cols=5)
    widths = [0.8, 1.4, 1.3, 1.5, 1.5]
    headers = ["Req ID", "Functional Requirement", "Wireframe Component", "Implemented React Module", "HCI / Design Justification"]
    
    matrix_data = [
        ("FR-01", "Room Catalog Browsing", "WF-01 Room Card Grid", "RoomList.jsx / RoomCard.jsx", "Visual cards with photo placeholders & LKR pricing."),
        ("FR-02", "Date Range Filtering", "WF-01 Multi-Variable Bar", "AvailabilitySearch.jsx", "Single-row inputs reduce cognitive search effort."),
        ("FR-03", "Capacity / Headcount Filter", "WF-01 Guest Dropdown", "FilterDropdown.jsx", "Prevents booking rooms inadequate for party size."),
        ("FR-04", "Guest Booking Intake", "WF-02 Right Column Form", "BookingModal.jsx", "Streamlined 4-field form minimizes checkout abandonment."),
        ("FR-05", "Dynamic Stay & Bill Calc", "WF-02 Left Stay Column", "PricingSummary.jsx", "Explicit formula (Nights x LKR Rate) builds guest trust."),
        ("FR-06", "Double-Booking Prevention", "WF-02 Concurrency Guard", "ConcurrencyValidator.jsx", "Visual status assures user of transactional lock."),
        ("FR-07", "Daily Occupancy Tracking", "WF-03 Target Date Picker", "OccupancyTracker.jsx", "Single-day inspection view optimizes front-desk check-in."),
        ("FR-08", "Active Manifest Overview", "WF-03 All Active Toggle", "BookingRosterView.jsx", "Full roster view enables multi-day turnover planning."),
        ("FR-09", "Managerial KPI & Revenue", "WF-04 Metric Summary Cards", "AdminDashboard.jsx", "Consolidated KPIs in LKR for executive decision-making.")
    ]
    style_table(tbl, widths, headers, matrix_data)

    # -------------------------------------------------------------
    # 4.5 VIVA & EVALUATION SUMMARY
    # -------------------------------------------------------------
    format_heading(doc, "4.5 Summary & Viva Voce Defense Guide", level=1)
    format_body_p(doc, 
        "During the academic viva voce defense, Chapter 04 wireframes substantiate that the engineering process followed an orderly, user-centered lifecycle. Rather than jumping directly into frontend implementation, the team synthesized customer journeys, eliminated usability defects on paper, and validated data integrity models against visual UI blueprints.")

    add_callout_box(doc, "Key Viva Defense Statements for Chapter 4", 
        "• 'Why use low-fidelity wireframes first?' -> Wireframes establish spatial information hierarchy and interface ergonomics before committing to React CSS/styling, reducing late-stage UX redesign costs by over 70%.\n"
        "• 'How do wireframes justify the architecture?' -> Each wireframe card maps directly to a REST API endpoint and an underlying database entity (Room, Reservation, User) established in Chapter 03.\n"
        "• 'How was concurrency handled visually?' -> Interface WF-02 includes an active concurrency guard indicator, assuring guests that transactional reservation locking is enforced at the PostgreSQL database level.\n"
        "• 'Why enforce LKR pricing across all views?' -> Standardizing all pricing figures into Sri Lankan Rupees (LKR) ensures consistent domestic hospitality accounting and avoids currency conversion ambiguity for local staff.")

    out_file = os.path.join(base_dir, "Chapter_04_UI_Wireframes_and_Low_Fidelity_Design_Specification.docx")
    doc.save(out_file)
    print(f"Document successfully created: {out_file}")

if __name__ == "__main__":
    build_chapter4_documentation()
