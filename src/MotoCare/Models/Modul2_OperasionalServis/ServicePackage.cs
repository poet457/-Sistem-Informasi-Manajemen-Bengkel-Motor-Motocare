using System;
using MotoCare.Models.Modul2_OperasionalServis.Abstracts;

namespace MotoCare.Models.Modul2_OperasionalServis
{
    /// <summary>
    /// Modul 2: Operasional Servis & Inventaris
    /// Penanggung Jawab: Putrana Yudhistira
    /// 
    /// Kelas ServicePackage mewarisi BaseServiceItem.
    /// Merepresentasikan paket jasa pekerjaan servis motor (misal: Servis Ringan, Tune-up, Servis CVT, Overhaul).
    /// Mengimplementasikan:
    /// 1. Inheritance dari BaseServiceItem
    /// 2. Variable & Get-Set Properties untuk estimasi waktu pengerjaan
    /// 3. Override Abstract Method CalculateDiscount (diskon jasa hingga 30%)
    /// </summary>
    public class ServicePackage : BaseServiceItem
    {
        // Field private
        private int _estimatedMinutes;

        // Auto Properties
        public string ServiceType { get; set; } = "Reguler"; // Reguler, Berkala, Darurat/Bongkar Mesin
        public string Description { get; set; } = string.Empty;

        // Property Get-Set dengan enkapsulasi durasi estimasi
        public int EstimatedMinutes
        {
            get => _estimatedMinutes;
            set
            {
                if (value <= 0)
                    throw new ArgumentException("Estimasi waktu pengerjaan minimal harus 1 menit.");
                _estimatedMinutes = value;
            }
        }

        // Constructor
        public ServicePackage() : base()
        {
        }

        public ServicePackage(int id, string packageCode, string packageName, decimal fee, int estimatedMinutes, string serviceType, string description)
            : base(id, packageCode, packageName, fee, 1, "Jasa Servis")
        {
            EstimatedMinutes = estimatedMinutes;
            ServiceType = serviceType;
            Description = description;
        }

        // Override Abstract Method dari BaseServiceItem
        // Diskon jasa servis diperbolehkan promo hingga maksimal 30%
        public override decimal CalculateDiscount(decimal discountPercentage)
        {
            decimal effectiveDiscount = Math.Min(discountPercentage, 30m);
            decimal normalSubtotal = CalculateTotalCost();
            return normalSubtotal * (effectiveDiscount / 100m);
        }

        public override string GetServiceItemDetail()
        {
            return $"[JASA SERVIS] {ItemName} ({ServiceType}) | Estimasi: {EstimatedMinutes} Menit | Tarif: Rp {UnitPrice:N0}";
        }
    }
}
