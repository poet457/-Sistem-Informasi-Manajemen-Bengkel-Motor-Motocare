using System;

namespace MotoCare.Models.Common
{
    /// <summary>
    /// Base Entity bersifat abstract sebagai kerangka dasar seluruh entitas di sistem MotoCare.
    /// Menerapkan konsep Abstraction dan Encapsulation (Variable, Get, Set).
    /// </summary>
    public abstract class BaseEntity
    {
        // Field private (encapsulation)
        private int _id;

        // Property Get-Set dengan enkapsulasi dan validasi
        public int Id
        {
            get => _id;
            set
            {
                if (value < 0)
                {
                    throw new ArgumentException("ID tidak boleh bernilai negatif.");
                }
                _id = value;
            }
        }

        // Auto-implemented property
        public DateTime CreatedAt { get; set; } = DateTime.Now;
        public DateTime? UpdatedAt { get; set; }
        public bool IsActive { get; set; } = true;

        // Abstract method yang wajib diimplementasikan oleh setiap entitas turunan
        public abstract string GetEntityInfo();
    }
}
