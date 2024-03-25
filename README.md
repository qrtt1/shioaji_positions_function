## 永豐金證券 Sinopac 報價函式

這個專案包裝永豐金證券 Python API 為 AWS Lambda Function 作為日常查詢持股價格使用。主要的功能：

1. 使用 GitHub Action 自動部署
2. 提供 AWS Lambda Function 查詢持股狀態

## .env 設定

開發的 `.env` 檔，請包含下列變數，複製並修改 [.env.example](.env.example) 完成填寫：

| 變數名稱                           | 說明                        |
|--------------------------------|---------------------------|
| AWS_ACCESS_KEY_ID              | 用於訪問 AWS 服務的存取金鑰 ID       |
| AWS_SECRET_ACCESS_KEY          | 用於訪問 AWS 服務的秘密存取金鑰        |
| AWS_DEFAULT_REGION             | 指定 AWS 服務的預設區域            |
| TARGET_S3_BUCKET               | 目標 S3 儲存桶的名稱              |
| TARGET_S3_KEY                  | 目標 S3 儲存桶內的檔案鍵值           |
| TARGET_LAMBDA_FUNCTION         | 目標 Lambda 函式的名稱           |
| TARGET_LAMBDA_FUNCTION_HANDLER | 處理目標 Lambda 函式的處理器名稱      |
| TARGET_LAMBDA_ROLE             | 執行目標 Lambda 函式所需的 IAM 角色  |
| SNIOPAC_API_KEY                | 用於存取 SNIOPAC 服務的 API 金鑰   |
| SNIOPAC_API_SECRET_KEY         | 用於存取 SNIOPAC 服務的 API 秘密金鑰 |

### AWS 帳號

為了要能夠由 GitHub Action 自動更新 AWS Lambda Function，請完成下列變數的設定。

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
```

請由 AWS IAM 建立出新的使用者，並授予適當的權限。請參考文件 [IAM 權限](README.IAM.md) 進行設定。

### Function 建立與更新的變數

AWS Lambda Function 相關的變數分為二組：

```
TARGET_LAMBDA_FUNCTION=
TARGET_LAMBDA_FUNCTION_HANDLER=
TARGET_LAMBDA_ROLE=
```

```
TARGET_S3_BUCKET=
TARGET_S3_KEY=
```

與 AWS Lambda 相關的會用在函式的建立與更新。`TARGET_LAMBDA_FUNCTION` 是函式的名稱，`TARGET_LAMBDA_FUNCTION_HANDLER` 則是指向
Python method 的資訊，而 `TARGET_LAMBDA_ROLE` 決定了函式可以有什麼權限來使用 AWS 資源。請事先在 AWS IAM
內建立好 `TARGET_LAMBDA_ROLE`。

與 AWS S3 相關的變數會用在「程式碼」資訊，因為我們透過 [pack-for-lambda.sh](pack-for-lambda.sh) 在 GitHub Action
內打包好所有的「相依函式庫」內容會變得巨大，無法直接使用 inline code 的方式更新 AWS Lambda。我們採用指定 AWS S3
位置的方式更新。這樣的更新方式，有一個細節要注意，那就是 AWS S3 的 region 必需與 AWS Lambda 一致才行，否則被 AWS Lambda
拒絕使用。

### 永豐金證券 API Token

請由永豐金證券網站上申請使用，至少開通 `帳務` 的權限。

```
SNIOPAC_API_KEY=
SNIOPAC_API_SECRET_KEY=
```

## GitHub Action Secret

上述的變數都得設定至 GitHub Action 內的 Repository Secret 之內。你可以透過 [GitHub CLI](https://cli.github.com/) 來完成這件事。

假設你 fork 了這個專案，取名為 `foo/barbar` 那請執行此 `gh` 指令：

```bash
$ gh secret set -f .env --repo foo/barbar
✓ Set Actions secret SNIOPAC_API_SECRET_KEY for foo/barbar
✓ Set Actions secret TARGET_LAMBDA_ROLE for foo/barbar
✓ Set Actions secret TARGET_S3_KEY for foo/barbar
✓ Set Actions secret AWS_DEFAULT_REGION for foo/barbar
✓ Set Actions secret AWS_SECRET_ACCESS_KEY for foo/barbar
✓ Set Actions secret TARGET_LAMBDA_FUNCTION for foo/barbar
✓ Set Actions secret AWS_ACCESS_KEY_ID for foo/barbar
✓ Set Actions secret TARGET_S3_BUCKET for foo/barbar
✓ Set Actions secret SNIOPAC_API_KEY for foo/barbar
✓ Set Actions secret TARGET_LAMBDA_FUNCTION_HANDLER for foo/barbar
```
