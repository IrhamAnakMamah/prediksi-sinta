import streamlit as st
import importlib

# --- IMPORT FILE MODUL ASLI ---
import publikasi
import research
import abdimas
import hki
import kelembagaan
import sdm

# --- KONFIGURASI HALAMAN UTAMA ---
st.set_page_config(layout="wide", page_title="SINTA Master Simulator")

# ==============================================================================
# 1. PERSIAPAN DATA STORAGE & MONKEY PATCH (PENYELAMAT DATA)
# ==============================================================================

# Buat "Brankas" penyimpanan data yang permanen
if "SINTA_DB" not in st.session_state:
    st.session_state["SINTA_DB"] = {}

# Simpan fungsi asli st.number_input agar tidak hilang
_original_number_input = st.number_input

def _patched_number_input(label, *args, **kwargs):
    """
    Fungsi bajakan untuk st.number_input.
    Setiap kali user input angka, kita simpan juga ke SINTA_DB.
    """
    # Panggil fungsi asli untuk menampilkan widget
    val = _original_number_input(label, *args, **kwargs)
    
    # Tentukan ID untuk penyimpanan
    # Cek apakah modul menggunakan 'key' khusus (seperti publikasi.py)
    # Jika tidak ada key, gunakan label (seperti sdm.py yang pakai "v_R1")
    storage_key = kwargs.get("key", label)
    
    # Simpan nilai ke brankas permanen
    st.session_state["SINTA_DB"][storage_key] = val
    
    return val

# Ganti fungsi asli Streamlit dengan fungsi bajakan kita
# Ini akan berlaku untuk semua modul yang di-import setelah baris ini
st.number_input = _patched_number_input

# ==============================================================================
# 2. DATA KONSTANTA & REFERENSI (Copy dari modul asli untuk rumus)
# ==============================================================================

# 1. PUBLIKASI
NORMALIZER_PUB = 1776.69
DATA_PUBLIKASI = [
    ("Intl", "AI1", "ARTIKEL JURNAL INTERNASIONAL Q1", 40),
    ("Intl", "AI2", "ARTIKEL JURNAL INTERNASIONAL Q2", 35),
    ("Intl", "AI3", "ARTIKEL JURNAL INTERNASIONAL Q3", 30),
    ("Intl", "AI4", "ARTIKEL JURNAL INTERNASIONAL Q4", 25),
    ("Intl", "AI5", "ARTIKEL JURNAL INTERNASIONAL NON Q", 20),
    ("Intl", "AI6", "ARTIKEL NON JURNAL INTERNASIONAL", 15),
    ("Intl", "AI7", "JUMLAH SITASI PUBLIKASI INTERNASIONAL", 1),
    ("Intl", "AI8", "JUMLAH DOKUMEN PUBLIKASI INTERNASIONAL TERSITASI", 1),
    ("Nas", "AN1", "ARTIKEL JURNAL NASIONAL PERINGKAT 1", 25),
    ("Nas", "AN2", "ARTIKEL JURNAL NASIONAL PERINGKAT 2", 20),
    ("Nas", "AN3", "ARTIKEL JURNAL NASIONAL PERINGKAT 3", 15),
    ("Nas", "AN4", "ARTIKEL JURNAL NASIONAL PERINGKAT 4", 10),
    ("Nas", "AN5", "ARTIKEL JURNAL NASIONAL PERINGKAT 5", 5),
    ("Nas", "AN6", "ARTIKEL JURNAL NASIONAL PERINGKAT 6", 2),
    ("Nas", "AN8", "PROSIDING NASIONAL", 2),
    ("Nas", "AN9", "JUMLAH SITASI PUBLIKASI NASIONAL PER DOSEN", 1),
    ("Other", "DGS2", "GS CITATION PER LECTURER", 1),
    ("Other", "B1", "BUKU AJAR", 20),
    ("Other", "B2", "BUKU REFERENSI", 40),
    ("Other", "B3", "BUKU MONOGRAF", 20),
]

# 2. RESEARCH
PEMBAGI_NORMALISASI_RES = 261491.37
DATA_RESEARCH = [
    ("P1", "JUMLAH PENELITIAN HIBAH LUAR NEGERI (KETUA)", 40),
    ("P2", "JUMLAH PENELITIAN HIBAH LUAR NEGERI (ANGGOTA)", 10),
    ("P3", "JUMLAH PENELITIAN HIBAH EKSTERNAL (KETUA)", 30),
    ("P4", "JUMLAH PENELITIAN HIBAH EKSTERNAL (ANGGOTA)", 10),
    ("P5", "JUMLAH PENELITIAN INTERNAL INSTITUSI (KETUA)", 15),
    ("P6", "JUMLAH PENELITIAN INTERNAL INSTITUSI (ANGGOTA)", 5),
    ("P7", "JUMLAH RUPIAH PENELITIAN (JUTA RUPIAH)", 0.05),
]

