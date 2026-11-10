using System;
using System.Collections.Generic;

namespace MotoCare.Models.Modul1_MasterData
{
    public class Customer : Person
    {
        private int _loyaltyPoints;

        // Auto-implemented Properties
        public string CustomerCode { get; set; } = string.Empty;
        public string Address { get; set; } = string.Empty;
        public DateTime MemberSince { get; set; } = DateTime.Now;

        // Property dengan validasi Get-Set
        public int LoyaltyPoints
        {
            get => _loyaltyPoints;
            private set
            {
                if (value < 0)
                    _loyaltyPoints = 0;
                else
                    _loyaltyPoints = value;
            }
        }

        // Collection: Menyimpan daftar kendaraan yang dimiliki oleh pelanggan ini
        public List<Vehicle> RegisteredVehicles { get; set; } = new List<Vehicle>();

        // Constructor
        public Customer() : base()
        {
        }

        public Customer(int id, string fullName, string phoneNumber, string email, string customerCode, string address)
            : base(id, fullName, phoneNumber, email)
        {
            CustomerCode = customerCode;
            Address = address;
            LoyaltyPoints = 0;
        }

        // Method untuk menambah kendaraan ke dalam koleksi pelanggan
        public void AddVehicle(Vehicle vehicle)
        {
            if (vehicle == null)
                throw new ArgumentNullException(nameof(vehicle), "Data kendaraan tidak boleh null.");

            RegisteredVehicles.Add(vehicle);
        }

        // Method untuk menambah poin loyalitas servis
        public void AddLoyaltyPoints(int points)
        {
            if (points > 0)
            {
                LoyaltyPoints += points;
            }
        }

        // Method untuk menukar poin menjadi diskon
        public bool RedeemPoints(int pointsToRedeem, out decimal discountAmount)
        {
            discountAmount = 0m;
            if (pointsToRedeem <= LoyaltyPoints && pointsToRedeem > 0)
            {
                LoyaltyPoints -= pointsToRedeem;
                // Setiap 10 poin bernilai diskon Rp 5.000
                discountAmount = (pointsToRedeem / 10m) * 5000m;
                return true;
            }
            return false;
        }

        // Override method dari Base Class (Polymorphism)
        public override string GetProfileSummary()
        {
            return $"[Pelanggan #{CustomerCode}] {FullName} | Total Kendaraan: {RegisteredVehicles.Count} | Poin: {LoyaltyPoints}";
        }
    }
}
