
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from datetime import datetime, timedelta


class SimplePKI:
    def __init__(self):
        # Load Root CA Private Key
        with open("Root_CA_private_key.pem", "rb") as f:
          self.root_private_key = serialization.load_pem_private_key(f.read(),password=None)
        with open("Root_CA_certificate.pem", "rb") as f: # Loading Root CA
         self.root_certificate = x509.load_pem_x509_certificate(f.read())
        self.intermediate_ca = {"name": "My_glos_CA"}
        self.users = {}
        self.next_serial_number = 1
        self.model = None
        self.trust = {}
        self.revoked_serials = set()

        self.ra_approved = set()
        self.validated_certificates = set()


    # Registration Authority (RA)

    def verify_identity(self, username):
        if username in self.ra_approved:
            return True

        self.ra_approved.add(username)
        return True


    # Certificate Authority (CA)

    def issue_certificate(self, username):
        if username not in self.ra_approved:
            raise ValueError(f"User '{username}' not approved by RA.")

            # Generate user key pair
        user_private_key = ec.generate_private_key(ec.SECP256R1())
        user_public_key = user_private_key.public_key()

        subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, username),])

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(self.root_certificate.subject)
            .public_key(user_public_key)
            .serial_number(self.next_serial_number)
            .not_valid_before(datetime.now())
            .not_valid_after(datetime.now() + timedelta(days=365))
            .add_extension(

            x509.BasicConstraints(ca=False, path_length=None),critical=True)
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_encipherment=False,
                    content_commitment=False,
                    data_encipherment=False,
                    key_agreement=True,  # IMPORTANT for ECDH
                    key_cert_sign=False,
                    crl_sign=False,
                    encipher_only=False,
                    decipher_only=False
                ),
                critical=True
            )
            .sign(self.root_private_key, hashes.SHA256())
            )


        self.next_serial_number += 1

        # Store data
        self.users[username] = {
            "Private_key": user_private_key,
            "cert": cert
        }
        with open(f"{username}_private_key.pem", "wb") as f: # Save the User_ECC Private Key to a PEM file
            f.write(user_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ))
        with open(f"{username}_certificate.pem", "wb") as f: # Save User_CA_Certificate
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        return cert

    # Verify certificate

    def verify_certificate(self, cert):
        if cert.serial_number in self.revoked_serials:
            raise ValueError("Certificate revoked.")

        root_public_key = self.root_certificate.public_key()
        root_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            ec.ECDSA(hashes.SHA256())
        )
        return True

    # User Registration Flow

    def register_user(self, username):
        if username in self.users:
            raise ValueError(f"User '{username}' already exists.")

        self.verify_identity(username)
        cert = self.issue_certificate(username)

        self.users[username] = {
            "certificate": cert
        }



    # Revoke certificate function
    def revoke_certificate(self,cert):
        self.revoked_serials.add(cert.serial_number)
        print(f"Cert with serial number{cert.serial_number} is revoked.")



    # PKI Models to select from

    def setup_hierarchical(self):
        self.model = "hierarchical"
        self.trust = {
            "root": ["intermediate_ca"],
            "intermediate_ca": list(self.users.keys())
        }

    def setup_web_of_trust(self):
        self.model = "web_of_trust"
        users = list(self.users.keys())
        self.trust = {
            user: [u for u in users if u != user]
            for user in users
        }

    def setup_bridge(self):
        self.model = "bridge"
        self.trust = {
            "ca_group_a": ["joe", "hassan"],
            "ca_group_b": ["callum"],
            "bridge_ca": ["ca_group_a", "ca_group_b"]
        }

    def select_model(self, model_name):
        model_name = model_name.lower()

        if model_name == "hierarchical":
            self.setup_hierarchical()
        elif model_name in ("wot", "web", "web_of_trust"):
            self.setup_web_of_trust()
        elif model_name in ("bridge", "bridge_ca"):
            self.setup_bridge()
        else:
            raise ValueError("Invalid PKI model.")


    # Messaging function

    def send_message(self, sender, receiver, message):
        if sender not in self.users or receiver not in self.users:
            raise ValueError("Sender or receiver not registered in PKI.")

        sender_cert = self.users[sender]["certificate"]
        receiver_cert = self.users[receiver]["certificate"]

        # Verify certificate
        if not self.verify_certificate(receiver_cert):
            raise ValueError("receiver certificate invalid.")
        if not self.verify_certificate(sender_cert):
            raise ValueError("Sender certificate invalid.")

        encrypted_message = message[::-1]  # Placeholder encryption
        signature = f"signature_from_{sender}"

        return {
            "sender": sender,
            "receiver": receiver,
            "encrypted_message": encrypted_message,
            "signature": signature
        }

    def receive_message(self, msg):
        expected_signature = f"signature_from_{msg['sender']}"

        if msg["signature"] != expected_signature:
            return False, "Invalid signature."

        decrypted = msg["encrypted_message"][::-1]
        return True, decrypted





print("User certificate and private_key have been saved.")

# Example Usage to test functionality

if __name__ == "__main__":
    pki = SimplePKI()

    # Register users
    pki.register_user("Mitchell")
    pki.register_user("Paul")

    # Select PKI model
    pki.select_model("hierarchical")

    # Send message
    msg = pki.send_message("Mitchell", "Paul", "Cryptography")

    # Receive message
    success, content = pki.receive_message(msg)

    if success:
        print("Decrypted:", content)
    else:
        print("Error:", content)

print("DONE")