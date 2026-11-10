using System;
using System.Collections.Generic;
using System.Linq;
using MotoCare.Models.Common;
using MotoCare.Models.Modul3_TransaksiDanRepository.Interfaces;

namespace MotoCare.Models.Modul3_TransaksiDanRepository.Repositories
{
    /// <summary>
    /// Modul 3: Transaksi Pembayaran & Generic Repository
    /// Penanggung Jawab: Rafli Apriliandi
    /// 
    /// Kelas Generic InMemoryRepository<T> menyediakan implementasi repository pola generik
    /// menggunakan DICTIONARY sebagai penyimpanan data in-memory cepat berdasarkan Key (Id).
    /// Mengimplementasikan:
    /// 1. GENERIC CLASS (T where T : BaseEntity)
    /// 2. DICTIONARY (Dictionary<int, T>)
    /// 3. COLLECTION (List<T>, IEnumerable<T>)
    /// 4. INTERFACE IMPLEMENTATION (IRepository<T>)
    /// 5. Variable & Method
    /// </summary>
    /// <typeparam name="T">Tipe kelas yang mewarisi BaseEntity</typeparam>
    public class InMemoryRepository<T> : IRepository<T> where T : BaseEntity
    {
        // DICTIONARY: Digunakan sebagai penyimpanan cepat O(1) berdasarkan ID entitas
        private readonly Dictionary<int, T> _storage = new Dictionary<int, T>();
        private int _autoIncrementId = 1;

        // Property Repository Name
        public string RepositoryName { get; set; }

        public InMemoryRepository(string repoName)
        {
            RepositoryName = repoName;
        }

        // Method Generic: Menambahkan entitas baru
        public void Add(T entity)
        {
            if (entity == null)
                throw new ArgumentNullException(nameof(entity), "Entitas yang ditambahkan tidak boleh null.");

            if (entity.Id <= 0)
            {
                entity.Id = _autoIncrementId++;
            }

            if (_storage.ContainsKey(entity.Id))
            {
                throw new InvalidOperationException($"Entitas dengan ID {entity.Id} sudah ada di {RepositoryName}.");
            }

            _storage.Add(entity.Id, entity);
        }

        // Method Generic: Mengambil entitas berdasarkan Id dari Dictionary
        public T? GetById(int id)
        {
            if (_storage.TryGetValue(id, out T? entity))
            {
                return entity;
            }
            return null;
        }

        // Method Generic: Mengambil seluruh entitas sebagai Collection List
        public IEnumerable<T> GetAll()
        {
            return _storage.Values.ToList();
        }

        // Method Generic: Pencarian berdasarkan kondisi lambda filter
        public IEnumerable<T> Find(Func<T, bool> predicate)
        {
            return _storage.Values.Where(predicate).ToList();
        }

        // Method Generic: Memperbarui data entitas
        public bool Update(T entity)
        {
            if (entity == null || !_storage.ContainsKey(entity.Id))
                return false;

            entity.UpdatedAt = DateTime.Now;
            _storage[entity.Id] = entity;
            return true;
        }

        // Method Generic: Menghapus data dari Dictionary
        public bool Delete(int id)
        {
            return _storage.Remove(id);
        }

        // Method Generic: Menghitung total entitas yang tersimpan
        public int Count()
        {
            return _storage.Count;
        }
    }
}
