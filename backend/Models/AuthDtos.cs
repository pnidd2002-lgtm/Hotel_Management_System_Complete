using System.ComponentModel.DataAnnotations;

namespace HotelManagementApi.Models
{
    public class LoginRequest
    {
        [Required]
        public string Email { get; set; } = string.Empty; // Accepts Username (e.g. Pasindu) or Email

        [Required]
        public string Password { get; set; } = string.Empty;
    }

    public class RegisterRequest
    {
        [Required]
        [MaxLength(100)]
        public string FullName { get; set; } = string.Empty;

        [Required]
        [EmailAddress]
        [MaxLength(150)]
        public string Email { get; set; } = string.Empty;

        [Required]
        [MinLength(3)]
        public string Password { get; set; } = string.Empty;

        [Required]
        public string Phone { get; set; } = string.Empty;

        public string? Address { get; set; }
    }

    public class AuthResponse
    {
        public int CustomerId { get; set; }
        public string FullName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string Phone { get; set; } = string.Empty;
        public string? Address { get; set; }
        public string Role { get; set; } = string.Empty;

        //Jwt//
        public string Token {  get; set; } = string.Empty;
    }
}
