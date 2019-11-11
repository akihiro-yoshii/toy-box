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
- BTC取り扱い単位のsatoshi化
- データ抜けチェック
- データのソート箇所の設計
- 定常動作時用の動作を設計
- データ取り扱いのpandas化
