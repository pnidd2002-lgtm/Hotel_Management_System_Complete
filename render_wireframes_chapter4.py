import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

def draw_window_frame(ax, x, y, w, h, title):
    # Outer Window Box
    window = FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                            fc="#FFFFFF", ec="#94A3B8", lw=1.5, zorder=2)
    ax.add_patch(window)
    
    # Header Title Bar
    title_bar = FancyBboxPatch((x, y - 0.45), w, 0.45, boxstyle="round,pad=0.02,rounding_size=0.1",
                               fc="#F1F5F9", ec="#94A3B8", lw=1.2, zorder=3)
    ax.add_patch(title_bar)
    
    # Window Buttons (Red, Yellow, Green dots)
    dot_colors = ["#EF4444", "#F59E0B", "#10B981"]
    for i, c in enumerate(dot_colors):
        dot = Circle((x + 0.2 + (i * 0.18), y - 0.22), 0.05, fc=c, ec="none", zorder=4)
        ax.add_patch(dot)
        
    # Window Title
    ax.text(x + w/2, y - 0.22, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#475569", zorder=4)

def draw_wireframe_box(ax, x, y, w, h, label="", fc="#F8FAFC", ec="#CBD5E1", lw=1.0):
    box = FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0.01,rounding_size=0.04",
                         fc=fc, ec=ec, lw=lw, zorder=3)
    ax.add_patch(box)
    if label:
        ax.text(x + w/2, y - h/2, label, ha='center', va='center', fontsize=7.5, color="#64748B", zorder=4, multialignment='center')

def draw_img_placeholder(ax, x, y, w, h, label="[ IMAGE PLACEHOLDER ]"):
    box = Rectangle((x, y - h), w, h, fc="#F1F5F9", ec="#94A3B8", lw=1.0, zorder=3)
    ax.add_patch(box)
    # Cross lines (X)
    ax.plot([x, x + w], [y - h, y], color="#CBD5E1", lw=1.0, zorder=3)
    ax.plot([x, x + w], [y, y - h], color="#CBD5E1", lw=1.0, zorder=3)
    if label:
        ax.text(x + w/2, y - h/2, label, ha='center', va='center', fontsize=7.0, color="#64748B", zorder=4,
                bbox=dict(boxstyle="round,pad=0.15", fc="#FFFFFF", ec="#CBD5E1", lw=0.8))

