using System;
using MotoCare.Models.Common;

namespace MotoCare.Models.Modul1_MasterData
{
    /// <summary>
    /// Modul 1: Master Data
    /// Penanggung Jawab: Izat Ibrahimovic
    /// 
    /// Kelas Vehicle merepresentasikan sepeda motor pelanggan bengkel.
    /// Mengimplementasikan:
    /// 1. Inheritance dari BaseEntity
    /// 2. Variable (field private)
    /// 3. Get-Set Property dengan validasi plat nomor dan kilometer
    /// 4. Business Method (cek kebutuhan servis berkala)
    /// </summary>
    public class Vehicle : BaseEntity
    {
        // Field private backing fields
        private string _licensePlate = string.Empty;
        private int _currentKilometers;

        // Auto Properties
        public int CustomerId { get; set; }
        public string Brand { get; set; } = string.Empty;       // Honda, Yamaha, Suzuki, Kawasaki
        public string Model { get; set; } = string.Empty;       // Vario 160, NMAX, Satria F150
        public int ProductionYear { get; set; }
        public int EngineCapacityCc { get; set; }               // 110, 125, 150, 160, 250
        public DateTime? LastServiceDate { get; set; }

        // Property dengan validasi Plat Nomor
        public string LicensePlate
        {
            get => _licensePlate;
            set
            {
                if (string.IsNullOrWhiteSpace(value))
                    throw new ArgumentException("Plat nomor motor wajib diisi.");
                _licensePlate = value.Trim().ToUpper();
            }
        }

        // Property dengan validasi Kilometer kendaraan
        public int CurrentKilometers
        {
            get => _currentKilometers;
            set
            {
                if (value < 0)
                    throw new ArgumentException("Jarak tempuh (KM) tidak boleh negatif.");
                _currentKilometers = value;
            }
        }

        // Constructor
        public Vehicle()
        {
        }

        public Vehicle(int id, int customerId, string licensePlate, string brand, string model, int year, int cc, int km)
        {
            Id = id;
            CustomerId = customerId;
            LicensePlate = licensePlate;
            Brand = brand;
            Model = model;
            ProductionYear = year;
            EngineCapacityCc = cc;
            CurrentKilometers = km;
        }

        // Business Method: Memeriksa apakah motor sudah saatnya ganti oli atau servis rutin
        public bool NeedsPeriodicService()
        {
            // Jika belum pernah servis atau sudah lebih dari 2.500 km sejak servis terakhir
            if (!LastServiceDate.HasValue)
                return true;

            TimeSpan diff = DateTime.Now - LastServiceDate.Value;
            return diff.TotalDays >= 60; // Atau lebih dari 2 bulan
        }

        // Method update kilometer setelah servis
        public void UpdateOdometer(int newKilometers)
        {
            if (newKilometers < CurrentKilometers)
                throw new InvalidOperationException("Odometer baru tidak boleh lebih kecil dari sebelumnya.");

            CurrentKilometers = newKilometers;
            LastServiceDate = DateTime.Now;
            UpdatedAt = DateTime.Now;
        }

        public override string GetEntityInfo()
        {
            return $"Kendaraan [{LicensePlate}]: {Brand} {Model} ({ProductionYear}) - {CurrentKilometers} KM";
        }
    }
}
