using System;

namespace MotoCare.Models.Modul1_MasterData
{
    /// <summary>
    /// Modul 1: Master Data
    /// Penanggung Jawab: Izat Ibrahimovic
    /// 
    /// Kelas Mechanic mewarisi (Inheritance) dari kelas Person.
    /// Mengimplementasikan:
    /// 1. Inheritance (Person -> Mechanic)
    /// 2. Variable & Get-Set Properties dengan business constraints
    /// 3. Business Methods untuk manajemen performa mekanik
    /// 4. Polymorphism (Override GetProfileSummary)
    /// </summary>
    public class Mechanic : Person
    {
        // Field private
        private decimal _hourlyRate;
        private int _totalServicesHandled;

        // Properties
        public string MechanicCode { get; set; } = string.Empty;
        public string Specialization { get; set; } = "Umum"; // Contoh: Mesin, Injeksi, Kelistrikan, Kaki-kaki
        public bool IsOnDuty { get; set; } = true;

        // Property Get-Set dengan enkapsulasi nilai tarif per jam
        public decimal HourlyRate
        {
            get => _hourlyRate;
            set
            {
                if (value < 0)
                    throw new ArgumentException("Tarif mekanik tidak boleh bernilai negatif.");
                _hourlyRate = value;
            }
        }

        // Property read-only dari luar (private set)
        public int TotalServicesHandled
        {
            get => _totalServicesHandled;
            private set => _totalServicesHandled = value;
        }

        // Constructor
        public Mechanic() : base()
        {
        }

        public Mechanic(int id, string fullName, string phoneNumber, string email, string mechanicCode, string specialization, decimal hourlyRate)
            : base(id, fullName, phoneNumber, email)
        {
            MechanicCode = mechanicCode;
            Specialization = specialization;
            HourlyRate = hourlyRate;
            TotalServicesHandled = 0;
        }

        // Method untuk mencatat penyelesaian pekerjaan servis
        public void RecordCompletedService()
        {
            TotalServicesHandled++;
            UpdatedAt = DateTime.Now;
        }

        // Method menghitung bonus insentif servis berdasarkan jumlah penanganan
        public decimal CalculateIncentiveBonus()
        {
            // Bonus Rp 15.000 per servis yang diselesaikan
            return TotalServicesHandled * 15000m;
        }

        // Override method dari Base Class (Polymorphism)
        public override string GetProfileSummary()
        {
            string status = IsOnDuty ? "Sedang Bertugas" : "Libur / Istirahat";
            return $"[Mekanik #{MechanicCode}] {FullName} ({Specialization}) | Status: {status} | Servis Selesai: {TotalServicesHandled}";
        }
    }
}
