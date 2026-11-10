using System;
using MotoCare.Models.Common;

namespace MotoCare.Models.Modul1_MasterData
{
    /// <summary>
    /// Modul 1: Master Data
    /// Penanggung Jawab: Izat Ibrahimovic
    /// 
    /// Kelas Person merupakan Base Class untuk entitas individu (Customer dan Mechanic).
    /// Mengimplementasikan:
    /// 1. Inheritance dari BaseEntity
    /// 2. Variable (field private)
    /// 3. Get-Set Property dengan validasi logika
    /// 4. Method biasa dan Virtual Method untuk Polymorphism
    /// </summary>
    public class Person : BaseEntity
    {
        // Private backing fields (Enkapsulasi)
        private string _fullName = string.Empty;
        private string _phoneNumber = string.Empty;
        private string _email = string.Empty;

        // Default Constructor
        public Person()
        {
        }

        // Parameterized Constructor
        public Person(int id, string fullName, string phoneNumber, string email)
        {
            Id = id;
            FullName = fullName;
            PhoneNumber = phoneNumber;
            Email = email;
        }

        // Property dengan validasi pada Getter / Setter
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

        public string Email
        {
            get => _email;
            set
            {
                if (!string.IsNullOrWhiteSpace(value) && !value.Contains("@"))
                    throw new ArgumentException("Format email tidak valid.");
                _email = value?.Trim() ?? string.Empty;
            }
        }

        // Method biasa untuk update data kontak
        public void UpdateContact(string newPhone, string newEmail)
        {
            PhoneNumber = newPhone;
            Email = newEmail;
            UpdatedAt = DateTime.Now;
        }

        // Virtual method agar bisa di-override oleh kelas turunan (Polymorphism)
        public virtual string GetProfileSummary()
        {
            return $"[ID: {Id}] {FullName} | Telp: {PhoneNumber} | Email: {Email}";
        }

        // Implementasi abstract method dari BaseEntity
        public override string GetEntityInfo()
        {
            return $"Entitas Person: {FullName} ({GetType().Name})";
        }
    }
}
