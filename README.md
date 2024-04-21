# Linovelib Novel Crawler

This is a novel crawler specifically designed to crawl novels from the website [https://tw.linovelib.com/](https://tw.linovelib.com/). The crawler allows you to specify the range of novels you want to crawl and provides progress logging and error handling functionalities.

## Getting Started

To use this novel crawler, follow the steps below:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/listenrwt/linovelib-novel-crawler.git
   ```

2. Install the required dependencies. Make sure you have Python 3.x and pip installed, and then run the following command:

   ```bash
   pip install -r requirements.txt
   ```

3. Open the `crawler.py` file and modify the `start_book_no` and `end_book_no` variables to set the range of novels you want to crawl. These variables represent the starting and ending book numbers respectively.

4. Run the crawler script:

   ```bash
   python novel_crawler.py
   ```

   The crawler will start fetching and saving the novels within the specified range. The progress will be logged in the terminal, displaying the current book number being crawled.
   ![Screenshot 2024-04-21 155910](https://github.com/listenrwt/linovelib-novel-crawler/assets/123095693/a7df6c46-ef2c-4ab0-80a1-f53edf585460)

## Logging

The crawler provides logging functionality to track the progress and handle errors. Two log files are created:

1. `progressLog.txt`: This file keeps track of the number of crawled novels and the number of failed crawls. It is updated in real-time during the crawling process.

2. `errorLog.txt`: This file stores all the error messages encountered during failed crawling attempts. Each error message is appended to the file, allowing you to review and troubleshoot any issues.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this code for personal or commercial purposes.

