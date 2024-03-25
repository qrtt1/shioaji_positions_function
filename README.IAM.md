## IAM 權限

為了讓 GitHub Action 能順便部署 AWS Lambda Function 請至少設定下列權限。

> 請把 json 範例內的 `<aws-account-number>` 換成你的數字帳號。

### PassRole 權限

在 AWS 外使用 AWS Lambda Function 時需要的權限

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::<aws-account-number>:role/*"
    }
  ]
}
```

### 建立與更新 AWS Lambda Function 的權限

這些權限會用在 [create-or-update-lambda-function.sh](scripts%2Fcreate-or-update-lambda-function.sh) 之內：

* get-function：先確認有無同名的 function 存在，當 function 不存在時就建立它。反之，使用最新的程式更新它。
* create-function：建立新的 function 與初始設定。
* update-function：用新的程式更新既有的 function。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": [
        "lambda:CreateFunction",
        "lambda:CreateCodeSigningConfig",
        "lambda:Get*",
        "lambda:List*",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionCodeSigningConfig",
        "lambda:UpdateFunctionConfiguration",
        "lambda:UpdateFunctionEventInvokeConfig",
        "lambda:UpdateFunctionUrlConfig"
      ],
      "Resource": "arn:aws:lambda:*:<aws-account-number>:*"
    }
  ]
}
```

### 程式碼上傳與下載的權限

當 AWS Lambda 使用的「程式碼」太大時，推薦的方法是先上傳至 AWS S3，再透過指定 AWS S3 的位置進行更新。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::qty.lambda/*"
    }
  ]
}
```