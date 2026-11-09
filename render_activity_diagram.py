import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Rectangle

def draw_action(ax, x, y, text, w=3.4, h=0.65, bg="#EBF3FA", border="#1E56A0", text_color="#0F2C59", fontsize=9.0):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.04,rounding_size=0.18",
                         fc=bg, ec=border, lw=1.8, zorder=3)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight='bold',
            color=text_color, zorder=4, multialignment='center')
    return {"top": y + h/2, "bottom": y - h/2, "left": x - w/2, "right": x + w/2, "center_x": x, "center_y": y}

def draw_decision(ax, x, y, text, size=0.55, bg="#FEF9E7", border="#B7950B"):
    # Diamond shape
    diamond = Polygon([
        [x, y + size],
        [x + size * 1.5, y],
        [x, y - size],
        [x - size * 1.5, y]
    ], fc=bg, ec=border, lw=2, zorder=3)
    ax.add_patch(diamond)
    ax.text(x, y, text, ha='center', va='center', fontsize=8.0, fontweight='bold',
            color="#7D6608", zorder=4, multialignment='center')
    return {"top": y + size, "bottom": y - size, "left": x - size * 1.5, "right": x + size * 1.5, "center_x": x, "center_y": y}

def draw_arrow(ax, x1, y1, x2, y2, label="", label_pos=(0.5, 0.5), color="#0F2C59", lw=1.8, linestyle='-'):
    ax.annotate(
        '', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color=color, lw=lw, linestyle=linestyle, shrinkA=0, shrinkB=0),
        zorder=2
    )
    if label:
        lx = x1 + (x2 - x1) * label_pos[0]
        ly = y1 + (y2 - y1) * label_pos[1]
        ax.text(lx, ly, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color=color,
                bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="none", alpha=0.9), zorder=5)

def draw_start_node(ax, x, y, label="Start"):
    c = Circle((x, y), 0.22, fc="#0F2C59", ec="none", zorder=4)
    ax.add_patch(c)
    ax.text(x, y + 0.35, label, ha='center', va='bottom', fontsize=9.0, fontweight='bold', color="#0F2C59", zorder=4)
    return {"top": y + 0.22, "bottom": y - 0.22, "center_x": x, "center_y": y}

def draw_end_node(ax, x, y, label="End"):
    # Outer circle + Inner filled circle
    c_out = Circle((x, y), 0.26, fc="#FFFFFF", ec="#0F2C59", lw=2, zorder=3)
    c_in = Circle((x, y), 0.16, fc="#0F2C59", ec="none", zorder=4)
    ax.add_patch(c_out)
    ax.add_patch(c_in)
    ax.text(x, y - 0.38, label, ha='center', va='top', fontsize=9.0, fontweight='bold', color="#0F2C59", zorder=4)
    return {"top": y + 0.26, "bottom": y - 0.26, "center_x": x, "center_y": y}

