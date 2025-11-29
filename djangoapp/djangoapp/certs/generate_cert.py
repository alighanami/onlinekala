from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

# 1) generate private key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# 2) write private key to key.pem (بدون پسورد، مثل -nodes)
with open("key.pem", "wb") as f:
    f.write(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

# 3) build self‑signed certificate
subject = issuer = x509.Name(
    [
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Tehran"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Tehran"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "OnlineKala Dev"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ]
)

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow() - timedelta(minutes=1))
    .not_valid_after(datetime.utcnow() + timedelta(days=365))  # 1 سال
    .add_extension(
        x509.SubjectAlternativeName(
            [x509.DNSName("localhost")]
        ),
        critical=False,
    )
    .sign(key, hashes.SHA256())
)

# 4) write cert to cert.pem
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("✅ cert.pem و key.pem با موفقیت ساخته شدند.")
