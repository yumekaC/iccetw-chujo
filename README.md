# iccetw-chujo
## 4.B On-demand streaming
・１フレームあたりの点群の描画にかかる処理時間を考慮して，再生フレームレートを決め，ダウンロードするフレーム番号をスキップすることで，30fpsと同じ速さで再生させる．

・１フレームあたりの点群のダウンロードにかかる処理時間を考慮して，再生終了までバッファが枯渇しないように初期バッファサイズを決定する．


表1　パラメータ設定とデモ動画のリンク

| setting | voxel size(m) | initial buffer size(frames) | frame rate(fps) | demo video link |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 0 | 29 | 5 | [条件1デモ動画](https://waseda.box.com/s/j1j5r2h9y4u20q8sp215was04gda9xdw) |
| 2 | 0.003 | 65 | 10 | [条件2デモ動画](https://waseda.box.com/s/y94tg5xyte84mzaf1dywkod5tw12j7pa) |
| 3 | 0.005 | 79 | 15 | [条件3デモ動画](https://waseda.box.com/s/07o83jqg69dkn6p9dhgd95twe4whz925) |
| 4 | 0.01 | 131 | 30 | [条件4デモ動画](https://waseda.box.com/s/8lx2g0xlujup4jwl3xk1y4qui5sl4bx0) |

[比較動画](https://waseda.box.com/s/p6n9tkek7unc1n8oreqxb2fkt35wyekr)

## 4.C Live streaming　
※デモ動画撮影用に原稿とは異なるシーケンスの結果を示す（実験結果の傾向は、原稿と同様のものである）

・１フレームあたりの点群の取得から生成までにかかる処理時間を考慮して，再生フレームレートを決める．(LiDARカメラでの取得フレームレートも同じに設定する)

・初期バッファサイズは５フレームとし，安定してバッファが枯渇しないようなデータサイズとなるvoxel sizeを選択する．


表2　パラメータ設定とデモ動画のリンク

| setting | voxel size(m) | initial buffer size(frames) | frame rate(fps) | demo video link |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 0.005 | 5 | 5 | [条件1デモ動画](https://waseda.box.com/s/zswfm4pbiqxnl69mawh6qdwrnzmxrc6u) |
| 2 | 0.007 | 5 | 10 | [条件2デモ動画](https://waseda.box.com/s/cgykdhppa0fxl7wuc9jkatx68q981b6k) |

[比較動画](https://waseda.box.com/s/jc6vvjr4w2vw7tzin1ca0s3h4lc8incy)
