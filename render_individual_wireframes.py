import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import os

def draw_window_frame(ax, x, y, w, h, title):
    # Outer Window Box
    window = FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0.02,rounding_size=0.15",
                            fc="#FFFFFF", ec="#94A3B8", lw=1.5, zorder=2)
    ax.add_patch(window)
    
    # Header Title Bar
    title_bar = FancyBboxPatch((x, y - 0.55), w, 0.55, boxstyle="round,pad=0.02,rounding_size=0.15",
                               fc="#F1F5F9", ec="#94A3B8", lw=1.2, zorder=3)
    ax.add_patch(title_bar)
    
    # Window Buttons
    dot_colors = ["#EF4444", "#F59E0B", "#10B981"]
    for i, c in enumerate(dot_colors):
        dot = Circle((x + 0.3 + (i * 0.25), y - 0.28), 0.08, fc=c, ec="none", zorder=4)
        ax.add_patch(dot)
        
    # Window Title
    ax.text(x + w/2, y - 0.28, title, ha='center', va='center', fontsize=11, fontweight='bold', color="#334155", zorder=4)

def draw_box(ax, x, y, w, h, label="", fc="#F8FAFC", ec="#CBD5E1", lw=1.0, zorder=3):
    box = FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0.01,rounding_size=0.06",
                         fc=fc, ec=ec, lw=lw, zorder=zorder)
    ax.add_patch(box)
    if label:
        ax.text(x + w/2, y - h/2, label, ha='center', va='center', fontsize=9, color="#64748B", zorder=zorder+1, multialignment='center')

