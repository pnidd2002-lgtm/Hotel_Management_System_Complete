import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Ellipse, Rectangle

def draw_stick_figure(ax, x, y, label, scale=1.0):
    # Head
    head_radius = 0.18 * scale
    head = plt.Circle((x, y + 0.65 * scale), head_radius, fill=False, color='#0F2C59', lw=2.2)
    ax.add_patch(head)
    
    # Body
    ax.plot([x, x], [y + 0.47 * scale, y - 0.05 * scale], color='#0F2C59', lw=2.2)
    
    # Arms
    ax.plot([x - 0.35 * scale, x + 0.35 * scale], [y + 0.28 * scale, y + 0.28 * scale], color='#0F2C59', lw=2.2)
    
    # Left Leg
    ax.plot([x, x - 0.28 * scale], [y - 0.05 * scale, y - 0.55 * scale], color='#0F2C59', lw=2.2)
    
    # Right Leg
    ax.plot([x, x + 0.28 * scale], [y - 0.05 * scale, y - 0.55 * scale], color='#0F2C59', lw=2.2)
    
    # Label
    ax.text(x, y - 0.82 * scale, label, ha='center', va='top', fontsize=11, fontweight='bold', color='#0F2C59')

def draw_use_case(ax, x, y, text, w=2.8, h=0.75, bg='#EBF3FA', border='#1E56A0'):
    ellipse = Ellipse((x, y), w, h, facecolor=bg, edgecolor=border, lw=2, zorder=3)
    ax.add_patch(ellipse)
    ax.text(x, y, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F2C59', zorder=4, multialignment='center')

def draw_arrow(ax, x1, y1, x2, y2, label="", dashed=True, color='#B8860B'):
    linestyle = '--' if dashed else '-'
    ax.annotate(
        '', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color=color, lw=1.8, linestyle=linestyle),
        zorder=2
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.12, label, ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=color, zorder=5,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))

def draw_association(ax, x1, y1, x2, y2, color='#2C3E50'):
    ax.plot([x1, x2], [y1, y2], color=color, lw=1.5, zorder=1)

