using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
public class Ondemand : MonoBehaviour
{
    public const int MAX_QUE = 295; // 【the number of frames】295/305/165
    public Queue<byte[]> que = new Queue<byte[]>(MAX_QUE);
    public bool runningFlag = true;
    public byte[] data = null;
    public int k = 0;
    public int i = 0;
    public int dequeue_wait_count = 0;
    public int enqueue_wait_count = 0;
    public float dl_time;

    public float dp_time;
    public float inv_time;
    public float del_time;
    public DateTime display_time1;
    public DateTime display_time2;
    public DateTime delete_time1;

    public string dlts;
    public string dists;
    public string invts;
    public string delts;

    public DateTime download1;
    public DateTime download2;

    public int skip_frame = 1;//【skip frame+1】1/2/3/6
    public int fps = 30;//【playing frame rate】30/15/10/5

    /*meta.json*/
    public int FRAME = 294;
    public string sequence = "greeting";
    public int cur_num = 0;
    public int initialBuffersize = 131;

    void Start()
    {
        DateTime startTime = DateTime.UtcNow;
        string start_ts = startTime.Year + "-" + startTime.Month + "-" + startTime.Day + "T" + startTime.Hour + ":" + startTime.Minute + ":" + startTime.Second + "." + startTime.Millisecond + "Z";
        dlts = start_ts;
        dists = start_ts;
        invts = start_ts;
        delts = start_ts;

        var produceTask = Task.Run(() => {
            DownloadHandler();
        });
        /*var postTask = Task.Run(() => {
            LogPost();
        });*/
        for (int b = 0; b < 720; b++)//40-10sec/720-180sec
        {
            //int mq = 131;//【initial buffer size】MAX_QUE or 131/79/65/29
            initialBuffersize = MAX_QUE;
            if (que.Count >= initialBuffersize)//mq
            {
                Debug.Log(que.Count);
                Thread.Sleep(250);
                DeleteMethod();
                break;
            }
            else
            {
                Thread.Sleep(250);
            }
        }
    }

    void DownloadHandler()
    {
        string voxel_size = "001";//【voxel size】"001"/"0005"/"0003"/"0"
        //string sequence = "greeting";//【sequence name】"greeting"/"teleconf3"/"bear"
        byte[] wwwdata = null;
        for (i = cur_num; i <= FRAME; i++)
        {
            int j = i * skip_frame;
            if (j > FRAME)
            {
                break;
            }
            
            /*IP address on apache server*/
            string url = "http://XXXX/ply_dataset/" + sequence + "/" + voxel_size + "/" + j + ".ply";
            while (true)
            {
                try
                {
                    DateTime dl_ts = DateTime.UtcNow;
                    dlts = dl_ts.Year + "-" + dl_ts.Month + "-" + dl_ts.Day + "T" + dl_ts.Hour + ":" + dl_ts.Minute + ":" + dl_ts.Second + "." + dl_ts.Millisecond + "Z";
                    download1 = DateTime.Now;
                    WebRequest req = WebRequest.Create(url);
                    using (WebResponse res = req.GetResponse())
                    {
                        using (Stream st = res.GetResponseStream())
                        {
                            wwwdata = MyClass.ReadBinaryData(st);
                            if (wwwdata != null)
                            {
                                download2 = DateTime.Now;
                                break;
                            }
                        }
                    }
                }
                catch (WebException ex)
                {
                    if (ex.Status == WebExceptionStatus.ProtocolError)
                    {
                        //Debug.Log(ex.Message);
                    }
                    else
                    {
                        //Debug.Log(ex.Message);
                    }
                }
            }
            // enqueue
            lock (que) // get exclusive lock
            {
                while (que.Count >= MAX_QUE)
                {
                    // wait enqueue not to exceed MAX_QUE
                    Debug.Log($"wait enqueue");
                    enqueue_wait_count++;
                    System.Threading.Monitor.Wait(que); // thread wait
                }
                que.Enqueue(wwwdata);
                System.Threading.Monitor.PulseAll(que); // thread restart
            } // release eclusive lock
            TimeSpan dl_timespan = download2 - download1;
            double dl_double = dl_timespan.TotalSeconds;
            dl_time = (float)dl_double;

        }
        runningFlag = false; // notify end enqueue
    }

