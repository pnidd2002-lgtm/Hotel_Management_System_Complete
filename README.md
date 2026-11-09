# Web Based Hotel Management System - Presentation Demo

Tailored for **ESOFT BIT Project Proposal**  
**Faculty of Computing – ESOFT Uni**

---

## 📌 Project Overview
This project is an automated, web-based Hotel Management System developed according to the specifications in the project proposal. It replaces error-prone manual paper-based hotel operations with an integrated digital platform that streamlines room reservations, monitors room occupancy, and prevents booking conflicts.

### Key Highlights for Demo Presentation:
1. **Three User Roles Supported**:
   - **Administrator**: Hotel analytics dashboard, revenue KPIs, room inventory management.
   - **Receptionist**: Occupied rooms tracker, check-in / check-out operations, reservation management.
   - **Customer**: Real-time room availability search, online reservations, booking history, profile.
2. **Prevent Double Booking (Mandatory Feature)**:
   - Evaluates date overlaps (`CheckIn < RequestedCheckOut && CheckOut > RequestedCheckIn`).
   - Blocks conflicting bookings and displays high-visibility alert with conflicting dates and guest info.
3. **Show Occupied Rooms (Mandatory Feature)**:
   - Dedicated interactive tracker showing occupied rooms, guest contact details, stay duration, and check-in/out status.
4. **Clean Code & Architecture**:
   - Backend structure kept simple and intuitive.
   - All database entities placed inside the `Models` folder (`Customer.cs`, `Room.cs`, `Booking.cs`, and DTOs).
   - **No Pomelo used**: Uses the official **Oracle `MySql.EntityFrameworkCore`** provider.
   - **Authentication**: Password hashing left out (plain-text authentication for interim demo requirements).
   - **Visual Assets**: Real hotel and room images downloaded and bundled directly in `src/assets/`.

---

## 🏗️ Technology Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 19, Bootstrap 5, Bootstrap Icons, Vite |
| **Backend** | ASP.NET Core 10 Web API |
| **ORM** | Entity Framework Core via `MySql.EntityFrameworkCore` (Official Oracle Provider, No Pomelo) |
| **Database** | MySQL 8.0 (`hotel_db`) |
| **API Format** | RESTful JSON APIs |

---

## 🗄️ Database Structure (`hotel_db`)

The complete SQL schema and seed data are located in `database/hotel_db.sql`:

1. **`Customers`**: Stores user credentials, phone, address, and role (`Customer`, `Receptionist`, `Admin`).
2. **`Rooms`**: Room number, type, nightly rate, guest capacity, amenities, description, and image reference.
3. **`Bookings`**: Foreign keys to `Customers` and `Rooms`, check-in/check-out dates, guest count, total amount, status (`Confirmed`, `Checked-In`, `Completed`, `Cancelled`), and special requests.

---

## 🔑 Quick Demo Credentials

For quick presentation during the viva or demonstration:

| Role | Email | Password |
|---|---|---|
| **Administrator** | `admin@hotel.com` | `admin123` |
| **Receptionist** | `reception@hotel.com` | `reception123` |
| **Customer** | `john.doe@example.com` | `customer123` |
| **Customer 2** | `sarah.c@example.com` | `sarah2026` |

*Note: The UI includes a 1-click **"Demo Role"** switcher in the navigation bar and quick pre-fill buttons inside the sign-in modal for quick switching during presentations.*

---

## 🚀 How to Run

### 1. Database Setup (Already configured)
The database script is available in:
```bash
database/hotel_db.sql
```
To import into MySQL (if re-creating):
```bash
mysql -u root -p < database/hotel_db.sql
```

### 2. Backend (ASP.NET Core Web API)
```bash
cd backend
dotnet run --launch-profile http
```
- API Base URL: `http://localhost:5000`
- Swagger / OpenAPI: `http://localhost:5000/openapi/v1.json`

### 3. Frontend (React + Bootstrap 5)
```bash
cd frontend
npm install
npm run dev
```
- Web Application URL: `http://localhost:5173`

---

## 🎯 Verification of Demo Requirements

1. **Prevent Double Booking**:
   - Try booking Room 101 for dates overlapping `2026-09-27` to `2026-10-02`.
   - The backend halts the transaction and returns a conflict response, displaying a clear prompt explaining that Room 101 is already booked by John Doe.
2. **Show Occupied Rooms**:
   - Click the **"Occupied Rooms"** tab in the navigation bar.
   - Room 101 is shown with an **OCCUPIED** badge, guest details, check-in and check-out dates.
   - Staff can execute quick **Check-In** or **Check-Out** directly from this screen.
3. **Room Availability Search**:
   - Changing the Check-In and Check-Out dates on the home screen immediately flags any room with conflicting reservations as **OCCUPIED**.
