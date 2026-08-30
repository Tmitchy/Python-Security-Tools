from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from datetime import datetime, timedelta

# Generate key pair for Certificate of Authority:
ca_private_key = ec.generate_private_key(ec.SECP256R1())
ca_public_key = ca_private_key.public_key()


# Certificate subject & issuer:
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"UK"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Gloucestershire"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Cheltenham"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"UOG"),
    x509.NameAttribute(NameOID.COMMON_NAME, u".glos.ac.uk"),
])

# Build certificate:
ca_cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(subject)  # self-signed
    .public_key(ca_public_key)
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.now())
    .not_valid_after(datetime.now() + timedelta(days=365))
    .sign(ca_private_key, hashes.SHA256())
)

# Save the ECC Private Key to a PEM file:
with open("Root_CA_private_key.pem", "wb") as f:
    f.write(ca_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

# Save CA_Certificate:
with open("Root_CA_certificate.pem", "wb") as f:
    f.write(ca_cert.public_bytes(serialization.Encoding.PEM))

print("Root_CA cert and private_key have been saved.")

