# test_password_generator.py
import string
from src.password_generator import generate_password

def test_length():
    pwd = generate_password(10)
    assert len(pwd) == 10

def test_characters():
    pwd = generate_password(12)
    for ch in pwd:
        assert ch in (string.ascii_letters + string.digits + string.punctuation)

if __name__ == "__main__":
    test_length()
    test_characters()
    print("All tests passed!")
