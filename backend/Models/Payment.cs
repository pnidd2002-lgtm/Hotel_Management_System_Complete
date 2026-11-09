using HotelManagementApi.Models;
using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;


namespace HotelManagementApi.Models
{
    public class Payment
    {
        [Key] // payments table primary key c# attribute//
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int PaymentId { get; set; }

        [Required]
        public int BookingId { get; set; }

        [Required]
        [Column(TypeName ="decimal(18,2)")]
        public decimal Amount { get; set; }

        [Required] // not allow NULL records//
        [StringLength(50)]// varchar(50)//
        public string PaymentMethod { get; set; } = "Credit Card";

        [Required]
        [StringLength(100)]
        public string TransactionId { get; set; } = string.Empty;

        [Required]
        [StringLength(50)]
        public string PaymentStatus { get; set; } = "Completed";
        public DateTime PaymentDate { get; set; } = DateTime.UtcNow; // when the payment was  done//

        [ForeignKey("BookingId")]// link with booking table//
        public Booking? Booking { get; set; }



    }
}
