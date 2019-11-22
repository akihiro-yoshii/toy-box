# Python 3.7.5 メモ
## 環境構築
過去にminicondaを入れてあったのでそれで実験
```
$ conda create -n bitflyer python=3.7
```

必要なパッケージ
```
$ conda install pybitflyer matplotlib pandas mpl_finance
```

## 実行方法
環境に入る
```
$ conda activate bitflyer
```

## 作業メモ
下記Documentによると，約定履歴は31日分が取得可能．
https://lightning.bitflyer.com/docs/api?lang=ja#%E7%B4%84%E5%AE%9A%E5%B1%A5%E6%AD%B4

試してみたところ，1回あたり500件取得できる様子．

### 統計処理
下記を参考にした
https://www.moneypartners.co.jp/support/tech/sma.html
単純移動平均線には終値を使うらしい

ロウソク足チャート
https://qiita.com/toyolab/items/1b5d11b5d376bd542022


## 気をつけること
BTCは小数点以下の値を持つが，0.00000001BTCが最小単位のため，妙にfloatで扱うと少数以下の空間で誤差が生じる．

## TODO
- データ抜けチェック
- データのソート箇所の設計
- 定常動作時用の動作を設計

## シミュレータ要件
### 買い注文
- 注文の1分後に指定された価格で買い注文の成立判定を開始
- 指定価格よりterm内最安値が安ければ指定された価格で注文成立
- 不成立時は次のtermへ注文持ち越し
- 最長掲示時間を超えたら注文取消し

### 売り注文
- 注文の1分後に指定された価格で売り注文の成立判定を開始
- 指定価格よりterm内最高値が高ければ指定された価格で注文成立
- 不成立時は次のtermへ注文持ち越し
- 最長掲示時間を超えたら注文取消し

###
