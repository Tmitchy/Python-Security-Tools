import secrets
import time
import hashlib
import tracemalloc
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography import x509
from cryptography.hazmat. primitives import serialization


def load_pri_key(path): # Creating a function to upload recipient private key
    with open(path, "rb") as f: return serialization.load_pem_private_key(f.read(), password= None)

def load_pub_key_from_cert(cert_path): # Creating a function to upload recipient public/cert key
    with open(cert_path, "rb") as f: cert = x509.load_pem_x509_certificate(f.read())
    return cert.public_key(), cert
def verify_certificate(cert, ca_cert_path):# Creating a function to verify certificate with CA_ertificate
    with open(ca_cert_path, "rb") as f:
        ca_cert = x509.load_pem_x509_certificate(f.read())

    ca_public_key = ca_cert.public_key()

    ca_public_key.verify(
        cert.signature,
        cert.tbs_certificate_bytes,
        ec.ECDSA(cert.signature_hash_algorithm)
    )

    print("Certificate verified successfully.")

# Creating  and Designing a lightweight Cryptographic system


def encrypt(data: bytes,receiver_public_key): # The Encrypt System function
  sha_256 = hashlib.sha256(data).hexdigest() # Hashing the (data)

  tracemalloc.start() # memory usage measurement
  start_time = time.time() # Calculating for encrypt start to end time.

  start_time_gen_keypair = time.perf_counter()      #start time for key pair generation
  eph_pri = sender_pri #ECC private Key
  eph_pub = sender_pub # ECC public Key
  end_time_gen_keypair = time.perf_counter()         #end time for key pair generation

  # ECDH shared secret to create the key
  shared_sec= eph_pri.exchange(ec.ECDH(), receiver_public_key)

  # Deriving symmetric key using HKDF for AES
  key = HKDF(
      algorithm=hashes.SHA256(),
      length=32,
      salt=None,
      info=b"Light weight cryptographic system",
  ).derive(shared_sec)


  encryptor = AESGCM(key) #Encrypt data with AES.MODE_GCM
  nonce = secrets.token_bytes(16)
  ciphertext = encryptor.encrypt(nonce,data,None) # This is responsible for encrypt the contents in data


  end_time = time.time()
  currentMem,peakMem = tracemalloc.get_traced_memory()# Gathering information on current and peak memory
  tracemalloc.stop()

  print("Encrypted Message:", ciphertext)
  print("Encrypt Time: ", (end_time - start_time))
  print("key pair generation time: ", (end_time_gen_keypair - start_time_gen_keypair))
  print("peak Memory for encryption:", peakMem,"bytes")
  print("Current Memory for encryption:", currentMem,"bytes")

  return {          # returning the values and output = payload

    "ciphertext": ciphertext,
    "nonce": nonce,
    "eph_pub":eph_pub,
    "sha_256":sha_256,
  }



def decrypt(payload, receiver_private_key):  #The Encrypt System function.
    tracemalloc.start()  #memory usage measurement.
    start_time = time.time()  # Calculating for encrypt start to end time.

    shared_sec = receiver_private_key.exchange(ec.ECDH(), payload["eph_pub"]) #creating shared key for decryption.
    key = HKDF(
      algorithm=hashes.SHA256(),
      length=32,
      salt=None,
      info=b"Light weight cryptographic system",
    ).derive(shared_sec)

    decryptor = AESGCM(key)   #Decrypt data with AES.MODE_GCM.
    plaintext = decryptor.decrypt(
      payload['nonce'],
      payload['ciphertext'],
      None
    )

    decrypt_hash= hashlib.sha256(plaintext).hexdigest()
    print("Decrypt Hash: ", decrypt_hash)

    if decrypt_hash != payload['sha_256']:  # Hash verification, to determine if the payload/data was modified
     raise RuntimeError()

    end_time = time.time()
    currentMem,peakMem = tracemalloc.get_traced_memory()

    print("Decrypted Message:", plaintext)
    print("Decrypt Time: ", (end_time - start_time))
    print("Peak Memory for decryption:", peakMem,"bytes")
    print("Current Memory for decryption:", currentMem,"bytes")

    return {                  #returning the values and output = plainT
     "plaintext": plaintext,
     "peakMem":peakMem,
     "currentMem":currentMem
    }

with open("SOC Analyst.txt", "rb") as f:  # To read the contents of the file(SOC Analyst.txt) in binary.
  data = f.read()


recipient_pri = load_pri_key("Mitchell_private_key.pem") # The user's private key
recipient_pub, recipient_cert = load_pub_key_from_cert("Mitchell_certificate.pem")# The user's public key

verify_certificate(recipient_cert, "Root_CA_certificate.pem") # Verifies the certification

sender_pri = load_pri_key("Paul_private_key.pem")
sender_pub, sender_cert = load_pub_key_from_cert("Paul_certificate.pem")

verify_certificate(sender_cert, "Root_CA_certificate.pem")
payload = encrypt(data,recipient_pub) # executes the encrypt function
plainT = decrypt(payload,recipient_pri)# executes the decrypt function

print("DONE")





