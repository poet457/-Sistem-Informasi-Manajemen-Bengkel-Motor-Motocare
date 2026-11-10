using System;
using System.Collections.Generic;
using MotoCare.Models.Common;

namespace MotoCare.Models.Modul3_TransaksiDanRepository.Interfaces
{
    /// <summary>
    /// Modul 3: Transaksi Pembayaran & Generic Repository
    /// Penanggung Jawab: Rafli Apriliandi
    /// 
    /// Interface Generic IRepository<T> mendefinisikan operasi standar CRUD (Create, Read, Update, Delete)
    /// untuk semua tipe data entitas yang mewarisi BaseEntity.
    /// Mengimplementasikan:
    /// 1. INTERFACE
    /// 2. GENERIC INTERFACE (T where T : BaseEntity)
    /// 3. COLLECTION (IEnumerable<T>, List<T>)
    /// </summary>
    /// <typeparam name="T">Tipe entitas turunan dari BaseEntity</typeparam>
    public interface IRepository<T> where T : BaseEntity
    {
        // Method CRUD Generic
        void Add(T entity);
        T? GetById(int id);
        IEnumerable<T> GetAll();
        IEnumerable<T> Find(Func<T, bool> predicate);
        bool Update(T entity);
        bool Delete(int id);
        int Count();
    }
}
