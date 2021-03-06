Giriş
Bu projede bilgisayarımızın özelliklerinin Matris çarpma işlemine etkisini inceleyeceğiz.
2. Sistem Bilgileri
2.1 Bilgisayarınızın FLOP/s kapasitesi nedir?
SiSoftware Sandra da güncel olarak yaptığım Benchmark testinde aşağıdaki sonuçları aldım.
•	Single Core  için 4.36 GFLOPS
•	Multi Core için 14.81 GFLOPS



2.2 Sisteminizin Cache belleğin özelliklerini açıklayınız, I-Cache, D-Cache kapasiteleri nelerdir?
Cache: İşlemci önbelleği, CPU'nun hafızadaki verilere ulaşma süresini azaltan bir donanımdır. Ana belleğe kıyasla küçük, hızlı ve işlemci çekirdeğine yakındır. Sık kullanılan veriler ya da en güncel veriler işlemci önbelleğinde saklanır.
Bu soruyu yanıtlamak için CPU-Z isimli programı kurdum ve Cache özelliklerimi aşağıdaki gibi görüntüledim.
Yandaki görüntüde ilk satırda D-cache kapasitesi, ikinci satırda I-cache kapasitesi gözükmektedir.


2.3 Tampon bellekler için 4-yönlü (4-way) ne demektir?
4 yönlü önbellek, bir kümeye o kümenin veri eşlemesinin bulunabileceği 4 blok vererek veri çakışmalarını azaltır. Bellek adresleri bir kümeyle eşleştirilir. Ancak 4 blok herhangi bir kümeyle eşleştirilebilir. 

2.8.1 Hazırladığınız FLOAT ve DOUBLE sürümlerde farklılık var mıdır?
Float ve Double değişken tiplerinin bellekteki saklama kapasitelerinin farklı olması sebebiyle koşma sürelerinde farklılıklar vardır. Float veri tipi bellekte 4 bytelık bir alan kaplarken Double 8 bytelık bir alan kaplar.


 Projeyi gerçekleştirirken OpenMP kullandım.
OpenMP
OpenMP çoklu iş parçacığı gerçekleştirimidir. Çoklu iş parçacığı ana iş parçacığının(sırasıyla yürütülen komutların bir dizisi) belirli bir sayıda yardımcı iş parçacıklarını durdurması ve bir görev onlar arasında paylaştırması olan paralelleştirme metodudur. İş parçacıkları birbiri ardında paralel şekilde çalışırlar. Farklı işlemcilerin iş parçacıkları farklı çalışma zamanı ortamlarını kendilerine tahsis ederler.
Paralel çalışacak olan kodun bir bölümü sırasıyla işaretlenir. Bu işaretleme kod bölümünün yürütülmesinden önce iş parçacıklarının o kod bölümüne girmelerine sebep olacak ön işlemci direktifleridir. Her bir iş parçacığı onlara bağlı bir ID'ye sahiptir. omp_get_thread_num()fonksiyonu ile bu ID elde edilir.İş parçacığı ID'si bir tam sayıdır ve ana iş parçacığının ID'si sıfırdır. Paralelleştirilmiş kodun yürütülmesinden sonra iş parçacıkları ana iş parçacığına tekrar geri katılırlar. Programın sonuna kadar bu böyle devam eder.
Varsayılan olarak her bir iş parçacığı kodun paralelleştirilmiş bölümünü birbirinden bağımsız şekilde yürütür. İş paylaşımı yapıları iş parçacıkları arasında bir görevi paylaştırmak için kullanılabilir, böylece her bir iş parçacığı kodun kendisine ayrılan bölümünde çalışır. Hem görev paralelleştirme hem de veri paralelleştirme OpenMP kullanarak bu yöntemle yapılır.
Çalışma zamanı ortamı kullanıma bağlı olarak işlemcilere iş parçacığı tahsis eder, makine yükleme ve diğer faktörler gibi. İş parçacıklarının sayısı ortam değişkenleri veya kod içerisinde kullanılan fonksiyonlara bağlı olarak çalışma zamanı ortamı tarafından atanır. OpenMP fonksiyonları omp.h etiketli C/C++ header dosyaları ile programa dahil edilir.



