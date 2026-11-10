using System;
using System.Collections.Generic;
using System.Linq;
using MotoCare.Models.Common;
using MotoCare.Models.Modul1_MasterData;
using MotoCare.Models.Modul2_OperasionalServis.Abstracts;

namespace MotoCare.Models.Modul2_OperasionalServis
{
    public enum ServiceOrderStatus
    {
        Antrian = 0,
        SedangDikerjakan = 1,
        MenungguSparepart = 2,
        Selesai = 3,
        Dibatalkan = 4
    }

    /// <summary>
    /// Modul 2: Operasional Servis & Inventaris
    /// Penanggung Jawab: Putrana Yudhistira
    /// 
    /// Kelas ServiceOrder merepresentasikan surat perintah kerja / tiket servis motor.
    /// Mengimplementasikan:
    /// 1. Collection (List<BaseServiceItem>)
    /// 2. Relasi komposisi dengan Customer, Vehicle, dan Mechanic
    /// 3. Variable, Get-Set properties
    /// 4. Business Methods untuk manajemen pengerjaan servis
    /// </summary>
    public class ServiceOrder : BaseEntity
    {
        // Field private backing fields
        private string _orderNumber = string.Empty;

        // Properties Get-Set
        public string OrderNumber
        {
            get => _orderNumber;
            set
            {
                if (string.IsNullOrWhiteSpace(value))
                    throw new ArgumentException("Nomor SPK Servis tidak boleh kosong.");
                _orderNumber = value.Trim().ToUpper();
            }
        }

        public DateTime ServiceDate { get; set; } = DateTime.Now;
        public string CustomerComplaint { get; set; } = string.Empty; // Keluhan pemilik motor
        public ServiceOrderStatus Status { get; set; } = ServiceOrderStatus.Antrian;

        // Relasi Antar Objek
        public Customer Customer { get; set; } = null!;
        public Vehicle Vehicle { get; set; } = null!;
        public Mechanic AssignedMechanic { get; set; } = null!;

        // COLLECTION: Menyimpan daftar rincian pekerjaan dan sparepart yang dipakai
        public List<BaseServiceItem> ServiceItems { get; set; } = new List<BaseServiceItem>();

        // Constructor
        public ServiceOrder()
        {
        }

        public ServiceOrder(int id, string orderNumber, Customer customer, Vehicle vehicle, Mechanic mechanic, string complaint)
        {
            Id = id;
            OrderNumber = orderNumber;
            Customer = customer ?? throw new ArgumentNullException(nameof(customer));
            Vehicle = vehicle ?? throw new ArgumentNullException(nameof(vehicle));
            AssignedMechanic = mechanic ?? throw new ArgumentNullException(nameof(mechanic));
            CustomerComplaint = complaint;
            Status = ServiceOrderStatus.Antrian;
        }

        // Method menambah item (Jasa atau Sparepart) ke dalam pesanan servis
        public void AddServiceItem(BaseServiceItem item)
        {
            if (item == null)
                throw new ArgumentNullException(nameof(item), "Item servis tidak boleh null.");

            // Jika item adalah Sparepart, kurangi stok gudang secara otomatis
            if (item is Sparepart sparepart)
            {
                sparepart.DeductStock(item.Quantity);
            }

            ServiceItems.Add(item);
        }

        // Method menghitung total biaya kotor sebelum diskon
        public decimal CalculateSubtotal()
        {
            return ServiceItems.Sum(item => item.CalculateTotalCost());
        }

        // Method update status pengerjaan servis
        public void MarkAsCompleted()
        {
            Status = ServiceOrderStatus.Selesai;
            AssignedMechanic.RecordCompletedService();
            Customer.AddLoyaltyPoints((int)(CalculateSubtotal() / 10000m)); // 1 poin per Rp 10.000
            UpdatedAt = DateTime.Now;
        }

        public override string GetEntityInfo()
        {
            return $"SPK [{OrderNumber}] - Kendaraan: {Vehicle.LicensePlate} | Mekanik: {AssignedMechanic.FullName} | Status: {Status} | Total Item: {ServiceItems.Count}";
        }
    }
}
