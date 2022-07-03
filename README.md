# Honey-Encryption-with-HoneyWord
using NLP and honeyword to construct a honey encryption algorithm

## Introduction of honey-encryption
Original Password-Based Encrytion (PBE):
  攻擊者能一次嘗試大量的密碼(key)來對密文進行解密，而且他也能從過去被洩漏出的用戶密碼資料預測出用戶會使用什麼樣的密碼，因此若是使用低強度密碼的用戶，我們基本可以假設攻擊者嘗試的key的集合裡一定有正確的key，那重點就變成攻擊者能不能從用這些key解密出的可能明文中，分辨出真正的明文。使用傳統PBE的情況下，用錯誤key解密出的明文有極大機率會是一串亂碼或是沒有意義的字串，
  ![](https://www.researchgate.net/profile/Oludare-Omolara/publication/329999109/figure/fig1/AS:709414373826561@1546148975326/An-illustration-of-the-setting-of-the-conventional-encryption-scheme-in-a-brute-force.ppm)
Honey encryption 便是為了反制 brute-force attack 而被設計出來的系統，它能強化傳統的 Password-Based Encryption (PBE)，讓使用低強度密碼的用戶也能獲得相當的安全性
