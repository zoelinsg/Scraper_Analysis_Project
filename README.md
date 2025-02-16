# Scraper_Analysis_Project

## 專案簡介
網頁爬蟲和數據分析的專案，旨在從網頁中提取數據並進行分析。

## 安裝

1. 克隆此專案到本地：

    ```sh
    git clone https://github.com/zoelinsg/Scraper_Analysis_Project.git
    ```

2. 安裝 Poetry（如果尚未安裝）：

    ```sh
    pip install poetry
    ```

3. 使用 Poetry 安裝所需的依賴：

    ```sh
    poetry install
    ```

4. 遷移數據庫：

    ```sh
    poetry run python manage.py migrate
    ```

5. 啟動開發伺服器：

    ```sh
    poetry run python manage.py runserver
    ```