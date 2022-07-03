# Honey-Encryption-with-HoneyWord
using NLP and honeyword to construct a honey encryption algorithm

## Introduction of honey-encryption
#### Original Password-Based Encrytion (PBE):
  
  
  攻擊者能一次嘗試大量的密碼(key)來對密文進行解密，而且他也能從過去被洩漏出的用戶密碼資料預測出用戶會使用什麼樣的密碼，因此若是使用低強度密碼的用戶，我們基本可以假設攻擊者嘗試的key的集合裡一定有正確的key，那重點就變成攻擊者能不能從用這些key解密出的可能明文中，分辨出真正的明文。使用傳統PBE的情況下，用錯誤key解密出的明文有極大機率會是一串亂碼或是沒有意義的字串
  
![](https://i.imgur.com/9xVUw7B.png)
  
  
#### Password-Based Encryption with Honeyword
Honey encryption 便是為了反制 brute-force attack 而被設計出來的系統，即使使用錯誤的key，解密出的明文也會是有意義的字串或假的明文，讓攻擊者以為就是真正的明文。它能強化傳統的 Password-Based Encryption (PBE)，讓使用低強度密碼的用戶也能獲得相當的安全性。

![](https://i.imgur.com/NHbe8Dc.png)

Honey encryption由兩個主要步驟組成。
首先使用 DTE (Distribution Transforming Encoder) 將需要加密的明文從Message space(M)映射到Seed space(S)，然後再用 PBE (Password-Based Encryption) 對seed進行加密得到密文。


## Implementation

![image](https://user-images.githubusercontent.com/71398477/177034248-96bcab2d-95e6-4670-ab32-1c3337655745.png)

#### Step1 :
我們透過spaCy這個套件得到我們想要的句子各種屬性後，開始產生我們的seed。這邊做法就是把這個字詞在我們從opensource的dataset中收集到的dictionary在第幾個字，存下來他的index，還有句型，將這些數字通通串再一起，與randomNumber做xor產生seed。

#### Step2 :
為了防範dictionary attack，我們同樣對password加鹽，產生我們的key
