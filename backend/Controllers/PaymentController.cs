using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using HotelManagementApi.Data;
using HotelManagementApi.Models;

namespace HotelManagementApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PaymentsController : ControllerBase
    {
        private readonly HotelDbContext _context;

        public PaymentsController(HotelDbContext context)
        {
            _context = context;
        }

        // POST: api/payments/process
        [HttpPost("process")]
        public async Task<IActionResult> ProcessPayment([FromBody] ProcessPaymentRequest request)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            //Verify the booking exists//
            var booking = await _context.Bookings
                .Include(b => b.Customer)
                .Include(b => b.Room)
                .FirstOrDefaultAsync(b => b.BookingId == request.BookingId);

            if (booking == null)
            {
                return NotFound(new { message = $"Booking with ID {request.BookingId} was not found." });
            }

            //Prevent double-charging: Check if already paid//
            var alreadyPaid = await _context.Payments
                .AnyAsync(p => p.BookingId == request.BookingId && p.PaymentStatus == "Completed");

            if (alreadyPaid)
            {
                return BadRequest(new { message = "This booking has already been paid for." });
            }

            // Validate Card Expiry Date//
            var now = DateTime.UtcNow;
            if (request.ExpiryYear < now.Year || (request.ExpiryYear == now.Year && request.ExpiryMonth < now.Month))
            {
                return BadRequest(new { message = "The payment card has expired. Please use a valid card." });
            }

            // Generate a Unique Transaction Reference (e.g. TXN-20261108-A1B2C3)//
            var transactionId = $"TXN-{DateTime.UtcNow:yyyyMMdd}-{Guid.NewGuid().ToString()[..6].ToUpper()}";

            // Create Payment record in the database//
            var payment = new Payment
            {
                BookingId = booking.BookingId,
                Amount = booking.TotalAmount,
                PaymentMethod = request.PaymentMethod,
                TransactionId = transactionId,
                PaymentStatus = "Completed",
                PaymentDate = DateTime.UtcNow
            };

            _context.Payments.Add(payment);

            // Update Booking status to "Confirmed"//
            booking.BookingStatus = "Confirmed";

            await _context.SaveChangesAsync();

            //  Mask the card number (keep only the last 4 digits)//
            var cleanCard = request.CardNumber.Replace(" ", "").Replace("-", "");
            var last4 = cleanCard.Length >= 4 ? cleanCard[^4..] : "0000";
            var maskedCard = $"**** **** **** {last4}";

            // Return receipt response//
            var response = new PaymentResponse
            {
                Success = true,
                Message = "Payment processed successfully! Your booking is confirmed.",
                PaymentId = payment.PaymentId,
                BookingId = booking.BookingId,
                TransactionId = payment.TransactionId,
                Amount = payment.Amount,
                PaymentStatus = payment.PaymentStatus,
                PaymentDate = payment.PaymentDate,
                MaskedCardNumber = maskedCard
            };

            return Ok(response);
        }

        // GET: api/payments/booking/{bookingId}//
        // Retrieve payment receipt for a specific booking//
        [HttpGet("booking/{bookingId}")]
        public async Task<IActionResult> GetPaymentByBookingId(int bookingId)
        {
            var payment = await _context.Payments
                .FirstOrDefaultAsync(p => p.BookingId == bookingId);

            if (payment == null)
            {
                return NotFound(new { message = "No payment record found for this booking." });
            }

            return Ok(payment);
        }

        // GET: api/payments//
        // List all payments for Admin financial auditing//
        [HttpGet]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> GetAllPayments()
        {
            var payments = await _context.Payments
                .Include(p => p.Booking)
                    .ThenInclude(b => b!.Customer)
                .OrderByDescending(p => p.PaymentDate)
                .ToListAsync();

            return Ok(payments);
        }
    }
}