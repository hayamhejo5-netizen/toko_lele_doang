import streamlit as st
from datetime import datetime
import urllib.parse

# 1. KONFIGURASI HALAMAN PREMIUM (Mobile & Desktop Friendly)
st.set_page_config(
    page_title="Toko Lele Berkah - Premium",
    page_icon="🐟",
    layout="centered"
)

# INTERFACE STYLING (Custom CSS)
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
.hero-banner { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 30px; border-radius: 16px; margin-bottom: 25px; box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.2); }
.hero-banner h1 { color: white !important; margin: 0; font-size: 28px; font-weight: 700; }
.hero-banner p { margin: 5px 0 0 0; opacity: 0.9; font-size: 14px; }
.custom-card { background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px; }
.invoice-box { background-color: white; padding: 30px; border-radius: 16px; border: 1px solid #cbd5e1; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); color: #1e293b; }
.invoice-table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 15px; }
.invoice-table th { background-color: #f1f5f9; color: #475569; text-align: left; padding: 10px; font-size: 13px; text-transform: uppercase; border-bottom: 2px solid #cbd5e1; }
.invoice-table td { padding: 12px 10px; border-bottom: 1px solid #e2e8f0; font-size: 14px; }
.btn-whatsapp { background-color: #25D366; color: white !important; text-decoration: none; display: block; text-align: center; padding: 14px; border-radius: 8px; font-weight: bold; font-size: 16px; margin-top: 20px; box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3); }
</style>
""", unsafe_allow_html=True)

# 2. HERO BANNER
st.markdown("""
<div class="hero-banner">
    <h1>🐟 Toko Lele Berkah Digital</h1>
    <p>Sistem Pemesanan Resmi - Segar, Higienis, dan Siap Kirim ke Lokasi Anda</p>
</div>
""", unsafe_allow_html=True)

# 3. DATA PRODUK (KATALOG)
st.markdown("### 🛍️ 1. Pilih Produk Lele Terbaik")

daftar_lele = {
    "Lele Segar Konsumsi (Isi 6-8 ekor/kg)": {"harga": 26000, "desc": "Cocok untuk konsumsi harian, rumah makan, dan pecel lele."},
    "Lele Hidup Jumbo (Isi 4-5 ekor/kg)": {"harga": 28000, "desc": "Ukuran besar mantap, daging tebal dan gurih."},
    "Lele Bumbu Siap Goreng (Per Pack 500g)": {"harga": 35000, "desc": "Praktis, sudah dibersihkan dan dibumbui rempah alami."},
    "Bibit Lele Unggul Sangkuriang (Per 100 Ekor)": {"harga": 40000, "desc": "Bibit lincah, daya tahan tinggi, cocok untuk budidaya."}
}

pesanan = {}
total_belanja = 0

for produk, info in daftar_lele.items():
    st.markdown(f"""
    <div style="background: white; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
        <strong style="font-size:16px; color:#1e3a8a;">{produk}</strong><br>
        <span style="font-size:12px; color:#64748b;">{info['desc']}</span><br>
        <span style="font-size:14px; font-weight:bold; color:#0f172a;">Harga: Rp {info['harga']:,}</span>
    </div>
    """, unsafe_allow_html=True)
    
    qty = st.number_input(f"Jumlah Beli ({produk})", min_value=0, value=0, step=1, key=f"qty_{produk}")
    
    if qty > 0:
        subtotal = qty * info['harga']
        pesanan[produk] = {"qty": qty, "harga": info['harga'], "subtotal": subtotal}
        total_belanja += subtotal

st.markdown("---")

# 4. FORM IDENTITAS & ALAMAT
st.markdown("### 🚚 2. Informasi Penerima & Alamat")
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
nama_pembeli = st.text_input("👤 Nama Lengkap Pembeli:", placeholder="Contoh: Budi Setiadi")
no_whatsapp = st.text_input("📱 No. WhatsApp / HP:", placeholder="Contoh: 081234567xxx")
alamat_kirim = st.text_area("📍 Alamat Lengkap Pengiriman:", placeholder="Tuliskan Nama Jalan, Nomor Rumah, RT/RW, Kecamatan, Kota/Kabupaten...")
st.markdown('</div>', unsafe_allow_html=True)

# Perhitungan Biaya
ongkir = 15000 if alamat_kirim else 0
grand_total = total_belanja + ongkir

st.markdown("---")

# 5. TOMBOL AKSI UTAMA & PENERBITAN INVOICE
st.markdown("### 🧾 3. Tinjau & Terbitkan Nota")

if st.button("✨ KLIK: Proses & Cetak Invoice Resmi", type="primary", use_container_width=True):
    if total_belanja == 0:
        st.error("❌ Eror: Anda belum menentukan jumlah barang pada Katalog Produk.")
    elif not nama_pembeli.strip() or not no_whatsapp.strip() or not alamat_kirim.strip():
        st.warning("⚠️ Perhatian: Mohon lengkapi Nama, No. WhatsApp, dan Alamat Pengiriman agar Invoice bisa dicetak.")
    else:
        st.success("🎉 Invoice Berhasil Diterbitkan!")
        waktu_transaksi = datetime.now().strftime("%d %B %Y - %H:%M WIB")
        no_invoice = f"INV/LELE/{datetime.now().strftime('%Y%m%d')}/{id(nama_pembeli)%1000:03d}"
        
        # Merakit baris produk tanpa spasi baris baru (Anti-Bug)
        html_rows = ""
        rincian_wa = ""
        for item, detail in pesanan.items():
            html_rows += f"<tr><td><b>{item}</b></td><td style='text-align:center;'>{detail['qty']}</td><td style='text-align:right;'>Rp {detail['harga']:,}</td><td style='text-align:right; font-weight:bold;'>Rp {detail['subtotal']:,}</td></tr>"
            rincian_wa += f"• {item} (x{detail['qty']}) -> Sub: Rp {detail['subtotal']:,}\n"
        
        # Menggabungkan seluruh HTML secara flat tanpa spasi di awal string
        invoice_html = (
            f'<div class="invoice-box">'
            f'<table style="width:100%; border:none;"><tr>'
            f'<td><h2 style="margin:0; color:#1e3a8a; font-weight:800;">INVOICE PENJUALAN</h2><span style="font-size:12px; color:#64748b;">No: {no_invoice}</span></td>'
            f'<td style="text-align:right;"><h3 style="margin:0; color:#475569;">TOKO LELE BERKAH</h3><span style="font-size:12px; color:#64748b;">{waktu_transaksi}</span></td>'
            f'</tr></table>'
            f'<hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">'
            f'<table style="width:100%; border:none; font-size:14px; margin-bottom:20px;"><tr>'
            f'<td style="width:15%; color:#64748b; vertical-align:top;"><b>Ditujukan ke:</b></td>'
            f'<td><b>{nama_pembeli}</b><br>Telp: {no_whatsapp}<br>Alamat: {alamat_kirim}</td>'
            f'</tr></table>'
            f'<table class="invoice-table">'
            f'<thead><tr><th>Item Produk</th><th style="text-align:center;">Qty</th><th style="text-align:right;">Harga Satuan</th><th style="text-align:right;">Total</th></tr></thead>'
            f'<tbody>{html_rows}</tbody>'
            f'</table>'
            f'<table style="width:100%; border:none; margin-top:20px; font-size:14px;">'
            f'<tr><td style="text-align:right; color:#64748b; padding:5px;">Subtotal Belanja:</td><td style="text-align:right; width:30%; padding:5px;">Rp {total_belanja:,}</td></tr>'
            f'<tr><td style="text-align:right; color:#64748b; padding:5px;">Ongkos Kirim (Flat):</td><td style="text-align:right; padding:5px;">Rp {ongkir:,}</td></tr>'
            f'<tr style="font-size:18px; font-weight:bold; color:#1e3a8a;"><td style="text-align:right; padding:10px 5px;">GRAND TOTAL:</td><td style="text-align:right; padding:10px 5px; border-top:2px solid #1e3a8a;">Rp {grand_total:,}</td></tr>'
            f'</table>'
            f'<p style="text-align:center; font-size:12px; color:#94a3b8; margin-top:30px; font-style:italic;">Terima kasih atas kepercayaan Anda berbelanja di Toko Lele Berkah.</p>'
            f'</div>'
            )
        
        st.markdown(invoice_html, unsafe_allow_html=True)
        # INTEGRASI TELEPON / WHATSAPP ADMIN (Fix Eror String Unterminated)
        nomor_admin_wa = "6282119635990"
        format_pesan_wa = (
        f"🟢 *PESANAN BARU - TOKO LELE BERKAH DIGITAL* 🟢\n"
        f"No Invoice: {no_invoice}\n"
        f"Waktu: {waktu_transaksi}\n\n"
        f"👤 *DATA PELANGGAN*:\n"
        f"Nama: {nama_pembeli}\n"
        f"No. HP: {no_whatsapp}\n"
        f"📍 *ALAMAT PENGIRIMAN*:\n"
        f"{alamat_kirim}\n\n"
        f"📋 *RINCIAN PESANAN*:\n"
        f"{rincian_wa}\n"
        f"----------------------------------------\n"
        f"Subtotal: Rp {total_belanja:,}\n"
        f"Ongkos Kirim: Rp {ongkir:,}\n"
        f"💰 *TOTAL BAYAR: Rp {grand_total:,}*\n\n"
        f"Mohon konfirmasi ketersediaan stok dan jadwal pengiriman ya Admin. Terima kasih!"
)

encoded_wa_text = urllib.parse.quote(format_pesan_wa)
link_kirim_wa = f"https://api.whatsapp.com/send?phone=6282119635990&text={encoded_wa_text}"

# Ini tombol WhatsApp bawaan kode kamu
st.markdown(f'<a class="btn-whatsapp" href="{link_kirim_wa}" target="_blank" style="color: white; text-align: center;">Kirim ke WhatsApp</a>', unsafe_allow_html=True)


# =========================================================
# TARUH KODE GOOGLE SHEETS DI SINI (SETELAH TOMBOL WA SELESAI)
# =========================================================
import requests

data_ke_sheet = {
    "no_invoice": no_invoice,
    "tanggal": waktu_transaksi,
    "nama": nama_pembeli,
    "whatsapp": no_whatsapp,     
    "alamat": alamat_kirim,       
    "rincian": format_pesan_wa,   # <--- Sekarang ini aman karena sudah dibuat di atas!
    "total_belanja": int(total_belanja),
    "ongkir": int(ongkir),
    "grand_total": int(grand_total)
}

# ⚠️ JANGAN LUPA: Ganti teks di bawah ini dengan URL Web App dari Google Sheets kamu!
url_jembatan_sheets = "https://script.google.com/macros/s/AKfycbyI94fiH4UocDQIJU_XJid3V6bviqYzQzbrpke7LyAru1ljdoLWu9ziG8QPM4W67PBvYQ/exec"

try:
    requests.post(url_jembatan_sheets, json=data_ke_sheet)
except Exception as e:
    pass
