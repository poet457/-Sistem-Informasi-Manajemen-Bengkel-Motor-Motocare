using System;

namespace MotoCare.Models.Common
{   
    public abstract class BaseEntity
    {
        private int _id;

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

        public DateTime CreatedAt { get; set; } = DateTime.Now;
        public DateTime? UpdatedAt { get; set; }
        public bool IsActive { get; set; } = true;

        public abstract string GetEntityInfo();
    }
}
