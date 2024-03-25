## AWS Lambda 函式使用方式

一旦部署完成，我們可以使用有 `invoke` 權限的帳號來呼叫它 (你也可以由 AWS Web Console 直接測試):

```
aws lambda invoke \
  --function-name <your-function-name> \
  --cli-binary-format raw-in-base64-out \
  --payload file://input.json \
  --profile <aws-profile> \
  --no-cli-pager \
  output.json
```

### Input

函式參數有 2 個必要的欄位，是永豐金證券用到的 API Token:

```
$ cat input.json | jq ". | keys"
[
  "sniopac_api_key",
  "sniopac_api_secret_key"
]
```

> 我是將 AWS Lambda 函式設計為多人共用，所以每一次透過 input 給予登入資訊。若想要改寫的朋友，可以將它放到 AWS Secret
> Manager 或隱秘的存放地方。

> 要注意，不能放在 AWS Lambda Function 的環境變數中，因為它是可以直接透過 `get-function` 查到的。 

### Output

輸出的部分，為使用 StockPosition 這個 data class 內的所有欄位，以下列出最初的 2 筆作為範例：

```
$ cat output.json | jq ".[:2]"
[
  {
    "id": 0,
    "code": "0056",
    "quantity": 12200,
    "price": 34.63,
    "last_price": 39.62,
    "pnl": 59770,
    "yd_quantity": 12200,
    "margin_purchase_amount": 0,
    "collateral": 0,
    "short_sale_margin": 0,
    "interest": 0
  },
  {
    "id": 1,
    "code": "006208",
    "quantity": 6250,
    "price": 73.24,
    "last_price": 92.1,
    "pnl": 116505,
    "yd_quantity": 6250,
    "margin_purchase_amount": 0,
    "collateral": 0,
    "short_sale_margin": 0,
    "interest": 0
  }
]
```

### Output :: legacy

由於，我自己是從還沒有正式 API 就開始實作「土炮」API 的使用者，為了相容於舊有的格式，我也有製作 `legacy` 版本，只要在 input
多加 `{"legacy": true}` 即可：

```
$ cat output.json | jq ".[:2]"
[
  {
    "stock": "0056",
    "stocknm": "元大高股息",
    "qty": 12200,
    "mprice": 39.62,
    "real_namt": 483364,
    "namt": 482256,
    "ur_ratio": 14.14721434556412,
    "unreal": 59770
  },
  {
    "stock": "006208",
    "stocknm": "富邦台50",
    "qty": 6250,
    "mprice": 92.1,
    "real_namt": 575625,
    "namt": 574255,
    "ur_ratio": 25.451665756417263,
    "unreal": 116505
  }
]
```