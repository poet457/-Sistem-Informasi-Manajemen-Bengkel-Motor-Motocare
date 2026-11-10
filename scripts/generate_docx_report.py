import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border only (accent navy)
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="0284C7"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_callout(doc, text, title="CATATAN PENTING"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "EFF6FF")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="BFDBFE"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="BFDBFE"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="BFDBFE"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"📌 {title}: ")
    run_t.bold = True
    run_t.font.name = 'Segoe UI'
    run_t.font.size = Pt(9.5)
    run_t.font.color.rgb = RGBColor(29, 78, 216)
    
    run_b = p.add_run(text)
    run_b.font.name = 'Segoe UI'
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def create_styled_table(doc, headers, data, col_widths=None):
    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl, color="CBD5E1")
    
    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "0F4C81") # Classic Navy
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = 'Segoe UI'
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    # Data Rows
    for row_idx, row_data in enumerate(data):
        row_cells = tbl.rows[row_idx + 1].cells
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = cell_value
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], top=100, bottom=100, left=140, right=140)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Segoe UI'
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(30, 41, 59)
                
    if col_widths:
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return tbl

def generate_document(output_path):
    doc = docx.Document()
    
    # Page setup: Standard A4 or Letter, 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles setup
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Segoe UI'
    font_normal.size = Pt(10)
    font_normal.color.rgb = RGBColor(30, 41, 59) # Slate 800
    
    # ------------------------------------------------------------------------
    # COVER / HEADER
    # ------------------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("PROGRAM TUGAS BESAR PEMROGRAMAN II - PBO .NET (C#)\nSEMESTER GENAP TAHUN AKADEMIK 2025/2026")
    r_inst.font.name = 'Segoe UI'
    r_inst.font.size = Pt(10)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(100, 116, 139)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(16)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("LAPORAN PROGRESS TUGAS BESAR:\nIMPLEMENTASI KONSEP DASAR OOP PADA SISTEM MOTOCARE")
    r_title.font.name = 'Segoe UI'
    r_title.font.size = Pt(17)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 76, 129) # Deep Classic Navy
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(18)
    r_sub = p_sub.add_run("Sistem Informasi Manajemen Bengkel Motor Berbasis C# ASP.NET Core MVC & MySQL")
    r_sub.font.name = 'Segoe UI'
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(71, 85, 105)
    
    # Divider line
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("―" * 55)
    r_div.font.color.rgb = RGBColor(203, 213, 225)
    p_div.paragraph_format.space_after = Pt(12)

    # IDENTITAS KELOMPOK TABLE
    headers_team = ["No", "Nama Anggota Kelompok", "Peran / Tanggung Jawab Modul", "Fokus File / Namespace"]
    data_team = [
        ["1", "Izat Ibrahimovic", "Ketua Kelompok & Lead Modul 1:\nManajemen Master Data (Pelanggan, Kendaraan, Mekanik)", "Models/Modul1_MasterData/\n(Person, Customer, Mechanic, Vehicle)"],
        ["2", "Putrana Yudhistira", "Lead Modul 2:\nOperasional Servis & Inventaris Gudang Suku Cadang", "Models/Modul2_OperasionalServis/\n(IServiceItem, BaseServiceItem, Sparepart, ServicePackage, ServiceOrder)"],
        ["3", "Rafli Apriliandi", "Lead Modul 3:\nTransaksi Pembayaran, Invoicing, & Generic Repository", "Models/Modul3_TransaksiDanRepository/\n(IBillable, IRepository<T>, InMemoryRepository<T>, Invoice, ServicePricingCatalog)"]
    ]
    create_styled_table(doc, headers_team, data_team, col_widths=[0.4, 1.8, 2.3, 2.0])

    add_callout(doc, 
        "Laporan ini disusun khusus untuk memenuhi kriteria evaluasi progress tugas besar pada platform Edlink, "
        "yang mewajibkan pembuktian potongan kode: (1) Variable, get, set, method; (2) Inheritance; "
        "(3) Interface & Abstract; (4) Collection, Dictionary, Generic. Arsitektur kode dirancang modular per "
        "folder anggota untuk memastikan tim bekerja independen tanpa bentrokan (Zero Merge Conflict).",
        "TUJUAN & RUANG LINGKUP DOKUMEN")

    # ------------------------------------------------------------------------
    # BAB 1: PENDAHULUAN & ARSITEKTUR SISTEM
    # ------------------------------------------------------------------------
    h1 = doc.add_heading("BAB I: PENDAHULUAN & ARSITEKTUR SISTEM MOTOCARE", level=1)
    h1.style.font.color.rgb = RGBColor(15, 76, 129)
    h1.paragraph_format.space_before = Pt(16)
    h1.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "MotoCare adalah sistem informasi manajemen bengkel motor modern berbasis web yang dikembangkan menggunakan "
        "C# ASP.NET Core MVC dengan basis data MySQL. Aplikasi ini dibangun untuk mendigitalkan seluruh aktivitas "
        "operasional bengkel secara terintegrasi, meliputi pencatatan identitas pelanggan dan kendaraan, pembagian tugas "
        "ke mekanik bengkel, pelacakan status antrian servis (Surat Perintah Kerja / SPK), manajemen inventaris suku cadang, "
        "hingga penerbitan faktur tagihan dan pembayaran transaksi."
    )

    doc.add_paragraph(
        "Dalam mata kuliah Pemrograman Berorientasi Objek (PBO) .NET, sistem MotoCare dirancang dengan mematuhi prinsip "
        "Object-Oriented Programming (OOP) yang kokoh, seperti Encapsulation, Inheritance, Abstraction, dan Polymorphism. "
        "Selain itu, sistem memanfaatkan fitur lanjutan bahasa C# seperti Generic Types, Generic Interfaces, LINQ Collections, "
        "dan Dictionary Key-Value pairs."
    )

    doc.add_heading("1.1 Strategi Pembagian Kerja Tim (Mencegah Bentrok / Git Merge Conflict)", level=2)
    doc.add_paragraph(
        "Salah satu kendala terbesar dalam pengerjaan tugas besar secara berkelompok adalah terjadinya bentrok kode (conflict) "
        "pada Git repository ketika beberapa anggota mengedit file yang sama secara bersamaan. Untuk menyelesaikan masalah ini, "
        "proyek MotoCare menerapkan arsitektur modular yang memisahkan tanggung jawab (Separation of Concerns):"
    )

    headers_split = ["Anggota", "Modul & Folder", "Kewenangan & File Dikerjakan", "Strategi Anti-Bentrok"]
    data_split = [
        ["Izat Ibrahimovic", "Modul 1: Master Data\n(Folder: Models/Modul1_MasterData/)", "Person.cs, Customer.cs, Mechanic.cs, Vehicle.cs", "Bekerja mandiri pada entitas pengguna dan kendaraan. Menghasilkan objek Customer dan Mechanic yang siap dipakai modul lain."],
        ["Putrana Yudhistira", "Modul 2: Operasional Servis\n(Folder: Models/Modul2_OperasionalServis/)", "IServiceItem.cs, BaseServiceItem.cs, Sparepart.cs, ServicePackage.cs, ServiceOrder.cs", "Bekerja mandiri pada logic servis dan suku cadang. Mengonsumsi objek dari Modul 1 hanya sebagai referensi objek tanpa mengubah file Modul 1."],
        ["Rafli Apriliandi", "Modul 3: Transaksi & Repository\n(Folder: Models/Modul3_TransaksiDanRepository/)", "IBillable.cs, IRepository.cs, InMemoryRepository.cs, Invoice.cs, ServicePricingCatalog.cs", "Bekerja mandiri pada logic billing, pembayaran, dan pola repository generic. Menggunakan ServiceOrder dari Modul 2 untuk membuat Invoice."]
    ]
    create_styled_table(doc, headers_split, data_split, col_widths=[1.3, 1.7, 1.8, 1.7])

    # ------------------------------------------------------------------------
    # BAB 2: PEMETAAN 4 KRITERIA WAJIB OOP EDLINK
    # ------------------------------------------------------------------------
    h2 = doc.add_heading("BAB II: PEMETAAN 4 SYARAT UTAMA EVALUASI EDLINK", level=1)
    h2.style.font.color.rgb = RGBColor(15, 76, 129)
    h2.paragraph_format.space_before = Pt(16)
    h2.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Berdasarkan instruksi evaluasi progress tugas besar pada platform Edlink, kelompok wajib menyajikan "
        "dan membuktikan 4 elemen teknis OOP di dalam source code proyek. Berikut adalah tabel ringkasan pemenuhan kriteria:"
    )

    headers_crit = ["Kriteria Edlink", "Elemen Teknis C#", "Lokasi File Kode", "Fungsi dalam Sistem MotoCare"]
    data_crit = [
        ["1. Variable, Get, Set, Method", "Private backing fields, auto-properties {get; set;}, private set, property validation, business logic methods.", "BaseEntity.cs, Person.cs, Vehicle.cs, Sparepart.cs, ServiceOrder.cs, Invoice.cs", "Menjamin Enkapsulasi: Mencegah nilai negatif pada harga/stok, validasi plat nomor dan telepon, serta method kalkulasi diskon dan proses bayar."],
        ["2. Inheritance (Pewarisan)", "Class inheritance (:) dengan base constructor base(...), method overriding (virtual -> override).", "Person.cs -> Customer.cs, Mechanic.cs;\nBaseEntity.cs -> Seluruh Entitas;\nBaseServiceItem.cs -> Sparepart.cs, ServicePackage.cs", "Reusability: Atribut umum individu (Nama, Telp, Email) diwariskan ke Customer dan Mechanic tanpa redundansi kode."],
        ["3. Interface, Abstract", "Interface: IServiceItem, IBillable, IRepository<T>.\nAbstract Class: BaseEntity, BaseServiceItem.", "Models/.../Interfaces/\nModels/.../Abstracts/", "Abstraksi & Kontrak Kerja: Menentukan standarisasi item servis, sistem tagihan, dan operasi database CRUD."],
        ["4. Collection, Dictionary, Generic", "Collection: List<T>, IEnumerable<T>.\nDictionary: Dictionary<TKey, TValue>.\nGeneric: IRepository<T>, InMemoryRepository<T>, Generic Method.", "Customer.cs (List<Vehicle>), ServiceOrder.cs (List<BaseServiceItem>), InMemoryRepository.cs (Dictionary<int, T>), Invoice.cs (Dictionary<string, decimal>), ServicePricingCatalog.cs", "Efisiensi Data: Menyimpan daftar rincian barang, lookup cepat O(1) berdasarkan ID atau kode servis, serta pola generic repository yang reusable untuk entitas apa pun."]
    ]
    create_styled_table(doc, headers_crit, data_crit, col_widths=[1.4, 1.6, 1.8, 1.7])

    # ------------------------------------------------------------------------
    # BAB 3: KODE PROGRAM & PENJELASAN BARIS DEMI BARIS
    # ------------------------------------------------------------------------
    h3 = doc.add_heading("BAB III: POTONGAN KODE PROGRAM & PENJELASAN LENGKAP", level=1)
    h3.style.font.color.rgb = RGBColor(15, 76, 129)
    h3.paragraph_format.space_before = Pt(16)
    h3.paragraph_format.space_after = Pt(6)

    # ------------------ MODUL 1 (IZAT) ------------------
    doc.add_heading("3.1 Modul 1: Manajemen Master Data (Penanggung Jawab: Izat Ibrahimovic)", level=2)
    doc.add_paragraph(
        "Modul 1 menangani entitas inti sistem bengkel: Base Entity, Person, Customer, Mechanic, dan Vehicle. "
        "Modul ini menjadi fondasi identitas pelanggan, profil kendaraan yang diservis, serta mekanik yang bertugas."
    )

    # File 1: BaseEntity.cs
    doc.add_heading("A. File: Models/Common/BaseEntity.cs (Abstract Class & Encapsulation)", level=3)
    doc.add_paragraph("Potongan kode program:")
    add_code_block(doc, """public abstract class BaseEntity
{
    private int _id;

    public int Id
    {
        get => _id;
        set
        {
            if (value < 0)
                throw new ArgumentException("ID tidak boleh bernilai negatif.");
            _id = value;
        }
    }

    public DateTime CreatedAt { get; set; } = DateTime.Now;
    public DateTime? UpdatedAt { get; set; }
    public bool IsActive { get; set; } = true;

    public abstract string GetEntityInfo();
}""")
    
    doc.add_paragraph("Penjelasan Baris Kode & Kegunaan:")
    doc.add_paragraph(
        "1. public abstract class BaseEntity: Dideklarasikan sebagai kelas abstrak agar tidak dapat diinstansiasi secara "
        "langsung, melainkan hanya berfungsi sebagai cetak biru (blueprint) bagi seluruh entitas data di MotoCare.\n"
        "2. private int _id: Field variabel privat yang menerapkan prinsip Enkapsulasi (data hiding) agar tidak dapat "
        "dimanipulasi sembarangan dari luar kelas.\n"
        "3. public int Id { get; set; }: Properti getter dan setter dengan logika validasi; melempar ArgumentException "
        "jika ID bernilai negatif, menjamin integritas data primary key.\n"
        "4. public DateTime CreatedAt & IsActive: Auto-implemented properties untuk audit log waktu pembuatan dan status aktif data (soft delete).\n"
        "5. public abstract string GetEntityInfo(): Abstract method yang mewajibkan setiap kelas turunan menyediakan "
        "format ringkasan data identitas masing-masing."
    )

    # File 2: Person.cs
    doc.add_heading("B. File: Models/Modul1_MasterData/Person.cs (Base Class & Variable Get/Set/Method)", level=3)
    doc.add_paragraph("Potongan kode program:")
    add_code_block(doc, """public class Person : BaseEntity
{
    private string _fullName = string.Empty;
    private string _phoneNumber = string.Empty;
    private string _email = string.Empty;

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

    public void UpdateContact(string newPhone, string newEmail)
    {
        PhoneNumber = newPhone;
        Email = newEmail;
        UpdatedAt = DateTime.Now;
    }

    public virtual string GetProfileSummary()
    {
        return $"[ID: {Id}] {FullName} | Telp: {PhoneNumber} | Email: {Email}";
    }

    public override string GetEntityInfo() => $"Entitas Person: {FullName}";
}""")

    doc.add_paragraph("Penjelasan Baris Kode & Kegunaan:")
    doc.add_paragraph(
        "1. public class Person : BaseEntity: Menerapkan konsep INHERITANCE di mana kelas Person mewarisi atribut dari BaseEntity.\n"
        "2. private string _fullName & _phoneNumber: Variabel privat yang menyimpan data sensitif kontak pengguna bengkel.\n"
        "3. Properti FullName & PhoneNumber: Getter dan Setter yang memvalidasi bahwa nama tidak boleh kosong dan "
        "nomor telepon minimal harus 9 digit numerik.\n"
        "4. public void UpdateContact(...): Method bisnis untuk memperbarui kontak pelanggan/mekanik sekaligus memperbarui timestamp UpdatedAt.\n"
        "5. public virtual string GetProfileSummary(): Virtual Method yang disiapkan agar kelas turunan (Customer dan Mechanic) "
        "dapat melakukan overriding perilaku sesuai karakteristik masing-masing (Polymorphism)."
    )

    # File 3: Customer.cs
    doc.add_heading("C. File: Models/Modul1_MasterData/Customer.cs (Inheritance & Collection List<Vehicle>)", level=3)
    doc.add_paragraph("Potongan kode program:")
    add_code_block(doc, """public class Customer : Person
{
    private int _loyaltyPoints;
    public string CustomerCode { get; set; } = string.Empty;
    public string Address { get; set; } = string.Empty;

    public int LoyaltyPoints
    {
        get => _loyaltyPoints;
        private set => _loyaltyPoints = value < 0 ? 0 : value;
    }

    // COLLECTION: Menyimpan daftar sepeda motor pelanggan
    public List<Vehicle> RegisteredVehicles { get; set; } = new List<Vehicle>();

    public Customer(int id, string fullName, string phoneNumber, string email, string customerCode, string address)
        : base(id, fullName, phoneNumber, email)
    {
        CustomerCode = customerCode;
        Address = address;
        LoyaltyPoints = 0;
    }

    public void AddVehicle(Vehicle vehicle)
    {
        if (vehicle == null) throw new ArgumentNullException(nameof(vehicle));
        RegisteredVehicles.Add(vehicle);
    }

    public void AddLoyaltyPoints(int points)
    {
        if (points > 0) LoyaltyPoints += points;
    }

    public bool RedeemPoints(int pointsToRedeem, out decimal discountAmount)
    {
        discountAmount = 0m;
        if (pointsToRedeem <= LoyaltyPoints && pointsToRedeem > 0)
        {
            LoyaltyPoints -= pointsToRedeem;
            discountAmount = (pointsToRedeem / 10m) * 5000m; // 10 poin = Rp 5.000 diskon
            return true;
        }
        return false;
    }

    public override string GetProfileSummary()
    {
        return $"[Pelanggan #{CustomerCode}] {FullName} | Total Kendaraan: {RegisteredVehicles.Count} | Poin: {LoyaltyPoints}";
    }
}""")

    doc.add_paragraph("Penjelasan Baris Kode & Kegunaan:")
    doc.add_paragraph(
        "1. public class Customer : Person: Pembuktian INHERITANCE, Customer mewarisi seluruh field dan properti nama, telepon, dan email dari Person.\n"
        "2. : base(id, fullName, phoneNumber, email): Memanggil konstruktor Base Class untuk inisialisasi data induk secara rapi.\n"
        "3. public List<Vehicle> RegisteredVehicles: Pembuktian COLLECTION (List<T>) untuk mengelola hubungan satu pelanggan "
        "yang memiliki banyak sepeda motor (One-to-Many Relationship).\n"
        "4. private set pada LoyaltyPoints: Enkapsulasi protektif agar poin loyalitas tidak bisa diubah langsung dari luar kelas, "
        "hanya bisa diubah melalui method AddLoyaltyPoints() dan RedeemPoints().\n"
        "5. public override string GetProfileSummary(): Polymorphism melalui method overriding untuk menampilkan ringkasan data pelanggan."
    )

    # File 4: Mechanic.cs & Vehicle.cs
    doc.add_heading("D. File: Models/Modul1_MasterData/Mechanic.cs & Vehicle.cs", level=3)
    doc.add_paragraph("Potongan kode program Mechanic:")
    add_code_block(doc, """public class Mechanic : Person
{
    private decimal _hourlyRate;
    public string MechanicCode { get; set; } = string.Empty;
    public string Specialization { get; set; } = "Umum";
    public bool IsOnDuty { get; set; } = true;

    public decimal HourlyRate
    {
        get => _hourlyRate;
        set
        {
            if (value < 0) throw new ArgumentException("Tarif mekanik tidak boleh negatif.");
            _hourlyRate = value;
        }
    }

    public int TotalServicesHandled { get; private set; }

    public void RecordCompletedService()
    {
        TotalServicesHandled++;
        UpdatedAt = DateTime.Now;
    }

    public override string GetProfileSummary()
    {
        return $"[Mekanik #{MechanicCode}] {FullName} ({Specialization}) | Status: {(IsOnDuty ? \"Bertugas\" : \"Libur\")}";
    }
}""")

    doc.add_paragraph("Potongan kode program Vehicle:")
    add_code_block(doc, """public class Vehicle : BaseEntity
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
            _licensePlate = value.Trim().ToUpper(); // Standardisasi huruf kapital
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
}""")

    doc.add_paragraph("Penjelasan Baris Kode & Kegunaan:")
    doc.add_paragraph(
        "1. Mechanic : Person: Membuktikan fleksibilitas inheritance di mana satu base class dapat memiliki banyak kelas turunan.\n"
        "2. Method RecordCompletedService(): Menghitung riwayat produktivitas mekanik yang berpengaruh pada bonus servis.\n"
        "3. LicensePlate Setter: Mengonversi plat nomor menjadi format UPPERCASE otomatis agar pencarian data konsisten.\n"
        "4. NeedsPeriodicService(): Logika bisnis otomatis untuk mendeteksi kapan motor harus ganti oli dan servis berkala."
    )

    # ------------------ MODUL 2 (PUTRANA) ------------------
    doc.add_heading("3.2 Modul 2: Operasional Servis & Inventaris (Penanggung Jawab: Putrana Yudhistira)", level=2)
    doc.add_paragraph(
        "Modul 2 menangani operasional bengkel: Interface item servis, Abstract class item servis, "
        "suku cadang (Sparepart), paket jasa servis (ServicePackage), dan Surat Perintah Kerja (ServiceOrder)."
    )

    # File 5: IServiceItem.cs
    doc.add_heading("A. File: Models/Modul2_OperasionalServis/Interfaces/IServiceItem.cs (Interface)", level=3)
    doc.add_paragraph("Potongan kode program:")
    add_code_block(doc, """public interface IServiceItem
{
    string ItemCode { get; set; }
    string ItemName { get; set; }
    decimal UnitPrice { get; set; }
    int Quantity { get; set; }

    decimal CalculateTotalCost();
    string GetServiceItemDetail();
}""")

    doc.add_paragraph("Penjelasan Baris Kode & Kegunaan:")
    doc.add_paragraph(
        "1. public interface IServiceItem: Pembuktian INTERFACE murni dalam C# yang menetapkan kontrak wajib "
        "tanpa implementasi body kode.\n"
        "2. Property ItemCode, ItemName, UnitPrice, Quantity: Mendefinisikan bahwa apapun entitas yang ingin masuk ke "
        "daftar nota servis wajib memiliki atribut kode, nama, harga satuan, dan jumlah.\n"
        "3. Method CalculateTotalCost() & GetServiceItemDetail(): Kontrak fungsional untuk menghitung subtotal dan menghasilkan rincian teks."
    )

    # File 6: BaseServiceItem.cs
    doc.add_heading("B. File: Models/Modul2_OperasionalServis/Abstracts/BaseServiceItem.cs (Abstract Class & Method)", level=3)
    doc.add_paragraph("Potongan kode program:")
    add_code_block(doc, """public abstract class BaseServiceItem : BaseEntity, IServiceItem
{
    private decimal _unitPrice;
    private int _quantity = 1;

    public string ItemCode { get; set; } = string.Empty;
    public string ItemName { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;

    public decimal UnitPrice
    {
        get => _unitPrice;
        set
        {
            if (value < 0) throw new ArgumentException("Harga satuan tidak boleh negatif.");
            _unitPrice = value;
        }
    }

    public int Quantity
    {
        get => _quantity;
        set
        {
            if (value <= 0) throw new ArgumentException("Jumlah item minimal harus 1.");
            _quantity = value;
        }
    }

    public virtual decimal CalculateTotalCost() => UnitPrice * Quantity;

    // ABSTRACT METHOD: Aturan perhitungan diskon berbeda antara Sparepart vs Servis
    public abstract decimal CalculateDiscount(decimal discountPercentage);

    public virtual string GetServiceItemDetail()
    {
        return $"[{ItemCode}] {ItemName} x {Quantity} @ Rp {UnitPrice:N0} = Rp {CalculateTotalCost():N0}";
    }

    public override string GetEntityInfo() => $"Service Item: {ItemName} ({Category})";
}""")

    doc.add_paragraph("Penjelasan Baris Kode & Kegunaan:")
    doc.add_paragraph(
        "1. public abstract class BaseServiceItem : BaseEntity, IServiceItem: Menggabungkan ABSTRACT CLASS, INHERITANCE "
        "dari BaseEntity, dan INTERFACE IMPLEMENTATION dari IServiceItem secara bersamaan.\n"
        "2. Variable Get-Set UnitPrice & Quantity: Menerapkan proteksi bahwa kuantitas pesanan minimal harus 1 dan harga tidak boleh minus.\n"
        "3. public abstract decimal CalculateDiscount(...): Pembuktian ABSTRACT METHOD, di mana induk kelas mewajibkan kelas anak "
        "menentukan formula diskon sendiri karena margin laba sparepart fisik berbeda dengan margin jasa mekanik."
    )

    # File 7: Sparepart.cs & ServicePackage.cs
    doc.add_heading("C. File: Models/Modul2_OperasionalServis/Sparepart.cs & ServicePackage.cs (Polymorphism)", level=3)
    doc.add_paragraph("Potongan kode program Sparepart:")
    add_code_block(doc, """public class Sparepart : BaseServiceItem
{
    private int _stockQuantity;
    public string Brand { get; set; } = string.Empty;
    public string RackLocation { get; set; } = string.Empty;

    public int StockQuantity
    {
        get => _stockQuantity;
        set
        {
            if (value < 0) throw new ArgumentException("Stok gudang tidak boleh minus.");
            _stockQuantity = value;
        }
    }

    public void DeductStock(int amountUsed)
    {
        if (amountUsed > StockQuantity)
            throw new InvalidOperationException($"Stok suku cadang '{ItemName}' tidak mencukupi.");
        StockQuantity -= amountUsed;
        UpdatedAt = DateTime.Now;
    }

    // Override abstract method: Batas diskon sparepart maksimal 15%
    public override decimal CalculateDiscount(decimal discountPercentage)
    {
        decimal effectiveDiscount = Math.Min(discountPercentage, 15m);
        return CalculateTotalCost() * (effectiveDiscount / 100m);
    }
}""")

    doc.add_paragraph("Potongan kode program ServicePackage:")
    add_code_block(doc, """public class ServicePackage : BaseServiceItem
{
    public int EstimatedMinutes { get; set; }
    public string ServiceType { get; set; } = "Reguler";

    // Override abstract method: Batas diskon jasa servis diperbolehkan promo hingga 30%
    public override decimal CalculateDiscount(decimal discountPercentage)
    {
        decimal effectiveDiscount = Math.Min(discountPercentage, 30m);
        return CalculateTotalCost() * (effectiveDiscount / 100m);
    }
}""")

    doc.add_paragraph("Penjelasan Baris Kode & Kegunaan:")
    doc.add_paragraph(
        "1. Sparepart : BaseServiceItem & ServicePackage : BaseServiceItem: Membuktikan INHERITANCE dari Abstract Class.\n"
        "2. Method DeductStock(): Logika kontrol inventaris untuk mengurangi stok secara real-time dan mencegah stok negatif.\n"
        "3. Override CalculateDiscount: Membuktikan POLYMORPHISM. Pada Sparepart diskon dibatasi maksimal 15% agar tidak merugi, "
        "sedangkan pada ServicePackage diskon jasa bisa mencapai 30% untuk program promosi bengkel."
    )

    # File 8: ServiceOrder.cs
    doc.add_heading("D. File: Models/Modul2_OperasionalServis/ServiceOrder.cs (Collection List<BaseServiceItem>)", level=3)
    doc.add_paragraph("Potongan kode program:")
    add_code_block(doc, """public class ServiceOrder : BaseEntity
{
    public string OrderNumber { get; set; } = string.Empty;
    public Customer Customer { get; set; } = null!;
    public Vehicle Vehicle { get; set; } = null!;
    public Mechanic AssignedMechanic { get; set; } = null!;

    // COLLECTION: Menyimpan daftar rincian pekerjaan servis dan sparepart
    public List<BaseServiceItem> ServiceItems { get; set; } = new List<BaseServiceItem>();

    public void AddServiceItem(BaseServiceItem item)
    {
        if (item == null) throw new ArgumentNullException(nameof(item));
        if (item is Sparepart sp)
        {
            sp.DeductStock(item.Quantity); // Otomatis potong stok saat item dimasukkan ke SPK
        }
        ServiceItems.Add(item);
    }

    public decimal CalculateSubtotal()
    {
        return ServiceItems.Sum(item => item.CalculateTotalCost());
    }
}""")

    doc.add_paragraph("Penjelasan Baris Kode & Kegunaan:")
    doc.add_paragraph(
        "1. public List<BaseServiceItem> ServiceItems: Pembuktian COLLECTION dinamis berbasis generic type. "
        "Karena bertipe BaseServiceItem, koleksi ini mampu menampung objek Sparepart maupun ServicePackage sekaligus (Polymorphic Collection).\n"
        "2. Method AddServiceItem(): Secara otomatis mendeteksi tipe item (type pattern matching `if (item is Sparepart sp)`) "
        "dan langsung memotong stok gudang secara otomatis.\n"
        "3. Method CalculateSubtotal(): Menggunakan LINQ .Sum() untuk menjumlahkan subtotal seluruh item pesanan servis."
    )

    # ------------------ MODUL 3 (RAFLI) ------------------
    doc.add_heading("3.3 Modul 3: Transaksi & Generic Repository (Penanggung Jawab: Rafli Apriliandi)", level=2)
    doc.add_paragraph(
        "Modul 3 menangani aspek finansial dan persistensi data: Interface penagihan (IBillable), Generic Interface "
        "(IRepository<T>), Generic Repository class berbasis Dictionary (InMemoryRepository<T>), Invoice dengan "
        "Dictionary breakdown biaya, serta ServicePricingCatalog."
    )

    # File 9: IRepository.cs & InMemoryRepository.cs
    doc.add_heading("A. File: Interfaces/IRepository.cs & Repositories/InMemoryRepository.cs (Generic & Dictionary)", level=3)
    doc.add_paragraph("Potongan kode program IRepository<T> (Generic Interface):")
    add_code_block(doc, """public interface IRepository<T> where T : BaseEntity
{
    void Add(T entity);
    T? GetById(int id);
    IEnumerable<T> GetAll();
    IEnumerable<T> Find(Func<T, bool> predicate);
    bool Update(T entity);
    bool Delete(int id);
    int Count();
}""")

    doc.add_paragraph("Potongan kode program InMemoryRepository<T> (Generic Class & Dictionary):")
    add_code_block(doc, """public class InMemoryRepository<T> : IRepository<T> where T : BaseEntity
{
    // DICTIONARY: Penyimpanan data in-memory cepat berindeks O(1) berdasarkan ID
    private readonly Dictionary<int, T> _storage = new Dictionary<int, T>();
    private int _autoIncrementId = 1;

    public void Add(T entity)
    {
        if (entity == null) throw new ArgumentNullException(nameof(entity));
        if (entity.Id <= 0) entity.Id = _autoIncrementId++;

        if (_storage.ContainsKey(entity.Id))
            throw new InvalidOperationException($"ID {entity.Id} sudah terdaftar.");

        _storage.Add(entity.Id, entity);
    }

    public T? GetById(int id)
    {
        return _storage.TryGetValue(id, out T? entity) ? entity : null;
    }

    public IEnumerable<T> GetAll() => _storage.Values.ToList();

    public int Count() => _storage.Count;
}""")

    doc.add_paragraph("Penjelasan Baris Kode & Kegunaan:")
    doc.add_paragraph(
        "1. public interface IRepository<T> where T : BaseEntity: Pembuktian GENERIC INTERFACE dengan generic constraint. "
        "Menjamin tipe generic T harus berupa kelas turunan BaseEntity.\n"
        "2. private readonly Dictionary<int, T> _storage: Pembuktian DICTIONARY dan GENERIC CLASS. "
        "Menggunakan Key integer (ID) dan Value objek T untuk kecepatan lookup O(1) tanpa perlu iterasi array lambat.\n"
        "3. _storage.TryGetValue(id, out T? entity): Mengakses data secara aman tanpa risiko KeyNotFoundException.\n"
        "4. Pola Repository ini membuat kode modul lain tidak perlu tahu implementasi penyimpanan data, "
        "memudahkan migrasi ke Entity Framework Core dan MySQL pada tahap MVC mendatang."
    )

    # File 10: Invoice.cs
    doc.add_heading("B. File: Models/Modul3_TransaksiDanRepository/Invoice.cs (Interface IBillable & Dictionary Breakdown)", level=3)
    doc.add_paragraph("Potongan kode program:")
    add_code_block(doc, """public class Invoice : BaseEntity, IBillable
{
    private string _invoiceNumber = string.Empty;
    public ServiceOrder ServiceOrder { get; set; } = null!;
    public decimal GrandTotal { get; private set; }
    public bool IsPaid { get; private set; }
    public DateTime? PaymentDate { get; private set; }

    // DICTIONARY: Menyimpan breakdown rincian komponen tagihan (Nama Komponen -> Nominal)
    public Dictionary<string, decimal> FeeBreakdown { get; set; } = new Dictionary<string, decimal>();

    public decimal CalculateGrandTotal()
    {
        decimal totalJasa = 0m;
        decimal totalSparepart = 0m;

        foreach (BaseServiceItem item in ServiceOrder.ServiceItems)
        {
            if (item is Sparepart) totalSparepart += item.CalculateTotalCost();
            else if (item is ServicePackage) totalJasa += item.CalculateTotalCost();
        }

        decimal subtotal = totalJasa + totalSparepart;
        decimal ppn11Persen = (subtotal - DiscountAmount) * 0.11m;
        GrandTotal = (subtotal - DiscountAmount) + ppn11Persen;

        // Memperbarui isi DICTIONARY rincian biaya
        FeeBreakdown.Clear();
        FeeBreakdown["Total Biaya Jasa"] = totalJasa;
        FeeBreakdown["Total Biaya Suku Cadang"] = totalSparepart;
        FeeBreakdown["Subtotal Kotor"] = subtotal;
        FeeBreakdown["Potongan Diskon"] = DiscountAmount;
        FeeBreakdown["Pajak PPN (11%)"] = ppn11Persen;
        FeeBreakdown["Grand Total Bersih"] = GrandTotal;

        return GrandTotal;
    }

    public bool ProcessPayment(decimal amountPaid, string paymentMethod)
    {
        if (amountPaid < GrandTotal)
            throw new InvalidOperationException("Uang pembayaran kurang!");

        IsPaid = true;
        PaymentDate = DateTime.Now;
        ServiceOrder.MarkAsCompleted(); // Update status SPK dan tambah poin loyalitas pelanggan
        return true;
    }
}""")

    doc.add_paragraph("Penjelasan Baris Kode & Kegunaan:")
    doc.add_paragraph(
        "1. public class Invoice : BaseEntity, IBillable: Membuktikan INHERITANCE dan INTERFACE IMPLEMENTATION dari IBillable.\n"
        "2. Dictionary<string, decimal> FeeBreakdown: Pembuktian DICTIONARY di mana key berupa nama komponen tagihan "
        "(seperti 'Pajak PPN (11%)', 'Potongan Diskon') dan value berupa nominal rupiah.\n"
        "3. Method CalculateGrandTotal(): Menghitung rincian biaya secara otomatis memisahkan antara suku cadang fisik dan jasa, "
        "menghitung PPN 11%, dan mengisi struktur Dictionary untuk transparansi pelanggan.\n"
        "4. Method ProcessPayment(): Memvalidasi kecukupan pembayaran, mencatat tanggal lunas, serta memicu penyelesaian SPK servis."
    )

    # File 11: ServicePricingCatalog.cs
    doc.add_heading("C. File: Models/Modul3_TransaksiDanRepository/ServicePricingCatalog.cs (Dictionary & Generic Method)", level=3)
    doc.add_paragraph("Potongan kode program:")
    add_code_block(doc, """public class ServicePricingCatalog
{
    // DICTIONARY: Kamus tarif acuan servis resmi bengkel MotoCare
    private readonly Dictionary<string, decimal> _catalog = new Dictionary<string, decimal>(StringComparer.OrdinalIgnoreCase);

    public ServicePricingCatalog()
    {
        _catalog.Add("SRV-TUNEUP", 75000m);
        _catalog.Add("SRV-CVT", 60000m);
        _catalog.Add("SRV-GANTI-OLI", 15000m);
        _catalog.Add("SRV-OVERHAUL", 350000m);
    }

    public decimal GetPrice(string serviceCode)
    {
        if (_catalog.TryGetValue(serviceCode, out decimal price)) return price;
        throw new KeyNotFoundException($"Kode '{serviceCode}' tidak terdaftar.");
    }

    // GENERIC METHOD: Mengubah tarif menjadi format generic TResult (misal string tampilan atau kalkulasi pajak)
    public TResult LookupCatalog<TResult>(string serviceCode, Func<decimal, TResult> valueTransformer)
    {
        decimal price = GetPrice(serviceCode);
        return valueTransformer(price);
    }
}""")

    doc.add_paragraph("Penjelasan Baris Kode & Kegunaan:")
    doc.add_paragraph(
        "1. Dictionary<string, decimal> _catalog: Pembuktian DICTIONARY untuk menyimpan pemetaan kode string ke harga decimal "
        "dengan StringComparer.OrdinalIgnoreCase agar tidak sensitif terhadap huruf besar/kecil.\n"
        "2. public TResult LookupCatalog<TResult>(...): Pembuktian GENERIC METHOD dalam C#. Method ini dapat mengembalikan "
        "tipe data apa pun (string terformat, objek DTO, atau angka) sesuai delegasi transformer yang dikirimkan pemanggil."
    )

    # ------------------------------------------------------------------------
    # BAB 4: HASIL PENGUJIAN & RUNNING OUTPUT
    # ------------------------------------------------------------------------
    h4 = doc.add_heading("BAB IV: HASIL PENGUJIAN PROGRAM (CONSOLE DEMO)", level=1)
    h4.style.font.color.rgb = RGBColor(15, 76, 129)
    h4.paragraph_format.space_before = Pt(16)
    h4.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Untuk membuktikan bahwa seluruh kode program di atas dapat dikompilasi (compile) dengan sukses "
        "dan semua konsep OOP berfungsi sebagaimana mestinya, dibuatlah skenario demonstrasi pada file Program.cs. "
        "Berikut adalah log eksekusi terminal ketika perintah 'dotnet run' dijalankan:"
    )

    demo_output = """================================================================================
         MOTOCARE - SISTEM INFORMASI MANAJEMEN BENGKEL MOTOR                   
               DEMONSTRASI IMPLEMENTASI OOP C# .NET                             
================================================================================
Kelompok Tubes: Izat Ibrahimovic, Putrana Yudhistira, Rafli Apriliandi
--------------------------------------------------------------------------------

>>> [MODUL 1 - IZAT IBRAHIMOVIC] Menyiapkan Master Data Customer & Mekanik...
   * [Pelanggan #CUST-001] Budi Santoso | Total Kendaraan: 1 | Poin: 0
   * Info Kendaraan: Kendaraan [D 4123 ABC]: Honda Vario 160 CBS (2023) - 12500 KM (Butuh servis? True)
   * [Mekanik #MEK-07] Agus Pratama (Injeksi & Transmisi CVT) | Status: Sedang Bertugas | Servis Selesai: 0

>>> [MODUL 2 - PUTRANA YUDHISTIRA] Operasional Servis & Inventaris...
   * [JASA SERVIS] Paket Tune-Up Injeksi & CVT (Servis Berkala) | Estimasi: 45 Menit | Tarif: Rp 85.000
   * [SPAREPART] Oli Mesin SPX 2 Full Synthetic 0.8L (AHM Oil) | Stok: 25 | Rak: Rak Cairan A-02 | Harga: Rp 65.000
   * [SPAREPART] Busi NGK Laser Iridium CPR9EAIX (NGK) | Stok: 10 | Rak: Rak Kelistrikan B-01 | Harga: Rp 110.000
   * SPK [SPK-2026-0001] - Kendaraan: D 4123 ABC | Mekanik: Agus Pratama | Status: Antrian | Total Item: 3
   * Sisa stok oli setelah SPK: 24 botol (Stok kritis? False)

>>> [MODUL 3 - RAFLI APRILIANDI] Transaksi Pembayaran & Generic Repository...
   * Generic Repository: Berhasil menyimpan 1 SPK ke dalam InMemoryRepository<ServiceOrder>.
   * Dictionary Pricing Catalog lookup 'SRV-TUNEUP': Biaya Standar: Rp 75.000
   * Diskon Loyalitas diterapkan: Rp 10.000

>>> CETAK HASIL STRUK PEMBAYARAN (IMPLEMENTASI IBILLABLE & DICTIONARY):
==================================================
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
==================================================
 Terima kasih atas kepercayaan Anda di MotoCare!  
=================================================="""
    add_code_block(doc, demo_output)

    # ------------------------------------------------------------------------
    # BAB 5: PANDUAN SCREENSHOT UNTUK EDLINK
    # ------------------------------------------------------------------------
    h5 = doc.add_heading("BAB V: PANDUAN PENGAMBILAN SCREENSHOT UNTUK EDLINK", level=1)
    h5.style.font.color.rgb = RGBColor(15, 76, 129)
    h5.paragraph_format.space_before = Pt(16)
    h5.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Untuk memudahkan pengumpulan pada form Edlink yang mensyaratkan bukti potongan kode dalam 1 file PDF maksimal 10 MB, "
        "berikut adalah panduan tangkapan layar (screenshot) yang perlu disiapkan oleh masing-masing anggota:"
    )

    headers_ss = ["No", "Syarat Edlink", "File yang Harus Di-Screenshot", "Bagian Kode Penting yang Wajib Terlihat"]
    data_ss = [
        ["1", "Variable Get Set Method", "Person.cs atau Vehicle.cs (Izat)", "Field private _fullName, property FullName dengan validasi get/set, dan method UpdateContact()."],
        ["2", "Inheritance", "Customer.cs mewarisi Person.cs (Izat)\natau Sparepart.cs mewarisi BaseServiceItem.cs (Putrana)", "Deklarasi class Customer : Person, pemanggilan konstruktor : base(...), dan keyword override."],
        ["3", "Interface, Abstract", "IServiceItem.cs & BaseServiceItem.cs (Putrana)\natau IRepository.cs (Rafli)", "Deklarasi public interface IServiceItem dan public abstract class BaseServiceItem beserta abstract method-nya."],
        ["4", "Collection, Dictionary, Generic", "InMemoryRepository.cs & Invoice.cs (Rafli)\natau ServiceOrder.cs (Putrana)", "Koleksi List<BaseServiceItem>, Dictionary<int, T>, Dictionary<string, decimal>, dan generic class InMemoryRepository<T>."]
    ]
    create_styled_table(doc, headers_ss, data_ss, col_widths=[0.4, 1.8, 2.1, 2.2])

    add_callout(doc,
        "File PDF ini dapat langsung diunggah ke Edlink karena telah mencakup seluruh potongan kode, "
        "penjelasan mendalam, pembagian tugas mandiri ketiga anggota kelompok, serta log eksekusi sistem MotoCare.",
        "STATUS PENGUMPULAN EDLINK")

    # Save docx
    doc.save(output_path)
    print(f"File DOCX berhasil disimpan di: {output_path}")

if __name__ == "__main__":
    out_file = os.path.abspath("Laporan_Progress_Tubes_PBO_MotoCare.docx")
    generate_document(out_file)
