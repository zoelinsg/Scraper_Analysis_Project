# 新聞分析系統

## 簡介

新聞分析系統是一個基於 Django 的網頁應用，用於分析和展示新聞數據。該系統可以從 NewsAPI 獲取新聞資料，並提供多種分析功能，包括新聞發布趨勢、來源分佈、關鍵字分析、文章情感分析和類別分類分析。

## 安裝

1. 克隆此專案到本地：

    ```sh
    git clone https://github.com/yourusername/news-analysis-system.git
    cd news-analysis-system
    ```

2. 安裝 Poetry（如果尚未安裝）：

    ```sh
    pip install poetry
    ```

3. 使用 Poetry 安裝所需的依賴：

    ```sh
    poetry install
    ```

4. 配置環境變數：

    創建 [.env](http://_vscodecontentref_/2) 文件並添加你的 NewsAPI API Key：

    ```env
    NEWSAPI_KEY=your_newsapi_key
    ```

5. 遷移數據庫：

    ```sh
    poetry run python manage.py migrate
    ```

6. 啟動開發伺服器：

    ```sh
    poetry run python manage.py runserver
    ```

## 使用說明

1. 打開瀏覽器並訪問 `http://127.0.0.1:8000/` 以查看首頁。
2. 使用導航欄中的鏈接訪問不同的分析頁面：
    - 首頁
    - 新聞列表
    - 新聞分析
    - 關鍵字分析
    - 來源分佈分析
    - 文章情感分析
    - 類別分類分析
    - 導出資料

## 功能介紹

### 新聞發布趨勢

顯示新聞發布的日期趨勢圖，展示不同日期的新聞數量。

### 來源分佈分析

顯示新聞來源的分佈圖，展示不同來源的新聞數量。

### 關鍵字分析

顯示新聞描述中的關鍵字及其出現頻率。

### 文章情感分析

顯示新聞描述的情感分析結果，展示不同情感類別的新聞數量。

### 類別分類分析

顯示新聞標題的類別分類結果，展示不同類別的新聞數量。

