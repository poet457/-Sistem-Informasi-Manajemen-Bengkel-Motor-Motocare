using System;
using System.Collections.Generic;
using System.Text;
using MotoCare.Models.Common;
using MotoCare.Models.Modul2_OperasionalServis;
using MotoCare.Models.Modul2_OperasionalServis.Abstracts;
using MotoCare.Models.Modul3_TransaksiDanRepository.Interfaces;

namespace MotoCare.Models.Modul3_TransaksiDanRepository
{
    /// <summary>
    /// Modul 3: Transaksi Pembayaran & Generic Repository
    /// Penanggung Jawab: Rafli Apriliandi
    /// 
    /// Kelas Invoice merepresentasikan kuitansi dan transaksi pembayaran akhir servis di bengkel.
    /// Mengimplementasikan:
    /// 1. INTERFACE (IBillable)
    /// 2. INHERITANCE (BaseEntity)
    /// 3. DICTIONARY (Dictionary<string, decimal> untuk rincian biaya, pajak, dan diskon)
    /// 4. COLLECTION (Iterasi ServiceItems)
    /// 5. Variable & Get-Set Properties dengan validasi
    /// 6. Business Methods (Hitung Grand Total, Proses Pembayaran, Cetak Struk)
    /// </summary>
    public class Invoice : BaseEntity, IBillable
    {
        // Field private backing fields
        private string _invoiceNumber = string.Empty;
        private decimal _discountAmount;
        private decimal _amountPaid;

        // Auto-implemented Properties
        public ServiceOrder ServiceOrder { get; set; } = null!;
        public string PaymentMethod { get; set; } = "Tunai"; // Tunai, QRIS, Transfer Bank, Debit
        public bool IsPaid { get; private set; }
        public DateTime? PaymentDate { get; private set; }

        // DICTIONARY: Menyimpan breakdown rincian komponen tagihan (komponen biaya -> nominal)
        public Dictionary<string, decimal> FeeBreakdown { get; set; } = new Dictionary<string, decimal>();

        // Properties Get-Set dengan validasi
        public string InvoiceNumber
        {
            get => _invoiceNumber;
            set
            {
                if (string.IsNullOrWhiteSpace(value))
                    throw new ArgumentException("Nomor invoice tidak boleh kosong.");
                _invoiceNumber = value.Trim().ToUpper();
            }
        }

        public decimal DiscountAmount
        {
            get => _discountAmount;
            set
            {
                if (value < 0)
                    throw new ArgumentException("Nominal diskon tidak boleh negatif.");
                _discountAmount = value;
            }
        }

        public decimal GrandTotal { get; private set; }

        public decimal AmountPaid
        {
            get => _amountPaid;
            private set => _amountPaid = value;
        }

        // Constructor
        public Invoice()
        {
        }

        public Invoice(int id, string invoiceNumber, ServiceOrder order)
        {
            Id = id;
            InvoiceNumber = invoiceNumber;
            ServiceOrder = order ?? throw new ArgumentNullException(nameof(order));
            IsPaid = false;
            CalculateGrandTotal();
        }

        // Method: Menghitung total tagihan dengan rincian ke dalam Dictionary
        public decimal CalculateGrandTotal()
        {
            decimal totalJasa = 0m;
            decimal totalSparepart = 0m;

            foreach (BaseServiceItem item in ServiceOrder.ServiceItems)
            {
                if (item is Sparepart)
                    totalSparepart += item.CalculateTotalCost();
                else if (item is ServicePackage)
                    totalJasa += item.CalculateTotalCost();
            }

            decimal subtotal = totalJasa + totalSparepart;
            decimal ppn11Persen = (subtotal - DiscountAmount) > 0 ? (subtotal - DiscountAmount) * 0.11m : 0m;
            decimal grandTotal = Math.Max(0m, (subtotal - DiscountAmount) + ppn11Persen);

            GrandTotal = grandTotal;

            // Memperbarui isi DICTIONARY rincian biaya
            FeeBreakdown.Clear();
            FeeBreakdown["Total Biaya Jasa"] = totalJasa;
            FeeBreakdown["Total Biaya Suku Cadang"] = totalSparepart;
            FeeBreakdown["Subtotal Kotor"] = subtotal;
            FeeBreakdown["Potongan Diskon"] = DiscountAmount;
            FeeBreakdown["Pajak PPN (11%)"] = ppn11Persen;
            FeeBreakdown["Grand Total Bersih"] = grandTotal;

            return GrandTotal;
        }

