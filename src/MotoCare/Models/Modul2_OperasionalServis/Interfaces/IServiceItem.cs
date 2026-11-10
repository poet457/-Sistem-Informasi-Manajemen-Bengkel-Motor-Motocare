using System;

namespace MotoCare.Models.Modul2_OperasionalServis.Interfaces
{
    /// <summary>
    /// Modul 2: Operasional Servis & Inventaris
    /// Penanggung Jawab: Putrana Yudhistira
    /// 
    /// Interface IServiceItem mendefinisikan kontrak bagi seluruh item yang dapat dimasukkan
    /// ke dalam nota kerja servis (baik jasa servis maupun suku cadang/sparepart).
    /// Mengimplementasikan: INTERFACE dalam OOP C#.
    /// </summary>
    public interface IServiceItem
    {
        // Property contract
        string ItemCode { get; set; }
        string ItemName { get; set; }
        decimal UnitPrice { get; set; }
        int Quantity { get; set; }

        // Method contract
        decimal CalculateTotalCost();
        string GetServiceItemDetail();
    }
}