    void RenderingController()
    {
        lock (que) // get exclusive lock
        {
            while (que.Count == 0 && runningFlag)
            {
                // wait during empty queue
                dequeue_wait_count++;
                System.Threading.Monitor.Wait(que); // thread wait
            }
            // dequeue
            if (que.Count > 0)
            {
                DateTime dis_ts = DateTime.UtcNow;
                dists = dis_ts.Year + "-" + dis_ts.Month + "-" + dis_ts.Day + "T" + dis_ts.Hour + ":" + dis_ts.Minute + ":" + dis_ts.Second + "." + dis_ts.Millisecond + "Z";
                display_time1 = DateTime.Now;
                k++;
                data = que.Dequeue();
                System.Threading.Monitor.PulseAll(que); // thread restart
            }

        } // release exclusive lock
        // data processing is after release lock
        if (data != null)
        {
            RenderingHandler();
            double in_sp = 1.0 / fps;
            float invoke_span = (float)in_sp;
            Invoke("DeleteMethod", invoke_span);//0.2/0.1//0.033f/0.067f/0.100f/0.200f
        }
    }
    void RenderingHandler()
    {
        Stream stream = new MemoryStream(data);
        var gameObject = new GameObject();
        gameObject.name = "frame" + k;

        var mesh = MyClass.ImportAsMesh(stream);
        var meshFilter = gameObject.AddComponent<MeshFilter>();
        meshFilter.sharedMesh = mesh;
        var meshRenderer = gameObject.AddComponent<MeshRenderer>();
        meshRenderer.sharedMaterial = MyClass.GetDefaultMaterial();

        gameObject.transform.position = new Vector3(0, 0, 0.75f);
        gameObject.transform.rotation = Quaternion.Euler(0, 0, 0);
        gameObject.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
        DateTime inv_ts = DateTime.UtcNow;
        invts = inv_ts.Year + "-" + inv_ts.Month + "-" + inv_ts.Day + "T" + inv_ts.Hour + ":" + inv_ts.Minute + ":" + inv_ts.Second + "." + inv_ts.Millisecond + "Z";
        display_time2 = DateTime.Now;
        TimeSpan display_ts = display_time2 - display_time1;
        double dp_double = display_ts.TotalSeconds;
        dp_time = (float)dp_double;
    }
    void DeleteMethod()
    {
        int r_FRAME = FRAME / skip_frame;
        if (k == 0)
        {
            RenderingController();

        }
        else if (k < r_FRAME)
        {
            DateTime del_ts = DateTime.UtcNow;
            delts = del_ts.Year + "-" + del_ts.Month + "-" + del_ts.Day + "T" + del_ts.Hour + ":" + del_ts.Minute + ":" + del_ts.Second + "." + del_ts.Millisecond + "Z";
            DateTime invoke_time1 = DateTime.Now;
            TimeSpan inv_ts = invoke_time1 - display_time2;
            double inv_double = inv_ts.TotalSeconds;
            inv_time = (float)inv_double;

            GameObject obj = GameObject.Find("frame" + k);
            Destroy(obj);
            delete_time1 = DateTime.Now;
            TimeSpan del_timespan = delete_time1 - invoke_time1;

            double del_double = del_timespan.TotalSeconds;
            del_time = (float)del_double;

            RenderingController();
        }
        else
        {
            DateTime invoke_time = DateTime.Now;
            TimeSpan inv_ts = invoke_time - display_time2;
            double inv_double = inv_ts.TotalSeconds;
            inv_time = (float)inv_double;

            GameObject obj = GameObject.Find("frame" + k);
            Destroy(obj);
            delete_time1 = DateTime.Now;
            TimeSpan del_timespan = delete_time1 - invoke_time;
            double del_double = del_timespan.TotalSeconds;
            del_time = (float)del_double;

            Debug.Log("Loop stop");
        }
    }
    /*void LogPost()
    {
        for (int m = 0; m < 500; m++)
        {
            DateTime dateTime = DateTime.UtcNow;
            string ts = dateTime.Year + "-" + dateTime.Month + "-" + dateTime.Day + "T" + dateTime.Hour + ":" + dateTime.Minute + ":" + dateTime.Second + "." + dateTime.Millisecond + "Z";

            int size = (int)MyClass.datasize;
            var display = new PosDisplayLog3
            {
                timestamp = dists,
                processing_time = dp_time
            };
            var invoke = new PosDisplayLog3
            {
                timestamp = invts,
                processing_time = inv_time
            };
            var delete = new PosDisplayLog3
            {
                timestamp = delts,
                processing_time = del_time
            };
            var detail = new PosDetailLog3
            {
                display_state = display,
                invoke_state = invoke,
                delete_state = delete
            };
            var myjson3 = new PosLog3
            {
                timestamp = ts,
                data_size = size,
                download_time = dl_time,
                buffer_size = que.Count,
                state_name = "add playout buffer",
                dltimestamp = dlts,
                dl_frame_num = i,
                dp_frame_num = k,
                detail_logs = detail
            };
            var jsonpost3 = new PostQue3
            {
                id = "id" + k,
                type = "log",
                timestamp = ts,
                pointcloud_name = i + ".ply",
                log = myjson3
            };
            string json = JsonUtility.ToJson(jsonpost3);
            var re = new Regex("_");
            string replace = re.Replace(json, " ", 5);
            //Debug.Log("replace:" + replace);
            byte[] data = Encoding.UTF8.GetBytes(replace);
            string REST_API = "/logger/v1/put/data";
            
            string url = "http://XXXX/" + REST_API;  //IP address on log server
            
            // create request
            WebRequest req = WebRequest.Create(url);
            req.Method = "POST";
            req.ContentType = "application/json";
            req.ContentLength = data.Length;

            // write down POST data
            Stream reqStream = req.GetRequestStream();
            reqStream.Write(data, 0, data.Length);
            reqStream.Close();
            Thread.Sleep(250);//250/550
        }
        Debug.Log("END");
    }*/
}
