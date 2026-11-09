using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using HotelManagementApi.Data;
using HotelManagementApi.Models;
using BCrypt.Net;

namespace HotelManagementApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly HotelDbContext _context;

        public AuthController(HotelDbContext context)
        {
            _context = context;
        }

        // POST: api/auth/login
        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginRequest request)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            var identifier = request.Email.Trim().ToLower();

            // Match by Email, Username, or FullName (supports username "Pasindu")
            var user = await _context.Customers
                .FirstOrDefaultAsync(u => u.Email.ToLower() == identifier || 
                                          u.FullName.ToLower() == identifier ||
                                          (identifier == "pasindu" && u.Role == "Admin"));

            bool passwordValid = false;
            if (user != null)
            {
                // If password is a BCrypt hash (starts with $2a$, $2b$, or $2y$), verify with BCrypt
                if (user.Password.StartsWith("$2a$") || user.Password.StartsWith("$2b$") || user.Password.StartsWith("$2y$"))
                {
                    passwordValid = BCrypt.Net.BCrypt.Verify(request.Password, user.Password);
                }
                else
                {
                    // Fallback / Auto-upgrade plain text passwords to BCrypt upon successful login
                    if (user.Password == request.Password)
                    {
                        passwordValid = true;
                        user.Password = BCrypt.Net.BCrypt.HashPassword(request.Password, workFactor: 12);
                        await _context.SaveChangesAsync();
                    }
                }
            }

            if (user == null || !passwordValid)
            {
                return Unauthorized(new { message = "Invalid username/email or password." });
            }

            return Ok(new AuthResponse
            {
                CustomerId = user.CustomerId,
                FullName = user.FullName,
                Email = user.Email,
                Phone = user.Phone,
                Address = user.Address,
                Role = user.Role
            });
        }

        // POST: api/auth/register
        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] RegisterRequest request)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            var existingUser = await _context.Customers
                .AnyAsync(u => u.Email.ToLower() == request.Email.ToLower());

            if (existingUser)
            {
                return Conflict(new { message = "An account with this email already exists." });
            }

            // Security enforcement: All public registrations are strictly assigned Role = "Customer"
            var newUser = new Customer
            {
                FullName = request.FullName.Trim(),
                Email = request.Email.Trim().ToLower(),
                Password = BCrypt.Net.BCrypt.HashPassword(request.Password, workFactor: 12), 
                Phone = request.Phone.Trim(),
                Address = request.Address?.Trim(),
                Role = "Customer", // Hardcoded security enforcement - cannot choose Admin
                CreatedAt = DateTime.UtcNow
            };

            _context.Customers.Add(newUser);
            await _context.SaveChangesAsync();

            return Ok(new AuthResponse
            {
                CustomerId = newUser.CustomerId,
                FullName = newUser.FullName,
                Email = newUser.Email,
                Phone = newUser.Phone,
                Address = newUser.Address,
                Role = newUser.Role
            });
        }

        // GET: api/auth/customers
        [HttpGet("customers")]
        public async Task<IActionResult> GetAllCustomers()
        {
            var customers = await _context.Customers
                .OrderBy(c => c.CustomerId)
                .Select(c => new AuthResponse
                {
                    CustomerId = c.CustomerId,
                    FullName = c.FullName,
                    Email = c.Email,
                    Phone = c.Phone,
                    Address = c.Address,
                    Role = c.Role
                })
                .ToListAsync();

            return Ok(customers);
        }

        // PUT: api/auth/profile/{id}
        [HttpPut("profile/{id}")]
        public async Task<IActionResult> UpdateProfile(int id, [FromBody] Customer updated)
        {
            var customer = await _context.Customers.FindAsync(id);
            if (customer == null)
                return NotFound(new { message = "Customer not found." });

            customer.FullName = updated.FullName;
            customer.Phone = updated.Phone;
            customer.Address = updated.Address;

            if (!string.IsNullOrWhiteSpace(updated.Password))
            {
                customer.Password = updated.Password;
            }

            await _context.SaveChangesAsync();

            return Ok(new AuthResponse
            {
                CustomerId = customer.CustomerId,
                FullName = customer.FullName,
                Email = customer.Email,
                Phone = customer.Phone,
                Address = customer.Address,
                Role = customer.Role
            });
        }
    }
}
