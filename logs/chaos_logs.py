import time
import random
import datetime

# List of realistic DevOps disasters
ERROR_TEMPLATES = [
    # 1. Database & Connection Issues
    "ERROR [payment-service] Database connection timed out after 3000ms. Host: rds.aws.internal",
    "CRITICAL [order-service] Could not connect to Redis at 10.0.1.5:6379. Connection refused.",

    # 2. Security & SSL Errors
    "ERROR [nginx-ingress] SSL_do_handshake() failed (SSL: error:14094412:ssl3_read_bytes:sslv3 alert bad certificate)",
    "FATAL [gateway-service] Upstream SSL certificate expired. Target: api.stripe.com",

    # 3. Secrets & Auth Errors
    "ERROR [auth-service] botocore.exceptions.ClientError: An error occurred (AccessDenied) when calling the GetSecretValue operation.",
    "ERROR [user-service] Failed to fetch JWT_SECRET from HashiCorp Vault. Permission denied.",

    # 4. Java/Python Specific Exceptions
    "FATAL [inventory-java] java.lang.NullPointerException: Cannot invoke 'String.length()' because 'input' is null at Service.java:102",
    "ERROR [analytics-py] ZeroDivisionError: division by zero in /app/math_utils.py line 15",

    # 5. Infrastructure/Resource Issues
    "CRITICAL [worker-node-1] System running out of memory (OOM). Killing process 4512.",
    "ERROR [disk-monitor] No space left on device: /var/lib/docker/overlay2"
]


def generate_chaos():
    print("🔥 Chaos Log Generator Started...")
    while True:
        # Pick a random error
        error_msg = random.choice(ERROR_TEMPLATES)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        full_log = f"{timestamp} {error_msg}\n"

        # Write to the shared log file
        with open("/home/logs/app.log", "a") as f:
            f.write(full_log)

        print(f"Generated: {error_msg}")

        # Random delay between 2 to 8 seconds to mimic real traffic
        time.sleep(random.uniform(2, 8))


if __name__ == "__main__":
    generate_chaos()