from cryptography.hazmat.primitives import hashes, serialization
x = private_key_pem = b"""-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCzb2bTVd3ePy/Xx8c+OYfv1JG0n//UB+kLUvJLH0cvbK5KFdkj
+F07Ly/Rj3VszTDVGohgjaop83mW1yPLI1/2ENX9afvmWzuYm4kGWgq2EHamwcqA
B/yyfK1A7CiLqBdmaDPP9q7RLv/yn/8a+vV6uc+c2FyNtR4984MLitAAWQIDAQAB
AoGAOYpH1w16EIMCvJd79SBNz0LDVsDYMQ44VUFMIXruQO8BFRDciQRkIU6IbxMp
/LHwLuZLRWsoXjuNiimDeOjnJF9TqXpTNTQv6nIAcP0E88o6lLYlBCHKWeISLUjP
kfZYKRMfIgrtTebDSq+GqS/i2AzyTzPl5bNSUEC/RBHxiOECQQDEQlnsMtrKQ7sZ
AQn4/oJAlVdCrBTYmEZK1eeBD2gcmnSOjdXc1lGWzMLAXK4ktEnmK2K3YKv/eJLc
62ysZDxnAkEA6g4Ghk3G+Brdx2STQw7rzokhr7mgzAMfi6PnXbA/1KWWmPB2hNpv
8/ufhDXbjq11PSaQZL8msGJ7ZewM+NvlPwJAE9n2SIr4UH87XJMbVCFCQZAZjHfl
f+cfLRCn4wkQ6dvBsG2uVTEkfZFmnZiCUNofo3V9/bh8jVG/4TK7AlD9PwJBALzr
k0Km1vp+nRML0H3pNlcgg0tW9z6VKspJA0CxOeSHwBY0ykWUF5eFPA24dz8kLaSt
UxGu5SisZVQwg4v/2nsCQC0ggKRKp8ULo0uJ5uQVePNjt/l+FZ/XfsHmGEKkQWw0
tfftguIM+pxGiJPUNcjtvIqfu0GfoxyyzniDvfjkzCs=
-----END RSA PRIVATE KEY-----"""


key = serialization.load_pem_private_key(
   x,
    password=None,
)

print(key)