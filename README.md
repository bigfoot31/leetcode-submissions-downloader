# Leetcode submissions downloader

works as of 29 / 05 / 2021.

## Requirememts

1. python3. Tested on `Python 3.6.8`
2. install dependencies

   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Running the code

1. Enter the current [Leetcode](www.leetcode.com) cookie from developer console.

   ```bash
   export LEETCODE_COOKIE_ID=< your leetcode cookie >
   ```

2. Retrived metadata for all problems in [Leetcode](www.leetcode.com). Then download code
   submissions for each of your **Accepted** code.

   ```bash
   python3 leetcode-submissions-downloader.py
   ```

   Leetcode rate limits your api requests. So, there might be a submissions that
   might not get downloaded at the first attempt. Such failed attempts are stored
   in `error.json` file.

   User should retry to download the failed requests again.

   1. commment out `get_all_problems()` in `leetcode-submissions-downloader.py`
   2. run the above bash command again.

3. Once all the submissions are retrieved i.e `error.json` file is empty. Parse through the submissions
   to retrieve the fastest submission for a particular question. If multiple submissions with the same
   fastest runtime then code for the first one is saved with a warning to the user.

   ```bash
   python3 parser.py
   ```

---

Feel free to fork and modify. You may want to download all submissions instead of just the fastest, etc.
