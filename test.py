from kata import Kata

kt = ['semaunya', 'paseban', 'berlabuh']
kt_gt = ['mau', 'paseban', 'laba']

for x, y in zip(kt, kt_gt):
    kata = Kata(x)
    kata.stem()
    assert kata.bentuk_dasar == y, f"Got {kata.bentuk_dasar}, should be {y}" 

print("All test passed")