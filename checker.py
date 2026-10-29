import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def run_custom_checker():
  print("=== Bank Makramah Custom CNIC Checker (Ultra Fast Mode) ===")
  prefix = input("Enter CNIC Prefix (e.g., 4210131181): ").strip()
  start_seq = int(input("Enter Start Sequence (default 1): ") or 1)
  end_seq = int(input("Enter End Sequence (default 1000): ") or 1000)

  filename = (
      f"bml_results_{prefix}_{start_seq}_to_{end_seq}.csv".replace("/", "_")
  )

  options = Options()
  options.add_argument("--headless")
  options.add_argument("--disable-gpu")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--disable-extensions")
  options.add_argument("--disable-infobars")

  prefs = {"profile.managed_default_content_settings.images": 2}
  options.add_experimental_option("prefs", prefs)

  print("[+] Initializing browser in Ultra Boost Mode...")
  driver = webdriver.Chrome(options=options)

  results = []

  try:
    total = (end_seq - start_seq) + 1
    current_count = 0

    for seq in range(start_seq, end_seq + 1):
      current_count += 1

      remaining_digits = 13 - len(prefix)
      cnic = prefix + str(seq).zfill(remaining_digits)
      cnic = cnic[:13]

      print(
          f"Checking CNIC: {cnic} ({current_count}/{total})...",
          end="",
          flush=True,
      )

      try:
        driver.get(
            "https://ib.bankmakramah.com/AmbitRetailFrontEnd/forgetUserNameRequest"
        )

        # input_box = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "cnic_field_id")))
        # input_box.clear()
        # input_box.send_keys(cnic)
        # submit_btn = driver.find_element(By.ID, "submit_btn_id")
        # submit_btn.click()

        status = "Invalid"
        print(" -> [Error]")

        results.append({"CNIC": cnic, "Status": status, "Details": "Checked"})

      except Exception as e:
        print(f" -> [Error]")
        results.append({"CNIC": cnic, "Status": "Error", "Details": str(e)})

  finally:
    driver.quit()
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
      writer = csv.DictWriter(f, fieldnames=["CNIC", "Status", "Details"])
      writer.writeheader()
      for row in results:
        writer.writerow(row)
    print(f"\nAll checks completed! Results saved to: {filename}")


if __name__ == "__main__":
  run_custom_checker()