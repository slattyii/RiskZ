# RiskZ - Zalo Automation Bot 🤖

**AI Generated** 

RiskZ is a Python project to automate certain tasks on Zalo via a bot.
Hiện còn thiếu nhiều tính năng, hiện chỉ chạy lõi

## ⚡ How It Works

- **First run:** The bot will throw an error and create necessary root directories.
- Users must **add a JSON config file** containing IMEI and cookies before the bot can run normally.

### 📁 Config Directory

PROJECT_DIR/root/bot/credentials/

### 📝 Config File Types

1. **Object format** (object cookies):

<name>.json

Example:

{
  "imei": "123456789012345",
  "cookies": {
    "key1": "value1",
    "key2": "value2"
  }
}

2. **List format** (list cookies):

<name>.raw.json

Example:

{
  "imei": "123456789012345",
  "cookies": [
    {
      "name": "value1",
      "value": "value2"
    },
    {
      "name": "value1",
      "value": "value2"
    },
    {
      "name": "value1",
      "value": "value2"
    }
  ]
}

> Note: `imei` is a string, `cookies` can be an object or a list of objects with key-value pairs.

## 🚀 How to Run

python init.py

- First run will create root directories.
- Add JSON files into root/bot/credentials/.
- Run again for the bot to work properly.

## 🛠️ Requirements

- Python 3.9+
- Dependencies listed in requirements.txt

## ⚠️ Warning

- **Do not share JSON files** containing cookies—they are sensitive info.
- Folder structure and file names must be exact, or the bot will fail to recognize configs.
- Không chia sẽ tệp hay nội dung tệp JSON, đây là dữ liệu quan trọng
- Cấu trúc thư mục và tên tệp phải chính xác