# 3. ABDIMAS
PEMBAGI_NORMALISASI_ABDIMAS = 447937.99
DATA_ABDIMAS = [
    ("PM1", "JUMLAH PENGABDIAN MASYARAKAT INTERNASIONAL (KETUA)", 40),
    ("PM2", "JUMLAH PENGABDIAN MASYARAKAT INTERNASIONAL (ANGGOTA)", 10),
    ("PM3", "JUMLAH PENGABDIAN MASYARAKAT NASIONAL/EKSTERNAL (KETUA)", 30),
    ("PM4", "JUMLAH PENGABDIAN MASYARAKAT NASIONAL/EKSTERNAL (ANGGOTA)", 10),
    ("PM5", "JUMLAH PENGABDIAN MASYARAKAT LOKAL/INTERNAL INSTITUSI (KETUA)", 15),
    ("PM6", "JUMLAH PENGABDIAN MASYARAKAT LOKAL/INTERNAL INSTITUSI (ANGGOTA)", 5),
    ("PM7", "JUMLAH RUPIAH PENGABDIAN MASYARAKAT (JUTA RUPIAH)", 0.05),
]

# 4. HKI
PEMBAGI_NORMALISASI_HKI = 14.7
DATA_HKI = [
    ("KI1", "HKI PATEN", 40),
    ("KI2", "HKI PATEN SEDERHANA", 20),
    ("KI3", "HKI MEREK", 1),
    ("KI4", "HKI INDIKASI GEOGRAFIS", 10),
    ("KI5", "HKI DESAIN INDUSTRI", 20),
    ("KI6", "HKI DESAIN TATA LETAK SIRKUIT TERPADU", 20),
    ("KI7", "HKI RAHASIA DAGANG", 0),
    ("KI8", "HKI PERLINDUNGAN VARIETAS TANAMAN", 40),
    ("KI9", "HKI HAK CIPTA", 1),
    ("KI10", "HKI SELAIN TERDAFTAR / DIBERI / DITERIMA", 1),
]

# 5. SDM
PEMBAGI_NORMALISASI_SDM = 2.443
DATA_SDM = [
    ("R1", "REVIEWER JURNAL INTERNASIONAL (ORANG)", 2),
    ("R2", "REVIEWER JURNAL NASIONAL SINTA 1 & 2 (ORANG)", 1),
    ("R3", "REVIEWER JURNAL NASIONAL SINTA 3 S.D. 6 (ORANG)", 0.5),
    ("DOS1", "DOSEN PROFESSOR", 4),
    ("DOS2", "DOSEN LEKTOR KEPALA", 3),
    ("DOS3", "DOSEN LEKTOR", 2),
    ("DOS4", "DOSEN ASISTEN AHLI", 1),
    ("DOS5", "DOSEN NON JAFA", 0),
]

# 6. KELEMBAGAAN
FAKTOR_PENYESUAIAN_KEL = 0.30
PEMBAGI_NORMALISASI_KEL = 2181.33
DATA_KELEMBAGAAN = [
    ("Akreditasi", "APS1", "AKREDITASI PRODI A/UNGGUL/INTERNASIONAL", 40),
    ("Akreditasi", "APS2", "AKREDITASI PRODI B/BAIK SEKALI", 30),
    ("Akreditasi", "APS3", "AKREDITASI PRODI C/BAIK", 20),
    ("Akreditasi", "APS4", "AKREDITASI PRODI D/TIDAK TERAKREDITASI", 0),
    ("Jurnal", "JO1", "JUMLAH JURNAL TERAKREDITASI S1", 40),
    ("Jurnal", "JO2", "JUMLAH JURNAL TERAKREDITASI S2", 30),
    ("Jurnal", "JO3", "JUMLAH JURNAL TERAKREDITASI S3", 20),
    ("Jurnal", "JO4", "JUMLAH JURNAL TERAKREDITASI S4", 10),
    ("Jurnal", "JO5", "JUMLAH JURNAL TERAKREDITASI S5", 5),
    ("Jurnal", "JO6", "JUMLAH JURNAL TERAKREDITASI S6", 2),
]

# ==============================================================================
# 3. UTILITIES
# ==============================================================================

def run_module_safely(module_main_func):
    """Menjalankan modul lain tanpa error double st.set_page_config"""
    original_set_page_config = st.set_page_config
    st.set_page_config = lambda *args, **kwargs: None
    try:
        module_main_func()
    except Exception as e:
        st.error(f"Error pada modul: {e}")
    finally:
        st.set_page_config = original_set_page_config

def get_val(key):
    """Mengambil data dari brankas SINTA_DB"""
    return st.session_state["SINTA_DB"].get(key, 0.0)