def draw_img_placeholder(ax, x, y, w, h, label="[ IMAGE PLACEHOLDER ]"):
    box = Rectangle((x, y - h), w, h, fc="#F1F5F9", ec="#94A3B8", lw=1.0, zorder=3)
    ax.add_patch(box)
    ax.plot([x, x + w], [y - h, y], color="#CBD5E1", lw=1.0, zorder=3)
    ax.plot([x, x + w], [y, y - h], color="#CBD5E1", lw=1.0, zorder=3)
    if label:
        ax.text(x + w/2, y - h/2, label, ha='center', va='center', fontsize=8.5, color="#64748B", zorder=4,
                bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#CBD5E1", lw=0.8))

def render_wf01(out_dir):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    
    # Outer Window
    draw_window_frame(ax, 0.4, 7.6, 11.2, 7.2, "WF-01: Public Guest Portal & Multi-Variable Search UI")
    
    # Navbar
    draw_box(ax, 0.6, 6.9, 10.8, 0.65, fc="#0F2C59")
    ax.text(0.9, 6.57, "DUTCH POINT NEGOMBO", fontsize=11, fontweight='bold', color="#D4AF37", zorder=5)
    ax.text(5.5, 6.57, "HOME     ROOMS     OCCUPIED     ABOUT     CONTACT", fontsize=9.5, color="#E2E8F0", zorder=5)
    draw_box(ax, 10.1, 6.75, 1.1, 0.35, label="SIGN IN", fc="#B8860B", ec="none")
    ax.text(10.65, 6.57, "SIGN IN", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#FFFFFF", zorder=6)

    # Search Container
    draw_box(ax, 0.8, 6.1, 10.4, 1.45, fc="#F8FAFC", ec="#0F2C59", lw=1.5)
    ax.text(1.1, 5.8, "Check Rates & Real-Time Availability (Multi-Variable Search Filter)", fontsize=11, fontweight='bold', color="#0F2C59", zorder=5)
    
    # Search Inputs
    draw_box(ax, 1.1, 5.4, 2.2, 0.65, label="Check-In:\n2026-10-10", fc="#FFFFFF", ec="#94A3B8")
    draw_box(ax, 3.5, 5.4, 2.2, 0.65, label="Check-Out:\n2026-10-12", fc="#FFFFFF", ec="#94A3B8")
    draw_box(ax, 5.9, 5.4, 2.2, 0.65, label="Guests:\n2 Adults", fc="#FFFFFF", ec="#94A3B8")
    draw_box(ax, 8.3, 5.4, 2.6, 0.65, fc="#0F2C59", ec="#0F2C59")
    ax.text(9.6, 5.07, "[ CHECK RATES ]", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#FFFFFF", zorder=6)

    # Inventory Cards Title
    ax.text(0.9, 4.45, "Featured Suites & Beachfront Villas (Capacity >= 2 Filtered)", fontsize=11, fontweight='bold', color="#0F2C59", zorder=5)
    
    # 3 Cards
    card_w = 3.3
    rooms = [
        ("Room #101 - Standard Queen", "LKR 28,000 / night", "Max 2 Guests • AC, Free WiFi, City View", "[ AVAILABLE ]", "#10B981", "[ BOOK NOW ]", "#0F2C59"),
        ("Room #201 - Ocean View Suite", "LKR 65,000 / night", "Max 2 Guests • Balcony, Ocean View, King Bed", "[ AVAILABLE ]", "#10B981", "[ BOOK NOW ]", "#0F2C59"),
        ("Room #301 - Family Beach Villa", "LKR 95,000 / night", "Max 4 Guests • Private Pool, Beach Access", "[ OCCUPIED ]", "#EF4444", "[ VIEW OCCUPIED ]", "#EF4444")
    ]
    for idx, (r_name, r_price, r_desc, r_badge, b_col, btn_txt, btn_col) in enumerate(rooms):
        cx = 0.8 + (idx * 3.6)
        cy = 4.2
        draw_box(ax, cx, cy, card_w, 3.4, fc="#FFFFFF", ec="#CBD5E1", lw=1.2)
        draw_img_placeholder(ax, cx+0.15, cy-0.15, card_w-0.3, 1.4, label="Suite Photo")
        # Badge
        draw_box(ax, cx+card_w-1.3, cy-0.25, 1.15, 0.35, fc=b_col, ec="none")
        ax.text(cx+card_w-0.72, cy-0.42, r_badge, ha='center', va='center', fontsize=8, fontweight='bold', color="#FFFFFF", zorder=6)
        # Text
        ax.text(cx+0.2, cy-1.75, r_name, fontsize=9.5, fontweight='bold', color="#0F2C59", zorder=5)
        ax.text(cx+0.2, cy-2.1, r_price, fontsize=10, fontweight='bold', color="#B8860B", zorder=5)
        ax.text(cx+0.2, cy-2.4, r_desc, fontsize=8, color="#64748B", zorder=5)
        # Button
        draw_box(ax, cx+0.2, cy-2.75, card_w-0.4, 0.45, fc=btn_col)
        ax.text(cx+card_w/2, cy-2.97, btn_txt, ha='center', va='center', fontsize=9, fontweight='bold', color="#FFFFFF", zorder=6)

    plt.tight_layout()
    p = os.path.join(out_dir, "wireframe_wf01_home_search.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", p)

def render_wf02(out_dir):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    
    # Outer Window
    draw_window_frame(ax, 0.4, 7.6, 11.2, 7.2, "WF-02: Direct Booking Modal & Concurrency Guard UI")
    
    # Dimmed Backdrop
    draw_box(ax, 0.6, 6.9, 10.8, 6.3, fc="#E2E8F0", ec="#CBD5E1")
    
    # Centered Modal
    mx, my, mw, mh = 1.6, 6.6, 8.8, 5.7
    draw_box(ax, mx, my, mw, mh, fc="#FFFFFF", ec="#0F2C59", lw=2.0)
    
    # Modal Header
    draw_box(ax, mx, my, mw, 0.6, fc="#0F2C59")
    ax.text(mx+0.4, my-0.3, "RESERVE SUITE: Room #201 - Ocean View Suite", fontsize=11, fontweight='bold', color="#FFFFFF", zorder=5)
    ax.text(mx+mw-0.4, my-0.3, "[ X ]", fontsize=11, fontweight='bold', color="#FFFFFF", ha='right', zorder=5)

    # Left Column: Stay & Pricing
    lx, ly, lw, lh = mx+0.4, my-0.8, 3.8, 4.6
    draw_box(ax, lx, ly, lw, lh, fc="#F8FAFC", ec="#CBD5E1")
    ax.text(lx+0.2, ly-0.3, "Reservation Stay Summary", fontsize=10.5, fontweight='bold', color="#0F2C59", zorder=5)
    draw_img_placeholder(ax, lx+0.2, ly-0.5, lw-0.4, 1.2, label="Suite Preview")
    
    stay_details = [
        ("Check-In Date:", "2026-10-10", "#334155"),
        ("Check-Out Date:", "2026-10-12", "#334155"),
        ("Stay Duration:", "2 Nights", "#334155"),
        ("Nightly Rate:", "LKR 65,000", "#B8860B"),
        ("Headcount:", "2 Guests", "#334155"),
        ("Capacity Check:", "PASS (2 <= 2 Max)", "#10B981"),
        ("TOTAL CHARGE:", "LKR 130,000", "#B8860B")
    ]
    for idx, (label, val, col) in enumerate(stay_details):
        sy = ly - 2.0 - (idx * 0.35)
        ax.text(lx+0.25, sy, label, fontsize=9, color="#64748B", zorder=5)
        ax.text(lx+lw-0.25, sy, val, fontsize=9.5, fontweight='bold', color=col, ha='right', zorder=5)

    # Right Column: Guest Input Form
    rx, ry, rw, rh = mx+4.4, my-0.8, 4.0, 4.6
    draw_box(ax, rx, ry, rw, rh, fc="#FFFFFF", ec="#CBD5E1")
    ax.text(rx+0.2, ry-0.3, "Guest Information Form", fontsize=10.5, fontweight='bold', color="#0F2C59", zorder=5)
    
    draw_box(ax, rx+0.2, ry-0.55, rw-0.4, 0.45, label="Full Name: Pasindu Nirmal", fc="#F8FAFC")
    draw_box(ax, rx+0.2, ry-1.15, rw-0.4, 0.45, label="Email Address: pasindu@demo.com", fc="#F8FAFC")
    draw_box(ax, rx+0.2, ry-1.75, rw-0.4, 0.45, label="Contact Phone: +94 77 812 2419", fc="#F8FAFC")
    draw_box(ax, rx+0.2, ry-2.35, rw-0.4, 0.65, label="Special Requests: Late check-in requested", fc="#F8FAFC")

    # Double Booking Warning Banner
    draw_box(ax, rx+0.2, ry-3.2, rw-0.4, 0.55, fc="#FEF2F2", ec="#EF4444", lw=1.2)
    ax.text(rx+rw/2, ry-3.47, "[CONCURRENCY GUARD]: Real-time overlap validation active", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#B91C1C", zorder=5)

    # Modal Actions
    draw_box(ax, rx+0.2, ry-3.95, 1.6, 0.5, label="[ CANCEL ]", fc="#E2E8F0", ec="#94A3B8")
    draw_box(ax, rx+2.0, ry-3.95, 1.8, 0.5, fc="#0F2C59")
    ax.text(rx+2.9, ry-4.2, "[ CONFIRM BOOKING ]", ha='center', va='center', fontsize=9, fontweight='bold', color="#FFFFFF", zorder=6)

    plt.tight_layout()
    p = os.path.join(out_dir, "wireframe_wf02_booking_modal.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", p)

def render_wf03(out_dir):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    
    # Outer Window
    draw_window_frame(ax, 0.4, 7.6, 11.2, 7.2, "WF-03: Front-Desk Occupancy Tracker (Daily Date & Active Roster)")
    
    # Tracker Header
    draw_box(ax, 0.6, 6.9, 10.8, 0.95, fc="#F8FAFC", ec="#CBD5E1")
    ax.text(0.9, 6.55, "Front-Desk Occupied Rooms Tracker", fontsize=12, fontweight='bold', color="#0F2C59", zorder=5)
    ax.text(0.9, 6.25, "Real-time room occupancy and guest reservation records for Dutch Point Negombo", fontsize=9, color="#64748B", zorder=5)
    
    # Mode Switcher
    draw_box(ax, 7.8, 6.75, 1.8, 0.45, label="● Filter by Date", fc="#0F2C59")
    ax.text(8.7, 6.52, "● Filter by Date", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#FFFFFF", zorder=6)
    draw_box(ax, 9.7, 6.75, 1.5, 0.45, label="All Active (4)", fc="#E2E8F0")

    # Filter Toolbar
    draw_box(ax, 0.6, 5.8, 10.8, 0.7, fc="#FFFFFF", ec="#0F2C59", lw=1.2)
    ax.text(0.9, 5.45, "Target Date: [ 2026-10-10 ]", fontsize=10, fontweight='bold', color="#0F2C59", zorder=5)
    draw_box(ax, 4.0, 5.7, 3.2, 0.5, label="[ Sync Search: 2026-10-10 to 12 ]", fc="#E0F2FE", ec="#0284C7")
    draw_box(ax, 7.4, 5.7, 1.3, 0.5, label="[ Today ]", fc="#F1F5F9", ec="#94A3B8")
    ax.text(11.1, 5.45, "Status: 1 Occupied Suite", ha='right', fontsize=10, fontweight='bold', color="#B91C1C", zorder=5)

    # 2 Big Occupancy Cards
    cw = 5.2
    # Card 1: Occupied Room
    c1x, c1y = 0.6, 4.9
    draw_box(ax, c1x, c1y, cw, 4.2, fc="#FFFFFF", ec="#EF4444", lw=1.5)
    draw_box(ax, c1x+cw-1.6, c1y-0.2, 1.4, 0.4, label="[ OCCUPIED ]", fc="#EF4444")
    ax.text(c1x+cw-0.9, c1y-0.4, "[ OCCUPIED ]", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#FFFFFF", zorder=6)
    draw_img_placeholder(ax, c1x+0.3, c1y-0.2, 1.6, 1.2, label="Room #201")
    ax.text(c1x+2.1, c1y-0.4, "Room #201 - Ocean View Suite", fontsize=10.5, fontweight='bold', color="#0F2C59", zorder=5)
    ax.text(c1x+2.1, c1y-0.75, "Reservation ID: #RES-7", fontsize=9, color="#64748B", zorder=5)
    ax.text(c1x+2.1, c1y-1.1, "Primary Guest: Pasindu Nirmal", fontsize=9.5, fontweight='bold', color="#334155", zorder=5)
    
    occ_info = [
        ("Phone Number:", "+94 77 812 2419"),
        ("Email Address:", "pnidd2002@gmail.com"),
        ("Stay Period:", "2026-10-10 to 2026-10-12 (2 Nights)"),
        ("Guest Count:", "2 Guests (Room Max: 2)"),
        ("Total Billing:", "LKR 130,000 (Payment Confirmed)"),
        ("Special Requests:", "Admin demo booking - Late check-in")
    ]
    for idx, (label, val) in enumerate(occ_info):
        oy = c1y - 1.6 - (idx * 0.38)
        ax.text(c1x+0.3, oy, label, fontsize=8.5, color="#64748B", zorder=5)
        ax.text(c1x+1.8, oy, val, fontsize=8.8, fontweight='bold', color="#0F2C59" if "LKR" in val else "#334155", zorder=5)

    # Card 2: Vacant / Available Room
    c2x, c2y = 6.2, 4.9
    draw_box(ax, c2x, c2y, cw, 4.2, fc="#F8FAFC", ec="#10B981", lw=1.5)
    draw_box(ax, c2x+cw-1.6, c2y-0.2, 1.4, 0.4, label="[ AVAILABLE ]", fc="#10B981")
    ax.text(c2x+cw-0.9, c2y-0.4, "[ AVAILABLE ]", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#FFFFFF", zorder=6)
    draw_img_placeholder(ax, c2x+0.3, c2y-0.2, 1.6, 1.2, label="Room #101")
    ax.text(c2x+2.1, c2y-0.4, "Room #101 - Standard Queen", fontsize=10.5, fontweight='bold', color="#0F2C59", zorder=5)
    ax.text(c2x+2.1, c2y-0.75, "Status: Ready for Check-In", fontsize=9, color="#10B981", fontweight='bold', zorder=5)
    ax.text(c2x+2.1, c2y-1.1, "Nightly Rate: LKR 28,000 / night", fontsize=9.5, fontweight='bold', color="#B8860B", zorder=5)

    vac_info = [
        "• No active or overlapping reservations for selected target date.",
        "• Housekeeping Inspection: Completed & Sanitized (10:30 AM).",
        "• Keycard Access: Initialized at Front Desk Terminal.",
        "• Ready for immediate walk-in guest check-in."
    ]
    for idx, v in enumerate(vac_info):
        ax.text(c2x+0.3, c2y - 1.7 - (idx * 0.42), v, fontsize=8.5, color="#475569", zorder=5)
        
    draw_box(ax, c2x+0.3, c2y-3.5, cw-0.6, 0.5, label="[ + Create Walk-In Reservation ]", fc="#0F2C59")
    ax.text(c2x+cw/2, c2y-3.75, "[ + Create Walk-In Reservation ]", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#FFFFFF", zorder=6)

    plt.tight_layout()
    p = os.path.join(out_dir, "wireframe_wf03_occupancy_tracker.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", p)

def render_wf04(out_dir):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    
    # Outer Window
    draw_window_frame(ax, 0.4, 7.6, 11.2, 7.2, "WF-04: Admin Operational Dashboard (KPIs, Inventory & Roster)")
    
    # Admin Header
    draw_box(ax, 0.6, 6.9, 10.8, 0.65, fc="#0F2C59")
    ax.text(0.9, 6.57, "ADMIN PORTAL: Pasindu (System Administrator)", fontsize=11, fontweight='bold', color="#D4AF37", zorder=5)
    ax.text(11.1, 6.57, "[ + ADD ROOM ]    [ REVENUE REPORT ]    [ LOGOUT ]", fontsize=8.5, color="#E2E8F0", ha='right', zorder=5)

    # 3 KPI Cards
    kw = 3.4
    kpis = [
        ("TOTAL REVENUE (LKR)", "LKR 1,250,000", "+14.2% vs previous period", "#10B981"),
        ("OCCUPANCY RATE", "78% Occupied", "14 of 18 Rooms Booked", "#D97706"),
        ("ACTIVE GUESTS", "24 In-House", "Current confirmed reservations", "#2563EB")
    ]
    for idx, (kt, kv, ks, kc) in enumerate(kpis):
        kx = 0.6 + (idx * 3.7)
        ky = 6.1
        draw_box(ax, kx, ky, kw, 1.25, fc="#F8FAFC", ec="#CBD5E1")
        ax.text(kx+0.25, ky-0.3, kt, fontsize=8.5, fontweight='bold', color="#64748B", zorder=5)
        ax.text(kx+0.25, ky-0.72, kv, fontsize=13, fontweight='bold', color=kc, zorder=5)
        ax.text(kx+0.25, ky-1.05, ks, fontsize=8, color="#94A3B8", zorder=5)

    # Table Title
    ax.text(0.6, 4.65, "Active Reservation Transactions & Guest Manifest Roster", fontsize=11, fontweight='bold', color="#0F2C59", zorder=5)
    
    # Data Table Container
    ty = 4.4
    th_w = 10.8
    th_h = 3.8
    draw_box(ax, 0.6, ty, th_w, th_h, fc="#FFFFFF", ec="#CBD5E1")
    
    # Table Header Row
    draw_box(ax, 0.6, ty, th_w, 0.45, fc="#F1F5F9", ec="#CBD5E1")
    cols_x = [0.8, 2.0, 3.8, 5.8, 7.5, 9.0, 10.2]
    headers = ["RES ID", "GUEST NAME", "ASSIGNED SUITE", "DATES", "TOTAL AMOUNT", "STATUS", "ACTIONS"]
    for cx, th in zip(cols_x, headers):
        ax.text(cx, ty-0.28, th, fontsize=8.5, fontweight='bold', color="#0F2C59", zorder=5)

    # Rows
    rows = [
        ("#RES-7", "Pasindu Nirmal", "Ocean View #201", "10/10 - 10/12", "LKR 130,000", "Confirmed", "[Cancel]"),
        ("#RES-6", "Kasun Silva", "Deluxe Double #102", "10/10 - 10/15", "LKR 210,000", "Cancelled", "[Restore]"),
        ("#RES-5", "John Doe", "Standard Queen #101", "10/10 - 10/15", "LKR 140,000", "Confirmed", "[Details]"),
        ("#RES-4", "Sarah Smith", "Family Villa #301", "10/12 - 10/16", "LKR 380,000", "Confirmed", "[Details]"),
        ("#RES-3", "David Miller", "Ocean View #202", "10/15 - 10/18", "LKR 195,000", "Confirmed", "[Details]"),
        ("#RES-2", "Emma Watson", "Presidential #401", "10/20 - 10/25", "LKR 700,000", "Confirmed", "[Details]"),
        ("#RES-1", "Robert Brown", "Standard Queen #103", "10/01 - 10/05", "LKR 112,000", "Checked Out", "[Archive]")
    ]
    for r_idx, r_data in enumerate(rows):
        ry = ty - 0.5 - (r_idx * 0.44)
        if r_idx % 2 == 1:
            draw_box(ax, 0.6, ry+0.05, th_w, 0.42, fc="#F8FAFC", ec="none")
        for cx, val in zip(cols_x, r_data):
            col = "#10B981" if val == "Confirmed" else ("#EF4444" if val == "Cancelled" else ("#B8860B" if "LKR" in val else "#334155"))
            bld = 'bold' if (val == "Confirmed" or "LKR" in val) else 'normal'
            ax.text(cx, ry-0.2, val, fontsize=8.5, color=col, fontweight=bld, zorder=5)

    plt.tight_layout()
    p = os.path.join(out_dir, "wireframe_wf04_admin_dashboard.png")
    plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", p)

if __name__ == "__main__":
    out_dir = r"C:\Users\PASINDU\Desktop\Interim"
    render_wf01(out_dir)
    render_wf02(out_dir)
    render_wf03(out_dir)
    render_wf04(out_dir)
