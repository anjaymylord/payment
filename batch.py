# batch.py

import threading


def batch_execute(func, messages, batch_size=10):
    # Memecah pesan menjadi batch sesuai dengan ukuran batch yang diberikan
    batches = [messages[i:i + batch_size] for i in range(0, len(messages), batch_size)]

    # Eksekusi setiap batch dalam thread terpisah
    for batch in batches:
        t = threading.Thread(target=func, args=(batch,))
        t.start()
