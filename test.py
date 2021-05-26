import time

start_time = time.time()
try:
    import gtu_result_fetcher
except KeyboardInterrupt:
    print("User exit the program")

end_time = time.time()
total_time = end_time - start_time

print("\n\nTime: ", total_time)
