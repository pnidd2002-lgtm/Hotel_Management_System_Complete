import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen standard dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    # Color Palette: Executive Navy, Rich Gold, Clean Slate, Card Fill
    DARK_NAVY = RGBColor(11, 25, 44)       # #0B192C (Title Slide Background)
    NAVY = RGBColor(15, 44, 89)            # #0F2C59 (Main Titles / Header)
    GOLD = RGBColor(184, 134, 11)          # #B8860B (Accent Gold)
    BG_LIGHT = RGBColor(248, 249, 250)     # #F8F9FA (Slide Light Background)
    CARD_BG = RGBColor(255, 255, 255)      # White
    CARD_BORDER = RGBColor(222, 226, 230)  # Border gray
    TEXT_DARK = RGBColor(33, 37, 41)       # Body text
    TEXT_MUTED = RGBColor(108, 117, 125)   # Subtitles
    GREEN = RGBColor(40, 167, 69)          # Success
    RED = RGBColor(220, 53, 69)            # Error / Conflict
    BLUE_ACCENT = RGBColor(13, 110, 253)   # Tech accent

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_text="DUTCH POINT NEGOMBO • HOTEL MANAGEMENT SYSTEM"):
        # Header banner shape
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        banner.fill.background()
        banner.line.fill.background()
        
        tf = banner.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = GOLD
        p_cat.space_after = Pt(2)
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(24)
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
        tf.margin_top = Inches(0.22)
        tf.margin_bottom = Inches(0.2)
        
        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Calibri"
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(8)
            
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Premium Theme)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, DARK_NAVY)

    # University Header
    tx_uni = slide1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(0.8))
    tf_uni = tx_uni.text_frame
    p_u1 = tf_uni.paragraphs[0]
    p_u1.text = "ESOFT METRO CAMPUS • FACULTY OF COMPUTING"
    p_u1.font.name = "Calibri"
    p_u1.font.size = Pt(13)
    p_u1.font.bold = True
    p_u1.font.color.rgb = GOLD
    p_u1.alignment = PP_ALIGN.CENTER
    
    p_u2 = tf_uni.add_paragraph()
    p_u2.text = "BIT (Hons) in Software Engineering Degree Programme"
    p_u2.font.name = "Calibri"
    p_u2.font.size = Pt(11)
    p_u2.font.color.rgb = RGBColor(180, 195, 215)
    p_u2.alignment = PP_ALIGN.CENTER

    # Main Project Title
    tx_main = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(1.8))
    tf_main = tx_main.text_frame
    tf_main.word_wrap = True
    p_m1 = tf_main.paragraphs[0]
    p_m1.text = "Web-Based Hotel Management System"
    p_m1.font.name = "Calibri"
    p_m1.font.size = Pt(36)
    p_m1.font.bold = True
    p_m1.font.color.rgb = RGBColor(255, 255, 255)
    p_m1.alignment = PP_ALIGN.CENTER
    p_m1.space_after = Pt(4)
    
    p_m2 = tf_main.add_paragraph()
    p_m2.text = "Case Study: Dutch Point Negombo Boutique Resort"
    p_m2.font.name = "Calibri"
    p_m2.font.size = Pt(20)
    p_m2.font.color.rgb = GOLD
    p_m2.alignment = PP_ALIGN.CENTER

    p_m3 = tf_main.add_paragraph()
    p_m3.text = "Project Interim Viva & Demonstration (55% - 60% Milestone Completion)"
    p_m3.font.name = "Calibri"
    p_m3.font.size = Pt(13)
    p_m3.font.color.rgb = RGBColor(160, 185, 210)
    p_m3.alignment = PP_ALIGN.CENTER

    # 4 Team Members Cards (Grid of 4)
    members = [
        ("I.D.P.N Iddamalgoda", "E269559", "Lead Developer & System Admin", "Architecture & Concurrency"),
        ("H.M.Y.R Herath", "E267614", "Backend Software Engineer", "ASP.NET Core Web API & LINQ"),
        ("Y.M.A.Y Bandara", "E267609", "Frontend Software Engineer", "React SPA & Booking UI"),
        ("A.G.H.H Jinadasa", "E267612", "QA & Requirements Engineer", "Requirements Traceability & Testing")
    ]
    card_w = 2.65
    start_x = 1.0
    for i, (name, sid, role, area) in enumerate(members):
        c_left = start_x + (i * 2.9)
        card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(4.3), Inches(card_w), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(19, 42, 74)
        card.line.color.rgb = RGBColor(35, 70, 115)
        card.line.width = Pt(1.5)
        
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.15)
        ctf.margin_top = Inches(0.18)
        
        p = ctf.paragraphs[0]
        p.text = name
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
        
        p2 = ctf.add_paragraph()
        p2.text = f"ID: {sid}"
        p2.font.name = "Calibri"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = GOLD
        p2.alignment = PP_ALIGN.CENTER
        p2.space_after = Pt(6)
        
        p3 = ctf.add_paragraph()
        p3.text = role
        p3.font.name = "Calibri"
        p3.font.size = Pt(10)
        p3.font.bold = True
        p3.font.color.rgb = RGBColor(210, 225, 245)
        p3.alignment = PP_ALIGN.CENTER
        
        p4 = ctf.add_paragraph()
        p4.text = area
        p4.font.name = "Calibri"
        p4.font.size = Pt(9.5)
        p4.font.color.rgb = RGBColor(140, 165, 195)
        p4.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: PROBLEM BACKGROUND & CONTEXT
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_LIGHT)
    add_header(slide2, "Background & The Operational Problem in Negombo", "CHAPTER 01 • INTRODUCTION")

    # 3 Cards Layout: The Business Context, The Core Operational Problems, The Impact
    c1 = add_card(slide2, 0.8, 1.8, 3.7, 5.0, "1. Boutique Resort Context")
    tf1 = c1.text_frame
    bullets1 = [
        ("Location: ", "Dutch Point Negombo is a boutique beachfront resort in Western Province, Sri Lanka."),
        ("Inventory: ", "Operates luxury accommodations (Deluxe, Ocean View Suites, Family Villas)."),
        ("Guest Demographic: ", "Serves both international tourists and domestic weekend travelers."),
        ("Current Operation: ", "Historically relied on handwritten paper registers, phone calls, and WhatsApp messages for booking rooms.")
    ]
    for b_title, b_desc in bullets1:
        p = tf1.add_paragraph()
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.space_after = Pt(8)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = TEXT_DARK

    c2 = add_card(slide2, 4.8, 1.8, 3.7, 5.0, "2. Critical Flaws Identified")
    tf2 = c2.text_frame
    bullets2 = [
        ("Frequent Double Bookings: ", "Front-desk shifts overlapping led to two guests booking the same suite on the same night."),
        ("Severe Commission Loss: ", "Third-party OTAs (Booking.com / Agoda) charge 15% - 20% commission on every reservation."),
        ("No Real-Time Visibility: ", "Guests calling reception had to wait 10+ minutes for staff to physically search through paper ledgers."),
        ("Lost Guest Records: ", "Handwritten cards often misplaced, causing disputes over headcounts, special requests, and room rates.")
    ]
    for b_title, b_desc in bullets2:
        p = tf2.add_paragraph()
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.space_after = Pt(8)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.color.rgb = RED
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = TEXT_DARK

    c3 = add_card(slide2, 8.8, 1.8, 3.7, 5.0, "3. Currency & Localization")
    tf3 = c3.text_frame
    bullets3 = [
        ("Foreign Currency Disconnect: ", "Commercial software quotes rates in USD ($), forcing confusing bank conversion rates on Sri Lankan guests."),
        ("Lack of Direct Settlement: ", "Hotel management demanded all rates and invoices be localized strictly in Sri Lankan Rupees (LKR)."),
        ("Headcount Safety: ", "Guests booking 2-person suites were arriving with 4–5 guests without capacity validation."),
        ("The Solution Needed: ", "A dedicated, web-based hotel management system built specifically for Dutch Point Negombo's workflow.")
    ]
    for b_title, b_desc in bullets3:
        p = tf3.add_paragraph()
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.space_after = Pt(8)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.color.rgb = GOLD
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 3: PROJECT AIMS & CORE OBJECTIVES
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_LIGHT)
    add_header(slide3, "Project Aims & Business Objectives", "PROJECT GOALS & SCOPE")

    objectives = [
        ("Objective 1: Direct Commission-Free Bookings",
         "Develop a responsive Single Page Application (React) allowing travelers to browse suites, check real-time availability, and reserve directly with zero OTA commission deductions.",
         "Presentation Tier", BLUE_ACCENT),
        ("Objective 2: 100% Prevention of Double Bookings",
         "Design an atomic transactional check inside ASP.NET Core 8 Web API that mathematically verifies date intervals before saving, returning HTTP 409 Conflict upon collision.",
         "Backend Concurrency", RED),
        ("Objective 3: Secure Role-Based Access Control (RBAC)",
         "Implement isolated user access claims (Admin, Receptionist, Customer) to ensure public visitors cannot escalate privileges while staff manage operations safely.",
         "Security & Identity", NAVY),
        ("Objective 4: Currency Localization & Capacity Safety",
         "Standardize all room prices in Sri Lankan Rupees (LKR 28,000 to LKR 140,000) and enforce guest headcount validation (Capacity >= Guests) on all reservations.",
         "Business Localization", GOLD),
        ("Objective 5: Operational Front-Desk Occupancy Tracker",
         "Equip front-desk staff with an interactive live Occupancy Tracker providing single-day occupancy inspection and full resort booking roster synchronization.",
         "Hotel Operations", GREEN)
    ]
    
    for idx, (title, desc, tag, tag_color) in enumerate(objectives):
        top_pos = 1.7 + (idx * 1.05)
        card = add_card(slide3, 0.8, top_pos, 11.733, 0.95)
        tf = card.text_frame
        p = tf.paragraphs[0]
        p.space_after = Pt(2)
        r_tag = p.add_run(); r_tag.text = f"[{tag.upper()}]  "; r_tag.font.bold = True; r_tag.font.size = Pt(10.5); r_tag.font.color.rgb = tag_color
        r_tit = p.add_run(); r_tit.text = title; r_tit.font.bold = True; r_tit.font.size = Pt(13); r_tit.font.color.rgb = NAVY
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 4: LITERATURE & INDUSTRIAL COMPARISON
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_LIGHT)
    add_header(slide4, "Literature Review & Industrial Systems Comparison", "CHAPTER 01 • BENCHMARKING")

    # 4 Column Comparison Table Layout
    cols = [
        ("Cloudbeds PMS", "Commercial Cloud PMS", CARD_BG, [
            ("Target Market", "Mid-to-large international chains"),
            ("Pricing Model", "High monthly subscription ($150+ / mo)"),
            ("Commission", "Zero direct, but adds channel manager fees"),
            ("Currency", "Defaults to USD / EUR (Conversion friction)"),
            ("Downside", "Cost-prohibitive for small boutique hotels")
        ]),
        ("Oracle Opera Cloud", "Enterprise Resort PMS", CARD_BG, [
            ("Target Market", "5-star multi-national resorts"),
            ("Pricing Model", "Enterprise licensing ($1,000s + setup)"),
            ("Hardware", "Requires dedicated enterprise infrastructure"),
            ("Complexity", "Steep learning curve; weeks of staff training"),
            ("Downside", "Massively over-engineered for 10-25 rooms")
        ]),
        ("Booking.com Extranet", "OTA Channel Platform", CARD_BG, [
            ("Target Market", "Global booking visibility"),
            ("Pricing Model", "No monthly fee, but heavy 15-20% cut"),
            ("Overbooking", "Sync delays cause frequent double bookings"),
            ("Control", "Resort has zero ownership of guest data"),
            ("Downside", "Eats significant portion of hotel profits")
        ]),
        ("Dutch Point PMS (Proposed)", "Custom In-House Solution", RGBColor(240, 246, 255), [
            ("Target Market", "Tailored for Dutch Point Negombo"),
            ("Pricing Model", "One-time internal build; ZERO subscriptions"),
            ("Commission", "100% Commission-Free direct bookings"),
            ("Currency", "Natively in Sri Lankan Rupees (LKR)"),
            ("Advantage", "Direct database control, lightweight & fast")
        ])
    ]

    for c_idx, (c_name, c_sub, bg, items) in enumerate(cols):
        c_x = 0.8 + (c_idx * 2.95)
        card = add_card(slide4, c_x, 1.8, 2.85, 5.1, bg_color=bg)
        tf = card.text_frame
        
        p = tf.paragraphs[0]
        p.text = c_name
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = GOLD if "Proposed" in c_name else NAVY
        p.space_after = Pt(1)
        
        p_sub = tf.add_paragraph()
        p_sub.text = c_sub
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(9.5)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(10)
        
        for k, v in items:
            p_item = tf.add_paragraph()
            p_item.font.name = "Calibri"
            p_item.font.size = Pt(10)
            p_item.space_after = Pt(6)
            r_k = p_item.add_run(); r_k.text = k + ":\n"; r_k.font.bold = True; r_k.font.color.rgb = NAVY
            r_v = p_item.add_run(); r_v.text = v; r_v.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 5: REQUIREMENTS ENGINEERING (THE 5 STAGES)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_LIGHT)
    add_header(slide5, "Requirements Engineering (Lecturer's 5-Stage SFE Process)", "CHAPTER 02 • METHODOLOGY")

    stages = [
        ("1. Stakeholder Identification",
         "Identified 4 primary user groups: Resort General Manager, Front Desk Receptionists, Guests/Tourists, and System Administrator. Formulated Table 5 Stakeholder Profiles.",
         NAVY),
        ("2. Requirements Gathering",
         "Collected operational needs using 4 proven techniques: Semi-Structured Interviews with GM, Historical Logbook Audits, Direct Front-Desk Observation, and 25 Guest Surveys.",
         BLUE_ACCENT),
        ("3. Requirements Analysis",
         "Examined findings to resolve conflicting needs and prioritize essential scope using the MoSCoW Framework (Must, Should, Could, Won't Have) in Table 6.",
         GOLD),
        ("4. Requirements Specification",
         "Documented unambiguous functional rules adhering to IEEE 830 standards, Agile User Stories ('As a [role], I want [feature] so that [benefit]'), and measurable Acceptance Criteria.",
         NAVY),
        ("5. Requirements Validation",
         "Verified specifications before writing code via Formal Supervisor Walkthroughs, Throwaway UI Mockup testing with receptionists, and the Requirements Traceability Matrix (RTM).",
         GREEN)
    ]

    for s_idx, (s_title, s_desc, s_color) in enumerate(stages):
        top_pos = 1.75 + (s_idx * 1.02)
        card = add_card(slide5, 0.8, top_pos, 11.733, 0.92)
        tf = card.text_frame
        
        p = tf.paragraphs[0]
        p.space_after = Pt(2)
        r_step = p.add_run(); r_step.text = f"STAGE {s_idx+1}: "; r_step.font.bold = True; r_step.font.size = Pt(11); r_step.font.color.rgb = s_color
        r_tit = p.add_run(); r_tit.text = s_title; r_tit.font.bold = True; r_tit.font.size = Pt(13); r_tit.font.color.rgb = NAVY
        
        p2 = tf.add_paragraph()
        p2.text = s_desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 6: MOSCOW PRIORITIZATION MATRIX
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_LIGHT)
    add_header(slide6, "Requirements Analysis: MoSCoW Prioritization", "CHAPTER 02 • SCOPE SELECTION")

    # 4 Quadrants / Cards: MUST, SHOULD, COULD, WON'T
    moscow = [
        ("MUST HAVE (Mandatory for Interim)", GREEN, [
            "• Secure User Authentication & JWT Claims",
            "• Multi-Variable Room Search (Dates & Capacity)",
            "• Transactional Double-Booking Prevention (409 Conflict)",
            "• Room Pricing Displayed Strictly in Sri Lankan Rupees (LKR)",
            "• Customer Reservation Booking Creation & Persistence"
        ]),
        ("SHOULD HAVE (Highly Desirable)", BLUE_ACCENT, [
            "• Interactive Occupied Rooms Tracker for Front Desk",
            "• Guest Headcount Filter & Overcapacity Rejection",
            "• Real-Time Dynamic Room Status Badges (Available / Occupied)",
            "• Administrative Room Inventory Management (Add/Edit Suites)",
            "• Front-Desk Booking Cancellation & History Roster"
        ]),
        ("COULD HAVE (Nice to Have)", GOLD, [
            "• Housekeeping Cleaning Status Tags (Clean / Dirty)",
            "• Special Guest Request Notes field on Checkout",
            "• Automated SMS Alerts upon Booking Confirmation",
            "• Multi-photo Room Image Gallery Carousel",
            "• Seasonal Promotional Discount Banners"
        ]),
        ("WON'T HAVE (Deferred to Final Submission)", RED, [
            "• Live IPG Payment Gateway (PayHere Sandbox held for 100% demo)",
            "• Automated PDF Invoice & Printable Receipt Generation",
            "• Automated Email Server SMTP Dispatching",
            "• Predictive Occupancy Machine Learning Analytics",
            "• Multi-property Hotel Group Management"
        ])
    ]

    for m_idx, (m_title, m_color, m_items) in enumerate(moscow):
        col = m_idx % 2
        row = m_idx // 2
        m_x = 0.8 + (col * 5.95)
        m_y = 1.8 + (row * 2.6)
        
        card = add_card(slide6, m_x, m_y, 5.75, 2.45, m_title, title_color=m_color)
        tf = card.text_frame
        for item in m_items:
            p = tf.add_paragraph()
            p.text = item
            p.font.name = "Calibri"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_DARK
            p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 7: THREE-TIER SYSTEM ARCHITECTURE
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_LIGHT)
    add_header(slide7, "Three-Tier Enterprise System Architecture", "CHAPTER 03 • SYSTEM DESIGN")

    # 3 Large Tier Cards
    tiers = [
        ("Tier 1: Presentation Tier", "Client-Side User Interface", BLUE_ACCENT, [
            ("Core Framework", "React 18 + Vite SPA Client"),
            ("UI & Styling", "Bootstrap 5 + Custom Boutique Coastal Theme"),
            ("State Management", "React Hooks (useState, useEffect, custom context)"),
            ("Communication", "Asynchronous HTTP REST calls via fetch() API"),
            ("Key Screens", "Guest Search Portal, Booking Modal, Front-Desk Occupancy Tracker, Admin Dashboard")
        ]),
        ("Tier 2: Application Tier", "Business Logic & REST API", NAVY, [
            ("Backend Framework", "ASP.NET Core 8 Web API (C#)"),
            ("Data Access ORM", "Entity Framework Core (EF Core 8)"),
            ("Core Controllers", "AuthController, RoomsController, BookingsController, DashboardController"),
            ("Key Algorithm", "Double-Booking Transactional Overlap Prevention"),
            ("Security Controls", "CORS policy, model validation, parameterized queries, RBAC claim validation")
        ]),
        ("Tier 3: Data Tier", "Relational Database Management", GOLD, [
            ("Database Engine", "MySQL 8.0 Relational Server (Port 3306)"),
            ("Database Schema", "hotel_db (Users, Rooms, Bookings, Payments)"),
            ("Referential Integrity", "Strict Foreign Key constraints (CASCADE / RESTRICT)"),
            ("Currency Precision", "decimal(10,2) for exact Sri Lankan Rupee calculations"),
            ("Optimization", "Indexed columns on CheckInDate, CheckOutDate, RoomId for sub-50ms query latency")
        ])
    ]

    for t_idx, (t_name, t_sub, t_color, t_items) in enumerate(tiers):
        t_x = 0.8 + (t_idx * 3.95)
        card = add_card(slide7, t_x, 1.8, 3.8, 5.0)
        tf = card.text_frame
        
        p = tf.paragraphs[0]
        p.text = t_name
        p.font.name = "Calibri"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = t_color
        p.space_after = Pt(1)
        
        p_sub = tf.add_paragraph()
        p_sub.text = t_sub
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(10)
        
        for k, v in t_items:
            p_item = tf.add_paragraph()
            p_item.font.name = "Calibri"
            p_item.font.size = Pt(10.5)
            p_item.space_after = Pt(6)
            r_k = p_item.add_run(); r_k.text = "• " + k + ": "; r_k.font.bold = True; r_k.font.color.rgb = NAVY
            r_v = p_item.add_run(); r_v.text = v; r_v.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 8: DATABASE DESIGN & ENTITIES
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, BG_LIGHT)
    add_header(slide8, "Database Design & Data Dictionary (hotel_db)", "CHAPTER 03 • RELATIONAL SCHEMA")

    # 4 Tables Cards: Users, Rooms, Bookings, Payments
    db_tables = [
        ("Table: Users", NAVY, [
            ("UserId (PK)", "INT AUTO_INCREMENT", "Unique identifier"),
            ("FullName", "VARCHAR(100)", "Customer or staff name"),
            ("Email (UNIQUE)", "VARCHAR(100)", "Login identity"),
            ("PasswordHash", "VARCHAR(255)", "Secure credentials"),
            ("Role", "VARCHAR(20)", "Admin / Customer"),
            ("Phone", "VARCHAR(20)", "Contact phone number")
        ]),
        ("Table: Rooms", BLUE_ACCENT, [
            ("RoomId (PK)", "INT AUTO_INCREMENT", "Unique room ID"),
            ("RoomNumber (UQ)", "VARCHAR(10)", "e.g., Room 101, 201"),
            ("RoomType", "VARCHAR(50)", "Deluxe, Ocean Suite"),
            ("PricePerNight", "DECIMAL(10,2)", "Price in LKR"),
            ("Capacity", "INT", "Max headcount (2, 4)"),
            ("Status", "VARCHAR(20)", "Available / Maintenance")
        ]),
        ("Table: Bookings", GREEN, [
            ("BookingId (PK)", "INT AUTO_INCREMENT", "Reservation number"),
            ("CustomerId (FK)", "INT", "References Users(UserId)"),
            ("RoomId (FK)", "INT", "References Rooms(RoomId)"),
            ("CheckInDate", "DATE", "Stay arrival date"),
            ("CheckOutDate", "DATE", "Stay departure date"),
            ("NumberOfGuests", "INT", "Enforced <= Capacity"),
            ("TotalAmount", "DECIMAL(10,2)", "Total Stay in LKR"),
            ("BookingStatus", "VARCHAR(30)", "Confirmed / Cancelled")
        ]),
        ("Table: Payments", GOLD, [
            ("PaymentId (PK)", "INT AUTO_INCREMENT", "Transaction ID"),
            ("BookingId (FK)", "INT", "References Bookings"),
            ("Amount", "DECIMAL(10,2)", "Settlement amount LKR"),
            ("PaymentMethod", "VARCHAR(30)", "Cash / Card / Transfer"),
            ("PaymentStatus", "VARCHAR(20)", "Completed / Pending"),
            ("PaidAt", "DATETIME", "Timestamp of payment")
        ])
    ]

    for d_idx, (t_name, t_color, t_cols) in enumerate(db_tables):
        d_x = 0.8 + (d_idx * 2.95)
        card = add_card(slide8, d_x, 1.8, 2.85, 5.0, t_name, title_color=t_color)
        tf = card.text_frame
        for col_name, col_type, col_note in t_cols:
            p = tf.add_paragraph()
            p.font.name = "Calibri"
            p.font.size = Pt(10)
            p.space_after = Pt(4)
            r_n = p.add_run(); r_n.text = col_name + "\n"; r_n.font.bold = True; r_n.font.color.rgb = NAVY
            r_t = p.add_run(); r_t.text = f"{col_type} - {col_note}"; r_t.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 9: KEY TECHNICAL INNOVATION: DOUBLE BOOKING ALGORITHM
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, BG_LIGHT)
    add_header(slide9, "Core Technical Highlight: Concurrency & Overlap Algorithm", "CHAPTER 04 • IMPLEMENTATION")

    # Left: Explanation & Math Formula | Right: Code Snippet
    c_left = add_card(slide9, 0.8, 1.8, 5.7, 5.0, "The Double-Booking Problem")
    tf_l = c_left.text_frame
    bullets_algo = [
        ("The Challenge: ", "If two guests book Room 101 simultaneously, a race condition could accept both, humiliating hotel staff when guests arrive."),
        ("Mathematical Rule: ", "Two date intervals [A_in, A_out] and [B_in, B_out] overlap IF AND ONLY IF:\n(ExistingCheckIn < RequestedCheckOut) AND (ExistingCheckOut > RequestedCheckIn)."),
        ("Server-Side Enforcement: ", "Validation is never trusted to the frontend. The check executes inside an ACID database transaction in ASP.NET Core prior to saving."),
        ("Immediate Rejection: ", "If an overlap exists, the backend instantly rejects the request with HTTP 409 Conflict, returning the existing booking ID and dates."),
        ("Clean Cancellation: ", "Cancelled bookings are ignored by the filter, immediately freeing up dates for other travelers.")
    ]
    for b_title, b_desc in bullets_algo:
        p = tf_l.add_paragraph()
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = TEXT_DARK

    c_right = add_card(slide9, 6.8, 1.8, 5.733, 5.0, "C# / EF Core LINQ Implementation", title_color=NAVY, bg_color=DARK_NAVY)
    tf_r = c_right.text_frame
    
    code_lines = [
        "// BookingsController.cs (Transactional Overlap Check)",
        "var isOverlapping = await _context.Bookings",
        "    .AnyAsync(b =>",
        "        b.RoomId == request.RoomId &&",
        "        (b.BookingStatus == \"Confirmed\" ||",
        "         b.BookingStatus == \"Checked-In\") &&",
        "        b.CheckInDate < request.CheckOutDate &&",
        "        b.CheckOutDate > request.CheckInDate",
        "    );",
        "",
        "if (isOverlapping)",
        "{",
        "    // Rejects with HTTP 409 Conflict",
        "    return Conflict(new {",
        "        message = \"Room already booked for selected dates.\"",
        "    });",
        "}",
        "",
        "// Proceed to save reservation in LKR",
        "_context.Bookings.Add(newBooking);",
        "await _context.SaveChangesAsync();"
    ]
    for cl in code_lines:
        p = tf_r.add_paragraph()
        p.font.name = "Consolas"
        p.font.size = Pt(9.5)
        p.space_after = Pt(0)
        if "//" in cl:
            p.font.color.rgb = RGBColor(140, 160, 180)
        elif "Conflict" in cl or "isOverlapping" in cl:
            p.font.color.rgb = RGBColor(255, 120, 120)
            p.font.bold = True
        elif "await" in cl or "var" in cl or "return" in cl:
            p.font.color.rgb = RGBColor(120, 200, 255)
        else:
            p.font.color.rgb = RGBColor(230, 235, 240)

    # =========================================================================
    # SLIDE 10: SECURITY & BASELINE ADJUSTMENTS
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, BG_LIGHT)
    add_header(slide10, "Security Hardening & Scope Baseline Adjustments", "CHAPTER 02 • REQUIREMENTS CHANGE CONTROL")

    # 3 Cards: Broken Access Control Fix, Currency Migration, Headcount Safety
    changes = [
        ("Change 1: Broken Access Control Fixed", RED, [
            ("Issue Identified", "Initial prototype had a dropdown on the signup modal where any public user could select 'Admin'."),
            ("Security Vulnerability", "OWASP Top 10 - Broken Access Control & Privilege Escalation."),
            ("Resolution", "Completely removed client-side role dropdown. Public registrations are strictly hardcoded to 'Customer' on the backend."),
            ("Admin Isolation", "Dedicated Admin credentials (username: Pasindu) are managed directly in the MySQL database.")
        ]),
        ("Change 2: Currency Localization to LKR", GOLD, [
            ("Issue Identified", "Early proposal drafts used US Dollars ($), leading to exchange rate confusion."),
            ("Stakeholder Need", "Dutch Point Negombo management required all billing in Sri Lankan Rupees for accurate daily reconciliation."),
            ("Resolution", "Migrated all pricing models, API calculations, and UI displays to Sri Lankan Rupees (LKR 28,000 to LKR 140,000 / night)."),
            ("Impact", "Clean local guest transactions and direct matching with commercial bank deposits.")
        ]),
        ("Change 3: Guest Headcount & Safety", BLUE_ACCENT, [
            ("Issue Identified", "Guests were booking 2-person suites for 5 adults without warning, violating resort safety regulations."),
            ("Resolution", "Added dynamic Guest Count selector to search bar. The backend enforces Capacity >= Guests upon booking."),
            ("UI Feedback", "Rooms with insufficient capacity are automatically filtered out of search results."),
            ("Verification", "Verified via Test Case TC-09 (Overcapacity Headcount Rejection).")
        ])
    ]

    for ch_idx, (ch_title, ch_color, ch_items) in enumerate(changes):
        ch_x = 0.8 + (ch_idx * 3.95)
        card = add_card(slide10, ch_x, 1.8, 3.8, 5.0, ch_title, title_color=ch_color)
        tf = card.text_frame
        for k, v in ch_items:
            p = tf.add_paragraph()
            p.font.name = "Calibri"
            p.font.size = Pt(11)
            p.space_after = Pt(8)
            r_k = p.add_run(); r_k.text = "• " + k + ":\n"; r_k.font.bold = True; r_k.font.color.rgb = NAVY
            r_v = p.add_run(); r_v.text = v; r_v.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 11: SYSTEM DEMONSTRATION HIGHLIGHTS
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, BG_LIGHT)
    add_header(slide11, "Practical Demonstration Highlights (What We Show Live)", "INTERIM SYSTEM DEMO")

    demo_steps = [
        ("Step 1: Public Registration & RBAC",
         "Demonstrate registering 'Kasun Silva' as a Customer. Prove via MySQL Workbench that Kasun is inserted with Role='Customer', and admin menu items remain hidden.",
         BLUE_ACCENT),
        ("Step 2: Availability & Capacity Search",
         "Select stay dates (Oct 10-12, 2026) and 2 Guests. Demonstrate dynamic green 'AVAILABLE' badge and LKR rate calculation (2 nights * LKR 28,000 = LKR 56,000).",
         GREEN),
        ("Step 3: Live Booking Persistence",
         "Complete reservation for Deluxe Suite 101. Show instant generation of Reservation ID (RES-1001) and query MySQL Bookings table to prove row insertion.",
         GOLD),
        ("Step 4: Live Double-Booking Prevention",
         "Attempt to book the identical Suite 101 for overlapping dates (Oct 11-14). Show immediate UI rejection and inspect F12 DevTools returning HTTP 409 Conflict.",
         RED),
        ("Step 5: Front-Desk Occupancy Tracker",
         "Open Occupancy Tracker. Demonstrate single-date occupancy query (showing Suite 101 Occupied) and toggle to 'All Active Bookings' showing the full resort roster.",
         NAVY),
        ("Step 6: Admin Dashboard & Revenue KPIs",
         "Log in as Admin ('Pasindu'). Show dynamic appearance of Admin Dashboard, live revenue tracking in LKR, and active reservation management tools.",
         BLUE_ACCENT)
    ]

    for d_idx, (d_title, d_desc, d_color) in enumerate(demo_steps):
        col = d_idx % 2
        row = d_idx // 2
        d_x = 0.8 + (col * 5.95)
        d_y = 1.8 + (row * 1.7)
        
        card = add_card(slide11, d_x, d_y, 5.75, 1.55, d_title, title_color=d_color)
        tf = card.text_frame
        p = tf.paragraphs[0]
        p.font.size = Pt(13)
        p.space_after = Pt(2)
        
        p2 = tf.add_paragraph()
        p2.text = d_desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 12: TESTING & VALIDATION (TRACEABILITY MATRIX)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, BG_LIGHT)
    add_header(slide12, "System Verification & Traceability Matrix (RTM)", "CHAPTER 05 • TESTING & QUALITY")

    # Table of Test Cases: ID, Scenario, Input, Expected, Status
    test_cases = [
        ("TC-01", "Valid Room Booking", "Select available dates & 2 guests", "Booking saved, total LKR calculated, RES ID issued", "PASS"),
        ("TC-02", "Past Date Rejection", "Select check-in earlier than today", "Frontend & API block submission with date error", "PASS"),
        ("TC-03", "Reversed Dates Rejection", "Check-out date set before check-in", "Validation error: Check-out must follow check-in", "PASS"),
        ("TC-04", "Double-Booking Overlap", "Book room with overlapping dates", "Rejected with HTTP 409 Conflict, no DB write", "PASS"),
        ("TC-05", "Customer Role Isolation", "Register new public user account", "Assigned 'Customer' role, admin menus hidden", "PASS"),
        ("TC-06", "Admin Dashboard Access", "Authenticate with 'Pasindu' credentials", "Admin navbar unlocked, revenue stats displayed", "PASS"),
        ("TC-07", "Reservation Cancellation", "Click Cancel in My Bookings / Admin", "Status updated to 'Cancelled', room freed up", "PASS"),
        ("TC-08", "Occupancy Tracker Sync", "Query target date in Occupancy view", "Displays occupied suites, guest name, contact info", "PASS"),
        ("TC-09", "Overcapacity Rejection", "Book 2-person suite with 4 guests", "Search filters room out; API rejects with HTTP 400", "PASS")
    ]

    for t_idx, (tid, scen, inp, exp, stat) in enumerate(test_cases):
        top_pos = 1.7 + (t_idx * 0.57)
        card = add_card(slide12, 0.8, top_pos, 11.733, 0.52)
        tf = card.text_frame
        p = tf.paragraphs[0]
        p.space_after = Pt(0)
        
        r_id = p.add_run(); r_id.text = f"[{tid}]  "; r_id.font.bold = True; r_id.font.size = Pt(10.5); r_id.font.color.rgb = NAVY
        r_sc = p.add_run(); r_sc.text = scen + "  |  "; r_sc.font.bold = True; r_sc.font.size = Pt(10.5); r_sc.font.color.rgb = BLUE_ACCENT
        r_ex = p.add_run(); r_ex.text = "Expected: " + exp + "  "; r_ex.font.size = Pt(9.5); r_ex.font.color.rgb = TEXT_DARK
        r_st = p.add_run(); r_st.text = f"[{stat}]"; r_st.font.bold = True; r_st.font.size = Pt(10.5); r_st.font.color.rgb = GREEN

    # =========================================================================
    # SLIDE 13: PROJECT MANAGEMENT & INTERIM PROGRESS
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, BG_LIGHT)
    add_header(slide13, "Project Management & Milestone Completion (55%–60%)", "CHAPTER 06 • PROGRESS REVIEW")

    # Left: Completed Modules (55-60%) | Right: Gantt Chart Tracking
    c_comp = add_card(slide13, 0.8, 1.8, 5.7, 5.0, "Completed Modules (55% - 60%)", title_color=GREEN)
    tf_c = c_comp.text_frame
    comp_items = [
        ("Stakeholder Identification & Elicitation: ", "100% Complete"),
        ("Literature Review & Technology Benchmarking: ", "100% Complete"),
        ("Database Relational Schema (hotel_db): ", "100% Complete"),
        ("Three-Tier ASP.NET Core Web API: ", "100% Complete"),
        ("React Single Page Application Client: ", "100% Complete"),
        ("Double-Booking Concurrency Algorithm: ", "100% Complete"),
        ("Currency Localization to LKR: ", "100% Complete"),
        ("Interactive Front-Desk Occupancy Tracker: ", "100% Complete"),
        ("Admin KPI Revenue Dashboard: ", "80% Complete")
    ]
    for it, st in comp_items:
        p = tf_c.add_paragraph()
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.space_after = Pt(4)
        r1 = p.add_run(); r1.text = "✔ " + it; r1.font.bold = True; r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = st; r2.font.bold = True; r2.font.color.rgb = GREEN

    c_gantt = add_card(slide13, 6.8, 1.8, 5.733, 5.0, "Milestone Tracking & Schedule Status", title_color=NAVY)
    tf_g = c_gantt.text_frame
    gantt_items = [
        ("Phase 1: Project Proposal & Scope Approval", "Weeks 1 - 3", "Completed on Schedule"),
        ("Phase 2: Requirements Engineering (SFE 5 Stages)", "Weeks 4 - 6", "Completed on Schedule"),
        ("Phase 3: Database & Core Backend Architecture", "Weeks 7 - 9", "Completed on Schedule"),
        ("Phase 4: Frontend Development & Concurrency", "Weeks 10 - 12", "Completed on Schedule"),
        ("Phase 5: Interim Report & System Demo (55-60%)", "Current Viva", "Delivered Today"),
        ("Phase 6: Payment Gateway, PDF & SMS Alerts", "Weeks 13 - 16", "Final Semester Target"),
        ("Phase 7: Final Dissertation & Live Defense", "Weeks 17 - 18", "Final Submission Target")
    ]
    for m_name, m_time, m_stat in gantt_items:
        p = tf_g.add_paragraph()
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.space_after = Pt(5)
        r1 = p.add_run(); r1.text = "• " + m_name + "\n"; r1.font.bold = True; r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = f"  Timeline: {m_time}  |  Status: "; r2.font.color.rgb = TEXT_MUTED
        r3 = p.add_run(); r3.text = m_stat; r3.font.bold = True
        r3.font.color.rgb = GREEN if "Completed" in m_stat or "Today" in m_stat else GOLD

    # =========================================================================
    # SLIDE 14: FINAL SEMESTER ROADMAP (REMAINING 40%)
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, BG_LIGHT)
    add_header(slide14, "Final Semester Roadmap (Remaining 40% to 100%)", "FUTURE IMPLEMENTATION")

    # 4 Cards for Final Features
    final_features = [
        ("Module 1: Payment Gateway (IPG)", BLUE_ACCENT, [
            ("Objective", "Integrate PayHere Sandbox payment gateway for online credit/debit card processing."),
            ("Security", "Tokenized card transactions, webhook signature verification, and HTTPS encryption."),
            ("Outcome", "Eliminates cash-only restrictions and guarantees prepaid revenue for the hotel.")
        ]),
        ("Module 2: Automated PDF Invoicing", NAVY, [
            ("Objective", "Implement automated PDF invoice and receipt generation upon booking confirmation."),
            ("Features", "Official Dutch Point Negombo letterhead, tax breakdown, guest details, and unique QR code."),
            ("Outcome", "Allows guests and corporate travelers to instantly download travel expense receipts.")
        ]),
        ("Module 3: SMS & Email Notifications", GOLD, [
            ("Objective", "Connect Twilio / Dialog SMS Gateway and SMTP email dispatcher."),
            ("Triggers", "Immediate SMS dispatch upon reservation, 24-hour pre-arrival reminders, and cancellation alerts."),
            ("Outcome", "Reduces guest no-shows and eliminates telephone confirmation delays.")
        ]),
        ("Module 4: Business Intelligence Analytics", GREEN, [
            ("Objective", "Build advanced operational analytics for resort management."),
            ("Metrics", "Monthly RevPAR (Revenue Per Available Room), Average Daily Rate (ADR), and occupancy heatmaps."),
            ("Outcome", "Empowers hotel management with data-driven peak-season pricing strategies.")
        ])
    ]

    for f_idx, (f_title, f_color, f_items) in enumerate(final_features):
        f_x = 0.8 + (f_idx * 2.95)
        card = add_card(slide14, f_x, 1.8, 2.85, 5.0, f_title, title_color=f_color)
        tf = card.text_frame
        for k, v in f_items:
            p = tf.add_paragraph()
            p.font.name = "Calibri"
            p.font.size = Pt(10.5)
            p.space_after = Pt(8)
            r_k = p.add_run(); r_k.text = "• " + k + ":\n"; r_k.font.bold = True; r_k.font.color.rgb = NAVY
            r_v = p.add_run(); r_v.text = v; r_v.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 15: CONCLUSION & Q&A DEFENSE (Dark Navy Theme)
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15, DARK_NAVY)

    tx_concl = slide15.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(10.333), Inches(4.8))
    tf_c = tx_concl.text_frame
    tf_c.word_wrap = True
    
    p1 = tf_c.paragraphs[0]
    p1.text = "DUTCH POINT NEGOMBO • HOTEL MANAGEMENT SYSTEM"
    p1.font.name = "Calibri"
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = GOLD
    p1.alignment = PP_ALIGN.CENTER
    p1.space_after = Pt(8)

    p2 = tf_c.add_paragraph()
    p2.text = "Summary of Interim Outcomes"
    p2.font.name = "Calibri"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)
    p2.alignment = PP_ALIGN.CENTER
    p2.space_after = Pt(20)

    concl_points = [
        "✔ Successfully built an enterprise Three-Tier solution (React SPA + ASP.NET Core 8 Web API + MySQL).",
        "✔ Mathematically eradicated double bookings via transactional server-side LINQ overlap checks (HTTP 409).",
        "✔ Fully localized pricing into Sri Lankan Rupees (LKR) and enforced guest headcount capacity limits.",
        "✔ Delivered an intuitive front-desk Occupancy Tracker with single-day filter and full booking roster views.",
        "✔ Project is strictly on schedule at 55% - 60% completion, prepared for Final Semester implementation."
    ]
    for cp in concl_points:
        p = tf_c.add_paragraph()
        p.text = cp
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(220, 235, 250)
        p.space_after = Pt(8)

    p_qa = tf_c.add_paragraph()
    p_qa.text = "\nThank you! We welcome questions from the examination panel."
    p_qa.font.name = "Calibri"
    p_qa.font.size = Pt(18)
    p_qa.font.bold = True
    p_qa.font.color.rgb = GOLD
    p_qa.alignment = PP_ALIGN.CENTER

    # Save presentation
    out_pptx = r"C:\Users\PASINDU\Desktop\Interim\Dutch_Point_Negombo_Hotel_Management_System_Interim_Presentation.pptx"
    prs.save(out_pptx)
    print(f"Presentation saved successfully: {out_pptx}")

if __name__ == "__main__":
    create_deck()
