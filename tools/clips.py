import json

clips = []
def c(id, ms, en, note=""):
    clips.append({"id": id, "ms": ms, "en": en, "note": note})

# A — welcome and instructions
c("A01", "Selamat datang ke Rumah Sayang! Ini Oyen. Oyen perlukan seseorang yang baik hati untuk menjaganya. Boleh kamu tolong?",
  "Welcome to Rumah Sayang! This is Oyen. Oyen needs someone kind to look after him. Can you help?", "Ceria, mesra")
c("A02", "Selamat kembali! Kawan-kawan rindu kamu.", "Welcome back! Your friends missed you.", "Gembira")
c("A03", "Ada kawan perlukan bantuan! Perhatikan dan tekan kawan yang perlukan kamu.",
  "Someone needs help! Look carefully and tap the friend who needs you.")
c("A04", "Dua kawan perlukan bantuan! Lihat kedua-duanya. Siapa patut kita tolong dulu? Tekan kawan itu.",
  "Two friends need help! Look at both of them. Who should we help first? Tap that friend.")
c("A05", "Cuba lagi!", "Try again!", "Memberi semangat")
c("A06", "Betul!", "Yes!", "Gembira")
c("A07", "Itu lebih penting, jadi kita tolong dia dulu.", "That is more urgent, so we help them first.")
c("A08", "Kawan ini pun perlukan bantuan. Tapi lihat dulu kawan yang satu lagi.",
  "This friend needs help too. But look at the other friend first.", "Lembut, tidak memarahi")
c("A09", "Kamu semakin pandai! Jom cuba yang lebih mencabar sedikit.",
  "You are getting so good at this! Let's try something a little harder.")
c("A10", "Dia suka sentuhan lembut kamu. Pilihan mana tunjuk kasih sayang?",
  "They like your gentle touch. Which choice shows love?")
c("A11", "Jom pilih yang selamat.", "Let's choose something safe.")
c("A12", "Kawan ini tak apa-apa. Lihat dua kawan yang ada gelembung.",
  "This friend is fine. Look at the two friends with bubbles.")
c("A13", "Kawan ini sedang gembira. Cari kawan yang ada gelembung.",
  "This friend is happy right now. Look for the friend with a bubble.")

# B — Bismillah, day cycle and values
c("B01", "Pilihan yang bagus! Sebelum makan, kita baca Bismillah. Tekan untuk baca Bismillah.",
  "Good choice! Before eating, we say Bismillah. Tap to say Bismillah.")
c("B02", "Pilihan yang bagus! Sebelum minum, kita baca Bismillah. Tekan untuk baca Bismillah.",
  "Good choice! Before drinking, we say Bismillah. Tap to say Bismillah.")
c("B03", "Bismillah.", "Bismillah.", "Perlahan dan jelas")
c("B04", "Alhamdulillah! Hari ini kamu tolong kawan-kawan lima kali. Mereka sudah mengantuk. Selamat malam!",
  "Alhamdulillah! Today you helped your friends five times. They are sleepy now. Good night!", "Tenang, suara waktu tidur")
c("B05", "Selamat pagi! Jom jaga kawan-kawan lagi.", "Good morning! Let's look after our friends again.", "Ceria")
c("B06", "Menjaga haiwan ialah tanggungjawab yang besar. Kamu berjaya!",
  "Looking after animals is a big responsibility. You did it!")
c("B07", "Allah sayang orang yang lemah lembut dan baik hati.", "Allah loves people who are gentle and kind.")
c("B08", "Bila kita jaga orang lain, kita tunjukkan kasih sayang.", "When we care for others, we show love.")
c("B09", "Kawan yang baik perasan bila orang lain perlukan bantuan.", "A good friend notices when someone needs help.")
c("B10", "Dahulu, seorang lelaki memberi air kepada anjing yang dahaga, dan Allah sayang akan kebaikannya.",
  "Long ago, a kind man gave water to a thirsty dog, and Allah loved his kindness.", "Nada bercerita")

# C — praise
c("C01", "Kamu perhati dengan teliti dan pilih dengan betul!", "You looked carefully and chose well!", "Bangga, gembira")
c("C02", "Tangan baik, hati baik!", "Kind hands, kind heart!", "Bangga, gembira")
c("C03", "Pilihan yang bijak!", "That was a smart choice!", "Bangga, gembira")
c("C04", "Dia rasa disayangi!", "They feel loved!", "Bangga, gembira")
c("C05", "Syabas! Kamu sudah menolong kawan.", "Well done! You helped a friend.", "Bangga, gembira")

# D — unsafe foods (gentle, never scolding)
c("D01", "Coklat beracun untuk haiwan. Ia boleh buat mereka sakit teruk.", "Chocolate is poison for animals. It can make them very sick.", "Lembut, tidak menakutkan")
c("D02", "Gula-gula tak elok untuk gigi dan perut haiwan.", "Sweets are bad for animal teeth and tummies.", "Lembut")
c("D03", "Cili terlalu pedas! Mulut mereka akan pedih.", "Chili is too hot! It will hurt their mouth.", "Lembut")
c("D04", "Anggur boleh buat anjing sakit teruk.", "Grapes can make dogs very sick.", "Lembut")
c("D05", "Avokado beracun untuk burung.", "Avocado is poison for birds.", "Lembut")
c("D06", "Susu lembu buat kucing sakit perut. Air bersih paling baik.", "Cow's milk gives cats a tummy ache. Clean water is best.", "Lembut")
c("D07", "Air bergas terlalu manis. Haiwan perlukan air bersih.", "Fizzy drinks are too sweet. Animals need clean water.", "Lembut")

# E–H — one section per pet
NEEDS = [("hungry","lapar"),("thirsty","dahaga"),("dirty","kotor"),("sleepy","mengantuk"),
         ("bored","bosan"),("lonely","kesunyian"),("hurt","cedera"),("sick","tidak sihat")]
for sec, pet, name in [("E","kitten","Oyen"),("F","puppy","Bobo"),("G","rabbit","Gebu"),("H","bird","Kiki")]:
    c(sec+"01", f"Apa yang {name} perlukan?", f"What does {name} need?", "Nada bertanya")
    c(sec+"02", f"Perhatikan {name} baik-baik.", f"Look at {name} carefully.")
    c(sec+"03", f"Bukan itu yang {name} perlukan sekarang.", f"That's not what {name} needs right now.", "Lembut")
    c(sec+"04", f"Sekarang jom tolong {name}.", f"Now let's help {name}.")
    c(sec+"05", f"Tekan {name} dulu.", f"Tap {name} first.")
    if pet != "kitten":
        c(sec+"06", f"Kawan baru! Kenalkan, {name}.", f"A new friend! Say hello to {name}.", "Teruja")
    for i,(en,ms) in enumerate(NEEDS):
        c(f"{sec}{7+i:02d}", f"{name} {ms}.", f"{name} is {en}.", "")

json.dump(clips, open("clips.json","w"), ensure_ascii=False, indent=0)
print(len(clips))
