import React, { useState, useEffect } from 'react';
import { images, getRoomImage } from './assets/images';
import LoginModal from './components/LoginModal';
import BookingModal from './components/BookingModal';
import PaymentModal from './components/PaymentModal';

export default function App() {
  // Current user state (null on launch until logged in)
  const [user, setUser] = useState(null);

  const [activeTab, setActiveTab] = useState('home'); // 'home', 'rooms', 'occupied', 'my-bookings', 'admin-rooms'
  
  // Date & Room filters
  const [checkInFilter, setCheckInFilter] = useState('2026-10-10');
  const [checkOutFilter, setCheckOutFilter] = useState('2026-10-15');
  const [roomTypeFilter, setRoomTypeFilter] = useState('');
  const [guestsFilter, setGuestsFilter] = useState('2');

  // Data state
  const [rooms, setRooms] = useState([]);
  const [loadingRooms, setLoadingRooms] = useState(false);
  const [occupiedRooms, setOccupiedRooms] = useState([]);
  const [occupiedDate, setOccupiedDate] = useState('2026-10-10');
  const [occupiedTargetLabel, setOccupiedTargetLabel] = useState('2026-10-10');
  const [occupancyViewMode, setOccupancyViewMode] = useState('date'); // 'date' or 'all'
  const [allActiveBookings, setAllActiveBookings] = useState([]);
  const [loadingOccupancy, setLoadingOccupancy] = useState(false);
  const [myBookings, setMyBookings] = useState([]);

  // Modals state
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedBookingForPayment, setSelectedBookingForPayment] = useState(null);
  const [selectedRoom, setSelectedRoom] = useState(null);

  // Notifications
  const [message, setMessage] = useState('');

  // Admin Dashboard & Reports State
  const [dashboardStats, setDashboardStats] = useState(null);
  const [adminPayments, setAdminPayments] = useState([]);
  const [loadingDashboard, setLoadingDashboard] = useState(false);

  // Gallery & Contact Form State
  const [galleryFilter, setGalleryFilter] = useState('all'); // 'all', 'suites', 'views'
  const [inquiryName, setInquiryName] = useState('');
  const [inquiryEmail, setInquiryEmail] = useState('');
  const [inquirySubject, setInquirySubject] = useState('Reservation Inquiry');
  const [inquiryMessage, setInquiryMessage] = useState('');

  // Admin Room Form State
  const [newRoomNumber, setNewRoomNumber] = useState('');
  const [newRoomType, setNewRoomType] = useState('Ocean View Suite');
  const [newRoomPrice, setNewRoomPrice] = useState('65000');
  const [newRoomCapacity, setNewRoomCapacity] = useState('2');
  const [newRoomAmenities, setNewRoomAmenities] = useState('Private Balcony, Ocean View, Mini Bar, AC, WiFi');
  const [newRoomDesc, setNewRoomDesc] = useState('');
  const [newRoomImage, setNewRoomImage] = useState('room_suite.jpg');

  // Load Rooms from Backend
  const loadRooms = async () => {
    setLoadingRooms(true);
    try {
      let url = `http://localhost:5000/api/rooms?checkIn=${checkInFilter}&checkOut=${checkOutFilter}`;
      if (roomTypeFilter) url += `&roomType=${roomTypeFilter}`;
      if (guestsFilter) url += `&guests=${guestsFilter}`;

      const res = await fetch(url);
      const data = await res.json();
      setRooms(data);
    } catch (err) {
      console.error('Failed to load rooms:', err);
    } finally {
      setLoadingRooms(false);
    }
  };

  // Load Occupied Rooms (Supports single date or date range)
  const loadOccupiedRooms = async (date = occupiedDate, checkOut = null) => {
    setLoadingOccupancy(true);
    try {
      let url = `http://localhost:5000/api/bookings/occupied-rooms?targetDate=${date}`;
      if (checkOut) {
        url = `http://localhost:5000/api/bookings/occupied-rooms?checkIn=${date}&checkOut=${checkOut}`;
      }
      const res = await fetch(url);
      const data = await res.json();
      setOccupiedRooms(data.occupiedRooms || []);
      setOccupiedTargetLabel(data.targetDate || date);
    } catch (err) {
      console.error('Failed to load occupied rooms:', err);
    } finally {
      setLoadingOccupancy(false);
    }
  };

  // Load All Active Reservations across the resort
  const loadAllActiveBookings = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/bookings');
      const data = await res.json();
      const active = data.filter(b => b.bookingStatus === 'Confirmed' || b.bookingStatus === 'Checked-In');
      setAllActiveBookings(active);
    } catch (err) {
      console.error('Failed to load all active bookings:', err);
    }
  };

  // Open Occupancy Tracker synchronized with search dates
  const openOccupancyTracker = (date = null, checkOut = null) => {
    const targetCheckIn = date || checkInFilter || '2026-10-10';
    const targetCheckOut = checkOut || checkOutFilter || '2026-10-15';
    setOccupiedDate(targetCheckIn);
    setOccupancyViewMode('date');
    setActiveTab('occupied');
    loadOccupiedRooms(targetCheckIn, targetCheckOut);
    loadAllActiveBookings();
  };

  // Load Customer's Bookings
  const loadMyBookings = async () => {
    if (!user) return;
    try {
      const res = await fetch(`http://localhost:5000/api/bookings?customerId=${user.customerId}`);
      const data = await res.json();
      setMyBookings(data);
    } catch (err) {
      console.error('Failed to load my bookings:', err);
    }
  };

  // Load Admin Dashboard Metrics & Card Transactions
  const loadAdminDashboard = async () => {
    if (!user || user.role !== 'Admin') return;
    setLoadingDashboard(true);
    try {
      // 1. Fetch KPI metrics (Total Revenue, Total Bookings, Registered Customers)
      const statsRes = await fetch('http://localhost:5000/api/dashboard/stats');
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setDashboardStats(statsData);
      }

      // 2. Fetch Card Payment Transactions (Requires Admin Bearer Token)
      const paymentsRes = await fetch('http://localhost:5000/api/payments', {
        headers: {
          'Authorization': `Bearer ${user.token}`
        }
      });
      if (paymentsRes.ok) {
        const paymentsData = await paymentsRes.json();
        setAdminPayments(Array.isArray(paymentsData) ? paymentsData : []);
      }
    } catch (err) {
      console.error('Failed to load admin dashboard:', err);
    } finally {
      setLoadingDashboard(false);
    }
  };

  // Initial load
  useEffect(() => {
    loadRooms();
    loadAllActiveBookings();
  }, []);

  useEffect(() => {
    if (activeTab === 'occupied') {
      loadOccupiedRooms(occupiedDate);
      loadAllActiveBookings();
    } else if (activeTab === 'my-bookings') {
      loadMyBookings();
    } else if (activeTab === 'admin-dashboard') {
      loadAdminDashboard();
    }
  }, [activeTab, occupiedDate, user]);

  // Cancel Booking
  const handleCancelBooking = async (bookingId) => {
    if (!window.confirm('Cancel this reservation?')) return;
    try {
      await fetch(`http://localhost:5000/api/bookings/${bookingId}`, {
        method: 'DELETE'
      });
      setMessage(`Reservation #${bookingId} was successfully cancelled.`);
      setTimeout(() => setMessage(''), 4000);
      loadMyBookings();
      loadRooms();
      loadOccupiedRooms(occupiedDate);
      loadAllActiveBookings();
    } catch (err) {
      alert('Error cancelling booking');
    }
  };

  // Admin Add Room
  const handleAddRoom = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:5000/api/rooms', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': user?.token ? `Bearer ${user.token}` : ''
        },
        body: JSON.stringify({
          roomNumber: newRoomNumber,
          roomType: newRoomType,
          pricePerNight: parseFloat(newRoomPrice),
          capacity: parseInt(newRoomCapacity),
          status: 'Available',
          amenities: newRoomAmenities,
          description: newRoomDesc,
          imageName: newRoomImage
        })
      });
      if (res.ok) {
        setMessage(`Suite #${newRoomNumber} added to inventory!`);
        setTimeout(() => setMessage(''), 4000);
        setNewRoomNumber('');
        setNewRoomDesc('');
        loadRooms();
        loadAdminDashboard();
      } else {
        const err = await res.json();
        alert(err.message || 'Error creating room');
      }
    } catch (err) {
      alert('Error connecting to backend');
    }
  };

  // Contact Inquiry Submission Handler
  const handleInquirySubmit = (e) => {
    e.preventDefault();
    setMessage(`Thank you, ${inquiryName}! Your inquiry regarding "${inquirySubject}" has been sent to our concierge.`);
    setTimeout(() => setMessage(''), 5000);
    setInquiryName('');
    setInquiryEmail('');
    setInquiryMessage('');
  };

  return (
    <div className="min-vh-100 d-flex flex-column bg-white">

      {/* TOP NAVIGATION BAR - Matches Uploaded Screenshot */}
      <header className="border-bottom sticky-top bg-white shadow-sm" style={{ zIndex: 100 }}>
        <div className="container py-2 d-flex align-items-center justify-content-between">
          
          {/* Left Links */}
          <nav className="d-none d-lg-flex align-items-center gap-1">
            <button 
              className={`btn btn-link nav-link-custom text-decoration-none ${activeTab === 'home' ? 'active' : ''}`}
              onClick={() => setActiveTab('home')}
            >
              HOME
            </button>
            <button 
              className={`btn btn-link nav-link-custom text-decoration-none ${activeTab === 'rooms' ? 'active' : ''}`}
              onClick={() => setActiveTab('rooms')}
            >
              ROOMS ▾
            </button>
            <button 
              className={`btn btn-link nav-link-custom text-decoration-none ${activeTab === 'occupied' ? 'active' : ''}`}
              onClick={() => openOccupancyTracker(checkInFilter, checkOutFilter)}
            >
              OCCUPIED
            </button>
            <button 
              className={`btn btn-link nav-link-custom text-decoration-none ${activeTab === 'dining' ? 'active' : ''}`}
              onClick={() => setActiveTab('dining')}
            >
              DINING
            </button>
            <button 
              className={`btn btn-link nav-link-custom text-decoration-none ${activeTab === 'gallery' ? 'active' : ''}`}
              onClick={() => setActiveTab('gallery')}
            >
              GALLERY
            </button>
          </nav>

          {/* Center Logo - Dutch Point Negombo */}
          <div 
            className="d-flex align-items-center gap-2 cursor-pointer text-center mx-auto mx-lg-0"
            onClick={() => setActiveTab('home')}
            style={{ cursor: 'pointer' }}
          >
            {/* Sunset & Palm SVG Icon */}
            <div className="d-flex align-items-center justify-content-center" style={{ width: '48px', height: '48px' }}>
              <svg viewBox="0 0 100 100" width="46" height="46">
                <defs>
                  <linearGradient id="sunGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#ff7e40" />
                    <stop offset="100%" stopColor="#f5b041" />
                  </linearGradient>
                </defs>
                <circle cx="50" cy="50" r="46" fill="url(#sunGrad)" />
                {/* Ocean line */}
                <path d="M 4 64 Q 50 60 96 64 L 96 96 L 4 96 Z" fill="#0b1320" />
                {/* Palm silhouettes */}
                <path d="M 40 70 Q 42 42 50 35 Q 52 42 46 70 Z" fill="#0b1320" />
                <path d="M 50 35 Q 36 28 26 36 Q 38 33 50 35 Z" fill="#0b1320" />
                <path d="M 50 35 Q 60 22 72 26 Q 60 30 50 35 Z" fill="#0b1320" />
                <path d="M 50 35 Q 46 18 36 20 Q 44 26 50 35 Z" fill="#0b1320" />
                <path d="M 50 35 Q 56 20 64 16 Q 58 26 50 35 Z" fill="#0b1320" />
              </svg>
            </div>
            <div className="text-start">
              <span className="brand-serif fs-4 fw-bold text-dark d-block lh-1">Dutch Point</span>
              <small className="brand-gold fw-bold text-uppercase" style={{ fontSize: '0.62rem', letterSpacing: '2px' }}>
                Negombo Resort
              </small>
            </div>
          </div>

          {/* Right Links & Auth */}
          <div className="d-flex align-items-center gap-2">
            <button 
              className={`btn btn-link nav-link-custom text-decoration-none d-none d-lg-inline ${activeTab === 'about' ? 'active' : ''}`}
              onClick={() => setActiveTab('about')}
            >
              ABOUT US
            </button>
            <button 
              className={`btn btn-link nav-link-custom text-decoration-none d-none d-lg-inline ${activeTab === 'contact' ? 'active' : ''}`}
              onClick={() => setActiveTab('contact')}
            >
              CONTACT US
            </button>

            {user ? (
              <div className="d-flex align-items-center gap-2 ms-2">
                <button 
                  className={`btn btn-sm btn-luxury-pill py-1 px-3 ${activeTab === 'my-bookings' ? 'bg-light border-dark' : ''}`}
                  onClick={() => setActiveTab('my-bookings')}
                >
                  My Bookings
                </button>

                {user.role === 'Admin' && (
                  <>
                    <button 
                      className={`btn btn-sm btn-luxury-pill py-1 px-3 ${activeTab === 'admin-dashboard' ? 'bg-light border-dark' : ''}`}
                      onClick={() => setActiveTab('admin-dashboard')}
                    >
                      <i className="bi bi-graph-up me-1"></i> Reports
                    </button>
                    <button 
                      className={`btn btn-sm btn-luxury-pill py-1 px-3 ${activeTab === 'admin-rooms' ? 'bg-light border-dark' : ''}`}
                      onClick={() => setActiveTab('admin-rooms')}
                    >
                      <i className="bi bi-door-open me-1"></i> Inventory
                    </button>
                  </>
                )}

                <div className="d-none d-md-block text-end ps-2 border-start">
                  <span className="small fw-bold text-dark d-block lh-sm">{user.fullName}</span>
                  <span className="badge rounded-pill bg-dark" style={{ fontSize: '0.65rem' }}>{user.role}</span>
                </div>

                <button 
                  className="btn btn-sm btn-outline-secondary rounded-pill ms-1"
                  onClick={() => {
                    setUser(null);
                    setActiveTab('home');
                    setMessage('Signed out successfully.');
                    setTimeout(() => setMessage(''), 3000);
                  }}
                  title="Log Out"
                >
                  <i className="bi bi-box-arrow-right"></i>
                </button>
              </div>
            ) : (
              <div className="d-flex align-items-center gap-2">
                <button 
                  className="btn btn-luxury-pill btn-sm px-3"
                  onClick={() => setShowLoginModal(true)}
                >
                  SIGN IN
                </button>
                <button 
                  className="btn btn-luxury-dark btn-sm px-3"
                  onClick={() => setShowLoginModal(true)}
                >
                  LOG IN
                </button>
              </div>
            )}
          </div>

        </div>
      </header>

      {/* Global Notification Banner */}
      {message && (
        <div className="container mt-3">
          <div className="alert alert-success alert-dismissible fade show py-2 small shadow-sm rounded-pill px-4" role="alert">
            <i className="bi bi-check-circle-fill me-2 brand-gold"></i> {message}
            <button type="button" className="btn-close py-2" onClick={() => setMessage('')}></button>
          </div>
        </div>
      )}

      {/* MAIN VIEW AREA */}
      <main className="flex-grow-1">

        {/* 1. HERO & HOME VIEW (Exact visual layout of uploaded screenshot) */}
        {activeTab === 'home' && (
          <div>
            {/* HERO SECTION */}
            <section className="py-5 position-relative overflow-hidden">
              <div className="container">
                <div className="row align-items-center g-4">
                  
                  {/* Left Column: Text Presentation */}
                  <div className="col-lg-6 position-relative ps-lg-4">
                    
                    {/* Far Left Vertical Caption */}
                    <div className="position-absolute start-0 top-50 translate-middle-y d-none d-md-block" style={{ left: '-35px' }}>
                      <span className="scroll-perspective">SCROLL PERSPECTIVE</span>
                    </div>

                    <div className="ps-md-4">
                      {/* Boutique Luxury Tagline */}
                      <div className="boutique-tagline mb-3">
                        —— BOUTIQUE LUXURY
                      </div>

                      {/* Main Title */}
                      <h1 className="display-3 fw-bold mb-0 text-dark brand-serif lh-sm" style={{ letterSpacing: '-0.5px' }}>
                        Dutch Point
                      </h1>
                      <h2 className="display-4 brand-gold-italic mb-3 fw-normal" style={{ marginTop: '-8px' }}>
                        Negombo
                      </h2>

                      {/* Subtitle */}
                      <p className="lead text-secondary opacity-90 mb-4" style={{ maxWidth: '480px', fontSize: '1.05rem', lineHeight: '1.7' }}>
                        Where the golden shores of Sri Lanka meet the pinnacle of coastal elegance. 
                        Experience a sanctuary designed for the discerning traveler.
                      </p>

                      {/* Buttons */}
                      <div className="d-flex flex-wrap align-items-center gap-3 mb-5">
                        <button 
                          className="btn btn-luxury-dark"
                          onClick={() => {
                            setActiveTab('rooms');
                            setTimeout(() => {
                              window.scrollTo({ top: 550, behavior: 'smooth' });
                            }, 100);
                          }}
                        >
                          EXPERIENCE LUXURY
                        </button>
                        <button 
                          className="btn btn-luxury-pill d-flex align-items-center gap-2"
                          onClick={() => setActiveTab('rooms')}
                        >
                          <span>🏖️</span> BEACHFRONT PARADISE
                        </button>
                      </div>

                      {/* Stats */}
                      <div className="row pt-3 border-top g-4" style={{ maxWidth: '420px' }}>
                        <div className="col-6">
                          <div className="fs-3 fw-bold text-dark lh-1 mb-1">
                            4.8 <span className="brand-gold fs-5">★</span>
                          </div>
                          <small className="text-muted fw-bold text-uppercase" style={{ fontSize: '0.68rem', letterSpacing: '1px' }}>
                            GUEST RATING
                          </small>
                        </div>
                        <div className="col-6">
                          <div className="fs-3 fw-bold text-dark lh-1 mb-1">
                            Direct
                          </div>
                          <small className="text-muted fw-bold text-uppercase" style={{ fontSize: '0.68rem', letterSpacing: '1px' }}>
                            BEACH ACCESS
                          </small>
                        </div>
                      </div>

                    </div>
                  </div>

                  {/* Right Column: Multi-Layer Luxury Collage */}
                  <div className="col-lg-6 position-relative">
                    <div className="position-relative mx-auto" style={{ maxWidth: '520px', minHeight: '480px' }}>
                      
                      {/* Main Large Card: Illuminated Night Resort */}
                      <div className="hero-card-main w-100" style={{ height: '440px' }}>
                        <img 
                          src={images.resortNight} 
                          alt="Dutch Point Negombo at Night" 
                          className="w-100 h-100 object-fit-cover"
                        />
                      </div>

                      {/* Floating Top-Right Badge: NEGOMBO'S FINEST */}
                      <div className="position-absolute" style={{ top: '-15px', right: '-15px', zIndex: 10 }}>
                        <div className="circle-badge-finest">
                          <span>NEGOMBO'S<br />FINEST</span>
                        </div>
                      </div>

                      {/* Floating Bottom-Left Tilted Card: Balcony View */}
                      <div className="position-absolute hero-card-sub" style={{ bottom: '-30px', left: '-25px', width: '220px', height: '240px', zIndex: 8 }}>
                        <img 
                          src={images.balconyView} 
                          alt="Oceanfront Balcony View" 
                          className="w-100 h-100 object-fit-cover"
                        />
                      </div>

                      {/* Floating Bottom-Right Circular Beach Photo */}
                      <div className="position-absolute circle-badge-img" style={{ bottom: '25px', right: '-20px', zIndex: 9 }}>
                        <img 
                          src={images.beachView} 
                          alt="Golden Sand Beach Negombo" 
                          className="w-100 h-100 object-fit-cover"
                        />
                      </div>

                    </div>
                  </div>

                </div>
              </div>
            </section>

            {/* DATE & CONCIERGE SEARCH BAR */}
            <section className="py-4" style={{ backgroundColor: '#fcfbf8' }}>
              <div className="container">
                <div className="card shadow-sm border-0 rounded-4 p-4 bg-white mx-auto" style={{ maxWidth: '1060px' }}>
                  <div className="row g-3 align-items-end">
                    <div className="col-lg-3 col-md-6">
                      <label className="form-label small fw-bold text-uppercase text-secondary mb-1" style={{ fontSize: '0.72rem', letterSpacing: '1px' }}>
                        Check-In Date
                      </label>
                      <input 
                        type="date" 
                        className="form-control rounded-pill px-3 py-2"
                        value={checkInFilter}
                        onChange={(e) => setCheckInFilter(e.target.value)}
                      />
                    </div>

                    <div className="col-lg-3 col-md-6">
                      <label className="form-label small fw-bold text-uppercase text-secondary mb-1" style={{ fontSize: '0.72rem', letterSpacing: '1px' }}>
                        Check-Out Date
                      </label>
                      <input 
                        type="date" 
                        className="form-control rounded-pill px-3 py-2"
                        value={checkOutFilter}
                        min={checkInFilter}
                        onChange={(e) => setCheckOutFilter(e.target.value)}
                      />
                    </div>

                    <div className="col-lg-2 col-md-4">
                      <label className="form-label small fw-bold text-uppercase text-secondary mb-1" style={{ fontSize: '0.72rem', letterSpacing: '1px' }}>
                        Guest Count
                      </label>
                      <select 
                        className="form-select rounded-pill px-3 py-2"
                        value={guestsFilter}
                        onChange={(e) => setGuestsFilter(e.target.value)}
                      >
                        <option value="">Any Guests</option>
                        <option value="1">1 Guest</option>
                        <option value="2">2 Guests</option>
                        <option value="3">3 Guests</option>
                        <option value="4">4 Guests</option>
                        <option value="5">5+ Guests</option>
                      </select>
                    </div>

                    <div className="col-lg-2 col-md-4">
                      <label className="form-label small fw-bold text-uppercase text-secondary mb-1" style={{ fontSize: '0.72rem', letterSpacing: '1px' }}>
                        Suite Category
                      </label>
                      <select 
                        className="form-select rounded-pill px-3 py-2"
                        value={roomTypeFilter}
                        onChange={(e) => setRoomTypeFilter(e.target.value)}
                      >
                        <option value="">All Suites & Villas</option>
                        <option value="Standard">Standard Queen</option>
                        <option value="Deluxe">Deluxe Double</option>
                        <option value="Suite">Ocean View Suite</option>
                        <option value="Executive">Executive King</option>
                        <option value="Presidential">Presidential Penthouse</option>
                        <option value="Family">Family Villa</option>
                      </select>
                    </div>

                    <div className="col-lg-2 col-md-4">
                      <button 
                        className="btn btn-luxury-dark w-100 py-2"
                        onClick={loadRooms}
                      >
                        Check Rates
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* ROOMS & SUITES SECTION */}
            <section className="py-5">
              <div className="container">
                <div className="d-flex flex-wrap justify-content-between align-items-end mb-4 pb-2 border-bottom">
                  <div>
                    <span className="boutique-tagline d-block mb-1">ACCOMMODATION</span>
                    <h3 className="brand-serif fw-bold text-dark fs-2 mb-0">Luxury Coastal Suites</h3>
                  </div>
                  <button 
                    className="btn btn-luxury-pill btn-sm d-flex align-items-center gap-1"
                    onClick={() => openOccupancyTracker(checkInFilter, checkOutFilter)}
                  >
                    <i className="bi bi-door-closed text-danger"></i> View Occupancy Tracker
                  </button>
                </div>

                {loadingRooms ? (
                  <div className="text-center py-5">
                    <div className="spinner-border text-warning" role="status"></div>
                    <p className="mt-2 text-muted small">Checking live room availability...</p>
                  </div>
                ) : (
                  <div className="row g-4">
                    {rooms.map((room) => {
                      const isOccupied = room.displayStatus === 'Occupied';

                      return (
                        <div key={room.roomId} className="col-md-6 col-lg-4">
                          <div className="card card-room h-100 position-relative">
                            
                            {/* Live Availability Badge */}
                            <span 
                              className={`position-absolute top-0 end-0 m-3 badge rounded-pill px-3 py-2 shadow-sm ${
                                isOccupied ? 'bg-danger text-white cursor-pointer' : 'bg-success text-white'
                              }`}
                              style={{ zIndex: 2, fontSize: '0.72rem', letterSpacing: '1px', cursor: isOccupied ? 'pointer' : 'default' }}
                              onClick={() => isOccupied && openOccupancyTracker(checkInFilter, checkOutFilter)}
                              title={isOccupied ? "Click to view occupancy records" : ""}
                            >
                              {isOccupied ? 'OCCUPIED' : 'AVAILABLE'}
                            </span>

                            {/* Room Image */}
                            <div className="overflow-hidden position-relative" style={{ height: '220px' }}>
                              <img 
                                src={getRoomImage(room.imageName)} 
                                alt={room.roomType} 
                                className="w-100 h-100 object-fit-cover"
                              />
                              <div 
                                className="position-absolute bottom-0 start-0 w-100 p-2 text-white"
                                style={{ background: 'linear-gradient(transparent, rgba(0,0,0,0.7))' }}
                              >
                                <span className="badge rounded-pill bg-dark bg-opacity-75">Room #{room.roomNumber}</span>
                                <span className="badge rounded-pill bg-secondary ms-1">Max {room.capacity} Guests</span>
                              </div>
                            </div>

                            {/* Card Content */}
                            <div className="card-body p-4 d-flex flex-column">
                              <div className="d-flex justify-content-between align-items-start mb-2">
                                <h5 className="brand-serif fw-bold text-dark fs-4 mb-0">{room.roomType}</h5>
                                <div className="text-end">
                                  <span className="fs-5 fw-bold brand-gold">LKR {Number(room.pricePerNight).toLocaleString()}</span>
                                  <small className="text-muted d-block" style={{ fontSize: '0.75rem' }}>/ night</small>
                                </div>
                              </div>

                              <p className="card-text text-secondary small mb-3 flex-grow-1" style={{ minHeight: '44px' }}>
                                {room.description}
                              </p>

                              <div className="small text-muted mb-3">
                                <i className="bi bi-gem text-warning me-1"></i>
                                {room.amenities}
                              </div>

                              <div className="pt-2 border-top mt-auto">
                                {isOccupied ? (
                                  <button 
                                    className="btn btn-outline-danger w-100 rounded-pill btn-sm py-2"
                                    onClick={() => openOccupancyTracker(checkInFilter, checkOutFilter)}
                                  >
                                    <i className="bi bi-calendar-x me-1"></i> View Occupancy Details
                                  </button>
                                ) : (
                                  <button 
                                    className="btn btn-luxury-dark w-100 btn-sm py-2"
                                    onClick={() => {
                                      if (!user) {
                                        setMessage('Please sign in or register to reserve a suite.');
                                        setShowLoginModal(true);
                                        return;
                                      }
                                      setSelectedRoom(room);
                                      setShowBookingModal(true);
                                    }}
                                  >
                                    Reserve Suite
                                  </button>
                                )}
                              </div>

                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </section>
          </div>
        )}

        {/* 2. ROOMS ONLY VIEW */}
        {activeTab === 'rooms' && (
          <section className="py-5">
            <div className="container">
              <div className="d-flex flex-wrap justify-content-between align-items-center mb-4 pb-2 border-bottom">
                <div>
                  <span className="boutique-tagline d-block mb-1">RESERVATIONS</span>
                  <h3 className="brand-serif fw-bold text-dark fs-2 mb-0">All Hotel Rooms & Suites</h3>
                </div>
                <div className="d-flex gap-2">
                  <button className="btn btn-luxury-pill btn-sm" onClick={() => openOccupancyTracker(checkInFilter, checkOutFilter)}>
                    <i className="bi bi-door-closed text-danger me-1"></i> View Occupied Rooms
                  </button>
                </div>
              </div>

              <div className="row g-4">
                {rooms.map((room) => {
                  const isOccupied = room.displayStatus === 'Occupied';
                  return (
                    <div key={room.roomId} className="col-md-6 col-lg-4">
                      <div className="card card-room h-100 position-relative">
                        <span 
                          className={`position-absolute top-0 end-0 m-3 badge rounded-pill px-3 py-2 ${
                            isOccupied ? 'bg-danger text-white cursor-pointer' : 'bg-success text-white'
                          }`}
                          style={{ zIndex: 2, cursor: isOccupied ? 'pointer' : 'default' }}
                          onClick={() => isOccupied && openOccupancyTracker(checkInFilter, checkOutFilter)}
                          title={isOccupied ? "Click to view occupancy records" : ""}
                        >
                          {isOccupied ? 'OCCUPIED' : 'AVAILABLE'}
                        </span>

                        <img 
                          src={getRoomImage(room.imageName)} 
                          alt={room.roomType} 
                          className="card-img-top object-fit-cover"
                          style={{ height: '210px' }}
                        />

                        <div className="card-body p-4 d-flex flex-column">
                          <div className="d-flex justify-content-between align-items-start mb-2">
                            <div>
                              <span className="badge rounded-pill bg-dark mb-1">Room #{room.roomNumber}</span>
                              <h5 className="brand-serif fw-bold text-dark fs-4 mb-0">{room.roomType}</h5>
                            </div>
                            <span className="fs-5 fw-bold brand-gold">LKR {Number(room.pricePerNight).toLocaleString()}</span>
                          </div>

                          <p className="card-text text-secondary small mb-3 flex-grow-1">
                            {room.description}
                          </p>

                          <div className="small text-muted mb-3">
                            <i className="bi bi-check2 text-success me-1"></i> {room.amenities}
                          </div>

                          <div className="pt-2 border-top mt-auto">
                            {isOccupied ? (
                              <button className="btn btn-outline-danger w-100 rounded-pill btn-sm" onClick={() => openOccupancyTracker(checkInFilter, checkOutFilter)}>
                                <i className="bi bi-calendar-x me-1"></i> View Occupied Details
                              </button>
                            ) : (
                              <button 
                                className="btn btn-luxury-dark w-100 btn-sm py-2"
                                onClick={() => {
                                  if (!user) {
                                    setMessage('Please sign in or register to reserve a suite.');
                                    setShowLoginModal(true);
                                    return;
                                  }
                                  setSelectedRoom(room);
                                  setShowBookingModal(true);
                                }}
                              >
                                Reserve Room
                              </button>
                            )}
                          </div>
                        </div>

                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </section>
        )}

        {/* 3. OCCUPIED ROOMS TRACKER */}
        {activeTab === 'occupied' && (
          <section className="py-5" style={{ backgroundColor: '#fcfbf8' }}>
            <div className="container">
              
              {/* Header & Controls */}
              <div className="d-flex flex-wrap justify-content-between align-items-center mb-4 pb-3 border-bottom gap-3">
                <div>
                  <span className="boutique-tagline d-block mb-1">FRONT DESK & OCCUPANCY</span>
                  <h3 className="brand-serif fw-bold text-dark fs-2 mb-1">Occupied Rooms Tracker</h3>
                  <p className="text-muted small mb-0">
                    Real-time room occupancy and guest reservation records for Dutch Point Negombo.
                  </p>
                </div>

                {/* View Mode Switcher Pills */}
                <div className="d-flex align-items-center gap-2 bg-white p-1 rounded-pill shadow-sm border">
                  <button 
                    className={`btn btn-sm rounded-pill px-3 fw-bold ${occupancyViewMode === 'date' ? 'btn-luxury-dark text-white' : 'btn-light text-secondary'}`}
                    onClick={() => setOccupancyViewMode('date')}
                  >
                    <i className="bi bi-calendar-event me-1"></i> Filter by Date
                  </button>
                  <button 
                    className={`btn btn-sm rounded-pill px-3 fw-bold ${occupancyViewMode === 'all' ? 'btn-luxury-dark text-white' : 'btn-light text-secondary'}`}
                    onClick={() => {
                      setOccupancyViewMode('all');
                      loadAllActiveBookings();
                    }}
                  >
                    <i className="bi bi-card-checklist me-1"></i> All Active Bookings ({allActiveBookings.length})
                  </button>
                </div>
              </div>

              {/* Mode A: Filter by Specific Date */}
              {occupancyViewMode === 'date' && (
                <div>
                  {/* Date Filter Toolbar & Quick Presets */}
                  <div className="card border-0 shadow-sm rounded-4 p-3 mb-4 bg-white">
                    <div className="d-flex flex-wrap justify-content-between align-items-center gap-3">
                      <div className="d-flex align-items-center gap-2">
                        <label className="small fw-bold text-secondary mb-0">Select Target Date:</label>
                        <input 
                          type="date" 
                          className="form-control form-control-sm rounded-pill px-3 border shadow-sm"
                          style={{ width: '180px' }}
                          value={occupiedDate}
                          onChange={(e) => {
                            setOccupiedDate(e.target.value);
                            loadOccupiedRooms(e.target.value);
                          }}
                        />
                      </div>

                      {/* Quick Sync Buttons */}
                      <div className="d-flex flex-wrap align-items-center gap-2">
                        <span className="text-muted small">Quick Sync:</span>
                        <button 
                          className="btn btn-outline-primary btn-sm rounded-pill px-3"
                          onClick={() => {
                            setOccupiedDate(checkInFilter);
                            loadOccupiedRooms(checkInFilter, checkOutFilter);
                          }}
                        >
                          <i className="bi bi-arrow-repeat me-1"></i> Search Dates ({checkInFilter} to {checkOutFilter})
                        </button>
                        <button 
                          className="btn btn-outline-secondary btn-sm rounded-pill px-3"
                          onClick={() => {
                            const today = new Date().toISOString().split('T')[0];
                            setOccupiedDate(today);
                            loadOccupiedRooms(today);
                          }}
                        >
                          Today
                        </button>
                      </div>
                    </div>

                    {/* Active Target Date Alert */}
                    <div className="mt-3 pt-2 border-top d-flex justify-content-between align-items-center">
                      <span className="small text-secondary">
                        <i className="bi bi-clock-history text-warning me-1"></i>
                        Showing Occupancy for: <strong className="text-dark">{occupiedTargetLabel || occupiedDate}</strong>
                      </span>
                      <span className={`badge rounded-pill px-3 py-2 ${occupiedRooms.length > 0 ? 'bg-danger' : 'bg-success'}`}>
                        {occupiedRooms.length > 0 ? `${occupiedRooms.length} Occupied Suite(s)` : '0 Occupied Suites (Vacant)'}
                      </span>
                    </div>
                  </div>

                  {/* Occupancy Results */}
                  {loadingOccupancy ? (
                    <div className="text-center py-5">
                      <div className="spinner-border text-primary" role="status"></div>
                      <p className="mt-2 text-muted small">Fetching occupancy data...</p>
                    </div>
                  ) : occupiedRooms.length === 0 ? (
                    <div className="card border-0 shadow-sm rounded-4 text-center py-5 bg-white">
                      <i className="bi bi-shield-check text-success fs-1 mb-2"></i>
                      <h5 className="brand-serif fw-bold text-dark fs-3">No Occupied Rooms on {occupiedDate}</h5>
                      <p className="text-muted small mb-3 max-w-500 mx-auto">
                        All suites are currently vacant on this specific date. If you booked for another date (such as <strong>{checkInFilter}</strong>), click below to check that date, or view all active reservations.
                      </p>
                      <div className="d-flex justify-content-center gap-2">
                        <button 
                          className="btn btn-luxury-dark btn-sm px-4" 
                          onClick={() => {
                            setOccupiedDate(checkInFilter);
                            loadOccupiedRooms(checkInFilter, checkOutFilter);
                          }}
                        >
                          Check Search Dates ({checkInFilter})
                        </button>
                        <button 
                          className="btn btn-outline-secondary btn-sm px-4" 
                          onClick={() => {
                            setOccupancyViewMode('all');
                            loadAllActiveBookings();
                          }}
                        >
                          View All Active Bookings ({allActiveBookings.length})
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="row g-4">
                      {occupiedRooms.map((occ) => (
                        <div key={occ.bookingId} className="col-md-6 col-lg-4">
                          <div className="card card-room h-100 position-relative shadow-sm border-0 rounded-4 overflow-hidden">
                            <span className="position-absolute top-0 end-0 m-3 badge rounded-pill bg-danger text-white px-3 py-2 shadow-sm" style={{ zIndex: 2 }}>
                              <i className="bi bi-lock-fill me-1"></i> OCCUPIED
                            </span>

                            <img 
                              src={getRoomImage(occ.imageName)} 
                              alt={occ.roomType} 
                              className="card-img-top object-fit-cover"
                              style={{ height: '180px' }}
                            />

                            <div className="card-body p-4 d-flex flex-column">
                              <div className="d-flex justify-content-between align-items-center mb-1">
                                <span className="badge rounded-pill bg-dark">Room #{occ.roomNumber}</span>
                                <span className="badge rounded-pill bg-light text-secondary border">#RES-{occ.bookingId}</span>
                              </div>
                              <h5 className="brand-serif fw-bold text-dark fs-4 mb-2">{occ.roomType}</h5>

                              <div className="p-3 rounded-3 small mb-3" style={{ backgroundColor: '#f8fafc' }}>
                                <div className="fw-bold text-secondary mb-1">Occupying Guest:</div>
                                <div className="text-dark fw-bold fs-6">{occ.customerName}</div>
                                <div className="text-muted"><i className="bi bi-envelope me-1"></i>{occ.customerEmail || 'N/A'}</div>
                                <div className="text-muted"><i className="bi bi-telephone me-1"></i>{occ.customerPhone || 'N/A'}</div>
                              </div>

                              <div className="d-flex justify-content-between p-2 rounded-3 border small bg-white mb-3">
                                <div>
                                  <span className="text-muted d-block" style={{ fontSize: '0.75rem' }}>Check-In</span>
                                  <strong>{occ.checkInDate ? occ.checkInDate.split('T')[0] : 'N/A'}</strong>
                                </div>
                                <div className="text-end">
                                  <span className="text-muted d-block" style={{ fontSize: '0.75rem' }}>Check-Out</span>
                                  <strong>{occ.checkOutDate ? occ.checkOutDate.split('T')[0] : 'N/A'}</strong>
                                </div>
                              </div>

                              <div className="mt-auto pt-2 border-top d-flex justify-content-between align-items-center">
                                <span className="small text-muted">Total Paid / Rate:</span>
                                <strong className="brand-gold fs-6">LKR {Number(occ.totalAmount).toLocaleString()}</strong>
                              </div>

                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Mode B: All Active Reservations Roster */}
              {occupancyViewMode === 'all' && (
                <div>
                  <div className="card border-0 shadow-sm rounded-4 p-3 mb-4 bg-white">
                    <div className="d-flex flex-wrap justify-content-between align-items-center gap-2">
                      <div>
                        <h6 className="fw-bold mb-0 text-dark">
                          <i className="bi bi-card-checklist text-primary me-2"></i>
                          Resort Reservation Roster
                        </h6>
                        <span className="text-muted small">
                          Displaying all active and confirmed bookings stored in the MySQL database.
                        </span>
                      </div>
                      <button 
                        className="btn btn-outline-secondary btn-sm rounded-pill px-3"
                        onClick={loadAllActiveBookings}
                      >
                        <i className="bi bi-arrow-repeat me-1"></i> Refresh List
                      </button>
                    </div>
                  </div>

                  {allActiveBookings.length === 0 ? (
                    <div className="card border-0 shadow-sm rounded-4 text-center py-5 bg-white">
                      <i className="bi bi-inbox text-muted fs-1 mb-2"></i>
                      <h5 className="brand-serif fw-bold text-dark fs-3">No Active Bookings in System</h5>
                      <p className="text-muted small mb-0">No confirmed reservations currently exist in the database.</p>
                    </div>
                  ) : (
                    <div className="row g-4">
                      {allActiveBookings.map((b) => (
                        <div key={b.bookingId} className="col-md-6 col-lg-4">
                          <div className="card card-room h-100 position-relative shadow-sm border-0 rounded-4 overflow-hidden">
                            <span className="position-absolute top-0 end-0 m-3 badge rounded-pill bg-success text-white px-3 py-2 shadow-sm" style={{ zIndex: 2 }}>
                              <i className="bi bi-check-circle-fill me-1"></i> {b.bookingStatus}
                            </span>

                            <img 
                              src={getRoomImage(b.imageName)} 
                              alt={b.roomType} 
                              className="card-img-top object-fit-cover"
                              style={{ height: '170px' }}
                            />

                            <div className="card-body p-4 d-flex flex-column">
                              <div className="d-flex justify-content-between align-items-center mb-1">
                                <span className="badge rounded-pill bg-dark">Room #{b.roomNumber}</span>
                                <span className="badge rounded-pill bg-light text-secondary border">#RES-{b.bookingId}</span>
                              </div>
                              <h5 className="brand-serif fw-bold text-dark fs-5 mb-2">{b.roomType}</h5>

                              <div className="p-3 rounded-3 small mb-3" style={{ backgroundColor: '#f8fafc' }}>
                                <div className="fw-bold text-secondary mb-1">Guest Information:</div>
                                <div className="text-dark fw-bold fs-6">{b.customerName}</div>
                                <div className="text-muted"><i className="bi bi-telephone me-1"></i>{b.customerPhone || 'N/A'}</div>
                                <div className="text-muted"><i className="bi bi-people me-1"></i>{b.numberOfGuests} Guest(s)</div>
                              </div>

                              <div className="d-flex justify-content-between p-2 rounded-3 border small bg-white mb-3">
                                <div>
                                  <span className="text-muted d-block" style={{ fontSize: '0.75rem' }}>Check-In</span>
                                  <strong>{b.checkInDate ? b.checkInDate.split('T')[0] : 'N/A'}</strong>
                                </div>
                                <div className="text-end">
                                  <span className="text-muted d-block" style={{ fontSize: '0.75rem' }}>Check-Out</span>
                                  <strong>{b.checkOutDate ? b.checkOutDate.split('T')[0] : 'N/A'}</strong>
                                </div>
                              </div>

                              <div className="d-flex justify-content-between align-items-center mb-3">
                                <span className="small text-muted">Total Amount:</span>
                                <strong className="brand-gold fs-5">LKR {Number(b.totalAmount).toLocaleString()}</strong>
                              </div>

                              <button 
                                className="btn btn-outline-primary btn-sm rounded-pill w-100 mt-auto"
                                onClick={() => {
                                  const cIn = b.checkInDate ? b.checkInDate.split('T')[0] : '2026-10-10';
                                  const cOut = b.checkOutDate ? b.checkOutDate.split('T')[0] : '2026-10-15';
                                  setOccupiedDate(cIn);
                                  setOccupancyViewMode('date');
                                  loadOccupiedRooms(cIn, cOut);
                                }}
                              >
                                <i className="bi bi-search me-1"></i> Focus On This Reservation Date
                              </button>

                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

            </div>
          </section>
        )}

        {/* 4. MY BOOKINGS VIEW */}
        {activeTab === 'my-bookings' && (
          <section className="py-5">
            <div className="container">
              <div className="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom">
                <div>
                  <span className="boutique-tagline d-block mb-1">GUEST PORTAL</span>
                  <h3 className="brand-serif fw-bold text-dark fs-2 mb-0">My Hotel Reservations</h3>
                </div>
                <button className="btn btn-luxury-dark btn-sm" onClick={() => setActiveTab('rooms')}>
                  Book Another Suite
                </button>
              </div>

              {myBookings.length === 0 ? (
                <div className="card border-0 shadow-sm rounded-4 text-center py-5 bg-light">
                  <h5 className="brand-serif fw-bold text-dark fs-3 mb-2">No Active Reservations</h5>
                  <p className="text-muted small mb-3">You do not have any room bookings under this account.</p>
                  <div>
                    <button className="btn btn-luxury-dark btn-sm px-4" onClick={() => setActiveTab('rooms')}>
                      Explore Luxury Suites
                    </button>
                  </div>
                </div>
              ) : (
                <div className="row g-4">
                  {myBookings.map((b) => (
                    <div key={b.bookingId} className="col-md-6 col-lg-4">
                      <div className="card card-room h-100">
                        <img 
                          src={getRoomImage(b.imageName)} 
                          alt={b.roomType} 
                          className="card-img-top object-fit-cover"
                          style={{ height: '170px' }}
                        />
                        <div className="card-body p-4">
                          <div className="d-flex justify-content-between align-items-start mb-1">
                            <h5 className="brand-serif fw-bold text-dark fs-4 mb-0">{b.roomType}</h5>
                            <span className={`badge rounded-pill ${b.bookingStatus === 'Confirmed' ? 'bg-primary' : 'bg-secondary'}`}>
                              {b.bookingStatus}
                            </span>
                          </div>
                          <small className="text-muted d-block mb-3">Room #{b.roomNumber}</small>

                          <div className="p-3 bg-light rounded-3 small mb-3">
                            <div className="d-flex justify-content-between mb-1">
                              <span>Stay Dates:</span>
                              <span className="fw-semibold text-dark">{b.checkInDate} to {b.checkOutDate}</span>
                            </div>
                            <div className="d-flex justify-content-between mb-1">
                              <span>Guest Count:</span>
                              <span className="fw-semibold text-dark">{b.numberOfGuests} {b.numberOfGuests === 1 ? 'Guest' : 'Guests'}</span>
                            </div>
                            <div className="d-flex justify-content-between border-top pt-1 mt-1 fs-6 fw-bold">
                              <span>Total Amount:</span>
                              <span className="brand-gold">LKR {Number(b.totalAmount).toLocaleString()}</span>
                            </div>
                          </div>

                          <button 
                            className="btn btn-warning btn-sm w-100 rounded-pill mb-2 fw-semibold text-dark shadow-sm"
                            onClick={() => {
                              setSelectedBookingForPayment(b);
                              setShowPaymentModal(true);
                            }}
                          >
                            💳 Pay with Card
                          </button>

                          {b.bookingStatus === 'Confirmed' && (
                            <button 
                              className="btn btn-outline-danger btn-sm w-100 rounded-pill"
                              onClick={() => handleCancelBooking(b.bookingId)}
                            >
                              Cancel Reservation
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>
        )}

        {/* 5. INVENTORY MANAGEMENT (Admin) */}
        {activeTab === 'admin-rooms' && (
          <section className="py-5" style={{ backgroundColor: '#fcfbf8' }}>
            <div className="container">
              <span className="boutique-tagline d-block mb-1">ADMINISTRATOR</span>
              <h3 className="brand-serif fw-bold text-dark fs-2 mb-4">Room Inventory Management</h3>

              {/* Add Room Card */}
              <div className="card border-0 shadow-sm rounded-4 p-4 bg-white mb-4">
                <h5 className="brand-serif fw-bold mb-3">Add New Suite / Villa</h5>
                <form onSubmit={handleAddRoom}>
                  <div className="row g-2 mb-3">
                    <div className="col-md-3">
                      <label className="form-label small fw-semibold text-secondary">Room Number</label>
                      <input 
                        type="text" 
                        className="form-control rounded-pill px-3" 
                        required 
                        placeholder="e.g. 401"
                        value={newRoomNumber}
                        onChange={(e) => setNewRoomNumber(e.target.value)}
                      />
                    </div>
                    <div className="col-md-3">
                      <label className="form-label small fw-semibold text-secondary">Room Type</label>
                      <input 
                        type="text" 
                        className="form-control rounded-pill px-3" 
                        required 
                        value={newRoomType}
                        onChange={(e) => setNewRoomType(e.target.value)}
                      />
                    </div>
                    <div className="col-md-3">
                      <label className="form-label small fw-semibold text-secondary">Price / Night (LKR)</label>
                      <input 
                        type="number" 
                        step="100" 
                        className="form-control rounded-pill px-3" 
                        required 
                        value={newRoomPrice}
                        onChange={(e) => setNewRoomPrice(e.target.value)}
                      />
                    </div>
                    <div className="col-md-3">
                      <label className="form-label small fw-semibold text-secondary">Capacity</label>
                      <input 
                        type="number" 
                        className="form-control rounded-pill px-3" 
                        required 
                        value={newRoomCapacity}
                        onChange={(e) => setNewRoomCapacity(e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="row g-2 mb-3">
                    <div className="col-md-6">
                      <label className="form-label small fw-semibold text-secondary">Amenities</label>
                      <input 
                        type="text" 
                        className="form-control rounded-pill px-3" 
                        value={newRoomAmenities}
                        onChange={(e) => setNewRoomAmenities(e.target.value)}
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-semibold text-secondary">Photo Asset</label>
                      <select 
                        className="form-select rounded-pill px-3"
                        value={newRoomImage}
                        onChange={(e) => setNewRoomImage(e.target.value)}
                      >
                        <option value="room_suite.jpg">Ocean View Suite</option>
                        <option value="room_deluxe.jpg">Deluxe Double</option>
                        <option value="room_standard.jpg">Standard Queen</option>
                        <option value="room_executive.jpg">Executive King Suite</option>
                        <option value="room_presidential.jpg">Presidential Penthouse</option>
                        <option value="room_family.jpg">Family Villa</option>
                      </select>
                    </div>
                  </div>

                  <button type="submit" className="btn btn-luxury-dark btn-sm px-4">
                    Save Room to Database
                  </button>
                </form>
              </div>

              {/* Table of rooms */}
              <div className="table-responsive bg-white rounded-4 shadow-sm border">
                <table className="table table-hover align-middle mb-0">
                  <thead className="table-light small">
                    <tr>
                      <th>Room #</th>
                      <th>Suite Type</th>
                      <th>Nightly Rate</th>
                      <th>Capacity</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rooms.map((r) => (
                      <tr key={r.roomId}>
                        <td className="fw-bold">#{r.roomNumber}</td>
                        <td className="fw-semibold">{r.roomType}</td>
                        <td className="brand-gold fw-bold">LKR {Number(r.pricePerNight).toLocaleString()}</td>
                        <td>{r.capacity} Guests</td>
                        <td>
                          <span className={`badge rounded-pill ${r.displayStatus === 'Occupied' ? 'bg-danger' : 'bg-success'}`}>
                            {r.displayStatus || r.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

            </div>
          </section>
        )}

        {/* 6. ADMIN DASHBOARD & MANAGEMENT REPORTS */}
        {activeTab === 'admin-dashboard' && user?.role === 'Admin' && (
          <section className="py-5" style={{ backgroundColor: '#fcfbf8' }}>
            <div className="container">
              {/* Header */}
              <div className="d-flex flex-wrap justify-content-between align-items-center mb-4">
                <div>
                  <span className="boutique-tagline d-block mb-1">EXECUTIVE OVERVIEW</span>
                  <h3 className="brand-serif fw-bold text-dark fs-2 mb-0">Management Reports & Financials</h3>
                </div>
                <button 
                  className="btn btn-sm btn-outline-dark rounded-pill px-3 py-1"
                  onClick={loadAdminDashboard}
                  disabled={loadingDashboard}
                >
                  <i className={`bi ${loadingDashboard ? 'bi-arrow-repeat' : 'bi-arrow-clockwise'} me-1`}></i>
                  {loadingDashboard ? 'Updating...' : 'Refresh Data'}
                </button>
              </div>

              {/* 3 Simple Metric Cards */}
              <div className="row g-4 mb-4">
                {/* 1. Total Revenue */}
                <div className="col-md-4">
                  <div className="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
                    <div className="d-flex align-items-center justify-content-between mb-2">
                      <span className="small text-muted text-uppercase fw-semibold" style={{ letterSpacing: '1px' }}>Total Revenue</span>
                      <div className="p-2 rounded-circle bg-light text-warning">
                        <i className="bi bi-cash-stack fs-5"></i>
                      </div>
                    </div>
                    <h3 className="brand-gold fw-bold mb-1 fs-2">
                      LKR {Number(dashboardStats?.totalRevenue || 0).toLocaleString()}
                    </h3>
                    <p className="text-secondary small mb-0">Total revenue generated from confirmed reservations</p>
                  </div>
                </div>

                {/* 2. Total Reservations */}
                <div className="col-md-4">
                  <div className="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
                    <div className="d-flex align-items-center justify-content-between mb-2">
                      <span className="small text-muted text-uppercase fw-semibold" style={{ letterSpacing: '1px' }}>Total Reservations</span>
                      <div className="p-2 rounded-circle bg-light text-primary">
                        <i className="bi bi-calendar2-check fs-5"></i>
                      </div>
                    </div>
                    <h3 className="brand-serif fw-bold text-dark mb-1 fs-2">
                      {dashboardStats?.totalBookings ?? 0}
                    </h3>
                    <p className="text-secondary small mb-0">Cumulative guest bookings processed by the system</p>
                  </div>
                </div>

                {/* 3. Registered Guests */}
                <div className="col-md-4">
                  <div className="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
                    <div className="d-flex align-items-center justify-content-between mb-2">
                      <span className="small text-muted text-uppercase fw-semibold" style={{ letterSpacing: '1px' }}>Registered Guests</span>
                      <div className="p-2 rounded-circle bg-light text-success">
                        <i className="bi bi-people fs-5"></i>
                      </div>
                    </div>
                    <h3 className="brand-serif fw-bold text-dark mb-1 fs-2">
                      {dashboardStats?.totalCustomers ?? 0}
                    </h3>
                    <p className="text-secondary small mb-0">Active customer accounts</p>
                  </div>
                </div>
              </div>

              {/* Card Payment Transactions Audit Table */}
              <div className="card border-0 shadow-sm rounded-4 p-4 bg-white">
                <div className="d-flex flex-wrap justify-content-between align-items-center mb-3">
                  <div>
                    <h5 className="brand-serif fw-bold text-dark mb-1">Card Payment Transactions</h5>
                    <p className="text-muted small mb-0">Verified electronic transactions and  audit logs</p>
                  </div>
                  <span className="badge rounded-pill bg-light text-dark border px-3 py-2 small">
                    {adminPayments.length} Payment{adminPayments.length === 1 ? '' : 's'}
                  </span>
                </div>

                {loadingDashboard ? (
                  <div className="text-center py-5">
                    <div className="spinner-border text-warning" role="status"></div>
                    <p className="small text-muted mt-2">Loading transactions...</p>
                  </div>
                ) : adminPayments.length === 0 ? (
                  <div className="text-center py-5 border rounded-3 bg-light">
                    <i className="bi bi-credit-card-2-front text-muted fs-1 mb-2 d-block"></i>
                    <p className="text-muted mb-0">No card transactions recorded yet.</p>
                  </div>
                ) : (
                  <div className="table-responsive">
                    <table className="table table-hover align-middle mb-0">
                      <thead className="table-light small">
                        <tr>
                          <th>Transaction ID</th>
                          <th>Guest Name</th>
                          <th>Card Used</th>
                          <th>Amount (LKR)</th>
                          <th>Date & Time</th>
                          <th>Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {adminPayments.map((p) => {
                          const txId = p.transactionId || p.TransactionId || `TXN-${p.paymentId || p.PaymentId}`;
                          const guestName = p.booking?.customer?.fullName || p.Booking?.Customer?.FullName || 'Guest';
                          const guestEmail = p.booking?.customer?.email || p.Booking?.Customer?.Email || '';
                          const card = p.maskedCardNumber || p.MaskedCardNumber || '**** 4242';
                          const amount = p.amount ?? p.Amount ?? 0;
                          const date = p.paymentDate || p.PaymentDate;
                          const status = p.paymentStatus || p.PaymentStatus || 'Completed';

                          return (
                            <tr key={p.paymentId || p.PaymentId || txId}>
                              <td>
                                <code className="text-dark fw-bold bg-light px-2 py-1 rounded border">
                                  {txId}
                                </code>
                              </td>
                              <td>
                                <div className="fw-semibold text-dark">{guestName}</div>
                                {guestEmail && (
                                  <div className="text-muted small" style={{ fontSize: '0.75rem' }}>{guestEmail}</div>
                                )}
                              </td>
                              <td>
                                <span className="badge bg-light text-dark border rounded-pill px-2 py-1">
                                  <i className="bi bi-credit-card me-1"></i>{card}
                                </span>
                              </td>
                              <td className="brand-gold fw-bold">
                                LKR {Number(amount).toLocaleString()}
                              </td>
                              <td className="small text-secondary">
                                {date ? new Date(date).toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' }) : 'N/A'}
                              </td>
                              <td>
                                <span className="badge rounded-pill bg-success-subtle text-success border border-success-subtle px-3 py-1">
                                  <i className="bi bi-check-circle-fill me-1"></i>{status}
                                </span>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>

            </div>
          </section>
        )}

        {/* 7. DINING SECTION */}
        {activeTab === 'dining' && (
          <section className="py-5" style={{ backgroundColor: '#fcfbf8' }}>
            <div className="container">
              <div className="text-center mb-5">
                <span className="boutique-tagline d-block mb-1">COASTAL GASTRONOMY & FINE DRINKS</span>
                <h3 className="brand-serif fw-bold text-dark fs-2 mb-2">Dining at Dutch Point Negombo</h3>
                <p className="text-muted mx-auto" style={{ maxWidth: '650px' }}>
                  Indulge in the finest culinary offerings of Sri Lanka's western coast. Savor fresh catch from the Negombo lagoon, aromatic Ceylon spices, and international culinary classics prepared by our master chefs.
                </p>
              </div>

              <div className="row g-4 mb-5">
                {/* Restaurant 1 */}
                <div className="col-lg-4 col-md-6">
                  <div className="card h-100 border-0 shadow-sm rounded-4 overflow-hidden bg-white">
                    <div style={{ height: '220px', overflow: 'hidden' }}>
                      <img src={images.beachView} alt="The Cinnamon Coast Seafood Grill" className="w-100 h-100" style={{ objectFit: 'cover' }} />
                    </div>
                    <div className="card-body p-4 d-flex flex-column">
                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <span className="badge rounded-pill bg-warning text-dark small fw-semibold">BEACHFRONT GRILL</span>
                        <small className="text-muted"><i className="bi bi-clock me-1"></i>12:00 PM – 11:00 PM</small>
                      </div>
                      <h5 className="brand-serif fw-bold text-dark mb-2">The Cinnamon Coast Seafood Grill</h5>
                      <p className="text-secondary small flex-grow-1">
                        Located directly on the sands, offering wild-caught Negombo lagoon mud crabs, giant tiger prawns, grilled red snapper, and flame-grilled lobsters seasoned with Ceylon lemongrass and pepper.
                      </p>
                      <div className="border-top pt-3 mt-auto">
                        <span className="small text-muted d-block mb-2"><i className="bi bi-geo-alt me-1 text-danger"></i> Beachfront Pavilion</span>
                        <a href="https://wa.me/94770000000?text=Hi%20Dutch%20Point,%20I%20would%20like%20to%20reserve%20a%20table%20at%20The%20Cinnamon%20Coast%20Seafood%20Grill" target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-luxury-dark w-100 rounded-pill">
                          Reserve a Table
                        </a>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Restaurant 2 */}
                <div className="col-lg-4 col-md-6">
                  <div className="card h-100 border-0 shadow-sm rounded-4 overflow-hidden bg-white">
                    <div style={{ height: '220px', overflow: 'hidden' }}>
                      <img src={images.resortNight} alt="Dutch Fort Colonial Lounge & Bar" className="w-100 h-100" style={{ objectFit: 'cover' }} />
                    </div>
                    <div className="card-body p-4 d-flex flex-column">
                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <span className="badge rounded-pill bg-dark text-white small fw-semibold">HERITAGE LOUNGE & BAR</span>
                        <small className="text-muted"><i className="bi bi-clock me-1"></i>4:00 PM – 1:00 AM</small>
                      </div>
                      <h5 className="brand-serif fw-bold text-dark mb-2">Dutch Fort Colonial Lounge & Bar</h5>
                      <p className="text-secondary small flex-grow-1">
                        Sip on signature Ceylon arrack cocktails, imported single malts, and vintage wines under colonial Dutch archways. Featuring live evening acoustic jazz and panoramic ocean breezes.
                      </p>
                      <div className="border-top pt-3 mt-auto">
                        <span className="small text-muted d-block mb-2"><i className="bi bi-geo-alt me-1 text-danger"></i> Main Courtyard</span>
                        <a href="https://wa.me/94770000000?text=Hi%20Dutch%20Point,%20I%20would%20like%20to%20inquire%20about%20Dutch%20Fort%20Lounge" target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-luxury-dark w-100 rounded-pill">
                          View Cocktail Menu
                        </a>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Restaurant 3 */}
                <div className="col-lg-4 col-md-6">
                  <div className="card h-100 border-0 shadow-sm rounded-4 overflow-hidden bg-white">
                    <div style={{ height: '220px', overflow: 'hidden' }}>
                      <img src={images.balconyView} alt="The Palms Sunrise Terrace" className="w-100 h-100" style={{ objectFit: 'cover' }} />
                    </div>
                    <div className="card-body p-4 d-flex flex-column">
                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <span className="badge rounded-pill bg-success text-white small fw-semibold">ALL-DAY BREAKFAST</span>
                        <small className="text-muted"><i className="bi bi-clock me-1"></i>6:30 AM – 11:30 AM</small>
                      </div>
                      <h5 className="brand-serif fw-bold text-dark mb-2">The Palms Sunrise Terrace</h5>
                      <p className="text-secondary small flex-grow-1">
                        Start your day overlooking the sparkling Indian Ocean with our tropical breakfast buffet. Enjoy organic tropical fruits, artisan French croissants, and traditional Sri Lankan egg hoppers and sambols.
                      </p>
                      <div className="border-top pt-3 mt-auto">
                        <span className="small text-muted d-block mb-2"><i className="bi bi-geo-alt me-1 text-danger"></i> Ocean View Mezzanine</span>
                        <button className="btn btn-sm btn-outline-dark w-100 rounded-pill" onClick={() => setActiveTab('rooms')}>
                          Included with Suites
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* In-Room Dining Banner */}
              <div className="card border-0 rounded-4 p-4 text-white shadow-sm" style={{ backgroundColor: '#0b1320' }}>
                <div className="row align-items-center">
                  <div className="col-md-8">
                    <span className="badge rounded-pill bg-warning text-dark mb-2">24/7 LUXURY SERVICE</span>
                    <h4 className="brand-serif fw-bold mb-1">In-Suite Private Dining & Room Service</h4>
                    <p className="small text-white-50 mb-0">
                      Private balcony candlelight dinners, champagne breakfasts, or midnight tapas delivered straight to your suite or villa. Simply dial <strong>Ext. 104</strong> from your room phone.
                    </p>
                  </div>
                  <div className="col-md-4 text-md-end mt-3 mt-md-0">
                    <a href="tel:+94312234567" className="btn btn-luxury-pill btn-light btn-sm px-4 py-2">
                      <i className="bi bi-telephone-fill me-1"></i> Call Room Service
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* 8. GALLERY SECTION */}
        {activeTab === 'gallery' && (
          <section className="py-5" style={{ backgroundColor: '#fcfbf8' }}>
            <div className="container">
              <div className="text-center mb-4">
                <span className="boutique-tagline d-block mb-1">MOMENTS OF TRANQUILITY</span>
                <h3 className="brand-serif fw-bold text-dark fs-2 mb-2">Resort Visual Gallery</h3>
                <p className="text-muted mx-auto" style={{ maxWidth: '600px' }}>
                  Explore the architecture, luxury suites, pristine beachfront, and tropical ambiance of Dutch Point Negombo.
                </p>

                {/* Filter Pills */}
                <div className="d-flex justify-content-center gap-2 mt-3">
                  <button 
                    className={`btn btn-sm rounded-pill px-3 ${galleryFilter === 'all' ? 'btn-dark' : 'btn-outline-secondary'}`}
                    onClick={() => setGalleryFilter('all')}
                  >
                    All Photos
                  </button>
                  <button 
                    className={`btn btn-sm rounded-pill px-3 ${galleryFilter === 'suites' ? 'btn-dark' : 'btn-outline-secondary'}`}
                    onClick={() => setGalleryFilter('suites')}
                  >
                    Suites & Villas
                  </button>
                  <button 
                    className={`btn btn-sm rounded-pill px-3 ${galleryFilter === 'views' ? 'btn-dark' : 'btn-outline-secondary'}`}
                    onClick={() => setGalleryFilter('views')}
                  >
                    Beach & Grounds
                  </button>
                </div>
              </div>

              {/* Gallery Grid */}
              <div className="row g-3">
                {(galleryFilter === 'all' || galleryFilter === 'views') && (
                  <>
                    <div className="col-md-6 col-lg-4">
                      <div className="card border-0 shadow-sm rounded-4 overflow-hidden h-100">
                        <img src={images.hero} alt="Resort Panorama" className="w-100" style={{ height: '260px', objectFit: 'cover' }} />
                        <div className="p-3 bg-white">
                          <span className="small fw-bold text-dark d-block">Panoramic Ocean Pool & Beachfront</span>
                          <small className="text-muted">Resort Grounds • Negombo Coast</small>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-6 col-lg-4">
                      <div className="card border-0 shadow-sm rounded-4 overflow-hidden h-100">
                        <img src={images.beachView} alt="Golden Beachfront" className="w-100" style={{ height: '260px', objectFit: 'cover' }} />
                        <div className="p-3 bg-white">
                          <span className="small fw-bold text-dark d-block">Pristine Golden Shoreline</span>
                          <small className="text-muted">Direct Private Beach Access</small>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-6 col-lg-4">
                      <div className="card border-0 shadow-sm rounded-4 overflow-hidden h-100">
                        <img src={images.resortNight} alt="Night Atmosphere" className="w-100" style={{ height: '260px', objectFit: 'cover' }} />
                        <div className="p-3 bg-white">
                          <span className="small fw-bold text-dark d-block">Midnight Illuminated Pool Deck</span>
                          <small className="text-muted">Courtyard & Lounge Ambiance</small>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-6 col-lg-4">
                      <div className="card border-0 shadow-sm rounded-4 overflow-hidden h-100">
                        <img src={images.balconyView} alt="Balcony Sunset" className="w-100" style={{ height: '260px', objectFit: 'cover' }} />
                        <div className="p-3 bg-white">
                          <span className="small fw-bold text-dark d-block">Private Balcony Sunset Perspective</span>
                          <small className="text-muted">Upper Deck Suites</small>
                        </div>
                      </div>
                    </div>
                  </>
                )}

                {(galleryFilter === 'all' || galleryFilter === 'suites') && (
                  <>
                    <div className="col-md-6 col-lg-4">
                      <div className="card border-0 shadow-sm rounded-4 overflow-hidden h-100">
                        <img src={images['room_suite.jpg']} alt="Ocean View Suite" className="w-100" style={{ height: '260px', objectFit: 'cover' }} />
                        <div className="p-3 bg-white">
                          <span className="small fw-bold text-dark d-block">Ocean View Suite Master Bedroom</span>
                          <small className="text-muted">King Canopy Bed & Ocean Facing Glazing</small>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-6 col-lg-4">
                      <div className="card border-0 shadow-sm rounded-4 overflow-hidden h-100">
                        <img src={images['room_presidential.jpg']} alt="Presidential Penthouse" className="w-100" style={{ height: '260px', objectFit: 'cover' }} />
                        <div className="p-3 bg-white">
                          <span className="small fw-bold text-dark d-block">Presidential Penthouse Suite</span>
                          <small className="text-muted">Jacuzzi, Butler Service & 360 View</small>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-6 col-lg-4">
                      <div className="card border-0 shadow-sm rounded-4 overflow-hidden h-100">
                        <img src={images['room_deluxe.jpg']} alt="Deluxe Double" className="w-100" style={{ height: '260px', objectFit: 'cover' }} />
                        <div className="p-3 bg-white">
                          <span className="small fw-bold text-dark d-block">Deluxe Double Suite</span>
                          <small className="text-muted">Floor-to-Ceiling Windows & Balcony</small>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-6 col-lg-4">
                      <div className="card border-0 shadow-sm rounded-4 overflow-hidden h-100">
                        <img src={images['room_family.jpg']} alt="Family Villa" className="w-100" style={{ height: '260px', objectFit: 'cover' }} />
                        <div className="p-3 bg-white">
                          <span className="small fw-bold text-dark d-block">Family Villa & Play Terrace</span>
                          <small className="text-muted">2 Interconnecting Bedrooms & Private Patio</small>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-6 col-lg-4">
                      <div className="card border-0 shadow-sm rounded-4 overflow-hidden h-100">
                        <img src={images['room_standard.jpg']} alt="Standard Queen" className="w-100" style={{ height: '260px', objectFit: 'cover' }} />
                        <div className="p-3 bg-white">
                          <span className="small fw-bold text-dark d-block">Standard Queen Room</span>
                          <small className="text-muted">Plush Queen Bed & Modern Ensuite</small>
                        </div>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </section>
        )}

        {/* 9. ABOUT US SECTION */}
        {activeTab === 'about' && (
          <section className="py-5" style={{ backgroundColor: '#fcfbf8' }}>
            <div className="container">
              {/* Header */}
              <div className="text-center mb-5">
                <span className="boutique-tagline d-block mb-1">OUR STORY & HERITAGE</span>
                <h3 className="brand-serif fw-bold text-dark fs-2 mb-2">Welcome to Dutch Point Negombo</h3>
                <p className="text-muted mx-auto" style={{ maxWidth: '650px' }}>
                  A coastal retreat inspired by centuries of maritime heritage, designed for tranquility and modern luxury.
                </p>
              </div>

              {/* Story 2-Column Banner */}
              <div className="card border-0 shadow-sm rounded-4 overflow-hidden bg-white p-4 p-lg-5 mb-5">
                <div className="row g-4 align-items-center">
                  <div className="col-lg-6">
                    <span className="badge rounded-pill bg-warning text-dark px-3 py-1 mb-3">ESTABLISHED ON PORUTOTA ROAD</span>
                    <h4 className="brand-serif fw-bold text-dark mb-3">Where Coastal Elegance Meets 17th-Century Dutch Heritage</h4>
                    <p className="text-secondary" style={{ lineHeight: '1.8' }}>
                      Nestled along the golden palm-fringed sands of Negombo, <strong>Dutch Point Negombo</strong> was conceived as an intimate sanctuary for travelers seeking escape from the ordinary. 
                    </p>
                    <p className="text-secondary" style={{ lineHeight: '1.8' }}>
                      Taking architectural cues from the historic Dutch colonial settlements of maritime Ceylon, our boutique resort combines grand arched verandas, terracotta finishes, and tropical teak wood with cutting-edge guest comfort.
                    </p>
                    <p className="text-secondary mb-0" style={{ lineHeight: '1.8' }}>
                      Whether you are visiting Sri Lanka for a coastal holiday, a romantic oceanfront getaway, or a peaceful stay near the international airport, our dedicated team is committed to providing warm, unhurried, authentic Sri Lankan hospitality.
                    </p>
                  </div>
                  <div className="col-lg-6">
                    <div className="position-relative rounded-4 overflow-hidden shadow-sm" style={{ height: '360px' }}>
                      <img src={images.hero} alt="Dutch Point Negombo Resort" className="w-100 h-100" style={{ objectFit: 'cover' }} />
                      <div className="position-absolute bottom-0 start-0 end-0 p-3 bg-dark bg-opacity-75 text-white">
                        <div className="d-flex justify-content-between align-items-center">
                          <div>
                            <span className="fw-bold d-block">Dutch Point Negombo Beachfront</span>
                            <small className="text-white-50">Porutota Road, Negombo, Sri Lanka</small>
                          </div>
                          <span className="badge bg-warning text-dark px-3 py-2 fw-bold">4.8 ★ Luxury Rating</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* 4 Pillars of Dutch Point */}
              <div className="row g-4 text-center">
                <div className="col-md-3">
                  <div className="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
                    <div className="fs-1 text-primary mb-2"><i className="bi bi-water"></i></div>
                    <h6 className="brand-serif fw-bold text-dark mb-2">Direct Ocean Access</h6>
                    <p className="text-secondary small mb-0">Step directly from your villa onto the pristine golden beach of Negombo.</p>
                  </div>
                </div>
                <div className="col-md-3">
                  <div className="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
                    <div className="fs-1 text-success mb-2"><i className="bi bi-tree"></i></div>
                    <h6 className="brand-serif fw-bold text-dark mb-2">Eco-Conscious Luxury</h6>
                    <p className="text-secondary small mb-0">Zero-plastic policy, solar water heating, and sustainably sourced seafood.</p>
                  </div>
                </div>
                <div className="col-md-3">
                  <div className="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
                    <div className="fs-1 text-warning mb-2"><i className="bi bi-bell"></i></div>
                    <h6 className="brand-serif fw-bold text-dark mb-2">24/7 Concierge</h6>
                    <p className="text-secondary small mb-0">Personal butler service, luxury airport transfers, and private lagoon boat safaris.</p>
                  </div>
                </div>
                <div className="col-md-3">
                  <div className="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
                    <div className="fs-1 text-danger mb-2"><i className="bi bi-shield-check"></i></div>
                    <h6 className="brand-serif fw-bold text-dark mb-2">Guaranteed Booking</h6>
                    <p className="text-secondary small mb-0">Transactional concurrency protection guaranteeing zero overbooking errors.</p>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* 10. CONTACT US SECTION */}
        {activeTab === 'contact' && (
          <section className="py-5" style={{ backgroundColor: '#fcfbf8' }}>
            <div className="container">
              {/* Header */}
              <div className="text-center mb-5">
                <span className="boutique-tagline d-block mb-1">GET IN TOUCH</span>
                <h3 className="brand-serif fw-bold text-dark fs-2 mb-2">Contact & Location</h3>
                <p className="text-muted mx-auto" style={{ maxWidth: '600px' }}>
                  Have questions regarding your reservation, airport transfers, or private events? Our front-desk team is at your service 24 hours a day.
                </p>
              </div>

              <div className="row g-4">
                {/* Contact Details Card */}
                <div className="col-lg-5">
                  <div className="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
                    <h5 className="brand-serif fw-bold text-dark mb-4">Resort Coordinates</h5>

                    <div className="d-flex align-items-start gap-3 mb-4">
                      <div className="p-3 rounded-circle bg-light text-primary">
                        <i className="bi bi-geo-alt-fill fs-5"></i>
                      </div>
                      <div>
                        <span className="fw-semibold text-dark d-block">Physical Address</span>
                        <small className="text-muted">Porutota Road, Negombo 11500,<br />Western Province, Sri Lanka</small>
                      </div>
                    </div>

                    <div className="d-flex align-items-start gap-3 mb-4">
                      <div className="p-3 rounded-circle bg-light text-success">
                        <i className="bi bi-telephone-fill fs-5"></i>
                      </div>
                      <div>
                        <span className="fw-semibold text-dark d-block">Telephone & WhatsApp</span>
                        <small className="text-muted d-block">Front Desk: +94 31 223 4567</small>
                        <small className="text-muted d-block">Direct Concierge: +94 77 123 4567</small>
                      </div>
                    </div>

                    <div className="d-flex align-items-start gap-3 mb-4">
                      <div className="p-3 rounded-circle bg-light text-warning">
                        <i className="bi bi-envelope-fill fs-5"></i>
                      </div>
                      <div>
                        <span className="fw-semibold text-dark d-block">Electronic Inquiries</span>
                        <small className="text-muted d-block">Reservations: reservations@dutchpoint.lk</small>
                        <small className="text-muted d-block">General: info@dutchpoint.lk</small>
                      </div>
                    </div>

                    <div className="d-flex align-items-start gap-3 mb-4">
                      <div className="p-3 rounded-circle bg-light text-info">
                        <i className="bi bi-airplane-fill fs-5"></i>
                      </div>
                      <div>
                        <span className="fw-semibold text-dark d-block">Airport Proximity</span>
                        <small className="text-muted">Only 15 minutes (12 km) drive from Bandaranaike International Airport (CMB).</small>
                      </div>
                    </div>

                    <div className="mt-auto pt-3 border-top">
                      <a 
                        href="https://wa.me/94770000000" 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="btn btn-success w-100 rounded-pill py-2 fw-semibold"
                      >
                        <i className="bi bi-whatsapp me-2"></i> Chat with Concierge on WhatsApp
                      </a>
                    </div>
                  </div>
                </div>

                {/* Inquiry Form Card */}
                <div className="col-lg-7">
                  <div className="card border-0 shadow-sm rounded-4 p-4 p-lg-5 bg-white h-100">
                    <h5 className="brand-serif fw-bold text-dark mb-1">Send an Inquiry</h5>
                    <p className="text-muted small mb-4">Our front office typically replies within 30 minutes.</p>

                    <form onSubmit={handleInquirySubmit}>
                      <div className="row g-3 mb-3">
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold text-secondary">Your Name</label>
                          <input 
                            type="text" 
                            className="form-control rounded-pill px-3" 
                            required 
                            placeholder="e.g. John Doe"
                            value={inquiryName}
                            onChange={(e) => setInquiryName(e.target.value)}
                          />
                        </div>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold text-secondary">Email Address</label>
                          <input 
                            type="email" 
                            className="form-control rounded-pill px-3" 
                            required 
                            placeholder="e.g. john@example.com"
                            value={inquiryEmail}
                            onChange={(e) => setInquiryEmail(e.target.value)}
                          />
                        </div>
                      </div>

                      <div className="mb-3">
                        <label className="form-label small fw-semibold text-secondary">Inquiry Type</label>
                        <select 
                          className="form-select rounded-pill px-3"
                          value={inquirySubject}
                          onChange={(e) => setInquirySubject(e.target.value)}
                        >
                          <option value="Reservation Inquiry">Room Reservation & Availability</option>
                          <option value="Airport Transfer">Airport Transfer (CMB to Hotel)</option>
                          <option value="Dining Reservation">Seafood Grill & Restaurant Booking</option>
                          <option value="Event Inquiry">Wedding / Beach Event Gathering</option>
                          <option value="General Inquiry">Other General Question</option>
                        </select>
                      </div>

                      <div className="mb-4">
                        <label className="form-label small fw-semibold text-secondary">Message</label>
                        <textarea 
                          rows="4" 
                          className="form-control rounded-4 p-3" 
                          required 
                          placeholder="How can we assist with your stay in Negombo?"
                          value={inquiryMessage}
                          onChange={(e) => setInquiryMessage(e.target.value)}
                        ></textarea>
                      </div>

                      <button type="submit" className="btn btn-luxury-dark rounded-pill px-5 py-2">
                        <i className="bi bi-send-fill me-2"></i> Submit Inquiry
                      </button>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

      </main>

      {/* FOOTER */}
      <footer className="py-4 text-center border-top text-secondary small" style={{ backgroundColor: '#fcfbf8' }}>
        <div className="container">
          <div 
            className="brand-serif fs-5 fw-bold text-dark mb-1 cursor-pointer" 
            onClick={() => setActiveTab('home')}
            style={{ cursor: 'pointer' }}
          >
            Dutch Point Negombo
          </div>
          <p className="mb-2 text-muted">Boutique Luxury Beach Resort • Porutota Road, Negombo, Sri Lanka</p>
          <div className="d-flex flex-wrap justify-content-center gap-3 small text-muted">
            <span className="cursor-pointer" style={{ cursor: 'pointer' }} onClick={() => setActiveTab('rooms')}>Suites</span>
            <span>•</span>
            <span className="cursor-pointer" style={{ cursor: 'pointer' }} onClick={() => setActiveTab('dining')}>Dining</span>
            <span>•</span>
            <span className="cursor-pointer" style={{ cursor: 'pointer' }} onClick={() => setActiveTab('gallery')}>Gallery</span>
            <span>•</span>
            <span className="cursor-pointer" style={{ cursor: 'pointer' }} onClick={() => setActiveTab('about')}>About Us</span>
            <span>•</span>
            <span className="cursor-pointer" style={{ cursor: 'pointer' }} onClick={() => setActiveTab('contact')}>Contact</span>
          </div>
        </div>
      </footer>

      {/* FLOATING WHATSAPP BUTTON (from uploaded design) */}
      <a 
        href="https://wa.me/94770000000" 
        target="_blank" 
        rel="noopener noreferrer" 
        className="whatsapp-float"
        title="Chat on WhatsApp"
      >
        <i className="bi bi-whatsapp"></i>
      </a>

      {/* LOGIN / REGISTER MODAL */}
      <LoginModal 
        show={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        onLoginSuccess={(loggedUser) => {
          setUser(loggedUser);
          setMessage(`Welcome back, ${loggedUser.fullName}!`);
          setTimeout(() => setMessage(''), 4000);
        }}
      />

      {/* BOOKING MODAL (With Double Booking Prevention) */}
      <BookingModal 
        show={showBookingModal}
        room={selectedRoom}
        user={user}
        initialCheckIn={checkInFilter}
        initialCheckOut={checkOutFilter}
        initialGuests={guestsFilter}
        onClose={() => setShowBookingModal(false)}
        onBookingSuccess={(res) => {
          setMessage(`Reservation created for Suite #${res.roomNumber}! Please complete payment.`);
          setTimeout(() => setMessage(''), 4000);
          loadRooms();
          loadOccupiedRooms(checkInFilter, checkOutFilter);
          loadAllActiveBookings();
          loadMyBookings();
          setActiveTab('my-bookings');
          // Automatically open Payment Modal for instant checkout
          setSelectedBookingForPayment(res);
          setShowPaymentModal(true);
        }}
      />

      {/* 5. LUXURY PAYMENT MODAL */}
      <PaymentModal
        show={showPaymentModal}
        booking={selectedBookingForPayment}
        onClose={() => setShowPaymentModal(false)}
        onPaymentSuccess={(receipt) => {
          setMessage(`Payment of LKR ${Number(receipt.amount).toLocaleString()} confirmed! (Txn: ${receipt.transactionId})`);
          setTimeout(() => setMessage(''), 6000);
          loadMyBookings();
          loadRooms();
          loadOccupiedRooms(checkInFilter, checkOutFilter);
          loadAllActiveBookings();
          if (user?.role === 'Admin') {
            loadAdminDashboard();
          }
        }}
      />

    </div>
  );
}
