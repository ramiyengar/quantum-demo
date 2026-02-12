import oqs

# Initialize the KEM for ML-KEM-768 (NIST Level 3)
with oqs.KeyEncapsulation("ML-KEM-768") as kem:
    # 1. Alice generates her key pair
    public_key = kem.generate_keypair()
    
    # 2. Bob encapsulates a secret using Alice's public key
    # He gets a ciphertext (to send to Alice) and a shared secret
    ciphertext, shared_secret_bob = kem.encap_secret(public_key)
    
    # 3. Alice decapsulates the ciphertext using her secret key
    shared_secret_alice = kem.decap_secret(ciphertext)

    print(f"Shared secrets match: {shared_secret_alice == shared_secret_bob}")
