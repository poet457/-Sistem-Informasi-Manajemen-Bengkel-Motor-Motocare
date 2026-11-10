using System;
using MotoCare.Models.Common;
using MotoCare.Models.Modul2_OperasionalServis.Interfaces;

namespace MotoCare.Models.Modul2_OperasionalServis.Abstracts
{
    /// <summary>
    /// Modul 2: Operasional Servis & Inventaris
    /// Penanggung Jawab: Putrana Yudhistira
    /// 
    /// Kelas BaseServiceItem merupakan ABSTRACT CLASS yang mengimplementasikan interface IServiceItem.
    /// Mengimplementasikan:
    /// 1. Abstract Class & Interface implementation
    /// 2. Variable (field private)
    /// 3. Get-Set Property dengan validasi bisnis
    /// 4. Abstract Method & Virtual Method
    /// </summary>
    public abstract class BaseServiceItem : BaseEntity, IServiceItem
    {
        // Field private backing fields
        private decimal _unitPrice;
        private int _quantity = 1;

        // Auto-implemented Properties
        public string ItemCode { get; set; } = string.Empty;
        public string ItemName { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;

        // Property Get-Set dengan validasi
        public decimal UnitPrice
        {
            get => _unitPrice;
            set
            {
                if (value < 0)
                    throw new ArgumentException("Harga satuan tidak boleh bernilai negatif.");
                _unitPrice = value;
            }
        }

        public int Quantity
        {
            get => _quantity;
            set
            {
                if (value <= 0)
                    throw new ArgumentException("Jumlah quantity item minimal harus 1.");
                _quantity = value;
            }
        }

        // Constructor
        protected BaseServiceItem()
        {
        }

        protected BaseServiceItem(int id, string itemCode, string itemName, decimal unitPrice, int quantity, string category)
        {
            Id = id;
            ItemCode = itemCode;
            ItemName = itemName;
            UnitPrice = unitPrice;
            Quantity = quantity;
            Category = category;
        }

        // Virtual method: Perhitungan dasar subtotal
        public virtual decimal CalculateTotalCost()
        {
            return UnitPrice * Quantity;
        }

        // Abstract method: Wajib diimplementasikan kelas turunan (aturan diskon berbeda antara Sparepart vs Servis)
        public abstract decimal CalculateDiscount(decimal discountPercentage);

        // Virtual method untuk menampilkan format detail
        public virtual string GetServiceItemDetail()
        {
            return $"[{ItemCode}] {ItemName} x {Quantity} @ Rp {UnitPrice:N0} = Rp {CalculateTotalCost():N0}";
        }

        // Implementasi abstract method dari BaseEntity
        public override string GetEntityInfo()
        {
            return $"Service Item: {ItemName} ({Category})";
        }
    }
}
