import React, { useState } from 'react';

export default function PaymentModal({ show, booking, onClose, onPaymentSuccess }) {
  const [cardholderName, setCardholderName] = useState('');
  const [cardNumber, setCardNumber] = useState('');
  const [expiryMonth, setExpiryMonth] = useState('12');
  const [expiryYear, setExpiryYear] = useState('2026');
  const [cvv, setCvv] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [receipt, setReceipt] = useState(null);

  if (!show || !booking) return null;

  // Format card number with spaces every 4 digits (e.g. 1234 5678 9012 3456)
  const handleCardNumberChange = (e) => {
    const raw = e.target.value.replace(/\D/g, '').slice(0, 16);
    const formatted = raw.replace(/(\d{4})/g, '$1 ').trim();
    setCardNumber(formatted);
  };

  const handleCvvChange = (e) => {
    const raw = e.target.value.replace(/\D/g, '').slice(0, 4);
    setCvv(raw);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const cleanCard = cardNumber.replace(/\s+/g, '');
    if (cleanCard.length < 13 || cleanCard.length > 19) {
      setError('Please enter a valid 16-digit card number.');
      return;
    }

    if (cvv.length < 3) {
      setError('CVV must be 3 or 4 digits.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/payments/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bookingId: booking.bookingId,
          cardholderName: cardholderName.trim(),
          cardNumber: cleanCard,
          expiryMonth: parseInt(expiryMonth, 10),
          expiryYear: parseInt(expiryYear, 10),
          cvv: cvv.trim(),
          paymentMethod: 'Credit Card (Visa/Mastercard)'
        })
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || 'Payment processing failed.');
        return;
      }

      // Success! Show receipt view
      setReceipt(data);
      if (onPaymentSuccess) {
        onPaymentSuccess(data);
      }
    } catch (err) {
      setError('Server connection error. Please make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setReceipt(null);
    setError('');
    setCardholderName('');
    setCardNumber('');
    setCvv('');
    onClose();
  };

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(11, 19, 32, 0.85)' }}>
      <div className="modal-dialog modal-dialog-centered modal-md">
        <div className="modal-content shadow-lg border-0" style={{ borderRadius: '24px', overflow: 'hidden' }}>
          
          {/* Header */}
          <div className="modal-header py-3 px-4 text-white" style={{ backgroundColor: '#0b1320' }}>
            <div>
              <span className="boutique-tagline d-block text-warning" style={{ fontSize: '0.65rem' }}>
                SECURE CHECKOUT • 256-BIT ENCRYPTION
              </span>
              <h5 className="modal-title brand-serif fs-5 mb-0">
                {receipt ? 'Payment Receipt' : 'Complete Room Payment'}
              </h5>
            </div>
            <button type="button" className="btn-close btn-close-white" onClick={handleClose}></button>
          </div>

          {/* Modal Body */}
          <div className="modal-body p-4 bg-white">
            {receipt ? (
              /* RECEIPT VIEW */
              <div className="text-center py-2">
                <div className="mb-3">
                  <span className="badge rounded-circle p-3 bg-success-subtle text-success fs-1">
                    ✓
                  </span>
                </div>
                <h4 className="brand-serif fw-bold text-dark mb-1">Payment Successful!</h4>
                <p className="text-muted small mb-4">Your reservation has been officially confirmed.</p>

                <div className="p-3 bg-light rounded-3 text-start small mb-4">
                  <div className="d-flex justify-content-between mb-2">
                    <span className="text-muted">Transaction ID:</span>
                    <span className="fw-bold font-monospace text-dark">{receipt.transactionId}</span>
                  </div>
                  <div className="d-flex justify-content-between mb-2">
                    <span className="text-muted">Booking Reference:</span>
                    <span className="fw-semibold text-dark">#{receipt.bookingId}</span>
                  </div>
                  <div className="d-flex justify-content-between mb-2">
                    <span className="text-muted">Card Used:</span>
                    <span className="font-monospace text-dark">{receipt.maskedCardNumber}</span>
                  </div>
                  <div className="d-flex justify-content-between mb-2">
                    <span className="text-muted">Payment Date:</span>
                    <span className="text-dark">{new Date(receipt.paymentDate).toLocaleString()}</span>
                  </div>
                  <div className="d-flex justify-content-between border-top pt-2 mt-2 fs-6 fw-bold">
                    <span>Total Amount Paid:</span>
                    <span className="text-success">LKR {Number(receipt.amount).toLocaleString()}</span>
                  </div>
                </div>

                <button className="btn btn-luxury-dark w-100 rounded-pill py-2" onClick={handleClose}>
                  Done & View My Bookings
                </button>
              </div>
            ) : (
              /* PAYMENT FORM VIEW */
              <form onSubmit={handleSubmit}>
                {/* Summary Banner */}
                <div className="p-3 mb-3 rounded-3" style={{ backgroundColor: '#f8f9fa', border: '1px solid #e9ecef' }}>
                  <div className="d-flex justify-content-between align-items-center mb-1">
                    <span className="fw-bold text-dark">{booking.roomType || `Suite #${booking.roomNumber}`}</span>
                    <span className="badge bg-primary rounded-pill">Room #{booking.roomNumber}</span>
                  </div>
                  <div className="d-flex justify-content-between align-items-center border-top pt-2 mt-2">
                    <span className="text-muted small">Total Due:</span>
                    <span className="fs-5 fw-bold brand-gold">
                      LKR {Number(booking.totalAmount).toLocaleString()}
                    </span>
                  </div>
                </div>

                {error && (
                  <div className="alert alert-danger py-2 px-3 small rounded-3 mb-3">
                    {error}
                  </div>
                )}

                {/* Cardholder Name */}
                <div className="mb-3">
                  <label className="form-label small fw-semibold text-muted mb-1">Cardholder Name</label>
                  <input
                    type="text"
                    className="form-control rounded-3"
                    placeholder="e.g. Pasindu Nirmal"
                    value={cardholderName}
                    onChange={(e) => setCardholderName(e.target.value)}
                    required
                  />
                </div>

                {/* Card Number */}
                <div className="mb-3">
                  <label className="form-label small fw-semibold text-muted mb-1">Card Number</label>
                  <div className="input-group">
                    <input
                      type="text"
                      className="form-control rounded-start-3 font-monospace"
                      placeholder="4532 1234 5678 9010"
                      value={cardNumber}
                      onChange={handleCardNumberChange}
                      maxLength="19"
                      required
                    />
                    <span className="input-group-text bg-light rounded-end-3 text-muted small">💳</span>
                  </div>
                </div>

                {/* Expiry & CVV */}
                <div className="row g-2 mb-4">
                  <div className="col-4">
                    <label className="form-label small fw-semibold text-muted mb-1">Month</label>
                    <select
                      className="form-select rounded-3"
                      value={expiryMonth}
                      onChange={(e) => setExpiryMonth(e.target.value)}
                    >
                      {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
                        <option key={m} value={m}>
                          {m < 10 ? `0${m}` : m}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="col-4">
                    <label className="form-label small fw-semibold text-muted mb-1">Year</label>
                    <select
                      className="form-select rounded-3"
                      value={expiryYear}
                      onChange={(e) => setExpiryYear(e.target.value)}
                    >
                      {Array.from({ length: 10 }, (_, i) => 2025 + i).map((y) => (
                        <option key={y} value={y}>
                          {y}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="col-4">
                    <label className="form-label small fw-semibold text-muted mb-1">CVV</label>
                    <input
                      type="password"
                      className="form-control rounded-3 font-monospace text-center"
                      placeholder="•••"
                      value={cvv}
                      onChange={handleCvvChange}
                      maxLength="4"
                      required
                    />
                  </div>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  className="btn btn-luxury-dark w-100 rounded-pill py-2 fw-semibold"
                  disabled={loading}
                >
                  {loading ? (
                    <span>
                      <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                      Processing Payment...
                    </span>
                  ) : (
                    `Pay LKR ${Number(booking.totalAmount).toLocaleString()}`
                  )}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}