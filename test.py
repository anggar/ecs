from kata import Kata

kt = ['berbunga-bunga','menyia-nyiakan','menyanyi', 'menyangka', 'mencintaimu', 'mengharapkan', 'seperti', 'memedulikanmu', 'mempelajari', 'menakjubkan', 'memproklamasikan', 'mengaburkan', 'lamunannya', 'memberi', 'teman-temannya', 'semaunya', 'paseban', 'berlabuh', 'menelan', 'menahan']
kt_gt = ['bunga', 'sia','nyanyi', 'sangka','cinta', 'harap', 'seperti', 'peduli', 'ajar', 'takjub', 'proklamasi', 'kabur', 'lamun', 'beri', 'teman', 'mau', 'paseban', 'labuh', 'telan', 'tahan']

for x, y in zip(kt, kt_gt):
    # print(x, y)
    kata = Kata(x)
    kata.stem()
    # if( kata.bentuk_dasar != y) :
    print(f"{kata.bentuk_dasar} {y}" )

print("All test passed")