using System;
using System.Collections.Generic;
using MotoCare.Models.Modul1_MasterData;
using MotoCare.Models.Modul2_OperasionalServis;
using MotoCare.Models.Modul2_OperasionalServis.Abstracts;
using MotoCare.Models.Modul3_TransaksiDanRepository;
using MotoCare.Models.Modul3_TransaksiDanRepository.Interfaces;
using MotoCare.Models.Modul3_TransaksiDanRepository.Repositories;

namespace MotoCare
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            Console.WriteLine("================================================================================");
            Console.WriteLine("         MOTOCARE - SISTEM INFORMASI MANAJEMEN BENGKEL MOTOR                   ");
            Console.WriteLine("               DEMONSTRASI IMPLEMENTASI OOP C# .NET                             ");
            Console.WriteLine("================================================================================");
            Console.WriteLine("Kelompok Tubes: Izat Ibrahimovic, Putrana Yudhistira, Rafli Apriliandi");
            Console.WriteLine("--------------------------------------------------------------------------------\n");

            // ========================================================================
            // 1. MODUL 1 (Izat Ibrahimovic): Master Data (Customer, Mechanic, Vehicle)
            // Konsep OOP: Inheritance (Person), Encapsulation (Variable, Get/Set, Method)
            // ========================================================================
            Console.WriteLine(">>> [MODUL 1 - IZAT IBRAHIMOVIC] Menyiapkan Master Data Customer & Mekanik...");
            
            Customer customer1 = new Customer(
                id: 1,
                fullName: "Budi Santoso",
                phoneNumber: "081234567890",
                email: "budi.santoso@gmail.com",
                customerCode: "CUST-001",
                address: "Jl. Merdeka No. 45, Bandung"
            );

            Vehicle motor1 = new Vehicle(
                id: 1,
                customerId: customer1.Id,
                licensePlate: "D 4123 ABC",
                brand: "Honda",
                model: "Vario 160 CBS",
                year: 2023,
                cc: 160,
                km: 12500
            );

            customer1.AddVehicle(motor1);

            Mechanic mechanic1 = new Mechanic(
                id: 1,
                fullName: "Agus Pratama",
                phoneNumber: "085678901234",
                email: "agus.mekanik@motocare.id",
                mechanicCode: "MEK-07",
                specialization: "Injeksi & Transmisi CVT",
                hourlyRate: 50000m
            );

            Console.WriteLine($"   * {customer1.GetProfileSummary()}");
            Console.WriteLine($"   * Info Kendaraan: {motor1.GetEntityInfo()} (Butuh servis? {motor1.NeedsPeriodicService()})");
            Console.WriteLine($"   * {mechanic1.GetProfileSummary()}");
            Console.WriteLine();

            // ========================================================================
            // 2. MODUL 2 (Putrana Yudhistira): Operasional Servis & Inventaris
            // Konsep OOP: Interface (IServiceItem), Abstract Class (BaseServiceItem),
            //             Inheritance (Sparepart, ServicePackage), Polymorphism
            // ========================================================================
            Console.WriteLine(">>> [MODUL 2 - PUTRANA YUDHISTIRA] Operasional Servis & Inventaris...");

            // Abstract class instances via derived classes
            BaseServiceItem paketTuneup = new ServicePackage(
                id: 101,
                packageCode: "PKG-01",
                packageName: "Paket Tune-Up Injeksi & CVT",
                fee: 85000m,
                estimatedMinutes: 45,
                serviceType: "Servis Berkala",
                description: "Pembersihan throttle body, cek roller CVT, pembersihan kampas ganda"
            );

            Sparepart oliMesin = new Sparepart(
                id: 201,
                partCode: "OIL-AHM-01",
                partName: "Oli Mesin SPX 2 Full Synthetic 0.8L",
                sellingPrice: 65000m,
                stockQty: 25,
                brand: "AHM Oil",
                location: "Rak Cairan A-02"
            );

            Sparepart busiIridium = new Sparepart(
                id: 202,
                partCode: "SPK-NGK-09",
                partName: "Busi NGK Laser Iridium CPR9EAIX",
                sellingPrice: 110000m,
                stockQty: 10,
                brand: "NGK",
                location: "Rak Kelistrikan B-01"
            );

            Console.WriteLine($"   * {paketTuneup.GetServiceItemDetail()}");
            Console.WriteLine($"   * {oliMesin.GetServiceItemDetail()}");
            Console.WriteLine($"   * {busiIridium.GetServiceItemDetail()}");

            // Membuat ServiceOrder dan mengisi Collection (List<BaseServiceItem>)
            ServiceOrder order1 = new ServiceOrder(
                id: 501,
                orderNumber: "SPK-2026-0001",
                customer: customer1,
                vehicle: motor1,
                mechanic: mechanic1,
                complaint: "Tarikan gas motor terasa berat dan mesin cepat panas"
            );

            // Menambahkan item ke koleksi order (stok sparepart otomatis berkurang via method)
            order1.AddServiceItem(paketTuneup);
            order1.AddServiceItem(oliMesin);
            order1.AddServiceItem(busiIridium);

            Console.WriteLine($"   * {order1.GetEntityInfo()}");
            Console.WriteLine($"   * Sisa stok oli setelah SPK: {oliMesin.StockQuantity} botol (Stok kritis? {oliMesin.IsStockLow()})");
            Console.WriteLine();

            // ========================================================================
            // 3. MODUL 3 (Rafli Apriliandi): Transaksi, Generic Repository & Dictionary
            // Konsep OOP: Generic Interface (IRepository<T>), Generic Class (InMemoryRepository<T>),
            //             Dictionary (FeeBreakdown, ServicePricingCatalog), Interface (IBillable)
            // ========================================================================
            Console.WriteLine(">>> [MODUL 3 - RAFLI APRILIANDI] Transaksi Pembayaran & Generic Repository...");

            // 3.1 Penggunaan Generic Repository (IRepository<T>)
            IRepository<ServiceOrder> orderRepo = new InMemoryRepository<ServiceOrder>("ServiceOrderRepo");
            orderRepo.Add(order1);
            Console.WriteLine($"   * Generic Repository: Berhasil menyimpan {orderRepo.Count()} SPK ke dalam InMemoryRepository<ServiceOrder>.");

            // 3.2 Penggunaan ServicePricingCatalog dengan Dictionary dan Generic Method
            ServicePricingCatalog catalog = new ServicePricingCatalog();
            string formattedPrice = catalog.LookupCatalog<string>("SRV-TUNEUP", p => $"Biaya Standar: Rp {p:N0}");
            Console.WriteLine($"   * Dictionary Pricing Catalog lookup 'SRV-TUNEUP': {formattedPrice}");

            // 3.3 Pembuatan Invoice & Perhitungan Dictionary Breakdown
            Invoice invoice1 = new Invoice(id: 901, invoiceNumber: "INV-MC-20260401-001", order: order1);

            // Simulasi penukaran poin pelanggan (Modul 1 + Modul 3 integration)
            customer1.AddLoyaltyPoints(20);
            if (customer1.RedeemPoints(20, out decimal discountReward))
            {
                invoice1.ApplyDiscount(discountReward);
                Console.WriteLine($"   * Diskon Loyalitas diterapkan: Rp {discountReward:N0}");
            }

            // Memproses Pembayaran via Interface IBillable
            IBillable bill = invoice1;
            bill.ProcessPayment(amountPaid: 300000m, paymentMethod: "QRIS");

            Console.WriteLine($"\n>>> CETAK HASIL STRUK PEMBAYARAN (IMPLEMENTASI IBILLABLE & DICTIONARY):\n");
            Console.WriteLine(bill.GenerateReceiptText());

            Console.WriteLine("================================================================================");
            Console.WriteLine(" SEMUA 4 KRITERIA OOP (VARIABLE GET/SET, INHERITANCE, INTERFACE/ABSTRACT,       ");
            Console.WriteLine(" COLLECTION/DICTIONARY/GENERIC) BERJALAN DENGAN SEMPURNA!                      ");
            Console.WriteLine("================================================================================");
        }
    }
}