        // Method: Menerapkan diskon promo atau penukaran poin
        public void ApplyDiscount(decimal discount)
        {
            DiscountAmount = discount;
            CalculateGrandTotal();
        }

        // Method: Memproses transaksi pembayaran pelanggan
        public bool ProcessPayment(decimal paymentAmount, string paymentMethod)
        {
            if (paymentAmount < GrandTotal)
            {
                throw new InvalidOperationException($"Uang pembayaran kurang! Total tagihan: Rp {GrandTotal:N0}, Dibayar: Rp {paymentAmount:N0}");
            }

            PaymentMethod = paymentMethod;
            AmountPaid = paymentAmount;
            IsPaid = true;
            PaymentDate = DateTime.Now;
            ServiceOrder.MarkAsCompleted();
            UpdatedAt = DateTime.Now;

            return true;
        }

        // Method: Mencetak struk tanda terima transaksi
        public string GenerateReceiptText()
        {
            StringBuilder sb = new StringBuilder();
            sb.AppendLine("==================================================");
            sb.AppendLine("              BENGKEL MOTOR MOTOCARE             ");
            sb.AppendLine("         Sistem Informasi Manajemen Servis        ");
            sb.AppendLine("==================================================");
            sb.AppendLine($"No. Invoice  : {InvoiceNumber}");
            sb.AppendLine($"No. Order SPK: {ServiceOrder.OrderNumber}");
            sb.AppendLine($"Waktu Bayar  : {(PaymentDate.HasValue ? PaymentDate.Value.ToString("dd/MM/yyyy HH:mm:ss") : "Belum Lunas")}");
            sb.AppendLine($"Pelanggan    : {ServiceOrder.Customer.FullName} ({ServiceOrder.Customer.CustomerCode})");
            sb.AppendLine($"Kendaraan    : {ServiceOrder.Vehicle.Brand} {ServiceOrder.Vehicle.Model} [{ServiceOrder.Vehicle.LicensePlate}]");
            sb.AppendLine($"Mekanik      : {ServiceOrder.AssignedMechanic.FullName}");
            sb.AppendLine("--------------------------------------------------");
            sb.AppendLine("Rincian Pekerjaan & Suku Cadang:");

            foreach (var item in ServiceOrder.ServiceItems)
            {
                sb.AppendLine($" - {item.ItemName} x{item.Quantity} : Rp {item.CalculateTotalCost():N0}");
            }

            sb.AppendLine("--------------------------------------------------");
            sb.AppendLine("Ringkasan Tagihan (Dictionary Breakdown):");
            foreach (KeyValuePair<string, decimal> entry in FeeBreakdown)
            {
                sb.AppendLine($"   {entry.Key.PadRight(25)}: Rp {entry.Value:N0}");
            }

            sb.AppendLine("--------------------------------------------------");
            sb.AppendLine($"Metode Bayar : {PaymentMethod}");
            sb.AppendLine($"Nominal Uang : Rp {AmountPaid:N0}");
            sb.AppendLine($"Kembalian    : Rp {(AmountPaid - GrandTotal):N0}");
            sb.AppendLine($"Status Lunas : {(IsPaid ? "LUNAS (SUKSES)" : "BELUM LUNAS")}");
            sb.AppendLine("==================================================");
            sb.AppendLine(" Terima kasih atas kepercayaan Anda di MotoCare!  ");
            sb.AppendLine("==================================================");

            return sb.ToString();
        }

        public override string GetEntityInfo()
        {
            return $"Invoice [{InvoiceNumber}] - Total: Rp {GrandTotal:N0} | Status: {(IsPaid ? "Lunas" : "Belum Bayar")}";
        }
    }
}
