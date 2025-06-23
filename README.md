# FAQ 質問回答システム

## 目的

ChatGPTの検証ををFAQ検索というタスクで検証し、実現の可能性を検討する

くわしくはこちら
https://www.notion.so/crowdworks-product/ChatGPT-FAQ-63c449a7071045cbaf8f9b1a73b76223

## ローカル実行

### インデックスの作成



## デプロイ方法

[Serverless Framework](https://www.serverless.com/)により、AWS環境にデプロイします。

curl -i \
  -H "Content-type: application/json" \
  -H "Accept: application/json" \
  -d '{"query":"メールアドレスを変更したい"}' \
  'https://<your-api-id>.lambda-url.ap-northeast-1.on.aws/'
