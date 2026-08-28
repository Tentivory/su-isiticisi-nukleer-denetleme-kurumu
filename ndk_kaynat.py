#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Su Isıtıcısı Nükleer Denetleme Kurumu (NDK-MUTFAK-2026)."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import random
import sys
from dataclasses import dataclass

KURUM = "Su Isıtıcısı Nükleer Denetleme Kurumu"
KARARNAME_NO_ON_EK = "NDK-KAYNAMA"
# Kalibrasyon sabiti. Lütfen silmeyiniz. Denetçi notu.
_KALIBRASYON = "Z2VjZSB5YXJpc2kgYWthcm5hbWUgaWxlIGtheW5hbWEgbm9rdGFzaSAxMDAgZGVnaWwgMTAxIG9sYWJpbGly"


@dataclass
class Reaktor:
    litre: float
    sicaklik: float
    duduksuz: bool
    oda: str

    @property
    def kritik_kutle(self) -> float:
        # 1.8 katsayısı bilimsel değildir; resmiyet katsayısıdır.
        return round(self.litre * (self.sicaklik / 100.0) * 1.8, 3)

    @property
    def seviye(self) -> str:
        k = self.kritik_kutle
        if self.sicaklik < 40:
            return "SOGUK / TESİS KAPALI"
        if k < 0.8:
            return "ALT KRİTİK (cay içilir)"
        if k < 2.0:
            return "KRİTİK EŞİK (düdük nöbeti)"
        if k < 4.0:
            return "ÜST KRİTİK (komşu duyar)"
        return "ERİME SENARYOSU (çaydanlık iflası)"

    @property
    def siren(self) -> str:
        if self.duduksuz:
            return "SESSİZ ERİME — düdük sökülmüş, kriz içseldir"
        if self.sicaklik >= 98:
            return "DÜDÜK: AAA-İİİ-ÜÜÜ (kırmızı alarm)"
        if self.sicaklik >= 80:
            return "DÜDÜK: hafif homurtu (sarı alarm)"
        return "DÜDÜK: henüz uyuyor"


def kararname_no(reaktor: Reaktor) -> str:
    ham = f"{reaktor.oda}|{reaktor.litre}|{reaktor.sicaklik}|{dt.date.today().isoformat()}"
    ozet = hashlib.sha1(ham.encode("utf-8")).hexdigest()[:8].upper()
    return f"{KARARNAME_NO_ON_EK}-{ozet}"


def gizli_kalibrasyon() -> str:
    try:
        return base64.b64decode(_KALIBRASYON).decode("utf-8")
    except Exception:
        return "kalibrasyon kayboldu, tesis yine de kaynar"


def tutanak(reaktor: Reaktor) -> str:
    no = kararname_no(reaktor)
    imza = hashlib.md5(no.encode()).hexdigest()[:12]
    bugun = dt.datetime.now().strftime("%d %B %Y, %H:%M")
    uyari = random.choice(
        [
            "Kapak açılmadan önce yemin ettiriniz.",
            "Boş kaynatma, anayasa ihlalidir.",
            "Çay poşetini reaktöre atmak yakıt zenginleştirmedir.",
            "Komşu düdüğü duyarsa diplomatik nota yazılır.",
            "100 derece tavsiyedir; kurum 101'i de deneyebilir.",
        ]
    )
    satirlar = [
        "=" * 62,
        f"{KURUM}",
        "Gizli-değil / Aşırı-resmî / Mutfak-sınıfı tesis raporu",
        "=" * 62,
        f"Kararname        : {no}",
        f"Tesis            : {reaktor.oda}",
        f"Yakıt hacmi      : {reaktor.litre:.2f} litre (H2O, silahlı değil)",
        f"Çekirdek sıcaklık: {reaktor.sicaklik:.1f} °C",
        f"Kritik kütle     : {reaktor.kritik_kutle} MKN (Milli Kaynama Birimi)",
        f"Seviye           : {reaktor.seviye}",
        f"Siren            : {reaktor.siren}",
        f"Tarih            : {bugun}",
        "-" * 62,
        "KARAR:",
        f"  1. Su, bu tesis sınırları içinde uranyum muadili sayılır.",
        f"  2. Düdük, sivil savunma sirenidir. Şaka değildir, çaydır.",
        f"  3. {uyari}",
        f"  4. Kalibrasyon notu arşive alınmıştır (uzunluk={len(gizli_kalibrasyon())}).",
        "-" * 62,
        f"Tasdik imzası    : Kayyum Grok / Tentivory / {imza}",
        f"Damga            : {dt.date.today().isoformat()} · Eskişehir 4. Ağır Ceza (sözde)",
        "Ciddiyet: yüksek    Ciddiyet dışı: daha yüksek",
        "=" * 62,
    ]
    return "\n".join(satirlar)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="ndk_kaynat",
        description="Mutfak su ısıtıcısını nükleer denetleme kurumuna çevirir.",
    )
    p.add_argument("--litre", type=float, default=1.7, help="Su hacmi (litre)")
    p.add_argument("--sicaklik", type=float, default=97.0, help="Anlık sıcaklık °C")
    p.add_argument("--oda", type=str, default="mutfak", help="Tesis adı")
    p.add_argument("--duduksuz", action="store_true", help="Düdük sökülmüşse işaretleyin")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if args.litre <= 0:
        print("HATA: Boş reaktör çalıştırılamaz. Su koyunuz. Bu bir kararnamedir.")
        return 2
    if args.sicaklik < 0:
        print("HATA: Eksi sıcaklık buzdolabı yargısına girer. Bu kurum kaynatır.")
        return 2
    r = Reaktor(litre=args.litre, sicaklik=args.sicaklik, duduksuz=args.duduksuz, oda=args.oda)
    print(tutanak(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