def generate_wireframe_sheet():
    fig, ax = plt.subplots(figsize=(18, 12.5), dpi=300)
    ax.set_xlim(-0.5, 18.5)
    ax.set_ylim(-0.5, 13.0)
    ax.axis('off')
    
    fig.patch.set_facecolor('#F8FAFC')
    
    # Outer Border
    canvas = FancyBboxPatch((0.2, 0.2), 18.1, 12.6, boxstyle="round,pad=0.1,rounding_size=0.15",
                            fc="#FFFFFF", ec="#CBD5E1", lw=1.8, zorder=0)
    ax.add_patch(canvas)

    # Super Title Header
    ax.text(9.25, 12.4, "CHAPTER 04: LOW-FIDELITY WIREFRAME & UI DESIGN SPECIFICATION", ha='center', va='center',
            fontsize=18, fontweight='bold', color='#0F2C59', zorder=10)
    ax.text(9.25, 12.0, "Dutch Point Negombo Web-Based Hotel Management System • Interface Blueprints",
            ha='center', va='center', fontsize=11, fontweight='bold', color='#B8860B', zorder=10)

    # Layout: 2x2 Grid of Wireframes
    # W = 8.5, H = 5.2 each
    p1 = (0.7, 11.5)  # Panel 1: Top Left
    p2 = (9.6, 11.5)  # Panel 2: Top Right
    p3 = (0.7, 5.9)   # Panel 3: Bottom Left
    p4 = (9.6, 5.9)   # Panel 4: Bottom Right
    pw, ph = 8.3, 5.3

    # =========================================================================
    # PANEL 1: HOME & MULTI-VARIABLE SEARCH (WF-01)
    # =========================================================================
    draw_window_frame(ax, p1[0], p1[1], pw, ph, "WF-01: Home Portal & Multi-Variable Search (http://localhost:5173/)")
    
    # Navbar
    draw_wireframe_box(ax, p1[0]+0.2, p1[1]-0.55, pw-0.4, 0.45, fc="#0F2C59")
    ax.text(p1[0]+0.4, p1[1]-0.78, "DUTCH POINT NEGOMBO", fontsize=8.5, fontweight='bold', color="#D4AF37", zorder=5)
    ax.text(p1[0]+4.0, p1[1]-0.78, "HOME     ROOMS     OCCUPIED     ABOUT     CONTACT", fontsize=7.0, color="#E2E8F0", zorder=5)
    ax.text(p1[0]+pw-0.5, p1[1]-0.78, "[ SIGN IN ]", fontsize=7.5, fontweight='bold', color="#FFFFFF", ha='right', zorder=5)

    # Search Bar Container
    draw_wireframe_box(ax, p1[0]+0.3, p1[1]-1.15, pw-0.6, 1.05, fc="#F8FAFC", ec="#0F2C59", lw=1.2)
    ax.text(p1[0]+0.5, p1[1]-1.35, "Check Rates & Real-Time Availability", fontsize=8.5, fontweight='bold', color="#0F2C59", zorder=5)
    
    # Inputs: Check-In, Check-Out, Guests, Button
    draw_wireframe_box(ax, p1[0]+0.5, p1[1]-1.55, 1.6, 0.50, label="Check-In:\n2026-10-10", fc="#FFFFFF", ec="#94A3B8")
    draw_wireframe_box(ax, p1[0]+2.3, p1[1]-1.55, 1.6, 0.50, label="Check-Out:\n2026-10-12", fc="#FFFFFF", ec="#94A3B8")
    draw_wireframe_box(ax, p1[0]+4.1, p1[1]-1.55, 1.6, 0.50, label="Guest Count:\n2 Guests", fc="#FFFFFF", ec="#94A3B8")
    draw_wireframe_box(ax, p1[0]+5.9, p1[1]-1.55, 1.8, 0.50, label="[ CHECK RATES ]", fc="#0F2C59", ec="#0F2C59")
    ax.text(p1[0]+6.8, p1[1]-1.80, "[ CHECK RATES ]", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#FFFFFF", zorder=6)

    # Room Cards Grid (3 Cards)
    ax.text(p1[0]+0.4, p1[1]-2.35, "Luxury Suites & Beachfront Villas (Filtered: Capacity >= 2)", fontsize=8.0, fontweight='bold', color="#0F2C59", zorder=5)
    card_w = 2.45
    rooms_data = [
        ("Room #101 - Standard Queen", "LKR 28,000 / night", "Max 2 Guests • AC, WiFi", "[ AVAILABLE ]", "#10B981"),
        ("Room #201 - Ocean View Suite", "LKR 65,000 / night", "Max 2 Guests • Balcony, View", "[ AVAILABLE ]", "#10B981"),
        ("Room #301 - Family Beach Villa", "LKR 95,000 / night", "Max 4 Guests • Kitchen, Pool", "[ OCCUPIED ]", "#EF4444")
    ]
    for idx, (r_name, r_price, r_desc, r_badge, b_col) in enumerate(rooms_data):
        rx = p1[0] + 0.3 + (idx * 2.65)
        ry = p1[1] - 2.5
        draw_wireframe_box(ax, rx, ry, card_w, 2.55, fc="#FFFFFF", ec="#CBD5E1", lw=1.0)
        draw_img_placeholder(ax, rx+0.1, ry-0.1, card_w-0.2, 1.05)
        # Badge
        draw_wireframe_box(ax, rx+card_w-1.1, ry-0.2, 0.95, 0.28, label=r_badge, fc=b_col, ec="none")
        ax.text(rx+card_w-0.62, ry-0.34, r_badge, ha='center', va='center', fontsize=6.5, fontweight='bold', color="#FFFFFF", zorder=6)
        # Text
        ax.text(rx+0.15, ry-1.30, r_name, fontsize=7.5, fontweight='bold', color="#0F2C59", zorder=5)
        ax.text(rx+0.15, ry-1.55, r_price, fontsize=7.5, fontweight='bold', color="#B8860B", zorder=5)
        ax.text(rx+0.15, ry-1.80, r_desc, fontsize=6.5, color="#64748B", zorder=5)
        # Button
        b_txt = "[ BOOK NOW ]" if "AVAILABLE" in r_badge else "[ VIEW OCCUPIED ]"
        b_bg = "#0F2C59" if "AVAILABLE" in r_badge else "#EF4444"
        draw_wireframe_box(ax, rx+0.15, ry-2.05, card_w-0.3, 0.38, fc=b_bg)
        ax.text(rx+card_w/2, ry-2.24, b_txt, ha='center', va='center', fontsize=7.0, fontweight='bold', color="#FFFFFF", zorder=6)

    # =========================================================================
    # PANEL 2: BOOKING MODAL & CONCURRENCY (WF-02)
    # =========================================================================
    draw_window_frame(ax, p2[0], p2[1], pw, ph, "WF-02: Booking Reservation Modal & Concurrency Guard")
    
    # Dimmed background representation
    draw_wireframe_box(ax, p2[0]+0.2, p2[1]-0.55, pw-0.4, ph-0.65, fc="#E2E8F0", ec="#CBD5E1")
    
    # Centered Modal Box
    m_x, m_y, m_w, m_h = p2[0]+0.8, p2[1]-0.7, pw-1.6, 4.35
    draw_wireframe_box(ax, m_x, m_y, m_w, m_h, fc="#FFFFFF", ec="#0F2C59", lw=1.8)
    
    # Modal Header
    draw_wireframe_box(ax, m_x, m_y, m_w, 0.45, fc="#0F2C59")
    ax.text(m_x+0.3, m_y-0.22, "RESERVE SUITE: Room #201 - Ocean View Suite", fontsize=8.0, fontweight='bold', color="#FFFFFF", zorder=5)
    ax.text(m_x+m_w-0.3, m_y-0.22, "[ X ]", fontsize=8.0, fontweight='bold', color="#FFFFFF", ha='right', zorder=5)

    # Left: Stay & Cost Summary
    draw_wireframe_box(ax, m_x+0.3, m_y-0.6, 2.7, 3.45, fc="#F8FAFC", ec="#CBD5E1")
    ax.text(m_x+0.45, m_y-0.85, "Stay Summary & Rates", fontsize=8.0, fontweight='bold', color="#0F2C59", zorder=5)
    draw_img_placeholder(ax, m_x+0.45, m_y-1.0, 2.4, 0.9, label="Suite Preview")
    stay_info = [
        "Check-In: 2026-10-10",
        "Check-Out: 2026-10-12",
        "Duration: 2 Nights",
        "Rate: LKR 65,000 / Night",
        "Headcount: 2 Guests",
        "Capacity Check: PASS (2 <= 2)",
        "TOTAL: LKR 130,000"
    ]
    for idx, s in enumerate(stay_info):
        is_total = "TOTAL" in s
        col = "#B8860B" if is_total else ("#10B981" if "PASS" in s else "#334155")
        sz = 8.0 if is_total else 7.0
        ax.text(m_x+0.45, m_y-2.05-(idx*0.25), s, fontsize=sz, fontweight='bold' if is_total else 'normal', color=col, zorder=5)

    # Right: Guest Details & Double Booking Warning
    draw_wireframe_box(ax, m_x+3.2, m_y-0.6, 3.1, 3.45, fc="#FFFFFF", ec="#CBD5E1")
    ax.text(m_x+3.35, m_y-0.85, "Guest Information & Submission", fontsize=8.0, fontweight='bold', color="#0F2C59", zorder=5)
    
    # Form fields
    draw_wireframe_box(ax, m_x+3.35, m_y-1.05, 2.8, 0.38, label="Full Name: Pasindu Nirmal", fc="#F8FAFC")
    draw_wireframe_box(ax, m_x+3.35, m_y-1.50, 2.8, 0.38, label="Email: pasindu@demo.com", fc="#F8FAFC")
    draw_wireframe_box(ax, m_x+3.35, m_y-1.95, 2.8, 0.38, label="Phone: +94 77 123 4567", fc="#F8FAFC")
    draw_wireframe_box(ax, m_x+3.35, m_y-2.40, 2.8, 0.50, label="Special Requests: Late check-in", fc="#F8FAFC")

    # Double Booking Warning Banner
    draw_wireframe_box(ax, m_x+3.35, m_y-3.00, 2.8, 0.40, fc="#FEF2F2", ec="#EF4444")
    ax.text(m_x+4.75, m_y-3.20, "✔ Concurrency Guard: Real-time overlap check active", ha='center', va='center', fontsize=6.5, color="#B91C1C", zorder=5)

    # Modal Buttons
    draw_wireframe_box(ax, m_x+3.35, m_y-3.50, 1.2, 0.40, label="[ CANCEL ]", fc="#E2E8F0", ec="#94A3B8")
    draw_wireframe_box(ax, m_x+4.75, m_y-3.50, 1.4, 0.40, label="[ CONFIRM BOOKING ]", fc="#0F2C59")
    ax.text(m_x+5.45, m_y-3.70, "[ CONFIRM ]", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#FFFFFF", zorder=6)

    # =========================================================================
    # PANEL 3: FRONT-DESK OCCUPANCY TRACKER (WF-03)
    # =========================================================================
    draw_window_frame(ax, p3[0], p3[1], pw, ph, "WF-03: Front-Desk Occupancy Tracker (Single Date & Active Roster)")

    # Tracker Header & Mode Switcher
    draw_wireframe_box(ax, p3[0]+0.3, p3[1]-0.55, pw-0.6, 0.85, fc="#F8FAFC", ec="#CBD5E1")
    ax.text(p3[0]+0.5, p3[1]-0.75, "Front-Desk Occupied Rooms Tracker", fontsize=8.5, fontweight='bold', color="#0F2C59", zorder=5)
    ax.text(p3[0]+0.5, p3[1]-0.95, "Real-time room occupancy and guest reservation records for Dutch Point Negombo", fontsize=6.5, color="#64748B", zorder=5)
    
    # Toggle Buttons (Filter by Date vs All Active Bookings)
    draw_wireframe_box(ax, p3[0]+pw-3.6, p3[1]-0.65, 1.4, 0.32, label="● Filter by Date", fc="#0F2C59")
    ax.text(p3[0]+pw-2.9, p3[1]-0.81, "● Filter by Date", ha='center', va='center', fontsize=6.5, fontweight='bold', color="#FFFFFF", zorder=6)
    draw_wireframe_box(ax, p3[0]+pw-2.1, p3[1]-0.65, 1.7, 0.32, label="All Active Bookings (4)", fc="#E2E8F0")

    # Filter Toolbar
    draw_wireframe_box(ax, p3[0]+0.3, p3[1]-1.50, pw-0.6, 0.55, fc="#FFFFFF", ec="#0F2C59")
    ax.text(p3[0]+0.5, p3[1]-1.78, "Target Date: [ 2026-10-10 ]", fontsize=7.5, fontweight='bold', color="#0F2C59", zorder=5)
    draw_wireframe_box(ax, p3[0]+2.7, p3[1]-1.58, 2.4, 0.38, label="[ Sync Search: 2026-10-10 to 12 ]", fc="#E0F2FE", ec="#0284C7")
    draw_wireframe_box(ax, p3[0]+5.2, p3[1]-1.58, 1.1, 0.38, label="[ Today ]", fc="#F1F5F9", ec="#94A3B8")
    ax.text(p3[0]+pw-0.5, p3[1]-1.78, "Status: 1 Occupied Suite", ha='right', fontsize=7.5, fontweight='bold', color="#B91C1C", zorder=5)

    # Occupied Room Cards (2 Cards)
    occ_w = 3.7
    # Card 1: Occupied Suite
    draw_wireframe_box(ax, p3[0]+0.3, p3[1]-2.2, occ_w, 2.7, fc="#FFFFFF", ec="#EF4444", lw=1.2)
    draw_wireframe_box(ax, p3[0]+occ_w-1.1, p3[1]-2.3, 1.2, 0.28, label="[ OCCUPIED ]", fc="#EF4444")
    ax.text(p3[0]+occ_w-0.5, p3[1]-2.44, "[ OCCUPIED ]", ha='center', va='center', fontsize=6.5, fontweight='bold', color="#FFFFFF", zorder=6)
    draw_img_placeholder(ax, p3[0]+0.45, p3[1]-2.3, 1.2, 0.9, label="Room #201")
    ax.text(p3[0]+1.8, p3[1]-2.45, "Room #201 - Ocean View Suite", fontsize=7.5, fontweight='bold', color="#0F2C59", zorder=5)
    ax.text(p3[0]+1.8, p3[1]-2.70, "Reservation ID: #RES-7", fontsize=7.0, color="#64748B", zorder=5)
    ax.text(p3[0]+1.8, p3[1]-2.95, "Guest: Pasindu Nirmal", fontsize=7.0, fontweight='bold', color="#334155", zorder=5)
    
    occ_details1 = [
        "Phone: +94 77 812 2419  |  Email: pnidd2002@gmail.com",
        "Check-In: 2026-10-10   |   Check-Out: 2026-10-12",
        "Guests: 2 Guests       |   Paid Total: LKR 130,000",
        "Status: Confirmed      |   Notes: Admin demo booking"
    ]
    for idx, d in enumerate(occ_details1):
        ax.text(p3[0]+0.45, p3[1]-3.35-(idx*0.28), d, fontsize=6.8, color="#334155", zorder=5)

    # Card 2: Vacant Suite Example
    draw_wireframe_box(ax, p3[0]+4.3, p3[1]-2.2, occ_w, 2.7, fc="#F8FAFC", ec="#10B981", lw=1.2)
    draw_wireframe_box(ax, p3[0]+occ_w+2.9, p3[1]-2.3, 1.2, 0.28, label="[ AVAILABLE ]", fc="#10B981")
    ax.text(p3[0]+occ_w+3.5, p3[1]-2.44, "[ AVAILABLE ]", ha='center', va='center', fontsize=6.5, fontweight='bold', color="#FFFFFF", zorder=6)
    draw_img_placeholder(ax, p3[0]+4.45, p3[1]-2.3, 1.2, 0.9, label="Room #101")
    ax.text(p3[0]+5.8, p3[1]-2.45, "Room #101 - Standard Queen", fontsize=7.5, fontweight='bold', color="#0F2C59", zorder=5)
    ax.text(p3[0]+5.8, p3[1]-2.70, "Status: Ready for Check-In", fontsize=7.0, color="#10B981", zorder=5)
    ax.text(p3[0]+5.8, p3[1]-2.95, "Rate: LKR 28,000 / night", fontsize=7.0, color="#B8860B", zorder=5)
    ax.text(p3[0]+4.45, p3[1]-3.45, "• No overlapping reservations found for 2026-10-10.", fontsize=6.8, color="#475569", zorder=5)
    ax.text(p3[0]+4.45, p3[1]-3.75, "• Housekeeping status: Clean & Inspected.", fontsize=6.8, color="#475569", zorder=5)
    draw_wireframe_box(ax, p3[0]+4.45, p3[1]-4.3, occ_w-0.3, 0.35, label="[ Create Walk-In Reservation ]", fc="#0F2C59")
    ax.text(p3[0]+6.15, p3[1]-4.47, "[ Create Walk-In Reservation ]", ha='center', va='center', fontsize=7.0, fontweight='bold', color="#FFFFFF", zorder=6)

    # =========================================================================
    # PANEL 4: ADMIN OPERATIONAL DASHBOARD (WF-04)
    # =========================================================================
    draw_window_frame(ax, p4[0], p4[1], pw, ph, "WF-04: Admin Operational Dashboard (KPIs, Inventory & Roster)")

    # Admin Header Bar
    draw_wireframe_box(ax, p4[0]+0.2, p4[1]-0.55, pw-0.4, 0.45, fc="#0F2C59")
    ax.text(p4[0]+0.4, p4[1]-0.78, "ADMIN PORTAL: Pasindu (System Admin)", fontsize=8.0, fontweight='bold', color="#D4AF37", zorder=5)
    ax.text(p4[0]+pw-0.5, p4[1]-0.78, "[ ADD ROOM ]   [ REVENUE REPORT ]   [ LOGOUT ]", fontsize=7.0, color="#E2E8F0", ha='right', zorder=5)

    # KPI Metric Cards (3 Cards)
    kpis = [
        ("TOTAL REVENUE (LKR)", "LKR 1,250,000", "+14% vs last week", "#10B981"),
        ("OCCUPIED ROOMS", "78% Occupancy", "14 of 18 Rooms Booked", "#D97706"),
        ("TOTAL ACTIVE GUESTS", "24 Guests", "Check-in peak active", "#2563EB")
    ]
    kw = 2.45
    for idx, (k_title, k_val, k_sub, k_col) in enumerate(kpis):
        kx = p4[0] + 0.3 + (idx * 2.65)
        ky = p4[1] - 1.15
        draw_wireframe_box(ax, kx, ky, kw, 0.95, fc="#F8FAFC", ec="#CBD5E1")
        ax.text(kx+0.15, ky-0.22, k_title, fontsize=6.5, fontweight='bold', color="#64748B", zorder=5)
        ax.text(kx+0.15, ky-0.55, k_val, fontsize=10.0, fontweight='bold', color=k_col, zorder=5)
        ax.text(kx+0.15, ky-0.80, k_sub, fontsize=6.2, color="#94A3B8", zorder=5)

    # Reservation Table (Mini Data Grid)
    ax.text(p4[0]+0.4, p4[1]-2.30, "Recent Reservation Transactions & Active Roster", fontsize=8.0, fontweight='bold', color="#0F2C59", zorder=5)
    t_y = p4[1] - 2.5
    draw_wireframe_box(ax, p4[0]+0.3, t_y, pw-0.6, 2.55, fc="#FFFFFF", ec="#CBD5E1")
    
    # Table Header Row
    draw_wireframe_box(ax, p4[0]+0.3, t_y, pw-0.6, 0.35, fc="#F1F5F9", ec="#CBD5E1")
    cols_x = [p4[0]+0.4, p4[0]+1.3, p4[0]+2.6, p4[0]+4.1, p4[0]+5.4, p4[0]+6.5, p4[0]+7.3]
    headers_t = ["ID", "Guest", "Suite", "Dates", "Total LKR", "Status", "Actions"]
    for cx, th in zip(cols_x, headers_t):
        ax.text(cx, t_y-0.22, th, fontsize=6.8, fontweight='bold', color="#0F2C59", zorder=5)

    # Table Data Rows
    t_rows = [
        ("#RES-7", "Pasindu Nirmal", "Ocean View #201", "10/10 - 10/12", "LKR 130,000", "Confirmed", "[Cancel]"),
        ("#RES-6", "Kasun Silva", "Deluxe Double #102", "10/10 - 10/15", "LKR 210,000", "Cancelled", "[Restore]"),
        ("#RES-5", "John Doe", "Standard Queen #101", "10/10 - 10/15", "LKR 140,000", "Confirmed", "[Details]"),
        ("#RES-4", "Sarah Smith", "Family Villa #301", "10/12 - 10/16", "LKR 380,000", "Confirmed", "[Details]"),
        ("#RES-3", "David Miller", "Ocean View #202", "10/15 - 10/18", "LKR 195,000", "Confirmed", "[Details]"),
        ("#RES-2", "Emma Watson", "Presidential #401", "10/20 - 10/25", "LKR 700,000", "Confirmed", "[Details]")
    ]
    for r_idx, r_data in enumerate(t_rows):
        ry = t_y - 0.40 - (r_idx * 0.35)
        # zebra striping
        if r_idx % 2 == 1:
            draw_wireframe_box(ax, p4[0]+0.3, ry+0.05, pw-0.6, 0.32, fc="#F8FAFC", ec="none")
        for cx, val in zip(cols_x, r_data):
            c_color = "#10B981" if val == "Confirmed" else ("#EF4444" if val == "Cancelled" else ("#B8860B" if "LKR" in val else "#334155"))
            bld = "fontweight='bold'" if (val == "Confirmed" or "LKR" in val) else ""
            ax.text(cx, ry-0.12, val, fontsize=6.5, color=c_color, zorder=5)

    plt.tight_layout()
    
    # Save High-Res Wireframe Sheet
    out_png = r"C:\Users\PASINDU\Desktop\Interim\hotel_wireframes_chapter4_hd.png"
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Wireframe sheet saved successfully: {out_png}")

if __name__ == "__main__":
    generate_wireframe_sheet()
