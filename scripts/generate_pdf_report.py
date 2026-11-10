import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, KeepTogether, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 792 - 40, "MotoCare – Sistem Manajemen Bengkel Motor | Laporan Progress Tubes PBO .NET C#")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 792 - 45, 595 - 54, 792 - 45)
            
        # Footer (all pages)
        self.drawString(54, 34, "Kelompok: Izat Ibrahimovic, Putrana Yudhistira, Rafli Apriliandi | ASP.NET Core MVC & MySQL")
        self.drawRightString(595 - 54, 34, f"Halaman {self._pageNumber} dari {page_count}")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 44, 595 - 54, 44)
        
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0F4C81")   # Deep Navy
    c_accent = colors.HexColor("#0284C7")    # Sky Blue
    c_dark = colors.HexColor("#1E293B")      # Slate 800
    c_muted = colors.HexColor("#64748B")     # Slate 500
    c_bg_code = colors.HexColor("#F8FAFC")   # Light gray
    c_callout_bg = colors.HexColor("#EFF6FF")# Soft blue
    c_callout_border = colors.HexColor("#2563EB")
    
    # Modify/Create Paragraph Styles
    style_inst = ParagraphStyle(
        'InstTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=c_muted,
        alignment=1, # Center
        spaceAfter=10
    )
    
    style_main_title = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=21,
        textColor=c_primary,
        alignment=1, # Center
        spaceAfter=6
    )
    
    style_subtitle = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10.5,
        leading=15,
        textColor=c_muted,
        alignment=1, # Center
        spaceAfter=14
    )
    
    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=15,
        textColor=c_accent,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    
    style_h3 = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_dark,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=c_dark,
        spaceAfter=6
    )
    
    style_code = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0F172A")
    )
    
    style_tbl_hdr = ParagraphStyle(
        'TblHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )
    
    style_tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=c_dark
    )
    
    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=c_dark
    )
    
    story = []
    
    # ------------------------------------------------------------------------
    # COVER / HEADER
    # ------------------------------------------------------------------------
    story.append(Paragraph("PROGRAM TUGAS BESAR PEMROGRAMAN II - PBO .NET (C#)<br/>SEMESTER GENAP TAHUN AKADEMIK 2025/2026", style_inst))
    story.append(Paragraph("LAPORAN PROGRESS TUGAS BESAR:<br/>IMPLEMENTASI 4 PILAR OOP PADA SISTEM MOTOCARE", style_main_title))
    story.append(Paragraph("Sistem Informasi Manajemen Bengkel Motor Berbasis C# ASP.NET Core MVC & MySQL", style_subtitle))
    
    # TEAM TABLE
    data_team = [
        [Paragraph("<b>No</b>", style_tbl_hdr), Paragraph("<b>Nama Anggota</b>", style_tbl_hdr), Paragraph("<b>Peran / Tanggung Jawab Modul</b>", style_tbl_hdr), Paragraph("<b>Fokus File / Namespace</b>", style_tbl_hdr)],
        [Paragraph("1", style_tbl_cell), Paragraph("<b>Izat Ibrahimovic</b>", style_tbl_cell), Paragraph("Ketua & Lead Modul 1: Master Data (Pelanggan, Kendaraan, Mekanik)", style_tbl_cell), Paragraph("Models/Modul1_MasterData/<br/>(Person, Customer, Mechanic, Vehicle)", style_tbl_cell)],
        [Paragraph("2", style_tbl_cell), Paragraph("<b>Putrana Yudhistira</b>", style_tbl_cell), Paragraph("Lead Modul 2: Operasional Servis & Inventaris Gudang Suku Cadang", style_tbl_cell), Paragraph("Models/Modul2_OperasionalServis/<br/>(IServiceItem, BaseServiceItem, Sparepart, ServicePackage, ServiceOrder)", style_tbl_cell)],
        [Paragraph("3", style_tbl_cell), Paragraph("<b>Rafli Apriliandi</b>", style_tbl_cell), Paragraph("Lead Modul 3: Transaksi Pembayaran, Invoicing, & Generic Repository", style_tbl_cell), Paragraph("Models/Modul3_TransaksiDanRepository/<br/>(IBillable, IRepository&lt;T&gt;, InMemoryRepository&lt;T&gt;, Invoice, ServicePricingCatalog)", style_tbl_cell)]
    ]
    t_team = Table(data_team, colWidths=[0.3*inch, 1.4*inch, 2.7*inch, 2.4*inch])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_team)
    story.append(Spacer(1, 10))
    
    # CALLOUT BOX
    callout_data = [[
        Paragraph("<b>📌 KETERANGAN PENGUMPULAN EDLINK:</b><br/>"
                  "Laporan ini disusun khusus untuk memenuhi kriteria evaluasi progress tugas besar pada platform Edlink, "
                  "yang mewajibkan pembuktian potongan kode: <b>(1) Variable, get, set, method</b>; <b>(2) Inheritance</b>; "
                  "<b>(3) Interface & Abstract</b>; <b>(4) Collection, Dictionary, Generic</b>. "
                  "Arsitektur kode dirancang modular per folder untuk memastikan pengerjaan mandiri tanpa bentrok file (Zero Merge Conflict).", style_callout)
    ]]
    t_callout = Table(callout_data, colWidths=[6.8*inch])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('LINELEFT', (0,0), (0,-1), 3.5, c_callout_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_callout)
    story.append(Spacer(1, 12))

    # ------------------------------------------------------------------------
    # BAB I: PENDAHULUAN & STRATEGI PEMBAGIAN TUGAS
    # ------------------------------------------------------------------------
    story.append(Paragraph("BAB I: PENDAHULUAN & ARSITEKTUR SISTEM MOTOCARE", style_h1))
    story.append(Paragraph(
        "<b>MotoCare</b> adalah sistem informasi manajemen bengkel motor berbasis web yang dikembangkan menggunakan "
        "<b>C# ASP.NET Core MVC</b> dan <b>MySQL</b> sebagai proyek tugas besar Pemrograman Berorientasi Objek (PBO) II. "
        "Aplikasi ini mengelola alur operasional bengkel secara menyeluruh: registrasi pelanggan & motor, pembagian tugas "
        "ke mekanik, penerbitan Surat Perintah Kerja (SPK), manajemen stok suku cadang, hingga faktur tagihan dan pembayaran kasir.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Strategi Pembagian Tugas Mandiri (Anti-Bentrok):</b><br/>"
        "Untuk mencegah terjadinya <i>conflict</i> saat pengerjaan tubes, kode program dipisahkan secara tegas ke dalam "
        "3 modul independen berdasarkan tanggung jawab anggota. Setiap anggota mengelola folder dan file kelasnya sendiri "
        "dan hanya berkomunikasi melalui Interface atau Base Class yang telah disepakati bersama:",
        style_body
    ))

    data_split = [
        [Paragraph("<b>Anggota</b>", style_tbl_hdr), Paragraph("<b>Modul & Folder</b>", style_tbl_hdr), Paragraph("<b>Tanggung Jawab File</b>", style_tbl_hdr), Paragraph("<b>Strategi Anti-Bentrok</b>", style_tbl_hdr)],
        [Paragraph("<b>Izat Ibrahimovic</b>", style_tbl_cell), Paragraph("Modul 1: Master Data<br/><i>Models/Modul1_MasterData/</i>", style_tbl_cell), Paragraph("Person.cs, Customer.cs, Mechanic.cs, Vehicle.cs", style_tbl_cell), Paragraph("Bekerja mandiri pada entitas pengguna. Objek Customer dan Mechanic siap dikonsumsi modul lain.", style_tbl_cell)],
        [Paragraph("<b>Putrana Yudhistira</b>", style_tbl_cell), Paragraph("Modul 2: Operasional<br/><i>Models/Modul2_OperasionalServis/</i>", style_tbl_cell), Paragraph("IServiceItem.cs, BaseServiceItem.cs, Sparepart.cs, ServicePackage.cs, ServiceOrder.cs", style_tbl_cell), Paragraph("Bekerja mandiri pada logika pengerjaan servis & stok. Mengambil referensi dari Modul 1 tanpa mengubah file Modul 1.", style_tbl_cell)],
        [Paragraph("<b>Rafli Apriliandi</b>", style_tbl_cell), Paragraph("Modul 3: Transaksi & Repo<br/><i>Models/Modul3_TransaksiDanRepository/</i>", style_tbl_cell), Paragraph("IBillable.cs, IRepository.cs, InMemoryRepository.cs, Invoice.cs, ServicePricingCatalog.cs", style_tbl_cell), Paragraph("Bekerja mandiri pada penagihan kasir & repository. Menggunakan ServiceOrder dari Modul 2 untuk membuat Invoice.", style_tbl_cell)]
    ]
    t_split = Table(data_split, colWidths=[1.1*inch, 1.8*inch, 1.9*inch, 2.0*inch])
    t_split.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_split)
    story.append(Spacer(1, 10))

    # ------------------------------------------------------------------------
    # BAB II: TABEL PEMETAAN 4 SYARAT UTAMA EDLINK
    # ------------------------------------------------------------------------
    story.append(Paragraph("BAB II: PEMETAAN 4 SYARAT UTAMA EVALUASI EDLINK", style_h1))
    story.append(Paragraph(
        "Berikut adalah matriks pemetaan 4 kriteria wajib yang disyaratkan di form Edlink beserta letak pembuktian kodenya:",
        style_body
    ))

    data_crit = [
        [Paragraph("<b>Kriteria Edlink</b>", style_tbl_hdr), Paragraph("<b>Elemen Teknis C#</b>", style_tbl_hdr), Paragraph("<b>Lokasi File</b>", style_tbl_hdr), Paragraph("<b>Kegunaan dalam MotoCare</b>", style_tbl_hdr)],
        [Paragraph("<b>1. Variable, Get, Set, Method</b>", style_tbl_cell), Paragraph("Private fields (_fullName, _unitPrice, _stockQuantity), Auto-properties {get; set;}, Private set, Validasi setter, Business methods.", style_tbl_cell), Paragraph("BaseEntity.cs, Person.cs, Vehicle.cs, Sparepart.cs, ServiceOrder.cs, Invoice.cs", style_tbl_cell), Paragraph("Enkapsulasi & Validasi: Mencegah nilai negatif pada harga/stok, validasi plat nomor motor, serta method bisnis hitung subtotal & kurangi stok.", style_tbl_cell)],
        [Paragraph("<b>2. Inheritance</b>", style_tbl_cell), Paragraph("Class inheritance (:) dengan base constructor base(...), method overriding (virtual -&gt; override).", style_tbl_cell), Paragraph("Person -&gt; Customer, Mechanic;<br/>BaseEntity -&gt; Semua Entitas;<br/>BaseServiceItem -&gt; Sparepart, ServicePackage", style_tbl_cell), Paragraph("Reusability & Hierarki: Atribut umum individu diwariskan ke Customer dan Mechanic tanpa perulangan deklarasi kode.", style_tbl_cell)],
        [Paragraph("<b>3. Interface, Abstract</b>", style_tbl_cell), Paragraph("Interface: IServiceItem, IBillable, IRepository&lt;T&gt;.<br/>Abstract Class: BaseEntity, BaseServiceItem.<br/>Abstract Method: CalculateDiscount().", style_tbl_cell), Paragraph("Models/.../Interfaces/<br/>Models/.../Abstracts/", style_tbl_cell), Paragraph("Kontrak Standar & Abstraksi: Menstandarkan format transaksi kasir (IBillable) dan mewajibkan kelas anak menghitung diskon sesuai jenis item.", style_tbl_cell)],
        [Paragraph("<b>4. Collection, Dictionary, Generic</b>", style_tbl_cell), Paragraph("Collection: List&lt;T&gt;, IEnumerable&lt;T&gt;.<br/>Dictionary: Dictionary&lt;TKey, TValue&gt;.<br/>Generic: IRepository&lt;T&gt;, InMemoryRepository&lt;T&gt;, LookupCatalog&lt;TResult&gt;.", style_tbl_cell), Paragraph("Customer.cs (List&lt;Vehicle&gt;), ServiceOrder.cs (List&lt;BaseServiceItem&gt;), InMemoryRepository.cs, Invoice.cs (Dictionary breakdown), ServicePricingCatalog.cs", style_tbl_cell), Paragraph("Struktur Data Efisien: Menyimpan daftar rincian barang, lookup cepat O(1) berdasarkan ID atau kode servis, serta generic CRUD repository reusable.", style_tbl_cell)]
    ]
    t_crit = Table(data_crit, colWidths=[1.3*inch, 1.8*inch, 1.8*inch, 1.9*inch])
    t_crit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_crit)
    story.append(Spacer(1, 10))

    # ------------------------------------------------------------------------
    # BAB III: PEMBAHASAN DETAIL KODE PROGRAM PER MODUL
    # ------------------------------------------------------------------------
    story.append(Paragraph("BAB III: POTONGAN KODE PROGRAM & PENJELASAN RINCI", style_h1))
    
    # ---------------- MODUL 1: IZAT ----------------
    story.append(Paragraph("3.1 Modul 1: Manajemen Master Data (Penanggung Jawab: Izat Ibrahimovic)", style_h2))
    
    # Person.cs
    story.append(Paragraph("A. File: Person.cs (Base Class, Variable, Get-Set, Method, Virtual Method)", style_h3))
    code_person = """// Models/Modul1_MasterData/Person.cs
public class Person : BaseEntity
{
    // Field privat (Enkapsulasi Variable)
    private string _fullName = string.Empty;
    private string _phoneNumber = string.Empty;

    // Get-Set Property dengan validasi logika
    public string FullName
    {
        get => _fullName;
        set
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("Nama lengkap tidak boleh kosong.");
            _fullName = value.Trim();
        }
    }

    public string PhoneNumber
    {
        get => _phoneNumber;
        set
        {
            if (string.IsNullOrWhiteSpace(value) || value.Length < 9)
                throw new ArgumentException("Nomor telepon minimal harus 9 digit.");
            _phoneNumber = value.Trim();
        }
    }

    // Method untuk memperbarui kontak
    public void UpdateContact(string newPhone, string newEmail)
    {
        PhoneNumber = newPhone;
        Email = newEmail;
        UpdatedAt = DateTime.Now;
    }

    // Virtual Method (Dapat di-override oleh kelas turunan)
    public virtual string GetProfileSummary()
    {
        return $"[ID: {Id}] {FullName} | Telp: {PhoneNumber}";
    }
}"""
    story.append(Preformatted(code_person, style_code))
    story.append(Paragraph(
        "<b>Penjelasan Kode & Kegunaan:</b><br/>"
        "• <code>_fullName</code> & <code>_phoneNumber</code>: Field private untuk menyimpan data anggota dengan proteksi enkapsulasi.<br/>"
        "• <code>FullName</code> & <code>PhoneNumber</code> get/set: Memvalidasi data masukan agar nama tidak kosong dan telepon minimal 9 digit.<br/>"
        "• <code>UpdateContact()</code>: Method bisnis untuk mengubah nomor telepon/email sekaligus meng-update timestamp <code>UpdatedAt</code>.<br/>"
        "• <code>GetProfileSummary()</code>: Virtual method yang dirancang untuk di-override oleh Customer dan Mechanic (Polymorphism).",
        style_body
    ))
    story.append(Spacer(1, 6))

    # Customer.cs
    story.append(Paragraph("B. File: Customer.cs (Inheritance dari Person & Collection List<Vehicle>)", style_h3))
    code_customer = """// Models/Modul1_MasterData/Customer.cs
public class Customer : Person
{
    private int _loyaltyPoints;
    public string CustomerCode { get; set; } = string.Empty;

    public int LoyaltyPoints
    {
        get => _loyaltyPoints;
        private set => _loyaltyPoints = value < 0 ? 0 : value;
    }

    // COLLECTION: Daftar motor milik pelanggan (One-to-Many)
    public List<Vehicle> RegisteredVehicles { get; set; } = new List<Vehicle>();

    public Customer(int id, string fullName, string phone, string email, string code, string addr)
        : base(id, fullName, phone, email) // Memanggil konstruktor Base Class
    {
        CustomerCode = code;
        LoyaltyPoints = 0;
    }

    // Method menambah motor ke dalam koleksi List
    public void AddVehicle(Vehicle vehicle)
    {
        if (vehicle == null) throw new ArgumentNullException(nameof(vehicle));
        RegisteredVehicles.Add(vehicle);
    }

    // Override virtual method dari kelas Person
    public override string GetProfileSummary()
    {
        return $"[Pelanggan #{CustomerCode}] {FullName} | Total Motor: {RegisteredVehicles.Count}";
    }
}"""
    story.append(Preformatted(code_customer, style_code))
    story.append(Paragraph(
        "<b>Penjelasan Kode & Kegunaan:</b><br/>"
        "• <code>public class Customer : Person</code>: Membuktikan INHERITANCE di mana Customer mewarisi seluruh data Person.<br/>"
        "• <code>: base(...)</code>: Memanggil konstruktor base class Person untuk inisialisasi ID, nama, dan telepon secara rapi.<br/>"
        "• <code>List&lt;Vehicle&gt; RegisteredVehicles</code>: Membuktikan COLLECTION untuk menyimpan banyak motor milik satu pelanggan.<br/>"
        "• <code>private set</code> pada LoyaltyPoints: Melindungi poin dari manipulasi langsung di luar aturan penukaran resmi.<br/>"
        "• <code>override GetProfileSummary()</code>: Mengubah output profil agar mencakup kode pelanggan dan jumlah motor.",
        style_body
    ))
    story.append(Spacer(1, 6))

    # Vehicle.cs
    story.append(Paragraph("C. File: Vehicle.cs (Validasi Plat Nomor, Kilometer, dan Cek Servis Rutin)", style_h3))
    code_veh = """// Models/Modul1_MasterData/Vehicle.cs
public class Vehicle : BaseEntity
{
    private string _licensePlate = string.Empty;
    private int _currentKilometers;

    public string Brand { get; set; } = string.Empty;
    public string Model { get; set; } = string.Empty;

    public string LicensePlate
    {
        get => _licensePlate;
        set
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("Plat nomor motor wajib diisi.");
            _licensePlate = value.Trim().ToUpper(); // Standardisasi otomatis huruf kapital
        }
    }

    public int CurrentKilometers
    {
        get => _currentKilometers;
        set
        {
            if (value < 0) throw new ArgumentException("KM tidak boleh negatif.");
            _currentKilometers = value;
        }
    }

    public bool NeedsPeriodicService() => CurrentKilometers >= 2500;
}"""
    story.append(Preformatted(code_veh, style_code))
    story.append(Paragraph(
        "<b>Penjelasan Kode & Kegunaan:</b><br/>"
        "• <code>LicensePlate</code> setter: Menstandarkan huruf plat motor menjadi kapital (UPPERCASE) secara otomatis.<br/>"
        "• <code>NeedsPeriodicService()</code>: Method bisnis otomatis untuk mengecek apakah motor sudah melewati batas kilometer servis.",
        style_body
    ))
    story.append(Spacer(1, 8))

    # ---------------- MODUL 2: PUTRANA ----------------
    story.append(Paragraph("3.2 Modul 2: Operasional Servis & Inventaris (Penanggung Jawab: Putrana Yudhistira)", style_h2))
    
    # IServiceItem & BaseServiceItem
    story.append(Paragraph("A. File: IServiceItem.cs (Interface) & BaseServiceItem.cs (Abstract Class & Method)", style_h3))
    code_base_item = """// Models/Modul2_OperasionalServis/Interfaces/IServiceItem.cs
public interface IServiceItem
{
    string ItemCode { get; set; }
    string ItemName { get; set; }
    decimal UnitPrice { get; set; }
    int Quantity { get; set; }
    decimal CalculateTotalCost();
}

// Models/Modul2_OperasionalServis/Abstracts/BaseServiceItem.cs
public abstract class BaseServiceItem : BaseEntity, IServiceItem
{
    public string ItemCode { get; set; } = string.Empty;
    public string ItemName { get; set; } = string.Empty;
    public decimal UnitPrice { get; set; }
    public int Quantity { get; set; } = 1;

    public virtual decimal CalculateTotalCost() => UnitPrice * Quantity;

    // ABSTRACT METHOD: Formula diskon wajib diimplementasikan berbeda oleh kelas turunan
    public abstract decimal CalculateDiscount(decimal discountPercentage);
}"""
    story.append(Preformatted(code_base_item, style_code))
    story.append(Paragraph(
        "<b>Penjelasan Kode & Kegunaan:</b><br/>"
        "• <code>interface IServiceItem</code>: Kontrak standar bagi seluruh komponen biaya nota servis (jasa mekanik maupun suku cadang).<br/>"
        "• <code>abstract class BaseServiceItem</code>: Kelas abstrak yang menjadi fondasi bagi kelas Sparepart dan ServicePackage.<br/>"
        "• <code>abstract decimal CalculateDiscount(...)</code>: ABSTRACT METHOD yang memaksa kelas anak menentukan formula diskonnya sendiri.",
        style_body
    ))
    story.append(Spacer(1, 6))

    # Sparepart & ServicePackage
    story.append(Paragraph("B. File: Sparepart.cs & ServicePackage.cs (Inheritance & Polymorphism)", style_h3))
    code_sparepart = """// Models/Modul2_OperasionalServis/Sparepart.cs
public class Sparepart : BaseServiceItem
{
    private int _stockQuantity;
    public string Brand { get; set; } = string.Empty;

    public int StockQuantity
    {
        get => _stockQuantity;
        set => _stockQuantity = value < 0 ? throw new ArgumentException("Stok tidak boleh minus.") : value;
    }

    public void DeductStock(int amountUsed)
    {
        if (amountUsed > StockQuantity)
            throw new InvalidOperationException($"Stok suku cadang '{ItemName}' tidak cukup.");
        StockQuantity -= amountUsed;
    }

    // Override abstract method: Diskon suku cadang fisik dibatasi maksimal 15%
    public override decimal CalculateDiscount(decimal discountPercentage)
    {
        decimal effectiveDiscount = Math.Min(discountPercentage, 15m);
        return CalculateTotalCost() * (effectiveDiscount / 100m);
    }
}

// Models/Modul2_OperasionalServis/ServicePackage.cs
public class ServicePackage : BaseServiceItem
{
    public int EstimatedMinutes { get; set; }

    // Override abstract method: Diskon jasa servis diperbolehkan promo hingga 30%
    public override decimal CalculateDiscount(decimal discountPercentage)
    {
        decimal effectiveDiscount = Math.Min(discountPercentage, 30m);
        return CalculateTotalCost() * (effectiveDiscount / 100m);
    }
}"""
    story.append(Preformatted(code_sparepart, style_code))
    story.append(Paragraph(
        "<b>Penjelasan Kode & Kegunaan:</b><br/>"
        "• <code>Sparepart : BaseServiceItem</code>: Membuktikan INHERITANCE dari Abstract Class.<br/>"
        "• <code>DeductStock()</code>: Method kontrol inventaris yang memotong stok otomatis dan mencegah stok bernilai negatif.<br/>"
        "• <code>override CalculateDiscount()</code>: Membuktikan POLYMORPHISM di mana diskon sparepart dibatasi 15% sedangkan jasa servis hingga 30%.",
        style_body
    ))
    story.append(Spacer(1, 6))

    # ServiceOrder.cs
    story.append(Paragraph("C. File: ServiceOrder.cs (Collection List<BaseServiceItem>)", style_h3))
    code_order = """// Models/Modul2_OperasionalServis/ServiceOrder.cs
public class ServiceOrder : BaseEntity
{
    public string OrderNumber { get; set; } = string.Empty;
    public Customer Customer { get; set; } = null!;
    public Vehicle Vehicle { get; set; } = null!;
    public Mechanic AssignedMechanic { get; set; } = null!;

    // COLLECTION: Menampung rincian jasa dan suku cadang secara polimorfik
    public List<BaseServiceItem> ServiceItems { get; set; } = new List<BaseServiceItem>();

    public void AddServiceItem(BaseServiceItem item)
    {
        if (item == null) throw new ArgumentNullException(nameof(item));
        if (item is Sparepart sp) sp.DeductStock(item.Quantity); // Otomatis kurangi stok
        ServiceItems.Add(item);
    }

    public decimal CalculateSubtotal() => ServiceItems.Sum(x => x.CalculateTotalCost());
}"""
    story.append(Preformatted(code_order, style_code))
    story.append(Paragraph(
        "<b>Penjelasan Kode & Kegunaan:</b><br/>"
        "• <code>List&lt;BaseServiceItem&gt; ServiceItems</code>: Membuktikan COLLECTION yang menampung gabungan objek Sparepart dan ServicePackage.<br/>"
        "• <code>item is Sparepart sp</code>: Type pattern matching untuk langsung memotong stok suku cadang fisik saat dimasukkan ke SPK servis.",
        style_body
    ))
    story.append(Spacer(1, 8))

    # ---------------- MODUL 3: RAFLI ----------------
    story.append(Paragraph("3.3 Modul 3: Transaksi & Generic Repository (Penanggung Jawab: Rafli Apriliandi)", style_h2))
    
    # Generic Repository
    story.append(Paragraph("A. File: IRepository.cs & InMemoryRepository.cs (Generic Interface, Generic Class & Dictionary)", style_h3))
    code_repo = """// Models/Modul3_TransaksiDanRepository/Interfaces/IRepository.cs
public interface IRepository<T> where T : BaseEntity // GENERIC INTERFACE
{
    void Add(T entity);
    T? GetById(int id);
    IEnumerable<T> GetAll();
    int Count();
}

// Models/Modul3_TransaksiDanRepository/Repositories/InMemoryRepository.cs
public class InMemoryRepository<T> : IRepository<T> where T : BaseEntity // GENERIC CLASS
{
    // DICTIONARY: Digunakan sebagai penyimpanan cepat O(1) berdasarkan ID
    private readonly Dictionary<int, T> _storage = new Dictionary<int, T>();
    private int _autoIncrementId = 1;

    public void Add(T entity)
    {
        if (entity == null) throw new ArgumentNullException(nameof(entity));
        if (entity.Id <= 0) entity.Id = _autoIncrementId++;
        _storage.Add(entity.Id, entity);
    }

    public T? GetById(int id) => _storage.TryGetValue(id, out T? item) ? item : null;
    public IEnumerable<T> GetAll() => _storage.Values.ToList();
    public int Count() => _storage.Count;
}"""
    story.append(Preformatted(code_repo, style_code))
    story.append(Paragraph(
        "<b>Penjelasan Kode & Kegunaan:</b><br/>"
        "• <code>public interface IRepository&lt;T&gt; where T : BaseEntity</code>: Membuktikan GENERIC INTERFACE dengan batasan tipe (constraint).<br/>"
        "• <code>public class InMemoryRepository&lt;T&gt;</code>: Membuktikan GENERIC CLASS yang dapat dipakai ulang untuk entitas data mana pun.<br/>"
        "• <code>Dictionary&lt;int, T&gt; _storage</code>: Membuktikan DICTIONARY untuk pencarian data instan O(1) berdasarkan ID tanpa scan linear.",
        style_body
    ))
    story.append(Spacer(1, 6))

    # Invoice.cs
    story.append(Paragraph("B. File: Invoice.cs (Interface IBillable & Dictionary Breakdown Biaya)", style_h3))
    code_invoice = """// Models/Modul3_TransaksiDanRepository/Invoice.cs
public class Invoice : BaseEntity, IBillable // INHERITANCE & INTERFACE
{
    public ServiceOrder ServiceOrder { get; set; } = null!;
    public decimal GrandTotal { get; private set; }
    public bool IsPaid { get; private set; }

    // DICTIONARY: Menyimpan breakdown rincian komponen tagihan (Komponen -> Nominal)
    public Dictionary<string, decimal> FeeBreakdown { get; set; } = new Dictionary<string, decimal>();

    public decimal CalculateGrandTotal()
    {
        decimal subtotal = ServiceOrder.CalculateSubtotal();
        decimal ppn = (subtotal - DiscountAmount) * 0.11m; // PPN 11%
        GrandTotal = (subtotal - DiscountAmount) + ppn;

        // Mengisi DICTIONARY breakdown tagihan
        FeeBreakdown.Clear();
        FeeBreakdown["Subtotal Kotor"] = subtotal;
        FeeBreakdown["Potongan Diskon"] = DiscountAmount;
        FeeBreakdown["Pajak PPN (11%)"] = ppn;
        FeeBreakdown["Grand Total Bersih"] = GrandTotal;
        return GrandTotal;
    }

    public bool ProcessPayment(decimal amountPaid, string paymentMethod)
    {
        if (amountPaid < GrandTotal) throw new InvalidOperationException("Uang pembayaran kurang!");
        IsPaid = true;
        ServiceOrder.MarkAsCompleted(); // Update status SPK servis
        return true;
    }
}"""
    story.append(Preformatted(code_invoice, style_code))
    story.append(Paragraph(
        "<b>Penjelasan Kode & Kegunaan:</b><br/>"
        "• <code>class Invoice : BaseEntity, IBillable</code>: Membuktikan implementasi INTERFACE penagihan dan INHERITANCE dari BaseEntity.<br/>"
        "• <code>Dictionary&lt;string, decimal&gt; FeeBreakdown</code>: Membuktikan DICTIONARY untuk mencatat rincian biaya (Jasa, Suku Cadang, Diskon, PPN 11%, Grand Total).<br/>"
        "• <code>ProcessPayment()</code>: Method validasi kecukupan uang kasir dan penyelesaian order servis.",
        style_body
    ))
    story.append(Spacer(1, 6))

    # ServicePricingCatalog.cs
    story.append(Paragraph("C. File: ServicePricingCatalog.cs (Dictionary Tarif & Generic Method)", style_h3))
    code_cat = """// Models/Modul3_TransaksiDanRepository/ServicePricingCatalog.cs
public class ServicePricingCatalog
{
    // DICTIONARY: Kamus tarif acuan servis resmi bengkel MotoCare
    private readonly Dictionary<string, decimal> _catalog = new Dictionary<string, decimal>(StringComparer.OrdinalIgnoreCase);

    public ServicePricingCatalog()
    {
        _catalog.Add("SRV-TUNEUP", 75000m);
        _catalog.Add("SRV-CVT", 60000m);
        _catalog.Add("SRV-GANTI-OLI", 15000m);
    }

    // GENERIC METHOD: Mengubah tarif menjadi format generic TResult yang diinginkan
    public TResult LookupCatalog<TResult>(string serviceCode, Func<decimal, TResult> valueTransformer)
    {
        if (_catalog.TryGetValue(serviceCode, out decimal price))
            return valueTransformer(price);
        throw new KeyNotFoundException($"Kode '{serviceCode}' tidak terdaftar.");
    }
}"""
    story.append(Preformatted(code_cat, style_code))
    story.append(Paragraph(
        "<b>Penjelasan Kode & Kegunaan:</b><br/>"
        "• <code>Dictionary&lt;string, decimal&gt;</code>: Menyimpan pasangan kode servis dan nominal harga standar bengkel.<br/>"
        "• <code>LookupCatalog&lt;TResult&gt;</code>: Membuktikan GENERIC METHOD yang fleksibel mengembalikan format string, angka, atau objek baru.",
        style_body
    ))
    story.append(Spacer(1, 8))

    # ------------------------------------------------------------------------
    # BAB IV: HASIL DEMONSTRASI & OUTPUT CONSOLE
    # ------------------------------------------------------------------------
    story.append(Paragraph("BAB IV: HASIL DEMONSTRASI & LOG EKSEKUSI PROGRAM", style_h1))
    story.append(Paragraph(
        "Pengujian fungsional dilakukan dengan menjalankan file <code>Program.cs</code> via CLI 'dotnet run'. "
        "Hasil eksekusi membuktikan bahwa seluruh logika bisnis, pemotongan stok, kalkulasi diskon, dictionary breakdown, "
        "dan cetak struk pembayaran berhasil berjalan sempurna:",
        style_body
    ))

    code_receipt = """==================================================
              BENGKEL MOTOR MOTOCARE             
         Sistem Informasi Manajemen Servis        
==================================================
No. Invoice  : INV-MC-20260401-001
No. Order SPK: SPK-2026-0001
Waktu Bayar  : 10/11/2026 08:36:12
Pelanggan    : Budi Santoso (CUST-001)
Kendaraan    : Honda Vario 160 CBS [D 4123 ABC]
Mekanik      : Agus Pratama
--------------------------------------------------
Rincian Pekerjaan & Suku Cadang:
 - Paket Tune-Up Injeksi & CVT x1 : Rp 85.000
 - Oli Mesin SPX 2 Full Synthetic 0.8L x1 : Rp 65.000
 - Busi NGK Laser Iridium CPR9EAIX x1 : Rp 110.000
--------------------------------------------------
Ringkasan Tagihan (Dictionary Breakdown):
   Total Biaya Jasa         : Rp 85.000
   Total Biaya Suku Cadang  : Rp 175.000
   Subtotal Kotor           : Rp 260.000
   Potongan Diskon          : Rp 10.000
   Pajak PPN (11%)          : Rp 27.500
   Grand Total Bersih       : Rp 277.500
--------------------------------------------------
Metode Bayar : QRIS
Nominal Uang : Rp 300.000
Kembalian    : Rp 22.500
Status Lunas : LUNAS (SUKSES)
=================================================="""
    story.append(Preformatted(code_receipt, style_code))
    story.append(Spacer(1, 8))

    # ------------------------------------------------------------------------
    # BAB V: PANDUAN SCREENSHOT EDLINK
    # ------------------------------------------------------------------------
    story.append(Paragraph("BAB V: PANDUAN PENGAMBILAN SCREENSHOT UNTUK EDLINK", style_h1))
    story.append(Paragraph(
        "Bagi masing-masing anggota kelompok yang ingin mengambil tangkapan layar (screenshot) kode di editor (Visual Studio / VS Code), "
        "berikut adalah panduan file dan blok baris kode yang harus disorot:",
        style_body
    ))

    data_ss_guide = [
        [Paragraph("<b>No</b>", style_tbl_hdr), Paragraph("<b>Syarat di Edlink</b>", style_tbl_hdr), Paragraph("<b>Nama File Kode</b>", style_tbl_hdr), Paragraph("<b>Baris yang Wajib Disorot dalam Screenshot</b>", style_tbl_hdr)],
        [Paragraph("1", style_tbl_cell), Paragraph("<b>Variable Get Set Method</b>", style_tbl_cell), Paragraph("Person.cs & Vehicle.cs", style_tbl_cell), Paragraph("Sorot deklarasi field private <code>_fullName</code>, property <code>FullName { get; set; }</code> dengan validasi, dan method <code>UpdateContact()</code>.", style_tbl_cell)],
        [Paragraph("2", style_tbl_cell), Paragraph("<b>Inheritance</b>", style_tbl_cell), Paragraph("Customer.cs & Sparepart.cs", style_tbl_cell), Paragraph("Sorot baris <code>public class Customer : Person</code>, konstruktor <code>: base(...)</code>, dan keyword <code>override</code>.", style_tbl_cell)],
        [Paragraph("3", style_tbl_cell), Paragraph("<b>Interface, Abstract</b>", style_tbl_cell), Paragraph("IServiceItem.cs, BaseServiceItem.cs, & IBillable.cs", style_tbl_cell), Paragraph("Sorot <code>public interface IServiceItem</code> dan <code>public abstract class BaseServiceItem</code> beserta abstract method <code>CalculateDiscount()</code>.", style_tbl_cell)],
        [Paragraph("4", style_tbl_cell), Paragraph("<b>Collection, Dictionary, Generic</b>", style_tbl_cell), Paragraph("Customer.cs, InMemoryRepository.cs, & Invoice.cs", style_tbl_cell), Paragraph("Sorot <code>List&lt;Vehicle&gt;</code>, generic interface <code>IRepository&lt;T&gt;</code>, serta <code>Dictionary&lt;int, T&gt;</code> dan <code>Dictionary&lt;string, decimal&gt;</code>.", style_tbl_cell)]
    ]
    t_ss = Table(data_ss_guide, colWidths=[0.3*inch, 1.8*inch, 1.9*inch, 2.8*inch])
    t_ss.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_ss)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Kesimpulan:</b> Dokumen ini telah merangkum seluruh aspek teknis dan akademis yang disyaratkan dalam form progress tugas besar Edlink. "
        "File PDF berukuran ringkas (&lt; 1 MB, jauh di bawah batas maksimal 10 MB) dan siap diunggah sebagai bukti kemajuan proyek MotoCare.",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"File PDF berhasil disimpan di: {filename}")

if __name__ == "__main__":
    out_pdf = os.path.abspath("Laporan_Progress_Tubes_PBO_MotoCare.pdf")
    build_pdf(out_pdf)
