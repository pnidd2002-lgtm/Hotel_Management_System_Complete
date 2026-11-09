import React, { useState, useEffect } from 'react';
import { getRoomImage } from '../assets/images';

export default function BookingModal({ room, user, show, onClose, onBookingSuccess, initialCheckIn, initialCheckOut, initialGuests }) {
  const [checkIn, setCheckIn] = useState(initialCheckIn || '2026-10-10');
  const [checkOut, setCheckOut] = useState(initialCheckOut || '2026-10-14');
  const [guests, setGuests] = useState(initialGuests ? parseInt(initialGuests) : 1);
  const [specialRequests, setSpecialRequests] = useState('');

  const [loading, setLoading] = useState(false);
  const [conflictError, setConflictError] = useState('');
  const [generalError, setGeneralError] = useState('');

  // Synchronize modal state with search filters whenever the modal opens
  useEffect(() => {
    if (show) {
      if (initialCheckIn) setCheckIn(initialCheckIn);
      if (initialCheckOut) setCheckOut(initialCheckOut);
      if (initialGuests) {
        const val = parseInt(initialGuests, 10);
        const maxCap = room ? room.capacity : 2;
        setGuests(val > maxCap ? maxCap : (val > 0 ? val : 1));
      } else {
        setGuests(1);
      }
      setConflictError('');
      setGeneralError('');
    }
  }, [show, initialCheckIn, initialCheckOut, initialGuests, room]);

  if (!show || !room) return null;

  // Calculate nights and price
  const cin = new Date(checkIn);
  const cout = new Date(checkOut);
  const diffDays = Math.ceil((cout - cin) / (1000 * 60 * 60 * 24));
  const nights = diffDays > 0 ? diffDays : 1;
  const totalPrice = nights * room.pricePerNight;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setConflictError('');
    setGeneralError('');

    if (cin >= cout) {
      setGeneralError('Check-out date must be after check-in date.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/bookings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customerId: user ? user.customerId : 1,
          roomId: room.roomId,
          checkInDate: checkIn,
          checkOutDate: checkOut,
          numberOfGuests: parseInt(guests),
          specialRequests
        })
      });

      const data = await response.json();

      if (!response.ok) {
        if (data.message && data.message.toLowerCase().includes('double booking')) {
          setConflictError(data.message);
        } else {
          setGeneralError(data.message || 'Failed to complete booking.');
        }
        return;
      }

      onBookingSuccess(data);
      onClose();
    } catch (err) {
      setGeneralError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(11, 19, 32, 0.75)' }}>
      <div className="modal-dialog modal-dialog-centered modal-lg">
        <div className="modal-content shadow-lg border-0" style={{ borderRadius: '28px', overflow: 'hidden' }}>
          
          {/* Header */}
          <div className="modal-header py-3 px-4 text-white" style={{ backgroundColor: '#0b1320' }}>
            <div>
              <span className="boutique-tagline d-block" style={{ fontSize: '0.65rem' }}>DUTCH POINT NEGOMBO</span>
              <h5 className="modal-title brand-serif fs-4 mb-0">
                Reserve Suite #{room.roomNumber} • {room.roomType}
              </h5>
            </div>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>

          <div className="modal-body p-4 bg-white">
            {/* DOUBLE BOOKING PREVENTED ALERT */}
            {conflictError && (
              <div className="alert alert-danger border-2 p-3 mb-4 rounded-3 shadow-sm">
                <div className="fw-bold d-flex align-items-center gap-2 mb-1">
                  <i className="bi bi-shield-fill-x text-danger fs-5"></i>
                  <span>Double Booking Prevented!</span>
                </div>
                <div className="small text-dark mb-1">{conflictError}</div>
                <small className="text-muted">
                  💡 This room is already occupied during these dates. Please choose alternative dates.
                </small>
              </div>
            )}

            {generalError && (
              <div className="alert alert-danger py-2 small mb-3">{generalError}</div>
            )}

            <div className="row g-4">
              {/* Room Preview Card */}
              <div className="col-md-5">
                <div className="card h-100 border-0 rounded-4 overflow-hidden shadow-sm" style={{ backgroundColor: '#fbfbf9' }}>
                  <img 
                    src={getRoomImage(room.imageName)} 
                    alt={room.roomType} 
                    className="card-img-top"
                    style={{ height: '175px', objectFit: 'cover' }}
                  />
                  <div className="card-body p-3">
                    <span className="badge rounded-pill bg-dark mb-1 px-3 py-1">Room #{room.roomNumber}</span>
                    <h5 className="brand-serif fw-bold text-dark mb-1">{room.roomType}</h5>
                    <div className="text-muted small mb-3">
                      <i className="bi bi-people me-1"></i> Up to {room.capacity} Guests
                    </div>

                    <div className="p-3 bg-white rounded-3 border small">
                      <div className="d-flex justify-content-between text-secondary mb-1">
                        <span>Nightly Rate:</span>
                        <span className="fw-bold text-dark">LKR {Number(room.pricePerNight).toLocaleString()}</span>
                      </div>
                      <div className="d-flex justify-content-between text-secondary mb-1">
                        <span>Duration:</span>
                        <span className="fw-semibold text-dark">{nights} {nights === 1 ? 'Night' : 'Nights'}</span>
                      </div>
                      <div className="d-flex justify-content-between border-top pt-2 mt-2 fs-6 fw-bold">
                        <span className="text-secondary">Total Due:</span>
                        <span className="brand-gold">LKR {Number(totalPrice).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Form */}
              <div className="col-md-7">
                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label className="form-label small fw-semibold text-secondary">Guest Name</label>
                    <input 
                      type="text" 
                      className="form-control rounded-pill px-3 bg-light" 
                      disabled 
                      value={user ? `${user.fullName} (${user.email})` : 'Guest'}
                    />
                  </div>

                  <div className="row g-2 mb-3">
                    <div className="col-sm-6">
                      <label className="form-label small fw-semibold text-secondary">Check-In Date</label>
                      <input 
                        type="date" 
                        className="form-control rounded-pill px-3" 
                        required 
                        value={checkIn}
                        onChange={(e) => setCheckIn(e.target.value)}
                      />
                    </div>
                    <div className="col-sm-6">
                      <label className="form-label small fw-semibold text-secondary">Check-Out Date</label>
                      <input 
                        type="date" 
                        className="form-control rounded-pill px-3" 
                        required 
                        value={checkOut}
                        min={checkIn}
                        onChange={(e) => setCheckOut(e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="mb-3">
                    <label className="form-label small fw-semibold text-secondary">
                      Number of Guests <span className="text-muted">(Max {room.capacity} Persons)</span>
                    </label>
                    <select 
                      className="form-select rounded-pill px-3" 
                      value={guests} 
                      onChange={(e) => setGuests(parseInt(e.target.value))}
                    >
                      {Array.from({ length: room.capacity }, (_, i) => i + 1).map((n) => (
                        <option key={n} value={n}>{n === 1 ? '1 Guest (1 Person)' : `${n} Guests`}</option>
                      ))}
                    </select>
                  </div>

                  <div className="mb-4">
                    <label className="form-label small fw-semibold text-secondary">Special Preferences</label>
                    <textarea 
                      className="form-control rounded-3" 
                      rows="2"
                      placeholder="e.g. Quiet room, ocean view, late check-in..."
                      value={specialRequests}
                      onChange={(e) => setSpecialRequests(e.target.value)}
                    ></textarea>
                  </div>

                  <div className="d-flex justify-content-end gap-2">
                    <button type="button" className="btn btn-luxury-pill px-4" onClick={onClose}>
                      Cancel
                    </button>
                    <button type="submit" className="btn btn-luxury-dark px-4" disabled={loading}>
                      {loading ? 'Reserving...' : `Confirm • LKR ${Number(totalPrice).toLocaleString()}`}
                    </button>
                  </div>
                </form>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}
