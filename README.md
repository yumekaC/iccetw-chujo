# iccetw-chujo
## I. Demonstration of on-demand streaming
・Considering the rendering processing time per frame, we defined playing frame rate. By using frame-skip, point cloud streaming play at the same speed as capturing 30 fps.  

・Initial buffer size = all download frames - download frames during playing

Table1　Setting parameters and demo video links

| setting | voxel size(m) | initial buffer size(frames) | frame rate(fps) | demo video link |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 0 | 29 | 5 | [setting1 demo](https://waseda.box.com/s/j1j5r2h9y4u20q8sp215was04gda9xdw) |
| 2 | 0.003 | 65 | 10 | [setting2 demo](https://waseda.box.com/s/y94tg5xyte84mzaf1dywkod5tw12j7pa) |
| 3 | 0.005 | 79 | 15 | [setting3 demo](https://waseda.box.com/s/07o83jqg69dkn6p9dhgd95twe4whz925) |
| 4 | 0.01 | 131 | 30 | [setting4 demo](https://waseda.box.com/s/8lx2g0xlujup4jwl3xk1y4qui5sl4bx0) |

[demo comparison](https://waseda.box.com/s/p6n9tkek7unc1n8oreqxb2fkt35wyekr)

## II.  Demonstration of live streaming　
・Considering the processing time from capturing to creating ply data on the streaming server, we defined playing frame rate.

・Initial buffer size sets 5 frames.

・We set the voxel size not to occur freeze due to the lack of buffer.  

Table2　Setting parameters and demo video links

| setting | voxel size(m) | initial buffer size(frames) | frame rate(fps) | demo video link |
| :---: | :---: | :---: | :---: | :---: |
| A | 0.005 | 5 | 5 | [setting1 demo](https://waseda.box.com/s/zswfm4pbiqxnl69mawh6qdwrnzmxrc6u) |
| B | 0.007 | 5 | 10 | [setting2 demo](https://waseda.box.com/s/cgykdhppa0fxl7wuc9jkatx68q981b6k) |

[demo comparison](https://waseda.box.com/s/jc6vvjr4w2vw7tzin1ca0s3h4lc8incy)