Öncelikle VS2019 da OpenMP default olarak desteklenmediği için bu özelliği aktif hale getirdim. 

Sonrasında gerekli olan float ve double matrislerimi tanımlayarak bunların içerisini otomatik olarak istenilen değerlerle doldurmamı sağlayan matris() fonksiyonunu yazdım. Bu fonksiyon sayesinde matrismizin satır değerlerine 1.0 değerini verdim.
 
Bu adımdan sonra seri matris çarpım işlemlerini yapabilmek için çarpım fonksiyonlarımı yazmaya başladım. Aynı zamanda bu işlemler yapılırken süreyi ölçebilmek için hazır clock() fonksiyonunu kullandım.
 

 
Bu adımdan sonra aynı işlemi paralel bir şekilde koşmak için paralel çarpım fonksiyonlarını yazdım.
 
 

Gerekli fonksiyonları tanımladıktan sonra kodun en başında:

 #define N 1000 


Olarak tanımladığımız değer ile matrisin satır ve sütun sayı değerlerini değiştirerek farklı boyutlardaki matrisler için yapığımız çarpım işlemlerinin ne kadar süre aldıklarını ölçmek için programımı çalıştırdım.

1000*1000 lik matrislerin için Float ve Double veri tiplerindeki matrislerin seri ve paralel çarpım süreleri farklık göstermektedir. Çünkü Cpu-Z programından da gördüğümüz gibi bilgisyarımın thread sayısı 8’dir. Bizim yaptığım işlem seri olarak koştuğumuz programımızı 8 iş parçacığı halinde paralelleştirerek daha hızlı sonuç almayı amaçlamaktadır.
 

#define thread_sayisi 8

 

	Yukarıdaki örnek çıktıdan da gördüğümüz üzere seri işlem süreleri ile paralel işlem süreleri arasında çok büyük farklar vardır. Aynı zamanda görüldüğü gibi float veri tipi ve double veri tipi arsında da çarpma işlemi sürelerinde farklılık vardır. Bunun sebebi raporumun başında da açıkladığım gibi double ve float veri tipleri arasındaki boyut farkıdır.

	Aynı işlemleri farklı boyutlardaki matrisler ile de denediğimizde aşağıdaki değerleri alıyorum.
 
#define N 2000 için



 



#define N 3000 için



Burada dikkat etmemiz gereken noktalardan biri bu işlemler gerçekleştirilirken CPU daki yoğunluktur. Yaptığım denemelerden gözlemlediğim üzere CPU daki yoğunluğa göre işlem süreleri değişkenlik gösterebilmektedir. Örneğin 1000*1000 lik bir matris için 4 saniyede yapılan bir işlem başka bir zamanda yapıldığında 5 saniye çıkabilir. Aynı zamanda gözlemlerim üzerine yaptığım çıkarıma göre aynı boyuttaki matrisler için üst üste yaptığım aynı işlemlerde hem seri hem de paralel koşma sürelerinde azalma olmaktadır.



Koşma süreleri
(8 Thread’li)	1000*1000	2000*2000	3000*3000	4000*4000	5000*5000
SERİ	FLOAT	4.696 sn	104.732 sn	362.859 sn	861.485 sn	
	DOUBLE	5.827 sn	114.801sn	474.797 sn	975.159 sn	
PARALEL	FLOAT	0.3471 sn	3.1928 sn	13.0384 sn	36.0473 sn	
	DOUBLE	0.375 sn	3.5852 sn	14.5961 sn	38.145 sn	

Not :5000*5000 seri çarpım işlemleri çok fazla süre aldığı için bir yerden sonra işlemcim çok fazla ısındığı için ve düşünceme göre bellek çok şiştiği için değerleri gözlemleyemedim. Bu işlem için derlerken bir hata almadım ama derlenme süresinde bir çıktı alabilmek için yaklaşık 30 dakika kadar bekledim bu sırada VS19 ‘un özelliği sayesinde cpu nun %100 e kadar çalıştığını gözlemledim.
