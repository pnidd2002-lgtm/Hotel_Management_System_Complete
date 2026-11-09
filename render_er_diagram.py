import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle

def draw_table(ax, x, y, width, title, columns, header_bg="#0F2C59", title_color="#FFFFFF"):
    """
    Renders an enterprise relational database entity table with styled header,
    PK/FK badges, column names, types, and constraints.
    """
    row_height = 0.38
    header_height = 0.65
    total_height = header_height + (len(columns) * row_height) + 0.15
    top_y = y
    bottom_y = y - total_height
    
    # Outer Table Box (Shadow effect + Main Box)
    shadow = FancyBboxPatch((x + 0.08, bottom_y - 0.08), width, total_height,
                            boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc="#E2E8F0", ec="none", zorder=1)
    ax.add_patch(shadow)
    
    outer_box = FancyBboxPatch((x, bottom_y), width, total_height,
                               boxstyle="round,pad=0.02,rounding_size=0.12",
                               fc="#FFFFFF", ec="#CBD5E1", lw=1.5, zorder=2)
    ax.add_patch(outer_box)
    
    # Header Banner Box
    hdr_box = FancyBboxPatch((x, top_y - header_height), width, header_height,
                             boxstyle="round,pad=0.02,rounding_size=0.12",
                             fc=header_bg, ec="none", zorder=3)
    ax.add_patch(hdr_box)
    
    # Header Title
    ax.text(x + width/2, top_y - header_height/2, title, ha='center', va='center',
            fontsize=12, fontweight='bold', color=title_color, zorder=4)
    
    # Column Rows
    curr_y = top_y - header_height - 0.22
    for idx, (key_type, col_name, data_type, constraint) in enumerate(columns):
        # Alternating subtle row background
        if idx % 2 == 1:
            row_bg = Rectangle((x + 0.05, curr_y - 0.14), width - 0.1, row_height,
                               fc="#F8FAFC", ec="none", zorder=3)
            ax.add_patch(row_bg)
            
        # Key Badge ([PK], [FK], or bullet)
        if key_type == "PK":
            k_color = "#B8860B"  # Gold
            k_text = "[PK]"
        elif key_type == "FK":
            k_color = "#2563EB"  # Blue
            k_text = "[FK]"
        elif key_type == "UQ":
            k_color = "#0D9488"  # Teal
            k_text = "[UQ]"
        else:
            k_color = "#94A3B8"  # Slate
            k_text = " • "
            
        ax.text(x + 0.22, curr_y, k_text, ha='left', va='center',
                fontsize=8.5, fontweight='bold', color=k_color, zorder=4)
        
        # Column Name
        ax.text(x + 0.95, curr_y, col_name, ha='left', va='center',
                fontsize=9.5, fontweight='bold', color="#1E293B", zorder=4)
        
        # Data Type
        ax.text(x + width - 0.25, curr_y, data_type, ha='right', va='center',
                fontsize=8.5, fontweight='normal', color="#64748B", zorder=4)
        
        curr_y -= row_height
        
    return {
        "left": x,
        "right": x + width,
        "top": top_y,
        "bottom": bottom_y,
        "center_x": x + width / 2,
        "center_y": (top_y + bottom_y) / 2
    }

def draw_crows_foot_connector(ax, x1, y1, x2, y2, label="", label_pos=(0.5, 0.5), color="#0F2C59"):
    """
    Draws a clean orthogonal or direct relationship connector with Crow's foot cardinality notation.
    """
    # Main connecting line
    ax.plot([x1, x2], [y1, y2], color=color, lw=2.2, zorder=5)
    
    # 1 side notation (Two parallel tick marks: ||)
    # Direction vector
    dx = x2 - x1
    dy = y2 - y1
    dist = (dx**2 + dy**2)**0.5
    if dist > 0:
        ux, uy = dx / dist, dy / dist
        px, py = -uy, ux # Perpendicular
        
        # Tick 1 at start
        t1_x, t1_y = x1 + ux * 0.25, y1 + uy * 0.25
        ax.plot([t1_x - px * 0.16, t1_x + px * 0.16], [t1_y - py * 0.16, t1_y + py * 0.16], color=color, lw=2.0, zorder=6)
        # Tick 2 at start
        t2_x, t2_y = x1 + ux * 0.40, y1 + uy * 0.40
        ax.plot([t2_x - px * 0.16, t2_x + px * 0.16], [t2_y - py * 0.16, t2_y + py * 0.16], color=color, lw=2.0, zorder=6)
        
        # Crow's foot at end (Three prongs)
        cf_base_x, cf_base_y = x2 - ux * 0.35, y2 - uy * 0.35
        # Top prong
        ax.plot([cf_base_x + px * 0.22, x2], [cf_base_y + py * 0.22, y2], color=color, lw=2.0, zorder=6)
        # Bottom prong
        ax.plot([cf_base_x - px * 0.22, x2], [cf_base_y - py * 0.22, y2], color=color, lw=2.0, zorder=6)
        # Ring / circle (zero-or-many circle)
        circle_x, circle_y = x2 - ux * 0.55, y2 - uy * 0.55
        circ = plt.Circle((circle_x, circle_y), 0.10, fc="#FFFFFF", ec=color, lw=1.8, zorder=7)
        ax.add_patch(circ)

    # Relationship Label Badge
    if label:
        lx = x1 + dx * label_pos[0]
        ly = y1 + dy * label_pos[1]
        ax.text(lx, ly, label, ha='center', va='center', fontsize=9.0, fontweight='bold', color="#0F2C59",
                bbox=dict(boxstyle="round,pad=0.35", fc="#FFFFFF", ec="#0F2C59", lw=1.2, zorder=8), zorder=9)