def calculate_all_scores():
    """Menghitung total skor berdasarkan data di SINTA_DB"""
    
    # 1. SDM (Format label: v_Kode)
    raw_sdm = sum([get_val(f"v_{code}") * bobot for code, _, bobot in DATA_SDM])
    norm_sdm = (raw_sdm / PEMBAGI_NORMALISASI_SDM) * 100

    # 2. RESEARCH (Format label: v_Kode)
    raw_res = sum([get_val(f"v_{code}") * bobot for code, _, bobot in DATA_RESEARCH])
    norm_res = (raw_res / PEMBAGI_NORMALISASI_RES) * 100

    # 3. ABDIMAS (Format label: v_Kode)
    raw_abd = sum([get_val(f"v_{code}") * bobot for code, _, bobot in DATA_ABDIMAS])
    norm_abd = (raw_abd / PEMBAGI_NORMALISASI_ABDIMAS) * 100

    # 4. HKI (Format label: v_Kode)
    raw_hki = sum([get_val(f"v_{code}") * bobot for code, _, bobot in DATA_HKI])
    norm_hki = (raw_hki / PEMBAGI_NORMALISASI_HKI) * 100

    # 5. KELEMBAGAAN (Format label: v_Kode)
    raw_kel = sum([get_val(f"v_{code}") * bobot for _, code, _, bobot in DATA_KELEMBAGAAN])
    adj_kel = raw_kel * FAKTOR_PENYESUAIAN_KEL
    norm_kel = (adj_kel / PEMBAGI_NORMALISASI_KEL) * 100

    # 6. PUBLIKASI (Format Key khusus: Kode langsung, misal "AI1")
    # Perhatikan: Di file publikasi.py, st.number_input menggunakan key=kode (bukan v_kode)
    raw_pub = sum([get_val(code) * bobot for _, code, _, bobot in DATA_PUBLIKASI])
    norm_pub = (raw_pub / NORMALIZER_PUB) * 100

    # Total Weighted
    # A(25%) + B(10%) + C(15%) + D(15%) + E(15%) + F(15%)
    total = (norm_pub * 0.25) + (norm_hki * 0.10) + (norm_kel * 0.15) + (norm_res * 0.15) + (norm_abd * 0.15) + (norm_sdm * 0.15)
    
    return total, {
        "Publikasi (25%)": norm_pub, 
        "Research (15%)": norm_res, 
        "Abdimas (15%)": norm_abd, 
        "HKI (10%)": norm_hki, 
        "SDM (15%)": norm_sdm, 
        "Kelembagaan (15%)": norm_kel
    }

# ==============================================================================
# 4. MAIN NAVIGATION
# ==============================================================================

def main():
    with st.sidebar:
        st.title("🎛️ Navigasi")
        menu = st.radio("Pilih Modul", [
            "🏆 Dashboard Utama",
            "📚 Publikasi",
            "🔬 Research",
            "🤝 Abdimas",
            "💡 HKI",
            "👥 SDM",
            "🏛️ Kelembagaan"
        ])
        
        st.divider()
        # Preview skor kecil
        prev_total, _ = calculate_all_scores()
        st.metric("Total Score (95%)", f"{prev_total:,.2f}")
        st.caption("Pindah ke Dashboard untuk hasil detail.")

    # --- ROUTING ---
    if menu == "🏆 Dashboard Utama":
        st.title("🏆 Final Dashboard Prediction")
        st.markdown("Ringkasan prediksi Cluster Mandiri.")
        st.divider()
        
        total_score, rincian = calculate_all_scores()
        THRESHOLD = 28.26
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown("### Total Score Akhir")
            st.markdown(f"<h1 style='font-size: 48px;'>{total_score:,.2f}</h1>", unsafe_allow_html=True)
            
            if total_score >= THRESHOLD:
                st.success(f"✅ **Lolos Cluster Mandiri!**\n\nSurplus: +{total_score - THRESHOLD:.2f}")
            else:
                st.error(f"❌ **Belum Lolos.**\n\nKurang: {THRESHOLD - total_score:.2f}")
        
        with col2:
            st.markdown("### Rincian Skor Ternormalisasi")
            # Convert dict to dataframe for nicer display
            import pandas as pd
            df_rincian = pd.DataFrame(list(rincian.items()), columns=["Komponen", "Skor Ternormalisasi"])
            st.dataframe(
                df_rincian.style.format({"Skor Ternormalisasi": "{:.2f}"}),
                use_container_width=True,
                hide_index=True
            )

    # --- MODUL INPUT (Jalankan file asli) ---
    elif menu == "📚 Publikasi":
        run_module_safely(publikasi.main)
    elif menu == "🔬 Research":
        run_module_safely(research.main)
    elif menu == "🤝 Abdimas":
        run_module_safely(abdimas.main)
    elif menu == "💡 HKI":
        run_module_safely(hki.main)
    elif menu == "👥 SDM":
        run_module_safely(sdm.main)
    elif menu == "🏛️ Kelembagaan":
        run_module_safely(kelembagaan.main)

if __name__ == "__main__":
    main()