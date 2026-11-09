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
    run_t = p.add_run(f"KEY TESTING HIGHLIGHT / සුවිශේෂී කරුණ: {title}\n")
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
            elif "PASS" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129)
            elif "LKR" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(184, 134, 11)
            elif "409" in str(val) or "Conflict" in str(val) or "BLOCKED" in str(val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(220, 38, 38)
            else:
                r.font.color.rgb = RGBColor(60, 64, 67)

def build_testing_guide_doc():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    base_dir = r"C:\Users\PASINDU\Desktop\Interim"
    
    # Header Cover Title
    tp = doc.add_paragraph()
    tp.paragraph_format.space_after = Pt(2)
    r1 = tp.add_run("DUTCH POINT NEGOMBO • QUALITY ASSURANCE & TESTING SPECIFICATION\n")
    r1.font.name = 'Calibri'
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(184, 134, 11)
    
    r2 = tp.add_run("SOFTWARE TESTING & EVALUATION GUIDE (BILINGUAL: ENGLISH & SINHALA)")
    r2.font.name = 'Calibri'
    r2.font.size = Pt(18)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(15, 44, 89)
    
    mp = doc.add_paragraph()
    mp.paragraph_format.space_after = Pt(12)
    rm = mp.add_run("Comprehensive Test Strategy, 4 Testing Levels, Test Cases, Viva Voce Guide & සරල සිංහල පැහැදිලි කිරීම\nAuthor: Pasindu Nirmal Iddamalgoda (Student ID: E269559) • Lead Developer")
    rm.font.name = 'Calibri'
    rm.font.size = Pt(9.5)
    rm.font.italic = True
    rm.font.color.rgb = RGBColor(100, 116, 139)
    
    hr_p = doc.add_paragraph()
    hr_p.paragraph_format.space_after = Pt(12)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="0F2C59"/></w:pBdr>')
    hr_p._p.get_or_add_pPr().append(pBdr)

    # =========================================================================
    # PART 1: ENGLISH TESTING SPECIFICATION
    # =========================================================================
    format_heading(doc, "PART 1: ACADEMIC TESTING SPECIFICATION (FOR REPORT & VIVA VOCE)", level=1)
    
    format_heading(doc, "1.1 Introduction to Quality Assurance & Testing Strategy", level=2)
    format_body_p(doc, 
        "Software testing is an indispensable verification and validation phase in the Software Development Life Cycle (SDLC). For the Dutch Point Negombo Web-Based Hotel Management System, the testing strategy was structured to prove that all IEEE 830 functional requirements are satisfied, transactional data integrity is safeguarded, and high-concurrency race conditions (such as double-booking collisions) are completely mitigated before deployment.")

    add_callout_box(doc, "Core Purpose of Testing in this System",
        "1. Concurrency Protection: Verifies that Allen's Interval Algebra prevents room double-bookings across overlapping dates.\n"
        "2. Deterministic Billing: Confirms that total stay charges in Sri Lankan Rupees (LKR) are accurately calculated without rounding drift.\n"
        "3. Cross-Tier Communication: Validates asynchronous REST contract exchange between React 19, ASP.NET Core C#, and PostgreSQL.\n"
        "4. Operational Robustness: Validates front-desk occupancy tracking and administrative dashboard metrics under real-world usage.")

    format_heading(doc, "1.2 The Four Primary Levels of Testing", level=2)
    
    format_bullet(doc, "1. Unit / Component Testing", 
        "Focuses on testing individual algorithms, formulas, and domain rules in isolation. Examples include verifying the stay calculation formula (Nights = CheckOut - CheckIn), the LKR bill derivation (Nights * Room.PricePerNight), and guest capacity boundary assertions (NumberOfGuests <= Room.Capacity).")

    format_bullet(doc, "2. Integration Testing", 
        "Evaluates the communication and data pipeline across architectural boundaries. Validates that the React frontend successfully dispatches HTTP POST/GET requests to the ASP.NET Core Web API, and that Entity Framework Core properly commits transactional queries to PostgreSQL without foreign key violations or schema mismatch. Tools utilized: Swagger UI and Postman.")

    format_bullet(doc, "3. Black-Box / Functional System Testing", 
        "Evaluates complete end-to-end user journeys from the perspective of an external actor without inspecting internal source code. Scenarios include: guest multi-variable search -> suite selection -> modal reservation intake -> confirmation issuance -> instant synchronization on the front-desk occupancy tracker.")

    format_bullet(doc, "4. Boundary & Concurrency Testing", 
        "Exposes the core double-booking prevention engine to temporal edge cases. Verifies that overlapping reservation windows trigger an immediate HTTP 409 Conflict abort, whereas adjacent same-day turnover reservations (where previous checkout matches incoming check-in) are safely approved without false-positive blocks.")

    # 1.3 Formal Test Case Matrix
    format_heading(doc, "1.3 Formal Test Case Execution Matrix", level=2)
    format_body_p(doc, 
        "The following table details representative test cases executed across the Dutch Point Negombo hotel management system, verifying core functional requirements:")

    tbl_cases = doc.add_table(rows=8, cols=6)
    w_cases = [0.8, 1.3, 1.2, 1.2, 1.2, 0.8]
    h_cases = ["Test ID", "Description", "Input Data", "Expected Result", "Actual Result", "Status"]
    d_cases = [
        ("TC-01", "Double Booking (Middle Overlap)", "Room #101, Oct 12-14\n(Existing: Oct 10-15)", "HTTP 409 Conflict;\nBooking aborted", "HTTP 409 returned;\nDiagnostic banner shown", "PASS"),
        ("TC-02", "Double Booking (Partial Start)", "Room #201, Oct 08-12\n(Existing: Oct 10-15)", "HTTP 409 Conflict;\nOverlap detected", "Rejected with conflict details", "PASS"),
        ("TC-03", "Adjacent Turnover (Safe Checkout)", "Room #101, Oct 05-10\n(Existing: Oct 10-15)", "Approved (Guest departs Oct 10 morning)", "Booking created successfully", "PASS"),
        ("TC-04", "Adjacent Turnover (Safe Check-in)", "Room #101, Oct 15-18\n(Existing ends Oct 15)", "Approved (Guest arrives Oct 15 afternoon)", "Booking created successfully", "PASS"),
        ("TC-05", "Party Headcount Capacity Guard", "Room #101 (Max 2 Guests)\nRequested: 4 Guests", "HTTP 400 Bad Request;\nCapacity violation", "Blocked before submission;\nAlert displayed", "PASS"),
        ("TC-06", "LKR Financial Bill Derivation", "2 Nights @ LKR 65,000/night", "Total = LKR 130,000\n(decimal 18,2)", "Computed LKR 130,000", "PASS"),
        ("TC-07", "Front-Desk Date Filter Sync", "Target Date: 2026-10-10", "Returns exactly 1 occupied suite", "1 suite returned with guest info", "PASS")
    ]
    style_table(tbl_cases, w_cases, h_cases, d_cases)

    # 1.4 Viva Voce Script
    format_heading(doc, "1.4 Viva Voce Defense Script (English - Memorize for Presentation)", level=2)
    add_callout_box(doc, "30-Second Viva Answer for Testing",
        "Examiner: 'Pasindu, how did you verify and test your hotel management system?'\n\n"
        "Your Answer:\n"
        "\"Sir/Madam, our quality assurance strategy combined four systematic testing tiers:\n"
        "First, we applied Unit Testing on deterministic business logic, including LKR billing arithmetic and party capacity validation.\n"
        "Second, we conducted Integration Testing using Swagger and Postman to ensure seamless JSON serialization and transactional commits between React 19, ASP.NET Core C#, and PostgreSQL.\n"
        "Third, we performed Black-Box System Testing covering the complete guest reservation and front-desk occupancy tracking workflows.\n"
        "Finally, we executed Boundary and Concurrency Testing to prove that our interval overlap logic rigorously rejects double-booking attempts with an HTTP 409 Conflict while safely supporting same-day room turnaround.\"")

    # =========================================================================
    # PART 2: SINHALA EXPLANATION
    # =========================================================================
    format_heading(doc, "PART 2: සරල සිංහල පැහැදිලි කිරීම (SINHALA EXPLANATION GUIDE)", level=1)
    
    format_heading(doc, "2.1 ඇත්තටම Software Testing කියන්නේ මොකක්ද?", level=2)
    format_body_p(doc, 
        "Software Testing කියන්නේ අපි නිර්මාණය කරපු Dutch Point Negombo Hotel Management System එකේ සියලුම අංග (Features) කිසිදු දෝෂයකින් තොරව, අප සැලසුම් කළ ආකාරයටම නිවැරදිව ක්‍රියාත්මක වෙනවාදැයි විවිධ ක්‍රමවේද ඔස්සේ පරීක්ෂා කර සහතික කරගැනීමේ ක්‍රියාවලියයි.")
    
    format_body_p(doc, 
        "හෝටල් කළමනාකරණ පද්ධතියක සාර්ථකත්වය තීරණය වන්නේ එහි දත්තවල නිරවද්‍යතාවය (Data Integrity) මතයි. විශේෂයෙන්ම එකම කාමරය පුද්ගලයින් දෙදෙනෙකුට වෙන්වීම (Double Booking) වැළැක්වීම, ශ්‍රී ලංකා රුපියල් (LKR) වලින් නිවැරදිව බිල්පත් ගණනය වීම, සහ ආරක්ෂිතව දත්ත ගබඩා වීම මෙහිදී ප්‍රධාන වශයෙන්ම පරීක්ෂාවට ලක් කෙරේ.")

    format_heading(doc, "2.2 අප සිදුකළ ප්‍රධාන Testing වර්ග 4 (සරල සිංහලෙන්)", level=2)

    format_bullet(doc, "1. Unit Testing (කෑල්ලෙන් කෑල්ල පරීක්ෂා කිරීම)", 
        "පද්ධතියේ ඇති කුඩාම ගණනය කිරීම් සහ තර්කයන් (Functions & Formulas) වෙන වෙනම ගෙන පරීක්ෂා කිරීමයි. උදාහරණයක් ලෙස: රාත්‍රී 2ක් සඳහා රුපියල් 65,000 බැගින් මුළු මුදල රුපියල් 130,000ක් ලෙස නිවැරදිව හැදෙනවාද යන්න සහ කාමරයක උපරිම ධාරිතාව 2ක් නම්, පුද්ගලයින් 3ක් දැමූ විට එය ස්වයංක්‍රීයව අවහිර (Block) වෙනවාද යන්න පරීක්ෂා කිරීම.")

    format_bullet(doc, "2. Integration Testing (කොටස් එකතු කර පරීක්ෂා කිරීම)", 
        "පද්ධතියේ විවිධ තාක්ෂණික ස්ථර (Tiers) අතර සන්නිවේදනය නිවැරදිදැයි බැලීමයි. එනම් React Frontend එකෙන් යවන Booking දත්ත C# Web API එකට ලැබී, එයින් PostgreSQL Database එකේ නිවැරදිව තැන්පත් වී, නැවත සාර්ථක ප්‍රතිචාරයක් (Success Response) Frontend එකට එනවාදැයි බැලීමයි. මේ සඳහා අපි Postman සහ Swagger මෙවලම් භාවිත කළෙමු.")

    format_bullet(doc, "3. System / Black-Box Testing (සම්පූර්ණ පද්ධතියම පරිශීලක අතින් පරීක්ෂා කිරීම)", 
        "මෙහිදී Code එක දෙස නොබලා, සාමාන්‍ය හෝටල් අමුත්තෙකු (Guest) හෝ Front-Desk නිලධාරියෙකු පරිගණක තිරය භාවිත කරන අයුරින් මුල සිට අගටම පරීක්ෂා කරයි. උදාහරණ: හෝටල් කාමරයක් Search කිරීම -> Suite එකක් තෝරා ගැනීම -> විස්තර ඇතුළත් කර Book කිරීම -> Front-Desk එකේ Occupancy Tracker එකෙන් එම කාමරය Occupied ලෙස රතු පාටින් දිස්වීම.")

    format_bullet(doc, "4. Boundary & Concurrency Testing (දින සීමා සහ Double Booking පරීක්ෂාව)", 
        "Examiners ලා වඩාත්ම අවධානය යොමු කරන ප්‍රධානම පරීක්ෂාව මෙයයි. එකිනෙකට ගැටෙන (Overlap වන) දින වකවානු ඇතුළත් කළ විට පද්ධතිය HTTP 409 Conflict දෝෂයක් ලබා දෙමින් එය වළක්වනවාද යන්නත්, අමුත්තෙකු පිටව යන දිනයේදීම (Same-day Checkout) වෙනත් අයෙකුට එම කාමරය වෙන්කර ගැනීමට ඉඩ ලබා දෙනවාද යන්නත් මෙහිදී සනාථ කෙරේ.")

    format_heading(doc, "2.3 Double Booking වැළැක්වීම පරීක්ෂා කළ අයුරු (Live Scenarios)", level=2)
    format_body_p(doc, 
        "කාමර අංක 101 ඔක්තෝබර් 10 සිට 15 දක්වා කලින් වෙන්කර ඇති අවස්ථාවකදී පහත පරීක්ෂණ සිදුකරන ලදී:")

    format_bullet(doc, "මැදින් Overlap වන දින (Oct 12 - 14)", "පද්ධතිය වහාම Booking එක ප්‍රතික්ෂේප කර තිරයේ රතු පැහැති අනතුරු ඇඟවීමක් පෙන්වයි -> PASS ✅")
    format_bullet(doc, "ආරම්භය Overlap වන දින (Oct 08 - 12)", "ඔක්තෝබර් 10 සහ 11 කලින් වෙන්ව ඇති බැවින් පද්ධතිය එය අවහිර කරයි -> PASS ✅")
    format_bullet(doc, "කලින් දිනයේ Checkout වන දින (Oct 05 - 10)", "පෙර අමුත්තා 10 වනදා උදෑසන පිටව යන බැවින් පද්ධතිය සාර්ථකව Booking එක භාරගනී -> PASS ✅")
    format_bullet(doc, "පසු දිනයේ Check-in වන දින (Oct 15 - 18)", "පෙර අමුත්තා 15 වනදා උදෑසන පිටව ගොස් කාමරය සූදානම් බැවින් පද්ධතිය Booking එක භාරගනී -> PASS ✅")

    format_heading(doc, "2.4 Viva Voce එකට සූදානම් වීම සඳහා සිංහලෙන් උපදෙස්", level=2)
    format_body_p(doc, 
        "Viva එකේදී Examiner විසින් 'Testing කළේ කොහොමද?' කියා ඇසූ විට කලබල නොවී පහත කරුණු 4 මතක තබාගෙන පිළිතුරු දෙන්න:")
    format_bullet(doc, "පියවර 1", "අපි Unit Testing කළා බිල්පත් හැදෙන ගණිත සූත්‍ර සහ ධාරිතාව (Capacity) බලන්න.")
    format_bullet(doc, "පියවර 2", "Frontend එක සහ Backend Database එක සම්බන්ධ වෙන හැටි Swagger / Postman මගින් Integration Testing කළා.")
    format_bullet(doc, "පියවර 3", "Guest කෙනෙක් කාමරයක් book කරලා Front Desk එකට යන සම්පූර්ණ Flow එක Black-Box System Testing කළා.")
    format_bullet(doc, "පියවර 4", "Double booking නොවී නවතිනවද කියලා විවිධ දින වකවානු දාලා Boundary & Concurrency Testing කරලා තහවුරු කළා.")

    out_docx = os.path.join(base_dir, "Dutch_Point_Negombo_Software_Testing_Guide_Bilingual.docx")
    doc.save(out_docx)
    print(f"Bilingual Testing Guide DOCX created: {out_docx}")

if __name__ == "__main__":
    build_testing_guide_doc()