def generate_diagram():
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    ax.set_xlim(-2.5, 14.5)
    ax.set_ylim(-1.5, 10.5)
    ax.axis('off')
    
    # Figure Background
    fig.patch.set_facecolor('#FFFFFF')

    # System Boundary Box
    boundary = FancyBboxPatch((0.8, -0.6), 10.4, 10.2, boxstyle="round,pad=0.1,rounding_size=0.15",
                              fc="#F8FAFC", ec="#0F2C59", lw=2.5, zorder=0)
    ax.add_patch(boundary)
    
    # Boundary Title Banner
    ax.text(6.0, 9.35, "Dutch Point Negombo Hotel Management System", ha='center', va='center',
            fontsize=15, fontweight='bold', color='#0F2C59',
            bbox=dict(boxstyle="round,pad=0.4", fc="#E2E8F0", ec="#0F2C59", lw=1.2))

    # =========================================================================
    # ACTORS
    # =========================================================================
    # Left Actors
    draw_stick_figure(ax, -1.0, 7.3, "Guest /\nCustomer", scale=1.1)
    draw_stick_figure(ax, -1.0, 2.5, "Front Desk\nReceptionist", scale=1.1)
    
    # Right Actor
    draw_stick_figure(ax, 12.8, 4.8, "Hotel\nAdministrator", scale=1.1)

    # =========================================================================
    # USE CASES (Inside Boundary)
    # =========================================================================
    # Column 1 (Core Guest & Public Features)
    uc_search = (3.4, 8.2); draw_use_case(ax, *uc_search, "Search Available\nRooms & Rates")
    uc_details = (3.4, 6.8); draw_use_case(ax, *uc_details, "View Suite Details\n& Amenities")
    uc_auth = (3.4, 5.4); draw_use_case(ax, *uc_auth, "Register / Sign In\nAccount (RBAC)")
    uc_book = (3.4, 4.0); draw_use_case(ax, *uc_book, "Book Room /\nReservation", bg='#D4E6F1', border='#0F2C59')
    uc_mybook = (3.4, 2.6); draw_use_case(ax, *uc_mybook, "View / Cancel My\nReservations")
    
    # Column 2 (Operational & Extension Features)
    uc_double = (8.4, 5.2); draw_use_case(ax, *uc_double, "Prevent Double\nBooking", bg='#FADBD8', border='#C0392B')
    uc_lkr = (8.4, 4.0); draw_use_case(ax, *uc_lkr, "Calculate Rates\nin LKR", bg='#FCF3CF', border='#B7950B')
    uc_spec = (8.4, 2.8); draw_use_case(ax, *uc_spec, "Add Special\nRequests", bg='#EAFAF1', border='#27AE60')

    # Column 1 Bottom (Operational & Admin Features)
    uc_occupancy = (3.4, 1.2); draw_use_case(ax, *uc_occupancy, "Track Room\nOccupancy")
    uc_checkin = (3.4, -0.1); draw_use_case(ax, *uc_checkin, "Manage Check-In\n& Check-Out")

    # Column 2 Bottom (Admin Features)
    uc_rooms = (8.4, 1.2); draw_use_case(ax, *uc_rooms, "Manage Room\nInventory")
    uc_revenue = (8.4, -0.1); draw_use_case(ax, *uc_revenue, "View Revenue &\nKPI Dashboard")

    # =========================================================================
    # ASSOCIATIONS: GUEST / CUSTOMER
    # =========================================================================
    g_x, g_y = -0.6, 7.3
    draw_association(ax, g_x, g_y, 2.0, uc_search[1])
    draw_association(ax, g_x, g_y, 2.0, uc_details[1])
    draw_association(ax, g_x, g_y, 2.0, uc_auth[1])
    draw_association(ax, g_x, g_y, 2.0, uc_book[1])
    draw_association(ax, g_x, g_y, 2.0, uc_mybook[1])

    # =========================================================================
    # ASSOCIATIONS: FRONT DESK RECEPTIONIST
    # =========================================================================
    r_x, r_y = -0.6, 2.5
    draw_association(ax, r_x, r_y, 2.0, uc_search[1])
    draw_association(ax, r_x, r_y, 2.0, uc_auth[1])
    draw_association(ax, r_x, r_y, 2.0, uc_book[1])
    draw_association(ax, r_x, r_y, 2.0, uc_mybook[1])
    draw_association(ax, r_x, r_y, 2.0, uc_occupancy[1])
    draw_association(ax, r_x, r_y, 2.0, uc_checkin[1])

    # =========================================================================
    # ASSOCIATIONS: HOTEL ADMINISTRATOR
    # =========================================================================
    a_x, a_y = 12.4, 4.8
    draw_association(ax, a_x, a_y, 4.8, uc_auth[1])
    draw_association(ax, a_x, a_y, 9.8, uc_occupancy[1])
    draw_association(ax, a_x, a_y, 9.8, uc_rooms[1])
    draw_association(ax, a_x, a_y, 9.8, uc_revenue[1])

    # =========================================================================
    # INCLUDES & EXTENDS RELATIONSHIPS
    # =========================================================================
    # Book Room <<include>> Prevent Double Booking
    draw_arrow(ax, 4.7, 4.3, 7.0, 5.0, label="<<include>>", dashed=True, color='#C0392B')
    
    # Book Room <<include>> Calculate Rates in LKR
    draw_arrow(ax, 4.8, 4.0, 7.0, 4.0, label="<<include>>", dashed=True, color='#B7950B')
    
    # Add Special Requests <<extend>> Book Room
    draw_arrow(ax, 7.0, 3.2, 4.7, 3.8, label="<<extend>>", dashed=True, color='#27AE60')

    # Header Title
    plt.title("UML Use Case Diagram: Dutch Point Negombo Web-Based Hotel Management System",
              fontsize=16, fontweight='bold', color='#0F2C59', pad=18)
    
    plt.tight_layout()
    
    # Save High-Res PNG
    out_png = r"C:\Users\PASINDU\Desktop\Interim\use_case_diagram_hd.png"
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"High-resolution diagram saved to: {out_png}")

if __name__ == "__main__":
    generate_diagram()
