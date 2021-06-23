if __name__ == "__main__":
    import os
    print(os.urandom(24).hex())
    exit(0)
    if os.path.exists(".env"):
        print(".env file already exists. Exiting...")
    else:
        with open(".env", "w") as f:
            f.write(f"SECRET={os.urandom(24).hex()}")