using System;
using System.Collections.Generic;

namespace MotoCare.Models.Modul3_TransaksiDanRepository
{
    /// <summary>
    /// Modul 3: Transaksi Pembayaran & Generic Repository
    /// Penanggung Jawab: Rafli Apriliandi
    /// 
    /// Kelas ServicePricingCatalog mengelola kamus harga standar jasa bengkel.
    /// Mengimplementasikan:
    /// 1. DICTIONARY (Dictionary<string, decimal> untuk mapping Kode Layanan -> Tarif)
    /// 2. GENERIC METHOD (LookupCatalog<TResult>)
    /// 3. COLLECTION (List, IReadOnlyDictionary)
    /// 4. Variable & Encapsulation
    /// </summary>
    public class ServicePricingCatalog
    {
        // DICTIONARY: Menyimpan daftar tarif standar pekerjaan bengkel MotoCare
        private readonly Dictionary<string, decimal> _catalog = new Dictionary<string, decimal>(StringComparer.OrdinalIgnoreCase);

        public ServicePricingCatalog()
        {
            // Inisialisasi data default kamus harga servis
            _catalog.Add("SRV-TUNEUP", 75000m);
            _catalog.Add("SRV-CVT", 60000m);
            _catalog.Add("SRV-GANTI-OLI", 15000m);
            _catalog.Add("SRV-OVERHAUL", 350000m);
            _catalog.Add("SRV-BRAKE", 30000m);
            _catalog.Add("SRV-INJEKTOR", 50000m);
        }

        // Method: Menambah tarif baru ke dalam Dictionary
        public void RegisterPrice(string serviceCode, decimal price)
        {
            if (string.IsNullOrWhiteSpace(serviceCode))
                throw new ArgumentException("Kode servis tidak boleh kosong.");

            if (price < 0)
                throw new ArgumentException("Tarif tidak boleh negatif.");

            _catalog[serviceCode.ToUpper()] = price;
        }

        // Method: Mengambil harga dari Dictionary dengan proteksi KeyError
        public decimal GetPrice(string serviceCode)
        {
            if (_catalog.TryGetValue(serviceCode.ToUpper(), out decimal price))
            {
                return price;
            }
            throw new KeyNotFoundException($"Kode layanan '{serviceCode}' tidak ditemukan di katalog harga bengkel.");
        }

        // GENERIC METHOD: Mengambil data tarif dan mengonversinya ke format generic TResult
        public TResult LookupCatalog<TResult>(string serviceCode, Func<decimal, TResult> valueTransformer)
        {
            decimal price = GetPrice(serviceCode);
            return valueTransformer(price);
        }

        // Mengambil seluruh kamus harga sebagai pasangan key-value
        public IReadOnlyDictionary<string, decimal> GetAllPrices()
        {
            return _catalog;
        }
    }
}
