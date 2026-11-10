using System;
using MotoCare.Models.Modul2_OperasionalServis.Abstracts;

namespace MotoCare.Models.Modul2_OperasionalServis
{
    /// <summary>
    /// Modul 2: Operasional Servis & Inventaris
    /// Penanggung Jawab: Putrana Yudhistira
    /// 
    /// Kelas Sparepart mewarisi BaseServiceItem.
    /// Mengimplementasikan:
    /// 1. Inheritance dari Abstract Class (BaseServiceItem)
    /// 2. Variable & Get-Set Properties untuk stok fisik
    /// 3. Business Logic Inventaris (Pengecekan stok, restock, pengurangan stok)
    /// 4. Override Abstract Method (Polymorphism)
    /// </summary>
    public class Sparepart : BaseServiceItem
    {
        // Field private
        private int _stockQuantity;
        private int _minimumStockAlert = 5;

        // Auto Properties
        public string Brand { get; set; } = string.Empty;       // AHM, Yamalube, Aspira, Motul
        public string RackLocation { get; set; } = string.Empty; // Rak A-01, Rak B-03

        // Property Get-Set dengan validasi jumlah stok
        public int StockQuantity
        {
            get => _stockQuantity;
            set
            {
                if (value < 0)
                    throw new ArgumentException("Jumlah stok gudang tidak boleh minus.");
                _stockQuantity = value;
            }
        }

        public int MinimumStockAlert
        {
            get => _minimumStockAlert;
            set => _minimumStockAlert = value < 0 ? 0 : value;
        }

        // Constructor
        public Sparepart() : base()
        {
        }

        public Sparepart(int id, string partCode, string partName, decimal sellingPrice, int stockQty, string brand, string location)
            : base(id, partCode, partName, sellingPrice, 1, "Sparepart")
        {
            StockQuantity = stockQty;
            Brand = brand;
            RackLocation = location;
        }

        // Business Method: Cek apakah stok menipis
        public bool IsStockLow()
        {
            return StockQuantity <= MinimumStockAlert;
        }

        // Method pengurangan stok saat dipakai servis
        public void DeductStock(int amountUsed)
        {
            if (amountUsed <= 0)
                throw new ArgumentException("Jumlah pemakaian harus lebih dari nol.");

            if (amountUsed > StockQuantity)
                throw new InvalidOperationException($"Stok suku cadang '{ItemName}' tidak mencukupi (Tersedia: {StockQuantity}, Diminta: {amountUsed}).");

            StockQuantity -= amountUsed;
            UpdatedAt = DateTime.Now;
        }

        // Method penambahan stok saat barang masuk
        public void Restock(int incomingAmount)
        {
            if (incomingAmount <= 0)
                throw new ArgumentException("Jumlah restock harus lebih dari nol.");

            StockQuantity += incomingAmount;
            UpdatedAt = DateTime.Now;
        }

        // Override implementasi Abstract Method dari BaseServiceItem
        // Diskon suku cadang maksimal 15% untuk menjaga margin profit toko bengkel
        public override decimal CalculateDiscount(decimal discountPercentage)
        {
            decimal effectiveDiscount = Math.Min(discountPercentage, 15m);
            decimal normalSubtotal = CalculateTotalCost();
            return normalSubtotal * (effectiveDiscount / 100m);
        }

        public override string GetServiceItemDetail()
        {
            return $"[SPAREPART] {ItemName} ({Brand}) | Stok: {StockQuantity} | Rak: {RackLocation} | Harga: Rp {UnitPrice:N0}";
        }
    }
}