def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(18, 12.5), dpi=300)
    ax.set_xlim(-0.5, 18.5)
    ax.set_ylim(-0.5, 13.0)
    ax.axis('off')
    
    fig.patch.set_facecolor('#F8FAFC')

    # Main Canvas Box
    canvas = FancyBboxPatch((0.2, 0.2), 18.1, 12.6, boxstyle="round,pad=0.1,rounding_size=0.15",
                            fc="#FFFFFF", ec="#CBD5E1", lw=1.8, zorder=0)
    ax.add_patch(canvas)

    # Super Title Header
    ax.text(9.25, 12.35, "UML ACTIVITY DIAGRAM WITH SWIMLANES", ha='center', va='center',
            fontsize=20, fontweight='bold', color='#0F2C59', zorder=10)
    ax.text(9.25, 11.95, "Room Reservation & Transactional Double-Booking Prevention Workflow",
            ha='center', va='center', fontsize=12, fontweight='bold', color='#B8860B', zorder=10)

    # =========================================================================
    # SWIMLANES CONFIGURATION
    # =========================================================================
    lane_top = 11.5
    lane_bottom = 0.5
    lane_h = lane_top - lane_bottom
    header_h = 0.65

    lanes = [
        ("GUEST / CUSTOMER (React SPA Client)", 0.6, 5.6, "#EBF3FA", "#1E56A0"),
        ("APPLICATION SERVER (ASP.NET Core 8 Web API)", 6.4, 6.2, "#FEF3C7", "#D97706"),
        ("DATABASE TIER (MySQL hotel_db)", 12.8, 5.0, "#D1FAE5", "#059669")
    ]

    for title, lx, lw, bg_tint, header_color in lanes:
        # Lane Background
        lane_box = FancyBboxPatch((lx, lane_bottom), lw, lane_h,
                                  boxstyle="round,pad=0.02,rounding_size=0.08",
                                  fc=bg_tint, ec="#CBD5E1", lw=1.2, alpha=0.35, zorder=1)
        ax.add_patch(lane_box)
        
        # Lane Header Box
        hdr = FancyBboxPatch((lx, lane_top - header_h), lw, header_h,
                             boxstyle="round,pad=0.02,rounding_size=0.08",
                             fc=header_color, ec="none", zorder=2)
        ax.add_patch(hdr)
        
        # Lane Header Text
        ax.text(lx + lw/2, lane_top - header_h/2, title, ha='center', va='center',
                fontsize=11.5, fontweight='bold', color="#FFFFFF", zorder=3)

    # Centers of Swimlanes
    c1_x = 0.6 + 5.6 / 2   # 3.4
    c2_x = 6.4 + 6.2 / 2   # 9.5
    c3_x = 12.8 + 5.0 / 2  # 15.3

    # =========================================================================
    # ACTIVITIES & DECISION NODES
    # =========================================================================

    # Step 1: Start Node
    st = draw_start_node(ax, c1_x, 10.3)

    # Step 2: Guest Input
    a1 = draw_action(ax, c1_x, 9.35, "Select Stay Dates,\nGuest Headcount & Room Type")
    draw_arrow(ax, c1_x, st["bottom"], c1_x, a1["top"])

    # Step 3: Trigger Search
    a2 = draw_action(ax, c1_x, 8.2, "Click 'Check Rates & Availability'")
    draw_arrow(ax, c1_x, a1["bottom"], c1_x, a2["top"])

    # Step 4: Backend Process Search
    a3 = draw_action(ax, c2_x, 8.2, "Receive Search Parameters\n(checkIn, checkOut, guests)", bg="#FEF3C7", border="#D97706")
    draw_arrow(ax, a2["right"], a2["center_y"], a3["left"], a3["center_y"], label="HTTP GET /api/rooms")

    # Step 5: DB Query Available
    a4 = draw_action(ax, c3_x, 8.2, "Query Active Bookings\n& Room Capacities", bg="#D1FAE5", border="#059669")
    draw_arrow(ax, a3["right"], a3["center_y"], a4["left"], a4["center_y"], label="SQL Query")

    # Step 6: Backend evaluate status
    a5 = draw_action(ax, c2_x, 7.05, "Evaluate Room Occupancy\n(Assign AVAILABLE / OCCUPIED)", bg="#FEF3C7", border="#D97706")
    # Arrow from DB to Backend
    draw_arrow(ax, a4["center_x"], a4["bottom"], c2_x + 1.8, a5["top"], label="Return Data")

    # Step 7: Display to Guest
    a6 = draw_action(ax, c1_x, 7.05, "Display Available Suites,\nBadges & Rates in LKR")
    draw_arrow(ax, a5["left"], a5["center_y"], a6["right"], a6["center_y"], label="JSON Response")

    # Step 8: Guest Selects Suite
    a7 = draw_action(ax, c1_x, 5.9, "Click 'Book Now'\n& Enter Guest Details")
    draw_arrow(ax, c1_x, a6["bottom"], c1_x, a7["top"])

    # Step 9: Submit Reservation
    a8 = draw_action(ax, c1_x, 4.85, "Submit Reservation Form")
    draw_arrow(ax, c1_x, a7["bottom"], c1_x, a8["top"])

    # Step 10: Backend Validation
    a9 = draw_action(ax, c2_x, 4.85, "Validate Input Payload\n(CheckIn < CheckOut & Capacity)", bg="#FEF3C7", border="#D97706")
    draw_arrow(ax, a8["right"], a8["center_y"], a9["left"], a9["center_y"], label="HTTP POST /api/bookings")

    # Step 11: Decision 1 (Payload Valid?)
    d1 = draw_decision(ax, c2_x, 3.8, "Valid\nDates?")
    draw_arrow(ax, c2_x, a9["bottom"], c2_x, d1["top"])

    # If Invalid -> Return 400 Bad Request to Guest
    err1 = draw_action(ax, c1_x, 3.8, "Display Validation Error Alert\n(Invalid dates or overcapacity)", bg="#FEE2E2", border="#EF4444", text_color="#B91C1C")
    draw_arrow(ax, d1["left"], d1["center_y"], err1["right"], err1["center_y"], label="[No: Invalid]")

    # If Valid -> Concurrency Overlap Check
    a10 = draw_action(ax, c2_x, 2.65, "Execute Double-Booking Check:\n(ExistingIn < ReqOut && ExistingOut > ReqIn)", bg="#FDE68A", border="#D97706", w=4.5)
    draw_arrow(ax, c2_x, d1["bottom"], c2_x, a10["top"], label="[Yes: Valid]")

    # Step 12: Decision 2 (Overlap Exists?)
    d2 = draw_decision(ax, c2_x, 1.45, "Overlap\nExists?")
    draw_arrow(ax, c2_x, a10["bottom"], c2_x, d2["top"])

    # If Overlap Exists [Yes: Conflict] -> Reject with HTTP 409
    err2 = draw_action(ax, c1_x, 2.65, "Display Double-Booking Error:\n'Room already reserved' (HTTP 409)", bg="#FEE2E2", border="#EF4444", text_color="#B91C1C")
    # Route arrow from d2 up-left to err2
    draw_arrow(ax, d2["left"], d2["center_y"], err2["right"], err2["center_y"], label="[Yes: Overlap Found]")

    # If No Overlap [No: Free] -> DB Transaction Commit
    a11 = draw_action(ax, c3_x, 1.45, "Execute ACID Transaction:\nInsert Booking & Save Total LKR", bg="#D1FAE5", border="#059669")
    draw_arrow(ax, d2["right"], d2["center_y"], a11["left"], a11["center_y"], label="[No: Room Free]")

    # Step 13: Confirmation Receipt to Guest
    a12 = draw_action(ax, c1_x, 1.45, "Display Confirmation Modal\n& Reservation ID (#RES-XXXX)", bg="#DCFCE7", border="#16A34A", text_color="#15803D")
    draw_arrow(ax, a11["center_x"], a11["bottom"], c2_x + 1.2, 0.7, label="Commit OK")
    # Connect from c2 to a12
    draw_arrow(ax, c2_x + 1.2, 0.7, a12["right"], 0.7, label="HTTP 200 Created")
    draw_arrow(ax, a12["right"], 0.7, a12["center_x"] + 1.0, a12["bottom"])

    # Final End Nodes
    end1 = draw_end_node(ax, c1_x - 1.2, 0.65, "Success")
    draw_arrow(ax, a12["center_x"] - 0.5, a12["bottom"], end1["center_x"], end1["top"])

    end2 = draw_end_node(ax, c1_x - 2.0, 3.8, "Retry")
    draw_arrow(ax, err1["left"], err1["center_y"], end2["center_x"], end2["top"])

    plt.tight_layout()
    
    # Save HD PNG
    out_png = r"C:\Users\PASINDU\Desktop\Interim\activity_diagram_hd.png"
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Activity Diagram generated successfully: {out_png}")

if __name__ == "__main__":
    generate_activity_diagram()
