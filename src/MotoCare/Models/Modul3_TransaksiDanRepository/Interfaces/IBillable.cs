using System;

namespace MotoCare.Models.Modul3_TransaksiDanRepository.Interfaces
{
    /// <summary>
    /// Modul 3: Transaksi Pembayaran & Generic Repository
    /// Penanggung Jawab: Rafli Apriliandi
    /// 
    /// Interface IBillable menentukan standar kontrak untuk setiap transaksi atau invoice
    /// yang dapat ditagihkan dan dibayar oleh pelanggan.
    /// Mengimplementasikan: INTERFACE dalam OOP C#.
    /// </summary>
    public interface IBillable
    {
        string InvoiceNumber { get; set; }
        decimal GrandTotal { get; }
        bool IsPaid { get; }
        DateTime? PaymentDate { get; }

        decimal CalculateGrandTotal();
        bool ProcessPayment(decimal amountPaid, string paymentMethod);
        string GenerateReceiptText();
    }
}
