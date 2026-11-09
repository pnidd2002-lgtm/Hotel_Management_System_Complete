import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_system_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Palette
    DARK_NAVY = RGBColor(11, 25, 44)       # #0B192C Title bg
    NAVY = RGBColor(15, 44, 89)            # #0F2C59 Main titles
    GOLD = RGBColor(184, 134, 11)          # #B8860B Accent gold
    BG_LIGHT = RGBColor(248, 249, 250)     # #F8F9FA
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(222, 226, 230)
    TEXT_DARK = RGBColor(33, 37, 41)
    TEXT_MUTED = RGBColor(108, 117, 125)
    GREEN = RGBColor(16, 185, 129)
    RED = RGBColor(220, 38, 38)
    BLUE_ACCENT = RGBColor(13, 110, 253)

    assets_dir = r"C:\Users\PASINDU\Desktop\Interim\presentation_assets"

    def set_bg(slide, color):
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_text="DUTCH POINT NEGOMBO • WEB-BASED HOTEL MANAGEMENT SYSTEM"):
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.95))
        banner.fill.background()
        banner.line.fill.background()
        tf = banner.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = GOLD
        p_cat.space_after = Pt(2)
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

    def add_card(slide, left, top, width, height, title="", title_color=NAVY, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.2)
        else:
            card.line.fill.background()
            
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)
        
        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Calibri"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(6)
        return card

    def add_bullet(tf, bold_txt, normal_txt, bullet_char="•", pt_size=10):
        p = tf.add_paragraph()
        p.space_after = Pt(4)
        r0 = p.add_run()
        r0.text = f"{bullet_char} "
        r0.font.name = "Calibri"
        r0.font.size = Pt(pt_size)
        r0.font.bold = True
        r0.font.color.rgb = GOLD
        
        if bold_txt:
            r1 = p.add_run()
            r1.text = bold_txt + ": "
            r1.font.name = "Calibri"
            r1.font.size = Pt(pt_size)
            r1.font.bold = True
            r1.font.color.rgb = NAVY
            
        r2 = p.add_run()
        r2.text = normal_txt
        r2.font.name = "Calibri"
        r2.font.size = Pt(pt_size)
        r2.font.color.rgb = TEXT_DARK

    def add_img_safe(slide, img_name, left, top, width=None, height=None):
        path = os.path.join(assets_dir, img_name)
        if os.path.exists(path):
            kwargs = {}
            if width: kwargs['width'] = Inches(width)
            if height: kwargs['height'] = Inches(height)
            return slide.shapes.add_picture(path, Inches(left), Inches(top), **kwargs)
        return None

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (EXECUTIVE NAVY)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, DARK_NAVY)

    # Logo / Institution Header
    add_img_safe(s1, "image1.png", 0.8, 0.6, width=1.8)
    
    inst_box = s1.shapes.add_textbox(Inches(2.8), Inches(0.6), Inches(9.5), Inches(0.8))
    tf1 = inst_box.text_frame
    tf1.word_wrap = True
    p_inst = tf1.paragraphs[0]
    p_inst.text = "ESOFT METRO CAMPUS • FACULTY OF COMPUTING • BIT (HONS) DEGREE"
    p_inst.font.name = "Calibri"
    p_inst.font.size = Pt(11)
    p_inst.font.bold = True
    p_inst.font.color.rgb = GOLD

    # Main Project Title
    title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(2.2))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    
    p_sub = tf_t.paragraphs[0]
    p_sub.text = "ACADEMIC INTERIM REPORT DEFENSE • SYSTEM DEMONSTRATION"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(12)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(165, 215, 232)
    p_sub.space_after = Pt(4)
    
    p_main = tf_t.add_paragraph()
    p_main.text = "Web-Based Hotel Management System"
    p_main.font.name = "Calibri"
    p_main.font.size = Pt(34)
    p_main.font.bold = True
    p_main.font.color.rgb = RGBColor(255, 255, 255)
    
    p_desc = tf_t.add_paragraph()
    p_desc.text = "Dutch Point Negombo Resort — Decoupled 3-Tier Enterprise Architecture (React 19 + ASP.NET Core 10 + MySQL 8.0)"
    p_desc.font.name = "Calibri"
    p_desc.font.size = Pt(14)
    p_desc.font.color.rgb = GOLD

    # Team Members Container Cards
    members = [
        ("I.D.P.N Iddamalgoda", "E269559", "Team Lead / Presenter"),
        ("H.M.Y.R Herath", "E267614", "Team Member"),
        ("Y.M.A.Y Bandara", "E267609", "Team Member"),
        ("A.G.H.H Jinadasa", "E267612", "Team Member")
    ]
    for idx, (name, sid, role) in enumerate(members):
        mx = 0.8 + (idx * 2.95)
        my = 4.2
        c = add_card(s1, mx, my, 2.85, 2.4, bg_color=RGBColor(19, 42, 74), border_color=RGBColor(30, 60, 102))
        tf_m = c.text_frame
        p_rn = tf_m.paragraphs[0]
        p_rn.text = name
        p_rn.font.name = "Calibri"
        p_rn.font.size = Pt(12)
        p_rn.font.bold = True
        p_rn.font.color.rgb = RGBColor(255, 255, 255)
        p_rn.space_after = Pt(4)
        
        p_id = tf_m.add_paragraph()
        p_id.text = f"Student ID: {sid}"
        p_id.font.name = "Calibri"
        p_id.font.size = Pt(10.5)
        p_id.font.color.rgb = GOLD
        p_id.space_after = Pt(2)
        
        p_rl = tf_m.add_paragraph()
        p_rl.text = role
        p_rl.font.name = "Calibri"
        p_rl.font.size = Pt(9.5)
        p_rl.font.color.rgb = RGBColor(200, 210, 225)

    # Date badge
    dt_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.4))
    tf_dt = dt_box.text_frame
    p_dt = tf_dt.paragraphs[0]
    p_dt.text = "Date: October 5, 2026 • Interim Milestone Submission (55% Working Prototype Verified)"
    p_dt.font.name = "Calibri"
    p_dt.font.size = Pt(10)
    p_dt.font.color.rgb = RGBColor(140, 160, 185)

    # =========================================================================
    # SLIDE 2: SYSTEM VISION & PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, BG_LIGHT)
    add_header(s2, "System Vision & Core Operational Problems Solved")

    # 3 Cards Layout
    c1 = add_card(s2, 0.8, 1.5, 3.7, 5.4, "1. Manual Inefficiencies")
    tf = c1.text_frame
    add_bullet(tf, "Historical Ledgers", "Dutch Point Negombo relied on physical room diaries and phone notes.")
    add_bullet(tf, "Turnover Delay", "Front desk spent 10+ minutes per check-in cross-referencing paper receipts.")
    add_bullet(tf, "Unrecorded Data", "Customer contact numbers (+94) and special preferences frequently misplaced.")
    add_bullet(tf, "High Overhead", "Excessive staff workload during 11 AM checkout and 2 PM check-in rush hours.")

    c2 = add_card(s2, 4.8, 1.5, 3.7, 5.4, "2. Overbooking Vulnerability")
    tf = c2.text_frame
    add_bullet(tf, "4.2% Error Rate", "Academic research (Kumar et al., 2024) shows manual systems suffer 4.2% double bookings.")
    add_bullet(tf, "Overlapping Conflicts", "Simultaneous phone and walk-in inquiries frequently reserve the same bed.")
    add_bullet(tf, "Guest Dissatisfaction", "Walk-in friction and room disputes negatively impact hotel reputation.")
    add_bullet(tf, "Financial Loss", "OTA commissions drain 15% to 25% profit margin per external booking.")

    c3 = add_card(s2, 8.8, 1.5, 3.7, 5.4, "3. The Implemented Solution")
    tf = c3.text_frame
    add_bullet(tf, "Centralized 3-Tier Web PMS", "Seamlessly connects customers, receptionists, and administrators.")
    add_bullet(tf, "Automated ACID Concurrency", "Zero-latency interval overlap engine guarantees zero double bookings.")
    add_bullet(tf, "Domestic LKR Pricing Engine", "Instant multi-night calculations in Sri Lankan Rupees (LKR) with no hidden fees.")
    add_bullet(tf, "Live Front-Desk Tracker", "Real-time calendar occupancy view replaces paper diaries.")

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE (DECOUPLED 3-TIER PATTERN)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, BG_LIGHT)
    add_header(s3, "System Architecture: Decoupled 3-Tier Enterprise Pattern")

    c1 = add_card(s3, 0.8, 1.5, 3.7, 5.4, "Tier 1: Presentation (React 19)")
    tf = c1.text_frame
    add_bullet(tf, "Framework", "React 19 compiled with Vite 8.3 on localhost:5173.")
    add_bullet(tf, "Single Page App (SPA)", "Near-instantaneous tab transitions via React Virtual DOM without page reloads.")
    add_bullet(tf, "Luxury Styling", "Bootstrap 5.3 + bespoke CSS variables (Cormorant Garamond & gold palette).")
    add_bullet(tf, "State Hooks", "useState and useEffect manage search dates, capacity filters, and user session tokens.")
    add_bullet(tf, "Asynchronous REST", "Fires native async fetch() requests passing structured JSON payloads.")

    c2 = add_card(s3, 4.8, 1.5, 3.7, 5.4, "Tier 2: Application (ASP.NET Core 10)")
    tf = c2.text_frame
    add_bullet(tf, "Framework", "ASP.NET Core 10 Web API on localhost:5000.")
    add_bullet(tf, "RESTful Controllers", "AuthController, RoomsController, BookingsController, DashboardController.")
    add_bullet(tf, "Strongly-Typed DTOs", "Validates input payloads before reaching business logic.")
    add_bullet(tf, "Interval Engine", "Enforces Allen's Interval Algebra to block double-booking race conditions.")
    add_bullet(tf, "ORM Integration", "Oracle MySql.EntityFrameworkCore executes optimized, parameterized LINQ queries.")

    c3 = add_card(s3, 8.8, 1.5, 3.7, 5.4, "Tier 3: Data Tier (MySQL 8.0)")
    tf = c3.text_frame
    add_bullet(tf, "Database Engine", "MySQL Server 8.0 (InnoDB engine, UTF8MB4, port 3306).")
    add_bullet(tf, "Normalized Schema (3NF)", "Core tables: Customers, Rooms, Bookings.")
    add_bullet(tf, "Referential Integrity", "Foreign keys enforce relationships; ON DELETE RESTRICT prevents orphaned records.")
    add_bullet(tf, "Decimal Precision", "Monetary fields use DECIMAL(10,2) to eliminate binary rounding errors in LKR.")
    add_bullet(tf, "ACID Compliance", "Guarantees complete commit or immediate rollback upon any failure.")

    # =========================================================================
    # SLIDE 4: USE CASE DIAGRAM & OPERATIONAL ROLES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, BG_LIGHT)
    add_header(s4, "System Use Cases & Operational Persona Boundaries")

    # Left: Embed Use Case Diagram Image
    add_img_safe(s4, "image2.png", 0.8, 1.4, width=5.2)

    # Right: Persona breakdown
    c = add_card(s4, 6.3, 1.4, 6.2, 5.5, "Persona Permission Boundaries (RBAC)")
    tf = c.text_frame
    add_bullet(tf, "Guest Customer Persona", 
               "Can search rooms by dates/headcount, view suite amenities, register account, book rooms with live LKR pricing, and view/cancel personal reservations in 'My Bookings'.")
    add_bullet(tf, "Front-Desk Receptionist Persona", 
               "Can inspect the real-time Occupied Rooms Tracker by calendar date, access guest contact information (+94 phone/email), and coordinate check-in/out workflows.")
    add_bullet(tf, "Hotel Administrator Persona", 
               "Exclusive authority to manage hotel room inventory (Add new suites, update nightly LKR rates, configure capacities, bind photo assets), and review overall occupancy metrics.")
    add_bullet(tf, "Security Boundary", 
               "Strict server-side role separation ensures customers cannot access administrative controls or inspect other guests' reservation records.")

    # =========================================================================
    # SLIDE 5: DATABASE ARCHITECTURE & RELATIONAL ER MODEL
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, BG_LIGHT)
    add_header(s5, "Relational Database Design & MySQL 8.0 EER Model")

    # Left: Embed ER Diagram
    add_img_safe(s5, "image3.png", 0.8, 1.4, width=6.2)

    # Right: Data Dictionary Summary
    c = add_card(s5, 7.3, 1.4, 5.2, 5.5, "Normalized Schema (hotel_db)")
    tf = c.text_frame
    add_bullet(tf, "Customers Table", "CustomerId (PK), FullName, Email (Unique), Password, Phone, Address, Role ('Customer' vs 'Admin').")
    add_bullet(tf, "Rooms Table", "RoomId (PK), RoomNumber (Unique), RoomType, PricePerNight (DECIMAL), Capacity, Status, Amenities, ImageName.")
    add_bullet(tf, "Bookings Table", "BookingId (PK), CustomerId (FK), RoomId (FK), CheckInDate (DATE), CheckOutDate (DATE), NumberOfGuests, TotalAmount (DECIMAL), BookingStatus.")
    add_bullet(tf, "Referential Safeguards", "Foreign key constraints with ON DELETE RESTRICT ensure a room cannot be deleted if active bookings exist.")
    add_bullet(tf, "LKR Currency Standard", "All monetary transactions use 128-bit exact fixed-point decimal fields to eliminate floating-point drift.")

    # =========================================================================
    # SLIDE 6: SYSTEM ACTIVITY WORKFLOW (END-TO-END RESERVATION)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, BG_LIGHT)
    add_header(s6, "System Activity Flow: End-to-End Guest Reservation Workflow")

    # Left: Embed Activity Diagram
    add_img_safe(s6, "image4.jpeg", 0.8, 1.4, width=6.0)

    # Right: Step-by-Step Flow
    c = add_card(s6, 7.1, 1.4, 5.4, 5.5, "Three-Tier Transaction Lifecycle")
    tf = c.text_frame
    add_bullet(tf, "1. Search Initiation", "Customer selects Check-In, Check-Out, and Guest Count on React frontend -> Sends GET /api/rooms.")
    add_bullet(tf, "2. Availability Projection", "ASP.NET Core queries overlapping bookings -> Returns filtered room cards with dynamic AVAILABLE / OCCUPIED badges.")
    add_bullet(tf, "3. Reservation Intake", "Customer clicks 'Book Now' -> Modal calculates stay duration and total bill in LKR -> Dispatches POST /api/bookings.")
    add_bullet(tf, "4. Double-Booking Validation", "Backend evaluates date overlap conditions. If overlap found -> Returns HTTP 409 Conflict. If clear -> Inserts booking into MySQL.")
    add_bullet(tf, "5. Client Confirmation", "React displays confirmation modal with unique Reservation ID (#RES-XXXX) and triggers live inventory refresh.")

    # =========================================================================
    # SLIDE 7: LOW-FIDELITY WIREFRAMES VS IMPLEMENTATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, BG_LIGHT)
    add_header(s7, "UI Prototyping: Low-Fidelity Hand-Drawn Wireframes")

    # 4 Wireframe images side by side
    add_img_safe(s7, "image17.jpeg", 0.8, 1.4, width=2.8)
    add_img_safe(s7, "image18.jpeg", 3.8, 1.4, width=2.8)
    add_img_safe(s7, "image19.jpeg", 6.8, 1.4, width=2.8)
    add_img_safe(s7, "image20.jpeg", 9.8, 1.4, width=2.8)

    c = add_card(s7, 0.8, 5.5, 11.733, 1.5, "Architectural Purpose of Wireframing")
    tf = c.text_frame
    add_bullet(tf, "Spatial Information Architecture", "Mapped layout requirements before writing CSS: Sticky search bar, 3-card inventory grid, 2-column modal layout.")
    add_bullet(tf, "Usability & Cognitive Load", "Consolidated search parameters into a single line (Hick's Law) and prominent action buttons (Fitts's Law).")
    add_bullet(tf, "Traceability", "Directly translated into React components: App.jsx, BookingModal.jsx, and LoginModal.jsx.")

    # =========================================================================
    # SLIDE 8: CORE INNOVATION 1 — DOUBLE-BOOKING PREVENTION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, BG_LIGHT)
    add_header(s8, "Core Innovation 1: Double-Booking Prevention Algorithm")

    # Left: Code Screenshot
    add_img_safe(s8, "image21.png", 0.8, 1.4, width=6.2)

    # Right: Explanation Card
    c = add_card(s8, 7.3, 1.4, 5.2, 5.5, "Allen's Interval Algebra in C#")
    tf = c.text_frame
    add_bullet(tf, "The Overlap Condition", "A conflict exists if BOTH conditions evaluate to TRUE:\n  1. ExistingCheckIn < NewCheckOut\n  2. ExistingCheckOut > NewCheckIn")
    add_bullet(tf, "Scenario Example", "Room #101 booked Oct 10 to Oct 15. New guest requests Oct 12 to Oct 14:\n  • Oct 10 < Oct 14 -> TRUE\n  • Oct 15 > Oct 12 -> TRUE\n  -> Both TRUE = OVERLAP DETECTED!")
    add_bullet(tf, "HTTP 409 Conflict Abort", "Backend aborts transaction, returns HTTP 409 Conflict with booked date metadata, committing 0 rows to MySQL.")
    add_bullet(tf, "Same-Day Turnaround Supported", "Guest departing Oct 10 morning allows another guest arriving Oct 10 afternoon (Condition 1 evaluates to False -> Approved!).")

    # =========================================================================
    # SLIDE 9: SYSTEM UI 1 — LIVE ROOM CATALOG & STATUS BADGES
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9, BG_LIGHT)
    add_header(s9, "Live System Interface: Dynamic Room Inventory Catalog")

    # Large UI Screenshot
    add_img_safe(s9, "image22.png", 0.8, 1.4, width=6.8)

    # Right: Architectural Callouts
    c = add_card(s9, 7.9, 1.4, 4.6, 5.5, "Interface Engineering Highlights")
    tf = c.text_frame
    add_bullet(tf, "Boutique Luxury Aesthetic", "Italian serif typography (Cormorant Garamond) paired with coastal boutique styling.")
    add_bullet(tf, "Real-Time Status Badges", "Green 'AVAILABLE' pill vs Red 'OCCUPIED' pill dynamically reflect database state.")
    add_bullet(tf, "Transparent LKR Pricing", "Displays exact nightly rate in Sri Lankan Rupees (e.g. Standard Queen: LKR 28,000 / Deluxe: LKR 42,000 / Ocean Suite: LKR 65,000).")
    add_bullet(tf, "Action Context Triggers", "Available rooms trigger 'RESERVE SUITE' modal; occupied rooms trigger 'View Occupancy Details'.")
    add_bullet(tf, "Capacity Badges", "Max guest limits clearly highlighted to prevent overcrowded party bookings.")

    # =========================================================================
    # SLIDE 10: CORE INNOVATION 2 — DYNAMIC AVAILABILITY ENGINE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10, BG_LIGHT)
    add_header(s10, "Core Innovation 2: Dynamic Multi-Variable Availability Search")

    # Left: Code Screenshot
    add_img_safe(s10, "image23.png", 0.8, 1.4, width=6.2)

    # Right: Explanation Card
    c = add_card(s10, 7.3, 1.4, 5.2, 5.5, "In-Memory Availability Projection")
    tf = c.text_frame
    add_bullet(tf, "The Architecture Flaw Avoided", "Never mutate static Room.Status in the database! A room occupied today will be vacant next week. Mutating room rows causes permanent lockouts.")
    add_bullet(tf, "Dynamic Projection Logic", "Backend queries only active bookings overlapping with the requested date window, extracting distinct occupied RoomIds.")
    add_bullet(tf, "In-Memory Flagging", "Rooms NOT in the conflicting list are marked IsAvailable = true on-the-fly.")
    add_bullet(tf, "Capacity Filter", "Filters inventory where Capacity >= GuestCount, ensuring guests only see suitable suites.")
    add_bullet(tf, "Zero Page Reloads", "React Virtual DOM re-renders filtered cards instantly upon clicking 'CHECK RATES'.")

    # =========================================================================
    # SLIDE 11: CORE INNOVATION 3 — BILLING & RESERVATION MODAL
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11, BG_LIGHT)
    add_header(s11, "Core Innovation 3: Deterministic Billing & Reservation Modal")

    # Left: Pricing Code & Modal UI side by side
    add_img_safe(s11, "image25.png", 0.8, 1.4, width=5.5)
    add_img_safe(s11, "image26.png", 6.6, 1.4, width=5.9)

    # Bottom summary banner
    c = add_card(s11, 0.8, 5.5, 11.733, 1.5, "Deterministic Financial Computation in LKR")
    tf = c.text_frame
    add_bullet(tf, "Stay Duration Formula", "Nights = max(1, (CheckOutDate.Date - CheckInDate.Date).Days). Single day-use stays default to 1 night.")
    add_bullet(tf, "Total Bill Formula", "TotalAmount = Nights * Room.PricePerNight (e.g. 3 Nights * LKR 28,000 = LKR 84,000 total due displayed on button).")
    add_bullet(tf, "Focus-Locked Modal", "Darkened backdrop eliminates distraction and prevents checkout abandonment.")

    # =========================================================================
    # SLIDE 12: CORE INNOVATION 4 — ROLE-BASED ACCESS CONTROL (RBAC)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12, BG_LIGHT)
    add_header(s12, "Core Innovation 4: Role-Based Access Control & Identity Governance")

    # Left: Auth code & Customer reservations UI
    add_img_safe(s12, "image27.png", 0.8, 1.4, width=5.5)
    add_img_safe(s12, "image29.png", 6.6, 1.4, width=5.9)

    # Bottom summary card
    c = add_card(s12, 0.8, 5.5, 11.733, 1.5, "Security Engineering & Data Privacy")
    tf = c.text_frame
    add_bullet(tf, "Anti-Privilege Escalation", "Public registration strictly hardcodes Role = 'Customer' at the backend. Clients cannot submit 'Admin' roles.")
    add_bullet(tf, "Pre-Seeded Administrator", "Admin account ('Pasindu') is configured directly in the database, granting exclusive access to inventory controls.")
    add_bullet(tf, "Customer Data Isolation", "Queries in 'My Bookings' are partitioned by CustomerId, preventing unauthorized viewing of other guests' records.")

    # =========================================================================
    # SLIDE 13: CORE INNOVATION 5 — ADMIN SUITE INVENTORY MANAGEMENT
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13, BG_LIGHT)
    add_header(s13, "Core Innovation 5: Admin Dynamic Room Inventory Management")

    # Left: Admin Add Room Form & Newly Added Room on Home
    add_img_safe(s13, "image31.png", 0.8, 1.4, width=5.6)
    add_img_safe(s13, "image32.png", 6.7, 1.4, width=5.8)

    # Bottom summary card
    c = add_card(s13, 0.8, 5.5, 11.733, 1.5, "Live Inventory Provisioning Lifecycle")
    tf = c.text_frame
    add_bullet(tf, "Dynamic Provisioning", "Admin adds new suites (e.g. Room #501 Ocean View Suite @ LKR 65,000/night) directly through the browser.")
    add_bullet(tf, "Duplicate Number Guard", "Backend verifies AnyAsync(r => r.RoomNumber == room.RoomNumber) to prevent duplicate room door numbers.")
    add_bullet(tf, "Instant Reactive Re-Index", "React calls loadRooms() upon successful creation, immediately publishing the suite to the public guest catalog.")

    # =========================================================================
    # SLIDE 14: DATABASE VERIFICATION — LIVE MYSQL RECORDS
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_bg(s14, BG_LIGHT)
    add_header(s14, "Database Persistence Verification in MySQL 8.0 Workbench")

    # Left: MySQL Workbench screenshot
    add_img_safe(s14, "image33.png", 0.8, 1.4, width=6.6)

    # Right: Verification details
    c = add_card(s14, 7.7, 1.4, 4.8, 5.5, "Empirical Data Verification")
    tf = c.text_frame
    add_bullet(tf, "Live Persistence Proof", "Verified execution of 'SELECT * FROM rooms;' in MySQL Workbench confirms live insertion of Suite #501.")
    add_bullet(tf, "Schema Attributes Verified", "RoomId, RoomNumber, RoomType, PricePerNight (DECIMAL 10,2), Capacity, Status ('Available'), Amenities, ImageName.")
    add_bullet(tf, "Relational Constraints", "Foreign key cascades link bookings to specific room and customer records.")
    add_bullet(tf, "Transactional Logging", "MySQL InnoDB binary logs confirm zero dirty reads and strict transaction isolation.")

    # =========================================================================
    # SLIDE 15: SYSTEM VALIDATION & EMPIRICAL TEST CASES
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_bg(s15, BG_LIGHT)
    add_header(s15, "System Validation: Formal Test Execution Matrix (100% PASS)")

    c = add_card(s15, 0.8, 1.4, 11.733, 5.5, "Chapter 05 Empirical Test Results")
    tf = c.text_frame
    
    test_cases = [
        ("TC-01: Admin Authentication", "Login as 'Pasindu' / 'Pasindu@123'", "Issues Admin role claim, unlocks Inventory tab", "PASS"),
        ("TC-02: Public Guest Signup", "Register guest 'Anuradha' (+94771234567)", "Enforces Role = 'Customer' without admin option", "PASS"),
        ("TC-03: Real-Time Availability", "Search dates 2026-10-10 to 10-15, Guests: 3", "Filters rooms where Capacity >= 3, shows AVAILABLE", "PASS"),
        ("TC-04: Double-Booking Overlap", "Attempt booking Room #101 on taken dates", "Rejects with HTTP 409 Conflict, commits 0 rows", "PASS"),
        ("TC-05: Dynamic LKR Price Math", "Select Suite #102 (LKR 42,000) for 4 nights", "Modal calculates 4 * 42,000 = LKR 168,000 total", "PASS"),
        ("TC-06: Booking Cancellation", "Click 'Cancel Reservation' in My Bookings", "Deletes booking from MySQL, suite returns to AVAILABLE", "PASS"),
        ("TC-07: Live Occupancy Tracker", "Select date 2026-10-12 in Occupancy Tracker", "Displays Room #102 occupied by John Doe (+1 555-0199)", "PASS"),
        ("TC-08: Headcount Limit Guard", "Attempt booking Suite #101 (Max 2) with 4 guests", "Rejects submission with HTTP 400 Bad Request error", "PASS")
    ]
    for tid, action, exp, st in test_cases:
        p = tf.add_paragraph()
        p.space_after = Pt(2)
        r0 = p.add_run()
        r0.text = f"• {tid}: "
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = NAVY
        
        r1 = p.add_run()
        r1.text = f"{action} -> {exp} -> "
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        
        r2 = p.add_run()
        r2.text = f"[{st}]"
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.5)
        r2.font.bold = True
        r2.font.color.rgb = GREEN

    # =========================================================================
    # SLIDE 16: TECHNICAL REFLECTION & CHALLENGES RESOLVED
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_bg(s16, BG_LIGHT)
    add_header(s16, "Technical Reflection: Engineering Challenges & Resolutions")

    c1 = add_card(s16, 0.8, 1.4, 5.7, 5.5, "ASP.NET Core & C# Learning Curve")
    tf = c1.text_frame
    add_bullet(tf, "Async Pipeline (async/await)", "Initial blocking .Result calls caused Kestrel thread pool starvation. Resolved by migrating completely to non-blocking async streaming (.ToListAsync(), .CountAsync()).")
    add_bullet(tf, "Circular JSON Loops in EF Core", "Two-way navigational properties between Customer and Booking crashed the JSON serializer. Resolved by implementing flat Data Transfer Objects (DTOs).")
    add_bullet(tf, "Dependency Injection Scoping", "Early confusion between Scoped and Transient DbContext caused concurrency errors. Resolved by properly configuring Scoped lifetimes in Program.cs.")
    add_bullet(tf, "MySQL ORM Driver Selection", "Resolved package version mismatches by utilizing official Oracle MySql.EntityFrameworkCore (v10.0.9) configured cleanly without Pomelo conflicts.")

    c2 = add_card(s16, 6.8, 1.4, 5.7, 5.5, "API Integration & Testing Bottlenecks")
    tf = c2.text_frame
    add_bullet(tf, "DateTime Timezone Drift", "React ISO strings with Sri Lankan UTC+5:30 offset shifted dates by -1 day in MySQL. Resolved by enforcing strict DateTime.UtcNow.Date normalization at API entry.")
    add_bullet(tf, "CORS Pre-Flight Blocks", "Browser blocked cross-origin requests between Vite (port 5173) and ASP.NET Core (port 5000). Resolved by registering app.UseCors('AllowAll') in middleware.")
    add_bullet(tf, "REST Semantic Error Mapping", "Replaced generic 200 OK error payloads with strict HTTP status codes (HTTP 409 Conflict, HTTP 400 Bad Request, HTTP 404 Not Found).")
    add_bullet(tf, "Automated Postman Testing", "Validated API endpoints independently using Swagger UI and Postman before building React UI components.")

    # =========================================================================
    # SLIDE 17: PHASE 2 PRODUCTION ROADMAP (FUTURE ENHANCEMENTS)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_bg(s17, BG_LIGHT)
    add_header(s17, "Phase 2 Production Roadmap: Post-Interim Enhancements")

    c1 = add_card(s17, 0.8, 1.4, 5.7, 2.6, "1. Cryptographic Password Hashing")
    tf = c1.text_frame
    add_bullet(tf, "Salted BCrypt.Net", "Replace demo credentials with BCrypt (work factor 12) or Argon2id salted hashing, compliant with Sri Lanka PDPA No. 9 of 2022.")
    add_bullet(tf, "JWT Token Rotation", "Sign authentication tokens with HMAC-SHA256, stored in HttpOnly, SameSite=Strict cookies.")

    c2 = add_card(s17, 6.8, 1.4, 5.7, 2.6, "2. Two-Factor Authentication (2FA)")
    tf = c2.text_frame
    add_bullet(tf, "TOTP (RFC 6238)", "Require administrators to verify 6-digit ephemeral tokens via Google Authenticator before unlocking inventory controls.")
    add_bullet(tf, "SMS / Email OTP", "Twilio SMS integration to verify guest phone numbers (+94) for high-value suite reservations.")

    c3 = add_card(s17, 0.8, 4.3, 5.7, 2.6, "3. Executive Analytics Dashboard")
    tf = c3.text_frame
    add_bullet(tf, "Visual Telemetry", "Interactive charts (Chart.js / Recharts) tracking Monthly Revenue in LKR, ADR, and RevPAR.")
    add_bullet(tf, "30-Day Gantt Schedule", "Visual horizontal timeline for front-desk room allocation and housekeeping management.")

    c4 = add_card(s17, 6.8, 4.3, 5.7, 2.6, "4. Live Payment Gateway Integration")
    tf = c4.text_frame
    add_bullet(tf, "IPG / PayHere / Stripe", "Direct credit/debit card processing in Sri Lankan Rupees (LKR) with temporary 15-minute booking hold.")
    add_bullet(tf, "Automated Invoicing", "Instant PDF folio receipts emailed automatically to guests upon payment confirmation.")

    # =========================================================================
    # SLIDE 18: CONCLUSION & LIVE DEMONSTRATION HANDOVER
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_bg(s18, DARK_NAVY)

    # Conclusion Card
    c = add_card(s18, 1.5, 1.2, 10.333, 4.8, "Interim Milestone Summary & Handover to Live Demo", 
                 title_color=GOLD, bg_color=RGBColor(19, 42, 74), border_color=RGBColor(30, 60, 102))
    tf = c.text_frame
    
    p0 = tf.add_paragraph()
    p0.text = "All Interim Objectives Successfully Delivered:"
    p0.font.name = "Calibri"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(255, 255, 255)
    p0.space_after = Pt(8)

    add_bullet(tf, "Zero Double-Booking Guarantee", "Proven transactional interval overlap engine rejecting conflicting dates with HTTP 409 Conflict.", pt_size=11)
    add_bullet(tf, "Decoupled 3-Tier Enterprise Viability", "High-performance React 19 SPA communicating with ASP.NET Core 10 Web API and MySQL 8.0.", pt_size=11)
    add_bullet(tf, "Transparent Domestic LKR Pricing", "Exact multi-night bill derivation in Sri Lankan Rupees with zero floating-point rounding errors.", pt_size=11)
    add_bullet(tf, "Verified 55% Prototype", "All 8 formal empirical test cases passed with 100% data integrity verified in MySQL Workbench.", pt_size=11)

    p_hand = tf.add_paragraph()
    p_hand.space_before = Pt(14)
    p_hand.text = "Ready to proceed with Live Software Demonstration & Examiner Q&A."
    p_hand.font.name = "Calibri"
    p_hand.font.size = Pt(14)
    p_hand.font.bold = True
    p_hand.font.color.rgb = RGBColor(165, 215, 232)
    p_hand.alignment = PP_ALIGN.CENTER

    out_pptx = r"C:\Users\PASINDU\Desktop\Interim\Dutch_Point_Negombo_Hotel_Management_System_Interim_Presentation.pptx"
    prs.save(out_pptx)
    print(f"Presentation successfully created: {out_pptx}")

if __name__ == "__main__":
    create_system_presentation()
