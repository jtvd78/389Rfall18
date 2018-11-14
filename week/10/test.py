
import md5py

hash1 = 'c2b8cd14e80b5dd10fc0a2d633396e31'

hash2 = '14cdb8c2d15d0be8d6a2c00f316e3933'

# initialize hash object with state of a vulnerable hash
fake_md5 = md5py.new('A' * 64)
fake_md5.A, fake_md5.B, fake_md5.C, fake_md5.D = md5py._bytelist2long(hash2.decode('hex'))

print md5py._bytelist2long(hash2.decode('hex'))

# update legit hash with malicious message
#fake_md5.update(malicious)

# fake_hash is the hash for md5(secret + message + padding + malicious)
fake_hash = fake_md5.hexdigest()
print('Fake hash is "%s"' % fake_hash)