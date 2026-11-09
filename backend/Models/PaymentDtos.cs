using System;
using System.ComponentModel.DataAnnotations;

namespace HotelManagementApi.Models
{
    // 1. What the customer sends from the React checkout screen//
    public class ProcessPaymentRequest
    {
        [Required(ErrorMessage = "Booking Id is required.")]
        public int BookingId { get; set; }

        [Required(ErrorMessage = "Card holder name is required.")]
        [StringLength(100, MinimumLength = 2, ErrorMessage = "Card holder name must be between 2 and 100 characters.")]
        public string CardholderName { get; set; } = string.Empty;

        [Required(ErrorMessage = "Card number is required.")]
        [StringLength(19, MinimumLength = 13, ErrorMessage = "Enter a valid card number.")]
        public string CardNumber { get; set; } = string.Empty;

        [Required(ErrorMessage = "Expiry month is required.")]
        [Range(1, 12, ErrorMessage = "Expiry month must be between 1 and 12.")]
        public int ExpiryMonth { get; set; }

        [Required(ErrorMessage = "Expiry year is required.")]
        [Range(2025, 2040, ErrorMessage = "Expiry year must be valid.")]
        public int ExpiryYear { get; set; }

        [Required(ErrorMessage = "CVV security code is required.")]
        [RegularExpression(@"^\d{3,4}$", ErrorMessage = "CVV must be 3 or 4 digits.")]
        public string Cvv { get; set; } = string.Empty;

        public string PaymentMethod { get; set; } = "Credit Card";
    }

    // 2. What our backend sends back to React to confirm the payment//
    public class PaymentResponse
    {
        public bool Success { get; set; }
        public string Message { get; set; } = string.Empty;
        public int PaymentId { get; set; }
        public int BookingId { get; set; }
        public string TransactionId { get; set; } = string.Empty;
        public decimal Amount { get; set; }
        public string PaymentStatus { get; set; } = "Completed";
        public DateTime PaymentDate { get; set; }
        public string MaskedCardNumber { get; set; } = string.Empty; // show last 4 digits of customer's card//
    }
}