def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(18, 12), dpi=300)
    ax.set_xlim(-0.5, 18.5)
    ax.set_ylim(-0.5, 12.5)
    ax.axis('off')
    
    fig.patch.set_facecolor('#F8FAFC')
    
    # Outer Decorative Canvas Border
    canvas_border = FancyBboxPatch((0.2, 0.2), 18.1, 12.1, boxstyle="round,pad=0.1,rounding_size=0.15",
                                   fc="#FFFFFF", ec="#CBD5E1", lw=1.8, zorder=0)
    ax.add_patch(canvas_border)

    # Diagram Super Header
    ax.text(9.25, 11.8, "ENTITY-RELATIONSHIP (ER) DIAGRAM", ha='center', va='center',
            fontsize=20, fontweight='bold', color='#0F2C59', zorder=10)
    ax.text(9.25, 11.4, "Dutch Point Negombo Web-Based Hotel Management System (hotel_db Schema)",
            ha='center', va='center', fontsize=12, fontweight='bold', color='#B8860B', zorder=10)

    # =========================================================================
    # ENTITIES / TABLES DEFINITIONS
    # =========================================================================
    
    # 1. CUSTOMERS / USERS
    cols_customers = [
        ("PK", "CustomerId", "INT (AUTO_INC)", "Primary Key"),
        ("  ", "FullName", "VARCHAR(100)", "Full legal name"),
        ("UQ", "Email", "VARCHAR(150)", "Login identity"),
        ("  ", "Password", "VARCHAR(255)", "Encrypted hash"),
        ("  ", "Phone", "VARCHAR(25)", "Contact phone"),
        ("  ", "Address", "VARCHAR(255)", "Postal address"),
        ("  ", "Role", "VARCHAR(20)", "Admin / Customer"),
        ("  ", "CreatedAt", "DATETIME", "Audit timestamp")
    ]
    t_customers = draw_table(ax, 1.0, 10.5, 4.6, "CUSTOMERS / USERS", cols_customers, header_bg="#0F2C59")

    # 2. ROOMS
    cols_rooms = [
        ("PK", "RoomId", "INT (AUTO_INC)", "Primary Key"),
        ("UQ", "RoomNumber", "VARCHAR(20)", "Room 101, 201..."),
        ("  ", "RoomType", "VARCHAR(50)", "Deluxe, Ocean Suite"),
        ("  ", "PricePerNight", "DECIMAL(10,2)", "Native LKR rate"),
        ("  ", "Capacity", "INT", "Max headcount limit"),
        ("  ", "Status", "VARCHAR(30)", "Available / Occupied"),
        ("  ", "Description", "TEXT", "Suite overview"),
        ("  ", "Amenities", "VARCHAR(255)", "AC, WiFi, Mini Bar"),
        ("  ", "ImageName", "VARCHAR(100)", "Image asset filename")
    ]
    t_rooms = draw_table(ax, 1.0, 5.0, 4.6, "ROOMS", cols_rooms, header_bg="#1E3A8A")

    # 3. BOOKINGS (Central Transactional Entity)
    cols_bookings = [
        ("PK", "BookingId", "INT (AUTO_INC)", "Primary Key"),
        ("FK", "CustomerId", "INT", "References Customers"),
        ("FK", "RoomId", "INT", "References Rooms"),
        ("  ", "CheckInDate", "DATE", "Arrival date"),
        ("  ", "CheckOutDate", "DATE", "Departure date"),
        ("  ", "NumberOfGuests", "INT", "Enforced <= Capacity"),
        ("  ", "TotalAmount", "DECIMAL(10,2)", "Total stay in LKR"),
        ("  ", "BookingStatus", "VARCHAR(30)", "Confirmed / Cancelled"),
        ("  ", "SpecialRequests", "TEXT", "Guest requests"),
        ("  ", "CreatedAt", "DATETIME", "Booking timestamp")
    ]
    t_bookings = draw_table(ax, 7.8, 8.5, 4.8, "BOOKINGS", cols_bookings, header_bg="#047857")

    # 4. PAYMENTS
    cols_payments = [
        ("PK", "PaymentId", "INT (AUTO_INC)", "Primary Key"),
        ("FK", "BookingId", "INT", "References Bookings"),
        ("  ", "Amount", "DECIMAL(10,2)", "Settled amount LKR"),
        ("  ", "PaymentMethod", "VARCHAR(30)", "Cash / Card / IPG"),
        ("  ", "PaymentStatus", "VARCHAR(20)", "Completed / Pending"),
        ("UQ", "TransactionRef", "VARCHAR(100)", "Bank receipt code"),
        ("  ", "PaidAt", "DATETIME", "Payment timestamp")
    ]
    t_payments = draw_table(ax, 14.2, 8.0, 3.8, "PAYMENTS", cols_payments, header_bg="#B45309")

    # =========================================================================
    # RELATIONSHIP CONNECTORS (CROW'S FOOT NOTATION)
    # =========================================================================

    # 1. CUSTOMERS (1) -> (0..N) BOOKINGS
    # Line from right edge of Customers to left edge of Bookings
    draw_crows_foot_connector(
        ax,
        t_customers["right"], t_customers["center_y"] + 0.4,
        t_bookings["left"], t_bookings["top"] - 1.2,
        label="1 : N\n(places)",
        label_pos=(0.48, 0.52),
        color="#0F2C59"
    )

    # 2. ROOMS (1) -> (0..N) BOOKINGS
    # Line from right edge of Rooms to left edge of Bookings
    draw_crows_foot_connector(
        ax,
        t_rooms["right"], t_rooms["center_y"] + 0.6,
        t_bookings["left"], t_bookings["bottom"] + 1.2,
        label="1 : N\n(reserved for)",
        label_pos=(0.48, 0.48),
        color="#1E3A8A"
    )

    # 3. BOOKINGS (1) -> (0..1) PAYMENTS
    # Line from right edge of Bookings to left edge of Payments
    # Booking to Payment is 1 to 0..1 settlement
    draw_crows_foot_connector(
        ax,
        t_bookings["right"], t_bookings["center_y"] - 0.2,
        t_payments["left"], t_payments["center_y"] - 0.2,
        label="1 : 1\n(settled by)",
        label_pos=(0.50, 0.50),
        color="#047857"
    )

    # =========================================================================
    # LEGEND & ARCHITECTURAL ANNOTATION BOX
    # =========================================================================
    legend_box = FancyBboxPatch((13.5, 0.8), 4.5, 3.2, boxstyle="round,pad=0.05,rounding_size=0.1",
                                fc="#F8FAFC", ec="#94A3B8", lw=1.2, zorder=2)
    ax.add_patch(legend_box)
    
    ax.text(15.75, 3.65, "ERD NOTATION & CONSTRAINTS", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color="#0F2C59", zorder=3)
    
    legend_items = [
        ("[PK]", "#B8860B", "Primary Key (Unique, Auto-increment)"),
        ("[FK]", "#2563EB", "Foreign Key (Referential integrity constraint)"),
        ("[UQ]", "#0D9488", "Unique Key constraint (No duplicates)"),
        ("||", "#0F2C59", "One and only one (Mandatory parent)"),
        ("|<", "#0F2C59", "Zero or many (Crow's foot cardinality)"),
        ("LKR", "#047857", "Standardized in Sri Lankan Rupees (decimal 10,2)")
    ]
    
    ly = 3.25
    for tag, tcolor, desc in legend_items:
        ax.text(13.8, ly, tag, ha='left', va='center', fontsize=9.0, fontweight='bold', color=tcolor, zorder=3)
        ax.text(14.5, ly, f": {desc}", ha='left', va='center', fontsize=8.5, color="#334155", zorder=3)
        ly -= 0.40

    # Business Integrity Rules Callout
    rules_box = FancyBboxPatch((6.0, 0.8), 6.8, 3.2, boxstyle="round,pad=0.05,rounding_size=0.1",
                               fc="#EFF6FF", ec="#3B82F6", lw=1.2, zorder=2)
    ax.add_patch(rules_box)
    
    ax.text(9.4, 3.65, "DATABASE INTEGRITY & BUSINESS RULES", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color="#1E40AF", zorder=3)
    
    rules = [
        "1. Concurrency Safety: CheckInDate < RequestedCheckOut && CheckOutDate > RequestedCheckIn.",
        "2. Capacity Constraint: NumberOfGuests cannot exceed Rooms.Capacity (Strictly enforced).",
        "3. Zero Orphaned Records: ON DELETE RESTRICT on active bookings preserves financial ledger.",
        "4. Role Security: Customers table isolates Admin vs Customer credentials on server-side.",
        "5. Financial Precision: TotalAmount = Nights * PricePerNight stored natively in decimal(10,2)."
    ]
    ry = 3.25
    for rule in rules:
        ax.text(6.3, ry, rule, ha='left', va='center', fontsize=8.2, color="#1E3A8A", zorder=3)
        ry -= 0.42

    plt.tight_layout()
    
    # Save HD PNG
    out_png = r"C:\Users\PASINDU\Desktop\Interim\er_diagram.png"
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"ER Diagram generated successfully: {out_png}")

if __name__ == "__main__":
    generate_er_diagram()
